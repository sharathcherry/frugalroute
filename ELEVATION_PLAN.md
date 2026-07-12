# FrugalRoute — Elevation Plan (to recognized / winning-grade)

**Honest positioning:** strong engine, top-tier for a beginner Track-1 entry, but ~60–70% of the way to a *recognized* research-grade project. The gap is **credibility (real benchmarks + Pareto), polish (bug-free core + hosted demo), and narrative.** This plan closes it.

---

## HORIZON A — Lock the deadline submission (do NOT skip)
Whatever else happens, submit the current strong version so the work counts.
- [ ] Rotate the leaked Fireworks key; confirm `.env` / `MASTER_HANDOFF.md` are NOT in the public repo.
- [ ] One real batch run on MI300X → `results.jsonl`; **record accuracy vs floor** (not just tokens).
- [ ] Regenerate dashboard from the real run; record 2-min video.
- [ ] Submit on lablab with a buffer.
**Acceptance:** a valid, submitted entry exists. Everything below is elevation on top.

---

## HORIZON B — Elevate to recognized-grade (the "give it my best" work)

### B1. Credible benchmark results — the #1 credibility lever
Replace the homemade 36-task set with **standard, citable benchmarks.**
- [ ] Run FrugalRoute on **MT-Bench, GSM8K, MMLU (subset), and a routing set (RouteLLM's Chatbot-Arena / RouterBench)**.
- [ ] Report **accuracy + % handled local + remote-token cost** per benchmark.
- **Acceptance:** results on ≥2 public benchmarks, numbers anyone can reproduce.

### B2. The money chart — cost-vs-accuracy Pareto
- [ ] Produce a single figure: accuracy (y) vs remote-token cost (x), plotting:
  all-remote · all-local · random routing · naive length/keyword threshold · **RouteLLM-MF** · **FrugalRoute**.
- [ ] Show FrugalRoute on/above the Pareto frontier (e.g., "95% of GPT-4-class accuracy at 30% of the cost").
- **Acceptance:** the chart proves you beat naive routing and approach frontier accuracy far cheaper. This is *the* slide.

### B3. Harden the routing core (fix the leaks)
- [ ] Replace brittle keyword category detection with the **embedding/predictive router** (already have `predict.py` + fastembed) — the "how many continents → math → 279 tokens" class of bug disappears.
- [ ] **Cap remote `max_tokens`** + enforce terse output schemas (that 279-token answer to a 1-word question is pure waste).
- [ ] Turn on the **real semantic cache** (fastembed/Qdrant; it's showing 0 hits) and verify hits on repeats.
- [ ] Confirm **real LLMLingua-2** is loaded (not the extractive fallback); measure compression savings.
- [ ] Add a small **test suite** (pytest) for the router decisions + accuracy_check.
- **Acceptance:** no mis-routing on the eval set; remote tokens drop; tests green.

### B4. Hosted, reproducible demo — where recognition comes from
- [ ] A **Hugging Face Space** (or live URL) — paste a query, watch it triage local↔remote with the live token counter + the dashboard.
- [ ] One-command reproducible container + a `make bench` that regenerates the Pareto chart.
- **Acceptance:** a stranger can try it and reproduce your numbers.

### B5. Robustness / honesty
- [ ] Test on **held-out + adversarial / out-of-distribution** tasks; report where it fails (recognized projects are honest about limits).
- [ ] Sensitivity: how the Pareto shifts with threshold, model size, compression.
- **Acceptance:** a "limitations" section backed by data.

### B6. Narrative + writeup (sell the result)
- [ ] A **blog post / technical writeup**: "Cut LLM inference cost ~60% at equal accuracy on AMD MI300X" — problem, method, the Pareto chart, reproducibility.
- [ ] **Build-in-public** thread (X/LinkedIn) with the chart + MI300X shot, tag AMD. (ACT I rewarded this with a GPU.)
- [ ] Loud **AMD-silicon story**: `rocm-smi`, 192GB, prefix-cache hit rate, MI300X throughput.
- **Acceptance:** a shareable artifact that makes the result obvious in 30 seconds.

### B7. (Optional research edge)
- [ ] LoRA-fine-tune / distill a **dedicated router classifier** on the MI300X and show it beats prompt-based routing on the Pareto — a genuine contribution.

---

## Priority order (highest leverage first)
1. **B2 Pareto chart** (+ B1 benchmark to feed it) — turns "cool" into "credible."
2. **B3 harden core** — removes the embarrassing leaks; improves the numbers feeding B2.
3. **B4 hosted demo** — the recognition/engagement lever.
4. **B6 writeup + build-in-public** — sells it.
5. B5 robustness, B7 research edge — depth if time.

## The one-line test for "recognized-grade"
*Can a stranger, in 2 minutes, see a Pareto chart proving you cut cost ~60% at equal accuracy on real AMD hardware, and reproduce it from your repo?* When the answer is yes, you're there.
