"""Generate simple linear-regression samples."""
import numpy as np
from src.config import TRUE_BETA, INTERCEPT


def generate_sample(n: int, error_type: str, rng: np.random.Generator):
    if n < 4:
        raise ValueError("sample size must be at least 4")
    x = rng.normal(size=n)
    if error_type == "normal":
        eps = rng.normal(size=n)
    elif error_type == "heavy_tail":
        eps = rng.standard_t(df=3, size=n) / np.sqrt(3)  # Var(t_3)=3
    elif error_type == "heteroskedastic":
        eps = rng.normal(size=n) * np.sqrt(0.5 + x*x) / np.sqrt(1.5)
    else:
        raise ValueError(f"Unknown error distribution: {error_type}")
    y = INTERCEPT + TRUE_BETA*x + eps
    return x, y
