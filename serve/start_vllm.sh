#!/usr/bin/env bash
# vLLM server on AMD ROCm. --enable-prefix-caching is vLLM's RadixAttention equivalent
# (Automatic Prefix Caching). OpenAI-compatible endpoint at :8000/v1
#   -> set LOCAL_BASE_URL=http://localhost:8000/v1  in .env
set -e
MODEL="${LOCAL_MODEL:-Qwen/Qwen2.5-3B-Instruct}"
vllm serve "$MODEL" \
  --host 0.0.0.0 --port 8000 \
  --enable-prefix-caching \
  --gpu-memory-utilization 0.9
