"""Confidence calibration — the mechanism that prevents accuracy dips.

Raw confidence scores (from a local model self-rating or a judge) are usually
miscalibrated: a "0.9" may only be correct 60% of the time. We map raw scores to
TRUE empirical probabilities so the routing threshold behaves predictably.

Implements (pure Python, no sklearn required):
  - PlattCalibrator      : logistic (sigmoid) fit over raw scores. Data-efficient.
  - IsotonicCalibrator   : non-parametric monotone fit (PAVA). Better with more data.
  - ece(), brier()       : calibration quality metrics.

Usage:
    cal = IsotonicCalibrator().fit(raw_scores, correct_labels)
    p = cal.predict(raw_score)      # calibrated P(correct)
    cal.save("calib.json"); IsotonicCalibrator.load("calib.json")

Reference: FrugalGPT stop-judger + Platt scaling / Isotonic regression (ECE).
"""
import json
import math


def _sigmoid(z):
    if z < -60:
        return 0.0
    if z > 60:
        return 1.0
    return 1.0 / (1.0 + math.exp(-z))


class IdentityCalibrator:
    """Default: pass the raw score through unchanged (used before any fit)."""
    kind = "identity"

    def fit(self, scores, labels):
        return self

    def predict(self, score):
        return max(0.0, min(1.0, float(score)))

    def to_dict(self):
        return {"kind": self.kind}


class PlattCalibrator:
    """Fit p = sigmoid(a*score + b) via gradient descent on binary cross-entropy."""
    kind = "platt"

    def __init__(self, a=1.0, b=0.0):
        self.a = a
        self.b = b

    def fit(self, scores, labels, lr=0.1, epochs=2000):
        n = len(scores)
        if n == 0:
            return self
        for _ in range(epochs):
            ga = gb = 0.0
            for x, y in zip(scores, labels):
                p = _sigmoid(self.a * x + self.b)
                err = p - y
                ga += err * x
                gb += err
            self.a -= lr * ga / n
            self.b -= lr * gb / n
        return self

    def predict(self, score):
        return _sigmoid(self.a * score + self.b)

    def to_dict(self):
        return {"kind": self.kind, "a": self.a, "b": self.b}


class IsotonicCalibrator:
    """Pool-Adjacent-Violators (PAVA): piecewise-constant monotone increasing fit."""
    kind = "isotonic"

    def __init__(self, xs=None, ys=None):
        self.xs = xs or []   # sorted score thresholds
        self.ys = ys or []   # calibrated prob per threshold

    def fit(self, scores, labels):
        pairs = sorted(zip(scores, labels), key=lambda t: t[0])
        if not pairs:
            return self
        xs = [p[0] for p in pairs]
        # blocks: [value, weight]
        blocks = [[float(y), 1.0] for _, y in pairs]
        i = 0
        while i < len(blocks) - 1:
            if blocks[i][0] > blocks[i + 1][0]:  # violation -> pool
                v = (blocks[i][0] * blocks[i][1] + blocks[i + 1][0] * blocks[i + 1][1])
                w = blocks[i][1] + blocks[i + 1][1]
                blocks[i] = [v / w, w]
                del blocks[i + 1]
                if i > 0:
                    i -= 1
            else:
                i += 1
        # expand pooled values back to each x
        ys, idx = [], 0
        for b in blocks:
            for _ in range(int(b[1])):
                ys.append(b[0])
                idx += 1
        self.xs, self.ys = xs, ys
        return self

    def predict(self, score):
        if not self.xs:
            return max(0.0, min(1.0, float(score)))
        if score <= self.xs[0]:
            return self.ys[0]
        if score >= self.xs[-1]:
            return self.ys[-1]
        # linear interpolation between neighbours
        lo = 0
        for i in range(len(self.xs) - 1):
            if self.xs[i] <= score <= self.xs[i + 1]:
                lo = i
                break
        x0, x1 = self.xs[lo], self.xs[lo + 1]
        y0, y1 = self.ys[lo], self.ys[lo + 1]
        if x1 == x0:
            return y0
        return y0 + (y1 - y0) * (score - x0) / (x1 - x0)

    def to_dict(self):
        return {"kind": self.kind, "xs": self.xs, "ys": self.ys}


def from_dict(d):
    k = d.get("kind")
    if k == "platt":
        return PlattCalibrator(d["a"], d["b"])
    if k == "isotonic":
        return IsotonicCalibrator(d["xs"], d["ys"])
    return IdentityCalibrator()


def save(cal, path):
    with open(path, "w") as f:
        json.dump(cal.to_dict(), f)


def load(path):
    try:
        with open(path) as f:
            return from_dict(json.load(f))
    except Exception:
        return IdentityCalibrator()


# ---- calibration quality metrics ----
def brier(probs, labels):
    """Mean squared error between predicted prob and outcome. Lower = better."""
    if not probs:
        return 0.0
    return sum((p - y) ** 2 for p, y in zip(probs, labels)) / len(probs)


def ece(probs, labels, bins=10):
    """Expected Calibration Error. 0 = perfectly calibrated."""
    if not probs:
        return 0.0
    total = len(probs)
    err = 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        idx = [i for i, p in enumerate(probs) if (lo < p <= hi) or (b == 0 and p == 0)]
        if not idx:
            continue
        conf = sum(probs[i] for i in idx) / len(idx)
        acc = sum(labels[i] for i in idx) / len(idx)
        err += (len(idx) / total) * abs(acc - conf)
    return err
