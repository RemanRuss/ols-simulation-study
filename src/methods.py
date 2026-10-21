"""OLS confidence intervals using homoskedastic or HC3 standard errors."""
import numpy as np
from scipy.stats import t, norm
from src.config import ALPHA


def estimate(x, y, method="conventional", alpha=ALPHA):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) != len(y) or len(x) < 4 or not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("x and y must have equal length >=4 and be finite")
    X = np.column_stack([np.ones(len(x)), x])
    inv = np.linalg.inv(X.T @ X)
    beta = inv @ X.T @ y
    residual = y - X @ beta
    n = len(x)
    if method == "conventional":
        variance = (residual @ residual) / (n - 2) * inv
        crit = t.ppf(1 - alpha / 2, n - 2)
    elif method == "hc3":
        leverage = np.sum((X @ inv) * X, axis=1)
        adjusted = residual / (1 - leverage)
        variance = inv @ (X.T * adjusted**2) @ X @ inv
        crit = norm.ppf(1 - alpha / 2)
    else:
        raise ValueError(f"Unknown method: {method}")
    se = float(np.sqrt(max(variance[1, 1], 0)))
    return {"estimate": float(beta[1]), "se": se,
            "ci_low": float(beta[1] - crit*se), "ci_high": float(beta[1] + crit*se)}
