# FrugalRoute — lablab.ai Submission Text
## AMD Developer Hackathon ACT II · Track 1

---

## Project Title
**FrugalRoute — Hybrid Token-Efficient LLM Routing Agent on AMD Instinct MI300X**

---

## Short Description (≤ 160 chars)
Autonomous LLM router: sends tasks to a free local model on AMD MI300X or paid Fireworks API — minimizing paid tokens while holding accuracy above threshold.

---

## Long Description

### The Problem
Every call to a paid LLM API costs tokens. But most tasks don't need a 120B-parameter model. Sentiment classification, factual lookups, simple extractions — a free 7B model handles these correctly. The challenge: make that routing decision autonomously, accurately, and at inference time, without sacrificing accuracy.

### What FrugalRoute Does
FrugalRoute is a **hybrid token-efficient LLM routing agent** that, for each incoming task, decides whether a **free local model** (running on AMD Instinct MI300X) can answer it well enough, or whether to **escalate to a paid remote model** (Fireworks AI). It uses the fewest paid tokens while keeping accuracy above the configured threshold.

### Architecture — 7 Layers of Intelligence

1. **Semantic Triage** (Semantic-Router concept): instant zero-cost categorisation. Easy clusters stay local; blocked content is filtered immediately.
2. **Qdrant Semantic Cache**: vector similarity search over previous answers. Cache hit = 0 paid tokens, always.
3. **Predictive Router** (RouteLLM Matrix Factorization role): estimates P(need_remote) from task text + category. Skips the local call entirely for obviously-hard queries.
4. **Local Inference on AMD MI300X**: Qwen2.5-7B-Instruct served via vLLM with ROCm 7.2.4 and Automatic Prefix Caching (RadixAttention). Free.
5. **Calibrated Confidence Gate** (FrugalGPT cascade + AutoMix POMDP): the local model grades its own answer (free self-rating call). Platt/Isotonic calibration corrects overconfidence bias → reliable P(correct). If P(correct) ≥ threshold, accept local. Done.
6. **LLMLingua-2 Prompt Compression**: before any paid remote call, the prompt is compressed ~50% — directly halving input token cost.
7. **Remote Fallback** (Fireworks AI, OpenAI-compatible): only when the gate fires. Token usage is tracked and reported per task.

### AMD Hardware Story
- **AMD Instinct MI300X** (192 GB HBM3) on AMD Developer Cloud
- **ROCm 7.2.4 + vLLM** — Automatic Prefix Caching (RadixAttention) enabled
- Real calibration run on MI300X: Platt calibrator fitted, ECE 0.303 → 0.002
- Category-aware routing from real inference: classification/math → 100% local; summarization/reasoning → remote
- 61.1% of tasks served FREE from local GPU on real 36-task eval set
- `rocm-smi` GPU utilization verified: 53°C, 216W during inference

### Research Grounding
| Technique | Paper |
|---|---|
| RouteLLM predictive routing | Ong et al. 2024 |
| FrugalGPT cascade | Chen et al. 2023 |
| AutoMix POMDP gate | Madaan et al. 2023 |
| Platt/Isotonic calibration | Platt 1999 / Zadrozny 2001 |
| LLMLingua-2 compression | Pan et al. 2024 |
| Qdrant semantic cache | — |
| RadixAttention/APC | SGLang / vLLM team |

### Key Technical Details
- **Deterministic**: `temperature=0`, pinned pip deps, seeded randoms
- **Graceful degradation**: langgraph, fastembed, qdrant, llmlingua all optional — pure-Python fallbacks keep `python run.py` working with zero extras
- **Containerized**: `docker run` with AMD GPU device flags reads `/data/tasks.jsonl`, writes `/data/out/results.jsonl` (`{id, answer, source, remote_tokens}`)
- **Live dashboard**: React + Framer Motion + Recharts — routing mix, savings, per-category breakdown, KPIs

### Real End-to-End Run Confirmed
Verified on AMD MI300X + Fireworks remote: 3 local / 3 remote / 1 cache hit. Local model self-graded its answers (e.g. summarization confidence 0.35 → correctly escalated). Dashboard shows this run.

---

## Tags / Categories
`LLM Routing`, `Token Efficiency`, `AMD MI300X`, `ROCm`, `vLLM`, `LangGraph`, `FrugalGPT`, `RouteLLM`, `LLMLingua`, `Qdrant`, `Fireworks AI`, `Hybrid AI`, `Cost Optimization`, `Agentic AI`

---

## Tech Stack
- **Hardware**: AMD Instinct MI300X, AMD Developer Cloud
- **Inference**: vLLM + ROCm 7.2.4, Qwen2.5-7B-Instruct
- **Routing**: LangGraph, custom RouteLLM-style predictor, AutoMix POMDP
- **Gate**: Platt/Isotonic calibration, self-rating judge
- **Compression**: LLMLingua-2
- **Cache**: Qdrant + fastembed (BAAI/bge-small-en-v1.5)
- **Remote**: Fireworks AI (OpenAI-compatible) / Azure OpenAI
- **Dashboard**: React, Framer Motion, Recharts (CDN)
- **Container**: Docker, ROCm base image

---

## Demo Application URL
`http://129.212.178.3:8001` _(vLLM endpoint — for judges only)_

Or run locally: `python run.py` + open `dashboard/index.html`

---

## How to Run (copy-paste ready)

### Mock mode (no GPU, no keys — logic demo)
```bash
## GitHub Repository
https://github.com/sharathcherry/frugalroute

---

## Real Results (MI300X, Qwen2.5-7B, 36-task eval)

| Metric | Value |
|---|---|
| Free local % | **52.8%** |
| Paid remote % | **47.2%** |
| Remote tokens used | 828 tokens |
| Calibration ECE | 0.303 → 0.002 (Platt) |
| GPU temp during inference | 53°C |
| GPU power during inference | 216W |
| vLLM model | Qwen2.5-7B-Instruct |
| ROCm version | 7.2.4 |

cd frugalroute
pip install -r requirements.txt
python run.py
# open dashboard/index.html
```

### Docker (submission mode)
```bash
docker build -t frugalroute .
mkdir -p out
docker run --rm \
  --device=/dev/kfd --device=/dev/dri \
  -e REMOTE_BASE_URL=https://api.fireworks.ai/inference/v1 \
  -e REMOTE_API_KEY=<your-key> \
  -e REMOTE_MODEL=accounts/fireworks/models/gpt-oss-120b \
  -v $(pwd)/eval/tasks.sample.jsonl:/data/tasks.jsonl:ro \
  -v $(pwd)/out:/data/out \
  frugalroute
cat out/results.jsonl
```
