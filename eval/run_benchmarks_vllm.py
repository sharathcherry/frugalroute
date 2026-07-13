#!/usr/bin/env python3
"""
Gemma 4 vLLM benchmark - clean run.
Entrypoint in vllm/vllm-openai-rocm is ['vllm','serve'],
so model name goes directly after image as positional arg.
"""
import subprocess, time, sys, os, json, re, requests

HF_TOKEN  = os.environ.get("HF_TOKEN", "")
API_KEY   = "frugal-amd-7k2x"
IMAGE     = "vllm/vllm-openai-rocm:v0.23.0"
HF_CACHE  = os.path.expanduser("~/.cache/huggingface")
PORT      = 8010          # single port, sequential runs
RESULTS   = "/root/frugalroute/eval/benchmark_gemma4.json"

MODELS = [
    "google/gemma-4-E2B-it",
    "google/gemma-4-E4B-it",
    "google/gemma-4-12B-it",
    "google/gemma-4-26B-A4B-it",
    "google/gemma-4-31B-it",
]

def vram_pct():
    r = subprocess.run(["rocm-smi","--showmemuse"], capture_output=True, text=True)
    m = re.search(r"GPU Memory Allocated \(VRAM%\):\s*(\d+)", r.stdout)
    return int(m.group(1)) if m else 0

def server_ready(timeout=360):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if requests.get(f"http://localhost:{PORT}/health", timeout=3).status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(5)
    return False

def run(model):
    cname = "gemma4_bench"
    short = model.split("/")[-1]
    print(f"\n{'='*60}", flush=True)
    print(f"[{short}] Cleaning up previous container...", flush=True)
    subprocess.run(["docker","rm","-f", cname], capture_output=True)
    time.sleep(2)

    before = vram_pct()
    print(f"[{short}] VRAM before: {before}%  Starting container...", flush=True)

    # Correct invocation: entrypoint is 'vllm serve', model is positional arg
    proc = subprocess.run([
        "docker","run","-d","--name", cname,
        "--device=/dev/kfd","--device=/dev/dri",
        "--group-add","video",
        "--ipc=host","--shm-size=16g",
        "-v", f"{HF_CACHE}:/root/.cache/huggingface",
        "-p", f"{PORT}:{PORT}",
        "-e", f"HF_TOKEN={HF_TOKEN}",
        "-e", f"HUGGING_FACE_HUB_TOKEN={HF_TOKEN}",
        IMAGE,
        model,                          # positional: vllm serve <model>
        "--host","0.0.0.0",
        "--port", str(PORT),
        "--api-key", API_KEY,
        "--dtype","bfloat16",
        "--max-model-len","4096",
        "--trust-remote-code",
    ], capture_output=True, text=True)

    if proc.returncode != 0:
        print(f"[{short}] ABORT: docker run failed:\n{proc.stderr[:400]}", flush=True)
        return None

    print(f"[{short}] Container up. Waiting for server (up to 6 min)...", flush=True)
    if not server_ready(360):
        logs = subprocess.run(["docker","logs","--tail","40", cname],
                               capture_output=True, text=True)
        print(f"[{short}] ABORT: server not ready. Logs:\n{logs.stdout}\n{logs.stderr}", flush=True)
        subprocess.run(["docker","rm","-f", cname], capture_output=True)
        return None

    time.sleep(5)
    after = vram_pct()
    delta = after - before
    print(f"[{short}] VRAM after: {after}%  delta=+{delta}%", flush=True)

    if delta < 5:
        print(f"[{short}] *** ABORT: model NOT on GPU (delta only {delta}%) ***", flush=True)
        subprocess.run(["docker","rm","-f", cname], capture_output=True)
        return None

    print(f"[{short}] GPU CONFIRMED (+{delta}% VRAM). Running harness...", flush=True)

    env = {**os.environ,
           "LOCAL_MODEL": model,
           "MOCK": "0",
           "LOCAL_BASE_URL": f"http://localhost:{PORT}/v1",
           "LOCAL_API_KEY": API_KEY}

    harness = subprocess.run([sys.executable,"eval/harness.py"],
                             env=env, capture_output=True, text=True,
                             cwd="/root/frugalroute")
    acc = 0.0
    m = re.search(r"accuracy\s*=\s*([\d.]+)", harness.stdout)
    if m: acc = float(m.group(1))
    print(f"[{short}] accuracy={acc}", flush=True)

    os.makedirs("/root/frugalroute/out", exist_ok=True)
    out_f = f"/root/frugalroute/out/{short}.jsonl"
    run_p = subprocess.run([sys.executable,"run.py",
                            "--input","eval/tasks.jsonl","--output", out_f],
                           env=env, capture_output=True, text=True,
                           cwd="/root/frugalroute")
    hit, rtok = 0.0, 0.0
    m2 = re.search(r"free%\s*=\s*([\d.]+)", run_p.stdout)
    m3 = re.search(r"remote_tokens\s*=\s*([\d.]+)", run_p.stdout)
    if m2: hit  = float(m2.group(1))
    if m3: rtok = float(m3.group(1))

    result = {"model": model, "accuracy": acc, "local_hit_rate": hit,
              "remote_tokens": rtok, "vram_delta_pct": delta}
    print(f"[{short}] RESULT: {result}", flush=True)
    subprocess.run(["docker","rm","-f", cname], capture_output=True)
    return result


def main():
    print("="*60, flush=True)
    print("Gemma 4 Benchmark — GPU verified, sequential (resume-safe)", flush=True)
    print("="*60, flush=True)

    # Load existing results so we can resume after a crash
    results = []
    if os.path.exists(RESULTS):
        with open(RESULTS) as f:
            results = json.load(f)
    done = {r["model"] for r in results}

    remaining = [m for m in MODELS if m not in done]
    print(f"Already done : {list(done)}", flush=True)
    print(f"Still to run : {remaining}", flush=True)

    for model in remaining:
        r = run(model)
        if r:
            results.append(r)
        # Checkpoint after every model (done or skipped)
        with open(RESULTS, "w") as f:
            json.dump(results, f, indent=2)
        print(f"[checkpoint] {len(results)}/{len(MODELS)} done", flush=True)

    print(f"\n{'='*60}", flush=True)
    print(f"DONE: {len(results)}/{len(MODELS)} models benchmarked on GPU.", flush=True)
    print(f"Results: {RESULTS}", flush=True)

if __name__ == "__main__":
    main()
