# Project: FrugalRoute LLM Landscape Survey

## Architecture
- This project compiles and synthesizes open-weight LLM data to support routing decisions on AMD MI300X hardware.
- Information flows from web research (Explorers) -> Consolidated synthesis -> Report output at `eval/report.md` -> Scripted validation at `eval/verify_report.py`.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Planning & Setup | Establish plan.md, BRIEFING.md, progress.md, PROJECT.md | None | DONE |
| 2 | Parallel Research | Web search for 30+ models and 8+ families (MMLU, HumanEval, GSM8K, cutoffs) | Milestone 1 | DONE |
| 3 | Consolidated Report | Consolidate findings and draft `eval/report.md` | Milestone 2 | DONE |
| 4 | Verification | Implement `eval/verify_report.py` and run validations | Milestone 3 | DONE |

## Code Layout
- `.agents/` - Coordination metadata and progress logs.
- `eval/` - Final report and verification script.
- `eval/report.md` - Final compiled survey report.
- `eval/verify_report.py` - Script verifying completeness of report.
