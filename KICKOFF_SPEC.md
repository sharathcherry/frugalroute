# Track 1 — Kickoff Submission Spec (ASSUMED)

> ⚠️ **This is a reconstructed/assumed spec**, derived from the AMD ACT II Track 1
> rules (not the official kickoff doc, which was not available). Build against this
> now; **reconcile with the organizers' official spec** the moment you have it.
> Where the official spec differs, it wins — the code is parameterized so swapping
> paths/schemas/flags is trivial.

---

## 1. Challenge (from the public rules)
- Build an agent that, for each task, autonomously chooses a **free local model** or a **paid remote model** (Fireworks), minimizing paid tokens while staying above an accuracy threshold.
- **All submissions must be containerized.**
- Tasks + exact models are revealed at kickoff. **Local tokens count as zero.**
- Final scoring runs on a **standardized environment** only; the local model must fit it.
- Judging: **token count + output accuracy** (leaderboard).

## 2. Submission artifact
A **Docker image** (or a repo with a `Dockerfile` the organizers build) that runs the routing agent over a provided task set and produces answers, with remote token usage measured.

## 3. Runtime contract (assumed)

### Invocation
```bash
docker run --rm \
  -e REMOTE_BASE_URL -e REMOTE_API_KEY -e REMOTE_MODEL \
  -v /path/tasks.jsonl:/data/tasks.jsonl:ro \
  -v /path/out:/data/out \
  <image>   # entrypoint reads /data/tasks.jsonl, writes /data/out/results.jsonl
```
(GPU flags for local model: `--device=/dev/kfd --device=/dev/dri` on the AMD env.)

### Input — `/data/tasks.jsonl` (one JSON per line)
```json
{"id": "t1", "task": "Classify the sentiment: 'I love this.'"}
{"id": "t2", "task": "Summarize: ..."}
```
(Field may be `task` or `prompt`; possibly a `type`/`category`. Parameterized in code.)

### Output — `/data/out/results.jsonl` (one JSON per line, same ids)
```json
{"id": "t1", "answer": "positive", "source": "local", "remote_tokens": 0}
{"id": "t2", "answer": "...", "source": "remote", "remote_tokens": 128}
```
- `answer` — the final answer used for accuracy scoring.
- `source` — `local` | `remote` | `cache` (informational).
- `remote_tokens` — paid tokens used for this task (0 if answered locally/cached).

### Remote model access (provided by organizers via env)
- `REMOTE_BASE_URL`, `REMOTE_API_KEY`, `REMOTE_MODEL` — OpenAI-compatible (Fireworks).
- Assume the container may reach ONLY this endpoint (no general internet).

### Local model
- **Bundled inside the image** (weights baked in) OR loaded from a mounted cache — assume **no network to download at runtime**. Served in-process or via a local vLLM/SGLang started by the entrypoint.
- Must fit the standardized-env GPU (unknown size → keep a small default, e.g. Qwen2.5-3B/7B, plus a config to scale up if the env is a full MI300X).

### Resource / time limits (assume)
- One GPU (MI300X-class), a per-task and/or total time budget. Local model must be fast enough not to time out.

## 4. Scoring (assumed)
- **Primary:** total `remote_tokens` summed over all tasks — **lower is better.**
- **Gate:** overall accuracy must be **≥ threshold** (assume ~0.90–0.95). Below → penalized/disqualified.
- **Token definition:** assume **input + output** remote tokens are counted (so prompt compression helps). *Confirm — if output-only, disable compression weighting.*
- **Tie-break:** likely latency or accuracy.

## 5. Local vs remote accounting
- **Local** (own model, any size that fits the env) and **cache hits** = **0 tokens**.
- **Remote** (Fireworks) = counted tokens (input+output assumed).

## 6. Container contract
- `Dockerfile` builds an image that runs from README instructions alone.
- Entry point: `python run.py --input /data/tasks.jsonl --output /data/out/results.jsonl`.
- Reads remote creds from env; loads local model from baked-in weights.
- Deterministic: `temperature=0`, pinned versions, seeded.

## 7. How FrugalRoute maps to this
Already implemented: routing, calibrated gate, cache, compression, remote providers, token accounting. **Adaptation needed for submission (small):**
1. **Batch entrypoint** — add `--input/--output` file mode to `run.py` emitting `results.jsonl` with `id, answer, source, remote_tokens` (currently prints + writes dashboard). ~30 min.
2. **Bake the local model** into the image (or vLLM sidecar started by entrypoint) — no runtime download.
3. **Real `accuracy_check`** for the actual task type (replace stub) once the format is known.
4. **Fit `calib.json`** on the real tasks; set tuned `CONFIDENCE_THRESHOLD`.

## 8. Example
Input:
```json
{"id":"1","task":"What is the capital of France?"}
{"id":"2","task":"Explain step by step why the sky is blue."}
```
Output (FrugalRoute):
```json
{"id":"1","answer":"Paris","source":"local","remote_tokens":0}
{"id":"2","answer":"...scattering...","source":"remote","remote_tokens":142}
```

## 9. Open questions to confirm with organizers (ask in Discord)
1. Exact **input/output file paths + schema** (field names, ids).
2. **Token metric:** input+output or output-only? Are the local self-grade calls counted? (They shouldn't be — local is free — but confirm.)
3. **Accuracy threshold** value + how accuracy is computed (exact match / judge / per-type).
4. **Standardized env specs:** GPU/VRAM, per-task/total **time limit**, **network policy** (any egress besides the remote endpoint?).
5. Is the **remote endpoint/model** the same Fireworks account, or organizer-provided keys?
6. How is the submission delivered — **prebuilt image**, or repo they `docker build`?

---
**Next:** implement the batch entrypoint (#7.1) and a Dockerfile that bakes the local model, so we have a submittable container that matches this contract. Swap in the official schema when available.
