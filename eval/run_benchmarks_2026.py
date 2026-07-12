import os
import json
import subprocess
import re
import concurrent.futures

os.environ["OLLAMA_NUM_PARALLEL"] = "10"
os.environ["OLLAMA_MAX_VRAM"] = "192000000000"

# Based on 2026 model research, we try a few plausible Ollama tag formats 
# for the newest generation of edge/workstation models.
MODELS_TO_TEST = [
    "gemma4:12b",
    "gemma4:4b", 
    "qwen3:7b-instruct",
    "qwen3:14b-instruct",
    "phi4:medium",
    "phi4",
    "llama4:scout",
    "llama4:8b"
]

def benchmark_model(model):
    print(f"[{model}] Pulling from registry...")
    pull_res = subprocess.run(["ollama", "pull", model], capture_output=True, text=True)
    if pull_res.returncode != 0:
        print(f"[{model}] Failed to pull model (tag might not exist). Skipping.")
        return None

    print(f"[{model}] Successfully pulled! Running eval pipeline...")
    env = os.environ.copy()
    env["LOCAL_MODEL"] = model
    env["MOCK"] = "0"
    env["LOCAL_BASE_URL"] = "http://localhost:11434/v1"
    env["LOCAL_API_KEY"] = "ollama"

    # Harness run
    harness_res = subprocess.run(["python", "eval/harness.py"], env=env, capture_output=True, text=True)
    acc = 0.0
    m = re.search(r"accuracy = ([\d\.]+)", harness_res.stdout)
    if m:
        acc = float(m.group(1))
        
    # FrugalRoute run
    out_file = f"out/{model.replace(':', '_')}_2026.jsonl"
    os.makedirs("out", exist_ok=True)
    run_res = subprocess.run(["python", "run.py", "--input", "eval/tasks.jsonl", "--output", out_file], env=env, capture_output=True, text=True)
    
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
        print(f"[{model}] DONE: {result}")
        return result
    except Exception as e:
        print(f"[{model}] Parse error: {e}")
        return None

def main():
    print(f"Starting 2026 SOTA parallel benchmark for up to {len(MODELS_TO_TEST)} models...")
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_model = {executor.submit(benchmark_model, model): model for model in MODELS_TO_TEST}
        for future in concurrent.futures.as_completed(future_to_model):
            res = future.result()
            if res:
                results.append(res)

    out_path = "eval/benchmark_2026.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved {out_path}")

if __name__ == "__main__":
    main()
