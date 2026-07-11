# Local serving + prefix caching

Serve the local (free) model with a **prefix KV cache** so the shared prompt prefix
(system instructions + few-shot) is processed once and reused across every local
call. Result: lower time-to-first-token, higher throughput → the local model clears
more tasks inside any per-task time budget → fewer paid escalations.

## Engines (pick one), all OpenAI-compatible

| Engine | Prefix cache | Endpoint | Start |
|--------|--------------|----------|-------|
| SGLang | **RadixAttention** (default on) | `:30000/v1` | `bash serve/start_sglang.sh` |
| vLLM   | **Automatic Prefix Caching** (`--enable-prefix-caching`) | `:8000/v1` | `bash serve/start_vllm.sh` |
| Ollama | session KV reuse (weaker) | `:11434/v1` | `bash serve/start_ollama.sh` |

On AMD: use the ROCm builds (torch-ROCm; `rocm/vllm` image — see `Dockerfile.vllm.rocm`).
Then set `LOCAL_BASE_URL` in `.env` to the chosen endpoint and `MOCK=0`.

## The client side matters (this repo)

Prefix caching only hits if every local call shares a **byte-identical prefix**.
`prompts.py` guarantees this: a constant `SYSTEM_PREFIX` + fixed `FEWSHOT` first,
the variable task last. `nodes.local` builds local messages via
`prompts.build_local_messages`. Never f-string per-request content into the prefix
— a single changed whitespace breaks the cache key.

Confirm hits: SGLang logs a **cache hit rate**; vLLM exposes prefix-cache stats.

## Not for the remote path

RadixAttention on the REMOTE model needs control of that server — you don't control
Fireworks. So prefix caching is a LOCAL optimization only. The remote path uses
LLMLingua-2 compression instead (`compress.py`).
