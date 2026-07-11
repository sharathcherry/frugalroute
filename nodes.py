"""Node functions over a shared state dict. Used by BOTH the LangGraph graph
(graph.py) and the dependency-free engine (engine.py).

Pipeline (blueprint: Edge-Cloud Pareto-Router):
  ingest -> triage(Phase1) -> cache -> route(Phase2) -> local -> gate -> remote(Phase3) -> account
"""
import re
import providers
import verify
import triage as triage_mod
import predict
import compress
import prompts
import config

CATEGORY_KEYWORDS = {
    "math": ["calculate", "sum of", "product of", "solve", "equation", "how many", "multiply"],
    "reasoning": ["why", "explain", "reason", "deduce", "step by step"],
    "classification": ["classify", "category", "label", "sentiment"],
    "extraction": ["extract", "list all", "find the", "pull out"],
    "summarization": ["summarize", "tl;dr", "summary"],
}

# Local max tokens cap — prevents runaway generation over the network
LOCAL_MAX_TOKENS = int(__import__("os").getenv("LOCAL_MAX_TOKENS", "400"))


def classify(task):
    t = task.lower()
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(k in t for k in kws):
            return cat
    return "qa"


def _normalize(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def accuracy_check(gold, answer):
    """Correctness check. Extend per task type once the real format is known.
    Returns True/False/None (None = no gold label available).
    """
    g, a = _normalize(gold), _normalize(answer)
    if not g:
        return None          # no gold label — cannot score
    return g == a or g in a or a in g


# ---------------------------------------------------------------------------
# Node functions
# ---------------------------------------------------------------------------

def ingest(state):
    state["category"] = classify(state["task"])
    return state


def triage_node(state):
    d = triage_mod.triage(state["task"])
    if d == "block":
        state.update(answer="[blocked by safety route]", source="triage_block",
                     remote_tokens=0, done=True)
    elif d == "local":
        state["force_local"] = True          # easy cluster -> keep local, skip predictor
        state["source"] = "triage_local"
    return state


def cache_lookup(state, cache):
    hit = cache.lookup(state["task"])
    if hit is not None:
        state.update(answer=hit, source="cache", remote_tokens=0, done=True)
    return state


def route(state):
    """Phase 2: one-shot predictive routing. May skip the local pass for
    obviously-hard queries (unless triage already forced local)."""
    if state.get("force_local"):
        state["route_p"] = 0.0
        return state
    p = predict.need_remote_prob(state["task"], state["category"])
    state["route_p"] = round(p, 2)
    if p >= config.ROUTE_THRESHOLD:
        state["skip_local"] = True
    return state


def local(state, policy):
    cat = state["category"]
    if state.get("skip_local") or policy.prefer_remote(cat):
        state["skip_local"] = True
        return state
    msgs = prompts.build_local_messages(state["task"])   # prefix-stable for RadixAttention/APC
    text, _, _ = providers.complete(msgs, kind="local", max_tokens=LOCAL_MAX_TOKENS)
    state.update(candidate=text, source="local", remote_tokens=0)
    return state


def gate(state):
    """Phase 2 cascade: accept local only if CALIBRATED confidence clears the bar."""
    if state.get("skip_local"):
        state["confident"] = False
        return state
    accept, val = verify.accept_local(state["category"], state["task"], state.get("candidate", ""))
    state["confidence"] = round(val, 2)     # calibrated conf OR automix belief
    state["confident"] = accept
    if accept:
        state.update(answer=state["candidate"], done=True)
    return state


def remote(state):
    """Phase 3: compress the payload, then call the paid model."""
    prompt = state["task"]
    saved = 0
    if config.COMPRESS:
        prompt, saved = compress.compress(prompt)
    state["tokens_saved"] = state.get("tokens_saved", 0) + saved
    msgs = [{"role": "user", "content": prompt}]
    text, pt, ct = providers.complete(msgs, kind="remote")
    state.update(answer=text, source="remote", remote_tokens=pt + ct, done=True)
    return state


def account(state, cache, policy):
    """Post-task accounting: update cache + policy + log calibration signal."""
    cache.add(state["task"], state.get("answer", ""))

    went_local = state.get("source") in ("local", "triage_local")
    gold = state.get("gold")          # populated if the eval harness injected a label
    answer = state.get("answer", "")

    if gold is not None:
        correct = bool(accuracy_check(gold, answer))
    else:
        # No label — assume correct (leaderboard tasks don't expose gold at runtime)
        correct = True

    # Log (raw_conf, correct) for offline calibrator fitting (eval/harness.py)
    raw_conf = state.get("confidence")
    if raw_conf is not None and gold is not None:
        _append_calib_log(state.get("id", ""), raw_conf, int(correct))

    policy.update(state["category"], correct if went_local else True)
    return state


# ---------------------------------------------------------------------------
# Calibration data logger — appends to calib_log.jsonl for offline fitting
# ---------------------------------------------------------------------------
_CALIB_LOG = __import__("os").path.join(
    __import__("os").path.dirname(__import__("os").path.abspath(__file__)),
    "calib_log.jsonl"
)


def _append_calib_log(task_id, raw_conf, correct):
    try:
        with open(_CALIB_LOG, "a", encoding="utf-8") as f:
            f.write(__import__("json").dumps(
                {"id": task_id, "raw": raw_conf, "correct": correct}
            ) + "\n")
    except Exception:
        pass
