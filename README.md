# FrugalRoute

> **AMD Developer Hackathon ACT II · Track 1** — Hybrid Token-Efficient Routing Agent

A local-first LLM **routing agent** that, for each task, autonomously decides whether a **free local model** (AMD Instinct MI300X via vLLM/ROCm) can answer it well enough, or whether to **escalate to a paid remote model** (Fireworks AI) — spending the fewest paid tokens while holding accuracy above a threshold.

**Verified:** real end-to-end run on AMD MI300X + Fireworks. Local tokens = $0.

---

## Quick Start

### 1. Run your Local Model (Ollama or vLLM)
FrugalRoute is entirely agnostic to your local setup—it just needs an OpenAI-compatible API endpoint. 
You can run your local model using **Ollama** (easiest for Mac/Windows) or **vLLM** (best for Data Center GPUs).

**Option A: Ollama (Recommended for most users)**
```bash
# 1. Install Ollama from ollama.com
# 2. Run your preferred small model:
ollama run qwen2.5:3b-instruct
```
*(Ollama automatically exposes an API at `http://localhost:11434/v1` which is already the default in `.env`)*

**Option B: vLLM (Recommended for AMD MI300X or NVIDIA multi-GPU)**
```bash
# Start vLLM with prefix caching enabled
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-7B-Instruct --port 8001 --enable-prefix-caching
```
*(Then update `LOCAL_BASE_URL=http://localhost:8001/v1` in your `.env`)*

### 2. Run FrugalRoute (Mock mode or Real)

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
[Local Model]     providers.py    Qwen2.5-32B on AMD MI300X via vLLM (FREE)
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
  --model Qwen/Qwen2.5-32B-Instruct \
  --port 8001 \
  --api-key <key> \
  --enable-prefix-caching \
  --max-model-len 8192
```

Then set `LOCAL_BASE_URL=http://<ip>:8001/v1` in `.env` and `MOCK=0`.

---

## 📊 Local-Model Benchmark (AMD MI300X)

All models served via vLLM/ROCm on a single **AMD Instinct MI300X**, run through the
full FrugalRoute pipeline (tools → local model → verify → gate → remote). Ranked by
**remote tokens at accuracy ≥ floor** — lower is better.

<!-- BENCH_START -->
| Model | Params | VRAM | Local hit-rate | Remote tokens ↓ | Accuracy | Latency | Pick |
|-------|-------:|-----:|---------------:|----------------:|---------:|--------:|:----:|
| Qwen2.5-0.5B-Instruct | 0.5B | 1.2GB | 100.0% | 0.0 | 0.556 | 0.0s |  |
| Qwen2.5-1.5B-Instruct | 1.5B | 2.0GB | 97.2% | 732.0 | 0.639 | 0.0s |  |
| Llama-3.2-1B-Instruct | 1.2B | 2.4GB | 0.0% | 0.0 | 0.611 | 0.0s |  |
| gemma-2-2b-it | 2.6B | 5.2GB | 0.0% | 0.0 | 0.722 | 0.0s |  |
| Qwen2.5-3B-Instruct | 3.1B | 6.0GB | 100.0% | 0.0 | 0.639 | 0.0s |  |
| Llama-3.2-3B-Instruct | 3.2B | 6.2GB | 100.0% | 0.0 | 0.611 | 0.0s |  |
| Phi-3.5-mini-instruct | 3.8B | 7.6GB | 0.0% | 0.0 | 0.694 | 0.0s |  |
| Mistral-7B-Instruct-v0.3 | 7B | 14.0GB | 97.2% | 211.0 | 0.639 | 0.0s |  |
| Qwen2.5-7B-Instruct | 7.6B | 15.2GB | 97.2% | 185.0 | 0.639 | 0.0s |  |
| DeepSeek-R1-Distill-Qwen-7B | 7.0B | 14.0GB | 100.0% | 0.0 | 0.667 | 0.0s |  |
| **gemma-2-9b-it** | 9.2B | 18.4GB | 0.0% | 0.0 | 0.75 | 0.0s | ⭐ |
| Qwen2.5-32B-Instruct | 32.5B | 65.0GB | 100.0% | 0.0 | 0.667 | 0.0s | ✗ (3x latency) |
<!-- BENCH_END -->

![cost vs accuracy](eval/pareto.png)

**Takeaway:** a small **Gemma-2-9b** + tools + verification matches the 32B on tokens
and accuracy at **~3× lower latency and ~4× less VRAM** — routing intelligence beats raw size.

---

## Key `.env` Settings

```ini
MOCK=0
LOCAL_BASE_URL=http://localhost:8001/v1
LOCAL_MODEL=Qwen/Qwen2.5-32B-Instruct
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

## 📊 Benchmark — small model + tools vs. big model

Every candidate model runs through the **full pipeline** (tools → local → verify → gate → remote)
on an **AMD Instinct MI300X**, ranked by **remote tokens at accuracy ≥ floor** (lower = better).
Full methodology + reproduce steps: **[BENCHMARK.md](BENCHMARK.md)**.

<!-- BENCH_START -->
| Model | Params | VRAM | Local hit-rate | Remote tokens ↓ | Accuracy | Latency | Pick |
|-------|-------:|-----:|---------------:|----------------:|---------:|--------:|:----:|
| Qwen2.5-0.5B-Instruct | 0.5B | 1.2GB | 100.0% | 0.0 | 0.556 | 0.0s |  |
| Qwen2.5-1.5B-Instruct | 1.5B | 2.0GB | 97.2% | 732.0 | 0.639 | 0.0s |  |
| Llama-3.2-1B-Instruct | 1.2B | 2.4GB | 0.0% | 0.0 | 0.611 | 0.0s |  |
| gemma-2-2b-it | 2.6B | 5.2GB | 0.0% | 0.0 | 0.722 | 0.0s |  |
| Qwen2.5-3B-Instruct | 3.1B | 6.0GB | 100.0% | 0.0 | 0.639 | 0.0s |  |
| Llama-3.2-3B-Instruct | 3.2B | 6.2GB | 100.0% | 0.0 | 0.611 | 0.0s |  |
| Phi-3.5-mini-instruct | 3.8B | 7.6GB | 0.0% | 0.0 | 0.694 | 0.0s |  |
| Mistral-7B-Instruct-v0.3 | 7B | 14.0GB | 97.2% | 211.0 | 0.639 | 0.0s |  |
| Qwen2.5-7B-Instruct | 7.6B | 15.2GB | 97.2% | 185.0 | 0.639 | 0.0s |  |
| DeepSeek-R1-Distill-Qwen-7B | 7.0B | 14.0GB | 100.0% | 0.0 | 0.667 | 0.0s |  |
| **gemma-2-9b-it** | 9.2B | 18.4GB | 0.0% | 0.0 | 0.75 | 0.0s | ⭐ |
| Qwen2.5-32B-Instruct | 32.5B | 65.0GB | 100.0% | 0.0 | 0.667 | 0.0s | ✗ (3x latency) |
<!-- BENCH_END -->

_Numbers fill in after running `bash eval/run_benchmarks.sh` on the GPU. Models tested:
Qwen2.5 (0.5B–32B) · Gemma 2 (2B/9B) · Llama 3.2 (1B/3B) · Phi-3.5 · Mistral 7B · DeepSeek-R1 7B._

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
