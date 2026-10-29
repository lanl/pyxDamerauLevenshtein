# AGENTS.md

This file provides guidance to AI coding agents working with code in this repository.

## Setup

```bash
pip install . --group dev  # builds the Cython extension and installs test + lint tools (requires pip >= 25.1)
```

Build dependencies (setuptools, Cython) are declared in `[build-system]` in `pyproject.toml` and installed automatically during the build. Development dependencies are declared as [PEP 735](https://peps.python.org/pep-0735/) dependency groups in `pyproject.toml`: `test` (pytest), `lint` (ruff), and `dev` (both).

Rebuilding after changes to `_initialize.pyx` requires re-running `pip install .`.

## Running tests

```bash
pytest                                                                                 # all tests
pytest tests/test_pyxdl.py::TestDamerauLevenshteinDistance::test_distance              # one parametrized test
pytest "tests/test_pyxdl.py::TestDamerauLevenshteinDistance::test_distance[unicode]"   # one case
```

Run `pytest` directly, not `python -m pytest`: the latter puts the repository root on `sys.path`, so the uncompiled source directory shadows the installed extension and imports fail.

pytest is configured in `pyproject.toml` with `--strict-markers`, `--strict-config`, and `filterwarnings = error`. The tests include an exhaustive and a seeded-random cross-check against a pure-Python reference implementation (`osa_distance`), and run the docstring examples in `_initialize.pyx` via `doctest`.

## Linting

```bash
ruff check .
ruff format --check .
```

Ruff is configured in `pyproject.toml` (120-character lines, single quotes). Ruff does not understand Cython, so `_initialize.pyx` is not linted; follow the surrounding style there by hand.

## Architecture

All logic lives in a single file: `pyxdameraulevenshtein/_initialize.pyx`. This Cython file is compiled into a C extension and exports four `cpdef` functions:

- `damerau_levenshtein_distance(seq1, seq2, max_distance=None)` — raw edit distance (`int`). Accepts any sequence supporting `len()` and integer indexing (`str`, `bytes`, `list`, `tuple`, `range`, ...); elements are compared with `==`. `max_distance` must be a non-negative integer (`ValueError` if negative, `TypeError` if not an integer). When it is set and the true distance exceeds it, `max_distance + 1` is returned; computation stops early when the length difference alone exceeds it or when an entire DP row exceeds it.
- `normalized_damerau_levenshtein_distance(seq1, seq2)` — distance divided by `max(len(seq1), len(seq2))`, returning a `float` in [0.0, 1.0]. 0.0 = identical, 1.0 = nothing in common. Opposite of `difflib.SequenceMatcher.ratio()`.
- `damerau_levenshtein_distance_seqs(seq, seqs, max_distance=None)` — applies the raw distance function against each element of the iterable `seqs`, returning a list.
- `normalized_damerau_levenshtein_distance_seqs(seq, seqs)` — same but normalized.

`pyxdameraulevenshtein/__init__.py` re-exports the four functions explicitly; users import from `pyxdameraulevenshtein` directly. Type stubs live in `pyxdameraulevenshtein/__init__.pyi` (the package ships `py.typed`) and must be kept in sync with the `.pyx` signatures. `__all__` is defined in `_initialize.pyx`, `__init__.py`, and `__init__.pyi`, and a test asserts the public API is exactly these four functions.

The algorithm is O(N×M) time, O(M) space, using three rolling rows (`two_ago`, `one_ago`, `this_row`) carved out of one `calloc` buffer and rotated by pointer swaps. Each row has one extra slot at index `m` that stores the "column -1" value, so `j - 1`/`j - 2` wrap to it at the left edge. Any common prefix is skipped by index offset (not slicing), and the shorter sequence is always iterated in the outer loop. It implements the **optimal string alignment distance** variant of Damerau-Levenshtein (not the unrestricted DL distance), e.g. `'ca'` vs `'abc'` is 3, not 2.

## Releasing

1. Bump `version` in `pyproject.toml` and add a dated section to `CHANGES.md`.
2. Push a tag matching the version (e.g. `1.11.0`, no `v` prefix).

The **Publish** GitHub Actions workflow then builds wheels with cibuildwheel (configured in `[tool.cibuildwheel]` in `pyproject.toml`; it also runs the test suite against every built wheel) for Linux/macOS/Windows across all supported Python versions, builds the sdist, publishes to PyPI via trusted publishing, and finally creates a GitHub release. PyPI's trusted publisher must be configured for this repository, the `publish.yml` workflow, and the `pypi` environment.

## Supported Python versions

The project supports only CPython versions that are not end-of-life (currently 3.11–3.15). When adding or dropping a version, update all of: `requires-python` and the classifiers in `pyproject.toml`, `target-version` in `[tool.ruff]`, the matrices in `.github/workflows/tests.yml` and `.github/workflows/publish.yml`, the release body in `publish.yml`, `README.md`, and `CHANGES.md`.
