#!/usr/bin/env bash
set -uo pipefail
cd /root/frugalroute
mkdir -p out eval/gpu_logs eval/logs eval/calibs

TAGS=("qwen3:4b" "qwen3:8b" "qwen3:14b" "qwen3:30b-a3b" "qwen3:32b")

for TAG in "${TAGS[@]}"; do
  SAFE=$(echo "$TAG" | tr ':' '_')
  echo "=================== $TAG ==================="

  ollama run "$TAG" "hi" --verbose >/dev/null 2>&1 || true

  ( while true; do
      LINE=$(rocm-smi -u --showmemuse --csv 2>/dev/null | grep card0)
      echo "$(date +%s.%N),$LINE" >> "eval/gpu_logs/${SAFE}.csv"
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
echo ALL DONE QWEN3
