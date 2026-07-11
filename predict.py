"""Phase 2: Calibrated Predictive Routing (RouteLLM Matrix-Factorization role).

One-shot router: predict P(need_remote) from cheap features BEFORE generating.
Combined with the cascade gate (verify.py) this yields "unified cascade routing":
the predictor can send an obviously-hard query straight to remote (skipping the
wasted local pass), while borderline queries still try local first.

This is a lightweight logistic stand-in with a real, trainable interface. To use
the full RouteLLM MF model, train it offline on preference data (Chatbot Arena)
and replace `PredictiveRouter.predict`. The output is calibrated the same way
(Isotonic/Platt) to keep ECE low.
"""
import math
import config
import calibrate

_HARD = {"reasoning", "math", "multi_step"}


def features(task, category):
    """Cheap, free features. Extend with embedding-based features at kickoff."""
    length = min(len(task) / 400.0, 1.0)      # normalized length
    hard = 1.0 if category in _HARD else 0.0
    return [1.0, length, hard]                 # [bias, len, is_hard]


class PredictiveRouter:
    def __init__(self, weights=None, cal=None):
        # hand-tuned prior: hard category dominates, longer = more likely remote
        self.w = weights or [-1.2, 1.5, 3.0]
        self.cal = cal or calibrate.IdentityCalibrator()

    def _raw(self, task, category):
        z = sum(wi * fi for wi, fi in zip(self.w, features(task, category)))
        return 1.0 / (1.0 + math.exp(-z))

    def predict(self, task, category):
        """Calibrated P(query needs the remote model)."""
        return self.cal.predict(self._raw(task, category))

    def fit(self, samples, lr=0.1, epochs=1500):
        """samples: list of (task, category, needed_remote 0/1). Trains logistic weights."""
        for _ in range(epochs):
            grad = [0.0, 0.0, 0.0]
            for task, cat, y in samples:
                f = features(task, cat)
                p = 1.0 / (1.0 + math.exp(-sum(wi * fi for wi, fi in zip(self.w, f))))
                for j in range(3):
                    grad[j] += (p - y) * f[j]
            n = max(1, len(samples))
            self.w = [wi - lr * g / n for wi, g in zip(self.w, grad)]
        return self


_ROUTER = PredictiveRouter()


def need_remote_prob(task, category):
    return _ROUTER.predict(task, category)


def should_skip_local(task, category):
    """One-shot decision: if the router is confident the query needs remote,
    skip the local attempt entirely (saves the wasted local pass / latency)."""
    return need_remote_prob(task, category) >= config.ROUTE_THRESHOLD
