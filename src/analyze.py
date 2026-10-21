"""Summarize saved raw simulation results."""
import argparse
from pathlib import Path
import pandas as pd
from src.metrics import summarize


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="results/raw/simulation.csv")
    parser.add_argument("--output", default="results/summary.csv")
    args = parser.parse_args()
    raw = pd.read_csv(args.input)
    summary = summarize(raw)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output, index=False)
    print(summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))


if __name__ == "__main__":
    main()
