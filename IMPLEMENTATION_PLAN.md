# FrugalRoute — Implementation Plan (final sprint)

**Deadline:** Jul 11, 12:00 PM EDT (16:00 UTC).
**Guiding principle:** _Bank a valid, submitted 7B entry FIRST. Optimize only after. Accuracy ≥ floor is a hard gate on every change — lower tokens only counts if accuracy holds._

Legend: **[You]** human-only · **[Claude]** I can run it on the MI300X/sandbox · ✅ = acceptance gate.

---

## PHASE 0 — Preconditions (do immediately, in parallel)
- **[You]** Confirm you're **enrolled** on lablab for ACT II Track 1 and can open the submission form. ✅ *Form reachable.*
- **[You]** Ask in **AMD/lablab Discord** and record the answers (these decide Phase 5):
  1. **What GPU/VRAM does the standardized scoring environment provide?** (Not "is there a size limit" — the actual VRAM. A 32B is only safe if their scoring GPU fits it.)
  2. **Per-task / total time limit?**
  3. **Tokens counted: input+output or output-only?** (Decides if compression helps.)
  4. **How is the agent invoked** (exact input/output file paths + schema) and **is the local model bundled** or provided?
- **[You]** Put the **real Fireworks key** in the container `.env`:
  ```bash
  ssh -i c:\Users\katuk\.ssh\frugalroute_amd root@129.212.178.3
  docker exec frugal-vllm sh -c 'sed -i "s|REMOTE_API_KEY=.*|REMOTE_API_KEY=fw_REAL|" /frugalroute/.env'
  ```
  ✅ *A remote Fireworks call returns 200.*

---

## PHASE 1 — Bank the 7B baseline (the guaranteed entry) · [Claude]
Goal: a valid, real `results.jsonl` + real numbers, committed and tagged, so we always have something to submit.
```bash
# inside container, clear stale bytecode (known MOCK-pyc bug), run real batch
docker exec frugal-vllm sh -c 'cd /frugalroute && find . -name __pycache__ -type d -exec rm -rf {} + ; \
  python3 run.py --input eval/tasks.jsonl --output out/results.jsonl'
```
✅ **Gates (ALL must pass):**
1. `out/results.jsonl` has one `{id,answer,source,remote_tokens}` line per task, valid JSON.
2. **Accuracy ≥ floor** (run harness / accuracy_check on the labeled set) — record the number.
3. `remote_tokens` total recorded = **BASELINE** (currently ~828).
4. `git commit` + `git tag v1-baseline-7b` + push.

_This tag is the fallback we can always ship._

---

## PHASE 2 — Container reproducibility · [Claude]+[You]
Prove the scoring harness can build+run it.
```bash
# on the droplet host (not inside frugal-vllm)
cd /frugalroute && docker build -t frugalroute-sub .
docker run --rm --device=/dev/kfd --device=/dev/dri \
  -e REMOTE_BASE_URL -e REMOTE_API_KEY -e REMOTE_MODEL \
  -v $PWD/eval/tasks.jsonl:/data/tasks.jsonl:ro -v $PWD/out:/data/out \
  frugalroute-sub --input /data/tasks.jsonl --output /data/out/results.jsonl
```
✅ Builds clean, runs from README instructions alone, produces valid `results.jsonl`, **no secrets baked in** (`docker history`/scan).

---

## PHASE 3 — Refresh submission assets with REAL numbers · [Claude]+[You]
- **[Claude]** Regenerate `dashboard/data.js` from the **real Phase-1 run** (current one still shows mock `qwen2.5:3b`/`llama` — must show real MI300X numbers).
- **[Claude]** Update `submission_text.md` + `slide_deck.md`: real token-savings %, `rocm-smi` + prefix-cache-hit screenshots, literature citations (ACT I "real metrics + AMD-silicon" pattern).
- **[You]** Capture 2–3 screenshots on the droplet: `rocm-smi`, vLLM cache-hit log, a live run.
- **[You]** Record the **2-min video** (`video_script.md`): run → dashboard → MI300X shot.
✅ Assets reference the real baseline numbers; video recorded.

---

## PHASE 4 — SUBMIT the 7B baseline EARLY · [You]
Do NOT wait for the 32B experiment.
1. lablab form → paste `submission_text.md`, GitHub URL, cover image, slides, video.
2. **Submit with ≥1h buffer.**
✅ **Confirmed submitted.** _From here, everything else is upside._

---

## PHASE 5 — 32B upgrade (ONLY if Phase-0 answer allows + time remains) · [Claude]
**Gate to start:** scoring-env VRAM ≥ ~70GB (fits a 32B) AND no tight per-task timeout AND ≥3h to deadline.

**Test WITHOUT rebuilding the image** (fast, reversible):
```bash
# serve 32B on a second port on the MI300X (192GB fits it easily)
docker exec -d frugal-vllm sh -c 'VLLM_HOST_IP=127.0.0.1 vllm serve Qwen/Qwen2.5-32B-Instruct \
  --host 0.0.0.0 --port 8002 --api-key frugal-amd-7k2x --enable-prefix-caching --max-model-len 8192'
# point the pipeline at it + re-fit
docker exec frugal-vllm sh -c 'cd /frugalroute && \
  LOCAL_MODEL=Qwen/Qwen2.5-32B-Instruct LOCAL_BASE_URL=http://127.0.0.1:8002/v1 \
  python3 eval/harness.py'   # -> new per-category accuracy + calib.json
```
Then:
1. **Re-derive** `FORCE_LOCAL` / `FORCE_REMOTE` category sets from the **32B** per-category accuracy (do NOT reuse the 7B sets).
2. Re-run the batch with the 32B config.
✅ **Promotion gate (BOTH required):**
   - `remote_tokens` **<** baseline (828), **AND**
   - accuracy **≥ floor** (same or better than baseline).
   If both pass → bake 32B into the image (`docker-entrypoint.sh` default `HF_MODEL`), rebuild, re-run Phase 2, `git tag v2-32b`, **resubmit**.
   If either fails or time is short → **keep the 7B baseline. No change.**

**Fallback if 32B prohibited (7B-only): Phase 5b** · [Claude]
- Expand `prompts.py` `SYSTEM_PREFIX`/`FEWSHOT` with summarization + reasoning guidance (cached by APC → free accuracy).
- Re-run harness → if summarization/reasoning accuracy clears the floor, move them off `FORCE_REMOTE`.
- Same promotion gate: tokens ↓ AND accuracy ≥ floor.

---

## PHASE 6 — Squeeze remaining remote tokens (if time) · [Claude]
- Confirm the **real LLMLingua-2** is loaded in the container (not the extractive fallback); measure tokens saved on remote calls. Only pursue if scoring counts **input** tokens.
- Confirm semantic cache is on real embeddings (fastembed/Qdrant), not difflib; `cache_hits` currently 0.
✅ Any change must pass the tokens↓ / accuracy≥floor gate before promotion.

---

## PHASE 7 — Freeze & finalize · [You]+[Claude]
- Final `git push`; verify `.gitignore` still excludes `.env`, keys, `calib_log.jsonl`.
- If an improved version (v2) was promoted and re-verified → **resubmit** before deadline.
- **[You] Stop the MI300X droplet** to end billing once done.

---

## Global verification gates (apply to EVERY change)
| Gate | Check |
|---|---|
| Valid output | `results.jsonl` well-formed, one line per task id |
| **Accuracy** | ≥ floor on labeled set (hard gate — never trade accuracy for tokens) |
| Tokens | total `remote_tokens` **<** current baseline |
| Reproducible | clean `docker build` + run from README only |
| No secrets | `.env`/keys not in repo or image |

## Rollback
- Every promotable change is a git tag. If anything regresses, `git checkout v1-baseline-7b` and ship that.
- The 7B baseline submitted in Phase 4 is the floor — nothing after can make the outcome worse than "submitted, valid, working."

## Decision points (fast)
1. Phase 0 Discord answer → Phase 5 (32B) vs Phase 5b (7B prompt-tune) vs neither.
2. Phase 5 promotion gate → resubmit v2 vs keep v1.
3. Time check before each optional phase → if <2h to deadline, stop optimizing, ensure v1 is submitted.
