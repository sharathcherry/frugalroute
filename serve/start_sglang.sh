#!/usr/bin/env bash
# SGLang server on AMD ROCm. RadixAttention (prefix KV cache) is ON by default.
# OpenAI-compatible endpoint at :30000/v1
#   -> set LOCAL_BASE_URL=http://localhost:30000/v1  in .env
#
# Install (ROCm): pip install "sglang[all]"   (use the AMD/ROCm build of torch)
set -e
MODEL="${LOCAL_MODEL:-Qwen/Qwen2.5-3B-Instruct}"
python -m sglang.launch_server \
  --model-path "$MODEL" \
  --host 0.0.0.0 --port 30000 \
  --mem-fraction-static 0.85
# RadixAttention is enabled by default. Do NOT pass --disable-radix-cache.
# Watch the server log for "cache hit rate" to confirm prefix reuse.
