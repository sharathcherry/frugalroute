# FrugalRoute — Winning-Grade Submission Plan

## ⚠️ TIMELINE REALITY
- **Now:** Jul 11, 2026, ~03:00 UTC (Saturday).
- **Submission deadline:** **Jul 11, 12:00 PM EDT = 16:00 UTC → ~13 hours left.**
- Kickoff was Jul 6. This is the **final sprint**, not prep. Goal order: **(1) get a VALID submitted entry, (2) make it competitive, (3) polish for recognition.** A submitted good entry beats an unsubmitted perfect one.

## 0. BLOCKERS — resolve these first (they gate everything)
1. **Are you registered/enrolled** on lablab.ai for AMD ACT II? If not, do it now.
2. **Do you have the real Track 1 submission spec from the Jul 6 kickoff?** — the exact input/output format the organizers' scoring harness expects, the named models, and the scoring formula (input+output vs output tokens). We built a generic agent; it must match their required interface or it won't score. **Paste that spec to Claude.**
3. **GitHub**: repo must be public. Decide: connect a connector, or you run `git push`.
4. **Compute for scoring**: Track 1 is scored on the organizers' standardized env — you submit a **container**, they run it. Confirm whether the local model is bundled or provided.

---

## 1. What won ACT I — pattern (retrieved + analyzed)
ACT I ran **judged** tracks (AI Agents & Agentic Workflows, Fine-Tuning on AMD GPUs, Vision & Multimodal), $22.5k pool, $5k grand prize, a **Radeon GPU awarded for social engagement**, and a Hugging Face most-liked-Space prize. ~45 finalists. Four patterns:

1. **Agentic/autonomous systems dominated** — multi-agent, "runtime", "copilot", self-verifying loops (Chaos Economy, Research Crew, Adaptive Cognitive Runtime, AIPP, Ukhozi…).
2. **Concrete vertical problems** — medical, finance, security/compliance, EDA (CatalystMD, Credora, Norix, Verixa, AMD-Link, Verilog Fine-Tune…).
3. **A strong AMD-silicon story** — MI300X fine-tuning, chip design, PCB routing. On-brand = memorable to AMD judges.
4. **Build-in-public won its own prizes** — a whole GPU went to social engagement; HF ranking was by community likes. Promotion + demo polish materially changed outcomes.

## 2. How Track 1 winning is DIFFERENT
Track 1 (ACT II) is a **pure leaderboard** — ranked by **remote token count at/above the accuracy floor**, not judged on creativity. So:
- **Rank is decided by the metric**, not the idea. Winning = the most token-efficient router that holds accuracy on the hidden tasks.
- **The ACT I pattern still matters for the *submission wrapper*** — clean repo, crisp demo, live dashboard, and a loud "runs on AMD MI300X via ROCm" story help with recognition, tie-breakers, the social/Hugging-Face-style extras, and your portfolio. You already run on MI300X — lean into it hard.

## 3. THE WINNING FORMULA (Track 1)
Lowest paid tokens at the accuracy floor =
1. **Calibrated gate** — keep as much local as possible without dropping below the bar (fit `calib.json` on real data). *This is your #1 lever and it's not tuned yet.*
2. **Max local coverage** — biggest local model that fits the scoring env (you have a 192GB MI300X to test on).
3. **Ruthless remote-token minimization** — compression, terse output schemas, stop sequences, semantic cache.
4. **Robustness** — no crashes on the hidden env (container tested clean).

---

## 4. THE 13-HOUR SPRINT (hour-boxed · O = owner)

### Block A — Lock the target (now → +1h) · O: You
- [ ] Confirm registration/enrollment.
- [ ] Paste Claude the **real task format + scoring formula + required submission interface** from kickoff. **Everything below adapts to this.**

### Block B — Tune the router (now → +3h, parallel) · O: Claude (on your MI300X)
- [ ] Run calibration harness on the GPU → fit `calib.json`, pick `CONFIDENCE_THRESHOLD`.
- [ ] Fit AutoMix obs model (`automix.json`).
- [ ] Confirm which gate mode wins (calibrated vs automix) on the eval set.
- [ ] If scoring counts input tokens → confirm LLMLingua-2 on; else disable.
- [ ] Re-run pipeline → new dashboard showing improved local-keep %.

### Block C — Match the real interface (+1h → +5h) · O: Claude + You
- [ ] Wrap FrugalRoute to consume the **actual task format** and emit the **required output format** from the kickoff spec.
- [ ] Real `accuracy_check` for the actual task type (replace stub).
- [ ] Local eval run to confirm accuracy ≥ floor at min tokens.

### Block D — Containerize + test clean (+4h → +7h) · O: Claude + You
- [ ] Finalize `Dockerfile` for the router; **bake the local model in** if the scoring env has no network.
- [ ] `docker build` + run on a clean machine (your MI300X droplet is perfect) → confirm it runs from the README instructions alone.
- [ ] Pin versions, seed, `temperature=0`, secrets via env.

### Block E — Repo + assets (+5h → +9h) · O: Claude drafts, You publish
- [ ] Public **GitHub repo**, README + INSTRUCTIONS (done) + WINNING_PLAN.
- [ ] **Slide deck** (problem → architecture → results → AMD story). — Claude builds.
- [ ] **Demo video (~2 min)**: screen-record the dashboard + one live run on MI300X + narrate. — Claude writes script; you record.
- [ ] **Cover image**. — Claude builds.

### Block F — Submit (+9h → deadline) · O: You
- [ ] Fill lablab fields (Claude drafts all text), attach repo + video + slides + demo URL.
- [ ] **Submit before 16:00 UTC.** Leave ≥1h buffer.
- [ ] (Optional) Build-in-public post — the ACT I "social engagement" lever.

---

## 5. Submission checklist (lablab)
- [ ] Project title, short + long description, tech/category tags — *Claude drafts.*
- [ ] Cover image · **video presentation** · **slide presentation**.
- [ ] Public GitHub repo + README (setup + run) — **containerized, runnable**.
- [ ] Demo application platform + application URL.
- [ ] Submitted before **Jul 11, 12:00 PM EDT**.

## 6. Winning extras (borrowed from ACT I)
- **Loud AMD-silicon story:** "local model on AMD Instinct MI300X via ROCm + vLLM, prefix-cache (RadixAttention) hits" — you literally do this. Screenshot `rocm-smi` + the cache-hit logs in the deck.
- **Live dashboard** in the video = instant credibility.
- **Build-in-public** post (X/LinkedIn) — ACT I gave a whole GPU for engagement.
- **Cite the literature** (RouteLLM, FrugalGPT, AutoMix, LLMLingua-2, calibration) — signals depth.

## 7. Risk register
| Risk | Mitigation |
|---|---|
| Our interface ≠ their required submission format | **Get the kickoff spec now**; adapt in Block C |
| Container fails on scoring env | Test clean on the MI300X droplet (Block D) |
| Over-escalation (untuned gate) wastes tokens | Calibration (Block B) — top priority |
| No network in scoring env | Bake local model into the image |
| Run out of time on video/repo | Claude pre-builds all assets; you only record + click |
| GPU credit burn | Stop the droplet when not actively using it |

## 8. If the deadline is actually later / post-submission
- LoRA fine-tune the local model on the MI300X to raise free-coverage.
- Benchmark 0.5B→32B locals to pick the best that fits the scoring env.
- Expand the eval set; re-tune thresholds to the exact formula.
- Portfolio: this maps 1:1 to the KPMG-style "Agentic AI + Azure OpenAI + RAG" JD.

---
**Immediate next action:** (1) You paste the kickoff submission spec + confirm registration. (2) Claude runs calibration on the GPU. (3) Claude builds the deck + video script + container while you record. Then submit.
