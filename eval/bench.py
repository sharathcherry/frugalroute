"""Local-model benchmark — pick the best small model for the scoring environment.

For each candidate it reports accuracy (vs gold), avg latency, size, and the
implied remote-escalation rate (1 - accuracy). Recommends the model with the
highest accuracy that fits a latency budget, preferring smaller models (they fit
the standardized env and load faster).

MOCK mode simulates per-size behavior so it runs offline with no GPU. At kickoff
set MOCK=0 and point LOCAL_BASE_URL at each running model (edit CANDIDATES).

    python eval/bench.py
"""
import json
import os
import re
import sys
import time
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

TASKS = os.path.join(os.path.dirname(__file__), "tasks.jsonl")
LATENCY_BUDGET_MS = float(os.getenv("LATENCY_BUDGET_MS", "800"))
random.seed(11)

# (display name, model id served on LOCAL_BASE_URL). Edit for your endpoints.
CANDIDATES = [
    ("qwen2.5-0.5b", "qwen2.5:0.5b-instruct"),
    ("llama3.2-1b", "llama3.2:1b-instruct"),
    ("gemma2-2b", "gemma2:2b-instruct"),
    ("qwen2.5-3b", "qwen2.5:3b-instruct"),
    ("phi3.5-mini", "phi3.5:3.8b-instruct"),
    ("qwen2.5-7b", "qwen2.5:7b-instruct"),
]

# MOCK profiles: accuracy ceiling by size (B params) and per-difficulty penalty.
_CAP = {0.5: 0.62, 1: 0.70, 2: 0.78, 3: 0.83, 3.8: 0.86, 7: 0.90}
_PEN = {"easy": 0.0, "med": 0.10, "hard": 0.30}


def load():
    return [json.loads(l) for l in open(TASKS) if l.strip()]


def size_of(model):
    m = re.search(r"(\d+\.?\d*)\s*b", model.lower())
    return float(m.group(1)) if m else 3.0


def _cap(size):
    # nearest known cap
    return _CAP[min(_CAP, key=lambda s: abs(s - size))]


def normalize(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def accuracy_check(gold, answer):
    g, a = normalize(gold), normalize(answer)
    if not g:
        return None
    return g == a or g in a or a in g


def eval_mock(size, items):
    cap = _cap(size)
    correct = 0
    for it in items:
        p = max(0.0, cap - _PEN.get(it.get("difficulty", "med"), 0.15))
        correct += 1 if random.random() < p else 0
    latency = 40 * size + random.uniform(-15, 25)   # ms, grows with size
    return correct / len(items), max(20.0, latency)


def eval_real(model, items):
    import providers
    correct, total_ms = 0, 0.0
    for it in items:
        t0 = time.perf_counter()
        ans, _, _ = providers.complete([{"role": "user", "content": it["task"]}],
                                       kind="local", model=model)
        total_ms += (time.perf_counter() - t0) * 1000
        if accuracy_check(it["gold"], ans):
            correct += 1
    return correct / len(items), total_ms / len(items)


def main():
    items = load()
    rows = []
    for name, model in CANDIDATES:
        size = size_of(model)
        acc, lat = eval_mock(size, items) if config.MOCK else eval_real(model, items)
        rows.append((name, size, acc, lat))

    rows.sort(key=lambda r: (-r[2], r[1]))   # accuracy desc, then smaller size
    print(f"# local-model benchmark  (mode={'MOCK' if config.MOCK else 'REAL'}, "
          f"{len(items)} tasks, latency budget={LATENCY_BUDGET_MS:.0f}ms)\n")
    print(f"  {'model':14} {'size(B)':>7} {'accuracy':>9} {'latency_ms':>11} {'escalate%':>10}")
    for name, size, acc, lat in rows:
        print(f"  {name:14} {size:7.1f} {acc:9.3f} {lat:11.0f} {100*(1-acc):10.1f}")

    fit = [r for r in rows if r[3] <= LATENCY_BUDGET_MS]
    pool = fit or rows
    best = max(pool, key=lambda r: (r[2], -r[1]))
    print(f"\nRECOMMEND local model = {best[0]}  "
          f"(size={best[1]}B, accuracy={best[2]:.3f}, latency={best[3]:.0f}ms)")
    print("Rationale: highest accuracy within latency budget; smaller wins ties "
          "(fits the standardized env + loads faster).")


if __name__ == "__main__":
    main()
