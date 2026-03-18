# pyxDamerauLevenshtein

Cython-based implementation of the Damerau-Levenshtein distance algorithm. The core logic lives entirely in `pyxdameraulevenshtein/_initialize.pyx`.

## Setup

```bash
pip install -r requirements.txt  # Cython
pip install -r dev-requirements.txt  # pytest
pip install .  # builds the Cython extension in-place
```

Rebuilding after changes to `_initialize.pyx` requires re-running `pip install .`.

## Running tests

```bash
pytest tests/
```

## Releasing

Releases are triggered manually via the **Publish** GitHub Actions workflow. Provide the version number (e.g. `1.10.0`) as input. The workflow builds wheels for Linux/macOS/Windows across all supported Python versions, creates a GitHub release, and publishes to PyPI.
