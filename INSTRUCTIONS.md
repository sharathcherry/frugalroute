# FrugalRoute — Instructions

A local-first LLM **routing agent** for AMD Developer Hackathon: ACT II — Track 1
(Hybrid Token-Efficient Routing Agent). For each task it decides whether a **free
local model** can answer, or whether to escalate to a **paid remote model** — using
the fewest paid tokens while holding accuracy above a threshold.

---

## 1. Quick start (mock — no models, no keys, no GPU)

```bash
cd frugalroute
python run.py            # runs the full pipeline on sample tasks, writes dashboard/data.js
python eval/harness.py   # calibration + threshold tuning + AutoMix + PredictiveRouter
```

`MOCK=1` (the default) uses canned model text so you can verify the pipeline logic
— routing, calibration, cache, savings — with zero setup. Open `dashboard/index.html`
to see the run.

---

## 2. What's in the repo

| File | Purpose |
|------|---------|
| `run.py` | Entry point — runs the pipeline, writes `dashboard/data.js` |
| `graph.py` / `engine.py` | LangGraph pipeline (prod) / dependency-free runner (fallback) |
| `nodes.py` | Node logic: ingest → triage → cache → route → local → gate → remote → account |
| `triage.py` | Phase 1 semantic triage (Semantic-Router idea) |
| `predict.py` | Predictive router (RouteLLM Matrix-Factorization role) |
| `verify.py` | Confidence gate — `calibrated` or `automix` mode |
| `calibrate.py` | Platt / Isotonic calibration + ECE / Brier |
| `automix.py` | AutoMix POMDP belief gate (cost-aware escalation) |
| `compress.py` | LLMLingua-2 prompt compression (+ fallback) |
| `cache.py` | Semantic cache — Qdrant + fastembed (difflib fallback) |
| `prompts.py` | Prefix-stable prompts for RadixAttention/APC cache hits |
| `providers.py` | Provider layer — local + remote (fireworks / azure / openai) |
| `eval/tasks.jsonl` | 36 labeled eval tasks (category + difficulty + gold) |
| `eval/harness.py` | Calibrate, tune threshold, train router — the "test to threshold" |
| `eval/bench.py` | Benchmark candidate local models |
| `serve/` | SGLang / vLLM / Ollama launch scripts (AMD ROCm) |
| `dashboard/` | Routing & savings dashboard (React + Framer Motion + Recharts) |
| `test_azure.py` | Azure connectivity dry-test |

---

## 3. Run it for real (`MOCK=0`)

You need **two** things running: a local model (free) and a remote provider (paid).

### 3a. Local model (free path)

Pick one, all expose an OpenAI-compatible endpoint:

```bash
# Ollama (simplest)
ollama pull qwen2.5:3b-instruct        # Windows: install from ollama.com first
# -> http://localhost:11434/v1

# vLLM on AMD ROCm (Automatic Prefix Caching)
bash serve/start_vllm.sh               # -> http://localhost:8000/v1

# SGLang on AMD ROCm (RadixAttention)
bash serve/start_sglang.sh             # -> http://localhost:30000/v1
```

### 3b. Remote provider (paid path)

Set `REMOTE_PROVIDER` in `.env`:

- **`fireworks`** — the hackathon-scored path. `REMOTE_BASE_URL`, `REMOTE_API_KEY`, `REMOTE_MODEL`.
- **`azure`** — Azure OpenAI / AI Foundry (portfolio / dev). See §7.
- **`openai`** — any other OpenAI-compatible endpoint (`REMOTE_BASE_URL` + `REMOTE_API_KEY`).

### 3c. Run

```bash
# in .env: MOCK=0
python test_azure.py     # only if REMOTE_PROVIDER=azure — confirm it works first
python eval/harness.py   # fit calibrator -> calib.json, recommend CONFIDENCE_THRESHOLD
python run.py            # real routing + real token counts + dashboard
```

---

## 4. `.env` reference

```ini
MOCK=1                      # 1 = canned inference (logic only); 0 = real models

# Remote provider
REMOTE_PROVIDER=fireworks   # fireworks | azure | openai
REMOTE_BASE_URL=https://api.fireworks.ai/inference/v1
REMOTE_API_KEY=fw_xxx
REMOTE_MODEL=accounts/fireworks/models/llama-v3p1-8b-instruct

# Azure (only if REMOTE_PROVIDER=azure)
AZURE_OPENAI_ENDPOINT=https://<resource>.services.ai.azure.com   # base host, NO /openai/v1
AZURE_OPENAI_API_KEY=***
AZURE_OPENAI_DEPLOYMENT=<exact deployment name>
AZURE_OPENAI_API_VERSION=2024-06-01

# Local
LOCAL_BASE_URL=http://localhost:11434/v1
LOCAL_MODEL=qwen2.5:3b-instruct

# Gate + thresholds (tune with eval/harness.py)
GATE_MODE=calibrated        # calibrated | automix
CONFIDENCE_THRESHOLD=0.7     # calibrated mode: accept local if calibrated P >= this
CALIB_PATH=calib.json        # set after running the harness
ROUTE_THRESHOLD=0.75         # predictive router: skip local if P(need_remote) >= this

# AutoMix (automix mode)
AUTOMIX_PENALTY=-2.0         # raise magnitude -> escalate more (safer accuracy)
AUTOMIX_COST=0.3             # raise -> escalate less (cheaper)

# Compression
COMPRESS=1
COMPRESS_RATE=0.5

# Semantic cache
CACHE_BACKEND=auto           # auto | qdrant | difflib
EMBED_MODEL=BAAI/bge-small-en-v1.5
QDRANT_PATH=                 # set (e.g. ./qdrant_data) to persist the cache
```

---

## 5. Tune to the accuracy threshold

`eval/harness.py` is the evaluation tool:

1. Runs each labeled task, collects `(raw_confidence, correct)` pairs.
2. Fits Platt + Isotonic calibrators → saves the best to `calib.json` (lower ECE).
3. Sweeps the threshold → prints the **minimum remote calls that still hold the 0.95
   accuracy floor** → your `CONFIDENCE_THRESHOLD`.
4. Fits the AutoMix observation model → `automix.json`.
5. Trains the `PredictiveRouter`.

Then set `CALIB_PATH=calib.json` and the recommended `CONFIDENCE_THRESHOLD` in `.env`.

---

## 6. Gate modes

- **`calibrated`** — accept local if calibrated `P(correct) >= CONFIDENCE_THRESHOLD`.
- **`automix`** — Bayesian belief over correctness from noisy self-verification;
  escalates by expected-reward (cost-aware). Tune with `AUTOMIX_PENALTY` / `AUTOMIX_COST`.

Switch with `GATE_MODE` in `.env`.

---

## 7. Azure setup (the gotchas)

Azure has two resource types with **different** endpoints:

- Classic **Azure OpenAI** → `https://<name>.openai.azure.com`
- **Azure AI Foundry / AI Services** → `https://<name>.services.ai.azure.com`

Rules that trip people up:
- Use the **base host only** in `AZURE_OPENAI_ENDPOINT` — no `/openai/v1`, no trailing path.
- Auth is the **api-key** header (the `AzureOpenAI` client handles this). A `Bearer` token gives **401**.
- `AZURE_OPENAI_DEPLOYMENT` = the **exact deployment name** from the portal, not the model name.
- Get the real endpoint from **portal → resource → Keys and Endpoint**.

Diagnose fast:
```bash
python test_azure.py     # want: AZURE OK -> ok
```
Error meaning:
- `APIConnectionError` → wrong endpoint host / `/openai/v1` left in / network blocked.
- HTML `404` → endpoint host isn't a live resource (wrong name).
- JSON `500` → host + auth fine, but the **deployment is broken / has no quota** → fix it in the portal (check status = Succeeded, capacity > 0, test in Chat playground).

---

## 8. Dashboard

`run.py` writes `dashboard/data.js` each run. Open `dashboard/index.html` (double-click,
`file://` is fine — no server needed). Shows routing mix, cumulative remote tokens,
per-category breakdown, KPIs, and a per-task table. Refresh = rerun `run.py` + reload.
(It loads React/Framer Motion/Recharts from CDN, so it needs internet on open.)

---

## 9. Benchmark local models

```bash
# edit CANDIDATES in eval/bench.py, start each on LOCAL_BASE_URL, MOCK=0
python eval/bench.py
# -> accuracy / latency / size per model, recommends the best that fits a latency budget
```

---

## 10. Kickoff checklist (July 6)

1. Register by **July 2** (day-one credits). New-member credits: 2–3 day approval.
2. At "Introduction to the Challenge" capture: exact task format, **scoring formula
   (input+output vs output tokens)**, whether the env has **network**, and the named models.
3. Put the announced models in `.env`, `MOCK=0`, `REMOTE_PROVIDER=fireworks`.
4. Replace `TODO(kickoff)` stubs: real `verify.judge_raw` signal; fit calibrator on real data.
5. Seed `eval/tasks.jsonl` with real task shapes → `python eval/harness.py` → set threshold.
6. If the scoring env has **no network**, bake the local model into the container.
7. `python run.py`, check the dashboard, then submit.

---

## 11. Submission

- Public GitHub repo + README (this file helps).
- **Containerized** and runnable from instructions (`Dockerfile`).
- Title, descriptions, tags, cover image, **video**, **slides**, demo URL — on lablab.ai
  before **Jul 11, 12:00 PM EDT**.

---

## Notes

- `MOCK=1` proves the pipeline logic without any model. Real *answers* need a live
  endpoint (`MOCK=0`) — separate from whether the pipeline is correct.
- For the scored submission use **Fireworks**; Azure is for dev / portfolio.
- Heavy deps (langgraph, fastembed, qdrant-client, llmlingua) are all optional —
  the repo falls back gracefully so `python run.py` always works.
```
