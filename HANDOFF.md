# FrugalRoute — Project Handoff

_Last updated: Jul 11, 2026. Read this first — it captures everything to date so a new person or agent can continue without missing context._

---

## 1. What this project is
**FrugalRoute** is a **hybrid token-efficient LLM routing agent** built for the **AMD Developer Hackathon: ACT II, Track 1** ("Hybrid Token-Efficient Routing Agent"). For every incoming task it decides, autonomously, whether a **free local model** can answer it well enough, or whether to **escalate to a paid remote model** — spending the fewest paid tokens while keeping accuracy above a threshold.

- **Owner:** Sharath Chandra (B.Tech CSE-AIML). Goals: (1) win/place in Track 1, (2) use it as a portfolio piece for Gen-AI engineering roles (see `Consultant - Python Developer with Gen AI` KPMG JD in uploads).
- **Track 1 scoring:** a **leaderboard** — ranked by **remote token count at/above an accuracy floor**. Local tokens count as zero. Final scoring runs on the organizers' **standardized environment** (you submit a container; they run it).
- **Deadline:** **Jul 11, 2026, 12:00 PM EDT (16:00 UTC).**

## 2. Repo location & key docs
- Repo: `AMD Project/frugalroute/`
- `INSTRUCTIONS.md` — how to run (mock + real), `.env` reference, Azure troubleshooting.
- `WINNING_PLAN.md` — the 13-hour sprint plan to a winning-grade submission + ACT I pattern analysis.
- `FrugalRoute - Track 1 Strategy Plan.docx` (in `AMD Project/`) — the original strategy.
- `HANDOFF.md` — this file.

## 3. Architecture (Edge-Cloud Pareto-Router)
Pipeline: `ingest → triage → cache → route → local → gate → (compress) → remote → account`

| File | Role | Reference |
|------|------|-----------|
| `run.py` | Entry point; runs pipeline, writes `dashboard/data.js` | — |
| `graph.py` / `engine.py` | LangGraph pipeline (prod) / dependency-free runner (fallback) | — |
| `nodes.py` | All node logic (ingest, triage, cache, route, local, gate, remote, account) | — |
| `triage.py` | Phase 1 zero-cost semantic triage | Semantic-Router |
| `predict.py` | Predictive router → P(need_remote) | RouteLLM (MF role) |
| `verify.py` | Confidence gate; `judge_raw` = local self-grade | FrugalGPT |
| `calibrate.py` | Platt/Isotonic calibration + ECE/Brier | calibration theory |
| `automix.py` | AutoMix POMDP belief gate (cost-aware) | AutoMix |
| `compress.py` | LLMLingua-2 prompt compression (+fallback) | LLMLingua-2 |
| `cache.py` | Semantic cache: Qdrant + fastembed (difflib fallback) | RadixAttention idea |
| `prompts.py` | Prefix-stable prompts for RadixAttention/APC cache hits | — |
| `providers.py` | Provider layer: local + remote (fireworks/azure/openai) | — |
| `eval/harness.py` | Calibrate + tune threshold + train router (the "test to threshold") | — |
| `eval/bench.py` | Benchmark candidate local models | — |
| `eval/tasks.jsonl` | 36 labeled eval tasks (category + difficulty + gold) | — |
| `serve/` | SGLang/vLLM/Ollama launch scripts (AMD ROCm) | — |
| `dashboard/` | Routing & savings dashboard (React + Framer Motion + Recharts) | — |
| `test_azure.py` | Azure connectivity dry-test | — |

**Design theory implemented (from `Hybrid LLM Routing Architecture Research.md`):** RouteLLM predictive routing, FrugalGPT cascade, AutoMix POMDP, Semantic-Router triage, confidence calibration (Platt/Isotonic + ECE), LLMLingua-2 compression, Qdrant semantic cache, RadixAttention/APC prefix caching.
**Deliberately skipped (infeasible):** speculative decoding, RadixAttention on the remote, 500× compression — reasons in README.

## 4. Current state — WHAT WORKS (verified)
- **Full real end-to-end run confirmed** on **AMD Instinct MI300X (192GB) via vLLM/ROCm** as the local model + **Fireworks `gpt-oss-120b`** as remote. Latest real run: **3 local / 3 remote / 1 cache**, local model **self-rated** its answers (e.g. summary conf 0.35 → correctly escalated). Dashboard shows this run.
- **`judge_raw` self-verify is real** (`JUDGE_MODE=selfrate`): the local model grades its own answer → real, varied confidence drives routing. (Was a `0.5` stub before — that caused an all-remote run; now fixed.)
- **Remote providers both work:** Fireworks (scored path) and Azure OpenAI (`gpt-4o` via `services.ai.azure.com`).
- Mock mode (`MOCK=1`) runs the whole pipeline with zero deps for logic testing.
- vLLM prefix caching (RadixAttention/APC) observed hitting ~31% on shared prompt prefixes.

## 5. Live compute environment (IMPORTANT)
- **AMD Developer Cloud droplet** (DigitalOcean-backed): **MI300X x1**, Ubuntu, ROCm 7.2.4.
  - **Public IP:** `129.212.178.3`
  - **vLLM container:** `frugal-vllm`, serving `Qwen/Qwen2.5-7B-Instruct` on **port 8001**, OpenAI-compatible at `http://129.212.178.3:8001/v1`. Started with `--api-key`, `--enable-prefix-caching`, `--max-model-len 8192`, env `VLLM_HOST_IP=127.0.0.1` (needed to fix a gloo/host-networking init error on ROCm).
  - A separate `rocm` container holds ports 8000/8888/30000 (Jupyter etc.) — that's why vLLM is on 8001.
  - **Billing ~$1.99/hr while running.** $100 credit, expires ~28 days. **Stop the droplet when idle.**
  - SSH: an ed25519 keypair was generated; public key added to the droplet, private key delivered to the user. User = `root`.

## 6. Configuration (`.env`) — current effective values
```
MOCK=0
JUDGE_MODE=selfrate
GATE_MODE=calibrated          # or automix
CONFIDENCE_THRESHOLD=0.7      # NOT yet tuned on real data
CALIB_PATH=                   # empty -> identity calibrator (NOT fit yet)
# Local (MI300X vLLM)
LOCAL_BASE_URL=http://129.212.178.3:8001/v1
LOCAL_API_KEY=<vllm api-key>
LOCAL_MODEL=Qwen/Qwen2.5-7B-Instruct
# Remote — Fireworks is the SCORED path
REMOTE_PROVIDER=fireworks
REMOTE_BASE_URL=https://api.fireworks.ai/inference/v1
REMOTE_API_KEY=<fireworks key>
REMOTE_MODEL=accounts/fireworks/models/gpt-oss-120b
# Azure alt (works): REMOTE_PROVIDER=azure, AZURE_OPENAI_ENDPOINT=https://<res>.services.ai.azure.com (base host, NO /openai/v1), api-key header, deployment=gpt-4o
```
Valid Fireworks models on this account: `gpt-oss-120b`, `deepseek-v4-pro`, `glm-5p2`, `kimi-k2p6`.

## 7. What's DONE vs REMAINING (for a winning submission)
**Done:** full architecture + all differentiators; real run on AMD GPU + real remote; `judge_raw`; dashboard; docs.
**Remaining (see `WINNING_PLAN.md`):**
1. **Fit calibration on real data** (`eval/harness.py` on the GPU → `calib.json`, tune `CONFIDENCE_THRESHOLD`). *Top lever — currently on raw self-ratings, likely over-escalating.*
2. **Adapt to the real Track 1 task/output format + scoring formula** from the Jul 6 kickoff — **NOT yet obtained.** Everything runs on placeholder tasks (`eval/tasks.jsonl`). Real `accuracy_check` needed.
3. **Containerize the router + test clean** (Dockerfile exists, untested as a submission artifact; bake local model in if scoring env has no network).
4. **Public GitHub repo**, **demo video (~2 min)**, **slide deck**, **cover image**, **demo URL**.
5. **Submit on lablab** before the deadline. Confirm **registration/enrollment**.

## 8. Known issues & gotchas
- **Sandbox↔folder mount lag:** the Linux sandbox that Claude uses caches the `AMD Project` mount and often serves **stale/truncated copies of overwritten files**. New files sync fine; overwrites lag. Workaround used repeatedly: copy repo to `/tmp` (`cp -r`) or write fresh via heredoc, then run there. **The authoritative files are the ones the file tools wrote (what the user sees).**
- **Local calls generate uncapped** in the harness path → slow over the network. A `max_tokens=400` cap was patched in the `/tmp` copy for speed; consider adding it to `providers.py` for real runs.
- **Calibration not fit yet** → routing uses raw self-ratings; `summarization` under-confident (0.35) → over-escalation. Fix via harness.
- **Azure quirks (solved):** real resource is `...services.ai.azure.com` (not `...openai.azure.com`, which 404s); auth is the **api-key** header (Bearer → 401); endpoint must be the **base host, no `/openai/v1`**; a `500` = broken/no-quota deployment (fixed by using `gpt-4o`).

## 9. Secrets / security (ACTION)
- API keys (Fireworks, Azure) and the vLLM api-key live in `.env`. **They were shared in chat during setup and should be rotated.** **Do NOT commit `.env` or the SSH private key to GitHub** — add them to `.gitignore`. The SSH key is a throwaway generated in a sandbox.

## 10. Immediate next actions
1. Owner: confirm **lablab registration** + paste the **real kickoff task/submission spec** (blocks the interface adaptation + real calibration).
2. Run **calibration harness** on the MI300X → `calib.json` + tuned threshold.
3. Build **container + repo + video/slides/cover**; submit before 16:00 UTC.
4. **Stop the GPU droplet** when done to save credit.

## 11. Timeline of work done (summary)
Scraped + analyzed the full hackathon + ACT I winners → chose Track 1 → strategy doc → scaffolded FrugalRoute → added calibration, triage, predictive router, LLMLingua-2, Qdrant cache, AutoMix, RadixAttention serving, dashboard, Azure provider → built eval set + calibration harness + model benchmark → fixed `judge_raw` → provisioned MI300X, served Qwen2.5-7B on vLLM → **ran the full real pipeline (AMD local + Fireworks remote)** → wrote INSTRUCTIONS, WINNING_PLAN, this handoff.
