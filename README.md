# RealityLab

[![CI](https://github.com/northcity/RealityLab/actions/workflows/ci.yml/badge.svg)](https://github.com/northcity/RealityLab/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

RealityLab is a small, dependency-free Python library and CLI for exploring unusual statistical structure in time-series data.

> Tagline: test strange patterns, not metaphysics.

> This project does **not** prove whether the world is real or simulated.
> It only helps detect suspicious regularity, quantization, and temporal structure in observed data.

Repository: https://github.com/northcity/RealityLab

## Why this exists

The original idea started as a thought experiment:

- Can we look for signs of excessive regularity?
- Can we detect quantized or grid-like behavior in data?
- Can we score unusual sequential patterns without overclaiming?

This library turns that idea into a reusable toolkit.

## Use cases

- Analyze recorded sensor data
- Inspect latency or timing traces
- Compare synthetic vs natural-looking sequences
- Build weird but fun demos for blogs, talks, or social posts

## Features

- Shannon entropy scoring
- Lag-based autocorrelation
- Quantization / discretization score
- Median-based run-length deviation test
- CSV loader for quick experiments
- CLI for local analysis
- Pure standard library, no heavy dependencies

## Install

### Standard install

```bash
pip install .
```

### Editable install

```bash
python -m pip install --upgrade pip
pip install -e .
```

### Run tests

```bash
python -m pytest
```

## Quick start

### Python API

```python
from reality_detector import RealityAnomalyDetector

natural = [1, 4, 2, 7, 5, 9, 3, 6]
report = RealityAnomalyDetector(natural).analyze()
print(report.to_dict())
```

### CLI

```bash
reality-detector examples/demo.csv --column value
```

Or:

```bash
python -m reality_detector examples/demo.csv --column value --json
```

Example output:

```text
Reality Anomaly Detector Report
===============================
Samples: 12
Entropy: 3.5850
Autocorrelation (lag=1): -0.1940
Discretization score: 0.2727
Run-length deviation: 1.0000
Anomaly score: 0/4
Interpretation: No obvious anomaly detected.
```

## CSV format

Any CSV file with at least one numeric column works.

Example:

```csv
step,value
1,10
2,12
3,9
4,14
```

If `--column` is not provided, the CLI picks the first numeric-looking column.

## What the score means

The default score is a lightweight heuristic from 0 to 4:

- `0`: no obvious anomaly
- `1`: mild anomaly, likely normal variation
- `2`: notable anomaly, collect more data
- `3-4`: strong anomaly signal, but still not proof of simulation

## Project structure

```text
reality-anomaly-detector/
├── src/reality_detector/
├── tests/
├── examples/
└── .github/workflows/
```

## Roadmap

- JSON and NDJSON input
- Visualization helpers
- FFT-based periodicity checks
- Better statistical tests
- Benchmark dataset bundle

## GitHub tips

For better discoverability on GitHub, add these repository topics:

- python
- cli
- anomaly-detection
- time-series
- statistics
- simulation-hypothesis
- data-analysis

Suggested repository description:

> A tiny Python library for detecting unusual regularity, quantization, and sequential anomalies in time-series data.

## License

MIT
