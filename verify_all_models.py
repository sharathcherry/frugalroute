import json, re, time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

env = open("/root/frugalroute/.env").read()
KEY = re.search(r"REMOTE_API_KEY=(\S+)", env).group(1)

all_models = json.load(open("/tmp/all_fw_models.json"))
print(f"Total catalog entries: {len(all_models)}")

def try_call(entry):
    model_id = entry["name"]
    kind = entry.get("kind")
    # Embedding/rerank models use a different endpoint (not chat/completions) —
    # test those separately via /v1/embeddings instead of miscounting them as broken.
    if kind == "EMBEDDING_MODEL":
        url = "https://api.fireworks.ai/inference/v1/embeddings"
        body = json.dumps({"model": model_id, "input": "test"}).encode()
    elif kind in ("FLUMINA_BASE_MODEL", "FLUMINA_ADDON"):
        return model_id, kind, "skipped-image-gen", None
    elif kind in ("DRAFT_ADDON", "HF_TEFT_ADDON", "HF_PEFT_ADDON"):
        return model_id, kind, "skipped-addon", None
    else:
        url = "https://api.fireworks.ai/inference/v1/chat/completions"
        body = json.dumps({
            "model": model_id,
            "messages": [{"role": "user", "content": "hi"}],
            "max_tokens": 3,
        }).encode()

    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
    })
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                r.read()
            return model_id, kind, "OK", None
        except urllib.error.HTTPError as e:
            err_body = e.read().decode(errors="replace")[:200]
            if e.code == 429 and attempt == 0:
                time.sleep(3)
                continue
            return model_id, kind, f"HTTP_{e.code}", err_body
        except Exception as e:
            if attempt == 0:
                time.sleep(2)
                continue
            return model_id, kind, "ERROR", str(e)[:200]

results = []
with ThreadPoolExecutor(max_workers=8) as ex:
    futs = {ex.submit(try_call, m): m for m in all_models}
    done = 0
    for fut in as_completed(futs):
        res = fut.result()
        results.append(res)
        done += 1
        if done % 25 == 0:
            print(f"...{done}/{len(all_models)}")

json.dump(results, open("/tmp/verify_results.json", "w"))

ok = [r for r in results if r[2] == "OK"]
not_found = [r for r in results if r[2].startswith("HTTP_404") or "NOT_FOUND" in (r[3] or "")]
skipped = [r for r in results if r[2].startswith("skipped")]
other_err = [r for r in results if r not in ok and r not in not_found and r not in skipped]

print(f"\n=== RESULTS ===")
print(f"Total: {len(results)}")
print(f"OK (real, callable right now): {len(ok)}")
print(f"NOT_FOUND (needs deployment): {len(not_found)}")
print(f"Skipped (image-gen / addon, different API): {len(skipped)}")
print(f"Other errors: {len(other_err)}")
print("\n--- OK models ---")
for m, k, status, _ in sorted(ok):
    print(f"  {m}  [{k}]")
if other_err:
    print("\n--- Other errors (investigate) ---")
    for m, k, status, detail in other_err[:20]:
        print(f"  {m}  [{k}] -> {status}: {detail}")
