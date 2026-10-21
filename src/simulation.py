"""Run experiment with per-replicate deterministic seeds."""
import argparse
import logging
from pathlib import Path
import numpy as np
import pandas as pd
from src.config import SEED, SAMPLE_SIZES, ERROR_TYPES, METHODS, DEFAULT_REPS
from src.dgps import generate_sample
from src.methods import estimate


def simulate(reps=DEFAULT_REPS, seed=SEED):
    rows = []
    for n in SAMPLE_SIZES:
        for error_type in ERROR_TYPES:
            logging.info("Simulating n=%s, error=%s: %s replicates", n, error_type, reps)
            # Same generated dataset is evaluated by both methods: fair paired comparison.
            for rep in range(reps):
                rng = np.random.default_rng(np.random.SeedSequence([seed, n, ERROR_TYPES.index(error_type), rep]))
                x, y = generate_sample(n, error_type, rng)
                for method in METHODS:
                    rows.append({"n": n, "error_type": error_type, "replicate": rep,
                                 "method": method, **estimate(x, y, method)})
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reps", type=int, default=DEFAULT_REPS)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--output", default="results/raw/simulation.csv")
    args = parser.parse_args()
    if args.reps < 2:
        parser.error("--reps must be >= 2")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    results = simulate(args.reps, args.seed)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(out, index=False)
    logging.info("Saved %s method-by-replicate observations to %s", len(results), out)


if __name__ == "__main__":
    main()
