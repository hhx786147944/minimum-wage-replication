"""Sample construction, variable generation, and DID estimation helpers."""
import numpy as np
import pandas as pd
import statsmodels.api as sm

import config

C = config.C

# Temporarily closed stores (per DATA_DICTIONARY STATUS2 coding).
TEMP_CLOSED_CODES = {2, 4, 5}   # renovation, highway-construction, mall-fire


def add_derived_variables(df):
    """Add the employment, wage-gap, and price variables used by the analysis.

    Returns a new DataFrame; the input is never modified.
    """
    out = df.copy()

    # Employment: total and full-time-equivalent (paper footnote).
    # FTE = full-time workers (incl. managers) + 0.5 * part-time workers.
    out["tot"] = out[C["empft"]] + out[C["emppt"]] + out[C["nmgrs"]]
    out["tot2"] = out[C["empft2"]] + out[C["emppt2"]] + out[C["nmgrs2"]]
    out["fte"] = out[C["empft"]] + out[C["nmgrs"]] + 0.5 * out[C["emppt"]]
    out["fte2"] = out[C["empft2"]] + out[C["nmgrs2"]] + 0.5 * out[C["emppt2"]]

    # Percentage full-time employees (full-time incl. managers / total).
    out["pct_ft"] = 100.0 * (out[C["empft"]] + out[C["nmgrs"]]) / out["tot"]
    out["pct_ft2"] = 100.0 * (out[C["empft2"]] + out[C["nmgrs2"]]) / out["tot2"]

    # Price of a full meal = medium soda + small fries + entree.
    out["meal"] = out[C["psoda"]] + out[C["pfry"]] + out[C["pentree"]]
    out["meal2"] = out[C["psoda2"]] + out[C["pfry2"]] + out[C["pentree2"]]

    # NJ treatment dummy.
    out["nj"] = (out[C["state"]] == 1).astype(int)

    # Initial wage gap GAP: proportional increase needed to reach the new
    # minimum. 0 for PA stores and for NJ stores already at/above $5.05;
    # (5.05 - W)/W for NJ stores below $5.05. Undefined (NaN) where an NJ
    # store has no reported wave-1 starting wage.
    wage = out[C["wage_st"]]
    is_nj = out[C["state"]] == 1
    out["gap"] = np.where(
        is_nj & wage.notna() & (wage < config.NJ_NEW_MIN_WAGE),
        (config.NJ_NEW_MIN_WAGE - wage) / wage,
        0.0,
    )
    out.loc[is_nj & wage.isna(), "gap"] = np.nan

    # Change in FTE employment (wave 2 - wave 1).
    out["d_fte"] = out["fte2"] - out["fte"]

    # Variant where temporarily closed stores' wave-2 employment is set to 0
    # (rather than missing), used in Table 3 row 5.
    out["fte2_temp0"] = out["fte2"].copy()
    temp_closed = out[C["status2"]].isin(TEMP_CLOSED_CODES)
    out.loc[temp_closed, "fte2_temp0"] = 0.0
    out["d_fte_temp0"] = out["fte2_temp0"] - out["fte"]

    # Price changes (for the price pass-through extension).
    out["d_meal"] = out["meal2"] - out["meal"]
    out["d_psoda"] = out[C["psoda2"]] - out[C["psoda"]]
    out["d_pfry"] = out[C["pfry2"]] - out[C["pfry"]]
    out["d_pentree"] = out[C["pentree2"]] - out[C["pentree"]]

    return out


def mean_se(s):
    """Return (mean, standard error, n) of a Series, ignoring NaNs."""
    s = s.dropna()
    n = len(s)
    if n == 0:
        return np.nan, np.nan, 0
    return s.mean(), s.std(ddof=1) / np.sqrt(n), n


def se_diff(se1, se2):
    """Standard error of a difference of two independent means."""
    return np.sqrt(se1 ** 2 + se2 ** 2)


def mean_change_all_available(fte1, fte2):
    """Mean change in employment using all available observations in each wave.

    The change is mean(wave 2) - mean(wave 1) over the (possibly different) sets
    of stores observed in the two waves. The standard error accounts for the
    overlap between the waves: because most stores appear in both waves, the two
    cross-sectional means are correlated, and treating them as independent would
    overstate the standard error. This implements the variance of a difference
    of two overlapping-sample means.

    Returns (change, standard_error, n_overlap).
    """
    s1, s2 = fte1.notna(), fte2.notna()
    n1, n2 = int(s1.sum()), int(s2.sum())
    if n1 == 0 or n2 == 0:
        return np.nan, np.nan, 0
    both = s1 & s2
    n_both = int(both.sum())
    v1 = fte1[s1].var(ddof=1)
    v2 = fte2[s2].var(ddof=1)
    change = fte2[s2].mean() - fte1[s1].mean()
    cov = np.cov(fte1[both], fte2[both], ddof=1)[0, 1] if n_both > 1 else 0.0
    var = v2 / n2 + v1 / n1 - 2.0 * (n_both / (n1 * n2)) * cov
    return change, np.sqrt(max(var, 0.0)), n_both


def fit_ols(y, X, add_const=True):
    """Fit an OLS model; returns the fitted statsmodels result."""
    X = sm.add_constant(X) if add_const else X
    return sm.OLS(y, X).fit()


def table4_sample(df):
    """Subsample for Table 4 (paper note: 357 stores).

    Requires valid employment in both waves and a valid wave-1 starting wage.
    Wave-2 employment for a permanently closed store (STATUS2 = 3) is recorded
    as zero, and such stores have no wave-2 starting wage, so the wave-2 wage
    requirement is waived for them. This yields exactly the paper's 357-store
    sample (351 with a reported wave-2 wage + 6 permanent closures).
    """
    perm_closed = df[C["status2"]] == 3
    mask = (
        df["fte"].notna()
        & df["fte2"].notna()
        & df[C["wage_st"]].notna()
        & (df[C["wage_st2"]].notna() | perm_closed)
    )
    return df[mask].copy()


def chain_owned_controls(s):
    """Chain dummies (BK omitted as base) + company-owned dummy."""
    chain_d = pd.get_dummies(
        s[C["chain"]], prefix="chain", drop_first=True, dtype=int
    )
    ctrl = pd.concat(
        [chain_d, pd.Series(s[C["co_owned"]].astype(int), name="co_owned")],
        axis=1,
    )
    return ctrl


def region_dummies(s):
    """Region dummies: two NJ regions + two eastern-PA regions (North NJ is base)."""
    cols = [C["southj"], C["centralj"], C["pa1"], C["pa2"]]
    return s[cols].astype(int).rename(
        columns={c: c.lower() for c in cols}
    )
