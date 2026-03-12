# RealityLab

<p align="center">
  <img src="social-preview.png" alt="RealityLab" width="720" />
</p>

<p align="center">
  <a href="https://github.com/northcity/RealityLab/actions/workflows/ci.yml"><img src="https://github.com/northcity/RealityLab/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/dependencies-zero-brightgreen" alt="Dependencies">
  <img src="https://img.shields.io/github/stars/northcity/RealityLab?style=social" alt="Stars">
</p>

<p align="center"><b>Test strange patterns, not metaphysics.</b></p>

---

A tiny, **zero-dependency** Python library and CLI for spotting unusual statistical structure in time-series data.

> This project does **not** prove whether the world is real or simulated.
> It only helps detect suspicious regularity, quantization, and temporal structure in observed data.

## Why this exists | 为什么做这个

The original idea started as a thought experiment:

- Can we look for signs of excessive regularity?
- Can we detect quantized or grid-like behavior in data?
- Can we score unusual sequential patterns without overclaiming?

这个库的灵感来自一个"如果世界是模拟的，我们能不能用数据检测出来"的思想实验。
当然，它**不能**证明任何关于世界本质的东西。但它可以帮你快速检测数据里不寻常的统计结构。

## Use cases | 使用场景

- Analyze recorded sensor data / 检测传感器数据异常
- Inspect latency or timing traces / 分析网络延迟序列
- Compare synthetic vs natural-looking sequences / 区分人工和自然序列
- Build weird but fun demos for blogs, talks, or social posts / 做有趣的数据实验

## Features | 功能特性

| Feature | Description |
|---------|-------------|
| Shannon entropy | Measures information density in the sequence |
| Autocorrelation | Detects temporal dependencies between adjacent values |
| Discretization score | Finds quantization / grid-like step patterns |
| Run-length deviation | Checks if high/low runs are unnaturally regular |
| CSV loader | Load any CSV with a numeric column |
| CLI | One-command analysis from terminal |
| Zero dependencies | Pure Python standard library |

## Install | 安装

```bash
pip install .
```

## Quick start | 快速上手

### Python API

```python
from reality_detector import RealityAnomalyDetector

data = [1, 4, 2, 7, 5, 9, 3, 6]
report = RealityAnomalyDetector(data).analyze()
print(report.to_dict())
```

### CLI

```bash
# Text report
reality-detector examples/demo.csv --column value

# JSON output
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

## What the score means | 评分含义

| Score | Meaning |
|-------|---------|
| 0 | No obvious anomaly / 未发现异常 |
| 1 | Mild anomaly, likely normal variation / 轻微异常，很可能是正常波动 |
| 2 | Notable anomaly, collect more data / 值得注意，建议增加样本 |
| 3-4 | Strong anomaly signal, but still not proof of simulation / 异常较强，但仍不能证明是模拟 |

## Project structure

```text
RealityLab/
├── src/reality_detector/   # Core library
│   ├── core.py             # Detector & report
│   ├── io.py               # CSV loader
│   └── cli.py              # CLI entry point
├── tests/                  # Test suite
├── examples/               # Demo CSV data
├── scripts/                # Image generation helpers
└── .github/workflows/      # CI pipeline
```

## Roadmap | 路线图

- [ ] JSON and NDJSON input support
- [ ] Visualization helpers (matplotlib / plotly)
- [ ] FFT-based periodicity checks
- [ ] Chi-squared and Kolmogorov-Smirnov tests
- [ ] Benchmark dataset bundle
- [ ] PyPI release

## Contributing | 贡献

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[MIT](LICENSE)

---

<p align="center">
  <sub>Made with curiosity. Star this repo if you find the idea intriguing.</sub><br>
  <sub>如果觉得有趣，欢迎点一颗星。</sub>
</p>

## License

MIT
