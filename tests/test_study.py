import numpy as np
import pytest
from src.dgps import generate_sample
from src.methods import estimate
from src.metrics import summarize
from src.simulation import simulate


def test_dgp_has_correct_mean_slope():
    rng = np.random.default_rng(7)
    x, y = generate_sample(100000, "normal", rng)
    assert abs(np.cov(x, y)[0, 1] / np.var(x, ddof=1) - 1) < 0.02


def test_exact_linear_relationship_recovers_slope():
    x = np.linspace(-2, 2, 30)
    result = estimate(x, 0.5 + 1.0*x)
    assert result["estimate"] == pytest.approx(1.0, abs=1e-12)
    assert result["ci_low"] <= 1 + 1e-12 and result["ci_high"] >= 1 - 1e-12


def test_seed_reproducibility():
    a = simulate(reps=3, seed=123)
    b = simulate(reps=3, seed=123)
    assert a.equals(b)


def test_coverage_ranges_and_pairing():
    raw = simulate(reps=5, seed=44)
    s = summarize(raw)
    assert s.coverage.between(0, 1).all()
    assert (s.coverage_mcse >= 0).all()
    assert s.shape[0] == 18
    a = raw[raw.method=="conventional"].sort_values(["n", "error_type", "replicate"])
    b = raw[raw.method=="hc3"].sort_values(["n", "error_type", "replicate"])
    assert np.allclose(a.estimate.to_numpy(), b.estimate.to_numpy())


def test_unknown_dgp_rejected():
    with pytest.raises(ValueError):
        generate_sample(30, "incorrect", np.random.default_rng(2))
