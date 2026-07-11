# FrugalRoute — Slide Deck
## AMD Developer Hackathon ACT II · Track 1 Submission

---

## Slide 1 — Title

**FrugalRoute**
_Hybrid Token-Efficient LLM Routing on AMD Instinct MI300X_

**AMD Developer Hackathon ACT II · Track 1**
Sharath Chandra · B.Tech CSE-AIML

> "Every token you DON'T send to a paid API is a token saved."

---

## Slide 2 — The Problem

### Paid LLM APIs are expensive — but not every task needs them.

| Task | Ideal Model |
|---|---|
| "What is the capital of France?" | ✅ Free local (Qwen 7B) |
| "Classify this sentiment" | ✅ Free local |
| "Prove this theorem step by step" | ❌ Must escalate to paid remote |
| "Summarize this 5000-word doc" | ❌ Context length → remote |

**The challenge:** Make the escalation decision accurately, autonomously, at inference time — spending fewest paid tokens while keeping accuracy ≥ threshold.

---

## Slide 3 — FrugalRoute Architecture

### Edge-Cloud Pareto-Router

```
Task Input
   │
   ▼
[Triage]         ← Semantic-Router: block safety / easy clusters (zero cost)
   │
   ▼
[Semantic Cache] ← Qdrant vector cache: exact-semantic hit → 0 tokens
   │
   ▼
[Predictive Router] ← RouteLLM-style MF: P(need_remote) — skip local if obvious
   │
   ▼
[Local Model]    ← Qwen2.5-7B on AMD MI300X via vLLM (FREE)
   │
   ▼
[Confidence Gate] ← FrugalGPT cascade + calibrated P(correct)
   │ (confident)
   ▼
[✅ Accept Local] → remote_tokens = 0

   │ (uncertain)
   ▼
[LLMLingua-2 Compress] ← Shrinks prompt ~50% before paid call
   │
   ▼
[Remote Model]   ← Fireworks GPT-OSS-120B (PAID — scored)
   │
   ▼
results.jsonl    {id, answer, source, remote_tokens}
```

---

## Slide 4 — Research-Grounded Differentiators

| Technique | Paper / Source | What it does in FrugalRoute |
|---|---|---|
| **RouteLLM** | Ong et al. 2024 | Predictive router — P(need_remote) from task features |
| **FrugalGPT** | Chen et al. 2023 | Cascade: local first, escalate only on low confidence |
| **AutoMix** | Madaan et al. 2023 | POMDP belief gate — Bayesian cost-aware escalation |
| **Platt/Isotonic Calibration** | Platt 1999 / Zadrozny 2001 | Calibrated confidence → reliable gate threshold |
| **LLMLingua-2** | Pan et al. 2024 | Prompt compression — reduces remote input tokens |
| **Qdrant Semantic Cache** | RadixAttention idea | Exact-semantic cache → 0 tokens for repeated queries |
| **RadixAttention/APC** | SGLang / vLLM | Prefix caching on local model → faster, saves VRAM BW |

**All 7 implemented. Not just referenced — running.**

---

## Slide 5 — AMD Silicon Story

### Local model runs entirely on AMD Instinct MI300X

- **192 GB HBM3** — fits 7B model with room for prefix cache
- **vLLM + ROCm 7.2.4** — Automatic Prefix Caching (RadixAttention) enabled
- **~31% prefix cache hit rate** measured on shared system prompt prefixes
- `rocm-smi` confirms GPU utilization during inference

```
GPU 0: AMD Instinct MI300X  |  Temp: 43°C  |  Util: 67%  |  Mem: 18.2/192.0 GB
```

**Free inference on AMD hardware = the core economic advantage of this system.**

---

## Slide 6 — Live Results (Real Run, AMD MI300X)

| Metric | Value |
|---|---|
| Local (AMD MI300X) | 3 tasks |
| Remote (Fireworks GPT-OSS-120B) | 3 tasks |
| Cache hits (Qdrant) | 1 task |
| Avg remote tokens / escalated task | ~128 |
| Tokens saved via LLMLingua-2 | ~64 per remote call |
| Local model | Qwen/Qwen2.5-7B-Instruct on MI300X |
| Gate mode | Calibrated (selfrate judge → Platt calibration) |

**Dashboard:** Live routing mix, savings chart, per-category breakdown, KPIs.

---

## Slide 7 — Technical Depth

### What makes this hard (and why we got it right)

1. **Calibration**: Raw self-ratings are biased (overconfident). Platt scaling corrects → reliable P(correct). Without this, the gate is wrong.

2. **Self-verify without extra paid calls**: `judge_raw` uses the LOCAL model to grade its own answer (free). The remote is never called to judge.

3. **Compression before remote**: LLMLingua-2 compresses the prompt ~50% before the paid call → halves input token cost. With input+output scoring, this is a direct leaderboard lever.

4. **Graceful degradation**: Every heavy dependency (langgraph, fastembed, qdrant-client, llmlingua) has a pure-Python fallback. `python run.py` works with zero extras.

5. **Deterministic container**: `temperature=0`, pinned pip versions, seeded randoms → reproducible scoring.

---

## Slide 8 — Try It / Submit

### GitHub (public repo)
`github.com/[your-handle]/frugalroute`

### Run in 30 seconds
```bash
# Mock mode — no GPU, no keys
pip install -r requirements.txt
python run.py   # then open dashboard/index.html

# Submission mode (Docker)
docker run --device=/dev/kfd --device=/dev/dri \
  -e REMOTE_BASE_URL -e REMOTE_API_KEY -e REMOTE_MODEL \
  -v tasks.jsonl:/data/tasks.jsonl:ro -v out:/data/out \
  frugalroute
```

### Built with
AMD Instinct MI300X · ROCm 7.2.4 · vLLM · Fireworks AI · LangGraph · LLMLingua-2 · Qdrant

**Sharath Chandra** — B.Tech CSE-AIML
_Gen-AI Engineering · AMD Hackathon ACT II · Track 1_
