# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-03-12

### Added

- Core `RealityAnomalyDetector` class with four analysis methods:
  - Shannon entropy
  - Autocorrelation (configurable lag)
  - Discretization score
  - Run-length deviation
- `AnalysisReport` dataclass with `to_dict()` serialization
- CSV loader (`load_series_from_csv`) with auto column detection
- CLI entry point (`reality-detector`) with text and JSON output
- `python -m reality_detector` support
- Example CSV dataset
- GitHub Actions CI (Python 3.9 – 3.12)
- MIT license
