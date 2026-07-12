import os
import time
import json
import subprocess
import re
import concurrent.futures

# Configure Ollama for maximum concurrency since we have 192GB VRAM on MI300X
os.environ["OLLAMA_NUM_PARALLEL"] = "8"
os.environ["OLLAMA_MAX_VRAM"] = "192000000000"

# List the Gemma models to run simultaneously. 
# Update these tags if your local Ollama registry uses different names for Gemma 4!
MODELS_TO_TEST = [
    "gemma2:9b",      # Fallback to Gemma 2 if 4 isn't available
    "gemma2:27b",
    "gemma4:9b",      # Assuming these tags exist in your local setup
    "gemma4:27b"
]

def benchmark_model(model):
    print(f"[{model}] Starting benchmark pipeline...")
    
    # 1. Pull the model
    print(f"[{model}] Pulling from registry...")
    pull_res = subprocess.run(["ollama", "pull", model], capture_output=True, text=True)
    if pull_res.returncode != 0:
        print(f"[{model}] Failed to pull model (might not exist in registry). Skipping.")
        return None

    # Setup specific environment for this thread's subprocesses
    env = os.environ.copy()
    env["LOCAL_MODEL"] = model
    env["MOCK"] = "0"
    env["LOCAL_BASE_URL"] = "http://localhost:11434/v1"
    env["LOCAL_API_KEY"] = "ollama"

    # 2. Run Harness
    print(f"[{model}] Running eval/harness.py...")
    harness_res = subprocess.run(["python", "eval/harness.py"], env=env, capture_output=True, text=True)
    
    acc = 0.0
    m = re.search(r"accuracy = ([\d\.]+)", harness_res.stdout)
    if m:
        acc = float(m.group(1))
        
    # 3. Run FrugalRoute Pipeline
    print(f"[{model}] Running FrugalRoute evaluation...")
    out_file = f"out/{model.replace(':', '_')}_parallel.jsonl"
    os.makedirs("out", exist_ok=True)
    
    run_res = subprocess.run(["python", "run.py", "--input", "eval/tasks.jsonl", "--output", out_file], env=env, capture_output=True, text=True)
    
    # Extract stats
    try:
        def extract_stat(name):
            match = re.search(fr'{name}=([\d\.]+)', run_res.stdout)
            return float(match.group(1)) if match else 0.0
        
        local_hit = extract_stat(r"free%")
        rem_tokens = extract_stat(r"remote_tokens")
        
        result = {
            "model": model,
            "local_hit_rate": local_hit,
            "remote_tokens": rem_tokens,
            "accuracy": acc,
        }
        print(f"[{model}] FINISHED: {result}")
        return result
    except Exception as e:
        print(f"[{model}] Failed to parse run.py output: {e}")
        return None

def main():
    print(f"Starting parallel benchmark for {len(MODELS_TO_TEST)} models using 192GB VRAM...")
    
    results = []
    # Run all models simultaneously using a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(MODELS_TO_TEST)) as executor:
        future_to_model = {executor.submit(benchmark_model, model): model for model in MODELS_TO_TEST}
        
        for future in concurrent.futures.as_completed(future_to_model):
            model = future_to_model[future]
            try:
                res = future.result()
                if res:
                    results.append(res)
            except Exception as exc:
                print(f"[{model}] generated an exception: {exc}")

    # Save aggregated parallel results
    out_path = "eval/benchmark_parallel_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nAll parallel benchmarks complete! Saved results to {out_path}")

if __name__ == "__main__":
    main()
