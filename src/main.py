"""Main entry point: run the full replication end-to-end.

Run from the project root with::

    python src/main.py

This loads and validates the data, reproduces Tables 2-4 and Figure 1, runs the
price pass-through extension, and prints a summary comparing key estimates with
the values printed in Card & Krueger (1994).
"""
import sys
from pathlib import Path

# Make sibling modules importable regardless of how the script is invoked.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

import analysis
import config
import extension
import figures
import load_data
import tables

C = config.C

# Key values printed in the paper, used only for validation comparison.
PAPER_TARGETS = {
    "Table 3 DID (level FTE)": 2.76,
    "Table 3 DID t-statistic": 2.03,
    "Table 4 (i) NJ dummy": 2.33, "Table 4 (i) SE": 1.19,
    "Table 4 (ii) NJ dummy": 2.30, "Table 4 (ii) SE": 1.20,
    "Table 4 (iii) GAP": 15.65, "Table 4 (iii) SE": 6.08,
    "Table 4 (iv) GAP": 14.92, "Table 4 (iv) SE": 6.21,
    "Table 4 (v) GAP": 11.91, "Table 4 (v) SE": 7.39,
    "Table 4 sample size": 357,
    "Table 4 mean(dFte)": -0.237,
    "Table 4 sd(dFte)": 8.825,
    "Mean GAP among NJ stores": 0.11,
}


def _wage_group_counts(df):
    wage = df[C["wage_st"]]
    nj = df[C["state"]] == 1
    return {
        "NJ wage=$4.25": int((nj & (wage == 4.25)).sum()),
        "NJ wage=$4.26-$4.99": int((nj & (wage > 4.25) & (wage < 5.00)).sum()),
        "NJ wage>=$5.00": int((nj & (wage >= 5.00)).sum()),
    }


def _print_summary(t3, t4_results, t4_sample):
    """Print key estimates and compare them with the paper's printed values."""
    print("\n" + "=" * 72)
    print("REPLICATION SUMMARY vs. PAPER")
    print("=" * 72)

    # Table 3 DID (NJ-PA), rows 3 and 4.
    did3 = t3.loc[2, "NJ-PA_mean"], t3.loc[2, "NJ-PA_se"]
    did4 = t3.loc[3, "NJ-PA_mean"], t3.loc[3, "NJ-PA_se"]
    print(f"Table 3 DID, row 3 (all available): {did3[0]:.2f} (se {did3[1]:.2f})  "
          f"[paper: 2.76, t=2.03]")
    print(f"Table 3 DID, row 4 (balanced):      {did4[0]:.2f} (se {did4[1]:.2f})")
    print(f"Table 3 DID t (row 3):              {did3[0]/did3[1]:.2f}  [paper: 2.03]")

    # Table 4 coefficients.
    print("\nTable 4 (coef (se)):")
    r = t4_results
    for k, key, paper_c, paper_se in [
        ("i", "nj", 2.33, 1.19), ("ii", "nj", 2.30, 1.20),
        ("iii", "gap", 15.65, 6.08), ("iv", "gap", 14.92, 6.21),
        ("v", "gap", 11.91, 7.39),
    ]:
        got = r[k].params.get(key, np.nan)
        se = r[k].bse.get(key, np.nan)
        print(f"  ({k}) {key}: {got:6.2f} ({se:.2f})   paper: {paper_c:.2f} ({paper_se:.2f})")

    # Sample statistics.
    print(f"\nTable 4 sample: n={t4_sample['n']} [paper: 357], "
          f"mean(dFte)={t4_sample['mean_d_fte']:.3f} [paper: -0.237], "
          f"sd(dFte)={t4_sample['sd_d_fte']:.3f} [paper: 8.825]")
    print(f"Mean GAP among NJ stores: {t4_sample['gap_mean_nj']:.3f}  [paper: 0.11]")


def main():
    # 1. Load and validate the input data.
    df = load_data.load_public_csv()
    df = analysis.add_derived_variables(df)

    # 2. Reproduce Tables 2-4.
    t2 = tables.table2(df)
    t3 = tables.table3(df)
    t4, t4_results, t4_sample = tables.table4(df)

    # 3. Reproduce Figure 1.
    figures.figure1(df)

    # 4. Independent extension: price pass-through.
    ext_means, ext_regs = extension.price_pass_through(df)

    # 5. Print validation summary.
    print(f"\nNJ wage groups: {_wage_group_counts(df)}  [paper: 101 / 140 / 73]")
    _print_summary(t3, t4_results, t4_sample)

    print("\nAll outputs written to outputs/tables/ and outputs/figures/.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (FileNotFoundError, ValueError) as e:
        print(f"\n[error] {e}", file=sys.stderr)
        sys.exit(1)
