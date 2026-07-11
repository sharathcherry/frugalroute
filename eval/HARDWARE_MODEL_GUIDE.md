# FrugalRoute — Hardware-Aware Hybrid Model Selection Guide

> Which local model should you run based on your GPU? This guide maps every major hardware tier to the optimal local + remote model pairing for a hybrid routing system.

## VRAM Estimation Rules

| Precision | Formula | Use Case |
|---|---|---|
| **FP16 / BF16** | `Params (B) × 2 = GB` | Full accuracy, no quality loss |
| **Q8 (INT8)** | `Params (B) × 1 = GB` | Minimal quality loss (~0.5% MMLU drop) |
| **Q4 (GPTQ/AWQ)** | `Params (B) × 0.55 = GB` | Noticeable quality loss (~2-4% MMLU drop) |

> Add ~1.5-3 GB overhead for KV cache, framework runtime, and CUDA/ROCm context. Larger context windows need more KV cache memory.

---

## Tier 1: Consumer GPU — 8 GB VRAM
**GPUs**: RTX 3060 8GB, RTX 4060, RX 7600, Intel Arc A770

| Local Model (Q4) | Params | VRAM (Q4) | MMLU | HumanEval | GSM8K | Cutoff | Context |
|---|---|---|---|---|---|---|---|
| **Phi-3.5-mini-instruct** | 3.8B | ~2.1 GB | 75.1% | 62.8% | 86.8% | Oct 2023 | 128K |
| Llama-3.2-3B-Instruct | 3.2B | ~1.8 GB | 63.4% | 60.4% | 73.1% | Dec 2023 | 128K |
| Qwen2.5-7B-Instruct | 7.6B | ~4.2 GB | 74.2% | 79.9% | 85.4% | Aug 2024 | 128K |

### Recommended Pairing
| Role | Model | Why |
|---|---|---|
| **Local (free)** | **Qwen2.5-7B-Instruct (Q4)** | Best accuracy-per-GB; most recent cutoff (Aug 2024); fits in 8GB with Q4 |
| **Remote (paid)** | Fireworks GPT-OSS-120B / GPT-4o | Handles reasoning, math, long-context |

---

## Tier 2: Consumer GPU — 12 GB VRAM
**GPUs**: RTX 3060 12GB, RTX 4070, RX 7700 XT

| Local Model | Params | VRAM (FP16) | VRAM (Q4) | MMLU | HumanEval | GSM8K | Cutoff | Context |
|---|---|---|---|---|---|---|---|---|
| **Qwen2.5-7B-Instruct** | 7.6B | 15.2 GB | 4.2 GB | 74.2% | 79.9% | 85.4% | Aug 2024 | 128K |
| Gemma-2-9B-it | 9.2B | 18.4 GB | 5.1 GB | 79.6% | 68.3% | 77.9% | Mar 2024 | 8K |
| Llama-3.1-8B-Instruct | 8.0B | 16.0 GB | 4.4 GB | 73.0% | 72.6% | 85.7% | Dec 2023 | 128K |

### Recommended Pairing
| Role | Model | Why |
|---|---|---|
| **Local (free)** | **Qwen2.5-7B-Instruct (Q8)** | Q8 fits (~7.6 GB) with minimal quality loss; best coding score (79.9%); newest cutoff |
| **Remote (paid)** | Fireworks GPT-OSS-120B | Complex reasoning fallback |

---

## Tier 3: Consumer GPU — 16 GB VRAM
**GPUs**: RTX 4070 Ti, RTX 4080, RX 7800 XT

| Local Model | Params | VRAM (FP16) | MMLU | HumanEval | GSM8K | Cutoff | Context |
|---|---|---|---|---|---|---|---|
| **Qwen2.5-7B-Instruct** | 7.6B | 15.2 GB | 74.2% | 79.9% | 85.4% | Aug 2024 | 128K |
| Gemma-2-9B-it | 9.2B | 18.4 GB | 79.6% | 68.3% | 77.9% | Mar 2024 | 8K |
| Llama-3.1-8B-Instruct | 8.0B | 16.0 GB | 73.0% | 72.6% | 85.7% | Dec 2023 | 128K |

### Recommended Pairing
| Role | Model | Why |
|---|---|---|
| **Local (free)** | **Qwen2.5-7B-Instruct (FP16)** | Full precision fits perfectly; no quantization quality loss; Aug 2024 cutoff |
| **Remote (paid)** | Fireworks GPT-OSS-120B | For hard reasoning and math |

---

## Tier 4: Prosumer GPU — 24 GB VRAM
**GPUs**: RTX 3090, RTX 4090, RTX A5000, RX 7900 XTX

| Local Model | Params | VRAM (FP16) | VRAM (Q4) | MMLU | HumanEval | GSM8K | Cutoff | Context |
|---|---|---|---|---|---|---|---|---|
| Qwen2.5-7B-Instruct (FP16) | 7.6B | 15.2 GB | — | 74.2% | 79.9% | 85.4% | Aug 2024 | 128K |
| Gemma-2-9B-it (FP16) | 9.2B | 18.4 GB | — | 79.6% | 68.3% | 77.9% | Mar 2024 | 8K |
| **Gemma-2-27B-it (Q4)** | 27.2B | 54.4 GB | 15.0 GB | 81.8% | 72.0% | 87.5% | Mar 2024 | 8K |

### Recommended Pairing
| Role | Model | Why |
|---|---|---|
| **Local (free)** | **Gemma-2-27B-it (Q4)** | 81.8% MMLU at Q4 is incredible for 24 GB; strong reasoning |
| **Alt Local** | Qwen2.5-7B (FP16) if you need 128K context and newest cutoff |
| **Remote (paid)** | Fireworks GPT-OSS-120B | Only for truly hard multi-step reasoning |

> This is the sweet spot for hobbyists. A Q4-quantized 27B model on a 4090 gives you 80%+ MMLU accuracy locally for FREE, reducing remote API costs by 60-70%.

---

## Tier 5: Workstation GPU — 48 GB VRAM
**GPUs**: RTX A6000, RTX 6000 Ada, Dual RTX 3090 (NVLink)

| Local Model | Params | VRAM (Q8) | MMLU | HumanEval | GSM8K | Cutoff | Context |
|---|---|---|---|---|---|---|---|
| **Qwen2.5-32B-Instruct (Q8)** | 32.5B | 32.5 GB | 80.7% | 82.3% | 90.9% | Aug 2024 | 128K |
| Qwen2.5-Coder-32B (Q8) | 32.5B | 32.5 GB | 80.7% | 92.7% | 90.2% | Aug 2024 | 128K |
| Gemma-2-27B-it (FP16) | 27.2B | 27.2 GB | 81.8% | 72.0% | 87.5% | Mar 2024 | 8K |

### Recommended Pairing
| Role | Model | Why |
|---|---|---|
| **Local (free)** | **Qwen2.5-32B-Instruct (Q8)** | Fits at Q8 (~32.5 GB); HumanEval 82.3% beats Llama-3.1-70B; newest cutoff |
| **Alt Local** | Qwen2.5-Coder-32B (Q8) if workload is code-heavy (92.7% HumanEval!) |
| **Remote (paid)** | Fireworks GPT-OSS-120B | Rare fallback — 32B handles most tasks |

---

## Tier 6: Data Center GPU — 80 GB VRAM
**GPUs**: NVIDIA A100 80GB, NVIDIA H100, AMD MI250X

| Local Model | Params | VRAM (FP16) | MMLU | HumanEval | GSM8K | Cutoff | Context |
|---|---|---|---|---|---|---|---|
| **Qwen2.5-32B-Instruct (FP16)** | 32.5B | 65.0 GB | 80.7% | 82.3% | 90.9% | Aug 2024 | 128K |
| Llama-3.1-70B-Instruct (Q4) | 70.6B | 38.8 GB | 86.0% | 80.5% | 95.1% | Dec 2023 | 128K |
| Qwen2.5-72B-Instruct (Q4) | 72.7B | 40.0 GB | 85.3% | 86.6% | 93.1% | Aug 2024 | 128K |

### Recommended Pairing
| Role | Model | Why |
|---|---|---|
| **Local (free)** | **Qwen2.5-32B-Instruct (FP16)** | Full precision; no quality loss; Aug 2024 cutoff; 128K context |
| **Alt Local** | Qwen2.5-72B (Q4) if you want maximum accuracy (85.3% MMLU) |
| **Remote (paid)** | Fireworks GPT-OSS-120B | Only for edge-case reasoning |

---

## Tier 7: Cloud Enterprise GPU — 192 GB VRAM (OUR SETUP)
**GPUs**: AMD Instinct MI300X (192 GB HBM3), NVIDIA H200

| Local Model | Params | VRAM (FP16) | MMLU | HumanEval | GSM8K | Cutoff | Context |
|---|---|---|---|---|---|---|---|
| **Qwen2.5-32B-Instruct (FP16)** | 32.5B | 65.0 GB | 80.7% | 82.3% | 90.9% | Aug 2024 | 128K |
| Llama-3.1-70B-Instruct (FP16) | 70.6B | 141.2 GB | 86.0% | 80.5% | 95.1% | Dec 2023 | 128K |
| Qwen2.5-72B-Instruct (FP16) | 72.7B | 145.4 GB | 85.3% | 86.6% | 93.1% | Aug 2024 | 128K |

### Recommended Configuration (FrugalRoute Production)

**Option A: Single Large Model (Current Setup)**
| Role | Model | VRAM | Why |
|---|---|---|---|
| **Local (free)** | **Qwen2.5-32B-Instruct** | 65 GB | Best balance of accuracy, cutoff (Aug 2024), and headroom for KV cache |
| **Remote (paid)** | Fireworks GPT-OSS-120B | Complex reasoning only |
| **Free VRAM** | ~127 GB | Massive KV cache for high throughput batching |

**Option B: Dual-Model Stack (Maximum Intelligence)**
| Role | Model | VRAM | Why |
|---|---|---|---|
| **Local Fast (triage)** | Phi-3.5-mini-instruct | 7.6 GB | Ultra-fast classification, simple QA |
| **Local Smart (main)** | Qwen2.5-32B-Instruct | 65.0 GB | Mid-tier reasoning, coding, math |
| **Remote (paid)** | Fireworks GPT-OSS-120B | Only truly hard tasks |
| **Free VRAM** | ~119 GB | KV cache + batching |

**Option C: Maximum Accuracy Stack**
| Role | Model | VRAM | Why |
|---|---|---|---|
| **Local Oracle** | Qwen2.5-72B-Instruct | 145.4 GB | 85.3% MMLU; Aug 2024 cutoff; almost never needs remote |
| **Remote (paid)** | Fireworks GPT-OSS-120B | Extreme edge cases only |
| **Free VRAM** | ~46 GB | Enough for moderate batching |

---

## Tier 8: Multi-GPU Cluster — 320+ GB VRAM
**GPUs**: 2x MI300X (384 GB), 4x A100 (320 GB), 8x H100 (640 GB)

| Local Model | Params | VRAM (FP16) | MMLU | HumanEval | GSM8K | Cutoff |
|---|---|---|---|---|---|---|
| DeepSeek-V3 (MoE, 37B active) | 671B total | ~200 GB | 88.5% | 90.2% | 95.3% | Jul 2024 |
| DeepSeek-R1 (MoE, 37B active) | 671B total | ~200 GB | 89.1% | 92.8% | 96.3% | Jul 2024 |

### Recommended Pairing
| Role | Model | Why |
|---|---|---|
| **Local (free)** | **DeepSeek-V3 (MoE)** | 88.5% MMLU; only 37B active params = fast; rivals GPT-4 |
| **Remote (paid)** | Almost never needed | DeepSeek-V3 handles 95%+ of tasks locally |

> At this tier, the hybrid routing system becomes almost unnecessary — the local model is so powerful that remote escalation drops to less than 5% of queries.

---

## Knowledge Cutoff Quick Reference

| Cutoff Date | What the model KNOWS | What it will HALLUCINATE about |
|---|---|---|
| **Sep 2022** (Llama-2) | Pre-ChatGPT world | ChatGPT launch, GPT-4, all 2023-2025 events |
| **Oct 2023** (Phi-3.5) | ChatGPT era, early GPT-4 | 2024 elections, Gemini launch, DeepSeek |
| **Dec 2023** (Llama-3.1) | Full 2023 coverage | 2024 events onwards |
| **Aug 2024** (Qwen2.5) | Most of 2024 | Late 2024 and 2025 events |
| **Jul 2024** (DeepSeek-V3) | Most of 2024 | Late 2024 and 2025 events |

> **For FrugalRoute**: Qwen2.5-32B (Aug 2024 cutoff) is the safest choice for general-purpose routing because it has the most recent training data of any non-MoE model in its size class.

---

## Summary Decision Matrix

| Your GPU VRAM | Best Local Model | Precision | Free % (est.) | Knowledge Cutoff |
|---|---|---|---|---|
| **8 GB** | Qwen2.5-7B (Q4) | Q4 | ~45% | Aug 2024 |
| **12 GB** | Qwen2.5-7B (Q8) | Q8 | ~50% | Aug 2024 |
| **16 GB** | Qwen2.5-7B (FP16) | FP16 | ~55% | Aug 2024 |
| **24 GB** | Gemma-2-27B (Q4) | Q4 | ~60% | Mar 2024 |
| **48 GB** | Qwen2.5-32B (Q8) | Q8 | ~65% | Aug 2024 |
| **80 GB** | Qwen2.5-32B (FP16) | FP16 | ~65% | Aug 2024 |
| **192 GB** | Qwen2.5-32B (FP16) | FP16 | **~61%** (measured) | Aug 2024 |
| **384 GB+** | DeepSeek-V3 (FP16) | FP16 | ~95% | Jul 2024 |
