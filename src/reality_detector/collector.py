from __future__ import annotations

import csv
import re
import subprocess
import time
from pathlib import Path
from typing import List


def collect_clock_jitter(samples: int = 300, interval_ms: float = 10.0) -> List[float]:
    if samples < 10:
        raise ValueError("samples must be >= 10")
    if interval_ms <= 0:
        raise ValueError("interval_ms must be > 0")

    interval_seconds = interval_ms / 1000.0
    target_delta_ms = interval_ms

    series: List[float] = []
    previous = time.perf_counter_ns()

    for _ in range(samples):
        time.sleep(interval_seconds)
        current = time.perf_counter_ns()
        delta_ms = (current - previous) / 1_000_000
        series.append(delta_ms - target_delta_ms)
        previous = current

    return series


def collect_ping_latency(
    host: str = "1.1.1.1", samples: int = 25, interval_seconds: float = 0.2
) -> List[float]:
    if samples < 4:
        raise ValueError("samples must be >= 4")
    if interval_seconds <= 0:
        raise ValueError("interval_seconds must be > 0")

    command = [
        "ping",
        "-n",
        "-c",
        str(samples),
        "-i",
        str(interval_seconds),
        host,
    ]

    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    output = (completed.stdout or "") + "\n" + (completed.stderr or "")

    matches = re.findall(r"time=([0-9]+(?:\.[0-9]+)?)\s*ms", output)
    values = [float(item) for item in matches]

    if len(values) < max(3, samples // 3):
        raise RuntimeError(
            "Unable to collect enough ping latency samples. "
            "Check network access or try another host."
        )

    return values


def save_series_to_csv(path: Path, values: List[float], column_name: str = "value") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", column_name])
        for index, value in enumerate(values, start=1):
            writer.writerow([index, value])
