# Changes

## 1.11.0 (2026-10-29)
* Drop Python 3.9 and 3.10 support (EOL).
* Add Python 3.15 support.
* **Behavior change**: a negative `max_distance` now raises `ValueError` (previously `OverflowError`), and a non-integer `max_distance` (e.g., `1.5`) now raises `TypeError` (previously it was silently truncated). Any object implementing `__index__` is accepted, and arbitrarily large values are treated as no threshold (previously values that didn't fit in a C `unsigned long`, i.e., 2**32 or more on Windows, raised `OverflowError`).
* `damerau_levenshtein_distance` is roughly 2–3x faster: the inner loop now uses C integer arithmetic, rows are rotated by pointer swaps instead of copies, and `max_distance` short-circuits immediately when the length difference alone exceeds it.
* The common prefix is now skipped by index offset rather than slicing, so sequences that support indexing but not slicing (e.g., `collections.deque`) work.
* Widen the `seqs` type stub to `Iterable[Sequence[Any]]` (generators were already accepted), add `__all__`, and replace the star import in `__init__.py` with explicit imports.
* Publish Linux aarch64 wheels (manylinux and musllinux).
* Use PEP 639 license metadata (`license = "BSD-3-Clause"`); require `setuptools>=77` and `Cython>=3.1` to build.
* Replace `requirements.txt` and `dev-requirements.txt` with PEP 735 dependency groups (`test`, `lint`, `dev`); drop `pytest-cov`, which could not measure the compiled extension.
* Rewrite the test suite as parametrized pytest tests, including exhaustive and seeded-random cross-checks against a pure-Python reference implementation and the docstring examples.
* Add ruff linting and formatting, enforced in CI.
* Modernize GitHub Actions: pin all actions to commit SHAs, update cibuildwheel to v4.3.5, move cibuildwheel configuration into `pyproject.toml`, run tests on Linux, macOS and Windows, publish to PyPI before creating the GitHub release, and add Dependabot for action updates.
* Fix README description of normalization (`max(len(seq1), len(seq2))`) and the `max_distance` example.
* Replace `CLAUDE.md` with a tool-agnostic `AGENTS.md`.

## 1.10.1 (2026-03-19)
* Remove `max_distance` parameter from `normalized_damerau_levenshtein_distance` and `normalized_damerau_levenshtein_distance_seqs`. The parameter was a leaky abstraction: the return value when the threshold was exceeded was neither a consistent sentinel nor the true normalized distance, and varied with sequence length.

## 1.10.0 (2026-03-17)
* Add `max_distance` parameter to all four functions. When provided, computation terminates early and `max_distance + 1` (or a value greater than `max_distance` for normalized functions) is returned if the true distance exceeds the threshold. Closes #16.
* **Note**: normalized distance functions now return a 64-bit `float` (Python's native `float`) instead of a 32-bit C float. Return values are now more precise (e.g., `0.2` instead of `0.20000000298023224`). Code that relies on exact float32 values may need to be updated.
* Raise `TypeError` with a clear message when `None` is passed as an input sequence; previously, `None` inputs were not explicitly handled.
* Update type stubs (`__init__.pyi`) with modern typing syntax and `max_distance` parameters.
* Migrate CI from Travis CI to GitHub Actions.
* Modernize `pyproject.toml` with full PEP 621 metadata.
* Add Python 3.14 support.

## 1.9.0 (2025-07-29)
* Add Python wheel support (#8). (courtesy @jianlins)
* Drop Python 3.8 support.

## 1.8.0 (2024-05-02)
* Add Cython to the build process to reduce the likelihood of incompatabilities between the Cython-generated C code and CPython (#38). (courtesy @tacaswell)
* Drop Python 3.7 support.
* Add Python 3.11-3.13 support.

## 1.7.1 (2022-08-01)

* Drop Python 3.6 support (EOL).
* Add Python 3.10 support.
* Compiled with Cython 0.29.32.
* Updating project URL (moved from [@gfairchild](https://github.com/gfairchild)'s personal namespace to [@lanl](https://github.com/lanl)'s namespace).

## 1.7.0 (2021-02-09)

* Remove NumPy dependency to simplify build process. Rather than relying on `np.ndarray`, we'll now use native iterables like `list` or `tuple`.
    * **This is a breaking change if you currently rely on either of the `*_ndarray` methods.**
        * `damerau_levenshtein_distance_ndarray` refactored to `damerau_levenshtein_distance_seqs`, and the return value is now a `list` rather than `np.array`
        * `normalized_damerau_levenshtein_distance_ndarray` refactored to `normalized_damerau_levenshtein_distance_seqs`, and the return value is now a `list` rather than `np.array`
    * The simplest way to migrate to these new methods is to switch to using a native Python `list`. For example:
        * `damerau_levenshtein_distance_ndarray('test', np.array(['test1', 't1', 'test']))` is now `damerau_levenshtein_distance_seqs('test', ['test1', 't1', 'test'])`
        * `normalized_damerau_levenshtein_distance_ndarray('test', np.array(['test1', 't1', 'test']))` is now `normalized_damerau_levenshtein_distance_seqs('test', ['test1', 't1', 'test'])`
        * If you need the return value to be an `np.array`, then you can simply wrap the return value (a `list`) with `np.array` like so:
            * `np.array(damerau_levenshtein_distance_seqs('test', ['test1', 't1', 'test']))`
* Compiled with Cython 0.29.21.

## 1.6.2 (2021-02-08)

* Remove Python 2 and 3.5 support (they are EOL).
* Bump minimum NumPy version to 1.19.5.
* Add Python 3.9 support in `setup.py`.
* Compiled with Cython 0.29.21.

## 1.6.1 (2020-07-27)

* Fixed bug when first string is longer than the second string (#22). (courtesy @svenski)
* Compiled with Cython 0.29.21.
* Dropping Python 3.4 support from Travis.

## 1.6.0 (2020-05-01)

* Allow `np.ndarrays` as input.
* Add support for Python 3.8 to `setup.py`.
* Compiled with Cython 0.29.17.

## 1.5.3 (2019-02-25)

* Specifying minimum version numbers in `pyproject.toml` and `setup.py`.
* Compiled with Cython 0.29.5.

## 1.5.2 (2019-01-07)

* Using the `pyproject.toml` standard set forth in [PEP 518](https://www.python.org/dev/peps/pep-0518/), NumPy will now be correctly installed as a dependency prior to running `setup.py`.

## 1.5.1 (2019-01-04)

* Fixing NumPy-related install error. (courtesy @simobasso)
* Enabling Python 3.7 unit tests in Travis.
* Compiled with Cython 0.29.2.

## 1.5.0 (2018-02-04)

* Allow tuples and lists as input. (courtesy @internaut)
* Dropped support of EOL Python versions (2.6, 3.2, and 3.3). (courtesy @internaut)
* Fixed a possible division-by-zero exception. (courtesy @internaut)
* Fixed a formatting error in an exception message. (courtesy @internaut)
* Compiled with Cython 0.27.3.

## 1.4.1 (2016-07-18)
* Clarified that this implementation is of the [optimal string alignment distance algorithm](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance#Optimal_string_alignment_distance) (see [this issue](https://github.com/gfairchild/pyxDamerauLevenshtein/issues/6) for more information).
* Renamed `damerau_levenshtein_distance_withNPArray` to `damerau_levenshtein_distance_ndarray` and `normalized_damerau_levenshtein_distance_withNPArray` to `normalized_damerau_levenshtein_distance_ndarray`.
* Cleaned up `np.ndarray` type and dimension checks.
* Simplified NumPy functions using [`np.vectorize`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.vectorize.html).
* Hardened unicode conversion using [Cython's recommendations](http://docs.cython.org/src/tutorial/strings.html#accepting-strings-from-python-code).
* Compiled with Cython 0.24.1.

## 1.3.2 (2015-05-19)
* [@mittagessen](https://github.com/mittagessen) fixed a bug in `setup.py` that assumed NumPy was installed in [this PR](https://github.com/gfairchild/pyxDamerauLevenshtein/pull/5).

## 1.3.1 (2015-04-07)
* [@ovarene](https://github.com/ovarene) added the ability to compute the edit distance between a string and each string in a [NumPy](http://www.numpy.org/) array in [this PR](https://github.com/gfairchild/pyxDamerauLevenshtein/pull/3).
* Compiled with Cython 0.22.

## 1.2.0 (2014-05-06)
* Changed `xrange` to `range` in pyx code.
* Compiled with Cython 0.20.1.

## 1.1.0 (2013-10-04)
* Moving to setuptools (using [ez_setup.py](https://bitbucket.org/pypa/setuptools/downloads/ez_setup.py) to manage it).

## 1.0.2 (2013-09-23)
* Performance improvement for short-circuit.
* Changed `unsigned int` to `Py_ssize_t` (for 64-bit compatability).
* Improved readability (defined offset indices for `storage`).

## 1.0.1 (2013-09-23)
* Fixed Python 3 unicode issue (thanks to Stefan Behnel - https://groups.google.com/d/msg/cython-users/ofT3fo48ohs/rrf3dtbHkm4J).
* Fixed a possible memory leak (thanks to Stefan Behnel).
* Examples are now Python 3-compatible.

## 1.0.0 (2013-07-03)
* Initial release.
