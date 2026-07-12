"""FrugalRoute interactive playground — FastAPI backend.

Serves the compiled React frontend (frontend/dist) and exposes the routing
API at /api/route. All non-API paths are forwarded to index.html so that
TanStack Router can handle client-side navigation.

    pip install fastapi uvicorn
    uvicorn server:app --host 0.0.0.0 --port 8000
    # open http://localhost:8000
"""
import os
import sys
import time
from pathlib import Path

# Windows consoles default to cp1252; model answers can contain unicode (—, °, emoji).
# Force UTF-8 so debug prints can never crash a request with UnicodeEncodeError.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from cache import SemanticCache
from policy import OnlinePolicy
from run import _build_runner
import config

app = FastAPI(title="FrugalRoute Playground")

# Allow Vite dev-server (port 5173) to call the backend during development
_allow = os.getenv("ALLOW_ORIGINS", "*")
_allow_list = [o.strip() for o in _allow.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allow_list,
    allow_credentials=(_allow != "*"),
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── routing engine ────────────────────────────────────────────────────────────
_CACHE = SemanticCache()
_POLICY = OnlinePolicy()
_ENGINE, _RUN = _build_runner(_CACHE, _POLICY)

# session tally (for the live savings counter)
_STATE = {"queries": 0, "remote_tokens": 0, "free": 0}

# ── static assets ─────────────────────────────────────────────────────────────
_DIST = Path(__file__).parent / "frontend" / "dist"
_DIST_ASSETS = _DIST / "assets"

if _DIST.exists():
    # Serve /assets/* directly
    if _DIST_ASSETS.exists():
        app.mount("/assets", StaticFiles(directory=str(_DIST_ASSETS)), name="assets")
else:
    print("[WARNING] frontend/dist not found -- run `npm run build` inside frontend/")


# ── API routes ────────────────────────────────────────────────────────────────

class Query(BaseModel):
    task: str


import random
import re as _re

# Fallback pool — used if the local model is slow/unavailable. Sampled randomly
# so suggestions still vary between loads even without the model.
SUGGEST_POOL = [
    "What is the current price of AMD stock?",
    "Translate 'Good morning, how are you?' to French.",
    "What is 47 times 89?",
    "Summarize what photosynthesis is in one sentence.",
    "Who wrote the novel 1984?",
    "What is the capital of Australia?",
    "Extract the total from: 'Total due: $1,240.55'",
    "What's the weather in Tokyo right now?",
    "Explain in one line why the sky is blue.",
    "Classify the sentiment: 'this product is amazing'",
    "What is the square root of 2025?",
    "Translate 'thank you very much' to Spanish.",
    "What is the current price of NVDA stock?",
    "Give a one-sentence summary of how vaccines work.",
    "Who painted the Mona Lisa?",
]


def _clean_suggestion(line: str) -> str:
    line = line.strip()
    line = _re.sub(r"^\s*(?:\d+[\.\)]|[-*•])\s*", "", line)  # strip numbering/bullets
    line = line.strip(' "\'`')
    return line


@app.get("/api/suggestions")
def suggestions(n: int = 4):
    """Dynamically generated starter prompts. Primary: the FREE local model
    generates varied examples; fallback: a random sample of the curated pool."""
    if not config.MOCK:
        try:
            import providers
            prompt = (
                f"Generate exactly {n} short, varied example questions a user could ask an AI "
                "assistant. Use a different category for each: one math problem, one translation "
                "request, one real-time lookup (a stock price or the weather), and one general "
                "knowledge or summarization question. Output ONLY the questions, one per line, no "
                "numbering, no extra text. Keep each under 12 words."
            )
            text, _, _ = providers.complete(
                [{"role": "user", "content": prompt}], kind="local",
                max_tokens=160, temperature=0.9)
            picks = [c for c in (_clean_suggestion(l) for l in text.splitlines())
                     if len(c) >= 8 and len(c) <= 120]
            # de-dup preserving order
            seen, out = set(), []
            for p in picks:
                k = p.lower()
                if k not in seen:
                    seen.add(k); out.append(p)
            if len(out) >= n:
                return {"suggestions": out[:n], "source": "model"}
        except Exception:
            pass
    return {"suggestions": random.sample(SUGGEST_POOL, min(n, len(SUGGEST_POOL))),
            "source": "pool"}


def _ollama_base():
    # LOCAL_BASE_URL is the OpenAI-compat endpoint (…/v1); Ollama's native API is at the host root.
    return config.LOCAL_BASE_URL.rsplit("/v1", 1)[0].rstrip("/")


@app.get("/api/models")
def list_models():
    """Detect the LOCAL models installed in Ollama and flag which fit this GPU."""
    import json as _json
    import urllib.request
    import providers
    try:
        import hwselect
        vram = hwselect.total_vram_mb()
        reserve = hwselect.GPU_RESERVE_MB
        recommended = hwselect.choose()
    except Exception:
        vram, reserve, recommended = 0, 1100, None
    budget = max(0, vram - reserve)

    models = []
    try:
        with urllib.request.urlopen(_ollama_base() + "/api/tags", timeout=6) as r:
            data = _json.loads(r.read().decode("utf-8"))
        for m in data.get("models", []):
            size_mb = round((m.get("size", 0) or 0) / (1024 * 1024))
            need_mb = size_mb + 700  # weights + rough KV/compute headroom
            details = m.get("details", {}) or {}
            models.append({
                "name": m.get("name"),
                "params": details.get("parameter_size"),
                "quant": details.get("quantization_level"),
                "size_mb": size_mb,
                "fits_gpu": bool(budget) and need_mb <= budget,
                "tools": "tools" in (m.get("capabilities") or []),
            })
        # fits first, then smaller
        models.sort(key=lambda x: (not x["fits_gpu"], x["size_mb"]))
    except Exception as e:
        return {"available": [], "selected": providers.active_local_model(),
                "recommended": recommended, "gpu_vram_mb": vram, "gpu_budget_mb": budget,
                "error": f"Could not reach Ollama at {_ollama_base()}: {e}"}

    return {"available": models, "selected": providers.active_local_model(),
            "recommended": recommended, "gpu_vram_mb": vram, "gpu_budget_mb": budget}


class ModelChoice(BaseModel):
    model: str


@app.post("/api/models/select")
def select_model(choice: ModelChoice):
    """Switch the active LOCAL model at runtime (must be an installed Ollama model)."""
    import providers
    providers.set_local_model(choice.model)
    return {"ok": True, "selected": providers.active_local_model()}


# Curated one-click-downloadable models (Ollama tags) + rough footprints (MB).
CURATED_MODELS = [
    {"tag": "gemma2:2b", "label": "Gemma 2 · 2B", "params": "2.6B", "size_mb": 1600},
    {"tag": "gemma2:9b", "label": "Gemma 2 · 9B", "params": "9.2B", "size_mb": 5400},
    {"tag": "qwen2.5:0.5b-instruct", "label": "Qwen 2.5 · 0.5B", "params": "0.5B", "size_mb": 400},
    {"tag": "qwen2.5:1.5b-instruct", "label": "Qwen 2.5 · 1.5B", "params": "1.5B", "size_mb": 1000},
    {"tag": "qwen2.5:3b-instruct", "label": "Qwen 2.5 · 3B", "params": "3.1B", "size_mb": 1900},
    {"tag": "qwen2.5:7b-instruct", "label": "Qwen 2.5 · 7B", "params": "7.6B", "size_mb": 4700},
    {"tag": "llama3.2:1b", "label": "Llama 3.2 · 1B", "params": "1.2B", "size_mb": 1300},
    {"tag": "llama3.2:3b", "label": "Llama 3.2 · 3B", "params": "3.2B", "size_mb": 2000},
    {"tag": "phi3.5", "label": "Phi 3.5 · Mini", "params": "3.8B", "size_mb": 2200},
    {"tag": "mistral:7b", "label": "Mistral · 7B", "params": "7B", "size_mb": 4100},
    {"tag": "deepseek-r1:7b", "label": "DeepSeek-R1 · 7B", "params": "7B", "size_mb": 4700},
]

_PULLS = {}  # tag -> {status, percent, done, error}


def _installed_tags():
    import json as _json
    import urllib.request
    try:
        with urllib.request.urlopen(_ollama_base() + "/api/tags", timeout=6) as r:
            data = _json.loads(r.read().decode("utf-8"))
        return {m.get("name") for m in data.get("models", [])}
    except Exception:
        return set()


@app.get("/api/models/catalog")
def models_catalog():
    """Popular models the user can pull with one click."""
    try:
        import hwselect
        budget = max(0, hwselect.total_vram_mb() - hwselect.GPU_RESERVE_MB)
    except Exception:
        budget = 0
    installed = _installed_tags()
    out = [{**m, "fits_gpu": bool(budget) and (m["size_mb"] + 700) <= budget,
            "installed": m["tag"] in installed} for m in CURATED_MODELS]
    return {"models": out, "gpu_budget_mb": budget}


def _do_pull(tag):
    import json as _json
    import urllib.request
    _PULLS[tag] = {"status": "starting", "percent": 0, "done": False, "error": None}
    try:
        body = _json.dumps({"name": tag, "stream": True}).encode("utf-8")
        req = urllib.request.Request(_ollama_base() + "/api/pull", data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=3600) as resp:
            for line in resp:
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = _json.loads(line)
                except Exception:
                    continue
                st = ev.get("status", "")
                total, completed = ev.get("total"), ev.get("completed")
                pct = _PULLS[tag]["percent"]
                if total and completed:
                    pct = round(completed / total * 100)
                _PULLS[tag].update(status=st, percent=pct)
                if ev.get("error"):
                    _PULLS[tag].update(error=ev["error"], done=True)
                    return
                if st == "success":
                    _PULLS[tag].update(status="success", percent=100, done=True)
                    return
        _PULLS[tag].update(done=True)
    except Exception as e:
        _PULLS[tag].update(error=str(e), done=True)


@app.post("/api/models/pull")
def pull_model(choice: ModelChoice):
    """Kick off an `ollama pull` in the background; poll /api/models/pull/status."""
    import threading
    tag = choice.model
    cur = _PULLS.get(tag)
    if cur and not cur.get("done"):
        return {"started": True, "already": True}
    threading.Thread(target=_do_pull, args=(tag,), daemon=True).start()
    return {"started": True}


@app.get("/api/models/pull/status")
def pull_status(model: str):
    return _PULLS.get(model, {"status": "idle", "percent": 0, "done": False, "error": None})


def _ollama_online():
    """Quick reachability check — short timeout so the health endpoint stays snappy."""
    import urllib.request
    try:
        urllib.request.urlopen(_ollama_base() + "/api/tags", timeout=2)
        return True
    except Exception:
        return False


@app.get("/api/health")
def health():
    import providers
    try:
        import hwselect
        vram = hwselect.total_vram_mb()
        ram = hwselect.ram_gb()
        recommended = hwselect.choose()  # cached after first (startup) call
    except Exception:
        vram, ram, recommended = 0, 0.0, None
    return {
        "ok": True,
        "engine": _ENGINE,
        "mock": config.MOCK,
        "local_model": providers.active_local_model(),
        "remote_model": config.REMOTE_MODEL,
        "remote_provider": config.REMOTE_PROVIDER,
        "ollama_online": _ollama_online(),
        "gpu_vram_mb": vram,
        "ram_gb": ram,
        "recommended_model": recommended,
    }


@app.on_event("startup")
def _warm_hardware_detection():
    """Detect GPU/VRAM/RAM and pick the best-fit local model in the background as
    soon as the server boots, so the first /api/health or /api/models call from
    the UI is instant instead of paying the detection cost on-demand."""
    import threading

    def _run():
        try:
            import hwselect
            hwselect.choose(verbose=True)
        except Exception as e:
            print(f"[hwselect] background detection failed: {e}")

    threading.Thread(target=_run, daemon=True).start()


@app.post("/api/route")
def route(q: Query):
    t0 = time.time()
    state = _RUN({"id": "ui", "task": q.task})
    dt = round((time.time() - t0) * 1000)

    remote = state.get("remote_tokens", 0) or 0
    _STATE["queries"] += 1
    _STATE["remote_tokens"] += remote
    if remote == 0:
        _STATE["free"] += 1

    n = _STATE["queries"]
    return {
        "task": q.task,
        "answer": state.get("answer", ""),
        "category": state.get("category"),
        "source": state.get("source"),
        "route_p": state.get("route_p"),
        "confidence": state.get("confidence"),
        "remote_tokens": remote,
        "tokens_saved": state.get("tokens_saved", 0),
        "latency_ms": dt,
        "session": {
            "queries": n,
            "remote_tokens": _STATE["remote_tokens"],
            "free_pct": round(100 * _STATE["free"] / n, 1) if n else 0,
        },
    }


# ── SPA catch-all (must be last) ──────────────────────────────────────────────

@app.get("/{full_path:path}", include_in_schema=False)
def spa_fallback(full_path: str, request: Request):
    """Return index.html for all non-API paths so TanStack Router works."""
    index = _DIST / "index.html"
    if index.exists():
        return FileResponse(str(index), media_type="text/html")
    # Fallback message if frontend hasn't been built yet
    return HTMLResponse(
        content="""
        <html><body style="font-family:monospace;background:#0f0f17;color:#fff;padding:40px">
        <h2>[WARNING] Frontend not built yet</h2>
        <p>Run the following to build the React UI:</p>
        <pre style="background:#1a1a2e;padding:16px;border-radius:8px">
  cd frontend
  npm install
  npm run build</pre>
        <p>Then restart the server.</p>
        </body></html>
        """,
        status_code=503,
    )
