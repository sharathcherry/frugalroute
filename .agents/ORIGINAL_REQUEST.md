# Original User Request

## 2026-07-11T06:04:31Z

Conduct an exhaustive, data-driven survey of the open-weight Large Language Model (LLM) landscape. The deliverable is a comprehensive Markdown research report comparing all major publicly available open-weights models — their official evaluation metrics, knowledge cutoff dates, and suitability for use as a local routing model in a hybrid LLM system (FrugalRoute). This is for a hackathon evaluation context.

Working directory: c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\eval
Integrity mode: development

Context: This research supports the FrugalRoute project (AMD Developer Hackathon ACT II), a hybrid LLM routing agent that uses a free local model on AMD MI300X hardware and escalates to a paid remote model only when needed. We need to understand which open-weight models offer the best balance of accuracy, reasoning, and up-to-date world knowledge for use as the local router model.

## Requirements

### R1. Exhaustive Model Catalog via Web Research
Search the web to identify and catalog all major publicly available open-weights LLM families and their primary size variants. At minimum, cover these families: Llama (Meta), Qwen (Alibaba), Mistral/Mixtral (Mistral AI), Gemma (Google), Phi (Microsoft), DeepSeek (DeepSeek AI), Command (Cohere), Yi (01.AI), InternLM (Shanghai AI Lab), GLM/ChatGLM (Zhipu AI), DBRX (Databricks), Falcon (TII), StarCoder (BigCode), and any other prominent models currently dominating the LMSYS Chatbot Arena or Hugging Face Open LLM Leaderboard. For each model, record: model name, parameter count, developer/organization, release date, and context window size.

### R2. Official Evaluation Metrics Comparison
For every model identified in R1, search the web to extract the officially published evaluation metrics. Specifically gather: MMLU score (general knowledge/reasoning), HumanEval score (code generation), GSM8K score (math reasoning), and any other prominent benchmarks reported (e.g., MATH, ARC-Challenge, HellaSwag, TruthfulQA, MT-Bench). Use only scores from official technical reports, model cards, or developer blog posts — do not use third-party re-evaluations unless the official score is unavailable, in which case mark it clearly.

### R3. Knowledge Cutoff Analysis (Critical)
For every model, research and document the exact knowledge cutoff date — the latest date of training data. This is critical because models asked general questions about events after their cutoff will hallucinate. Search official technical reports, Hugging Face model cards, developer blogs, GitHub issues, and community forums. If a cutoff is not explicitly confirmed, search for consensus estimates and mark the entry as *(estimated)*. Group models by cutoff era (Pre-2023, Late 2023, 2024, 2025+) and analyze the risk implications for each group.

### R4. Synthesized Report with Recommendations
Produce a single comprehensive Markdown report file containing:
1. A **Master Comparison Table** with columns: Model Name, Parameter Size, Developer, Release Date, Knowledge Cutoff Date, MMLU Score, HumanEval Score, GSM8K Score, Context Window Size.
2. A **Knowledge Gap Analysis** section grouping models by cutoff era and summarizing deployment risks for general-purpose routing.
3. A **Recommendations** section identifying the top 3 models that provide the best balance of high reasoning capability (MMLU), coding ability (HumanEval), math (GSM8K), and the most recent knowledge cutoff — specifically for use as a local routing model on AMD MI300X (192 GB HBM3) hardware, meaning models up to ~70B parameters at FP16 are feasible.
4. A **Sources** section listing every URL consulted.

## Acceptance Criteria

### Completeness
- [ ] The report covers at minimum 30 distinct model variants across at least 8 different model families
- [ ] Every model entry has a value (or explicit "N/A — not reported") for each column in the Master Comparison Table
- [ ] Knowledge cutoff dates are documented for at least 80% of models, with unconfirmed dates marked *(estimated)*

### Accuracy
- [ ] Every metric value in the table is accompanied by a source citation (URL or paper reference)
- [ ] No metric values are fabricated — each is traceable to an official technical report, model card, or developer blog post

### Knowledge Cutoff Analysis
- [ ] Models are grouped into at least 3 cutoff eras with a written risk analysis for each group
- [ ] The analysis specifically addresses the impact on factual/contemporary question answering

### Recommendations
- [ ] Exactly 3 models are recommended with explicit justification referencing metrics and cutoff dates
- [ ] Recommendations account for the AMD MI300X 192 GB memory constraint (models must fit in VRAM)

### Report Quality
- [ ] The final report is a single well-formatted Markdown file saved to the working directory
- [ ] All tables render correctly in standard Markdown viewers
- [ ] A verification script or checklist is included that can independently confirm the report meets the above criteria

## 2026-07-11T06:13:26Z

You are the Victory Auditor.
Your working directory is: c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\.agents\victory_auditor

Your task is to independently audit the LLM survey deliverables and verify that they strictly comply with the user requirements and acceptance criteria.

Please check the following:
1. Verify `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\eval\report.md` exists and is properly structured in Markdown.
2. Confirm that the report catalogs at least 30 distinct model variants across at least 8 families.
3. Check the Master Comparison Table columns for completeness and verify that all metrics have official citations (URL or paper references).
4. Verify that knowledge cutoff dates are documented for at least 80% of the models (with unconfirmed marked as estimated) and grouped into at least 3 eras with risk analysis.
5. Verify exactly 3 models are recommended, with justifications based on metrics and cutoffs, and that their memory footprints fit within the VRAM limit of a single AMD MI300X (192 GB at BF16/FP16).
6. Run the verification script `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\eval\verify_report.py` to confirm that it runs successfully and returns exit code 0.
7. Output your findings and final verdict in `c:\Users\katuk\Claude\Projects\AMD Project\frugalroute\.agents\victory_auditor\handoff.md`.

Once complete, send a message to me (the parent/Sentinel) with your final verdict: either "VICTORY CONFIRMED" or "VICTORY REJECTED", along with a summary of your audit report.
