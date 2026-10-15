"""Generate Figure 1: distribution of starting wage rates (NJ vs PA, both waves)."""
import matplotlib
matplotlib.use("Agg")  # headless backend (no display required)
import matplotlib.pyplot as plt
import numpy as np

import config

C = config.C


def _bin_percentages(wage, bins):
    """Return the percentage of non-missing wages falling in each bin.

    ``bins`` are bin edges; returns bin centers and the corresponding counts
    expressed as percentages of the stores with a reported wage.
    """
    w = wage.dropna().to_numpy()
    counts, edges = np.histogram(w, bins=bins)
    pct = 100.0 * counts / len(w) if len(w) else np.zeros(len(counts))
    centers = 0.5 * (edges[:-1] + edges[1:])
    return centers, pct


def figure1(df, path=None):
    """Plot the starting-wage distributions before and after the increase."""
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = path or (config.FIGURES_DIR / "figure1_starting_wage_distribution.png")

    bins = np.arange(4.25, 6.51, 0.25)  # $0.25 wage bins, 4.25..6.50
    width = (bins[1] - bins[0]) * 0.42  # two grouped bars per bin

    nj_mask = df[C["state"]] == 1
    pa_mask = df[C["state"]] == 0

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)

    panels = [
        (0, "Wave 1 — February 1992 (before)", C["wage_st"]),
        (1, "Wave 2 — November 1992 (after)", C["wage_st2"]),
    ]

    for ax_i, title, wage_col in panels:
        ax = axes[ax_i]
        cx, nj_pct = _bin_percentages(df.loc[nj_mask, wage_col], bins)
        _, pa_pct = _bin_percentages(df.loc[pa_mask, wage_col], bins)

        ax.bar(cx - width / 2, nj_pct, width, label="New Jersey",
               color=config.COLOR_NJ, edgecolor="none")
        ax.bar(cx + width / 2, pa_pct, width, label="Pennsylvania",
               color=config.COLOR_PA, edgecolor="none")

        ax.set_title(title, fontsize=11)
        ax.set_xlabel("Starting wage ($/hour)")
        ax.set_xticks(bins)
        ax.set_xticklabels([f"{b:.2f}" for b in bins], rotation=45, ha="right", fontsize=8)
        ax.tick_params(axis="y", labelsize=9)
        ax.grid(axis="y", color=config.GRIDLINE, linewidth=0.7)
        ax.set_axisbelow(True)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)

    axes[0].set_ylabel("% of stores")
    axes[0].legend(frameon=False, loc="upper right", fontsize=9)

    fig.suptitle("Figure 1. Distribution of starting wage rates", fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[figures] wrote {path}")
    return path
