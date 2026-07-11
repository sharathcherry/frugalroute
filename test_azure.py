"""Azure OpenAI connectivity dry-test. Run on YOUR machine (needs your .env + openai).

    pip install openai python-dotenv
    python test_azure.py

Confirms endpoint/key/deployment work and prints token usage. Never prints the key.
Run this BEFORE the full pipeline so you know Azure is reachable.
"""
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

ep = os.getenv("AZURE_OPENAI_ENDPOINT", "")
key = os.getenv("AZURE_OPENAI_API_KEY", "")
dep = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
ver = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")

print("endpoint set :", bool(ep))
print("api key set  :", bool(key), f"(len {len(key)})")
print("deployment   :", dep or "(missing)")

missing = [n for n, v in [("AZURE_OPENAI_ENDPOINT", ep),
                          ("AZURE_OPENAI_API_KEY", key),
                          ("AZURE_OPENAI_DEPLOYMENT", dep)] if not v]
if missing:
    raise SystemExit("MISSING in .env: " + ", ".join(missing))

from openai import AzureOpenAI
client = AzureOpenAI(azure_endpoint=ep, api_key=key, api_version=ver)
try:
    r = client.chat.completions.create(
        model=dep,
        messages=[{"role": "user", "content": "Reply with the single word: ok"}],
        temperature=0, max_tokens=5)
    print("\nAZURE OK ->", r.choices[0].message.content.strip())
    print("tokens: prompt=%s completion=%s" % (r.usage.prompt_tokens, r.usage.completion_tokens))
except Exception as e:
    print("\nAZURE CALL FAILED:", type(e).__name__)
    print(str(e)[:300])
    print("\nCheck: deployment name (not model name), endpoint URL, api_version, and that "
          "the deployment exists in that resource/region.")
