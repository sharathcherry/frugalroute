# Deploying FrugalRoute to the cloud (Railway + AMD MI300X)

Goal: get everything off your laptop. Three pieces:

```
Browser ──> Frontend (Railway, Node/Nitro) ──> Backend (Railway, FastAPI)
                                                   │
                                   ┌───────────────┴───────────────┐
                                   ▼                               ▼
                          Local model (FREE)              Remote model (PAID)
                     AMD MI300X · vLLM (OpenAI API)          Fireworks
```

Your laptop ends up running only a browser tab.

---

## 1. Host the local model on AMD Developer Cloud (MI300X)

The AMD AI Developer Program gives ~**$100 free credits (~50 hrs on an MI300X, 192 GB VRAM)** — enough to serve a big model that won't garble answers like the 3B does.

1. Join the AMD AI Developer Program and launch an MI300X instance (AMD Developer Cloud).
2. On the instance, serve an OpenAI-compatible endpoint with vLLM (ROCm):
   ```bash
   vllm serve Qwen/Qwen2.5-32B-Instruct \
     --host 0.0.0.0 --port 8000 \
     --api-key YOUR_LOCAL_KEY \
     --enable-prefix-caching --max-model-len 8192
   ```
3. Expose the port publicly (or via the instance's public URL). Note the base URL, e.g.
   `https://<mi300x-host>:8000/v1`.

> Tip: spin this up when developing/demoing; it's billed per hour, not free-forever.

---

## 2. Push the repo to GitHub

```bash
cd frugalroute
git add -A && git commit -m "cloud deploy config"
git push origin main
```

`.env` is gitignored — real keys go into Railway's dashboard, not the repo.

---

## 3. Backend service on Railway (FastAPI)

1. Railway → **New Project → Deploy from GitHub repo** → pick this repo.
2. It auto-detects `railway.json` → builds `Dockerfile.web` (CPU-only; no model runs here).
3. Set **Variables** (from `.env.example`):
   ```
   MOCK=0
   LOCAL_BASE_URL=https://<mi300x-host>:8000/v1
   LOCAL_API_KEY=YOUR_LOCAL_KEY
   LOCAL_MODEL=Qwen/Qwen2.5-32B-Instruct
   REMOTE_PROVIDER=fireworks
   REMOTE_BASE_URL=https://api.fireworks.ai/inference/v1
   REMOTE_API_KEY=fw_xxx
   REMOTE_MODEL=accounts/fireworks/models/gpt-oss-120b
   CONFIDENCE_THRESHOLD=0.55
   CACHE_ENABLED=0
   ALLOW_ORIGINS=https://<your-frontend>.up.railway.app
   ```
4. Deploy → note the public URL, e.g. `https://frugalroute-api.up.railway.app`.
   Health check: open `/api/health`.

---

## 4. Frontend service on Railway (Node / TanStack Start)

Add a **second service** in the same Railway project, same repo:

1. **New Service → GitHub repo** (same repo).
2. **Settings → Root Directory:** `frontend`.
3. **Variables:**
   ```
   NITRO_PRESET=node-server          # build a Node server instead of Cloudflare
   VITE_API_URL=https://frugalroute-api.up.railway.app   # backend URL from step 3
   ```
4. **Build command:** `npm ci && npm run build`
   **Start command:** `npm run start`   (runs `node .output/server/index.mjs`)
5. Deploy → note the public URL, e.g. `https://frugalroute.up.railway.app`.
6. Go back to the **backend** and set `ALLOW_ORIGINS` to this frontend URL, redeploy.

Open the frontend URL — done.

---

## 5. Progressive changes (GitHub = CI/CD)

Both Railway services watch `main`. Your loop is now:

```bash
# edit files locally (no servers running on the laptop)
git commit -am "tweak"; git push
```

Push → Railway rebuilds both services automatically. Laptop stays idle.

---

## Immediate relief (before full frontend hosting)

If you just want the heavy stuff off your laptop *today*, host only the **model (step 1)** and **backend (step 3)**, then run the frontend locally pointing at the cloud backend:

```bash
cd frontend
# PowerShell:
$env:VITE_BACKEND_URL="https://frugalroute-api.up.railway.app"; npm run dev
```

The Vite dev proxy forwards `/api/*` to the cloud backend, so your laptop no longer runs Ollama, the model, or the Python backend — only the light Vite dev server.

---

## Notes

- `Dockerfile.web` uses `requirements.web.txt` (slim) — no fastembed/qdrant/llmlingua, so the container is small and low-RAM. The code falls back gracefully (keyword triage, cache disabled, no-op compression).
- The original `Dockerfile` (GPU, boots vLLM in-container) is untouched — keep it for the hackathon submission contract.
- `VITE_API_URL` empty ⇒ same-origin (local dev via proxy). Set it only for the hosted frontend.
