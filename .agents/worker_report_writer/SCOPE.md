# Scope: Report Compilation and Verification

## Architecture
- Input: 3 handoff files from research subagents
- Output: `eval/report.md` (Markdown report) and `eval/verify_report.py` (Verification script)
- Verification: Running `python eval/verify_report.py` and confirming success

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Report Compile | Create `eval/report.md` compiling 47 model variants | None | DONE |
| 2 | Verification Script | Create `eval/verify_report.py` to parse and check report | M1 | DONE |
| 3 | Execution & Gate | Run script via run_command, resolve issues | M2 | DONE |
| 4 | Final Handoff | Write handoff report to `.agents/worker_report_writer/handoff.md` | M3 | DONE |

## Interface Contracts
- `eval/report.md`: must follow the exact layout requested by the user, including Master Comparison Table and Factsheets.
- `eval/verify_report.py`: must parse `eval/report.md` and check:
  - Table has >= 30 distinct model variants.
  - At least 8 distinct model families are covered.
  - At least 80% of model cutoffs are documented.
  - Exactly 3 recommendations are present and fit VRAM (<= 70B parameters).
  - Citations are linked.
