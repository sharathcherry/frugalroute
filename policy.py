"""Online routing policy — the third token-saver.

Learns per task-category whether the local model is trustworthy, so we stop
paying to escalate categories the local model reliably nails, and skip the wasted
local pass on categories it reliably fails. Simple running-accuracy bandit; extend
to UCB/Thompson if useful.
"""
from collections import defaultdict


class OnlinePolicy:
    def __init__(self, warmup=3, trust=0.8):
        self.stats = defaultdict(lambda: [0, 0])  # category -> [attempts, successes]
        self.warmup = warmup
        self.trust = trust

    def _rate(self, category):
        a, s = self.stats[category]
        return (s / a) if a else 1.0

    def should_try_local(self, category):
        a, _ = self.stats[category]
        if a < self.warmup:
            return True  # explore during warmup
        return self._rate(category) >= 0.34

    def prefer_remote(self, category):
        """Local reliably fails this category -> skip local, go straight to remote."""
        a, _ = self.stats[category]
        return a >= self.warmup and self._rate(category) < 0.34

    def update(self, category, correct):
        self.stats[category][0] += 1
        if correct:
            self.stats[category][1] += 1
