"""AutoMix POMDP-style gate.

Self-verification is a NOISY observation of the hidden state "is the local answer
correct?". Instead of thresholding a single raw score, we:
  1. start from a prior P(correct) (per category),
  2. Bayes-update a belief with each noisy self-verify observation (POMDP belief),
  3. decide by EXPECTED REWARD (cost-aware): accept local vs escalate.

ObsModel = the meta-verifier: how the self-verify score distributes when the
answer is actually correct vs incorrect (fit from labeled data). Escalation
happens only when the expected quality gain justifies the token cost.

Reference: AutoMix (self-verification + belief state + cost-aware policy).
"""
import json
import math


def _gauss(x, mu, sd):
    sd = max(sd, 1e-3)
    return math.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))


class ObsModel:
    """Likelihood of a self-verify score given correct / incorrect."""
    def __init__(self, mu_c=0.80, sd_c=0.15, mu_w=0.45, sd_w=0.20):
        self.mu_c, self.sd_c, self.mu_w, self.sd_w = mu_c, sd_c, mu_w, sd_w

    def lik(self, x, correct):
        if correct:
            return _gauss(x, self.mu_c, self.sd_c)
        return _gauss(x, self.mu_w, self.sd_w)

    def to_dict(self):
        return {"mu_c": self.mu_c, "sd_c": self.sd_c, "mu_w": self.mu_w, "sd_w": self.sd_w}


def fit_obs_model(raws, labels):
    c = [r for r, l in zip(raws, labels) if l]
    w = [r for r, l in zip(raws, labels) if not l]

    def ms(a, dm):
        if not a:
            return dm, 0.2
        m = sum(a) / len(a)
        v = sum((x - m) ** 2 for x in a) / max(1, len(a) - 1)
        return m, max(v ** 0.5, 0.05)

    mc, sc = ms(c, 0.8)
    mw, sw = ms(w, 0.45)
    return ObsModel(mc, sc, mw, sw)


class AutoMixGate:
    def __init__(self, obs, r_correct=1.0, penalty_wrong=-2.0, cost_remote=0.3):
        self.obs = obs
        self.rc = r_correct
        self.pw = penalty_wrong        # cost of accepting a WRONG local answer (drops below bar)
        self.cost = cost_remote        # token cost of escalating

    def update_belief(self, prior, observations):
        b = min(max(prior, 1e-4), 1 - 1e-4)
        for x in observations:
            l1 = self.obs.lik(x, True)
            l0 = self.obs.lik(x, False)
            b = (b * l1) / (b * l1 + (1 - b) * l0 + 1e-12)
        return b

    def ev_local(self, b):
        return b * self.rc + (1 - b) * self.pw

    def ev_remote(self):
        return self.rc - self.cost      # remote assumed ~correct, minus token cost

    def accept_local(self, prior, observations):
        b = self.update_belief(prior, observations)
        return (self.ev_local(b) >= self.ev_remote(), b)

    def belief_threshold(self):
        """Belief above which we keep local (derived from costs, not hand-set)."""
        denom = (self.rc - self.pw)
        return (self.rc - self.cost - self.pw) / denom if denom else 0.5

    def to_dict(self):
        return {"obs": self.obs.to_dict(), "rc": self.rc, "pw": self.pw, "cost": self.cost}


def save(gate, path):
    with open(path, "w") as f:
        json.dump(gate.to_dict(), f)


def load(path):
    try:
        with open(path) as f:
            d = json.load(f)
        o = d["obs"]
        return AutoMixGate(ObsModel(o["mu_c"], o["sd_c"], o["mu_w"], o["sd_w"]),
                           d["rc"], d["pw"], d["cost"])
    except Exception:
        return AutoMixGate(ObsModel())
