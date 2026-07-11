"""Token counting. Uses tiktoken when available, else a rough fallback so the
skeleton runs with no dependencies."""
try:
    import tiktoken
    _enc = tiktoken.get_encoding("cl100k_base")

    def count(text):
        return len(_enc.encode(text or ""))
except Exception:
    def count(text):
        return max(1, len(text or "") // 4)
