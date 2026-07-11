#!/usr/bin/env bash
# ============================================================
# FrugalRoute — Block B: Run this on the MI300X
# SSH: ssh root@129.212.178.3
# Estimated time: ~15-25 min (depends on 36 eval tasks × 2 local calls each)
# ============================================================
set -euo pipefail

REPO="/path/to/frugalroute"   # ← set this to your repo path on the MI300X
cd "$REPO"

echo "=== [1/4] Verifying vLLM is up ==="
curl -sf http://127.0.0.1:8001/health && echo "vLLM: OK" || {
    echo "vLLM not running — starting it..."
    VLLM_HOST_IP=127.0.0.1 python -m vllm.entrypoints.openai.api_server \
        --model Qwen/Qwen2.5-7B-Instruct \
        --port 8001 \
        --api-key "$LOCAL_API_KEY" \
        --enable-prefix-caching \
        --max-model-len 8192 &
    echo "Waiting 90s for vLLM to start..."
    sleep 90
    curl -sf http://127.0.0.1:8001/health && echo "vLLM: OK"
}

echo ""
echo "=== [2/4] Running calibration harness (MOCK=0) ==="
# This runs all 36 eval tasks against the real local model,
# fits Platt + Isotonic calibrators, and recommends CONFIDENCE_THRESHOLD.
MOCK=0 python eval/harness.py 2>&1 | tee block_b_harness.log

echo ""
echo "=== [3/4] Checking outputs ==="
ls -lh calib.json automix.json || echo "WARNING: calibration files missing"

echo ""
echo "=== [4/4] Re-running full pipeline with new calibration ==="
MOCK=0 CALIB_PATH=calib.json python run.py --input eval/tasks.jsonl --output out/results_calibrated.jsonl
echo ""
echo "--- Block B DONE. Paste block_b_harness.log output to Claude ---"
echo "--- Update .env: CALIB_PATH=calib.json + CONFIDENCE_THRESHOLD=<recommended> ---"
