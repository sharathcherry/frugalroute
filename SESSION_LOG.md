# FrugalRoute — Claude Code Session Log

**Date:** 2026-07-03
**Project:** FrugalRoute — Local-first LLM routing agent (AMD Developer Hackathon: ACT II, Track 1)
**Scope of session:** project deep-dive, full pipeline runs, Azure fix, CLAUDE.md creation, hackathon page research, deep-research skill repair.

---

## 1. Project Understanding (INSTRUCTIONS.md + full codebase read)

- **Goal:** Route each task to a free local model (Ollama) or escalate to a paid remote model, minimizing paid tokens while holding accuracy ≥ 0.95.
- **Pipeline:** `ingest → triage → cache → route → local → gate → remote → account`
  - Shared node logic: `nodes.py`; LangGraph orchestration: `graph.py`; stdlib fallback: `engine.py`.
- **Phase 1:** Semantic triage (fastembed BGE / keyword fallback; easy → force_local, unsafe → block) + semantic cache (Qdrant + fastembed, difflib fallback, similarity threshold 0.92).
- **Phase 2:**
  - `PredictiveRouter` — 3-feature logistic [bias, norm_length, is_hard], weights [-1.2, 1.5, 3.0]; P(need_remote) ≥ `ROUTE_THRESHOLD` (0.75) → skip local entirely.
  - `OnlinePolicy` bandit — warmup 3, local success rate < 0.34 → prefer_remote.
  - Confidence gate, two modes: `calibrated` (judge_raw → calibrator → ≥ `CONFIDENCE_THRESHOLD` 0.7) or `automix` (Gaussian ObsModel, Bayes belief update, expected-reward decision).
- **Phase 3:** LLMLingua-2 prompt compression (stopword-strip fallback, rate 0.5) → remote call → `remote_tokens = prompt + completion`.
- **Calibration:** pure-Python Platt (GD on BCE) + Isotonic (PAVA); ECE/Brier metrics; `eval/harness.py` fits calibrator, recommends threshold.
- **Entry points:** `python run.py` (writes `dashboard/data.js`), `python eval/harness.py`, `python eval/run_eval.py`, `python eval/bench.py`.
- **Config gotchas:** `.env` has duplicate keys — python-dotenv keeps LAST occurrence; `os.environ` overrides `.env` (so inline `LOCAL_MODEL=x python run.py` works). Effective config: `MOCK=0`, `REMOTE_PROVIDER=azure`.
- **Known stubs (kickoff TODOs):** `verify.judge_raw` returns flat 0.5 in real mode; `nodes.account` hardcodes `correct = True`; `harness._mock_local` simulates overconfident model (delete at kickoff).

## 2. Full Pipeline Runs

Ran in 4 configurations:

| Run | Config | Result |
|-----|--------|--------|
| Real harness | 0.5B local | Degenerate sweep (judge_raw flat 0.5 → no calibration signal) — expected, known stub |
| Real local-only | `CONFIDENCE_THRESHOLD=0.0`, `ROUTE_THRESHOLD=1.1` | 6 local + 1 cache hit, 0 remote tokens |
| Full mock suite | `MOCK=1` | run.py: 87 remote tokens; run_eval.py: cache saves 48 tokens, ECE 0.146 → 0.000; bench.py recommends gemma2-2b |
| Full real E2E (post-Azure-fix) | Ollama 0.5B + Azure gpt-4o | `engine=langgraph`, remote_tokens=829, tokens_saved=11, free%=14.3, escalate%=85.7, cache_hits=1 |

High escalation (85.7%) expected: judge_raw stub returns 0.5 < 0.7 threshold, so everything except cache hit escalates. Remote path itself verified solid.

### GPU constraint discovered
- 4GB RTX 3050 Ti laptop: `qwen2.5:3b-instruct` fails to load — `cudaMalloc failed: out of memory ... CUDA0 buffer of size 1923955712` despite nvidia-smi showing ~3.9GB free (WDDM reservations invisible).
- Tried: retry, partial offload (num_gpu=20), CPU-only (num_gpu=0), reduced ctx — all failed (RAM also tight).
- **Fix:** `ollama pull qwen2.5:0.5b-instruct` (454MB, loads 100% GPU) + `LOCAL_MODEL=qwen2.5:0.5b-instruct` env override.

## 3. Azure Diagnosis & Fix (via az CLI)

**Symptom:** `test_azure.py` → NotFoundError with HTML 404 body.

**Root causes (three separate errors in `.env`):**
1. Endpoint host wrong: resource `resource1234stocks` is kind **AIServices** → real endpoint `resource1234stocks.cognitiveservices.azure.com`; `.env` pointed at `resource1234stocks.openai.azure.com` (does not exist → HTML 404).
2. That resource has **zero model deployments**.
3. Deployment `gpt-4o-mini` exists nowhere in the subscription.

**Fix:** Pointed `.env` at working resource `vani-aoai` (kind OpenAI, swedencentral, RG `vani-rg`):
- `AZURE_OPENAI_ENDPOINT=https://vani-aoai-ff646.openai.azure.com` (note `-ff646` suffix — portal endpoint ≠ resource name)
- `AZURE_OPENAI_DEPLOYMENT=gpt-4o` (status Succeeded, capacity 10)
- Key fetched via `az cognitiveservices account keys list` into `.env` (never printed).

**Verified:** `python test_azure.py` → `AZURE OK -> Ok`. Then full real E2E run succeeded (see table above).

**Note:** Azure = dev/portfolio path only. Fireworks AI = scored hackathon path.

## 4. CLAUDE.md Created

Project `CLAUDE.md` created at repo root. Mandates `/caveman:caveman` skill each session (level full; code/commits/PRs/security written normally). Documents pipeline, entry points, `.env` duplicate-key gotcha, MOCK modes, remote-provider roles, GPU constraint, never-print-API-keys rule.

## 5. Hackathon Page Research (firecrawl)

Installed `firecrawl-cli@1.19.6` globally, authenticated with user-provided API key, scraped `https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii` (53k chars markdown, saved to session scratchpad).

### Key facts
- **Event:** AMD Developer Hackathon: ACT II, online on lablab.ai. Prize pool $15,000. Kickoff **Jul 6, 12:00 PM EDT**; submissions close **Jul 11, 12:00 PM EDT**.
- **Track 1 — Hybrid Token-Efficient Routing Agent** (chosen): tasks revealed at kickoff; agent autonomously routes local vs remote (Fireworks AI). Judged on **token count + output accuracy**, leaderboard-ranked. **Local models/tokens count ZERO.** Final scoring on a **standardized environment** (specs at launch) — local model must fit it. Fine-tuned and prompt-based approaches scored identically. Models revealed launch day.
- Track 2 — Video Captioning: 30s–2min clips, 4 styles (formal, sarcastic, humorous-tech, humorous-non-tech), Fireworks API, LLM-judge.
- Track 3 — Unicorn: no benchmarks; judged on creativity, originality, completeness, AMD platform use, market potential.
- **All submissions must be containerized** (Dockerfile mandatory).
- **Submission fields:** title, short + long description, tags, cover image, video presentation, slide presentation, public GitHub repo with README (runnable per instructions), demo app URL. Original + MIT-compliant.
- **Prizes per track:** $2,500 / $1,500 / $1,000. Referral pool separate ($500/$300/$200; needs ≥100 approved referrals — not worth chasing).
- **Credits:** all participants get $50 Fireworks API hackathon credits; registered after Jul 2 → credits only from Jul 7. New AMD AI Developer Program members separately get $100 AMD Dev Cloud + $50 Fireworks (2–3 day manual approval).
- **Partner challenge:** "Best Use of Gemma Models" (Gemma via Fireworks/AMD Dev Cloud, Apache 2.0). Routing to a local Gemma (bench.py already lists gemma2-2b) could qualify for extra prize with zero architecture change.
- **Stack:** AMD Developer Cloud (AMD GPUs), ROCm, Fireworks AI API. Page recommends local eval before submitting (harness covers this).
- **Support:** AMD Discord `discord.gg/mVUBbE5KjN`, lablab Discord `discord.gg/lablabai`, livestream `twitch.tv/lablabai`.
- **Schedule (EDT):** Jul 6 — 12:00 kickoff, 12:15 Introduction to the Challenge (tasks/models drop), 12:35 Hackathon Guide, 13:00 Discord Q&A. Jul 11 12:00 — End of Submissions.

Facts saved to persistent Claude memory (`amd-hackathon-act2-rules`).

## 6. Deep-Research Skill (in progress at time of writing)

- `/deep-research` skill invoked with query: hybrid routing architectures (FrugalGPT, RouteLLM, LLM cascades, semantic routers), token-saving techniques (LLMLingua, speculative decoding, RadixAttention), Track 1 learning roadmap + architecture blueprint.
- Skill folder had only `SKILL.md` — `scripts/research.py` missing. Rebuilt it (stdlib-only, Gemini Interactions API: POST `/v1beta/interactions` with `agent=deep-research-preview-04-2026`, `background=true`, then poll).
- **Blocked:** `GEMINI_API_KEY` env var present (39 chars, `AIza...` format) but Google rejects it: `API_KEY_INVALID`. Needs a valid key from https://aistudio.google.com/ — or fallback to manual research via web search.

## 7. Outstanding Items

| Item | Priority | Notes |
|------|----------|-------|
| Dockerfile / containerization | **HIGH** | Mandatory for submission |
| Replace `verify.judge_raw` stub | **HIGH** | Flat 0.5 → everything escalates; need logprobs/self-rating signal at kickoff |
| Wire `accuracy_check` into `nodes.account` | HIGH | `correct = True` hardcoded |
| Switch remote to Fireworks | HIGH | Azure works but is dev-only; Fireworks is the scored path |
| Refit calibrator on real data | MED | `calib.json` currently from mock; `CALIB_PATH` empty in `.env` |
| Clean `.env` duplicate keys | LOW | Last-wins works but error-prone |
| Consider Gemma as local model | MED | Side-prize eligibility; re-run bench.py on real scoring env |
| Video + slides + cover image + demo URL | HIGH | Required submission assets, budget time before Jul 11 |
| Valid GEMINI_API_KEY | LOW | Only if deep-research skill wanted |

---

*Generated by Claude Code (Fable 5) — session log for the 2026-07-03 working session. No API keys included.*
