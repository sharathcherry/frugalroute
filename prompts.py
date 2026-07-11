"""Prefix-stable prompt construction for LOCAL inference.

RadixAttention (SGLang) and Automatic Prefix Caching (vLLM) cache the KV of shared
prompt PREFIXES in a radix tree keyed by the exact token sequence. Cache hits only
happen when every local call shares a byte-identical prefix.

So: put ALL static content (system instructions + few-shot) FIRST and IDENTICAL,
and vary only the trailing user task. A single differing whitespace changes the
cache key and misses — keep SYSTEM_PREFIX and FEWSHOT constant (never f-string
per request).

Effect: near-zero re-processing of the shared prefix -> lower time-to-first-token
and higher local throughput -> the local model clears more tasks within any
per-task time budget -> fewer paid escalations.
"""

# Keep EXACTLY constant across all local calls.
SYSTEM_PREFIX = (
    "You are a concise task solver. Answer correctly and briefly. "
    "For classification reply with the single label only. "
    "For extraction reply with the values only, comma-separated. "
    "For numeric questions reply with the number only."
)

# Optional fixed few-shot block — also part of the cached prefix. Keep constant.
FEWSHOT = [
    {"role": "user", "content": "Classify sentiment: 'great product'"},
    {"role": "assistant", "content": "positive"},
    {"role": "user", "content": "Calculate the sum of 2 and 3."},
    {"role": "assistant", "content": "5"},
]


def build_local_messages(task, use_fewshot=True):
    """Static prefix first (cacheable), variable task last."""
    msgs = [{"role": "system", "content": SYSTEM_PREFIX}]
    if use_fewshot:
        msgs = msgs + FEWSHOT
    msgs.append({"role": "user", "content": task})
    return msgs


def prefix_signature(use_fewshot=True):
    """The constant prefix (everything except the trailing task) — used to assert
    prefix stability so the radix cache actually hits."""
    import json
    pre = [{"role": "system", "content": SYSTEM_PREFIX}] + (FEWSHOT if use_fewshot else [])
    return json.dumps(pre, sort_keys=True)
