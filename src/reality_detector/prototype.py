from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict

from .collector import collect_clock_jitter, collect_ping_latency, save_series_to_csv
from .core import RealityAnomalyDetector


@dataclass
class PrototypeResult:
    timestamp: str
    clock_data_file: str
    ping_data_file: str
    clock_report: Dict[str, object]
    ping_report: Dict[str, object]
    reference_report: Dict[str, object]

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


def run_prototype(output_dir: Path) -> PrototypeResult:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    clock_series = collect_clock_jitter(samples=300, interval_ms=10.0)
    ping_series = collect_ping_latency(host="1.1.1.1", samples=25, interval_seconds=0.2)

    reference_series = [
        0.0,
        10.0,
        0.0,
        10.0,
        0.0,
        10.0,
        0.0,
        10.0,
        0.0,
        10.0,
        0.0,
        10.0,
    ]

    clock_path = output_dir / f"clock_jitter_{stamp}.csv"
    ping_path = output_dir / f"ping_latency_{stamp}.csv"

    save_series_to_csv(clock_path, clock_series, column_name="jitter_ms")
    save_series_to_csv(ping_path, ping_series, column_name="latency_ms")

    clock_report = RealityAnomalyDetector(clock_series).analyze().to_dict()
    ping_report = RealityAnomalyDetector(ping_series).analyze().to_dict()
    reference_report = RealityAnomalyDetector(reference_series).analyze().to_dict()

    result = PrototypeResult(
        timestamp=stamp,
        clock_data_file=str(clock_path),
        ping_data_file=str(ping_path),
        clock_report=clock_report,
        ping_report=ping_report,
        reference_report=reference_report,
    )

    report_path = output_dir / f"prototype_report_{stamp}.json"
    report_path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    return result
