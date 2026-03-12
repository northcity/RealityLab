from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .collector import collect_clock_jitter, collect_ping_latency, save_series_to_csv
from .core import RealityAnomalyDetector
from .io import CSVInputError, load_series_from_csv
from .prototype import run_prototype


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reality-detector",
        description="Analyze a numeric series for lightweight anomaly signals.",
    )
    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze a CSV file")
    analyze_parser.add_argument("input", type=Path, help="Path to a CSV file")
    analyze_parser.add_argument(
        "--column",
        help="Column name to analyze. If omitted, the first numeric column is used.",
    )
    analyze_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the report as JSON.",
    )

    collect_parser = subparsers.add_parser(
        "collect", help="Collect local experiment data to CSV"
    )
    collect_parser.add_argument(
        "--source",
        choices=["clock", "ping"],
        default="clock",
        help="Data source to collect",
    )
    collect_parser.add_argument(
        "--samples",
        type=int,
        default=200,
        help="Number of samples to collect",
    )
    collect_parser.add_argument(
        "--output",
        type=Path,
        default=Path("data") / "collected.csv",
        help="Output CSV path",
    )
    collect_parser.add_argument(
        "--host",
        default="1.1.1.1",
        help="Ping host when source=ping",
    )

    prototype_parser = subparsers.add_parser(
        "prototype",
        help="Run an end-to-end prototype (collect + analyze + compare)",
    )
    prototype_parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data") / "prototype_runs",
        help="Directory to write collected data and report",
    )
    prototype_parser.add_argument(
        "--json",
        action="store_true",
        help="Print prototype result as JSON",
    )

    return parser


def main() -> int:
    parser = build_parser()
    argv = sys.argv[1:]

    if argv and argv[0] not in {"analyze", "collect", "prototype", "-h", "--help"}:
        argv = ["analyze"] + argv

    args = parser.parse_args(argv)

    if args.command == "collect":
        return _run_collect(args)

    if args.command == "prototype":
        return _run_prototype(args)

    return _run_analyze(args, parser)


def _run_analyze(args: Any, parser: argparse.ArgumentParser) -> int:
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


def _run_collect(args: Any) -> int:
    if args.source == "clock":
        values = collect_clock_jitter(samples=args.samples, interval_ms=10.0)
        column = "jitter_ms"
    else:
        values = collect_ping_latency(host=args.host, samples=args.samples, interval_seconds=0.2)
        column = "latency_ms"

    save_series_to_csv(args.output, values, column_name=column)
    print(f"Collected {len(values)} samples from {args.source} and saved to {args.output}")
    return 0


def _run_prototype(args: Any) -> int:
    result = run_prototype(args.output_dir)
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(_format_prototype_result(result.to_dict()))
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


def _format_prototype_result(payload: Any) -> str:
    return "\n".join(
        [
            "Reality Prototype Result",
            "========================",
            f"Timestamp: {payload['timestamp']}",
            f"Clock data: {payload['clock_data_file']}",
            f"Ping data: {payload['ping_data_file']}",
            f"Clock anomaly score: {payload['clock_report']['anomaly_score']}/4",
            f"Ping anomaly score: {payload['ping_report']['anomaly_score']}/4",
            f"Reference (toy simulated) score: {payload['reference_report']['anomaly_score']}/4",
            "Interpretation: compare real-world samples vs toy simulated samples; higher score means more structural regularity.",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
