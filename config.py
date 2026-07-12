"""Central config. Reads from environment / .env. Defaults to MOCK so the repo
runs end-to-end with zero external dependencies or models."""
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


def _b(v):
    return str(v).lower() in ("1", "true", "yes", "on")


MOCK = _b(os.getenv("MOCK", "0"))  # default OFF for production (real inference)

# --- Remote (PAID) provider — Fireworks by default; any OpenAI-compatible API ---
REMOTE_BASE_URL = os.getenv("REMOTE_BASE_URL", "https://api.fireworks.ai/inference/v1")
REMOTE_API_KEY = os.getenv("REMOTE_API_KEY", "")
REMOTE_MODEL = os.getenv("REMOTE_MODEL", "accounts/fireworks/models/llama-v3p1-8b-instruct")

# Remote provider switch: fireworks (scored) | azure | openai
REMOTE_PROVIDER = os.getenv("REMOTE_PROVIDER", "fireworks")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")        # https://<res>.openai.azure.com
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")    # your deployment name = model

# --- Local (FREE) provider — vLLM/ROCm or Ollama; OpenAI-compatible endpoint ---
LOCAL_BASE_URL = os.getenv("LOCAL_BASE_URL", "http://localhost:11434/v1")
LOCAL_API_KEY = os.getenv("LOCAL_API_KEY", "ollama")

# LOCAL_MODEL=auto -> pick the best model that fits THIS machine's GPU (hwselect).
# Any explicit tag (e.g. qwen2.5:7b-instruct) overrides the auto-selection.
_LM = os.getenv("LOCAL_MODEL", "auto").strip()
if _LM.lower() in ("", "auto") and not MOCK:
    try:
        import hwselect
        LOCAL_MODEL = hwselect.choose()
    except Exception:
        LOCAL_MODEL = "qwen2.5:3b-instruct"
else:
    LOCAL_MODEL = _LM or "qwen2.5:3b-instruct"

# --- Thresholds (tune on your eval set via eval/harness.py) ---
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
# Fast gate: accept a short, non-hedging local answer without a 2nd selfrate call
FAST_GATE = _b(os.getenv("FAST_GATE", "1"))
FAST_GATE_MAXLEN = int(os.getenv("FAST_GATE_MAXLEN", "160"))
JUDGE_MODE = os.getenv("JUDGE_MODE", "selfrate")   # selfrate (real local self-grade) | heuristic
CACHE_SIM_THRESHOLD = float(os.getenv("CACHE_SIM_THRESHOLD", "0.92"))
# Semantic cache on/off. Off avoids stale answers on time-sensitive queries.
CACHE_ENABLED = _b(os.getenv("CACHE_ENABLED", "1"))
ROUTE_THRESHOLD = float(os.getenv("ROUTE_THRESHOLD", "0.75"))
COMPRESS = _b(os.getenv("COMPRESS", "1"))
CALIB_PATH = os.getenv("CALIB_PATH", "")

# --- Gate mode + AutoMix POMDP costs ---
GATE_MODE = os.getenv("GATE_MODE", "calibrated")          # calibrated | automix
AUTOMIX_PATH = os.getenv("AUTOMIX_PATH", "")              # fitted obs model (automix.json)
AUTOMIX_RC = float(os.getenv("AUTOMIX_RC", "1.0"))       # reward for a correct answer
AUTOMIX_PENALTY = float(os.getenv("AUTOMIX_PENALTY", "-2.0"))  # cost of accepting a wrong local answer
AUTOMIX_COST = float(os.getenv("AUTOMIX_COST", "0.3"))   # token cost of escalating to remote
AUTOMIX_SAMPLES = int(os.getenv("AUTOMIX_SAMPLES", "1")) # self-verify observations per query

# --- LLMLingua-2 prompt compression ---
COMPRESS_RATE = float(os.getenv("COMPRESS_RATE", "0.5"))   # keep ~50% of tokens
LLMLINGUA_MODEL = os.getenv("LLMLINGUA_MODEL", "microsoft/llmlingua-2-xlm-roberta-large-meetingbank")
LLMLINGUA_DEVICE = os.getenv("LLMLINGUA_DEVICE", "cpu")

# --- Semantic cache / embeddings (Qdrant) ---
CACHE_BACKEND = os.getenv("CACHE_BACKEND", "auto")          # auto | qdrant | difflib
EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
EMBED_DIM = int(os.getenv("EMBED_DIM", "384"))              # bge-small-en-v1.5 = 384
QDRANT_URL = os.getenv("QDRANT_URL", "")                    # e.g. http://localhost:6333
QDRANT_PATH = os.getenv("QDRANT_PATH", "")                  # persistent local dir
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "frugalroute_cache")
