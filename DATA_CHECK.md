# Data Validation Report: `public.csv` (Package 01)

This report documents the structural checks performed on the raw data before any analysis. It accompanies `README.md`; no regressions or results are reported here.

## 1. Source and location

- **Source**: course Package 01 (`01_DID.zip` → `data/public.csv`), the Card & Krueger (1994) fast-food restaurant survey.
- **Canonical raw-data location (used by the code)**: `data/raw/public.csv`
- **Equivalent original extraction**: `data/01_DID/data/public.csv` (the package extracted unchanged; SHA-1 identical to `data/raw/public.csv`: `f29f3a8fb9451791f0821d55a1f57daa11982e26`).
- **Variable documentation**: `DATA_DICTIONARY.md` inside the data package.

> Raw data are **not** committed to the public GitHub repository (see `.gitignore`, which excludes `data/` and `*.csv`).

## 2. File readability

- Readable as standard CSV: comma-delimited, with a header row; no BOM/encoding problems.
- Parsed cleanly by `pandas.read_csv` with no quoting or separator errors.

## 3. Dimensions and columns

- **410 observations × 46 columns** (matches the data dictionary).

The 46 fields are, in order:

```
SHEET CHAIN CO_OWNED STATE SOUTHJ CENTRALJ NORTHJ PA1 PA2 SHORE
NCALLS EMPFT EMPPT NMGRS WAGE_ST INCTIME FIRSTINC BONUS PCTAFF MEALS
OPEN HRSOPEN PSODA PFRY PENTREE NREGS NREGS11
TYPE2 STATUS2 DATE2 NCALLS2 EMPFT2 EMPPT2 NMGRS2 WAGE_ST2 INCTIME2
FIRSTIN2 SPECIAL2 MEALS2 OPEN2R HRSOPEN2 PSODA2 PFRY2 PENTREE2 NREGS2 NREGS112
```

Suffix `2` denotes the second survey wave; blank cells read as missing (`NaN`).

## 4. Data types (as inferred)

- Integer columns: `SHEET`, `CHAIN`, `CO_OWNED`, `STATE`, `SOUTHJ`, `CENTRALJ`, `NORTHJ`, `PA1`, `PA2`, `SHORE`, `NCALLS`, `BONUS`, `MEALS`, `TYPE2`, `STATUS2`, `DATE2`.
- Float columns (contain blanks → `NaN`): all employment, wage, hours, price, and call-count variables.

## 5. Missing values

| Column | Missing | Pct | Note |
|---|---|---|---|
| `NCALLS2` | 249 | 60.7% | call-count field; mostly blank for wave-2 respondents (not an employment variable) |
| `FIRSTINC` | 43 | 10.5% | first-wave wage-increase timing |
| `PCTAFF` | 44 | 10.7% | % unionized/affected (wave 1) |
| `INCTIME` | 31 | 7.6% | time-to-wage-increase |
| `WAGE_ST` | 20 | 4.9% | 17 NJ + 3 PA |
| `WAGE_ST2` | 21 | 5.1% | 13 NJ + 8 PA |
| `EMPFT`/`NMGRS` | 6 | 1.5% | |
| `EMPPT` | 4 | 1.0% | |
| `EMPFT2` | 12 | 2.9% | |
| `EMPPT2` | 10 | 2.4% | |
| `NMGRS2` | 6 | 1.5% | |
| price fields (`PSODA`, `PFRY`, `PENTREE`, and `2` variants) | 8–28 | 2–7% | |
| `NREGS`/`NREGS2` fields | 6–27 | 1.5–6.6% | |

Key structural point: **wave-2 employment missingness is driven by wave-2 nonresponse/closure**, not by random data-entry gaps (see §7).

## 6. Duplicates and identifier

- **Full-row duplicates**: 0.
- **`SHEET` duplicates**: 1 value is duplicated — `SHEET = 407` appears twice, but the two rows are **two different stores** (one KFC / PA-East, the other Wendy's / NJ-North). 409 unique `SHEET` values across 410 rows.

**Implication**: `SHEET` is **not a globally unique store identifier** in this dataset. Do not use it as a primary key; treat each row as one store-wave record.

## 7. Categorical variables and encodings

| Variable | Encoding (verified) | Counts |
|---|---|---|
| `STATE` | 1 = New Jersey, 0 = Pennsylvania | NJ 331, PA 79 |
| `CHAIN` | 1 = Burger King, 2 = KFC, 3 = Roy Rogers, 4 = Wendy's | 171 / 80 / 99 / 60 |
| `CO_OWNED` | 1 = company-owned, 0 = franchisee | 141 / 269 |
| `SOUTHJ` | 1 = southern NJ | 93 |
| `CENTRALJ` | 1 = central NJ | 63 |
| `NORTHJ` | 1 = northern NJ | 175 |
| `PA1` | 1 = NE Philadelphia suburbs (PA) | 36 |
| `PA2` | 1 = Easton area (PA) | 43 |
| `SHORE` | 1 = NJ shore | 35 |
| `BONUS` | 1 = recruiting bonus offered | 101 |
| `TYPE2` | 1 = telephone, 2 = personal interview | 371 / 39 |
| `STATUS2` | 0 = refused, 1 = answered, 2 = renovation closure, 3 = permanent closure, 4 = highway-construction closure, 5 = mall-fire closure | 1 / 399 / 2 / 6 / 1 / 1 |

**Region consistency check (passed)**: `STATE=1` rows carry exactly one of `SOUTHJ`/`CENTRALJ`/`NORTHJ` (93 + 63 + 175 = 331 = NJ count); `STATE=0` rows carry exactly one of `PA1`/`PA2` (36 + 43 = 79 = PA count). No cross-state region flags.

## 8. Wave-2 nonresponse and the paper's handling

Of 410 stores, `STATUS2 ≠ 1` for 11 stores. Verified against the paper's footnote:

- **6 permanent closures** (`STATUS2 = 3`): wave-2 employment is recorded as **0** (full-time, part-time, managers all `0.0`).
- **4 temporary closures** (`STATUS2 = 2, 4, 5`) and **1 refusal** (`STATUS2 = 0`): wave-2 employment is **missing** (`NaN`).

This matches the paper: permanent closures are set to zero employment; temporary closures/refusals are treated as missing. It is the key driver of wave-2 employment missingness and defines the "balanced sample" used in the DID analysis.

## 9. Validation checks (all passed unless noted)

- **No wage below $4.25** (the federal floor) in either wave — no obvious sub-minimum data errors.
- **NJ wave-2 starting wage ≥ $5.05** (the new minimum) for all but **1 store**, which reports $5.00 (a minor anomaly worth noting; does not affect employment analysis).
- **No negative employment values** in any employment variable.
- **Chain × state** distribution sums correctly to 410 (all four chains present in both states).
- `DATE2` is in `MMDDYY` format (e.g. `111792` = 1992-11-17), ranging 1992-11-05 to 1992-12-31 (27 distinct dates) — consistent with the paper's Nov–Dec 1992 wave-2 window.

## 10. Implications for the DID analysis (Phase 3)

1. **Sample**: the balanced panel is defined by non-missing employment in both waves (or by the paper's permanent-closure = zero convention); the exact rule will follow the paper and be re-verified in Phase 3.
2. **Employment measures**: total employment = `EMPFT + EMPPT + NMGRS`; FTE employment = `EMPFT + NMGRS + 0.5 × EMPPT` (per the paper's footnote).
3. **Treatment/time**: `STATE` (1 = NJ) × wave indicator; the DID coefficient is the interaction term.
4. **Identifier caution**: use the row (store) rather than `SHEET` as the unit of observation.

## 11. Data-access compliance

- Course data are for course use only; **not committed to the public repository**, and **no download link is published**.
- `data/` and `*.csv` are listed in `.gitignore`; the raw file at `data/raw/public.csv` is local-only.
