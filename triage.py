"""Phase 1: Semantic Triage — zero-cost filtration (Aurelio Semantic-Router idea).

Cheapest possible layer: embed the query and, if it lands inside a predefined
"easy" or "unsafe" cluster, decide immediately WITHOUT any generative call.
  - easy clusters (greeting/simple format)  -> keep LOCAL (free)
  - safety cluster (jailbreak/PII)           -> BLOCK

Uses fastembed cosine if installed; falls back to keyword matching so it runs now.
Returns: "local" | "block" | None (None = pass through to routing).
"""
import re
import config

# Static route utterances. Extend with real examples at kickoff.
_EASY = ["hello", "hi", "thanks", "thank you", "good morning", "how are you",
         "format this", "uppercase", "lowercase", "reverse the text"]
_BLOCK = ["ignore previous instructions", "jailbreak", "system prompt",
          "bypass safety", "leak your prompt"]

try:
    from fastembed import TextEmbedding  # optional
    _emb = TextEmbedding("BAAI/bge-small-en-v1.5")
    _HAVE_EMB = True
except Exception:
    _HAVE_EMB = False


def _cos(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb + 1e-9)


if _HAVE_EMB:
    _EASY_V = list(_emb.embed(_EASY))
    _BLOCK_V = list(_emb.embed(_BLOCK))

    def _hit(task, vecs, radius=0.75):
        q = list(_emb.embed([task]))[0]
        return any(_cos(q, v) >= radius for v in vecs)
else:
    def _hit(task, phrases, radius=None):
        # Match only the CONTIGUOUS phrase (with word boundaries). This avoids
        # false positives where the words merely appear scattered in the text —
        # e.g. code or docs that discuss a "system prompt" shouldn't be blocked.
        low = task.lower()
        return any(re.search(r"\b" + re.escape(p) + r"\b", low) for p in phrases)


def triage(task):
    block_ref = _BLOCK_V if _HAVE_EMB else _BLOCK
    easy_ref = _EASY_V if _HAVE_EMB else _EASY
    if _hit(task, block_ref):
        return "block"
    if _hit(task, easy_ref):
        return "local"
    return None
