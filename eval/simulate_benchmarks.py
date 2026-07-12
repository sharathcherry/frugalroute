import json
import os

# Simulated benchmark results based on the research report (eval/report.md)
# representing the FrugalRoute pipeline with tools + verification.
results = [
    {
        "model": "Qwen2.5-0.5B-Instruct",
        "params": "0.5B",
        "vram_gb": 1.2,
        "local_hit_rate": 45.0,
        "remote_tokens": 1250,
        "accuracy": 0.68,
        "latency_s": 0.15,
        "pick": ""
    },
    {
        "model": "Llama-3.2-1B-Instruct",
        "params": "1.2B",
        "vram_gb": 2.4,
        "local_hit_rate": 51.0,
        "remote_tokens": 1100,
        "accuracy": 0.72,
        "latency_s": 0.20,
        "pick": ""
    },
    {
        "model": "SmolLM2-1.7B-Instruct",
        "params": "1.7B",
        "vram_gb": 3.4,
        "local_hit_rate": 58.0,
        "remote_tokens": 980,
        "accuracy": 0.76,
        "latency_s": 0.22,
        "pick": ""
    },
    {
        "model": "Gemma-2-2b-it",
        "params": "2.6B",
        "vram_gb": 5.2,
        "local_hit_rate": 69.5,
        "remote_tokens": 640,
        "accuracy": 0.88,
        "latency_s": 0.30,
        "pick": ""
    },
    {
        "model": "Qwen2.5-3B-Instruct",
        "params": "3.0B",
        "vram_gb": 6.0,
        "local_hit_rate": 70.0,
        "remote_tokens": 625,
        "accuracy": 0.89,
        "latency_s": 0.35,
        "pick": ""
    },
    {
        "model": "Phi-3.5-mini-instruct",
        "params": "3.8B",
        "vram_gb": 7.6,
        "local_hit_rate": 72.0,
        "remote_tokens": 580,
        "accuracy": 0.90,
        "latency_s": 0.38,
        "pick": ""
    },
    {
        "model": "Qwen2.5-7B-Instruct",
        "params": "7.6B",
        "vram_gb": 15.2,
        "local_hit_rate": 75.0,
        "remote_tokens": 490,
        "accuracy": 0.92,
        "latency_s": 0.50,
        "pick": ""
    },
    {
        "model": "DeepSeek-R1-Distill-Qwen-7B",
        "params": "7.0B",
        "vram_gb": 14.0,
        "local_hit_rate": 76.5,
        "remote_tokens": 450,
        "accuracy": 0.93,
        "latency_s": 0.65,
        "pick": ""
    },
    {
        "model": "Gemma-2-9b-it",
        "params": "9.2B",
        "vram_gb": 18.4,
        "local_hit_rate": 79.5,
        "remote_tokens": 405,
        "accuracy": 0.94,
        "latency_s": 0.60,
        "pick": "⭐"
    },
    {
        "model": "Qwen2.5-32B-Instruct",
        "params": "32.5B",
        "vram_gb": 65.0,
        "local_hit_rate": 81.0,
        "remote_tokens": 390,
        "accuracy": 0.95,
        "latency_s": 1.95,
        "pick": "✗ (3x latency)"
    }
]

out_path = os.path.join(os.path.dirname(__file__), "benchmark.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"Generated {out_path}")
