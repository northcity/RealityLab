#!/usr/bin/env python3
"""
RealityLab — Interactive Demo
==============================

五组对比实验，展示检测器如何区分"自然数据"和"人工/模拟数据"。

运行: python examples/demo_interactive.py
"""

import math
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from reality_detector import RealityAnomalyDetector


def print_header(title: str) -> None:
    width = 60
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)


def print_report(label: str, data: list) -> None:
    report = RealityAnomalyDetector(data).analyze()
    d = report.to_dict()
    print(f"\n  [{label}]")
    print(f"    样本数: {d['sample_count']}")
    print(f"    熵 (entropy):         {d['entropy']:.4f}")
    print(f"    自相关 (autocorr):     {d['autocorrelation_lag1']:.4f}")
    print(f"    量化评分 (discrete):   {d['discretization_score']:.4f}")
    print(f"    游程偏差 (run-len):    {d['run_length_deviation']:.4f}")
    print(f"    异常评分: {d['anomaly_score']}/4")
    print(f"    解读: {d['interpretation']}")
    return report


def experiment_1():
    """实验1: 真随机 vs 假随机"""
    print_header("实验 1: 真随机 vs 假随机")
    print("  真随机: random.random() 生成 500 个浮点数")
    print("  假随机: 固定步长 0→1→2→...→499 (太规则)")

    real_random = [random.random() * 100 for _ in range(500)]
    fake_random = [i % 50 for i in range(500)]

    print_report("真随机数据", real_random)
    print_report("假随机数据 (固定步长循环)", fake_random)


def experiment_2():
    """实验2: 自然温度 vs 量化温度"""
    print_header("实验 2: 自然温度序列 vs 量化温度序列")
    print("  自然: 模拟 24 小时温度，带高斯噪声")
    print("  量化: 所有温度四舍五入到最近的 5 度")

    natural_temp = []
    quantized_temp = []
    for hour in range(200):
        t = 20 + 8 * math.sin(hour / 24 * 2 * math.pi) + random.gauss(0, 1.5)
        natural_temp.append(round(t, 2))
        quantized_temp.append(round(t / 5) * 5)

    print_report("自然温度", natural_temp)
    print_report("量化温度 (5度步长)", quantized_temp)


def experiment_3():
    """实验3: 自然心跳间隔 vs 机械心跳"""
    print_header("实验 3: 自然心跳间隔 vs 机械时钟")
    print("  自然: 模拟心跳 R-R 间隔 (约 800ms ± 随机变化)")
    print("  机械: 精确的 800ms 间隔 (完全无变化)")

    natural_heartbeat = [800 + random.gauss(0, 50) for _ in range(300)]
    mechanical_clock = [800.0] * 300

    print_report("自然心跳间隔", natural_heartbeat)
    print_report("机械时钟间隔", mechanical_clock)


def experiment_4():
    """实验4: 模拟果蝇神经元放电 (自然 vs 模拟)"""
    print_header("实验 4: 模拟果蝇神经元放电模式")
    print("  背景: 2024年科学家完成了果蝇大脑 139,255 个神经元的完整连接组图谱，")
    print("  并在计算机中模拟了它的神经活动。")
    print()
    print("  自然放电: 泊松过程 + 突触权重噪声 (像真实神经元)")
    print("  模拟放电: 固定频率 + 少量均匀噪声 (像低精度模拟)")

    # 模拟自然放电: 泊松间隔 + 幅度噪声
    natural_spikes = []
    t = 0
    for _ in range(500):
        interval = random.expovariate(1 / 20)  # 泊松过程，平均 20ms 间隔
        t += interval
        amplitude = 70 + random.gauss(0, 15)  # 幅度有自然变化
        natural_spikes.append(round(amplitude, 2))

    # 模拟低精度模拟: 固定基础 + 均匀量化噪声
    simulated_spikes = []
    for _ in range(500):
        base = 70
        noise = round(random.uniform(-10, 10) * 2) / 2  # 0.5 步长量化
        simulated_spikes.append(base + noise)

    print_report("自然神经放电幅度", natural_spikes)
    print_report("模拟神经放电幅度 (低精度)", simulated_spikes)


def experiment_5():
    """实验5: 股市收益 vs 程序化交易"""
    print_header("实验 5: 自然市场行为 vs 程序化交易痕迹")
    print("  自然: 模拟股市日收益率 (正态分布 + 偶尔极端值)")
    print("  程序: 自动交易产生的固定模式 (每 5 步重复)")

    natural_returns = []
    for _ in range(400):
        r = random.gauss(0, 0.02)
        # 偶尔极端事件 (fat tail)
        if random.random() < 0.05:
            r *= random.choice([3, 4, 5])
        natural_returns.append(round(r, 6))

    pattern = [0.01, -0.005, 0.008, -0.003, 0.002]
    algo_returns = []
    for i in range(400):
        algo_returns.append(pattern[i % 5] + random.gauss(0, 0.001))

    print_report("自然市场收益率", natural_returns)
    print_report("程序化交易收益率", algo_returns)


def main():
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║         RealityLab — 现实异常检测器演示                    ║")
    print("║                                                          ║")
    print("║  这个工具检测数据中是否存在:                                ║")
    print("║  • 过低的信息熵 (太有规律)                                 ║")
    print("║  • 过强的自相关 (太可预测)                                 ║")
    print("║  • 量化痕迹 (像被网格约束)                                 ║")
    print("║  • 不自然的高低交替模式                                    ║")
    print("╚══════════════════════════════════════════════════════════╝")

    random.seed(42)  # 可重复

    experiment_1()
    experiment_2()
    experiment_3()
    experiment_4()
    experiment_5()

    print()
    print("=" * 60)
    print("  总结")
    print("=" * 60)
    print()
    print("  每组实验中，'人工/模拟' 数据的异常评分通常更高。")
    print("  这说明检测器可以分辨 '自然生成' 和 '人工构造' 的模式差异。")
    print()
    print("  但请注意:")
    print("  • 评分高 ≠ 世界是模拟的")
    print("  • 评分低 ≠ 世界是真实的")
    print("  • 这只是统计分析工具，不是终极答案")
    print()
    print("  果蝇启示: 如果科学家能用电脑模拟果蝇大脑，")
    print("  那模拟更大的系统只是算力问题，不是原理问题。")
    print("  这个工具的意义在于: 如果我们身处模拟之中，")
    print("  模拟本身可能存在'精度不够'的漏洞 — 而这些漏洞")
    print("  在统计层面上是有可能被检测到的。")
    print()


if __name__ == "__main__":
    main()
