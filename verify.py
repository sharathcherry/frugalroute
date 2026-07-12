"""Confidence gate — two selectable modes (config.GATE_MODE):

  "calibrated" : FrugalGPT stop-judger + Platt/Isotonic calibration; accept local
                 if calibrated P(correct) >= CONFIDENCE_THRESHOLD.
  "automix"    : AutoMix POMDP gate; treat self-verification as a noisy observation,
                 maintain a Bayesian belief over correctness, escalate by
                 expected-reward (cost-aware) decision.

Both share judge_raw() (the free/local self-verify signal).
"""
import config
import calibrate
import automix

_HARD = {"reasoning", "math", "multi_step"}

_CAL = calibrate.load(config.CALIB_PATH) if config.CALIB_PATH else calibrate.IdentityCalibrator()
_AMX = (automix.load(config.AUTOMIX_PATH) if config.AUTOMIX_PATH
        else automix.AutoMixGate(automix.ObsModel(), config.AUTOMIX_RC,
                                 config.AUTOMIX_PENALTY, config.AUTOMIX_COST))


def set_calibrator(c):
    global _CAL
    _CAL = c


def set_automix(g):
    global _AMX
    _AMX = g


def judge_raw(category, task, answer):
    """Free/local self-verify signal in [0,1] — the raw confidence the gate calibrates.

    MOCK: heuristic. REAL: the local model grades its own answer (a free local call),
    per config.JUDGE_MODE:
      - "selfrate" (default): ask the local model to rate correctness 0..1
      - "heuristic": flat 0.5 (old stub — disables real routing)
    """
    if config.MOCK:
        base = 0.9 if category not in _HARD else 0.4
        if not answer or len(answer) < 5:
            base = 0.1
        return base

    if config.JUDGE_MODE == "heuristic" or not answer:
        return 0.5

    # self-rating: a second, FREE local call that scores the candidate answer
    import re
    import providers
    grade_prompt = (
        f"Question:\n{task}\n\nProposed answer:\n{answer}\n\n"
        "Rate how likely the proposed answer is correct AND complete. "
        "Respond with ONLY a number between 0 and 1 (e.g. 0.82)."
    )
    try:
        text, _, _ = providers.complete(
            [{"role": "user", "content": grade_prompt}], kind="local", max_tokens=8)
        m = re.search(r"(?:0(?:\.\d+)?|1(?:\.0+)?)", text)
        v = float(m.group()) if m else 0.5
        return max(0.0, min(1.0, v))
    except Exception:
        return 0.5


def confidence(category, task, answer):
    """Calibrated P(correct) — used by the 'calibrated' gate mode and for reporting."""
    return _CAL.predict(judge_raw(category, task, answer))


def is_confident(conf):
    return conf >= config.CONFIDENCE_THRESHOLD


def _prior(category):
    return 0.4 if category in _HARD else 0.75


def accept_local(category, task, answer):
    """Return (accept_local: bool, value). value = belief (automix) or calibrated conf."""
    if config.GATE_MODE == "automix":
        raw = judge_raw(category, task, answer)
        obs = [raw] * max(1, config.AUTOMIX_SAMPLES)   # k noisy self-verify observations
        accept, belief = _AMX.accept_local(_prior(category), obs)
        return accept, belief
    conf = confidence(category, task, answer)
    return is_confident(conf), conf
