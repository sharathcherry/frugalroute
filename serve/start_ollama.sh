#!/usr/bin/env bash
# Simplest local option (dev / smaller models). OpenAI-compatible endpoint at :11434/v1
#   -> set LOCAL_BASE_URL=http://localhost:11434/v1  in .env
# Note: Ollama reuses KV for a repeated prefix within a session but is less explicit
# than SGLang/vLLM prefix caching. Prefer SGLang/vLLM for the scored run.
set -e
ollama serve &
sleep 2
ollama pull "${OLLAMA_MODEL:-qwen2.5:3b-instruct}"
echo "Local model ready. Set LOCAL_BASE_URL=http://localhost:11434/v1"
