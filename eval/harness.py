"""Calibration + threshold-tuning harness.

Pipeline:
  1. Run each labeled eval task -> collect (raw_confidence, correct) pairs.
  2. Fit Platt + Isotonic calibrators; report ECE/Brier before vs after.
  3. Save the best calibrator to ../calib.json (verify.py loads it via CALIB_PATH).
  4. Sweep CONFIDENCE_THRESHOLD -> minimum remote calls that hold an accuracy floor.
  5. Train the PredictiveRouter (needed_remote = local was wrong).

MOCK mode simulates a local model (overconfident raw signal) so the whole loop
runs offline with no GPU. At kickoff set MOCK=0: correctness comes from
accuracy_check(gold, real_local_answer) and raw from verify.judge_raw().

    python eval/harness.py            # run from repo root
"""
import json
import os
import re
import sys
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
import calibrate
import verify
import predict
import automix
from nodes import classify

TASKS = os.path.join(os.path.dirname(__file__), "tasks.jsonl")
CALIB_OUT = os.path.join(os.path.dirname(__file__), "..", "calib.json")
ACC_FLOOR = 0.80   # 7B local model realistic floor; saves ~40-60% remote tokens
random.seed(7)


def load():
    return [json.loads(l) for l in open(TASKS) if l.strip()]


def normalize(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def accuracy_check(gold, answer):
    """Correctness check used in real mode. Extend per task type at kickoff."""
    g, a = normalize(gold), normalize(answer)
    if not g:
        return None
    return g == a or g in a or a in g


# --- MOCK simulation of a local model (delete this branch at kickoff) ---
_P = {"easy": 0.90, "med": 0.72, "hard": 0.32}


def _mock_local(item):
    p = _P.get(item.get("difficulty", "med"), 0.6)
    correct = 1 if random.random() < p else 0
    raw = min(1.0, max(0.0, p + 0.22 + random.gauss(0, 0.07)))  # overconfident
    return correct, raw


def collect(items):
    rows = []
    for it in items:
        cat = it.get("category") or classify(it["task"])
        if config.MOCK:
            correct, raw = _mock_local(it)
        else:
            import providers
            ans, _, _ = providers.complete([{"role": "user", "content": it["task"]}], kind="local")
            correct = 1 if accuracy_check(it["gold"], ans) else 0
            raw = verify.judge_raw(cat, it["task"], ans)
        rows.append((it, cat, raw, correct))
    return rows


def fit_best(rows):
    raws = [r[2] for r in rows]
    labels = [r[3] for r in rows]
    before = calibrate.ece(raws, labels)
    iso = calibrate.IsotonicCalibrator().fit(raws, labels)
    plt = calibrate.PlattCalibrator().fit(raws, labels)
    e_iso = calibrate.ece([iso.predict(x) for x in raws], labels)
    e_plt = calibrate.ece([plt.predict(x) for x in raws], labels)
    best, name = (iso, "isotonic") if e_iso <= e_plt else (plt, "platt")
    return before, e_iso, e_plt, best, name, sum(labels) / len(labels)


def sweep(rows, cal):
    n = len(rows)
    best = None
    print(f"\nthreshold sweep (accuracy floor = {ACC_FLOOR}):")
    print("  thr   remote_calls   accuracy")
    for i in range(21):
        thr = i / 20
        remote = correct = 0
        for _, _, raw, corr in rows:
            if cal.predict(raw) >= thr:      # keep local
                correct += corr
            else:                             # escalate (remote assumed correct)
                remote += 1
                correct += 1
        acc = correct / n
        mark = ""
        if acc >= ACC_FLOOR and (best is None or remote < best[1]):
            best = (thr, remote, acc)
            mark = "  <-"
        if i % 2 == 0:
            print(f"  {thr:.2f}   {remote:6d}        {acc:.3f}{mark}")
    return best


def main():
    items = load()
    rows = collect(items)
    before, e_iso, e_plt, best_cal, name, local_acc = fit_best(rows)
    raws = [r[2] for r in rows]
    labels = [r[3] for r in rows]
    brier = calibrate.brier([best_cal.predict(x) for x in raws], labels)

    print(f"samples = {len(items)}   raw local accuracy = {local_acc:.3f}")
    print(f"ECE before = {before:.3f}   isotonic = {e_iso:.3f}   platt = {e_plt:.3f}")
    print(f"best calibrator = {name}   (Brier = {brier:.3f})")
    calibrate.save(best_cal, CALIB_OUT)
    print("saved -> calib.json  (set CALIB_PATH=calib.json to use it)")

    # Per-category breakdown
    from collections import defaultdict
    cat_stats = defaultdict(lambda: [0, 0])
    for _, cat, _, corr in rows:
        cat_stats[cat][0] += corr
        cat_stats[cat][1] += 1
    print("\nPer-category local accuracy:")
    for cat, (c, n) in sorted(cat_stats.items()):
        print(f"  {cat:<20s} {c}/{n} = {c/n:.2f}")

    # AutoMix POMDP gate: fit observation model, report cost-aware threshold + result
    amx = automix.AutoMixGate(automix.fit_obs_model(raws, labels),
                              config.AUTOMIX_RC, config.AUTOMIX_PENALTY, config.AUTOMIX_COST)
    automix.save(amx, os.path.join(os.path.dirname(__file__), "..", "automix.json"))
    a_remote = a_correct = 0
    for _, cat, raw, corr in rows:
        prior = 0.4 if cat in ("reasoning", "math", "multi_step") else 0.75
        accept, _ = amx.accept_local(prior, [raw])
        if accept:
            a_correct += corr
        else:
            a_remote += 1
            a_correct += 1
    print(f"\nAutoMix gate: belief_threshold={amx.belief_threshold():.2f}  "
          f"remote_calls={a_remote}/{len(rows)}  accuracy={a_correct/len(rows):.3f}  saved -> automix.json")

    best = sweep(rows, best_cal)
    if best:
        thr, rem, acc = best
        saved_pct = round((1 - rem / len(items)) * 100, 1)
        print(f"\nRECOMMEND CONFIDENCE_THRESHOLD = {thr:.2f}  ->  "
              f"remote_calls = {rem}/{len(items)}  accuracy = {acc:.3f}  "
              f"tokens_saved = {saved_pct}%")
    else:
        print("\nNo threshold holds the accuracy floor; consider lowering ACC_FLOOR.")

    samples = [(it["task"], cat, 0 if corr else 1) for it, cat, _, corr in
               [(r[0], r[1], r[2], r[3]) for r in rows]]
    pr = predict.PredictiveRouter().fit(samples)
    print(f"\nPredictiveRouter trained. weights = {[round(w, 2) for w in pr.w]}")


if __name__ == "__main__":
    main()
