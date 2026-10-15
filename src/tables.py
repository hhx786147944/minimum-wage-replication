"""Generate Tables 2-4 of Card & Krueger (1994)."""
import numpy as np
import pandas as pd
from scipy import stats

import analysis
import config

C = config.C


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _state_stats(s, state):
    """Mean/SE/N of a store-level series for one state group (NJ or PA)."""
    mask = state == 1
    return analysis.mean_se(s[mask])


def _ttest(s, state):
    """Welch t-statistic for equality of means between NJ and PA."""
    nj = s[state == 1].dropna()
    pa = s[state == 0].dropna()
    if len(nj) < 2 or len(pa) < 2:
        return np.nan
    return stats.ttest_ind(nj, pa, equal_var=False).statistic


def _indicator(series, value):
    """Store-level 0/1 indicator, NaN where the underlying series is NaN."""
    out = (series == value).astype(float)
    out[series.isna()] = np.nan
    return out


def _save(df, name):
    config.TABLES_DIR.mkdir(parents=True, exist_ok=True)
    path = config.TABLES_DIR / name
    df.to_csv(path, index=False)
    print(f"[tables] wrote {path}")
    return path


# --------------------------------------------------------------------------
# Table 2
# --------------------------------------------------------------------------
def table2(df):
    """Table 2: means of key variables by state, with t-statistics.

    Columns: variable, NJ mean (SE), PA mean (SE), t (equal-means test).
    """
    st = df[C["state"]]
    rows = []

    def add(section, label, series, as_pct=False):
        nj_m, nj_se, nj_n = _state_stats(series, st)
        pa_m, pa_se, pa_n = _state_stats(series, 1 - st)
        if as_pct:
            nj_m, nj_se = nj_m * 100, nj_se * 100
            pa_m, pa_se = pa_m * 100, pa_se * 100
        t = _ttest(series, st)
        rows.append(dict(
            section=section, variable=label,
            NJ=nj_m, NJ_SE=nj_se, NJ_n=nj_n,
            PA=pa_m, PA_SE=pa_se, PA_n=pa_n, t=t,
        ))

    # Section 1: distribution of store types (percentages; time-invariant).
    for code, lab in config.CHAIN_LABELS.items():
        add("1. Distribution of store types (%)", lab,
            (df[C["chain"]] == code).astype(float), as_pct=True)
    add("1. Distribution of store types (%)", "Company-owned",
        df[C["co_owned"]].astype(float), as_pct=True)

    # Section 2: means in wave 1.
    add("2. Means in wave 1", "FTE employment", df["fte"])
    add("2. Means in wave 1", "Percentage full-time employees", df["pct_ft"])
    add("2. Means in wave 1", "Starting wage", df[C["wage_st"]])
    add("2. Means in wave 1", "Wage = $4.25 (%)",
        _indicator(df[C["wage_st"]], 4.25), as_pct=True)
    add("2. Means in wave 1", "Price of full meal", df["meal"])
    add("2. Means in wave 1", "Hours open (weekday)", df[C["hrsopen"]])
    add("2. Means in wave 1", "Recruiting bonus (%)",
        df[C["bonus"]].astype(float), as_pct=True)

    # Section 3: means in wave 2.
    # NOTE: public.csv has no wave-2 recruiting-bonus variable (only SPECIAL2,
    # "special program"), so the paper's wave-2 "recruiting bonus" row is not
    # reproduced here; this is flagged as a data-vs-paper discrepancy.
    add("3. Means in wave 2", "FTE employment", df["fte2"])
    add("3. Means in wave 2", "Percentage full-time employees", df["pct_ft2"])
    add("3. Means in wave 2", "Starting wage", df[C["wage_st2"]])
    add("3. Means in wave 2", "Wage = $4.25 (%)",
        _indicator(df[C["wage_st2"]], 4.25), as_pct=True)
    add("3. Means in wave 2", "Wage = $5.05 (%)",
        _indicator(df[C["wage_st2"]], 5.05), as_pct=True)
    add("3. Means in wave 2", "Price of full meal", df["meal2"])
    add("3. Means in wave 2", "Hours open (weekday)", df[C["hrsopen2"]])

    out = pd.DataFrame(rows)
    _save(out.round(3), "table2_means_by_state.csv")
    return out


# --------------------------------------------------------------------------
# Table 3
# --------------------------------------------------------------------------
def _group_mean_se(df, series, mask):
    """Mean/SE of a store-level series within a group defined by a boolean mask."""
    m, se, n = analysis.mean_se(series[mask])
    return m, se, n


def table3(df):
    """Table 3: average FTE employment per store before and after the increase.

    Columns: PA, NJ, NJ-PA, NJ(wage=$4.25), NJ($4.26-$4.99), NJ(>=$5.00),
    Low-High, Midrange-High. Rows 1-5 as in the paper.
    """
    st = df[C["state"]]
    wage = df[C["wage_st"]]
    nj = st == 1
    pa = st == 0
    g_low = nj & (wage == 4.25)
    g_mid = nj & (wage > 4.25) & (wage < 5.00)
    g_high = nj & (wage >= 5.00)
    base_groups = {
        "PA": pa, "NJ": nj, "NJ_425": g_low, "NJ_426_499": g_mid, "NJ_500": g_high,
    }

    # Store-level outcomes for each row.
    row_series = {
        1: df["fte"],        # FTE before, all available obs
        2: df["fte2"],       # FTE after, all available obs
        4: df["d_fte"],      # change, balanced (d_fte NaN unless both waves present)
        5: df["d_fte_temp0"],  # change, temporarily closed set to 0
    }

    stat = {r: {} for r in row_series}
    for r, s in row_series.items():
        for g, mask in base_groups.items():
            stat[r][g] = _group_mean_se(df, s, mask)

    rows = {}
    col_labels = ["PA", "NJ", "NJ-PA", "NJ(wage=4.25)", "NJ(4.26-4.99)",
                  "NJ(>=5.00)", "Low-High", "Midrange-High"]

    def diff(a, b):
        m = a[0] - b[0]
        se = np.sqrt(a[1] ** 2 + b[1] ** 2)
        return m, se, a[2]

    for r in [1, 2, 4, 5]:
        pa_, nj_, low_, mid_, high_ = (stat[r][g] for g in
                                       ["PA", "NJ", "NJ_425", "NJ_426_499", "NJ_500"])
        rows[r] = {
            "PA": pa_, "NJ": nj_, "NJ-PA": diff(nj_, pa_),
            "NJ(wage=4.25)": low_, "NJ(4.26-4.99)": mid_, "NJ(>=5.00)": high_,
            "Low-High": diff(low_, high_), "Midrange-High": diff(mid_, high_),
        }

    # Row 3 = change in mean FTE using all available observations in each wave.
    # The mean is mean(wave 2) - mean(wave 1); the SE accounts for the overlap
    # between waves (most stores appear in both waves, so the two cross-sectional
    # means are correlated). Treating them as independent would overstate the SE.
    pa3, nj3, low3, mid3, high3 = (
        analysis.mean_change_all_available(
            df.loc[base_groups[g], "fte"], df.loc[base_groups[g], "fte2"]
        )
        for g in ["PA", "NJ", "NJ_425", "NJ_426_499", "NJ_500"]
    )
    rows[3] = {
        "PA": pa3, "NJ": nj3, "NJ-PA": diff(nj3, pa3),
        "NJ(wage=4.25)": low3, "NJ(4.26-4.99)": mid3, "NJ(>=5.00)": high3,
        "Low-High": diff(low3, high3), "Midrange-High": diff(mid3, high3),
    }

    # Build output table: one row per estimate, with (mean, SE) pairs.
    out = pd.DataFrame()
    for c in col_labels:
        out[f"{c}_mean"] = [rows[r][c][0] for r in [1, 2, 3, 4, 5]]
        out[f"{c}_se"] = [rows[r][c][1] for r in [1, 2, 3, 4, 5]]
    out.insert(0, "row", [
        "1. FTE before (all available)",
        "2. FTE after (all available)",
        "3. Change in mean FTE",
        "4. Change, balanced sample",
        "5. Change, temp-closed = 0",
    ])

    _save(out.round(3), "table3_avg_employment.csv")
    return out


# --------------------------------------------------------------------------
# Table 4
# --------------------------------------------------------------------------
def table4(df):
    """Table 4: reduced-form DID models for the change in FTE employment.

    Returns a DataFrame with model coefficients and a dict of fitted results.
    """
    s = analysis.table4_sample(df)
    y = s["d_fte"]

    chain_owned = analysis.chain_owned_controls(s)
    region = analysis.region_dummies(s)

    nj = pd.Series(s["nj"], name="nj")
    gap = pd.Series(s["gap"], name="gap")

    specs = {
        "i": nj,
        "ii": pd.concat([nj, chain_owned], axis=1),
        "iii": gap,
        "iv": pd.concat([gap, chain_owned], axis=1),
        "v": pd.concat([gap, chain_owned, region], axis=1),
    }

    results = {}
    for k, X in specs.items():
        results[k] = analysis.fit_ols(y, X)

    coef_rows = []
    for k in ["i", "ii", "iii", "iv", "v"]:
        r = results[k]
        coef_rows.append({
            "model": k,
            "NJ_dummy_coef": r.params.get("nj", np.nan),
            "NJ_dummy_se": r.bse.get("nj", np.nan),
            "GAP_coef": r.params.get("gap", np.nan),
            "GAP_se": r.bse.get("gap", np.nan),
            "n": int(r.nobs),
            "resid_se": float(np.sqrt(r.mse_resid)),
            "r_squared": float(r.rsquared),
        })

    out = pd.DataFrame(coef_rows)
    _save(out.round(4), "table4_reduced_form.csv")

    # A human-readable coefficient table (coefficient over SE in parentheses).
    table = pd.DataFrame(index=["(i)", "(ii)", "(iii)", "(iv)", "(v)"])
    table["NJ dummy"] = [
        f"{r.params.get('nj', np.nan):.2f} ({r.bse.get('nj', np.nan):.2f})"
        if not np.isnan(r.params.get('nj', np.nan)) else "—"
        for r in [results[k] for k in ["i", "ii", "iii", "iv", "v"]]
    ]
    table["Initial wage gap (GAP)"] = [
        f"{r.params.get('gap', np.nan):.2f} ({r.bse.get('gap', np.nan):.2f})"
        if not np.isnan(r.params.get('gap', np.nan)) else "—"
        for r in [results[k] for k in ["i", "ii", "iii", "iv", "v"]]
    ]
    table["Chain+ownership"] = ["no", "yes", "no", "yes", "yes"]
    table["Region"] = ["no", "no", "no", "no", "yes"]
    table["N"] = [int(results[k].nobs) for k in ["i", "ii", "iii", "iv", "v"]]
    table["Resid SE"] = [
        f"{np.sqrt(results[k].mse_resid):.3f}" for k in ["i", "ii", "iii", "iv", "v"]
    ]
    _save(table, "table4_reduced_form_pretty.csv")

    # Sample statistics quoted in the paper's note.
    sample = dict(
        n=int(len(s)),
        mean_d_fte=float(y.mean()),
        sd_d_fte=float(y.std(ddof=1)),
        gap_mean_nj=float(s.loc[s["nj"] == 1, "gap"].mean()),
    )
    return out, results, sample
