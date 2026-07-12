# Running the Local Model — Choose Your Runtime

FrugalRoute's local (free) model is called over an **OpenAI-compatible API**. That means
**you can use almost any local LLM runtime** — you only set two things in `.env`:

```ini
LOCAL_BASE_URL=<the runtime's OpenAI endpoint>
LOCAL_MODEL=<the model name it serves>
```

Pick a runtime based on your hardware:

| Your setup | Use | Why |
|---|---|---|
| **Just want it to work (any OS, CPU or GPU)** | **Ollama** ⭐ | one command, cross-platform, easiest |
| Prefer a GUI (no terminal) | **LM Studio** | click-to-run, built-in OpenAI server |
| **AMD GPU (MI300X / Radeon, ROCm)** | **vLLM** or **SGLang** | high throughput + prefix caching (what this project used) |
| NVIDIA GPU (CUDA) | **vLLM** | high throughput |
| Low-end / no GPU | **Ollama** or **llama.cpp** with a small quantized model | runs on modest hardware |
| Just exploring the logic, no model | `MOCK=1` | zero setup — canned answers, real routing |

---

## Option A — Ollama (recommended default)
Works on Windows, macOS, Linux; CPU or GPU.
```bash
# 1. install from https://ollama.com/download
ollama pull gemma2:2b            # small + fast; or qwen2.5:3b / gemma2:9b for more accuracy
# Ollama auto-serves an OpenAI endpoint:
```
`.env`:
```ini
MOCK=0
LOCAL_BASE_URL=http://localhost:11434/v1
LOCAL_MODEL=gemma2:2b
LOCAL_API_KEY=ollama          # any non-empty string
```

## Option B — LM Studio (GUI)
Download the model in the app → **Developer → Start Server** (OpenAI-compatible).
```ini
LOCAL_BASE_URL=http://localhost:1234/v1
LOCAL_MODEL=<model id shown in LM Studio>
LOCAL_API_KEY=lm-studio
```

## Option C — vLLM (GPU / AMD ROCm — the project's setup)
Best throughput; supports prefix caching (RadixAttention/APC). On AMD use the ROCm build.
```bash
# AMD MI300X (ROCm):
VLLM_HOST_IP=127.0.0.1 vllm serve Qwen/Qwen2.5-7B-Instruct \
  --host 0.0.0.0 --port 8000 --enable-prefix-caching --max-model-len 8192
```
```ini
LOCAL_BASE_URL=http://localhost:8000/v1
LOCAL_MODEL=Qwen/Qwen2.5-7B-Instruct
LOCAL_API_KEY=vllm
```
(SGLang is equivalent: `python -m sglang.launch_server --model-path <hf-id> --port 30000`.)

## Option D — llama.cpp / llamafile (CPU-friendly)
Run a GGUF with the built-in server:
```bash
./llama-server -m gemma-2-2b-it-Q4_K_M.gguf --port 8080 --host 0.0.0.0
```
```ini
LOCAL_BASE_URL=http://localhost:8080/v1
LOCAL_MODEL=gemma-2-2b-it
```

## Option E — No model at all
```ini
MOCK=1
```
Runs the full routing/calibration/cache logic with canned model text — perfect for a quick look with zero setup.

---

## Recommended local models (all open-weight, OpenAI-servable)
| Model | Size | Good for | Runtime |
|---|---|---|---|
| `gemma2:2b` / Gemma-2-2B | 2.6B | fast, fits low VRAM / CPU | Ollama, llama.cpp |
| `qwen2.5:3b` / Qwen2.5-3B | 3B | strong all-rounder | Ollama, vLLM |
| `gemma2:9b` / Gemma-2-9B | 9B | higher accuracy, mid GPU | Ollama, vLLM |
| `qwen2.5:7b` / Qwen2.5-7B | 7B | balanced | Ollama, vLLM |

See `MODEL_BENCHMARK_PLAN.md` for the full accuracy-vs-cost comparison on AMD MI300X.

---

## TL;DR for repo users
1. Install **Ollama** → `ollama pull gemma2:2b`.
2. In `.env`: `MOCK=0`, `LOCAL_BASE_URL=http://localhost:11434/v1`, `LOCAL_MODEL=gemma2:2b`.
3. Add your remote key (`REMOTE_PROVIDER=fireworks` + `REMOTE_API_KEY`).
4. `python run.py` — or `uvicorn server:app` and open the playground.

No GPU? Use `gemma2:2b` on Ollama (CPU) or just `MOCK=1`. Any OpenAI-compatible server works — you're never locked to one platform.
