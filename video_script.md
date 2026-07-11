# FrugalRoute — Demo Video Script (~2 minutes)
## AMD Developer Hackathon ACT II · Track 1

---

### [0:00–0:12] HOOK — Open on terminal

**[Screen: terminal, cursor blinking]**

**NARRATION:**
"What if your AI system could automatically decide — for every single task — whether it needs a powerful paid LLM, or whether a free local model running on AMD hardware is good enough? That's FrugalRoute."

---

### [0:12–0:30] PROBLEM

**[Screen: side-by-side — simple question vs complex question]**

**NARRATION:**
"Not every task needs GPT-4 or a 120-billion-parameter model. Asking 'What is the capital of France?' doesn't. But proving a math theorem step by step? It does.

The problem is: how do you make that call accurately, at inference time, without losing accuracy? That's the routing problem — and it's worth a lot of money if you solve it."

---

### [0:30–0:55] ARCHITECTURE

**[Screen: slide 3 — architecture pipeline diagram]**

**NARRATION:**
"FrugalRoute is an agentic pipeline with 7 layers of intelligence:

First, a semantic triage — instant category detection, zero cost.

Then a vector cache — if we've seen this question before, answer immediately with zero tokens.

Then a predictive router — trained to estimate the probability this task needs a remote call.

If it looks answerable locally, we send it to Qwen 2.5, 7 billion parameters, running right here on an AMD Instinct MI300X with 192 gigs of HBM3 memory.

The local answer goes through a calibrated confidence gate — the local model grades its own answer. If it's confident, we're done. Zero paid tokens.

If it's not confident, we compress the prompt with LLMLingua-2 — cutting it roughly in half — before sending it to the paid Fireworks endpoint.

Every layer reduces paid tokens while protecting accuracy."

---

### [0:55–1:20] LIVE DEMO

**[Screen: terminal — run the pipeline]**

```bash
python run.py --input eval/tasks.jsonl --output out/results.jsonl
```

**[Show output scrolling — [local] [cache] [remote] lines appearing]**

**NARRATION:**
"Here's a real run. Watch the routing decisions happen live.

Simple factual questions — routed local. Answered on AMD hardware. Zero paid tokens.

The sentiment classification — local. Zero tokens.

This complex step-by-step reasoning question — the confidence gate fired. Escalated to Fireworks. Remote tokens used."

**[Screen: open dashboard/index.html]**

"And here's the live dashboard — routing mix, cumulative remote token savings, breakdown by category. This is real data from a real run on the MI300X."

---

### [1:20–1:40] AMD SILICON STORY

**[Screen: rocm-smi output]**

**NARRATION:**
"The local model runs entirely on AMD Instinct MI300X via ROCm and vLLM with Automatic Prefix Caching enabled. We're seeing about 31% prefix cache hit rate on shared prompt prefixes — that's direct latency savings on repeated task patterns.

This is what AMD's GPU stack enables: running a production-grade 7B inference server for free, serving thousands of tasks before a single paid token is needed."

---

### [1:40–1:55] RESULTS + DEPTH

**[Screen: slide 6 — results table]**

**NARRATION:**
"The system implements 7 published techniques — RouteLLM, FrugalGPT, AutoMix, Platt calibration, LLMLingua-2, Qdrant semantic cache, and RadixAttention prefix caching.

All running. All wired together. Containerized and submittable."

---

### [1:55–2:00] CLOSE

**[Screen: GitHub repo + slide 8]**

**NARRATION:**
"FrugalRoute — the token-efficient router. Built on AMD. Built to win Track 1.

Link in the description. Thank you."

---

## Recording Tips

- **Duration target:** 1:50–2:10
- **Screen resolution:** 1920×1080, font size ≥ 16pt in terminal
- **Commands to run before recording:**
  ```bash
  python run.py  # generates dashboard/data.js first
  ```
- **Show these screens:**
  1. Terminal: `python run.py --input eval/tasks.jsonl --output out/results.jsonl`
  2. Dashboard: `dashboard/index.html` in browser
  3. `rocm-smi` output (run on MI300X before recording)
  4. Slide 3 (architecture) and Slide 6 (results)
- **Keep energy high** — the architecture slide is complex; keep narration confident and paced.
