#!/usr/bin/env bash
set -uo pipefail
cd /root/frugalroute
mkdir -p out eval/gpu_logs eval/logs eval/calibs

TAGS=("gemma4:e2b" "gemma4:e4b" "gemma4:12b" "gemma4:26b" "gemma4:31b")

for TAG in "${TAGS[@]}"; do
  SAFE=$(echo "$TAG" | tr ':' '_')
  echo "=================== $TAG ==================="

  # make sure this model is warm / preloaded on GPU before timing
  ollama run "$TAG" "hi" --verbose >/dev/null 2>&1 || true

  # start GPU monitor loop
  ( while true; do
      echo "$(date +%s.%N),$(rocm-smi -u --showmemuse --csv 2>/dev/null | tail -1)" >> "eval/gpu_logs/${SAFE}.csv"
      sleep 1
    done ) &
  MONPID=$!

  echo "--- ollama ps before harness ---"
  ollama ps

  export LOCAL_MODEL="$TAG"
  echo "--- harness.py (calib fit) ---"
  .venv/bin/python eval/harness.py > "eval/logs/harness_${SAFE}.log" 2>&1
  tail -15 "eval/logs/harness_${SAFE}.log"
  cp calib.json "eval/calibs/calib_${SAFE}.json" 2>/dev/null || echo 'no calib.json produced'

  echo "--- run.py (real sweep over eval/tasks.jsonl) ---"
  START=$(date +%s.%N)
  LOCAL_MODEL="$TAG" .venv/bin/python run.py --input eval/tasks.jsonl --output "out/${SAFE}.jsonl" > "eval/logs/run_${SAFE}.log" 2>&1
  END=$(date +%s.%N)
  ELAPSED=$(python3 -c "print($END - $START)")
  N=$(wc -l < eval/tasks.jsonl)
  python3 -c "print('avg_latency_s', $ELAPSED / $N)"
  echo "$ELAPSED" > "eval/logs/${SAFE}.elapsed"
  tail -20 "eval/logs/run_${SAFE}.log"

  kill $MONPID 2>/dev/null
  wait $MONPID 2>/dev/null

  echo "--- ollama ps after run ---"
  ollama ps

  echo "--- score ---"
  .venv/bin/python eval/score.py "$SAFE"

done
echo ALL DONE
