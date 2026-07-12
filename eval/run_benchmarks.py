import os
import time
import json
import subprocess
import requests

MODELS = [
    "Qwen/Qwen2.5-0.5B-Instruct",
    "google/gemma-2-2b-it",
    "Qwen/Qwen2.5-3B-Instruct",
    "microsoft/Phi-3.5-mini-instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "google/gemma-2-9b-it"
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

SSH_CMD = ["ssh", "-o", "StrictHostKeyChecking=no", "-i", r"c:\Users\katuk\.ssh\frugalroute_amd", "root@129.212.178.3"]
API_URL = "http://129.212.178.3:8001/v1"
API_KEY = "frugal-amd-7k2x"

def run_ssh(command, timeout=900):
    print(f"Running on remote: {command}")
    try:
        res = subprocess.run(SSH_CMD + [command], capture_output=True, text=True, timeout=timeout)
        if res.returncode != 0:
            print(f"SSH Error: {res.stderr}")
        return res.returncode, res.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"SSH Timeout for {command}")
        return -1, ""

def wait_for_vllm():
    print("Waiting for vLLM to be ready...")
    for _ in range(60):
        try:
            r = requests.get(f"{API_URL}/models", headers={"Authorization": f"Bearer {API_KEY}"})
            if r.status_code == 200:
                print("vLLM is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(10)
    return False

def get_vram_usage():
    _, out = run_ssh("rocm-smi --showuse | grep 'GPU use'")
    # We can approximate VRAM usage or just hardcode based on params for now since parsing rocm-smi might be tricky
    return out

def run_benchmarks():
    results = []
    
    for model in MODELS:
        print(f"\n{'='*50}\nBenchmarking {model}\n{'='*50}")
        
        # 1. Start vLLM
        run_ssh("docker rm -f frugal-vllm")
        start_cmd = (
            f"docker run -d --name frugal-vllm --network host "
            f"-v /root/.cache/huggingface:/root/.cache/huggingface "
            f"-e VLLM_HOST_IP=127.0.0.1 -e GLOO_SOCKET_IFNAME=lo -e NCCL_SOCKET_IFNAME=lo "
            f"--device=/dev/kfd --device=/dev/dri --group-add video "
            f"--ipc=host --cap-add=SYS_PTRACE --security-opt seccomp=unconfined "
            f"vllm/vllm-openai-rocm:v0.23.0 "
            f"--model {model} --host 0.0.0.0 --port 8001 --api-key {API_KEY} "
            f"--enable-prefix-caching --max-model-len 8192 --trust-remote-code"
        )
        run_ssh(start_cmd)
        
        if not wait_for_vllm():
            print(f"Failed to start vLLM for {model}. Skipping.")
            run_ssh("docker rm -f frugal-vllm")
            continue
            
        # Optional: estimate VRAM (fallback to simple heuristic if needed)
        vram = get_vram_usage()
        
        # 2. Run harness (fit calib.json)
        os.environ["LOCAL_MODEL"] = model
        os.environ["LOCAL_BASE_URL"] = API_URL
        os.environ["LOCAL_API_KEY"] = API_KEY
        os.environ["MOCK"] = "0"
        
        print("Running harness.py...")
        harness_res = subprocess.run(["python", "eval/harness.py"], capture_output=True, text=True, check=False)
        print(harness_res.stdout)
        
        # Extract accuracy from harness.py output
        acc = 0.0
        import re
        m = re.search(r"accuracy = ([\d\.]+)", harness_res.stdout)
        if m:
            acc = float(m.group(1))
        
        # 3. Run eval
        print("Running run.py...")
        import time
        t0 = time.time()
        out_file = f"out/{model.split('/')[-1]}.jsonl"
        run_res = subprocess.run(["python", "run.py", "--input", "eval/tasks.jsonl", "--output", out_file], capture_output=True, text=True, check=False)
        total_time = time.time() - t0
        avg_lat = total_time / 36.0
        print(run_res.stdout)
        
        # 4. Parse results from run.py stdout
        print("Parsing results...")
        try:
            import re
            content = run_res.stdout
            
            def extract_stat(name):
                m = re.search(fr'{name}=([\d\.]+)', content)
                return float(m.group(1)) if m else 0.0
            
            local_hit = extract_stat(r"free%")
            rem_tokens = extract_stat(r"remote_tokens")
            lat = round(avg_lat, 2)
            
            model_name = model.split("/")[-1]
            meta = MODEL_METADATA.get(model_name, {"params": "?", "vram_gb": "?"})
            results.append({
                "model": model_name,
                "params": meta["params"],
                "vram_gb": meta["vram_gb"],
                "local_hit_rate": local_hit,
                "remote_tokens": rem_tokens,
                "accuracy": acc,
                "latency_s": lat,
                "pick": meta.get("pick", "")
            })
        except Exception as e:
            print(f"Failed to parse results for {model}: {e}")
            
        # 5. Stop vLLM
        run_ssh("docker rm -f frugal-vllm")
        print(f"Finished {model}\n")
        
    # Save benchmark.json
    out_path = "eval/benchmark.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved {out_path}")

if __name__ == "__main__":
    run_benchmarks()
