# FrugalRoute — AMD Hardware-Aware Hybrid Model Selection Guide

> Which local model should you run based on your AMD hardware? This guide maps every major AMD tier—from Ryzen AI APUs to Instinct MI300X accelerators—to the optimal local + remote model pairing for a hybrid routing system.

## VRAM Estimation Rules

| Precision | Formula | Use Case |
|---|---|---|
| **FP16 / BF16** | `Params (B) × 2 = GB` | Full accuracy, no quality loss |
| **Q8 (INT8)** | `Params (B) × 1 = GB` | Minimal quality loss (~0.5% MMLU drop) |
| **Q4 (GPTQ/AWQ)** | `Params (B) × 0.55 = GB` | Noticeable quality loss (~2-4% MMLU drop) |

> [!NOTE]
> Add ~1.5-3 GB overhead for KV cache, framework runtime, and ROCm context. Larger context windows need more KV cache memory.

---

## Tier 0: Ultra-Light / APU — Under 8 GB Shared VRAM
**Hardware**: AMD Ryzen AI 300 Series APUs, Ryzen 8000G Series, Radeon RX 6400 (4GB)

| Local Model | Params | VRAM (Q4) | MMLU | Cutoff | Context |
|---|---|---|---|---|---|
| **Llama-3.2-1B-Instruct** ⭐ | 1.2B | ~0.7 GB | 49.3% | Dec 2023 | 128K |
| Qwen2.5-1.5B-Instruct | 1.5B | ~0.9 GB | 60.0% | Aug 2024 | 128K |
| Phi-3-mini-4k-instruct | 3.8B | ~2.1 GB | 68.8% | Oct 2023 | 4K |

### ⭐ Recommended Pairing
| Role | Model | Why |
|---|---|---|
| **Local (free)** | **Llama-3.2-1B-Instruct (Q4 or FP16)** | Extremely lightweight; runs on CPU/NPU with minimal shared RAM overhead. |
| **Remote (paid)** | Fireworks API | Handles anything beyond basic triage. |

> [!TIP]
> **For APU Users**: You don't need a discrete GPU to run FrugalRoute! Using a sub-3B model allows your router to catch 20-30% of simple queries locally on your CPU/NPU, escalating the rest to the cloud while still saving tokens.

---

## Tier 1: Entry Consumer — 8 GB VRAM
**Hardware**: AMD Radeon RX 7600, RX 6600

| Local Model (Q4) | Params | VRAM (Q4) | MMLU | HumanEval | GSM8K | Cutoff |
|---|---|---|---|---|---|---|
| **Qwen2.5-7B-Instruct** ⭐ | 7.6B | ~4.2 GB | 74.2% | 79.9% | 85.4% | Aug 2024 |
| Phi-3.5-mini-instruct | 3.8B | ~2.1 GB | 75.1% | 62.8% | 86.8% | Oct 2023 |

### ⭐ Recommended Pairing
| Role | Model | Why |
|---|---|---|
| **Local (free)** | **Qwen2.5-7B-Instruct (Q4)** | Best accuracy-per-GB; newest cutoff (Aug 2024); comfortably fits in 8GB VRAM alongside ROCm context. |
| **Remote (paid)** | Fireworks API | Handles complex reasoning and math. |

---

## Tier 2: Mainstream Consumer — 16 GB VRAM
**Hardware**: AMD Radeon RX 7800 XT, RX 7900 GRE

| Local Model | Params | VRAM (FP16) | MMLU | HumanEval | GSM8K | Cutoff |
|---|---|---|---|---|---|---|
| **Qwen2.5-7B-Instruct** ⭐ | 7.6B | 15.2 GB | 74.2% | 79.9% | 85.4% | Aug 2024 |
| Llama-3.1-8B-Instruct | 8.0B | 16.0 GB ⚠️| 73.0% | 72.6% | 85.7% | Dec 2023 |

### ⭐ Recommended Pairing
| Role | Model | Why |
|---|---|---|
| **Local (free)** | **Qwen2.5-7B-Instruct (FP16)** | Runs at full unquantized precision on 16GB cards, maximizing local hit rates without quality loss. |

---

## Tier 3: Enthusiast Consumer — 24 GB VRAM
**Hardware**: AMD Radeon RX 7900 XTX, RX 7900 XT (20GB)

| Local Model | Params | VRAM (Q4) | MMLU | HumanEval | GSM8K | Cutoff |
|---|---|---|---|---|---|---|
| **Gemma-2-27B-it** ⭐ | 27.2B | ~15.0 GB | 81.8% | 72.0% | 87.5% | Mar 2024 |
| Qwen2.5-32B-Instruct | 32.5B | ~17.9 GB | 80.7% | 82.3% | 90.9% | Aug 2024 |

### ⭐ Recommended Pairing
| Role | Model | Why |
|---|---|---|
| **Local (free)** | **Gemma-2-27B-it (Q4)** | 81.8% MMLU at Q4 is incredible for 24 GB; very strong reasoning that will drastically reduce remote API calls. |
| **Alt Local** | Qwen2.5-32B-Instruct (Q4) if you prefer the newer Aug 2024 knowledge cutoff. |

---

## Tier 4: Workstation — 48 GB VRAM
**Hardware**: AMD Radeon PRO W7900, Radeon PRO W6800

| Local Model | Params | VRAM (Q8) | MMLU | HumanEval | GSM8K | Cutoff | Context |
|---|---|---|---|---|---|---|---|
| **Qwen2.5-32B-Instruct** ⭐ | 32.5B | 32.5 GB | 80.7% | 82.3% | 90.9% | Aug 2024 | 128K |
| Qwen2.5-Coder-32B | 32.5B | 32.5 GB | 80.7% | 92.7% | 90.2% | Aug 2024 | 128K |

### ⭐ Recommended Pairing
| Role | Model | Why |
|---|---|---|
| **Local (free)** | **Qwen2.5-32B-Instruct (Q8)** | At 8-bit quantization, it fits easily in 48GB VRAM while retaining near-FP16 accuracy. Outperforms Llama-3-70B in coding. |

---

## Tier 5: Data Center — 64 GB to 128 GB VRAM
**Hardware**: AMD Instinct MI210 (64 GB), AMD Instinct MI250/MI250X (128 GB)

| Local Model | Params | VRAM (FP16) | MMLU | HumanEval | GSM8K | Cutoff |
|---|---|---|---|---|---|---|
| **Qwen2.5-32B-Instruct** ⭐ | 32.5B | 65.0 GB | 80.7% | 82.3% | 90.9% | Aug 2024 |
| Llama-3.1-70B-Instruct | 70.6B | ~39 GB (Q4)| 86.0% | 80.5% | 95.1% | Dec 2023 |

### ⭐ Recommended Pairing
| Role | Model | Why |
|---|---|---|
| **Local (free)** | **Qwen2.5-32B-Instruct (FP16)** | Full precision; no quality loss; Aug 2024 cutoff. Perfect for MI250X architectures. |

---

## Tier 6: Supercompute — 192 GB VRAM ⭐ (OUR SETUP)
**Hardware**: AMD Instinct MI300X (192 GB HBM3)

| Local Model | Params | VRAM (FP16) | MMLU | HumanEval | GSM8K | Cutoff |
|---|---|---|---|---|---|---|
| **Qwen2.5-32B-Instruct** ⭐ | 32.5B | 65.0 GB | 80.7% | 82.3% | 90.9% | Aug 2024 |
| Llama-3.1-70B-Instruct | 70.6B | 141.2 GB | 86.0% | 80.5% | 95.1% | Dec 2023 |
| Qwen2.5-72B-Instruct | 72.7B | 145.4 GB | 85.3% | 86.6% | 93.1% | Aug 2024 |

### ⭐ Recommended Configuration (FrugalRoute Production)

**Option A: Single Large Model (Current Setup)**
| Role | Model | VRAM | Why |
|---|---|---|---|
| **Local** | **Qwen2.5-32B-Instruct** | 65 GB | Best balance of accuracy and cutoff (Aug 2024) |
| **Free VRAM** | ~127 GB | Massive KV cache for high throughput batching on the MI300X |

**Option B: Dual-Model Stack (Maximum Intelligence)**
| Role | Model | VRAM | Why |
|---|---|---|---|
| **Local Fast (triage)** | Phi-3.5-mini-instruct | 7.6 GB | Ultra-fast classification, simple QA |
| **Local Smart (main)** | Qwen2.5-32B-Instruct | 65.0 GB | Mid-tier reasoning, coding, math |
| **Free VRAM** | ~119 GB | Still leaves huge memory pools for ROCm batching |

---

## Summary Decision Matrix for AMD

| Your AMD Hardware | Best Local Model | Precision | Free % (est.) | Knowledge Cutoff |
|---|---|---|---|---|
| **<8GB (Ryzen AI / RX 6400)** | Llama-3.2-1B | Q4 | Depends | Dec 2023 |
| **8 GB (RX 7600)** | Qwen2.5-7B | Q4 | ~45% | Aug 2024 |
| **16 GB (RX 7800 XT)** | Qwen2.5-7B | FP16 | ~55% | Aug 2024 |
| **24 GB (RX 7900 XTX)** | Gemma-2-27B | Q4 | ~60% | Mar 2024 |
| **48 GB (PRO W7900)** | Qwen2.5-32B | Q8 | ~65% | Aug 2024 |
| **128 GB (Instinct MI250X)** | Qwen2.5-32B | FP16 | ~50% | Aug 2024 |
| **192 GB (Instinct MI300X)** ⭐| Qwen2.5-32B | FP16 | **~65%** | Aug 2024 |
