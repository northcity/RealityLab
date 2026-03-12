from pathlib import Path

from reality_detector.cli import build_parser, main


def test_build_parser_accepts_collect_subcommand() -> None:
    parser = build_parser()
    args = parser.parse_args(["collect", "--source", "clock", "--samples", "20"])

    assert args.command == "collect"
    assert args.source == "clock"
    assert args.samples == 20


def test_legacy_mode_still_works(tmp_path: Path, monkeypatch) -> None:
    csv_path = tmp_path / "simple.csv"
    csv_path.write_text("i,value\n1,1\n2,2\n3,3\n", encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["reality-detector", str(csv_path), "--column", "value"])
    exit_code = main()

    assert exit_code == 0
