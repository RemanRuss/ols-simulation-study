# Verification log

- Experiment: 9 simulation scenarios × 2,000 independent replicates = 18,000 generated datasets; 36,000 method-level output rows.
- Seed: 20261021.
- Smoke and correctness suite: `python -m pytest -q` — **5 passed**.
- Full simulation command: `python -m src.simulation --reps 2000` — completed successfully, elapsed wall time **10.43 seconds** on the creation environment, excluding analysis and plotting.
- Summary command: `python -m src.analyze` — completed successfully.
- Plot command: `python -m src.figures` — completed successfully.
- Files generated: `results/raw/simulation.csv`, `results/summary.csv`, and three figure files.
