# Changes

## 1.4 (2016-07-18)
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
