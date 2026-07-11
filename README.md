# FrugalRoute

> **AMD Developer Hackathon ACT II · Track 1** — Hybrid Token-Efficient Routing Agent

A local-first LLM **routing agent** that, for each task, autonomously decides whether a **free local model** (AMD Instinct MI300X via vLLM/ROCm) can answer it well enough, or whether to **escalate to a paid remote model** (Fireworks AI) — spending the fewest paid tokens while holding accuracy above a threshold.

**Verified:** real end-to-end run on AMD MI300X + Fireworks. Local tokens = $0.

---

## Quick Start

### Mock mode — no GPU, no keys, no deps

```bash
git clone https://github.com/[your-handle]/frugalroute
cd frugalroute
pip install -r requirements.txt
python run.py               # routes sample tasks, prints token report
# open dashboard/index.html
```

### Submission (batch) mode

```bash
python run.py --input /data/tasks.jsonl --output /data/out/results.jsonl
```

### Docker (scoring harness mode)

```bash
docker build -t frugalroute .
docker run --rm \
  --device=/dev/kfd --device=/dev/dri \
  -e REMOTE_BASE_URL=https://api.fireworks.ai/inference/v1 \
  -e REMOTE_API_KEY=<key> \
  -e REMOTE_MODEL=accounts/fireworks/models/gpt-oss-120b \
  -v $(pwd)/eval/tasks.sample.jsonl:/data/tasks.jsonl:ro \
  -v $(pwd)/out:/data/out \
  frugalroute
```

Output: `/data/out/results.jsonl` — `{id, answer, source, remote_tokens}` per task.

---

## Architecture — Edge-Cloud Pareto-Router

```
Task Input
   │
   ▼
[Triage]          triage.py       Semantic-Router: block / easy-cluster → 0 cost
   │
   ▼
[Semantic Cache]  cache.py        Qdrant + fastembed cosine / difflib fallback → 0 tokens
   │
   ▼
[Predictive Route] predict.py     RouteLLM-style MF: P(need_remote) — skip local if obvious
   │
   ▼
[Local Model]     providers.py    Qwen2.5-7B on AMD MI300X via vLLM (FREE)
   │
   ▼
[Confidence Gate] verify.py       FrugalGPT cascade + Platt/Isotonic calibration
   │ confident                                      |  uncertain
   ▼                                                ▼
[Accept Local]                            [LLMLingua-2 Compress]  compress.py
remote_tokens=0                                     │
                                                    ▼
                                           [Remote Model]  providers.py
                                           Fireworks GPT-OSS-120B (PAID)
```

| Phase | Module | Method |
|---|---|---|
| Semantic triage (zero-cost) | `triage.py` | Semantic-Router concept |
| Semantic cache (zero-cost) | `cache.py` | Qdrant + BGE cosine, difflib fallback |
| Predictive routing | `predict.py` | RouteLLM Matrix-Factorization role |
| Confidence gate | `verify.py` | FrugalGPT cascade |
| Calibration | `calibrate.py` | Platt / Isotonic + ECE / Brier |
| AutoMix POMDP gate | `automix.py` | Bayesian belief, cost-aware escalation |
| Prompt compression | `compress.py` | LLMLingua-2 (~50% compression) |
| Prefix caching | vLLM `--enable-prefix-caching` | RadixAttention / APC |

---

## Calibration + Threshold Tuning

```bash
python eval/harness.py    # fit calib.json, tune CONFIDENCE_THRESHOLD, train PredictiveRouter
```

1. Runs labeled tasks → collects `(raw_confidence, correct)` pairs.
2. Fits Platt + Isotonic calibrators; saves best to `calib.json`.
3. Sweeps threshold → minimum remote calls at ≥ 0.95 accuracy floor → recommends `CONFIDENCE_THRESHOLD`.
4. Fits AutoMix observation model → `automix.json`.
5. Trains `PredictiveRouter`.

Then set `CALIB_PATH=calib.json` + the recommended `CONFIDENCE_THRESHOLD` in `.env`.

---

## AMD MI300X Setup

```bash
# Start vLLM with ROCm + prefix caching
VLLM_HOST_IP=127.0.0.1 python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-7B-Instruct \
  --port 8001 \
  --api-key <key> \
  --enable-prefix-caching \
  --max-model-len 8192
```

Then set `LOCAL_BASE_URL=http://<ip>:8001/v1` in `.env` and `MOCK=0`.

---

## Key `.env` Settings

```ini
MOCK=0
LOCAL_BASE_URL=http://localhost:8001/v1
LOCAL_MODEL=Qwen/Qwen2.5-7B-Instruct
REMOTE_PROVIDER=fireworks
REMOTE_BASE_URL=https://api.fireworks.ai/inference/v1
REMOTE_API_KEY=fw_xxx
REMOTE_MODEL=accounts/fireworks/models/gpt-oss-120b
GATE_MODE=calibrated
CONFIDENCE_THRESHOLD=0.7
CALIB_PATH=calib.json
COMPRESS=1
```

See [INSTRUCTIONS.md](INSTRUCTIONS.md) for the full reference.

---

## Research Implemented

| Paper | Technique | Status |
|---|---|---|
| RouteLLM (Ong et al. 2024) | Predictive router | ✅ |
| FrugalGPT (Chen et al. 2023) | Cascade gate | ✅ |
| AutoMix (Madaan et al. 2023) | POMDP belief gate | ✅ |
| Platt 1999 / Zadrozny 2001 | Confidence calibration | ✅ |
| LLMLingua-2 (Pan et al. 2024) | Prompt compression | ✅ |
| Qdrant semantic cache | Vector similarity cache | ✅ |
| RadixAttention/APC | vLLM prefix caching | ✅ |

---

## Dashboard

`run.py` writes `dashboard/data.js` each run. Open `dashboard/index.html` (no server needed). Shows routing mix, remote token savings, per-category breakdown, KPIs, per-task table.

---

## Deliberately NOT included

- **Speculative decoding on remote** — needs token-level streaming control over the remote server.
- **RadixAttention on remote** — needs control of the remote serving stack.
- **500× compression** — needs target embedding-layer access, incompatible with a closed API.

---

## Author

**Sharath Chandra** — B.Tech CSE-AIML  
AMD Developer Hackathon ACT II · Track 1 · Jul 2026
