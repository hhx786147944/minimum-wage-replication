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

- **Data file**: `public.csv` (course Package 01, DID project; 410 observations × 46 columns).
- **Variable documentation**: see `DATA_DICTIONARY.md` inside the data package (`STATE=1` is NJ, `0` is PA; `EMPFT/EMPPT/NMGRS` and their wave-2 counterparts with suffix `2`, etc.).
- **Access**: the data are provided by the course; **this repository provides no download link**. Before running, place `public.csv` into the `data/` directory (see directory structure).
- **Compliance (important)**: the course data are for use in this course project only. **Raw data are not committed to the public GitHub repository** — they are excluded via `.gitignore` and kept locally only. Follow the course data-access terms.

## 7. Project directory structure

```
minimum-wage-replication/
├── README.md            # this file: project overview and reproduction guide
├── requirements.txt     # Python dependencies
├── .gitignore           # excludes raw data, .DS_Store, caches, etc.
├── data/                # raw data (local only, gitignored, not committed)
│   └── public.csv       # ← place here before running
├── src/                 # analysis code (implemented in Phase 3)
│   ├── config.py        # paths and constants
│   ├── load_data.py     # data loading and cleaning
│   ├── analysis.py      # sample construction, variable definitions, DID estimation
│   ├── tables.py        # generates Tables 2–4
│   ├── figures.py       # generates Figure 1
│   └── main.py          # one-command reproduction entry point
├── outputs/             # generated tables and figures
│   ├── tables/
│   └── figures/
└── report/              # report, extension analysis, validation, AI-use disclosure (Phase 4)
```

> Note: the `data/`, `src/`, `outputs/`, and `report/` directories already exist; `src/` and `report/` contents will be created in later phases and are currently empty (no placeholder files added just to populate directories).

## 8. Python environment and dependencies

- **Python**: 3.15.0 (the only interpreter on this machine).
- **Already installed**: `pandas 3.0.6`, `numpy 2.5.4`, `matplotlib 3.11.2`.
- **Planned (to be verified in Phase 3)**: `statsmodels` (DID regressions with robust/clustered standard errors) and `scipy`.
- Dependencies are listed in `requirements.txt` (final versions will be pinned in Phase 4).

> Risk note: Python 3.15 is relatively new, so whether `statsmodels`/`scipy` have prebuilt wheels for it will be verified when installing in Phase 3. Fallback options: a virtual environment on an older Python, or a `numpy`-only OLS + clustered-SE implementation.

## 9. How to run (planned; to be implemented in Phase 3)

1. Place `public.csv` into the `data/` directory (keep the filename unchanged).
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the entry point (planned command, subject to the final implementation):
   ```
   python src/main.py
   ```
4. The program generates Tables 2–4 and Figure 1 under `outputs/` and prints a comparison summary against the paper.

## 10. Independent extension analysis — candidate directions (pending data checks and methodological justification)

> The following are **candidates only** — not yet implemented, and not claimed as complete. One will be selected and fully justified after the data are inspected.

1. **Heterogeneous DID**: estimate by chain (Burger King / KFC / Roy Rogers / Wendy's) or company-owned vs. franchisee, to study heterogeneity of the minimum-wage effect.
2. **Price pass-through**: whether the minimum-wage increase was passed through to food prices (the reduced-form price regressions in the paper's Table 7).
3. **Starting-wage distribution**: building on Figure 1, characterize the compression of the starting-wage distribution.
4. **Proportional employment change**: robustness using the proportional change in employment as the dependent variable.
5. **Robustness and placebo checks**: clustered standard errors (state×time or store level), balanced vs. unbalanced samples, and a discussion of parallel trends.

## 11. Validation, limitations, and AI-use disclosure (planned)

- **Validation (to be implemented in Phases 3–4)**: compare reproduced numbers item-by-item against the paper's printed tables; verify the FTE definition, balanced-sample definition, and wave-2 missing-data handling against the paper; explain any discrepancies rather than forcing exact matches.
- **Limitations (to be written in Phase 4)**: the parallel-trends assumption cannot be fully tested; the sample is limited to four fast-food chains in a limited region; telephone-survey nonresponse/refusal handling; the questionnaire design in which starting wage is blank for NJ stores in wave 1.
- **AI-use disclosure (maintained throughout; finalized in Phase 4)**: a dedicated section in the report (and/or README) will state which work AI contributed to (data checks, code scaffolding, drafting), how outputs were verified (item-by-item comparison with the paper, code review, runtime self-checks), and which AI suggestions were corrected or rejected. **This README was drafted with AI assistance; key facts (paper details, replication targets, FTE definition) were verified against the paper's PDF text.**

## 12. Current progress and remaining work

- ✅ **Phase 1 (this phase)**: README and project overview, `.gitignore`, `requirements.txt` complete.
- ⬜ **Phase 2 (next)**: data placement and structural checks (raw data not committed).
- ⬜ **Phase 3**: analysis code reproducing Tables 2–4 and Figure 1.
- ⬜ **Phase 4**: report, extension analysis, validation, limitations, AI-use disclosure finalization, and final release.

## 13. Items to confirm (not yet established facts)

- **Target platform for the four-phase "uploads"**: the data-file "upload" refers to the course submission system (LMS), not the public GitHub repository; raw data never enter GitHub.
- The exact **row/column definitions** of Tables 2–4 and Figure 1 will follow the paper and will be re-verified before writing code in Phase 3.
- The **final choice of extension analysis**: to be determined after the data are inspected (see Section 10 candidates).
