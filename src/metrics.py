"""Summarize Monte Carlo operating characteristics."""
import numpy as np
import pandas as pd
from src.config import TRUE_BETA, ALPHA


def summarize(raw: pd.DataFrame, truth=TRUE_BETA):
    rows = []
    for (n, distribution, method), g in raw.groupby(["n", "error_type", "method"], sort=True):
        estimates = g["estimate"].to_numpy()
        covers = ((g["ci_low"] <= truth) & (truth <= g["ci_high"])).to_numpy()
        r = len(g)
        coverage = float(covers.mean())
        rows.append({"n": int(n), "error_type": distribution, "method": method,
            "reps": r, "bias": float(np.mean(estimates - truth)),
            "empirical_sd": float(np.std(estimates, ddof=1)),
            "rmse": float(np.sqrt(np.mean((estimates-truth)**2))),
            "mean_se": float(g["se"].mean()),
            "coverage": coverage,
            "coverage_mcse": float(np.sqrt(coverage*(1-coverage)/r)),
            "mean_ci_width": float((g["ci_high"]-g["ci_low"]).mean())})
    return pd.DataFrame(rows)
