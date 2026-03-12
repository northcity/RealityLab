from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .core import RealityAnomalyDetector
from .io import CSVInputError, load_series_from_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reality-detector",
        description="Analyze a numeric series for lightweight anomaly signals.",
    )
    parser.add_argument("input", type=Path, help="Path to a CSV file")
    parser.add_argument(
        "--column",
        help="Column name to analyze. If omitted, the first numeric column is used.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the report as JSON.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        series = load_series_from_csv(args.input, column=args.column)
        report = RealityAnomalyDetector(series).analyze()
    except (FileNotFoundError, CSVInputError, ValueError) as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")

    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(_format_report(report))
    return 0


def _format_report(report: Any) -> str:
    payload = report.to_dict()
    return "\n".join(
        [
            "Reality Anomaly Detector Report",
            "===============================",
            f"Samples: {payload['sample_count']}",
            f"Entropy: {payload['entropy']:.4f}",
            f"Autocorrelation (lag=1): {payload['autocorrelation_lag1']:.4f}",
            f"Discretization score: {payload['discretization_score']:.4f}",
            f"Run-length deviation: {payload['run_length_deviation']:.4f}",
            f"Anomaly score: {payload['anomaly_score']}/4",
            f"Interpretation: {payload['interpretation']}",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
