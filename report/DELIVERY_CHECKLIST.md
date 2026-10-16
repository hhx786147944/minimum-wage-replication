# Final Acceptance Checklist

> Status legend: ✅ completed and verified · ⚠️ completed with a documented caveat ·
> ❌ not completed. Every item lists the evidence.

## 1. Reproduction targets

| Item | Status | Evidence |
|---|---|---|
| Table 2 (means by state) reproduced | ✅ | `outputs/tables/table2_means_by_state.csv`; values match the paper (report §5) |
| Table 3 (average employment / DID) reproduced | ✅ | `outputs/tables/table3_avg_employment.csv`; rows 1–2, 4–5 exact, row 3 mean exact, SE ≈ (4%) — report §6, §9 |
| Table 4 (reduced-form regressions) reproduced | ✅ | `outputs/tables/table4_reduced_form.csv`; models (i)–(iv) exact, (v) ≈ (0.6%) — report §7, §9 |
| Figure 1 (starting-wage distribution) reproduced | ✅ | `outputs/figures/figure1_starting_wage_distribution.png` — report §8 |

## 2. Extension analysis

| Item | Status | Evidence |
|---|---|---|
| ≥ 1 independent extension completed | ✅ | Price pass-through — `outputs/tables/extension_price_did_means.csv`, `extension_price_did_regressions.csv`; `code/extension.py`; report §10 |

## 3. Results from real runs (no fabrication)

| Item | Status | Evidence |
|---|---|---|
| All numbers come from the code reading `public.csv` | ✅ | Single entry point `python code/run_all.py`; clean re-run regenerated all outputs identically |
| No unverified result labeled as verified | ✅ | Two residual discrepancies documented, not forced — report §9, README §11, AI disclosure §4 |

## 4. Documentation

| Item | Status | Evidence |
|---|---|---|
| Report complete (≥ 10 sections) | ✅ | `report/report.md` — 13 sections |
| Comparison vs. paper + discrepancy explanation | ✅ | report §9 |
| Limitations / conclusion | ✅ | report §12 |
| README sufficient (env, deps, data prep, run steps) | ✅ | `README.md` §6, §8, §9 |
| AI-use disclosure (standalone, stage-by-stage) | ✅ | `AI_USE_DISCLOSURE.md` (root) |
| Report PDF at repository root | ✅ | `report.pdf` (rendered from `report/report.md` via `scripts/make_report_pdf.py`) |
| All documentation in English | ✅ | README, DATA_CHECK.md, report/*.md, code comments |

## 5. Code and dependencies

| Item | Status | Evidence |
|---|---|---|
| Code complete and runnable | ✅ | `code/*.py`; single entry point `code/run_all.py` runs end-to-end with no manual steps |
| No hardcoded personal/absolute paths | ✅ | paths derived from project root in `code/config.py` |
| Dependencies listed and installed | ✅ | `requirements.txt`; pandas 3.0.6, numpy 2.5.4, matplotlib 3.11.2, statsmodels 0.15.0, scipy 1.18.1, fpdf2 2.8.9 (Python 3.15.0) |

## 6. Data compliance

| Item | Status | Evidence |
|---|---|---|
| Raw course data not committed | ✅ | `.gitignore` excludes raw and processed data files; only README placeholders under `data/` and aggregate result CSVs under `outputs/tables/` are committed |
| Raw data preserved locally, not overwritten | ✅ | `data/raw/public.csv` (SHA-256 `f29f3a8…`) untouched |
| No restricted data or download link published | ✅ | README §6 documents location/access without a link |

## 7. Git history and remote

| Item | Status | Evidence |
|---|---|---|
| Git history authentic (4-phase commits) | ✅ | The original phase commits are preserved; later commits include submission-layout updates |
| GitHub accessible and clean | ✅ | After synchronization, `origin/main` matches the local `main` branch |

## 8. Repository structure compliance (per the course example)

| Required path | Status | Evidence |
|---|---|---|
| `README.md` (root) | ✅ | Project overview + reproduction guide |
| `report.pdf` (root) | ✅ | Final report PDF |
| `AI_USE_DISCLOSURE.md` (root) | ✅ | Stage-by-stage AI-use disclosure |
| `data/raw/` | ✅ | `README.md` placeholder committed; `public.csv` kept local |
| `data/processed/` | ✅ | `README.md` placeholder committed; `analysis_ready.csv` written by `run_all.py` (local) |
| `code/run_all.py` (single entry point) | ✅ | Generates all tables and figures |
| `code/` other files | ✅ | `config.py`, `load_data.py`, `analysis.py`, `tables.py`, `figures.py`, `extension.py` |
| `outputs/tables/` | ✅ | Tables 2-4 + extension CSVs (committed) + `README.md` |
| `outputs/figures/` | ✅ | Figure 1 (committed) + `README.md` |
| `skills/SKILL.md` | ✅ | Reusable method for the main tables and figures |

> Repository name must be `Name_StudentID` — to be set once the user supplies their
> name and student ID (renamed on GitHub).

## 9. Caves (flagged, not hidden)

| Item | Status | Note |
|---|---|---|
| Table 4 model (v) | ⚠️ | ≈0.6% residual vs. paper — documented, not forced (report §9) |
| Table 3 row 3 SE | ⚠️ | ≈4% residual vs. paper — documented, not forced (report §9) |

> The generated CSV tables are committed via a `!outputs/tables/*.csv` exception in
> `.gitignore` (aggregate results, not raw course data). The raw `public.csv` and the
> derived `data/processed/analysis_ready.csv` stay excluded under `data/*` + `*.csv`.

## 10. Final acceptance

- [x] Tables 2–4 and Figure 1 reproduced from the course data by the code.
- [x] One extension analysis (price pass-through) completed and written up.
- [x] All results generated by real runs; residual discrepancies honestly documented.
- [x] Report, README, AI disclosure, and this checklist complete and in English.
- [x] Data compliance passed: raw data kept local and never committed/published.
- [x] Latest project structure and deliverables committed and pushed; raw course data remains excluded.
