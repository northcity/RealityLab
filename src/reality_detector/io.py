from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Optional, Union


class CSVInputError(ValueError):
    """Raised when no usable numeric series can be loaded from a CSV file."""


def load_series_from_csv(
    path: Union[str, Path], column: Optional[str] = None
) -> List[float]:
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise CSVInputError("CSV file has no header row")

        rows = list(reader)
        if not rows:
            raise CSVInputError("CSV file is empty")

    target_column = column or _find_first_numeric_column(rows, reader.fieldnames)
    if not target_column:
        raise CSVInputError("No numeric column found in CSV file")

    values: List[float] = []
    for row in rows:
        raw_value = (row.get(target_column) or "").strip()
        if not raw_value:
            continue
        try:
            values.append(float(raw_value))
        except ValueError as exc:
            raise CSVInputError(
                f"Column '{target_column}' contains a non-numeric value: {raw_value}"
            ) from exc

    if not values:
        raise CSVInputError(f"Column '{target_column}' does not contain numeric data")
    return values


def _find_first_numeric_column(
    rows: List[Dict[str, str]], fieldnames: List[str]
) -> Optional[str]:
    for field in fieldnames:
        numeric_found = False
        is_numeric_column = True
        for row in rows:
            raw_value = (row.get(field) or "").strip()
            if not raw_value:
                continue
            try:
                float(raw_value)
                numeric_found = True
            except ValueError:
                is_numeric_column = False
                break
        if is_numeric_column and numeric_found:
            return field
    return None
