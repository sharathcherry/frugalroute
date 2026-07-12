# Scope: Report Compilation and Verification

## Architecture
- Input: 3 handoff files containing details on 47 models across 13 families.
- Output 1: `eval/report.md` containing the compiled survey report.
- Output 2: `eval/verify_report.py` containing a script to programmatically verify report contents.
- Execution: Run verification script via command line and ensure it exits with code 0.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Report Compilation | Write `eval/report.md` according to the requested structure | none | PLANNED |
| 2 | Verification Script | Write `eval/verify_report.py` with the 5 checks | M1 | PLANNED |
| 3 | Execution & Handoff | Run `python eval/verify_report.py` and write the final handoff | M2 | PLANNED |

## Interface Contracts
- `eval/report.md` must be a high-quality Markdown file.
- `eval/verify_report.py` must run with `python` and exit with 0 on success.
