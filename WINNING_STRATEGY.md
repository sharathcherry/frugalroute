# FrugalRoute — Updated Winning Strategy
*Anchored to observed ACT I winning-team patterns + your current real state · Jul 11, 2026*

---

## 0. Where you stand right now (real, verified)
- Full agent runs **real** on **AMD MI300X** (Qwen2.5-7B via vLLM/ROCm) + **Fireworks** remote.
- **Category-aware gate calibrated on real GPU data:** classification/math = 100% local, qa/extraction = selfrate-gated, summarization/reasoning = force-remote.
- Latest 36-task run: **remote_tokens ≈ 828, free 52.8%, escalate 47.2%.**
- Submission-ready: batch mode (`--input/--output`), Dockerfile, GitHub repo, calib.json/automix.json from the real run, slide/video/submission text drafted.

**The gap to winning:** ~47% of tasks escalate, driven by **summarization (0%) and reasoning (33%) local accuracy on the 7B model.** That's where the paid tokens go.

---

## 1. What ACT I winners actually did (pattern analysis)
ACT I ran **judged** tracks (AI Agents & Agentic Workflows, Fine-Tuning on AMD GPUs, Vision & Multimodal), $22.5k pool, $5k grand prize, a **Radeon GPU for social engagement**, a Hugging Face most-liked-Space prize. From the ~45 finalists, five repeatable patterns:

1. **Autonomous / agentic framing** — winners were "agents", "runtimes", "copilots" with self-verifying loops, not scripts.
2. **A concrete problem with real numbers** — they showed measured outcomes, not abstract demos.
3. **A loud AMD-silicon story** — MI300X fine-tuning, chip design, PCB routing. On-brand = memorable to AMD judges.
4. **Build-in-public won its own prizes** — an entire GPU went to social engagement; HF ranking was community likes.
5. **Demo polish** — clean repo, 2-min video, a visual that makes the result obvious.

**Critical translation:** ACT I tracks were *judged*. **Track 1 (ACT II) is a pure leaderboard** — ranked by remote tokens at the accuracy floor. So the winning play is **two fronts**: win the *metric*, and *present* like an ACT I winner for recognition, tie-breaks, the social/HF-style extras, and your portfolio.

---

## 2. FRONT A — Win the leaderboard metric (this is what ranks you)
Goal: **lowest remote tokens while holding accuracy ≥ floor.** Levers, ranked by impact for your current state:

### Lever 1 (biggest): bigger local model on the idle MI300X
Your 192GB MI300X is running a 7B and is 95% idle. A **Qwen2.5-32B (or 72B)** almost certainly lifts summarization/reasoning local accuracy → moves them **off force-remote** → **large drop in remote_tokens.** This is the single highest-impact move.
- **Gated on:** the scoring env allowing that model size (rules hint "routing intelligence wins, not raw compute" → it may be capped). **Confirm in Discord first.**
- If capped → skip to Lever 4.

### Lever 2: keep the category-aware gate, re-calibrate on the bigger model
Re-run `eval/harness.py` with the new local model → fresh `calib.json` + category thresholds → the force_local/force_remote sets shift in your favor.

### Lever 3: squeeze remote calls you can't avoid
Confirm LLMLingua-2 compression actually lowers **counted** tokens (only if scoring counts input tokens), terse output schemas, stop sequences, semantic cache for repeats.

### Lever 4 (if model size is capped): lift weak categories on 7B
Better system prompt + few-shot for summarization/reasoning may push local accuracy above the floor → off force-remote. Cheaper than escalating.

**Target:** drive remote_tokens well below 828 at the same or better accuracy. Every lever above is a direct leaderboard gain.

---

## 3. FRONT B — Present like an ACT I winner (recognition + tie-break + portfolio)
Map each ACT I pattern to a concrete move you already can make:

| ACT I winning pattern | Your move (mostly done — make it LOUD) |
|---|---|
| Autonomous/agentic framing | Present FrugalRoute as an autonomous **LangGraph** routing agent with self-verification (it is). |
| Concrete problem + real numbers | Lead every asset with **real MI300X token-savings numbers**, not theory. Show the before/after. |
| Loud AMD-silicon story | Put **`rocm-smi` + vLLM prefix-cache-hit logs + "192GB MI300X"** screenshots in the deck AND video. This is your differentiator — most teams won't have run on real Instinct hardware. |
| Build-in-public won a GPU | Post on X/LinkedIn: dashboard + MI300X shot + one-line result. Tag AMD. Low effort, real upside. |
| Demo polish | 2-min video (script ready) + the live React dashboard. Show one real routing decision on the GPU. |

Plus a Track-1-specific edge: **cite the literature** (RouteLLM, FrugalGPT, AutoMix, LLMLingua-2, calibration) — signals depth few beginner entries have.

---

## 4. Final-hours execution (mapped to your task list)
**MUST (submit a valid entry):** confirm enrollment → real Fireworks key on MI300X → real batch run → record video → **submit before deadline.**
**EDGE (place higher):** confirm scoring-env limits in Discord → **32B local experiment + re-calibrate** → verify compression savings.
**PRESENT:** deck + video emphasize *real numbers + AMD-silicon story + literature depth*; build-in-public post.

Order of operations in the remaining hours:
1. In parallel: you record the video + confirm enrollment; Claude runs the 32B experiment + real batch test on the GPU.
2. If 32B wins and is legal → re-calibrate, re-run, update numbers in deck/dashboard.
3. Freeze, final container build test, push, **submit with ≥1h buffer.**

---

## 5. What "winning-grade" looks like at submission
- ✅ Submitted, **containerized**, reproducible agent that runs from the README alone.
- ✅ **Strong real token-efficiency numbers** on the leaderboard metric (the ranking).
- ✅ **Loud AMD MI300X/ROCm story** with hardware screenshots (recognition edge).
- ✅ Literature-grounded, autonomous **agentic** architecture (depth).
- ✅ Polished **2-min video + live dashboard** (demo).
- ✅ **Build-in-public** post (the ACT I social lever).

---

## 6. Risks & mitigations
| Risk | Mitigation |
|---|---|
| **Assumed spec ≠ real scoring interface** (biggest) | Confirm exact I/O format + token metric in Discord; code is parameterized to swap |
| Bigger local model illegal in scoring env | Confirm size limit first; keep the 7B path as the safe default |
| Over-escalation still too high | Re-calibrate on the chosen model; tune thresholds to sit just above the floor |
| Deadline crunch | MUST-do list first; submit early with buffer; edges only if time |
| Secrets in repo | Already scrubbed via filter-branch + .gitignore — re-verify before final push |

---
**Bottom line:** the metric is won by the **bigger-local-model + re-calibration** move (if the env allows), and the *win-grade presentation* is won by making your **real AMD MI300X story loud** — exactly what ACT I winners did. Do both; submit early.
