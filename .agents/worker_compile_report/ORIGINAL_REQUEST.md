# Original User Request

## Initial Request — 2026-07-11T06:07:29Z

You are tasked to act as the worker agent for compiling the final LLM comparison report and writing the verification script.

### Background & Context
We have conducted research on 47 models across 13 families. The research is recorded in the following handoff files:
1. `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\.agents\teamwork_preview_explorer_research_1\handoff.md` (Llama, Gemma, Phi)
2. `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\.agents\teamwork_preview_explorer_research_2\handoff.md` (Qwen, DeepSeek, Yi)
3. `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\.agents\teamwork_preview_explorer_research_3\handoff.md` (Mistral/Mixtral, Command, InternLM, GLM, DBRX, Falcon, StarCoder)

### Objectives
1. Read the research handoff files.
2. Compile and write a comprehensive, high-quality Markdown report to `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\eval\report.md`.
3. Create a Python verification script `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\eval\verify_report.py`.
4. Run the verification script to confirm everything passes.

### Report Structure for `eval/report.md`
- **Title**: Open-Weight LLM Survey and Comparison Report for FrugalRoute Hybrid Routing
- **Master Comparison Table**: Compile all 47 models. Columns must be:
  - Model Name
  - Parameter Size
  - Developer
  - Release Date
  - Knowledge Cutoff Date
  - MMLU Score (with citation)
  - HumanEval Score (with citation)
  - GSM8K Score (with citation)
  - Context Window Size
  *Note: Make sure every metric score is cited using markdown links or numbered citations (e.g. [1]) referring to the Sources section. Use N/A for missing or unreleased metrics (like MMLU for StarCoder).*
- **Detailed Factsheets**: Descriptions and specifications for each model family, with direct official URLs/citations for each variant.
- **Knowledge Cutoff & Risk Analysis**:
  - Group models into 4 eras: Pre-2023, Late 2023, 2024, 2025+.
  - Write a comprehensive risk analysis for each era, discussing factual accuracy and the impact on contemporary query routing in FrugalRoute.
- **Recommendations for AMD MI300X Routing**:
  - Recommend exactly 3 models:
    - 1. High-capacity model (e.g. Llama-3.1-70B-Instruct)
    - 2. Mid-size model (e.g. Qwen2.5-32B-Instruct or Qwen2.5-Coder-32B-Instruct)
    - 3. Small/fast model (e.g. Qwen2.5-7B-Instruct or Gemma-2-9B-it)
  - Explicitly justify each recommendation based on benchmarks and cutoff dates.
  - Explain how they fit the VRAM memory constraint of AMD MI300X (192 GB HBM3). (VRAM formula: parameters * 2 bytes/param at FP16/BF16. For example, 70B takes ~140 GB, which fits within 192 GB; 32B takes ~65 GB, etc. Exclude models that exceed 192 GB like Mixtral 8x22B or Falcon 180B).
- **Sources**: Standard numbered list of official developer links.

### Verification Script `eval/verify_report.py`
Write a robust script that programmatically reads `eval/report.md` and verifies:
- The file is not empty and contains the comparison table with >=30 distinct model variants.
- At least 8 distinct model families are covered.
- At least 80% of model cutoffs are documented.
- Exactly 3 recommendations are present and fit VRAM (<=70B parameters).
- Citations/sources are linked.
Print a summary of checks and exit with 0 if all pass, 1 if any fail.

### Execution
Run the verification script `python eval/verify_report.py` using run_command to verify it passes.
When complete, write your handoff report to `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\.agents\worker_compile_report\handoff.md` summarizing what you did, and send a message back to parent.
