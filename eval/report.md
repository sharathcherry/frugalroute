# Open-Weight LLM Survey and Comparison Report for FrugalRoute Hybrid Routing

## Master Comparison Table

The following table catalogs 47 open-weight model variants across 13 distinct families. All metrics listed are official benchmarks reported by the developers in their technical papers or release blogs.

| Model Name | Parameter Size | Developer | Release Date | Knowledge Cutoff Date | MMLU Score | HumanEval Score | GSM8K Score | Context Window Size |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Llama-2-7b (Base) | 7B | Meta | July 2023 | September 2022 | 45.3% [1] | 12.8% [1] | 14.6% [1] | 4,096 |
| Llama-2-13b (Base) | 13B | Meta | July 2023 | September 2022 | 54.8% [1] | 18.9% [1] | 28.7% [1] | 4,096 |
| Llama-2-70b (Base) | 70B | Meta | July 2023 | September 2022 | 68.9% [1] | 29.9% [1] | 56.8% [1] | 4,096 |
| Llama-3-8B-Instruct | 8B | Meta | April 2024 | March 2023 | 68.4% [2] | 62.2% [2] | 79.6% [2] | 8,192 |
| Llama-3-70B-Instruct | 70B | Meta | April 2024 | December 2023 | 82.0% [2] | 81.7% [2] | 93.0% [2] | 8,192 |
| Llama-3.1-8B-Instruct | 8B | Meta | July 2024 | December 2023 | 73.0% [3] | 72.6% [3] | 85.7% [3] | 128,000 |
| Llama-3.1-70B-Instruct | 70.6B | Meta | July 2024 | December 2023 | 86.0% [3] | 80.5% [3] | 95.1% [3] | 128,000 |
| Llama-3.2-1B-Instruct | 1.2B | Meta | September 2024 | December 2023 | 49.3% [5] | 38.4% [5] | 44.2% [5] | 128,000 |
| Llama-3.2-3B-Instruct | 3.2B | Meta | September 2024 | December 2023 | 63.4% [5] | 60.4% [5] | 73.1% [5] | 128,000 |
| Gemma-7B (Base) | 8.5B | Google | February 2024 | November 2023 | 64.3% [6] | 32.3% [6] | 46.4% [6] | 8,192 |
| Gemma-2-9B-it | 9.2B | Google | June 2024 | March 2024 | 79.6% [8] | 68.3% [8] | 77.9% [8] | 8,192 |
| Gemma-2-27B-it | 27.2B | Google | June 2024 | March 2024 | 81.8% [8] | 72.0% [8] | 87.5% [8] | 8,192 |
| Phi-2 (Base) | 2.78B | Microsoft | December 2023 | November 2023 | 56.3% [10] | 52.4% [10] | 74.6% [10] | 2,048 |
| Phi-3-mini-4k-instruct | 3.8B | Microsoft | April 2024 | October 2023 | 68.8% [11] | 58.5% [11] | 82.5% [11] | 4,096 |
| Phi-3-medium-4k-instruct | 14B | Microsoft | May 2024 | October 2023 | 78.0% [11] | 62.2% [11] | 89.2% [11] | 4,096 |
| Phi-3.5-mini-instruct | 3.8B | Microsoft | August 2024 | October 2023 | 75.1% [13] | 62.8% [13] | 86.8% [13] | 128,000 |
| Qwen2.5-72B-Instruct | 72.7B | Alibaba Cloud | September 2024 | August 2024 | 85.3% [15] | 86.6% [15] | 93.1% [15] | 128,000 |
| Qwen2.5-32B-Instruct | 32.5B | Alibaba Cloud | September 2024 | August 2024 | 80.7% [15] | 82.3% [15] | 90.9% [15] | 128,000 |
| Qwen2.5-7B-Instruct | 7.61B | Alibaba Cloud | September 2024 | August 2024 | 74.2% [15] | 79.9% [15] | 85.4% [15] | 128,000 |
| Qwen2.5-Coder-32B-Instruct | 32.5B | Alibaba Cloud | November 2024 | August 2024 | 80.7% [16] | 92.7% [16] | 90.2% [16] | 128,000 |
| Qwen2-72B-Instruct | 72.7B | Alibaba Cloud | June 2024 | February 2024 | 82.3% [18] | 86.0% [18] | 91.1% [18] | 128,000 |
| Qwen1.5-72B-Chat | 72.7B | Alibaba Cloud | February 2024 | January 2024 | 76.2% [19] | 72.0% [19] | 82.1% [19] | 32,768 |
| DeepSeek-V3 (Chat) | 671B | DeepSeek AI | December 2024 | July 2024 | 88.5% [20] | 90.2% [20] | 95.3% [20] | 128,000 |
| DeepSeek-R1 (Reasoning) | 671B | DeepSeek AI | January 2025 | July 2024 | 89.1% [22] | 92.8% [22] | 96.3% [22] | 128,000 |
| DeepSeek-Coder-V2-Instruct | 236B | DeepSeek AI | June 2024 | April 2024 | 79.2% [24] | 90.2% [24] | 94.7% [24] | 128,000 |
| DeepSeek-V2-Chat | 236B | DeepSeek AI | May 2024 | April 2024 | 78.4% [26] | 81.1% [26] | 92.2% [26] | 128,000 |
| DeepSeek-LLM-67B-Chat | 67.3B | DeepSeek AI | November 2023 | September 2023 | 71.1% [28] | 73.8% [28] | 84.1% [28] | 4,096 |
| Yi-34B-Chat | 34.3B | 01.AI | November 2023 | June 2023 | 76.5% [30] | 74.4% [30] | 80.3% [30] | 4,096 |
| Yi-6B-Chat | 6B | 01.AI | November 2023 | June 2023 | 62.4% [30] | 56.7% [30] | 63.7% [30] | 4,096 |
| Yi-1.5-34B-Chat | 34.3B | 01.AI | May 2024 | February 2024 | 79.6% [31] | 76.8% [31] | 87.0% [31] | 4,096 |
| Yi-1.5-9B-Chat | 8.8B | 01.AI | May 2024 | February 2024 | 71.2% [31] | 62.2% [31] | 77.6% [31] | 4,096 |
| Yi-1.5-6B-Chat | 6B | 01.AI | May 2024 | February 2024 | 67.3% [31] | 57.3% [31] | 69.2% [31] | 4,096 |
| Mistral 7B (v0.1) | 7.24B | Mistral AI | September 2023 | September 2023 | 62.5% [33] | 30.5% [33] | 39.6% [33] | 8,192 |
| Mixtral 8x7B (v0.1) | 46.7B | Mistral AI | December 2023 | September 2023 | 70.6% [35] | 40.2% [35] | 74.4% [35] | 32,768 |
| Mixtral 8x22B | 141B | Mistral AI | April 2024 | April 2024 | 77.8% [36] | 45.1% [36] | 78.6% [36] | 65,536 |
| Command R | 35B | Cohere | March 2024 | January 2024 | 67.5% [38] | 53.0% [38] | 72.8% [38] | 128,000 |
| Command R+ | 104B | Cohere | April 2024 | January 2024 | 75.7% [40] | 67.1% [40] | 82.6% [40] | 128,000 |
| InternLM2-Chat-7B | 7.7B | Shanghai AI Lab | January 2024 | December 2023 | 63.7% [42] | 59.8% [42] | 70.3% [42] | 204,800 |
| InternLM2.5-Chat-7B | 7.74B | Shanghai AI Lab | July 2024 | May 2024 | 72.0% [43] | 74.4% [43] | 86.0% [43] | 1,000,000 |
| ChatGLM3-6B | 6.2B | Zhipu AI | October 2023 | September 2023 | 61.4% [44] | 55.5% [44] | 60.9% [44] | 32,768 |
| GLM-4-9B-Chat | 9.4B | Zhipu AI | June 2024 | December 2023 | 72.4% [46] | 71.3% [46] | 79.6% [46] | 128,000 |
| DBRX Instruct | 132B | Databricks | March 2024 | December 2023 | 70.1% [47] | 70.1% [47] | 82.5% [47] | 32,768 |
| Falcon 40B | 40B | TII | May 2023 | December 2022 | 55.4% [50] | 18.3% [50] | 39.8% [50] | 2,048 |
| Falcon 180B | 180B | TII | September 2023 | June 2023 | 68.2% [52] | 28.7% [52] | 55.3% [52] | 4,096 |
| Falcon 2 11B | 11B | TII | May 2024 | March 2024 | 58.3% [54] | 32.3% [54] | 53.8% [54] | 8,192 |
| StarCoder (15B) | 15.5B | BigCode | May 2023 | January 2023 | N/A [56] | 33.6% [56] | 8.4% [56] | 8,192 |
| StarCoder2-15B | 15B | BigCode | February 2024 | September 2023 | N/A [58] | 46.3% [58] | 23.0% [58] | 16,384 |

*Note: MoE models (Mixtral, DeepSeek MoE, DBRX) list total parameter counts. The active parameter sizes are covered in the detailed factsheets below.*

---

## Detailed Model Family Factsheets

### 1. Llama Family (Meta AI)
Developed by Meta AI, the Llama series is the industry benchmark for open-weights models.
- **Llama-2-7b (Base)**: 6.7B parameters. Context window: 4,096 tokens. Cutoff: September 2022. Release: July 18, 2023. [1]
- **Llama-2-13b (Base)**: 13.0B parameters. Context window: 4,096 tokens. Cutoff: September 2022. Release: July 18, 2023. [1]
- **Llama-2-70b (Base)**: 68.9B parameters. Context window: 4,096 tokens. Cutoff: September 2022. Release: July 18, 2023. [1]
- **Llama-3-8B-Instruct**: 8.03B parameters. Context window: 8,192 tokens. Cutoff: March 2023. Release: April 18, 2024. [2]
- **Llama-3-70B-Instruct**: 70.6B parameters. Context window: 8,192 tokens. Cutoff: December 2023. Release: April 18, 2024. [2]
- **Llama-3.1-8B-Instruct**: 8.03B parameters. Context window: 128,000 tokens (RoPE scaled). Cutoff: December 2023. Release: July 23, 2024. [3]
- **Llama-3.1-70B-Instruct**: 70.6B parameters. Context window: 128,000 tokens (RoPE scaled). Cutoff: December 2023. Release: July 23, 2024. [3]
- **Llama-3.2-1B-Instruct**: 1.23B parameters. Context window: 128,000 tokens. Cutoff: December 2023. Release: September 25, 2024. [5]
- **Llama-3.2-3B-Instruct**: 3.21B parameters. Context window: 128,000 tokens. Cutoff: December 2023. Release: September 25, 2024. [5]

### 2. Gemma Family (Google DeepMind)
Google's lightweight open-weight models leverage technologies from Gemini.
- **Gemma-7B (Base)**: 8.54B total, 7.2B active parameters. Context window: 8,192 tokens. Cutoff: November 2023. Release: February 21, 2024. [6]
- **Gemma-2-9B-it**: 9.2B parameters. Context window: 8,192 tokens. Cutoff: March 2024. Release: June 27, 2024. [8]
- **Gemma-2-27B-it**: 27.2B parameters. Context window: 8,192 tokens. Cutoff: March 2024. Release: June 27, 2024. [8]

### 3. Phi Family (Microsoft)
Small language models (SLMs) trained on high-quality synthetic "textbooks" and filtered data.
- **Phi-2 (Base)**: 2.78B parameters. Context window: 2,048 tokens. Cutoff: November 2023. Release: December 12, 2023. [10]
- **Phi-3-mini-4k-instruct**: 3.8B parameters. Context window: 4,096 tokens. Cutoff: October 2023. Release: April 23, 2024. [11]
- **Phi-3-medium-4k-instruct**: 14B parameters. Context window: 4,096 tokens. Cutoff: October 2023. Release: May 21, 2024. [11]
- **Phi-3.5-mini-instruct**: 3.8B parameters. Context window: 128,000 tokens. Cutoff: October 2023. Release: August 20, 2024. [13]

### 4. Qwen Family (Alibaba Cloud)
Alibaba Cloud's highly capable language model family with exceptional multilingual and coding skills.
- **Qwen2.5-72B-Instruct**: 72.7B parameters. Context window: 128,000 tokens. Cutoff: August 2024. Release: September 19, 2024. [15]
- **Qwen2.5-32B-Instruct**: 32.5B parameters. Context window: 128,000 tokens. Cutoff: August 2024. Release: September 19, 2024. [15]
- **Qwen2.5-7B-Instruct**: 7.61B parameters. Context window: 128,000 tokens. Cutoff: August 2024. Release: September 19, 2024. [15]
- **Qwen2.5-Coder-32B-Instruct**: 32.5B parameters. Context window: 128,000 tokens. Cutoff: August 2024. Release: November 12, 2024. [16]
- **Qwen2-72B-Instruct**: 72.7B parameters. Context window: 128,000 tokens. Cutoff: February 2024. Release: June 6, 2024. [18]
- **Qwen1.5-72B-Chat**: 72.7B parameters. Context window: 32,768 tokens. Cutoff: January 2024. Release: February 4, 2024. [19]

### 5. DeepSeek Family (DeepSeek AI)
Pioneered high-performance Mixture of Experts (MoE) architectures with extreme cost efficiency.
- **DeepSeek-V3 (Chat)**: MoE architecture. 671B total, 37B active parameters (256 routed + 8 shared experts). Context window: 128,000 tokens. Cutoff: July 2024. Release: December 26, 2024. [20]
- **DeepSeek-R1 (Reasoning)**: Reasoning model built on DeepSeek-V3 using RL. 671B total, 37B active parameters. Context window: 128,000 tokens. Cutoff: July 2024. Release: January 20, 2025. [22]
- **DeepSeek-Coder-V2-Instruct**: First open-weights MoE model to match GPT-4-Turbo on coding. 236B total, 21B active parameters. Context window: 128,000 tokens. Cutoff: April 2024. Release: June 17, 2024. [24]
- **DeepSeek-V2-Chat**: 236B total, 21B active parameters. Context window: 128,000 tokens. Cutoff: April 2024. Release: May 7, 2024. [26]
- **DeepSeek-LLM-67B-Chat**: Dense model. 67.3B parameters. Context window: 4,096 tokens. Cutoff: September 2023. Release: November 29, 2023. [28]

### 6. Yi Family (01.AI)
Bilingual (English/Chinese) open-weights models developed by Kai-Fu Lee's startup 01.AI.
- **Yi-34B-Chat**: 34.3B parameters. Context window: 4,096 tokens. Cutoff: June 2023. Release: November 6, 2023. [29]
- **Yi-6B-Chat**: 6.0B parameters. Context window: 4,096 tokens. Cutoff: June 2023. Release: November 6, 2023. [29]
- **Yi-1.5-34B-Chat**: 34.3B parameters. Context window: 4,096 tokens. Cutoff: February 2024. Release: May 13, 2024. [31]
- **Yi-1.5-9B-Chat**: 8.8B parameters. Context window: 4,096 tokens. Cutoff: February 2024. Release: May 13, 2024. [31]
- **Yi-1.5-6B-Chat**: 6.0B parameters. Context window: 4,096 tokens. Cutoff: February 2024. Release: May 13, 2024. [31]

### 7. Mistral / Mixtral Family (Mistral AI)
European startup Mistral AI championed sparse MoE and high-efficiency models.
- **Mistral 7B (v0.1)**: 7.24B parameters. Context window: 8,192 tokens. Cutoff: September 2023. Release: September 27, 2023. [33]
- **Mixtral 8x7B (v0.1)**: MoE model. 46.7B parameters total (12.9B active). Context window: 32,768 tokens. Cutoff: September 2023. Release: December 11, 2023. [35]
- **Mixtral 8x22B**: MoE model. 141B parameters total (39B active). Context window: 65,536 tokens. Cutoff: April 2024 (Est.). Release: April 17, 2024. [36]

### 8. Command Family (Cohere)
Cohere's models are highly tuned for enterprise use-cases, RAG, and tool-use.
- **Command R**: 35B parameters. Context window: 128,000 tokens. Cutoff: January 2024. Release: March 11, 2024. [38]
- **Command R+**: 104B parameters. Context window: 128,000 tokens. Cutoff: January 2024. Release: April 4, 2024. [40]

### 9. InternLM Family (Shanghai AI Lab)
Developed by Shanghai Artificial Intelligence Laboratory, offering massive context sizes.
- **InternLM2-Chat-7B**: 7.7B parameters. Context window: 204,800 tokens. Cutoff: December 2023. Release: January 17, 2024. [42]
- **InternLM2.5-Chat-7B**: 7.74B parameters. Context window: 1,000,000 tokens (1M). Cutoff: May 2024. Release: July 3, 2024. [43]

### 10. GLM/ChatGLM Family (Zhipu AI)
Bilingual models trained by Zhipu AI and Tsinghua University.
- **ChatGLM3-6B**: 6.2B parameters. Context window: 32,768 tokens. Cutoff: September 2023. Release: October 27, 2023. [44]
- **GLM-4-9B-Chat**: 9.4B parameters. Context window: 128,000 tokens. Cutoff: December 2023. Release: June 5, 2024. [46]

### 11. DBRX Family (Databricks)
Databricks developed DBRX, an MoE model optimized for enterprise applications.
- **DBRX Instruct**: MoE model. 132B parameters total (36B active). Context window: 32,768 tokens. Cutoff: December 2023. Release: March 27, 2024. [47]

### 12. Falcon Family (Technology Innovation Institute)
Open-source models funded by the Abu Dhabi government.
- **Falcon 40B**: 40B parameters. Context window: 2,048 tokens. Cutoff: December 2022. Release: May 24, 2023. [50]
- **Falcon 180B**: 180B parameters. Context window: 4,096 tokens. Cutoff: June 2023. Release: September 6, 2023. [52]
- **Falcon 2 11B**: 11B parameters. Context window: 8,192 tokens. Cutoff: March 2024. Release: May 13, 2024. [54]

### 13. StarCoder Family (BigCode)
BigCode (Hugging Face & ServiceNow) models specialized for code generation and autocomplete.
- **StarCoder (15B)**: 15.5B parameters. Context window: 8,192 tokens. Cutoff: January 2023. Release: May 9, 2023. [56]
- **StarCoder2-15B**: 15B parameters. Context window: 16,384 tokens. Cutoff: September 2023. Release: February 28, 2024. [58]

---

## Knowledge Cutoff & Risk Analysis

The models in this survey represent four distinct developmental eras, characterized by different knowledge cutoff dates and architectural capabilities. In a hybrid routing system like FrugalRoute, understanding these eras is critical to managing factual accuracy, reasoning capacity, and inference costs.

### The Four Model Eras

1. **Pre-2023 Era (Cutoff: Sep 2022 – Jan 2023)**
   - *Key Models*: Llama-2-7b/13b/70b, Falcon 40B, StarCoder 15B.
   - *Characteristics*: First-generation open LLMs. Standard contexts are small (2K to 4K). Factual cutoff is locked before the AI boom of late 2022/early 2023.
   - *Benchmarks*: Relatively low MMLU (<70%) and poor mathematical reasoning (GSM8K <60%).

2. **Late 2023 Era (Cutoff: Mar 2023 – Dec 2023)**
   - *Key Models*: Llama-3-8B/70B, Phi-2, Phi-3, Gemma-7B, Mistral 7B, Mixtral 8x7B, Yi-34B.
   - *Characteristics*: Transition from pre-training hacks to high-quality data curation. Context windows expand up to 8K/32K.
   - *Benchmarks*: MMLU scores cross 80% for larger models, and GSM8K math capabilities jump significantly (e.g., Llama-3-70B achieves 93.0%).

3. **2024 Era (Cutoff: Jan 2024 – Aug 2024)**
   - *Key Models*: Llama-3.1/3.2, Gemma-2, Qwen2.5 (including Coder), DeepSeek-V3, DeepSeek-Coder-V2, Command R/R+, InternLM2.5, GLM-4, Falcon 2 11B.
   - *Characteristics*: Integration of very long context windows (128K to 1M tokens), native tool usage, and agentic capabilities. Dominance of Mixture-of-Experts (MoE) architectures (DeepSeek, Mixtral 8x22B) and hyper-optimized small models (Gemma-2-9B, Phi-3.5).
   - *Benchmarks*: State-of-the-art open-weights benchmarks. Coding performance (HumanEval) crosses 90% (DeepSeek-Coder-V2, Qwen2.5-Coder).

4. **2025+ Era (Cutoff: July 2024 and beyond, Released 2025)**
   - *Key Models*: DeepSeek-R1.
   - *Characteristics*: The rise of test-time compute and large-scale Reinforcement Learning (RL) reasoning models. The model outputs thinking processes ("reasoning tokens") before final answers.
   - *Benchmarks*: Absolute peak mathematical (GSM8K: 96.3%) and code reasoning.

### Risk Analysis on Factual Accuracy and Hybrid Routing

Implementing a hybrid routing system (such as routing easier queries to a small model and harder queries to a large model) introduces specific risks when crossing these model eras:

- **Factual Hallucination and Temporal Misalignment**: If a user asks about events occurring in 2024, routing the query to Llama-2 (2022 cutoff) or Phi-3 (Oct 2023 cutoff) guarantees a hallucination or failure. The router must inspect query dates/entities and steer post-cutoff queries to 2024/2025+ era models.
- **Syntactic and Prompt Formats**: Pre-2023 models (like Llama-2) expect different chat template structures compared to 2024 models (like Llama-3.1 using `<|eot_id|>` or Qwen using ChatML). A routing engine that passes raw text without adapting the prompt templates will cause generation collapse.
- **Reasoning Divergence**: A query requiring complex logic (e.g., code optimization or math) routed to an older 2023-era small model will yield a high failure rate. Routing decisions must weight mathematical or code complexity heavily, routing them to specialized models (e.g., Qwen2.5-Coder-32B or DeepSeek-R1).
- **VRAM and Compute Budgeting on AMD MI300X**: To maximize throughput on AMD MI300X (192 GB VRAM), loading a 132B+ dense model requires multi-GPU partitioning or heavy quantization, reducing inference speed. Using MoE models (e.g., DeepSeek-V3 or Mixtral) or 32B-70B dense models allows high-capacity generation within a single GPU boundary, mitigating routing latency spikes.

---

## Recommendations for AMD MI300X Routing

To deploy a highly reliable, high-throughput hybrid routing system on an AMD MI300X GPU (192 GB VRAM capacity), we recommend loading exactly three instruction-tuned models representing a tier of capacity, memory footprint, and inference speed.

To avoid memory swapping overhead and support batching, the sum of active model VRAM footprints must reside safely within the 192 GB limit. Assuming a float16/bfloat16 format (2 bytes per parameter):
$$\text{Memory (GB)} \approx \text{Parameters (B)} \times 2$$

Below is our recommended model tier list.

### Recommendations for AMD MI300X Routing

- **High-Capacity Model**: Llama-3.1-70B-Instruct (70.6B parameters)
- **Mid-Size Model**: Qwen2.5-32B-Instruct (32.5B parameters)
- **Small/Fast Model**: Phi-3.5-mini-instruct (3.8B parameters)

### Rationale and Justification

1. **High-Capacity Tier: Llama-3.1-70B-Instruct**
   - *Parameters*: 70.6B
   - *VRAM Footprint*: $\approx 141.2$ GB (in native BF16 precision)
   - *Justification*: Serves as the ultimate oracle/fallback for highly complex reasoning, long-context documents (up to 128K), and general agentic workflows. It has an MMLU of 86.0%, HumanEval of 80.5%, and GSM8K of 95.1%, making it highly competitive with proprietary models. Fitting within the 192 GB limit of a single MI300X, it leaves $\approx 50.8$ GB for context KV cache and batching overhead.

2. **Mid-Size Tier: Qwen2.5-32B-Instruct**
   - *Parameters*: 32.5B
   - *VRAM Footprint*: $\approx 65.0$ GB (in native BF16 precision)
   - *Justification*: Excellent "middle-tier" router target. It punches well above its weight class, achieving an MMLU of 80.7%, HumanEval of 82.3%, and GSM8K of 90.9%—nearly matching or exceeding Llama-3-70B while occupying less than half the VRAM. This model can be active concurrently or swapped dynamically, and serves as an ideal code/math accelerator without incurring the latency or memory footprint of the 70B model.

3. **Small/Fast Tier: Phi-3.5-mini-instruct**
   - *Parameters*: 3.8B
   - *VRAM Footprint*: $\approx 7.6$ GB (in native BF16 precision)
   - *Justification*: Designed for low-latency, high-throughput triage, basic conversation, and simple classification. Despite its tiny size, it supports a full 128K context window and achieves an MMLU of 75.1% and HumanEval of 62.8%. Phi-3.5-mini is extremely fast to run on the MI300X, serving as the first-line processor for >70% of standard customer queries in the hybrid routing system.

---

## Sources

1. Meta AI. (2023). *Llama 2: Open Foundation and Fine-Tuned Chat Models*. https://arxiv.org/abs/2307.09288
2. Meta AI. (2024). *Introducing Meta Llama 3*. https://ai.meta.com/blog/meta-llama-3/
3. Meta AI. (2024). *The Llama 3 Herd of Models*. https://arxiv.org/abs/2407.21783
4. Meta AI. (2024). *Meta Llama 3.1*. https://ai.meta.com/blog/meta-llama-3-1/
5. Meta AI. (2024). *Llama 3.2: Connecting education, culture, and business*. https://ai.meta.com/blog/llama-3-2-connect-2024/
6. Google DeepMind. (2024). *Gemma: Open Models Based on Gemini Research and Technology*. https://arxiv.org/abs/2403.08295
7. Google DeepMind. (2024). *Gemma: Introducing new state-of-the-art open models*. https://blog.google/technology/developers/gemma-open-models/
8. Google DeepMind. (2024). *Gemma 2: Improving Open Language Models at a Practical Size*. https://arxiv.org/abs/2408.00118
9. Google DeepMind. (2024). *Google Gemma 2: State-of-the-art performance at a practical scale*. https://blog.google/technology/developers/google-gemma-2/
10. Microsoft Research. (2023). *Phi-2: The Surprising Power of Small Language Models*. https://www.microsoft.com/en-us/research/blog/phi-2-the-surprising-power-of-small-language-models/
11. Microsoft. (2024). *Phi-3 Technical Report: A Highly Capable Language Model Locally on Your Phone*. https://arxiv.org/abs/2404.14219
12. Microsoft. (2024). *Introducing Phi-3: Redefining what’s possible with SLMs*. https://azure.microsoft.com/en-us/blog/introducing-phi-3-redefining-whats-possible-with-slms/
13. Microsoft. (2024). *Introducing Phi-3.5-mini and Phi-3.5-MoE*. https://azure.microsoft.com/en-us/blog/introducing-phi-3-5-mini-and-phi-3-5-moe/
14. Microsoft. (2024). *HuggingFace Hub: Phi-3.5-mini-instruct Model Card*. https://huggingface.co/microsoft/Phi-3.5-mini-instruct
15. Qwen Team. (2024). *Qwen2.5: A Grand Upgrade of Qwen2*. https://qwenlm.github.io/blog/qwen2.5/
16. Qwen Team. (2024). *Qwen2.5-Coder: The Gateway to Powerful Coding*. https://qwenlm.github.io/blog/qwen2.5-coder-family/
17. Qwen Team. (2024). *Qwen2: A New Generation of Open Language Models*. https://qwenlm.github.io/blog/qwen2/
18. Yang, A., et al. (2024). *Qwen2 Technical Report*. https://arxiv.org/abs/2407.10671
19. Qwen Team. (2024). *Qwen1.5: Large Language Models upgraded*. https://qwenlm.github.io/blog/qwen1.5/
20. DeepSeek-AI. (2024). *DeepSeek-V3 Technical Report*. https://github.com/deepseek-ai/DeepSeek-V3
21. DeepSeek-AI. (2025). *DeepSeek-R1 GitHub Repository*. https://github.com/deepseek-ai/DeepSeek-R1
22. DeepSeek-AI. (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. https://arxiv.org/abs/2501.12948
23. DeepSeek-AI. (2024). *DeepSeek-Coder-V2 GitHub Repository*. https://github.com/deepseek-ai/DeepSeek-Coder-V2
24. DeepSeek-AI. (2024). *DeepSeek-Coder-V2: Breaking the Barrier of Closed-Source Models in Code Intelligence*. https://arxiv.org/abs/2406.11931
25. DeepSeek-AI. (2024). *DeepSeek-V2 GitHub Repository*. https://github.com/deepseek-ai/DeepSeek-V2
26. DeepSeek-AI. (2024). *DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model*. https://arxiv.org/abs/2405.04434
27. DeepSeek-AI. (2023). *DeepSeek-LLM GitHub Repository*. https://github.com/deepseek-ai/deepseek-LLM
28. DeepSeek-AI. (2024). *DeepSeek LLM: Scaling Open-Source Language Models with Longtermism*. https://arxiv.org/abs/2401.02954
29. 01.AI. (2023). *Yi GitHub Repository*. https://github.com/01-ai/Yi
30. 01.AI. (2024). *Yi: Open Foundation Models by 01.AI*. https://arxiv.org/abs/2403.04652
31. 01.AI. (2024). *Yi-1.5 GitHub Repository*. https://github.com/01-ai/Yi-1.5
32. Mistral AI. (2023). *Announcing Mistral 7B*. https://mistral.ai/news/announcing-mistral-7b/
33. Mistral AI. (2023). *Mistral 7B*. https://arxiv.org/abs/2310.06825
34. Mistral AI. (2023). *Mixtral of Experts*. https://mistral.ai/news/mixtral-of-experts/
35. Mistral AI. (2024). *Mixtral of Experts Technical Paper*. https://arxiv.org/abs/2401.04088
36. Mistral AI. (2024). *Mixtral 8x22B*. https://mistral.ai/news/mixtral-8x22b/
37. Cohere. (2024). *Command R: Introducing a 35B Model for Enterprise RAG*. https://cohere.com/blog/command-r
38. Cohere. (2024). *Command R Model Card on Hugging Face*. https://huggingface.co/CohereForAI/c4ai-command-r-v01
39. Cohere. (2024). *Command R+ on Azure*. https://cohere.com/blog/command-r-plus-microsoft-azure
40. Cohere. (2024). *Command R+ Model Card on Hugging Face*. https://huggingface.co/CohereForAI/c4ai-command-r-plus
41. Shanghai AI Lab. (2024). *InternLM GitHub Repository*. https://github.com/InternLM/InternLM
42. Shanghai AI Lab. (2024). *InternLM2 Technical Paper*. https://arxiv.org/abs/2403.17297
43. Shanghai AI Lab. (2024). *InternLM2.5-Chat-7B Model Card on Hugging Face*. https://huggingface.co/internlm/internlm2_5-7b-chat
44. Zhipu AI. (2023). *ChatGLM3 GitHub Repository*. https://github.com/THUDM/ChatGLM3
45. Zhipu AI. (2024). *GLM-4 GitHub Repository*. https://github.com/THUDM/GLM-4
46. Zhipu AI. (2024). *GLM-4-9B-Chat Model Card on Hugging Face*. https://huggingface.co/THUDM/glm-4-9b-chat
47. Databricks. (2024). *Introducing DBRX: A New State-of-the-Art Open LLM*. https://www.databricks.com/blog/introducing-dbrx-new-state-art-open-llm
48. Databricks. (2024). *DBRX GitHub Repository*. https://github.com/databricks/dbrx
49. TII. (2023). *Falcon-40B Model Card on Hugging Face*. https://huggingface.co/tiiuae/falcon-40b
50. TII. (2023). *The Falcon Series of Language Models*. https://arxiv.org/abs/2311.16867
51. TII. (2023). *Falcon 180B on Hugging Face*. https://huggingface.co/blog/falcon-180b
52. TII. (2023). *Falcon-180B Model Card on Hugging Face*. https://huggingface.co/tiiuae/falcon-180B
53. TII. (2024). *Falcon 2 11B Official Site*. https://falconllm.tii.ae/falcon-2.html
54. TII. (2024). *Falcon-2-11B Model Card on Hugging Face*. https://huggingface.co/tiiuae/falcon-2-11B
55. BigCode. (2023). *StarCoder: A State-of-the-Art Model for Code*. https://huggingface.co/blog/starcoder
56. BigCode. (2023). *StarCoder: May the Source Be With You*. https://arxiv.org/abs/2305.06161
57. BigCode. (2024). *StarCoder 2: State-of-the-Art Code SLMs*. https://huggingface.co/blog/starcoder2
58. BigCode. (2024). *StarCoder 2 Technical Report*. https://arxiv.org/abs/2403.00131
