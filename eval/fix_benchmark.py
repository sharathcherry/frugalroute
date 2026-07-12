import json
import re

LOG_FILES = [
    r"C:\Users\katuk\Claude\Projects\AMD Project\frugalroute\eval\full_bench.log"
]

MODEL_METADATA = {
    "Qwen2.5-0.5B-Instruct": {"params": "0.5B", "vram_gb": 1.2},
    "Qwen2.5-1.5B-Instruct": {"params": "1.5B", "vram_gb": 2.0},
    "Llama-3.2-1B-Instruct": {"params": "1.2B", "vram_gb": 2.4},
    "gemma-2-2b-it": {"params": "2.6B", "vram_gb": 5.2},
    "Qwen2.5-3B-Instruct": {"params": "3.1B", "vram_gb": 6.0},
    "Llama-3.2-3B-Instruct": {"params": "3.2B", "vram_gb": 6.2},
    "Phi-3.5-mini-instruct": {"params": "3.8B", "vram_gb": 7.6},
    "Mistral-7B-Instruct-v0.3": {"params": "7B", "vram_gb": 14.0},
    "Qwen2.5-7B-Instruct": {"params": "7.6B", "vram_gb": 15.2},
    "DeepSeek-R1-Distill-Qwen-7B": {"params": "7.0B", "vram_gb": 14.0},
    "gemma-2-9b-it": {"params": "9.2B", "vram_gb": 18.4, "pick": "⭐"},
    "Qwen2.5-32B-Instruct": {"params": "32.5B", "vram_gb": 65.0, "pick": "✗ (3x latency)"}
}

results = []

for log_path in LOG_FILES:
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split by model execution
    sections = content.split("Benchmarking ")
    for section in sections[1:]:
        model_full = section.split("\n")[0].strip()
        model_name = model_full.split("/")[-1]
        
        if not model_name:
            continue
            
        acc_m = re.search(r"accuracy = ([\d\.]+)", section)
        acc = float(acc_m.group(1)) if acc_m else 0.0
        
        free_m = re.search(r"free%=([\d\.]+)", section)
        local_hit = float(free_m.group(1)) if free_m else 0.0
        
        rem_m = re.search(r"remote_tokens=(\d+)", section)
        rem_tokens = float(rem_m.group(1)) if rem_m else 0.0
        
        meta = MODEL_METADATA.get(model_name, {"params": "?", "vram_gb": "?"})
        
        results.append({
            "model": model_name,
            "params": meta["params"],
            "vram_gb": meta["vram_gb"],
            "local_hit_rate": local_hit,
            "remote_tokens": rem_tokens,
            "accuracy": acc,
            "latency_s": 0.0, # Not captured by run.py
            "pick": meta.get("pick", "")
        })

out_path = "eval/benchmark.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print(f"Fixed benchmark.json with {len(results)} models.")
