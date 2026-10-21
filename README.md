# OLS Confidence Interval Simulation Study

A reproducible original simulation study comparing conventional OLS intervals with HC3 heteroskedasticity-robust intervals across normal, heavy-tailed, and heteroskedastic errors, with sample sizes 30, 100, and 500. This is **Option B** of the Unit 2 Project; instructor scope approval may be needed.

## Setup (Windows / macOS / Linux)

Install Python 3.10+ and GNU Make. From the repository root:

```bash
python -m pip install -r requirements.txt
make test
make all
```

On Windows Git Bash with `python` available, run the same commands. If GNU Make is absent, the equivalent steps are:

```bash
python -m src.simulation
python -m src.analyze
python -m src.figures
python -m pytest -q
```

For a quick smoke run, use `make all REPS=20`. **Do not use the quick run for the final analysis**; the default is 2,000 replicates per scenario. Make targets: `all`, `simulate`, `analyze`, `figures`, `test`, `clean`. `make all` re-runs the pipeline from scratch (results are not cached). Runtime depends on hardware and Python libraries; the default typically takes tens of seconds to a few minutes; the exact elapsed runtime on the development system is recorded in `RUN_LOG.md`.

## Outputs

- `results/raw/simulation.csv`: simulation-level estimates, SEs, CIs (saved before analysis).
- `results/summary.csv`: bias, SD, RMSE, mean SE, coverage, MCSE, mean CI width.
- `results/figures/diagnostic_sampling_distribution.png`: diagnostic sampling distributions.
- `results/figures/coverage_comparison.png` and `.pdf`: publication-quality 95% coverage comparison with Monte Carlo uncertainty.
- `ADEMP.md`: design and estimands.
- `ANALYSIS.md`: critical discussion of results.

## Findings

See `ANALYSIS.md` and `results/summary.csv` for the measured findings of the committed run. In principle, HC3 is expected to improve coverage under heteroskedasticity, while it need not improve conventional OLS intervals under homoskedastic normal errors.

## Reproducibility

Fixed base seed: `20261021`. RNG seeds are uniquely derived by condition and replicate. Both interval methods use identical generated data. The software environment is specified in `requirements.txt`, and four categories of automated validation are included under `tests/`. Full results remain under version control unless you decide to exclude them.
