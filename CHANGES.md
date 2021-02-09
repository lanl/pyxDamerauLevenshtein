# Changes

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

## 1.6 (2020-05-01)

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

## 1.5 (2018-02-04)

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

## 1.2 (2014-05-06)
* Changed `xrange` to `range` in pyx code.
* Compiled with Cython 0.20.1.

## 1.1 (2013-10-04)
* Moving to setuptools (using [ez_setup.py](https://bitbucket.org/pypa/setuptools/downloads/ez_setup.py) to manage it).

## 1.0.2 (2013-09-23)
* Performance improvement for short-circuit.
* Changed `unsigned int` to `Py_ssize_t` (for 64-bit compatability).
* Improved readability (defined offset indices for `storage`).

## 1.0.1 (2013-09-23)
* Fixed Python 3 unicode issue (thanks to Stefan Behnel - https://groups.google.com/d/msg/cython-users/ofT3fo48ohs/rrf3dtbHkm4J).
* Fixed a possible memory leak (thanks to Stefan Behnel).
* Examples are now Python 3-compatible.

## 1.0 (2013-07-03)
* Initial release.
