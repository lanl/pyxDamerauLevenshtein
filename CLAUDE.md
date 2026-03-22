# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
pip install -r requirements.txt    # Cython
pip install -r dev-requirements.txt  # pytest, pytest-cov
pip install .                        # builds the Cython extension
```

Rebuilding after changes to `_initialize.pyx` requires re-running `pip install .`.

## Running tests

```bash
pytest tests/                        # all tests
pytest tests/test_pyxdl.py::TestDamerauLevenshtein::test_damerau_levenshtein_distance  # single test
```

Coverage runs automatically via `pytest-cov`. Note that `_initialize.pyx` does not appear in coverage reports — `Cython.Coverage` is incompatible with coverage 7.x on Python 3.12+.

## Architecture

All logic lives in a single file: `pyxdameraulevenshtein/_initialize.pyx`. This Cython file is compiled into a C extension and exports four `cpdef` functions:

- `damerau_levenshtein_distance(seq1, seq2, max_distance=None)` — raw edit distance (integer). Accepts any sequence type (str, list, tuple, range). When `max_distance` is set and the true distance exceeds it, returns `max_distance + 1` immediately via row-level early termination.
- `normalized_damerau_levenshtein_distance(seq1, seq2)` — distance divided by `max(len(seq1), len(seq2))`, returning a float in [0.0, 1.0]. 0.0 = identical, 1.0 = nothing in common. Opposite of `difflib.SequenceMatcher.ratio()`.
- `damerau_levenshtein_distance_seqs(seq, seqs, max_distance=None)` — applies the raw distance function against each element in `seqs`, returning a list.
- `normalized_damerau_levenshtein_distance_seqs(seq, seqs)` — same but normalized.

`pyxdameraulevenshtein/__init__.py` re-exports everything via `from pyxdameraulevenshtein._initialize import *`. Users import from `pyxdameraulevenshtein` directly.

The algorithm is O(N×M) time, O(M) space, using a rolling 3-row array (`TWO_AGO`, `ONE_AGO`, `THIS_ROW`) allocated with `calloc`. It implements the **optimal string alignment distance** variant of Damerau-Levenshtein (not the full DL distance).

## Releasing

Releases are triggered by pushing a tag (e.g. `1.10.0`). The **Publish** GitHub Actions workflow builds wheels for Linux/macOS/Windows across all supported Python versions, creates a GitHub release, and publishes to PyPI.
