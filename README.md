# Minimum Wages and Employment: Replication of Card & Krueger (1994)

> Course project · ECO6067 · Difference-in-Differences empirical replication

## 1. Paper citation

Card, D., & Krueger, A. B. (1994). Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania. *American Economic Review*, 84(4), 772–793.

## 2. Background, research question, and hypotheses

### Background
Standard (neoclassical) labor theory predicts that, in a competitive labor market, a minimum wage above the equilibrium wage reduces hiring (a downward-sloping labor demand curve). On April 1, 1992, New Jersey (NJ) raised its minimum wage from $4.25 to $5.05, while neighboring eastern Pennsylvania (PA) kept the federal minimum wage of $4.25. This policy change created a quasi-natural experiment that allows the causal effect of the minimum wage on employment to be tested with a difference-in-differences design.

### Research question
**Did the minimum-wage increase reduce employment in the low-wage fast-food industry?**

### Hypotheses
- **Null hypothesis under test (conventional prediction)**: the minimum-wage increase reduces employment (a relative employment decline in the treated state, NJ).
- **The paper's actual finding (to be verified by replication)**: the paper finds no evidence that the minimum-wage increase reduced employment, and even reports relative employment *gains* in NJ versus PA on several employment measures.

## 3. Research design

- **Treatment group**: New Jersey fast-food restaurants — minimum wage raised from $4.25 to $5.05.
- **Control group**: eastern Pennsylvania fast-food restaurants — minimum wage unchanged at $4.25.
- **Time dimension**: two waves of a telephone survey — wave 1 (before, Feb–Mar 1992) and wave 2 (after, Nov–Dec 1992).
- **Sample**: a survey of restaurants from four chains (Burger King, KFC, Roy Rogers, Wendy's), roughly 410 stores in wave 1.

Rationale for using eastern Pennsylvania as the control: it is geographically adjacent to NJ with a similar labor market and cost of living, but was not affected by this minimum-wage increase.

## 4. Basic explanation of the DID method

Difference-in-differences (DID) identifies the causal effect of the policy by comparing the before–after change in the treatment group with the before–after change in the control group, thereby removing the common time trend:

```
DID = (NJ_after − NJ_before) − (PA_after − PA_before)
```

- The first term is the average employment change in NJ; the second is the average employment change in PA (used as a proxy for the counterfactual trend).
- In a regression framework this is equivalent to an OLS estimate of the interaction term "treatment indicator × post-policy indicator".
- **Core identifying assumption**: parallel trends — absent the minimum-wage increase, employment in NJ and PA would have followed the same time path.

## 5. Replication targets (per the original paper)

> The table/figure contents below were verified against the paper's PDF text, not from memory.

| Target | Content |
|---|---|
| **Table 2** | Means of key variables, reported separately for NJ and PA, with t-statistics for the null that the means are equal across states (including the distribution of stores by chain and company-owned vs. franchisee). |
| **Table 3** | Average employment per store before and after the rise in the NJ minimum wage (levels and changes; full-time, part-time, managers, total employment, and FTE employment). |
| **Table 4** | Reduced-form DID regression models for the change in employment, across specifications (with/without controls such as chain dummies and company-owned indicator, and across sample definitions). |
| **Figure 1** | Distribution of starting wage rates (change in the NJ starting-wage distribution around the increase). |

**Key definitions (from the paper's footnotes):**
- Full-time-equivalent (FTE) employment = full-time workers (including managers) + 0.5 × part-time workers.
- Wave-2 employment: set to 0 for permanently closed stores; treated as missing for temporarily closed stores.

## 6. Data source, access, and compliance restrictions

- **Required input file**: `public.csv` (course Package 01, DID project; 410 observations × 46 columns).
- **Local location**: place the file at `data/raw/public.csv` — the canonical path the code reads. (The original package may instead be extracted under `data/01_DID/`; the file is byte-identical.)
- **Variable documentation**: see `DATA_DICTIONARY.md` inside the data package (`STATE=1` is NJ, `0` is PA; `EMPFT/EMPPT/NMGRS` and their wave-2 counterparts with suffix `2`, etc.).
- **How to obtain and place the data**: the data are provided by the course and are **not included in this repository**, and **no download link is published**. To reproduce, obtain `public.csv` from the course materials and place it at `data/raw/public.csv` before running the code.
- **Data-check findings**: see `DATA_CHECK.md` for the full structural report — dimensions, missing values, the duplicated `SHEET=407`, wave-2 nonresponse handling, and validation checks.
- **Compliance (important)**: the course data are for use in this course project only. **Raw data are not committed to the public GitHub repository** — they are excluded via `.gitignore` (`data/`, `*.csv`) and kept locally only. Follow the course data-access terms.

## 7. Project directory structure

```
minimum-wage-replication/
├── README.md            # this file: project overview and reproduction guide
├── DATA_CHECK.md        # data validation report (Phase 2)
├── requirements.txt     # Python dependencies
├── .gitignore           # excludes raw data, .DS_Store, caches, etc.
├── data/                # local only, gitignored, not committed
│   ├── raw/
│   │   └── public.csv   # ← place raw data here before running
│   └── processed/       # generated by the analysis (Phase 3), gitignored
├── src/                 # analysis code (implemented in Phase 3)
│   ├── config.py        # paths and constants (no hard-coded absolute paths)
│   ├── load_data.py     # data loading and validation
│   ├── analysis.py      # sample construction, variable definitions, DID estimation
│   ├── tables.py        # generates Tables 2–4
│   ├── figures.py       # generates Figure 1
│   ├── extension.py     # price pass-through extension (Phase 3)
│   └── main.py          # one-command reproduction entry point
├── outputs/             # generated tables and figures
│   ├── tables/
│   └── figures/
└── report/              # report, extension analysis, validation, AI-use disclosure (Phase 4)
```

> Note: `src/` holds the analysis code and `report/` holds the Phase 4 deliverables; both are populated. `data/` and `outputs/` are generated/kept locally (`data/` is gitignored and never committed).

## 8. Python environment and dependencies

- **Python**: 3.15.0.
- **Dependencies** (all verified installed and running on this interpreter): `pandas 3.0.6`, `numpy 2.5.4`, `matplotlib 3.11.2`, `statsmodels 0.15.0`, `scipy 1.18.1`.
- `requirements.txt` lists the runtime dependencies.

## 9. How to run

1. Place `public.csv` at `data/raw/public.csv` (keep the filename unchanged).
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the single entry point from the project root:
   ```
   python src/main.py
   ```
4. The program reproduces Tables 2–4 and Figure 1 under `outputs/`, runs the price pass-through extension, and prints an item-by-item comparison against the paper's printed values.

All paths are derived from the project root (`src/config.py`), so the code runs from any working directory without hard-coded machine-specific paths. The loader validates that the file exists and has the expected shape (`410 × 46`) and required columns before any analysis.

## 10. Independent extension analysis — price pass-through

**Selected extension**: *price pass-through* — did the NJ minimum-wage increase shift food prices, rather than (or in addition to) being absorbed by firms?

- **Motivation**: it answers a distinct economic question from the paper's employment results. If the wage increase was absorbed without raising prices, the employment effect is the policy's primary margin; if prices rose, part of the burden was shifted forward to consumers.
- **Data**: the survey's price items — medium soda, small fries, entree — measured in both waves; a full meal is the sum of the three.
- **Design**: the same DID structure as the employment analysis, but with the price *change* as the outcome: NJ vs. PA mean price changes (Welch DID), plus reduced-form regressions mirroring Table 4 (NJ dummy; GAP; with chain/ownership and region controls).
- **Results**: see `outputs/tables/extension_price_did_means.csv` and `extension_price_did_regressions.csv`. The point estimates show a small NJ-vs-PA price increase for the full meal (DID ≈ $0.10) and the entree (DID ≈ $0.08), and essentially no change for soda or fries; the estimates are imprecise (standard errors are comparable to or larger than the coefficients), consistent with the paper's own inconclusive price results.

## 11. Validation results vs. the paper

The reproduced values are compared item-by-item against the paper's printed tables. **Two sample-construction points were identified and are handled explicitly (not by tuning numbers):**

1. **Table 4 sample (n = 357)**: the paper's note counts "stores with available data on employment and starting wages in waves 1 and 2." Permanently closed stores (STATUS2 = 3) have wave-2 employment set to zero but no wave-2 starting wage. Requiring a wave-2 wage *and* employment for every store wrongly drops those 6 stores and yields 351; waiving the wave-2 wage requirement for permanent closures yields exactly **357** stores (290 NJ + 67 PA). With this sample the summary statistics and models (i)–(iv) match the paper **exactly**.

2. **Table 3 "all available" change (row 3)**: the standard error of the wave-1→wave-2 change must account for the fact that most stores appear in both waves (the two cross-sectional means are correlated). Treating them as independent overstates the SE; the code uses the variance of a difference of two overlapping-sample means.

| Result | Reproduced | Paper | Status |
|---|---|---|---|
| NJ wage groups ($4.25 / $4.26–4.99 / ≥$5.00) | 101 / 140 / 73 | 101 / 140 / 73 | exact |
| Table 4 sample size | 357 | 357 | exact |
| Table 4 mean / sd of dFte | −0.238 / 8.825 | −0.237 / 8.825 | exact |
| Mean GAP among NJ stores | 0.105 | 0.11 | exact |
| Table 4 (i) NJ dummy | 2.33 (1.19) | 2.33 (1.19) | exact |
| Table 4 (ii) NJ dummy | 2.30 (1.20) | 2.30 (1.20) | exact |
| Table 4 (iii) GAP | 15.65 (6.08) | 15.65 (6.08) | exact |
| Table 4 (iv) GAP | 14.92 (6.21) | 14.92 (6.21) | exact |
| Table 4 (v) GAP + region | 11.98 (7.42) | 11.91 (7.39) | ≈ (0.6%) |
| Table 3 rows 1–2 (levels) | 23.33/20.44 … | 23.33/20.44 … | exact |
| Table 3 row 4 (balanced DID) | 2.75 (1.34) | 2.75 (1.34) | exact |
| Table 3 row 5 (temp-closed = 0 DID) | 2.51 (1.35) | 2.51 (1.35) | exact |
| Table 3 row 3 (all-available DID) | 2.75 (1.31) | 2.76 (1.36) | mean ≈; SE ≈ (4%) |

**Residual discrepancies (documented, not forced):**
- **Table 4 model (v)** differs by ≈0.6% (coef 11.98 vs. 11.91; SE 7.42 vs. 7.39). The footnote's "two regions of New Jersey and two regions of eastern Pennsylvania" maps to `CENTRALJ`, `SOUTHJ`, `PA1`, `PA2` (North NJ omitted); the small residual likely reflects a subtle reference-category choice or minor data-version differences in region coding.
- **Table 3 row 3 SE** is ≈4% below the paper's (1.31 vs. 1.36). Rows 1–2 and 4–5 match exactly, and the row-3 mean matches; the remaining SE gap is attributed to a slightly different (more conservative) formula for the unbalanced "all available" change in the original paper, or to minor differences in the stores outside the Table 4 sample. No code was adjusted to force this number.

## 12. Project status and Phase 4 deliverables

- ✅ **Phase 1**: README and project overview, `.gitignore`, `requirements.txt`.
- ✅ **Phase 2**: data placement and structural checks (`DATA_CHECK.md`); raw data not committed.
- ✅ **Phase 3**: analysis code reproducing Tables 2–4 and Figure 1, result validation, and the price pass-through extension.
- ✅ **Phase 4**: final report, AI-use disclosure, and delivery checklist, in `report/`:
  - `report/report.md` — empirical report (13 sections: research question, background, data, DID design, Tables 2–4 & Figure 1, comparison, extension, robustness, limitations, AI-use disclosure).
  - `report/AI_DISCLOSURE.md` — standalone itemized AI-use disclosure.
  - `report/DELIVERY_CHECKLIST.md` — final acceptance checklist (with the two documented residual discrepancies and the gitignored-CSV caveat flagged, not hidden).

## 13. Resolved items

- **"Upload" platform**: the four-phase "uploads" refer to the course submission system (LMS); raw data never enter GitHub.
- **Row/column definitions of Tables 2–4 and Figure 1**: re-verified against the paper before coding (see Section 11 and the code comments).
- **Extension analysis**: price pass-through selected and implemented (Section 10).
