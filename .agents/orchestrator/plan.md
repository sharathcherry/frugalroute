# Execution Plan - LLM Landscape Survey and Comparison Report

This plan coordinates the research, compilation, and validation of the open-weight LLM survey report to support the FrugalRoute hybrid routing agent on AMD MI300X hardware.

## Milestones and Objectives

### Milestone 1: Planning, Setup & Project Framing
- Create project files: `plan.md`, `progress.md`, `PROJECT.md`.
- Establish constraints, checklist, and working directories.
- Status: **In-Progress**

### Milestone 2: Multi-Agent Parallel Web Research
- Spawn multiple read-only **Explorer** agents to search and compile data on the required 8+ LLM families:
  - **Explorer 1 (Llama, Gemma, Phi)**: Focus on Meta, Google, and Microsoft models.
  - **Explorer 2 (Qwen, DeepSeek, Yi)**: Focus on Alibaba, DeepSeek, and 01.AI models.
  - **Explorer 3 (Mistral, Cohere, InternLM, GLM, Falcon, DBRX)**: Focus on Mistral AI, Cohere, Shanghai AI Lab, Zhipu AI, TII, and Databricks.
- Deliverables: Research reports from each explorer containing name, size, developer, release date, context window, official benchmarks (MMLU, HumanEval, GSM8K, etc. with official source URLs), and knowledge cutoff dates.
- Status: **Planned**

### Milestone 3: Aggregation, Synthesis, and Report Writing
- Spawn a **Worker** agent to:
  - Consolidate research findings from Milestone 2.
  - Construct the Master Comparison Table with 30+ model variants.
  - Group models into cutoff eras (Pre-2023, Late 2023, 2024, 2025+) and draft the Knowledge Gap Analysis.
  - Formulate recommendations for local routing on AMD MI300X (VRAM constraint of 192 GB, allowing up to ~70B FP16).
  - Write the final comprehensive research report to `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\eval\report.md`.
- Status: **Planned**

### Milestone 4: Verification and Quality Assurance
- Spawn a **Reviewer** agent to:
  - Double-check all numbers in the report against the sources.
  - Verify formatting and markdown structure.
- Spawn a **Worker/Reviewer** agent to:
  - Create and execute a verification script (e.g. in Python) that parses `eval/report.md` to check:
    1. At least 30 distinct model variants.
    2. At least 8 model families.
    3. No blank/N/A columns for required fields (unless marked N/A explicitly).
    4. Citations are present for all metrics.
    5. Recommendations contain exactly 3 models fitting within VRAM.
- Status: **Planned**

## Verification Criteria
- Final report at `eval/report.md`.
- Verification script at `eval/verify_report.py`.
- Script runs successfully, confirming all acceptance criteria are met.
