"""Publication figure and Monte Carlo diagnostic."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.config import SAMPLE_SIZES, ERROR_TYPES, METHODS, TRUE_BETA

LABELS = {"normal": "Normal errors", "heavy_tail": "Heavy-tailed t(3)",
          "heteroskedastic": "Heteroskedastic errors",
          "conventional": "Conventional OLS", "hc3": "OLS + HC3"}


def make_figures(raw, summary, output_dir):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    # Diagnostic: sampling distribution; unique data per repetition, duplicate estimates across methods omitted.
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4), sharex=True, sharey=True)
    for ax, typ in zip(axes, ERROR_TYPES):
        for n in SAMPLE_SIZES:
            vals = raw.loc[(raw.error_type==typ)&(raw.n==n)&(raw.method=="conventional"), "estimate"]
            ax.hist(vals, bins=np.linspace(-0.3, 2.3, 55), alpha=0.36, density=True, label=f"n={n}")
        ax.axvline(TRUE_BETA, color="black", linestyle="--", linewidth=1.5, label="True slope")
        ax.set_title(LABELS[typ]); ax.set_xlabel("Estimated slope")
    axes[0].set_ylabel("Density")
    axes[-1].legend(fontsize=8)
    fig.suptitle("Diagnostic: Monte Carlo distribution of OLS slope estimates", fontsize=12)
    fig.tight_layout()
    fig.savefig(out/"diagnostic_sampling_distribution.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.4), sharey=True)
    for ax, typ in zip(axes, ERROR_TYPES):
        for method, marker in [("conventional", "o"), ("hc3", "s")]:
            g = summary.loc[(summary.error_type==typ)&(summary.method==method)].sort_values("n")
            x = g.n.to_numpy()
            y = g.coverage.to_numpy()
            e = 1.96*g.coverage_mcse.to_numpy()
            ax.errorbar(x, y, yerr=e, marker=marker, linewidth=1.7, capsize=4, label=LABELS[method])
        ax.axhline(0.95, linestyle="--", color="black", linewidth=1, label="Nominal 95%")
        ax.set_title(LABELS[typ]); ax.set_xlabel("Sample size")
        ax.set_xticks(SAMPLE_SIZES)
        ax.set_ylim(0.68, 1.01)
        ax.grid(alpha=.2)
    axes[0].set_ylabel("Empirical 95% interval coverage")
    axes[-1].legend(loc="lower right", fontsize=8)
    fig.suptitle("95% confidence-interval coverage by error type and sample size\nError bars: ±1.96 Monte Carlo standard errors", fontsize=12)
    fig.tight_layout()
    fig.savefig(out/"coverage_comparison.png", dpi=200, bbox_inches="tight")
    fig.savefig(out/"coverage_comparison.pdf", bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", default="results/raw/simulation.csv")
    parser.add_argument("--summary", default="results/summary.csv")
    parser.add_argument("--out", default="results/figures")
    args = parser.parse_args()
    make_figures(pd.read_csv(args.raw), pd.read_csv(args.summary), args.out)
    print("Saved diagnostic and publication figures to", args.out)


if __name__ == "__main__":
    main()
