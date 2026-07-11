#!/usr/bin/env bash
# docker-entrypoint.sh — FrugalRoute container entrypoint
#
# 1. Starts vLLM serving the baked-in local model on port 8001.
# 2. Polls until the endpoint is ready (up to 5 minutes).
# 3. Passes all CLI args to run.py (submission batch mode).
#
# Environment variables (injected at `docker run`):
#   REMOTE_BASE_URL  — Fireworks endpoint (required for remote calls)
#   REMOTE_API_KEY   — Fireworks API key
#   REMOTE_MODEL     — Fireworks model name
#   HF_MODEL         — local model (default: Qwen/Qwen2.5-7B-Instruct)
#   VLLM_PORT        — vLLM port (default: 8001)
#   MOCK             — set 1 to skip real models (CI/logic testing)

set -euo pipefail

VLLM_PORT="${VLLM_PORT:-8001}"
MODEL="${HF_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
VLLM_API_KEY="${LOCAL_API_KEY:-frugalroute-local}"

# -----------------------------------------------------------------------
# Start vLLM (skip in MOCK mode — no GPU needed)
# -----------------------------------------------------------------------
if [ "${MOCK:-0}" != "1" ]; then
    echo "[entrypoint] Starting vLLM for model: ${MODEL} on port ${VLLM_PORT}"

    python -m vllm.entrypoints.openai.api_server \
        --model "${MODEL}" \
        --model-dir /model-cache \
        --port "${VLLM_PORT}" \
        --api-key "${VLLM_API_KEY}" \
        --enable-prefix-caching \
        --max-model-len 8192 \
        --enforce-eager \
        --gpu-memory-utilization 0.85 \
        &
    VLLM_PID=$!

    # Wait for vLLM to become ready (max 5 min)
    echo "[entrypoint] Waiting for vLLM to be ready..."
    READY=0
    for i in $(seq 1 60); do
        if curl -sf "http://127.0.0.1:${VLLM_PORT}/health" > /dev/null 2>&1; then
            echo "[entrypoint] vLLM ready (attempt ${i})"
            READY=1
            break
        fi
        sleep 5
    done

    if [ "$READY" -ne 1 ]; then
        echo "[entrypoint] ERROR: vLLM did not become ready within 5 minutes."
        kill "$VLLM_PID" 2>/dev/null || true
        exit 1
    fi
fi

# -----------------------------------------------------------------------
# Run the FrugalRoute pipeline
# -----------------------------------------------------------------------
echo "[entrypoint] Running FrugalRoute: $*"
exec python /app/run.py "$@"
