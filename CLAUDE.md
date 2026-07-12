# FrugalRoute — Claude Instructions

## Response style (mandatory)

Invoke the `/caveman:caveman` skill (Skill tool: `caveman:caveman`) at the start of every session in this project, and respond in caveman style (level: full) for all responses: drop articles, filler, pleasantries, and hedging; fragments OK; keep all technical substance exact. Code, commits, PRs, and security warnings are written normally.

## Project

**Repo:** https://github.com/sharathcherry/frugalroute

Local-first LLM routing agent (AMD Hackathon Track 1). Routes each task to a free local model (Ollama `qwen2.5:3b-instruct`) or escalates to a paid remote model, minimizing paid tokens while holding accuracy ≥ 0.95.

- Pipeline: `ingest → triage → cache → route → local → gate → remote → account` (`nodes.py`; LangGraph in `graph.py`, stdlib fallback `engine.py`)
- Entry: `python run.py` — writes `dashboard/data.js`
- Tuning: `python eval/harness.py` — fits calibrator (`calib.json`), recommends `CONFIDENCE_THRESHOLD`
- Config: `.env` (note: duplicate keys — last occurrence wins with python-dotenv)
- `MOCK=1` = canned inference, zero setup; `MOCK=0` = real endpoints
- Remote: Fireworks = scored hackathon path; Azure (`vani-aoai-ff646.openai.azure.com`, deployment `gpt-4o`) = dev/portfolio only

## Environment constraints

- GPU: 4GB RTX 3050 Ti laptop — 3B model often fails to load (WDDM reservations); fallback `qwen2.5:0.5b-instruct` works
- Never print API keys from `.env`
