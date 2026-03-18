# pyxDamerauLevenshtein

Cython-based implementation of the Damerau-Levenshtein distance algorithm. The core logic lives entirely in `pyxdameraulevenshtein/_initialize.pyx`.

## Setup

```bash
pip install -r requirements.txt  # Cython
pip install -r dev-requirements.txt  # pytest
CYTHON_TRACE=1 pip install .  # builds the Cython extension in-place (with coverage support)
```

Rebuilding after changes to `_initialize.pyx` requires re-running `CYTHON_TRACE=1 pip install .`.

## Running tests

```bash
pytest tests/
```

## Releasing

Releases are triggered by pushing a tag (e.g. `1.10.0`). The **Publish** GitHub Actions workflow builds wheels for Linux/macOS/Windows across all supported Python versions, creates a GitHub release, and publishes to PyPI.
