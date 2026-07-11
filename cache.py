"""Semantic cache — first token-saver. A cache hit costs ZERO tokens.

Real backend: Qdrant vector DB + fastembed (BGE) embeddings — true semantic match,
optionally persistent or on a running Qdrant server. Falls back to difflib string
similarity (stdlib) when qdrant-client / fastembed aren't installed, so the repo
still runs with no dependencies.

Backend selection (config.CACHE_BACKEND): "auto" (default) | "qdrant" | "difflib".
Qdrant location: QDRANT_URL (server) -> QDRANT_PATH (persistent local) -> in-memory.
"""
import difflib
import uuid
import config

# ---------- embedding backend (swappable; inject a fake for tests) ----------
_EMBEDDER = "unset"


def set_embedder(fn):
    """fn(texts: list[str]) -> list[list[float]]. Override the default fastembed."""
    global _EMBEDDER
    _EMBEDDER = fn


def _embedder():
    global _EMBEDDER
    if _EMBEDDER != "unset":
        return _EMBEDDER
    try:
        from fastembed import TextEmbedding
        _m = TextEmbedding(config.EMBED_MODEL)
        _EMBEDDER = lambda texts: [list(v) for v in _m.embed(list(texts))]
    except Exception:
        _EMBEDDER = None
    return _EMBEDDER


def _embed_one(text):
    fn = _embedder()
    return fn([text])[0] if fn else None


# ---------- backends ----------
class _DifflibBackend:
    name = "difflib"

    def __init__(self):
        self._items = []  # [(query, answer)]

    def lookup(self, q):
        best, bs = None, 0.0
        for query, ans in self._items:
            r = difflib.SequenceMatcher(None, q, query).ratio()
            if r > bs:
                best, bs = ans, r
        return best if best is not None and bs >= config.CACHE_SIM_THRESHOLD else None

    def add(self, q, a):
        self._items.append((q, a))


class _QdrantBackend:
    name = "qdrant"

    def __init__(self):
        from qdrant_client import QdrantClient
        from qdrant_client import models as qm
        self.qm = qm
        if config.QDRANT_URL:
            self.client = QdrantClient(url=config.QDRANT_URL)
        elif config.QDRANT_PATH:
            self.client = QdrantClient(path=config.QDRANT_PATH)
        else:
            self.client = QdrantClient(location=":memory:")
        self.col = config.QDRANT_COLLECTION
        self._ensure()

    def _ensure(self):
        try:
            self.client.get_collection(self.col)
        except Exception:
            self.client.create_collection(
                self.col,
                vectors_config=self.qm.VectorParams(
                    size=config.EMBED_DIM, distance=self.qm.Distance.COSINE))

    def lookup(self, q):
        v = _embed_one(q)
        if v is None:
            return None
        try:
            hits = self.client.query_points(self.col, query=v, limit=1).points  # qdrant-client >=1.12
        except AttributeError:
            hits = self.client.search(self.col, query_vector=v, limit=1)        # older versions
        if hits and hits[0].score >= config.CACHE_SIM_THRESHOLD:
            return hits[0].payload.get("answer")
        return None

    def add(self, q, a):
        v = _embed_one(q)
        if v is None:
            return
        self.client.upsert(self.col, points=[self.qm.PointStruct(
            id=str(uuid.uuid4()), vector=v, payload={"query": q, "answer": a})])


def _make_backend():
    want = getattr(config, "CACHE_BACKEND", "auto")
    if want != "difflib":
        try:
            import qdrant_client  # noqa: F401
            if _embedder() is not None:
                return _QdrantBackend()
        except Exception:
            pass
    return _DifflibBackend()


class SemanticCache:
    """Public API unchanged: lookup(query)->answer|None, add(query, answer)."""

    def __init__(self):
        self._backend = _make_backend()

    @property
    def backend(self):
        return self._backend.name

    def lookup(self, query):
        return self._backend.lookup(query)

    def add(self, query, answer):
        self._backend.add(query, answer)
