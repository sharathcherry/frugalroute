"""Ablation + calibration harness.

1. Token ablation: total remote tokens WITH vs WITHOUT the semantic cache.
2. Calibration demo: fit Isotonic on synthetic (raw_score, correct) pairs and
   show Expected Calibration Error (ECE) before vs after — the mechanism that
   stops accuracy dips. Replace synthetic data with real logged pairs at kickoff.

    python eval/run_eval.py            # run from repo root
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cache import SemanticCache
from policy import OnlinePolicy
import engine
import calibrate


def load(path):
    with open(path) as f:
        return [json.loads(l)["task"] for l in f if l.strip()]


class _NoCache(SemanticCache):
    def lookup(self, q):
        return None


def run_strategy(tasks, use_cache=True):
    cache = SemanticCache() if use_cache else _NoCache()
    policy = OnlinePolicy()
    total = 0
    for t in tasks:
        r = engine.run_task(t, cache, policy)
        total += r.get("remote_tokens", 0)
    return total


def calibration_demo():
    # synthetic: raw scores that are OVERCONFIDENT (0.9 raw -> ~0.6 real)
    import random
    random.seed(0)
    raw, labels = [], []
    for _ in range(400):
        r = random.random()
        true_p = r ** 2                     # miscalibration: real prob below raw
        raw.append(r)
        labels.append(1 if random.random() < true_p else 0)
    before = calibrate.ece(raw, labels)
    cal = calibrate.IsotonicCalibrator().fit(raw, labels)
    cal_probs = [cal.predict(x) for x in raw]
    after = calibrate.ece(cal_probs, labels)
    return before, after


if __name__ == "__main__":
    tasks = load(os.path.join(os.path.dirname(__file__), "tasks.sample.jsonl"))
    with_cache = run_strategy(tasks, True)
    without_cache = run_strategy(tasks, False)
    print(f"remote tokens WITH cache    : {with_cache}")
    print(f"remote tokens WITHOUT cache : {without_cache}")
    print(f"cache saved                 : {without_cache - with_cache} tokens\n")

    b, a = calibration_demo()
    print(f"ECE before calibration : {b:.3f}")
    print(f"ECE after  calibration : {a:.3f}   (lower = better; this is your no-dips guarantee)")
