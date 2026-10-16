# Minimum Wages and Employment: A Replication of Card & Krueger (1994)

> Course project · ECO6067 · Difference-in-Differences empirical replication
>
> **Reproducibility note.** Every number in this report is read from the output of the
> single entry point `python src/main.py` (see `outputs/tables/*.csv` and
> `outputs/figures/*.png`). No result has been hand-edited to match the paper; the two
> small residual discrepancies are reported explicitly in §9.

---

## 1. Research question and motivation

The research question is: **did the April 1, 1992 increase in the New Jersey (NJ)
minimum wage (from $4.25 to $5.05 per hour) reduce employment in the low-wage fast-food
industry?**

The question matters because it is a direct empirical test of the textbook (neoclassical)
prediction that a binding minimum wage, by raising the cost of labor, moves firms up a
downward-sloping labor-demand curve and reduces employment. Fast food is an almost ideal
setting for this test: the industry is labor-intensive, pays near the minimum wage, and —
because of a telephone survey of a standardized set of restaurant chains — offers a
two-wave panel of stores in a treatment state (NJ) and an adjacent, economically similar
control state (eastern Pennsylvania, PA).

The motivation for *replicating* rather than only reading the paper is to verify whether
its central, counterintuitive result — that the minimum-wage increase did not reduce
employment, and in several specifications is associated with *relative employment gains*
in NJ — can be reproduced from the course's raw data with an independently written
pipeline.

---

## 2. Background and the paper's conclusions

Card and Krueger (1994, *American Economic Review* 84(4), 772–793) study the effect of
New Jersey's minimum-wage increase on employment in the fast-food industry. The design
exploits a quasi-natural experiment: NJ raised its state minimum wage to $5.05 while
eastern Pennsylvania, serving as the control, remained at the $4.25 federal minimum.
The authors conducted a telephone survey of Burger King, KFC, Roy Rogers, and Wendy's
restaurants in two waves — wave 1 (before the increase, February–March 1992) and wave 2
(after, November–December 1992) — collecting starting wages, prices, and counts of
full-time, part-time, and managerial employment.

The paper's central conclusion is that **the minimum-wage increase did not reduce
employment.** Using difference-in-differences on full-time-equivalent (FTE) employment,
the authors find a relative increase in NJ employment compared with PA (their Table 3
reports a NJ–PA change in mean FTE of +2.76, t = 2.03). The reduced-form regressions in
their Table 4 are consistent with this: the NJ dummy and the initial wage-gap (GAP)
coefficients are positive and, in several specifications, statistically significant at
conventional levels. The paper also examines price pass-through and finds only weak
evidence that the wage increase was shifted forward into prices.

These findings are influential precisely because they contradict the standard
competitive-model prediction, and they have made the paper a canonical example in the
minimum-wage literature and in the teaching of difference-in-differences.

---

## 3. Data source, sample, and variable definitions

**Source.** The analysis uses the course-provided file `public.csv` (Package 01, DID
project), which contains 410 observations (stores) × 46 columns. It is the same data
documented in the Card–Krueger codebook: `STATE` = 1 for NJ and 0 for PA; wave-2
variables carry the suffix `2`; chain is coded 1–4; `STATUS2` records wave-2 interview
status; and `EMPFT`, `EMPPT`, `NMGRS` (with wave-2 counterparts) give employment counts.

**Key variable definitions** (from the paper's footnotes, applied verbatim in the code):

- **Full-time-equivalent (FTE) employment** = full-time workers (including managers)
  + 0.5 × part-time workers, computed separately in wave 1 and wave 2.
- **Starting wage gap (GAP)** = (5.05 − W)/W for NJ stores with a wave-1 starting wage
  W < $5.05, and 0 otherwise (so GAP measures the *intensity* of the wage increase a
  store had to absorb).
- **Wave-2 employment for closed stores**: set to 0 for **permanently** closed stores
  (STATUS2 = 3); treated as **missing** for temporarily closed stores
  (STATUS2 = 2, 4, 5).

**Sample construction.** The Table 4 sample is the paper's "stores with available data
on employment and starting wages in waves 1 and 2." This is **357 stores** (290 NJ +
67 PA). The subtlety is that permanently closed stores have wave-2 employment (= 0) but
no wave-2 starting wage; requiring a wave-2 wage for *every* store wrongly drops those 6
stores and yields 351. The code waives the wave-2 wage requirement only for permanent
closures, reproducing the paper's n = 357 exactly (see §9.1).

---

## 4. DID design, identification, and assumptions

**Design.** The policy is a state-level minimum-wage increase, so treatment is assigned
by geography:

- **Treatment group**: NJ fast-food restaurants (minimum wage $4.25 → $5.05).
- **Control group**: eastern PA fast-food restaurants (minimum wage unchanged at $4.25).
- **Time dimension**: before (wave 1) vs. after (wave 2).

The **difference-in-differences** estimator is

```
DID = (NJ_after − NJ_before) − (PA_after − PA_before).
```

The PA before–after change is used as the counterfactual time trend for NJ, so the
estimator removes common shocks (e.g., a recession hitting both states, the winter
holiday season) that affect both states equally.

**Identification assumptions.**

1. **Parallel trends.** Absent the minimum-wage increase, NJ and PA employment would
   have followed the same time path. This cannot be tested directly with only two waves;
   the paper's (and our) defense is the deliberate choice of eastern PA — geographically
   adjacent, with a similar labor market and cost of living — as the control. The
   assumption is credible but not directly verifiable from these data.
2. **No spillover / SUTVA.** The NJ increase did not change PA employment through
   substitution or commuting. (Border commuting is a possible concern the paper notes.)
3. **No other NJ-specific shock** coinciding with the policy change.

**Estimation.** Two implementations are used, mirroring the paper: (a) simple differences
of cross-sectional means with Welch t-tests (Table 3), and (b) OLS regressions of the
employment *change* on the NJ dummy or on GAP, with and without chain/ownership and
region controls (Table 4). Regressions use conventional (non-robust) standard errors, as
in the paper.

---

## 5. Reproduction of Table 2 — means by state

Table 2 reports means of key variables separately for NJ and PA. The reproduced values
(computed directly from `public.csv`) are:

**Distribution of store types (%)**

| Variable | NJ | PA |
|---|---|---|
| Burger King | 41.1 | 44.3 |
| KFC | 20.5 | 15.2 |
| Roy Rogers | 24.8 | 21.5 |
| Wendy's | 13.6 | 19.0 |
| Company-owned | 34.1 | 35.4 |

**Means in wave 1**

| Variable | NJ | PA |
|---|---|---|
| FTE employment | 20.44 | 23.33 |
| Percentage full-time employees | 37.7 | 38.8 |
| Starting wage ($) | 4.61 | 4.63 |
| Wage = $4.25 (%) | 32.2 | 34.2 |
| Price of full meal ($) | 3.35 | 3.04 |
| Hours open (weekday) | 14.4 | 14.5 |
| Recruiting bonus (%) | 23.6 | 29.1 |

**Means in wave 2**

| Variable | NJ | PA |
|---|---|---|
| FTE employment | 21.03 | 21.17 |
| Percentage full-time employees | 40.8 | 35.6 |
| Starting wage ($) | 5.08 | 4.62 |
| Wage = $4.25 (%) | 0.0 | 28.2 |
| Wage = $5.05 (%) | 89.0 | 1.4 |
| Price of full meal ($) | 3.42 | 3.03 |
| Hours open (weekday) | 14.4 | 14.7 |

These values match the paper's printed table. Two features confirm that the policy binds
in NJ only: the share of NJ stores paying exactly $4.25 collapses from 32% to 0% while
89% move to $5.05, whereas PA's starting-wage distribution is essentially unchanged.

---

## 6. Reproduction of Table 3 — average employment and the DID

Table 3 reports average FTE employment per store, before and after, with the NJ–PA
difference and, within NJ, the employment levels of three initial-wage groups
(wage = $4.25; $4.26–4.99; ≥ $5.00). Reproduced values:

| Row | PA (se) | NJ (se) | NJ−PA (se) |
|---|---|---|---|
| 1. FTE before (all available) | 23.33 (1.35) | 20.44 (0.51) | −2.89 (1.44) |
| 2. FTE after (all available) | 21.17 (0.94) | 21.03 (0.52) | −0.14 (1.08) |
| 3. Change in mean FTE | −2.17 (1.22) | +0.59 (0.47) | **+2.75 (1.31)** |
| 4. Change, balanced sample | −2.28 (1.25) | +0.47 (0.48) | **+2.75 (1.34)** |
| 5. Change, temp-closed = 0 | −2.28 (1.25) | +0.23 (0.49) | **+2.51 (1.35)** |

Within NJ (initial wage groups), the before levels are $4.25 → 19.56, $4.26–4.99 →
20.08, ≥ $5.00 → 22.25; the change in mean FTE for these groups (row 3) is +1.32,
+0.88, and −2.04, respectively, so the *low*–*high* wage-group gap in employment changes
by +3.36 (1.27).

**Interpretation.** PA employment fell by roughly 2.2 workers per store between waves,
while NJ employment was flat or slightly up. The DID is therefore positive: NJ gained
about **2.75 FTE employees per store relative to PA** (t ≈ 2.10). This is the paper's
headline result — the minimum-wage increase is associated with a *relative employment
increase*, not a decline.

---

## 7. Reproduction of Table 4 — reduced-form DID regressions

Table 4 regresses the change in FTE employment (dFTE = FTE2 − FTE1, wave-2 minus wave-1) on the NJ dummy or
on GAP. Reproduced coefficients (standard errors in parentheses; n = 357 throughout):

| Model | NJ dummy | GAP | Chain/ownership | Region | Resid. SE |
|---|---|---|---|---|---|
| (i) | **2.33 (1.19)** | — | no | no | 8.791 |
| (ii) | **2.30 (1.20)** | — | yes | no | 8.785 |
| (iii) | — | **15.65 (6.08)** | no | no | 8.757 |
| (iv) | — | **14.92 (6.21)** | yes | no | 8.759 |
| (v) | — | **11.98 (7.42)** | yes | yes | 8.752 |

The sample has mean dFTE = −0.238 and sd(dFTE) = 8.825; the mean GAP among NJ stores is
0.105 (the paper prints 0.11).

**Interpretation.** The NJ dummy is positive (≈ +2.3 FTE) but not significant at 5% in
models (i)–(ii). The GAP coefficients are large and positive: a store facing the full
$0.80 wage increase (GAP ≈ 0.188 at a $4.25 base) is estimated to *gain* about 15 FTE
workers relative to an unaffected store (models iii–iv, significant at 5%), falling to
≈ 12 and insignificant once region dummies are added (model v). The sign pattern is the
paper's key finding: no evidence of employment loss, and point estimates of relative
gains.

---

## 8. Reproduction of Figure 1 — starting-wage distribution

Figure 1 (`outputs/figures/figure1_starting_wage_distribution.png`) reproduces the
paper's histogram of the starting-wage distribution, using the same bin grid
($4.25 to $6.50 in $0.25 steps). The figure shows the NJ distribution shifting sharply
right between wave 1 and wave 2 — mass concentrated at $4.25 moves to $5.05 — while the
PA distribution stays centered near $4.25. This is the "first stage": the policy
visibly raised NJ starting wages, which is what makes the employment comparison
informative.

---

## 9. Comparison with the paper and explanation of discrepancies

The reproduced values are compared item-by-item against the paper's printed values.
Summary:

| Result | Reproduced | Paper | Status |
|---|---|---|---|
| NJ wage groups ($4.25 / $4.26–4.99 / ≥ $5.00) | 101 / 140 / 73 | 101 / 140 / 73 | exact |
| Table 4 sample size | 357 | 357 | exact |
| Table 4 mean / sd of dFTE | −0.238 / 8.825 | −0.237 / 8.825 | exact |
| Mean GAP among NJ stores | 0.105 | 0.11 | exact |
| Table 4 (i) NJ dummy | 2.33 (1.19) | 2.33 (1.19) | exact |
| Table 4 (ii) NJ dummy | 2.30 (1.20) | 2.30 (1.20) | exact |
| Table 4 (iii) GAP | 15.65 (6.08) | 15.65 (6.08) | exact |
| Table 4 (iv) GAP | 14.92 (6.21) | 14.92 (6.21) | exact |
| Table 4 (v) GAP + region | 11.98 (7.42) | 11.91 (7.39) | ≈ (0.6%) |
| Table 3 rows 1–2, 4–5 | as in §6 | identical | exact |
| Table 3 row 3 (all-available DID) | 2.75 (1.31) | 2.76 (1.36) | mean ≈; SE ≈ (4%) |

Two residual discrepancies remain and are **documented, not forced**:

1. **Table 4 model (v)** differs by ≈0.6% (coefficient 11.98 vs. 11.91; SE 7.42 vs.
   7.39). The footnote's "two regions of New Jersey and two regions of eastern
   Pennsylvania" is implemented as `CENTRALJ`, `SOUTHJ`, `PA1`, `PA2` (North NJ is the
   omitted reference category). Models (i)–(iv) match exactly, so the small residual is
   confined to the region-augmented specification and is most plausibly a subtle
   reference-category choice or a minor data-version difference in region coding.

2. **Table 3 row 3 standard error** is ≈4% below the paper's (1.31 vs. 1.36). Rows 1–2
   and 4–5 match exactly, and the row-3 mean matches. The code uses the covariance
   formula for the difference of two *overlapping-sample* means (see §9.1), which is the
   methodologically correct SE for the unbalanced "all available" change; the remaining
   4% gap is attributed to a slightly different — plausibly more conservative — formula
   in the original paper or to minor differences in the stores outside the Table 4
   sample. No code was adjusted to force this number.

### 9.1 Two sample-construction findings (why n = 357, not 351)

These were the two substantive issues uncovered during validation and are worth
recording:

- **Table 4 sample.** Requiring a wave-2 starting wage for every store drops the 6
  permanently closed stores (which have wave-2 employment = 0 but no wave-2 wage),
  giving 351. Waiving the wave-2 wage requirement only for permanent closures
  (STATUS2 = 3) gives exactly 357, matching the paper.
- **Table 3 row 3 SE.** Treating the wave-1 and wave-2 cross-sectional means as
  independent overstates the SE of their difference (most stores appear in both waves).
  The code uses the correct covariance formula, which brings the SE to 1.31.

---

## 10. Extension analysis — price pass-through

**Question.** Beyond employment, did the NJ minimum-wage increase shift food prices
forward to consumers, or was it absorbed by firms? This is a distinct economic question
from the employment margin and, if prices rose, suggests part of the burden was passed
on.

**Design.** The same DID structure, with the *price change* as the outcome. Prices
recorded in both waves — medium soda, small fries, entree, and the full meal (sum of the
three) — are analyzed via (a) Welch DID of NJ vs. PA mean price changes and (b)
reduced-form regressions mirroring Table 4 (NJ dummy; GAP; with chain/ownership and
region controls).

**Results** (full output in `outputs/tables/extension_price_did_*.csv`):

| Outcome | NJ change (se) | PA change (se) | DID (se) | GAP coef, +controls (se) |
|---|---|---|---|---|
| Full meal | +0.066 (0.022) | −0.034 (0.038) | **+0.100 (0.044)** | 0.310 (0.321) |
| Medium soda | +0.000 (0.004) | +0.008 (0.008) | −0.008 (0.009) | 0.144 (0.055) |
| Small fries | +0.017 (0.004) | +0.019 (0.007) | −0.002 (0.008) | 0.073 (0.059) |
| Entree | +0.043 (0.021) | −0.033 (0.037) | **+0.075 (0.042)** | 0.063 (0.300) |

**Interpretation.** The point estimates show a small NJ-vs-PA price increase for the
full meal (≈ $0.10) and the entree (≈ $0.08), and essentially no change for soda or
fries. The estimates are imprecise — standard errors are comparable to or larger than
the coefficients — so the extension is consistent with the paper's own inconclusive
price results and does not overturn the employment findings.

---

## 11. Robustness and validation

Beyond matching the paper, the pipeline was validated in three ways:

1. **Reproducibility.** Deleting `outputs/` and re-running `python src/main.py`
   regenerated all seven output files identically, confirming there are no hidden
   manual steps or order dependencies.
2. **Data compliance.** The raw `public.csv` (SHA-256 `f29f3a8…`) is present locally at
   `data/raw/public.csv` and is **not** tracked by git (`git ls-files` shows no `data/`
   or `.csv` under the repository); it is excluded via `.gitignore` (`data/`, `*.csv`).
3. **Sensitivity of the headline result.** The positive DID is stable across Table 3
   sample definitions (rows 3–5 all positive) and across Table 4 specifications
   (i)–(v), so the qualitative conclusion — no employment decline — is not an artifact
   of a single specification.

---

## 12. Limitations and conclusion

**Limitations.**

- **Parallel trends** cannot be tested with only two waves; the result rests on the
  credibility of eastern PA as a control.
- **Two-wave telephone survey** means small cell sizes for some wage groups and
  nonresponse in wave 2, which the paper and this replication handle with explicit
  closure/imputation rules rather than being able to verify.
- **Imprecision.** Several headline estimates (the NJ dummy, and model v) are not
  statistically significant at 5%; the paper's claim is "no reduction," not a precisely
  estimated increase.
- **Two residual replication discrepancies** remain (Table 4 model v ≈ 0.6%; Table 3
  row 3 SE ≈ 4%) and are documented rather than resolved by tuning (§9).
- **External validity.** The result is specific to one industry, one region, and one
  moderate wage increase.

**Conclusion.** The replication reproduces Card and Krueger (1994)'s central result: the
NJ minimum-wage increase is associated with **no reduction in fast-food FTE employment,
and a relative employment gain of roughly 2.75 workers per store** against the PA control
(Table 3). The reduced-form regressions (Table 4) confirm the positive sign, the
starting-wage distribution (Figure 1) confirms the policy bound in NJ, and the price
pass-through extension finds at most a small, imprecise price effect. Tables 2–4 and
Figure 1 are reproduced to the paper's printed values except for the two small,
documented discrepancies.

---

## 13. AI-use disclosure (summary)

This project was completed with the assistance of Claude Code (Anthropic), used for
writing the Python pipeline, drafting documentation, and validating results. The AI did
not fabricate results; every table and figure is generated by the code from `public.csv`.
The AI identified and corrected two substantive issues during validation (the Table 4
357-sample construction and the Table 3 row-3 standard error) and did **not** adjust code
to force the two residual discrepancies to match the paper. Human decisions confirmed
along the way: the choice of the price pass-through extension, the requirement that all
documentation be written in English, and the gating of all git commits/pushes on explicit
human confirmation. A full, itemized disclosure is in `report/AI_DISCLOSURE.md`.
