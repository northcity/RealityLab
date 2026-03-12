# Contributing to RealityLab

Thanks for your interest in contributing!

## How to contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b my-feature`
3. Make your changes
4. Run the tests: `python -m pytest`
5. Commit with a clear message: `git commit -m "Add: my feature"`
6. Push and open a pull request

## Development setup

```bash
git clone https://github.com/northcity/RealityLab.git
cd RealityLab
python -m pip install --upgrade pip
pip install -e . pytest
python -m pytest
```

## Code style

- Use type hints
- Keep functions focused and small
- Write docstrings for public API
- No external dependencies in the core library

## Ideas for first contributions

- Add new statistical tests (FFT, chi-squared, K-S test)
- Support JSON / NDJSON input formats
- Add visualization helpers
- Improve documentation and examples
- Add more test cases

## Reporting bugs

Open an issue with:
- Python version
- OS
- Input data (if possible)
- Full error traceback

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
