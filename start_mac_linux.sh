#!/bin/bash
echo "=================================================="
echo "        Starting FrugalRoute Ecosystem"
echo "=================================================="

echo ""
echo "[1/3] Checking Python dependencies..."
pip install -r requirements.txt -q

echo ""
echo "[2/3] Booting Local Model Engine (Ollama)..."
echo "(If you don't have Ollama installed, get it at ollama.com)"
ollama run qwen2.5:3b-instruct &
OLLAMA_PID=$!

echo ""
echo "[3/3] Starting FrugalRoute Interface Server..."
python -m uvicorn server:app --port 8000 &
UVICORN_PID=$!

echo ""
echo "Waiting for services to initialize..."
sleep 4

echo ""
echo "Launching your web browser..."
if which xdg-open > /dev/null
then
  xdg-open http://localhost:8000
elif which open > /dev/null
then
  open http://localhost:8000
else
  echo "Please manually open http://localhost:8000 in your browser"
fi

echo ""
echo "=================================================="
echo "FrugalRoute is online!"
echo "Press Ctrl+C to shut down all services."
echo "=================================================="
wait $UVICORN_PID
