# AI-Use Disclosure

> How AI assistance was used at each stage of this replication, how the outputs
> were verified, which errors were found and corrected or rejected, and which
> decisions were confirmed by the human. Records only events that actually
> occurred.

## Stage 1 — Project setup and research plan (Phase 1)

- **Claude Code (Anthropic)** drafted the project README (paper citation,
  background, DID design, and hypotheses), `.gitignore`, and `requirements.txt`.
- **Human decision:** all project documents are written in English.

## Stage 2 — Data preparation and validation (Phase 2)

- Claude Code wrote `load_data.py` (loading + structural validation) and
  `DATA_CHECK.md` (dimensions, missing values, the duplicated `SHEET=407`
  record, and wave-2 non-response handling).
- **Human-set compliance rule:** the raw `public.csv` stays local, is never
  committed to GitHub, and no download link is published.

## Stage 3 — Replication code and result validation (Phase 3)

- Claude Code implemented the DID pipeline (`analysis.py`, `tables.py`,
  `figures.py`, `extension.py`) and the single entry point.
- **Errors found and corrected** (factually):
  1. Table 4 sample size was 351 instead of 357 — the wave-2 wage requirement
     wrongly dropped 6 permanently closed stores; fixed by waiving it only for
     permanent closures (n = 357 exact).
  2. Table 3 row-3 standard error was 1.80 instead of 1.36 — the wave-1/wave-2
     means were treated as independent; fixed with the overlapping-sample
     covariance formula (SE = 1.31).
- **Residual discrepancies documented, not forced:** Table 4 model (v) ≈0.6%,
  and Table 3 row-3 SE ≈4%. No code was adjusted to force these numbers.

## Stage 4 — Report and delivery (Phase 4)

- Claude Code drafted `report/report.md` (13 sections) and rendered it to
  `report.pdf`.
- **Human decisions confirmed:** the extension topic (price pass-through), the
  English documentation requirement, and commit/push gating.

## Tools used

| Tool | Role in this project |
|---|---|
| Claude Code (Anthropic) | Wrote the Python pipeline (`code/*.py`), the documentation, and performed result validation. |
| Python 3.15 (pandas, numpy, matplotlib, statsmodels, scipy) | Ran the actual data processing, estimation, and figure/table generation. |
| git / GitHub | Version control and remote publication of the code and documentation. |

The AI did **not** run a model to "predict" results: every number comes from the
Python pipeline reading `public.csv`.

## How the work was verified

- **Deterministic single entry point.** `python code/run_all.py` regenerates all
  tables and the figure from the raw data; no number is hand-entered.
- **Item-by-item comparison against the paper** (README §11, report §9).
- **Clean re-run.** `outputs/` was deleted and the pipeline re-run; all output
  files were regenerated identically.
- **Data-compliance check.** The raw data (SHA-256 `f29f3a8…`) is present
  locally but not tracked by git; the remote repository matches the local
  commits.

## Scope of AI responsibility

Claude Code wrote the code and text and performed the validation described
above. The human owns the project: they confirmed the design decisions, reviewed
the outputs, and retain responsibility for the final submission.
