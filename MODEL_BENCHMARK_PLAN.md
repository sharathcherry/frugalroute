# FrugalRoute — Small-Model Benchmark Plan (for the README)

**Goal:** benchmark a slate of best-in-class **small open-weight models** (Gemma + others) *inside the full FrugalRoute pipeline* (tools + verify + gate), on the **AMD MI300X**, and publish a clean **cost-vs-accuracy table** on the GitHub README. The table should prove the thesis: **small model + tools + verification ≈ big-model accuracy at a fraction of the tokens/latency.**

---

## 1. Candidate models (by size tier — pick what runs on your stack)
All served locally via vLLM/ROCm (or Ollama) on the MI300X; each is the *free* tier.

| Tier | Model | ~Params | ~VRAM (fp16) | Why it's a candidate |
|---|---|---|---|---|
| XS | `Qwen2.5-0.5B-Instruct` | 0.5B | ~1 GB | floor / latency baseline |
| XS | `SmolLM2-1.7B-Instruct` | 1.7B | ~3.5 GB | strong tiny model |
| XS | `Llama-3.2-1B-Instruct` | 1B | ~2 GB | Ryzen-APU tier story |
| S | `Gemma-2-2b-it` | 2.6B | ~5 GB | **Gemma small, punches up** |
| S | `Qwen2.5-3B-Instruct` | 3B | ~6 GB | strong all-rounder |
| S | `Llama-3.2-3B-Instruct` | 3B | ~6 GB | popular baseline |
| S | `Phi-3.5-mini-instruct` | 3.8B | ~8 GB | reasoning-dense small |
| M | `Gemma-2-9b-it` | 9B | ~18 GB | **Gemma mid — likely sweet spot** |
| M | `Qwen2.5-7B-Instruct` | 7B | ~15 GB | your current-known-good |
| M | `Mistral-7B-Instruct` / `Ministral-8B` | 7–8B | ~16 GB | alt family |
| M | `DeepSeek-R1-Distill-Qwen-7B` | 7B | ~15 GB | reasoning-tuned (hard categories) |
| L (control) | `Qwen2.5-32B-Instruct` | 32B | ~65 GB | **big-model control — show it's NOT worth it** |

> Note: confirm exact HF IDs + vLLM-ROCm support before running; some Gemma 3 / newer IDs may need a specific vLLM version. The 32B stays in as a *control* to make the "small wins" point.

---

## 2. Metrics to record (per model)
Run each model through the **full pipeline** (tools → small LLM → verify → gate → remote) on the labeled eval set, at the **tuned threshold** (from `eval/harness.py`), and log:

- **Local hit-rate** — % of tasks answered at **0 remote tokens** (tools + accepted local).
- **Remote tokens** — total paid tokens over the set (**the leaderboard metric**).
- **Accuracy** — overall + **per-category** (classification / extraction / math / qa / summarization / reasoning). Must be ≥ the accuracy floor to count.
- **Avg latency / tokens-per-sec** — throughput on the MI300X.
- **VRAM used** — from `rocm-smi`.
- **With-tools vs no-tools** (optional second run) — to quantify how much the tool tier adds.

Ranking key: **lowest remote tokens at accuracy ≥ floor**, tie-break by latency, then smaller VRAM.

---

## 3. Methodology / harness (what to build)
Extend the existing `eval/bench.py` + `eval/harness.py` into a **sweep**:

**New: `eval/run_benchmarks.sh`** (runs on the MI300X)
```
for MODEL in "${MODELS[@]}"; do
  1. serve $MODEL on vLLM (port 8001), health-poll
  2. LOCAL_MODEL=$MODEL python3 eval/harness.py       # fit calib.json for this model, get threshold
  3. LOCAL_MODEL=$MODEL python3 run.py --input eval/tasks.jsonl --output out/$MODEL.jsonl
  4. record: local%, remote_tokens, per-cat accuracy, latency, VRAM  -> eval/benchmark.json
  5. docker stop the vLLM container (free VRAM), next model
done
```

**New: `eval/make_readme_table.py`**
```
reads eval/benchmark.json  -> writes a sorted markdown table
                           -> injects it into README between markers:
<!-- BENCH_START --> ... auto-generated table ... <!-- BENCH_END -->
```
(so re-running updates the README automatically, no manual editing)

Also emit **`eval/pareto.png`** (matplotlib) — accuracy (y) vs remote-tokens (x), one dot per model + the tools-only point — the "money chart" for the README.

---

## 4. README section (target output)
Add this block to `README.md`:

```markdown
## 📊 Local-Model Benchmark (AMD MI300X)

All models served via vLLM/ROCm on a single **AMD Instinct MI300X**, run through the
full FrugalRoute pipeline (tools → local model → verify → gate → remote). Ranked by
**remote tokens at accuracy ≥ floor** — lower is better.

<!-- BENCH_START -->
| Model | Params | VRAM | Local hit-rate | Remote tokens ↓ | Accuracy | Latency | Pick |
|-------|-------:|-----:|---------------:|----------------:|---------:|--------:|:----:|
| Gemma-2-9b-it       | 9B  | 18GB | 78% | 412 | 0.94 | 0.6s | ⭐ |
| Qwen2.5-7B-Instruct | 7B  | 15GB | 74% | 501 | 0.93 | 0.5s |    |
| Gemma-2-2b-it       | 2.6B| 5GB  | 69% | 640 | 0.91 | 0.3s |    |
| ...                 | ... | ...  | ... | ... | ...  | ...  |    |
| Qwen2.5-32B (control)| 32B| 65GB | 79% | 405 | 0.94 | 1.9s | ✗ (3× latency, ~same tokens) |
<!-- BENCH_END -->

![cost vs accuracy](eval/pareto.png)

**Takeaway:** a small **Gemma-2-9b** + tools + verification matches the 32B on tokens
and accuracy at **~3× lower latency and ~4× less VRAM** — routing intelligence beats raw size.
```
*(Numbers above are illustrative placeholders — the real ones come from the run.)*

---

## 5. Execution order (time-boxed on the MI300X)
Each model ≈ download + serve + harness + eval + teardown (~10–20 min). Full sweep ≈ 2–3 h.
1. **Core 5 first** (fast, high value): `Gemma-2-2b`, `Gemma-2-9b`, `Qwen2.5-3B`, `Qwen2.5-7B`, `Phi-3.5-mini`.
2. Add `Llama-3.2-3B`, `SmolLM2-1.7B`, `DeepSeek-R1-Distill-Qwen-7B`.
3. Run the **32B control** last (proves the point).
4. `make_readme_table.py` → commit the table + `pareto.png` → push.

Prereq: the **tools + verification tier** should exist first (otherwise you're benchmarking the weaker LLM-only pipeline). If not built yet, add it before the sweep — it's what makes the small models competitive.

---

## 6. The story the table tells (why judges/recruiters care)
- **Reproducible, standard-ish methodology** on **real AMD hardware** → credible, not a toy.
- **Small model + tools ≈ big model** → the core research insight, shown with data.
- A **Pareto chart** anyone can grok in 5 seconds.
- Loud **MI300X / ROCm / vLLM** framing → the AMD-silicon story ACT I winners used.

---
**Next:** build (a) the tools+verify tier, (b) `run_benchmarks.sh` + `make_readme_table.py` + `pareto.png`, then run the core-5 sweep on your MI300X and auto-fill the README table.
