"""Phase 3: Payload compression (LLMLingua-2) — cut input tokens on paid calls.

Only helps the score if the formula counts INPUT tokens. Uses Microsoft
LLMLingua-2 (bidirectional token-classification compressor) when installed;
otherwise a lightweight extractive fallback so the pipeline runs now.

The heavy model is lazy-loaded on first use (not at import) so `python run.py`
stays fast when compression is off or llmlingua isn't installed.

Returns (compressed_text, tokens_saved).
"""
import re
import config
import tokens as tok

_FILLER = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "of", "to", "in", "on", "at", "for", "and", "or", "that", "this",
    "please", "kindly", "just", "really", "very", "actually", "basically",
}

_LL = None
_LL_TRIED = False


def _get_ll():
    global _LL, _LL_TRIED
    if _LL_TRIED:
        return _LL
    _LL_TRIED = True
    try:
        from llmlingua import PromptCompressor
        _LL = PromptCompressor(
            model_name=config.LLMLINGUA_MODEL,
            use_llmlingua2=True,
            device_map=config.LLMLINGUA_DEVICE,
        )
    except Exception:
        _LL = None
    return _LL


def _fallback(prompt):
    words = re.findall(r"\w+|[^\w\s]", prompt)
    kept = [w for w in words if w.lower() not in _FILLER]
    return re.sub(r"\s+", " ", " ".join(kept)).strip()


def compress(prompt, rate=None):
    rate = config.COMPRESS_RATE if rate is None else rate
    original = tok.count(prompt)
    ll = _get_ll()
    if ll is not None:
        try:
            out = ll.compress_prompt(prompt, rate=rate, force_tokens=["\n", "?", ".", ":"])
            text = out.get("compressed_prompt", prompt)
        except Exception:
            text = _fallback(prompt)
    else:
        text = _fallback(prompt)
    saved = max(0, original - tok.count(text))
    return text, saved
