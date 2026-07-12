@echo off
title FrugalRoute
echo ==================================================
echo         Starting FrugalRoute Ecosystem
echo ==================================================

echo.
echo [1/3] Checking Python dependencies...
pip install -r requirements.txt -q

echo.
echo [2/3] Booting Local Model Engine (Ollama)...
echo (This will open a minimized window running qwen2.5:3b-instruct)
start "FrugalRoute - Ollama Local Engine" /MIN ollama run qwen2.5:3b-instruct

echo.
echo [3/3] Starting FrugalRoute Interface Server...
start "FrugalRoute - UI Server" cmd /c "python -m uvicorn server:app --port 8000"

echo.
echo Waiting for services to initialize...
timeout /t 4 /nobreak >nul

echo.
echo Launching your web browser...
start http://localhost:8000

echo.
echo ==================================================
echo FrugalRoute is online! 
echo Close this window to exit.
echo ==================================================
pause
