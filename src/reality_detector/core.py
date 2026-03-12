from __future__ import annotations

import math
from collections import Counter
from dataclasses import asdict, dataclass
from statistics import StatisticsError, mean, median
from typing import Dict, Iterable, Union


@dataclass
class AnalysisReport:
    sample_count: int
    entropy: float
    autocorrelation_lag1: float
    discretization_score: float
    run_length_deviation: float
    anomaly_score: int
    interpretation: str

    def to_dict(self) -> Dict[str, Union[float, int, str]]:
        return asdict(self)


class RealityAnomalyDetector:
    """Analyze a numeric sequence for lightweight anomaly signals.

    The detector is intentionally conservative. It scores suspicious structure
    in the input series, but it does not claim to prove anything metaphysical.
    """

    def __init__(self, data: Iterable[Union[float, int]]):
        self.data = [float(value) for value in data]
        if not self.data:
            raise ValueError("data must contain at least one numeric sample")

    def shannon_entropy(self) -> float:
        counts = Counter(self.data)
        total = len(self.data)
        entropy = 0.0
        for count in counts.values():
            probability = count / total
            entropy -= probability * math.log2(probability)
        return entropy

    def autocorrelation(self, lag: int = 1) -> float:
        if lag < 1:
            raise ValueError("lag must be >= 1")

        values = self.data
        sample_count = len(values)
        if sample_count <= lag:
            return 0.0

        series_mean = mean(values)
        numerator = sum(
            (values[index] - series_mean) * (values[index - lag] - series_mean)
            for index in range(lag, sample_count)
        )
        denominator = sum((value - series_mean) ** 2 for value in values)
        return numerator / denominator if denominator else 0.0

    def discretization_score(self, precision: int = 6) -> float:
        if len(self.data) < 2:
            return 0.0

        diffs = [
            round(abs(self.data[index] - self.data[index - 1]), precision)
            for index in range(1, len(self.data))
            if self.data[index] != self.data[index - 1]
        ]
        if not diffs:
            return 1.0

        counts = Counter(diffs)
        most_common_count = counts.most_common(1)[0][1]
        return most_common_count / len(diffs)

    def run_length_deviation(self) -> float:
        if len(self.data) < 2:
            return 0.0

        midpoint = median(self.data)
        binary_sequence = [1 if value >= midpoint else 0 for value in self.data]
        if all(bit == binary_sequence[0] for bit in binary_sequence):
            return 0.0

        runs = 1
        for index in range(1, len(binary_sequence)):
            if binary_sequence[index] != binary_sequence[index - 1]:
                runs += 1

        ones = sum(binary_sequence)
        zeroes = len(binary_sequence) - ones
        if ones == 0 or zeroes == 0:
            return 0.0

        expected_runs = ((2 * ones * zeroes) / (ones + zeroes)) + 1
        return abs(runs - expected_runs)

    def analyze(self) -> AnalysisReport:
        entropy = self.shannon_entropy()
        autocorrelation = self.autocorrelation(lag=1)
        discretization = self.discretization_score()
        run_deviation = self.run_length_deviation()

        anomaly_score = 0
        if entropy < self._entropy_threshold():
            anomaly_score += 1
        if abs(autocorrelation) > 0.3:
            anomaly_score += 1
        if discretization > 0.4:
            anomaly_score += 1
        if run_deviation > 10:
            anomaly_score += 1

        return AnalysisReport(
            sample_count=len(self.data),
            entropy=round(entropy, 4),
            autocorrelation_lag1=round(autocorrelation, 4),
            discretization_score=round(discretization, 4),
            run_length_deviation=round(run_deviation, 4),
            anomaly_score=anomaly_score,
            interpretation=self._interpret(anomaly_score),
        )

    def _entropy_threshold(self) -> float:
        try:
            unique_values = len(set(self.data))
            if unique_values <= 1:
                return 0.1
            return min(2.0, math.log2(unique_values) * 0.5)
        except (ValueError, StatisticsError):
            return 2.0

    @staticmethod
    def _interpret(score: int) -> str:
        if score == 0:
            return "No obvious anomaly detected."
        if score == 1:
            return "Mild anomaly detected; likely normal variation."
        if score == 2:
            return "Notable anomaly detected; collect more data."
        return "Strong anomaly signal detected; not proof of simulation."
