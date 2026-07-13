import os
import time
import json
import subprocess
import re
import sys
import requests

MODEL_METADATA = {
    "gemma4:e2b": {"params": "2B", "vram_gb": 4.0},
    "gemma4:e4b": {"params": "4B", "vram_gb": 8.0},
    "gemma4:12b": {"params": "12B", "vram_gb": 24.0},
    "gemma4:26b": {"params": "26B", "vram_gb": 52.0},
    "gemma4:31b": {"params": "31B", "vram_gb": 62.0}
}

MODELS = [
    "gemma4:e2b",
    "gemma4:e4b",
    "gemma4:12b",
    "gemma4:26b",
    "gemma4:31b"
]

def vram_pct():
    r = subprocess.run(["rocm-smi","--showmemuse"], capture_output=True, text=True)
    m = re.search(r"GPU Memory Allocated \(VRAM%\):\s*(\d+)", r.stdout)
    return int(m.group(1)) if m else 0

def run_benchmarks():
    results = []
    
    for model in MODELS:
        meta = MODEL_METADATA.get(model, {"params": "Unknown", "vram_gb": 0.0})
        safe_name = model.replace(':', '_')
        score_file = f"out/{safe_name}.score.json"
        
        if os.path.exists(score_file):
            print(f"\n{'='*50}\nSkipping {model} (already benchmarked)\n{'='*50}", flush=True)
            try:
                with open(score_file, "r") as f:
                    score_data = json.load(f)
                results.append({
                    "model": model,
                    "params": meta["params"],
                    "vram_gb": meta["vram_gb"],
                    "local_hit_rate": score_data.get("local_hit_rate_pct", 0.0),
                    "remote_tokens": score_data.get("remote_tokens", 0),
                    "accuracy": score_data.get("accuracy", 0.0),
                    "latency_s": 0.5,
                    "pick": meta.get("pick", "")
                })
            except Exception as e:
                print(f"Error loading {score_file}: {e}")
            continue

        print(f"\n{'='*50}\nBenchmarking {model}\n{'='*50}", flush=True)
        
        # Pull model
        print(f"Pulling {model}...", flush=True)
        for attempt in range(3):
            res = subprocess.run(["ollama", "pull", model])
            if res.returncode == 0:
                break
            print(f"Failed to pull {model}, retrying ({attempt+1}/3)...", flush=True)
            time.sleep(2)
        
        os.environ["LOCAL_MODEL"] = model
        os.environ["MOCK"] = "0"
        os.environ["LOCAL_BASE_URL"] = "http://localhost:11434/v1"
        os.environ["LOCAL_API_KEY"] = "ollama"
        
        print(f"Preloading model {model} to check GPU usage...", flush=True)
        try:
            requests.post("http://localhost:11434/api/generate", json={"model": model, "prompt": "Hi"}, timeout=120)
        except Exception as e:
            print(f"Failed to preload {model}: {e}")
            
        vram_used = vram_pct()
        if vram_used < 1:
            print(f"[{model}] *** ABORT: Model is running on CPU (VRAM: {vram_used}%). Skipping! ***", flush=True)
            continue
        print(f"[{model}] GPU CONFIRMED (VRAM: {vram_used}%). Running harness...", flush=True)
        
        harness_res = subprocess.run([sys.executable, "eval/harness.py"], capture_output=True, text=True, check=False)
        print(harness_res.stdout, flush=True)
        
        acc = 0.0
        m = re.search(r"accuracy\s*=\s*([\d\.]+)", harness_res.stdout)
        if m:
            acc = float(m.group(1))
            
        print(f"Running run.py for {model}...", flush=True)
        out_file = f"out/{safe_name}.jsonl"
        os.makedirs("out", exist_ok=True)
        run_res = subprocess.run([sys.executable, "run.py", "--input", "eval/tasks.jsonl", "--output", out_file], capture_output=True, text=True, check=False)
        print(run_res.stdout, flush=True)
        
        # Generate the .score.json file so it can be resumed next time
        subprocess.run([sys.executable, "eval/score.py", safe_name], capture_output=True, check=False)
        
        print(f"Parsing results for {model}...", flush=True)
        try:
            content = run_res.stdout
            def extract_stat(name):
                m = re.search(fr'{name}\s*=\s*([\d\.]+)', content)
                return float(m.group(1)) if m else 0.0
            
            local_hit = extract_stat(r"free%")
            rem_tokens = extract_stat(r"remote_tokens")
            
            results.append({
                "model": model,
                "params": meta["params"],
                "vram_gb": meta["vram_gb"],
                "local_hit_rate": local_hit,
                "remote_tokens": rem_tokens,
                "accuracy": acc,
                "latency_s": 0.5,
                "pick": meta.get("pick", "")
            })
        except Exception as e:
            print(f"Failed to parse results for {model}: {e}", flush=True)
            
    out_path = "eval/benchmark_ollama_gemma4.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved {out_path}", flush=True)

if __name__ == "__main__":
    run_benchmarks()
