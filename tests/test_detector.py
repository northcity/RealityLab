from pathlib import Path

from reality_detector import RealityAnomalyDetector, load_series_from_csv


def test_analyze_returns_expected_keys() -> None:
    report = RealityAnomalyDetector([1, 2, 3, 4, 5, 6]).analyze().to_dict()

    assert report["sample_count"] == 6
    assert set(report) == {
        "sample_count",
        "entropy",
        "autocorrelation_lag1",
        "discretization_score",
        "run_length_deviation",
        "anomaly_score",
        "interpretation",
    }


def test_quantized_data_scores_higher_than_varied_data() -> None:
    varied = [1, 4, 2, 7, 5, 9, 3, 6, 8, 11]
    quantized = [0, 10, 20, 10, 20, 10, 20, 10, 20, 10]

    varied_score = RealityAnomalyDetector(varied).analyze().anomaly_score
    quantized_score = RealityAnomalyDetector(quantized).analyze().anomaly_score

    assert quantized_score >= varied_score


def test_load_series_from_csv_reads_numeric_column() -> None:
    csv_path = Path(__file__).resolve().parent.parent / "examples" / "demo.csv"
    values = load_series_from_csv(csv_path, column="value")

    assert values[:3] == [10.0, 12.0, 9.0]
    assert len(values) == 12
