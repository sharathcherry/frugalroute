"""Quick smoke test — one real local call, then check rocm-smi."""
import sys, os
sys.path.insert(0, '/frugalroute')
import providers, config

print("Making ONE real local call to vLLM on MI300X...")
print("Model:", config.LOCAL_MODEL)
print("URL:", config.LOCAL_BASE_URL)

msgs = [{"role": "user", "content": "What is 2+2? Answer with just the number."}]
try:
    text, prompt_tok, compl_tok = providers.complete(msgs, kind="local", max_tokens=10)
    print("RESPONSE:", repr(text))
    print("Tokens — prompt:", prompt_tok, "completion:", compl_tok)
    print("GPU IS WORKING" if text.strip() else "EMPTY RESPONSE")
except Exception as e:
    print("ERROR:", e)
