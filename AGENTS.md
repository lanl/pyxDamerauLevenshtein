# AGENTS.md

This file provides guidance to AI coding agents working with code in this repository.

## Setup

```bash
pip install . --group dev  # builds the extension and installs the test, coverage, and lint groups (pip >= 25.1)
```

Dependency groups ([PEP 735](https://peps.python.org/pep-0735/)) live in `pyproject.toml`: `test`, `coverage`, `lint`, and `dev` (all three). Re-run `pip install .` after any change to `_initialize.pyx`; the tests import the installed extension, not the source.

## Running tests

```bash
pytest                                                                                 # all tests
pytest "tests/test_pyxdl.py::TestDamerauLevenshteinDistance::test_distance[unicode]"   # one case
```

Run `pytest`, not `python -m pytest`: the latter puts the repository root on `sys.path`, so the uncompiled source directory shadows the installed extension and the import fails.

pytest runs with `filterwarnings = error`, `--strict-markers`, and `--strict-config`. The suite cross-checks against a pure-Python reference (`osa_distance`) and runs the docstring examples in `_initialize.pyx` via `doctest`, so keep those examples correct.

## Coverage

```bash
pip install --group coverage
PYXDL_COVERAGE=1 python setup.py build_ext --inplace   # traced in-place build
python -m pytest --cov --cov-report=term-missing
```

Here `python -m pytest` is required so that the in-place build is imported. Afterwards, delete `build/`, `pyxdameraulevenshtein/_initialize.c`, and the in-place `.so`/`.pyd` so they don't shadow a normal install.

CI enforces 100% line coverage (the `Cython.Coverage` plugin does not support branch coverage). Don't remove `core = "ctrace"` from `pyproject.toml` or `CYTHON_USE_SYS_MONITORING=0` from `setup.py`: the plugin only works with the C tracer and cannot read `sys.monitoring` events. Lines that can't be exercised or that Cython's tracing never reports (e.g. `free(storage)` in the `finally`) are marked `# pragma: no cover`.

## Linting

```bash
ruff check .
ruff format --check .
```

Ruff (pinned in the `lint` group) also formats Python code blocks inside the Markdown files. It does not process `_initialize.pyx`, so follow that file's style (120-character lines, single quotes) by hand. Every source file, including the stub, starts with the license header as a docstring; new files need it too.

## Architecture

All logic is in `pyxdameraulevenshtein/_initialize.pyx`, which defines four `cpdef` functions: `damerau_levenshtein_distance`, `normalized_damerau_levenshtein_distance`, and their `_seqs` variants. `__init__.py` re-exports them. When changing a signature, also update the stubs in `__init__.pyi` and `__all__` in all three files; `test_exports` asserts the public API is exactly these four names.

- It implements the **optimal string alignment** variant, not unrestricted Damerau-Levenshtein: `'ca'` vs `'abc'` is 3, not 2.
- Inputs can be any sequence supporting `len()` and integer indexing (slicing is not required, so `deque` works); elements are compared with `==`.
- `max_distance` goes through `operator.index` and must be non-negative (`ValueError` if negative, `TypeError` if not an integer). If the distance exceeds it, `max_distance + 1` is returned; a value at or above the longer length means no threshold. The normalized functions deliberately take no `max_distance` (it was removed in 1.10.1).
- Algorithm: the common prefix is skipped by index offset, then the sequences are swapped so that `seq2` is the longer one; the outer loop iterates `seq1`. Three rolling rows of length `m + 1` (`two_ago`, `one_ago`, `this_row`) share one `calloc` buffer and are rotated by pointer swap. Index `m` of each row is the "column -1" sentinel, so `j - 1`/`j - 2` wrap to it at the left edge. It returns early when the length difference, or an entire row's minimum, exceeds the threshold.

## Changelog and releasing

Record user-visible changes in the top section of `CHANGES.md`, marking incompatible ones as `**Behavior change**`. To release:

1. Bump `version` in `pyproject.toml` and date the top section of `CHANGES.md`.
2. Push a tag equal to the version, with no `v` prefix (e.g. `1.11.0`).

Pushing any tag triggers `.github/workflows/publish.yml`, which builds wheels with cibuildwheel (configured in `[tool.cibuildwheel]`; the tests run against every wheel), builds the sdist, publishes to PyPI, and creates the GitHub release. PyPI trusted publishing is tied to the workflow filename `publish.yml` and the environment `pypi`, so don't rename either.

## Supported Python versions

Only non-EOL CPython versions are supported (currently 3.11–3.15). When adding or dropping a version, update:

- `pyproject.toml`: the classifiers, plus `requires-python` and `[tool.ruff] target-version` if the minimum changes
- `.github/workflows/tests.yml`: the test matrix
- `.github/workflows/publish.yml`: the `python` matrix and the version list in the release notes
- `README.md`: "requires Python 3.x+" if the minimum changes
- `CHANGES.md`
- the version range in this file
