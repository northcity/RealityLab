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

## The Fruit Fly Argument | 果蝇的启示

In 2024, scientists completed the **full connectome of a fruit fly brain** — all 139,255 neurons and 54.5 million synaptic connections — and successfully simulated its neural activity in a computer ([Nature, 2024](https://www.nature.com/articles/s41586-024-07558-y)).

This means:

1. **Biological brains can be digitized.** If a fruit fly brain can be fully mapped and run as software, the gap between "biology" and "simulation" is not a wall — it's a scale problem.
2. **Simulating larger brains is a matter of compute, not principle.** A mouse brain has ~70 million neurons. A human brain has ~86 billion. The architecture is similar; we just need more power.
3. **If a simulation can produce real behavior, how would the simulated entity know?** The simulated fruit fly responds to stimuli just like a real one. From the inside, there may be no difference.

This doesn't *prove* we live in a simulation. But it removes the strongest objection: "you can't simulate a brain." We already can.

**What RealityLab does:** if a simulation has finite precision — quantized time steps, grid-snapped values, or deterministic pseudo-randomness — those artifacts might leak into observable data. This library looks for exactly those patterns.

> 2024 年科学家完成了果蝇大脑全部 139,255 个神经元、5450 万个突触连接的完整图谱，并在计算机中成功模拟了其神经活动。
>
> 这意味着：生物大脑**可以**被数字化运行。模拟更大的大脑只是算力问题，不是原理问题。
> 如果模拟能够产生和真实一样的行为，被模拟的对象从内部可能根本无法区分。
>
> RealityLab 的逻辑是：如果模拟存在有限精度（量化时间步、网格化数值、伪随机数），这些痕迹可能会泄露到可观测数据中。这个库就是用来寻找这些痕迹的。

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

### Interactive demo | 完整演示

```bash
python examples/demo_interactive.py
```

Runs 5 experiments comparing natural vs artificial data: random numbers, temperature, heartbeat, neuron spikes, and stock returns.

运行 5 组对比实验（真随机 vs 假随机、自然温度 vs 量化温度、心跳 vs 时钟、神经放电、股市收益），直观展示检测器的区分能力。

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

## Example datasets | 示例数据

| File | Description |
|------|-------------|
| `examples/demo.csv` | Basic numeric series |
| `examples/temperature.csv` | Natural vs quantized temperature |
| `examples/neuron_spikes.csv` | Natural vs simulated neuron firing |
| `examples/demo_interactive.py` | Full 5-experiment comparison script |

## Project structure

```text
RealityLab/
├── src/reality_detector/   # Core library
│   ├── core.py             # Detector & report
│   ├── io.py               # CSV loader
│   └── cli.py              # CLI entry point
├── tests/                  # Test suite
├── examples/               # Demo data & interactive script
├── scripts/                # Image generation helpers
└── .github/workflows/      # CI + PyPI publish
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
