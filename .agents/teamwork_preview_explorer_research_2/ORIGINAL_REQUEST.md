## 2026-07-11T06:05:41Z

You are teamwork_preview_explorer_research_2. Your working directory is c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\.agents\teamwork_preview_explorer_research_2.
Your parent is teamwork_preview_orchestrator (b2f15c67-2594-4cb6-be03-f5523b75a567).

Your task is to conduct web research to identify and catalog at least 10-12 model variants from the following families:
1. Qwen (Alibaba)
2. DeepSeek (DeepSeek AI)
3. Yi (01.AI)

For each model variant, you must gather:
- Model Name
- Parameter Size
- Developer/Organization
- Release Date
- Knowledge Cutoff Date (exact or estimated)
- MMLU Score (official)
- HumanEval Score (official)
- GSM8K Score (official)
- Context Window Size
- Official source URLs/citations for all the details above.

Guidelines:
- Only gather official metrics published by the developers (blog posts, model cards, papers, GitHub). Do not use third-party re-evaluations unless the official score is unavailable, and if so, clearly mark it.
- Try to include a wide range of size variants (e.g., Qwen-1.5, Qwen-2, Qwen-2.5, Qwen-2.5-Coder, DeepSeek-V2, DeepSeek-Coder-V2, DeepSeek-V3, DeepSeek-R1, Yi-6B, Yi-34B, Yi-1.5, etc.)
- Save your findings as a structured Markdown file at c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\.agents\teamwork_preview_explorer_research_2\handoff.md.
- When done, call the send_message tool to report completion and provide the absolute path to your handoff.md.
