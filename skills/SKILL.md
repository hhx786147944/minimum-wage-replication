# Skill: DID Replication of Card & Krueger (1994)

> Reusable method for generating this project's main tables (Tables 2-4) and
> Figure 1 from the fast-food survey data.

## What this skill does

Reproduces the difference-in-differences (DID) estimates of the minimum-wage
effect on fast-food employment (New Jersey vs. eastern Pennsylvania, waves 1-2),
and renders the paper's key tables and the starting-wage distribution figure.

## Inputs

- `data/raw/public.csv` — 410 stores × 46 columns (course Package 01).

## Steps

1. **Load and validate** (`code/load_data.py`): read `public.csv`, assert the
   expected shape (410 × 46) and required columns.
2. **Derive variables** (`code/analysis.py`):
   - FTE employment = full-time (incl. managers) + 0.5 × part-time, per wave.
   - Wave-2 employment = 0 for permanently closed stores (`STATUS2 = 3`),
     missing for temporary closures.
   - GAP = (5.05 − WAGE_ST) / WAGE_ST for NJ stores with WAGE_ST < 5.05, else 0.
   - Region dummies: `CENTRALJ`, `SOUTHJ`, `PA1`, `PA2` (North NJ is the
     reference category).
3. **Table 2** (`code/tables.py`): means by state with Welch t-tests of the
   NJ − PA difference.
4. **Table 3** (`code/tables.py`): average employment before/after and the DID;
   the "all available" change uses the covariance of two overlapping-sample
   means for its standard error.
5. **Table 4** (`code/tables.py`): reduced-form OLS of the change in FTE on the
   NJ dummy / GAP, with chain, ownership, and region controls; sample n = 357
   (wave-2 wage available, or permanently closed).
6. **Figure 1** (`code/figures.py`): distribution of starting wages in waves 1
   and 2.

## Outputs

- `outputs/tables/table2_means_by_state.csv`, `table3_avg_employment.csv`,
  `table4_reduced_form.csv`, and the price pass-through extension CSVs.
- `outputs/figures/figure1_starting_wage_distribution.png`.
- `data/processed/analysis_ready.csv` (analysis-ready dataset, kept local).

## Run

```bash
python code/run_all.py
```
