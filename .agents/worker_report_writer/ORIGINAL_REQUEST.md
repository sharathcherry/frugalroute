# Original User Request

## 2026-07-11T11:38:14Z

Please act as the worker agent to compile the final LLM comparison report and write the verification script.

### Tasks to Perform:
1. Read the three model research handoff files:
   - `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\.agents\teamwork_preview_explorer_research_1\handoff.md` (Llama, Gemma, Phi)
   - `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\.agents\teamwork_preview_explorer_research_2\handoff.md` (Qwen, DeepSeek, Yi)
   - `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\.agents\teamwork_preview_explorer_research_3\handoff.md` (Mistral/Mixtral, Command, InternLM, GLM, DBRX, Falcon, StarCoder)

2. Create the output Markdown report at `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\eval\report.md` containing:
   - Title: "Open-Weight LLM Survey and Comparison Report for FrugalRoute Hybrid Routing"
   - Master Comparison Table with all 47 models. Columns must be exactly:
     - Model Name
     - Parameter Size
     - Developer
     - Release Date
     - Knowledge Cutoff Date
     - MMLU Score (with citation, e.g., 85.3% [1] or linked)
     - HumanEval Score (with citation)
     - GSM8K Score (with citation)
     - Context Window Size
     Use "N/A" for missing or unreleased metrics.
   - Detailed Factsheets for each of the 13 families with specifications and official URLs/citations for each variant.
   - Knowledge Cutoff & Risk Analysis: group models into 4 eras (Pre-2023, Late 2023, 2024, 2025+) and write a risk analysis on factual accuracy and hybrid routing.
   - Recommendations for AMD MI300X Routing: recommend exactly 3 models (1 high-capacity, 1 mid-size, 1 small/fast) that fit the VRAM limit (parameters * 2 bytes/param <= 192 GB; limit parameters to <= 70B). Fully justify the recommendations.
   - Sources: Standard numbered list of official developer links.

3. Write the Python verification script at `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\eval\verify_report.py`.
   The script must programmatically parse `eval/report.md` and verify:
   - The file is not empty and has a table with >= 30 distinct model variants.
   - At least 8 distinct model families are covered.
   - At least 80% of model cutoffs are documented (i.e. not empty or "N/A" in cutoff column).
   - Exactly 3 recommendations are present and each recommended model fits VRAM (<=70B parameters).
   - Citations/sources are linked.
   - Print a summary of checks and exit with 0 if all pass, 1 if any fail.

4. Run `python eval/verify_report.py` using run_command to confirm everything passes.

5. When complete, write your handoff report to `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\.agents\worker_report_writer\handoff.md` and send a message back to the parent conversation (conversation ID: 32f0b253-ca47-4f79-bf93-6d35804be464) indicating that the task is complete.

MANDATORY INTEGRITY WARNING: DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
