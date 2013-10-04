# Changes

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
