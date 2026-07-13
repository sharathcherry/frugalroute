"""FrugalRoute interactive playground — FastAPI backend.

Serves the compiled React frontend (frontend/dist) and exposes the routing
API at /api/route. All non-API paths are forwarded to index.html so that
TanStack Router can handle client-side navigation.

    pip install fastapi uvicorn
    uvicorn server:app --host 0.0.0.0 --port 8000
    # open http://localhost:8000
"""
import json
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
    {"tag": "qwen3:4b", "label": "Qwen3 · 4B", "params": "4B", "size_mb": 2500,
     "accuracy": 0.694, "remote_tokens": 4627},
    {"tag": "gemma4:e2b", "label": "Gemma4 · E2B", "params": "5.1B", "size_mb": 7200,
     "accuracy": 0.667, "remote_tokens": 0},
    {"tag": "qwen3:8b", "label": "Qwen3 · 8B", "params": "8B", "size_mb": 5200,
     "accuracy": 0.75, "remote_tokens": 317},
    {"tag": "gemma4:e4b", "label": "Gemma4 · E4B", "params": "8.0B", "size_mb": 9600,
     "accuracy": 0.694, "remote_tokens": 317},
    {"tag": "gemma4:12b", "label": "Gemma4 · 12B", "params": "11.9B", "size_mb": 7600,
     "accuracy": 0.778, "remote_tokens": 317,
     "note": "Best measured accuracy-per-GB in our benchmark sweep — recommended default."},
    {"tag": "qwen3:14b", "label": "Qwen3 · 14B", "params": "14B", "size_mb": 9300,
     "accuracy": 0.694, "remote_tokens": 1004},
    {"tag": "gemma4:26b", "label": "Gemma4 · 26B", "params": "25.8B", "size_mb": 17000,
     "accuracy": 0.75, "remote_tokens": 317},
    {"tag": "qwen3:30b-a3b", "label": "Qwen3 · 30B-A3B (MoE)", "params": "30B (3.3B active)", "size_mb": 18000,
     "accuracy": 0.722, "remote_tokens": 2502},
    {"tag": "gemma4:31b", "label": "Gemma4 · 31B", "params": "31.3B", "size_mb": 19000,
     "accuracy": 0.778, "remote_tokens": 317},
    {"tag": "qwen3:32b", "label": "Qwen3 · 32B", "params": "32B", "size_mb": 20000,
     "accuracy": 0.722, "remote_tokens": 448},
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


# ── Remote (Fireworks) model catalog — lets the UI pick ANY chat-capable
# model the account has access to, instead of being pinned to one hardcoded
# REMOTE_MODEL forever. Grouped by inferred "provider family" (Fireworks
# itself hosts models originally built by many labs — OpenAI's gpt-oss,
# Zhipu's GLM, DeepSeek, Moonshot's Kimi, etc. — the /v1/models endpoint's
# own `owned_by` field is just "fireworks" for all of them, so we infer the
# real upstream family from the model's display name for a grouping that's
# actually useful).
#
# NOTE: Fireworks' public catalog (accounts/fireworks/models) lists ~290
# models total, but most require spinning up a paid on-demand deployment
# before they're callable — confirmed by direct chat/completions calls
# returning NOT_FOUND for models with supportsServerless=false. Only models
# with supportsServerless=true are instantly callable via this account's
# Fireworks credits with no extra deployment step, so that's what we filter to.
_REMOTE_FAMILY_HINTS = [
    ("openai", "OpenAI (gpt-oss)"),
    ("glm", "Zhipu (GLM)"),
    ("deepseek", "DeepSeek"),
    ("kimi", "Moonshot (Kimi)"),
    ("minimax", "MiniMax"),
    ("qwen", "Alibaba (Qwen)"),
    ("nvidia", "NVIDIA (Nemotron)"),
    ("nemotron", "NVIDIA (Nemotron)"),
    ("llama", "Meta (Llama)"),
    ("mixtral", "Mistral"),
    ("mistral", "Mistral"),
    ("yi ", "01.AI (Yi)"),
    ("phi-", "Microsoft (Phi)"),
    ("gemma", "Google (Gemma)"),
    ("flux", "Black Forest Labs (FLUX, image)"),
]

# Kinds that are real base/custom chat models. Excludes EMBEDDING_MODEL,
# FLUMINA_BASE_MODEL/FLUMINA_ADDON (image generation, e.g. FLUX), and the
# DRAFT/PEFT/TEFT addon kinds (speculative-decoding draft models, LoRA
# adapters — not standalone chat models you'd pick from a model picker).
_CHAT_KINDS = {"HF_BASE_MODEL", "CUSTOM_MODEL"}

_remote_catalog_cache = {"data": None, "ts": 0}


def _remote_family(display_name: str) -> str:
    name = display_name.lower()
    for hint, label in _REMOTE_FAMILY_HINTS:
        if hint in name:
            return label
    return "Other"


def _fetch_fireworks_catalog():
    """Paginated fetch of the full Fireworks account model catalog (control-plane
    API, NOT the OpenAI-compatible /v1/models — that one silently truncates to
    whatever subset happens to be pre-warmed, undercounting real access)."""
    import json as _json
    import urllib.request
    import time as _time

    if _remote_catalog_cache["data"] is not None and _time.time() - _remote_catalog_cache["ts"] < 300:
        return _remote_catalog_cache["data"]

    all_models = []
    token = None
    account = config.REMOTE_BASE_URL.rstrip("/").split("//", 1)[-1].split("/")[0]  # unused; account is always "fireworks" for the shared catalog
    base = "https://api.fireworks.ai/v1/accounts/fireworks/models"
    for _ in range(10):  # hard cap — ~290 models / 200 per page is 2 pages; 10 is a safety bound
        url = f"{base}?pageSize=200" + (f"&pageToken={token}" if token else "")
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {config.REMOTE_API_KEY}"})
        with urllib.request.urlopen(req, timeout=15) as r:
            d = _json.loads(r.read().decode("utf-8"))
        all_models.extend(d.get("models", []))
        token = d.get("nextPageToken")
        if not token or token in ("0", 0):
            break

    _remote_catalog_cache["data"] = all_models
    _remote_catalog_cache["ts"] = _time.time()
    return all_models


@app.get("/api/models/remote")
def remote_models_catalog():
    """List every chat-capable model that's actually instantly callable (no
    dedicated deployment needed) on the configured remote provider, grouped by
    inferred provider family."""
    import providers

    if config.REMOTE_PROVIDER != "fireworks":
        return {"groups": [], "active": providers.active_remote_model(),
                "error": f"Model listing only implemented for Fireworks (REMOTE_PROVIDER={config.REMOTE_PROVIDER})"}

    try:
        all_models = _fetch_fireworks_catalog()
    except Exception as e:
        return {"groups": [], "active": providers.active_remote_model(),
                "error": f"Could not reach Fireworks model catalog: {e}"}

    chat_models = [
        m for m in all_models
        if m.get("supportsServerless") and m.get("kind") in _CHAT_KINDS
    ]

    groups: dict[str, list] = {}
    for m in chat_models:
        display = m.get("displayName") or m["name"].rsplit("/", 1)[-1]
        fam = _remote_family(display)
        groups.setdefault(fam, []).append({
            "id": m["name"],
            "label": display,
            "context_length": m.get("contextLength") or None,
            "supports_tools": bool(m.get("supportsTools")),
            "supports_image_input": bool(m.get("supportsImageInput")),
        })
    ordered = [{"provider": k, "models": sorted(v, key=lambda x: x["label"])}
               for k, v in sorted(groups.items())]
    return {"groups": ordered, "active": providers.active_remote_model(),
            "total_catalog_size": len(all_models),
            "instantly_available": len(chat_models)}


class RemoteModelChoice(BaseModel):
    model: str


@app.post("/api/models/remote/select")
def select_remote_model(choice: RemoteModelChoice):
    """Switch the active REMOTE (Fireworks) model at runtime."""
    import providers
    providers.set_remote_model(choice.model)
    return {"ok": True, "selected": providers.active_remote_model()}


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
        "remote_model": providers.active_remote_model(),
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


# Real, persistent rolling query log for the Analytics page — every request
# through /api/route below is appended here (NOT synthetic/demo data). Kept as
# a JSONL file so it survives backend restarts; capped in memory to the most
# recent QUERY_LOG_MAX entries for the /api/analytics endpoint's fast path.
QUERY_LOG_PATH = Path(__file__).parent / "query_log.jsonl"
QUERY_LOG_MAX = 5000
_QUERY_LOG: list = []


def _load_query_log():
    if QUERY_LOG_PATH.exists():
        try:
            with open(QUERY_LOG_PATH) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        _QUERY_LOG.append(json.loads(line))
            del _QUERY_LOG[:-QUERY_LOG_MAX]
        except Exception as e:
            print(f"[analytics] could not load query_log.jsonl: {e}")


_load_query_log()


def _log_query(task, category, source, latency_ms, remote_tokens):
    entry = {
        "ts": time.time(),
        "task_preview": task[:80],
        "category": category,
        "source": source,
        "latency_ms": latency_ms,
        "remote_tokens": remote_tokens,
    }
    _QUERY_LOG.append(entry)
    if len(_QUERY_LOG) > QUERY_LOG_MAX:
        del _QUERY_LOG[: len(_QUERY_LOG) - QUERY_LOG_MAX]
    try:
        with open(QUERY_LOG_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"[analytics] could not append to query_log.jsonl: {e}")


# Real per-token cost assumption for the "savings" estimate — Fireworks bills
# per token on the remote model; this uses the same $/token figure the
# frontend already displays elsewhere in the app (see chat.tsx cost/saved
# calculations) so the numbers stay internally consistent across the UI.
REMOTE_COST_PER_TOKEN = 0.0000015


@app.get("/api/analytics")
def analytics():
    """Real, computed-from-the-actual-query-log analytics — no fabricated or
    simulated data. Numbers reflect exactly what /api/route has actually
    processed since the log file was created."""
    import datetime

    log = _QUERY_LOG
    n = len(log)
    if n == 0:
        return {
            "total_requests": 0, "avg_cost_per_request": 0, "total_savings": 0,
            "routing": [], "daily": [], "recent_queries": [],
        }

    src_counts = {"local": 0, "remote": 0, "cache": 0, "other": 0}
    for e in log:
        s = e.get("source") or "other"
        if s in ("local", "triage_local"):
            src_counts["local"] += 1
        elif s == "remote":
            src_counts["remote"] += 1
        elif s == "cache":
            src_counts["cache"] += 1
        else:
            src_counts["other"] += 1

    total_remote_tokens = sum(e.get("remote_tokens") or 0 for e in log)
    remote_calls = [e for e in log if e.get("source") == "remote" and e.get("remote_tokens")]
    avg_remote_tokens_per_call = (
        sum(e["remote_tokens"] for e in remote_calls) / len(remote_calls) if remote_calls else 0
    )
    actual_cost = total_remote_tokens * REMOTE_COST_PER_TOKEN
    # Counterfactual: what it would have cost if EVERY request (including the
    # ones that stayed local/cache for free) had gone to the remote model,
    # using the real observed average remote-call token cost from this same
    # log as the per-query estimate.
    cloud_only_cost = n * avg_remote_tokens_per_call * REMOTE_COST_PER_TOKEN
    total_savings = round(cloud_only_cost - actual_cost, 4)

    routing = [
        {"name": "Local", "value": round(100 * src_counts["local"] / n, 1)},
        {"name": "Remote", "value": round(100 * src_counts["remote"] / n, 1)},
        {"name": "Cache", "value": round(100 * src_counts["cache"] / n, 1)},
    ]

    # Daily buckets — only days that actually have real traffic appear.
    daily_map: dict = {}
    for e in log:
        day = datetime.datetime.utcfromtimestamp(e["ts"]).strftime("%Y-%m-%d")
        d = daily_map.setdefault(day, {"day": day, "requests": 0, "remote_tokens": 0})
        d["requests"] += 1
        d["remote_tokens"] += e.get("remote_tokens") or 0
    daily = []
    for day, d in sorted(daily_map.items()):
        actual = d["remote_tokens"] * REMOTE_COST_PER_TOKEN
        cloud_equiv = d["requests"] * avg_remote_tokens_per_call * REMOTE_COST_PER_TOKEN
        daily.append({
            "day": day, "requests": d["requests"],
            "actual_cost": round(actual, 4), "cloud_only_cost": round(cloud_equiv, 4),
        })

    recent = list(reversed(log[-50:]))
    recent_out = [{
        "ts": e["ts"], "task_preview": e["task_preview"], "category": e.get("category"),
        "source": e.get("source"), "latency_ms": e.get("latency_ms"),
    } for e in recent]

    return {
        "total_requests": n,
        "avg_cost_per_request": round(actual_cost / n, 6) if n else 0,
        "total_savings": total_savings,
        "routing": routing,
        "daily": daily,
        "recent_queries": recent_out,
    }


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
    _log_query(q.task, state.get("category"), state.get("source"), dt, remote)
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
