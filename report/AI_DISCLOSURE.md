# AI-Use Disclosure

> This file records, factually, how AI assistance was used in this project, how the
> outputs were verified, what errors were found and how they were corrected or
> rejected, and which decisions were confirmed by the human. It records only events that
> actually occurred.

## 1. Tools used

| Tool | Role in this project |
|---|---|
| Claude Code (Anthropic) | Wrote the Python analysis pipeline (`src/*.py`), drafted the documentation (`README.md`, `DATA_CHECK.md`, this report), and performed result validation. |
| Python 3.15 (pandas, numpy, matplotlib, statsmodels, scipy) | Ran the actual data processing, estimation, and figure/table generation. |
| git / GitHub | Version control and remote publication of the code and documentation. |

The AI did **not** run any model to "predict" results: all numbers come from the Python
pipeline reading `public.csv`.

## 2. How the work was verified

- **Deterministic single entry point.** The entire analysis is reproduced by
  `python src/main.py`, which regenerates all tables and the figure from the raw data.
  There is no hand-entered number in any table or figure.
- **Item-by-item comparison against the paper.** Key estimates were compared with the
  values printed in Card & Krueger (1994) and summarized in the README (§11) and the
  report (§9).
- **Clean re-run.** `outputs/` was deleted and the pipeline re-run; all seven output
  files were regenerated identically, confirming reproducibility.
- **Data-compliance check.** Confirmed the raw data (`public.csv`, SHA-256 `f29f3a8…`)
  is present locally but not tracked by git (`git ls-files` shows no `data/` or `.csv`),
  and that the remote repository is reachable and matches the local commits.

## 3. Errors found and how they were corrected

1. **Table 4 sample size was 351 instead of 357.** The initial sample filter required a
   wave-2 starting wage for every store, which wrongly dropped the 6 permanently closed
   stores (STATUS2 = 3: wave-2 employment = 0, but no wave-2 wage). **Fix:** waive the
   wave-2 wage requirement only for permanent closures. Result: n = 357 exactly, and
   Table 4 models (i)–(iv) then match the paper exactly.

2. **Table 3 row-3 standard error was 1.80 instead of 1.36.** The initial code treated
   the wave-1 and wave-2 cross-sectional means as independent, overstating the SE of
   their difference. **Fix:** use the covariance formula for the difference of two
   overlapping-sample means. Result: SE = 1.31, close to the paper's 1.36.

## 4. Errors / discrepancies that were rejected or documented rather than "fixed"

The following were deliberately **not** forced to match the paper:

- **Table 4 model (v)** differs by ≈0.6% (coefficient 11.98 vs. 11.91; SE 7.42 vs.
  7.39). A search over region-dummy combinations confirmed the footnote's "two NJ + two
  PA regions" maps to `CENTRALJ`, `SOUTHJ`, `PA1`, `PA2` (North NJ omitted); the small
  residual was left as-is and attributed to a reference-category choice or a minor
  data-version difference.
- **Table 3 row-3 SE** is ≈4% below the paper's (1.31 vs. 1.36). The methodologically
  correct overlapping-sample formula was used, and the gap was documented rather than
  tuned away.

No code, table, figure, or git history was fabricated or altered to make the checklist
appear "all passed."

## 5. Decisions confirmed by the human

- **Extension topic.** The price pass-through extension was chosen by the human from a
  set of candidate extensions.
- **Documentation language.** The human required all project documents to be written in
  English.
- **Commit/push gating.** Git commits and pushes are performed only after explicit human
  confirmation, including the final Phase 4 commit.

## 6. Scope of AI responsibility

The AI wrote the code and text and performed the validation described above. The human
owns the project: they confirmed the design decisions, reviewed the outputs, and retain
responsibility for the final submission.
