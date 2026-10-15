"""Independent extension: did the NJ minimum wage pass through to food prices?

Answers a distinct economic question from the paper's employment results:
whether the minimum-wage increase was absorbed by firms or shifted forward to
consumers as higher fast-food prices. Uses the survey price items (medium soda,
small fries, entree) and estimates the same difference-in-differences designs as
the employment analysis, but with price changes as the outcome.
"""
import numpy as np
import pandas as pd

import analysis
import config

C = config.C

PRICE_OUTCOMES = {
    "Full meal (soda+fries+entree)": "d_meal",
    "Medium soda": "d_psoda",
    "Small fries": "d_pfry",
    "Entree": "d_pentree",
}


def _did_means(df):
    """Mean price change by state, plus the DID (NJ - PA) and its SE."""
    st = df[C["state"]]
    rows = []
    for label, col in PRICE_OUTCOMES.items():
        nj_m, nj_se, nj_n = analysis.mean_se(df[col][st == 1])
        pa_m, pa_se, pa_n = analysis.mean_se(df[col][st == 0])
        did = nj_m - pa_m
        did_se = analysis.se_diff(nj_se, pa_se)
        rows.append(dict(
            outcome=label, NJ_change=nj_m, NJ_se=nj_se, NJ_n=nj_n,
            PA_change=pa_m, PA_se=pa_se, PA_n=pa_n,
            DID=did, DID_se=did_se,
        ))
    out = pd.DataFrame(rows)
    config.TABLES_DIR.mkdir(parents=True, exist_ok=True)
    path = config.TABLES_DIR / "extension_price_did_means.csv"
    out.round(4).to_csv(path, index=False)
    print(f"[extension] wrote {path}")
    return out


def _did_regressions(df):
    """Reduced-form DID regressions for the price change, mirroring Table 4."""
    rows = []
    for label, col in PRICE_OUTCOMES.items():
        y = df[col].dropna()
        ss = df.loc[y.index]
        nj = pd.Series(ss["nj"], name="nj")
        gap = pd.Series(ss["gap"], name="gap")
        co = analysis.chain_owned_controls(ss)
        reg = analysis.region_dummies(ss)

        # NJ-dummy models (require only non-missing price in both waves).
        for name, X in [
            ("NJ", nj),
            ("NJ + chain/owned", pd.concat([nj, co], axis=1)),
        ]:
            r = analysis.fit_ols(y, X)
            rows.append(dict(outcome=label, model=name,
                             coef=r.params.get("nj", np.nan),
                             se=r.bse.get("nj", np.nan), n=int(r.nobs)))

        # GAP models (also require a non-missing wave-1 starting wage).
        keep = gap.notna()
        yg, nj_g, gap_g = y[keep], nj[keep], gap[keep]
        co_g, reg_g = co[keep], reg[keep]
        for name, X in [
            ("GAP", gap_g),
            ("GAP + chain/owned", pd.concat([gap_g, co_g], axis=1)),
            ("GAP + chain/owned + region", pd.concat([gap_g, co_g, reg_g], axis=1)),
        ]:
            r = analysis.fit_ols(yg, X)
            rows.append(dict(outcome=label, model=name,
                             coef=r.params.get("gap", np.nan),
                             se=r.bse.get("gap", np.nan), n=int(r.nobs)))

    out = pd.DataFrame(rows)
    config.TABLES_DIR.mkdir(parents=True, exist_ok=True)
    path = config.TABLES_DIR / "extension_price_did_regressions.csv"
    out.round(4).to_csv(path, index=False)
    print(f"[extension] wrote {path}")
    return out


def price_pass_through(df):
    """Run the price pass-through extension and return its two result tables."""
    means = _did_means(df)
    regs = _did_regressions(df)
    return means, regs
