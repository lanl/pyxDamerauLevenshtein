# pyxDamerauLevenshtein

[![Tests](https://github.com/lanl/pyxDamerauLevenshtein/actions/workflows/tests.yml/badge.svg)](https://github.com/lanl/pyxDamerauLevenshtein/actions/workflows/tests.yml)

## LICENSE
This software is licensed under the [BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause). Please refer to the separate [LICENSE](LICENSE) file for the exact text of the license. You are obligated to give attribution if you use this code.

## ABOUT
pyxDamerauLevenshtein implements the Damerau-Levenshtein (DL) edit distance algorithm for Python in Cython for high performance. Courtesy [Wikipedia](http://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance):

> In information theory and computer science, the Damerau-Levenshtein distance (named after Frederick J. Damerau and Vladimir I. Levenshtein) is a "distance" (string metric) between two strings, i.e., finite sequence of symbols, given by counting the minimum number of operations needed to transform one string into the other, where an operation is defined as an insertion, deletion, or substitution of a single character, or a transposition of two adjacent characters.

This implementation is based on [Michael Homer's pure Python implementation](https://web.archive.org/web/20150909134357/http://mwh.geek.nz:80/2009/04/26/python-damerau-levenshtein-distance/), which implements the [optimal string alignment distance algorithm](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance#Optimal_string_alignment_distance). It runs in `O(N*M)` time using `O(M)` space. It supports unicode characters.

## REQUIREMENTS
This code requires Python 3.11+. Prebuilt wheels are published to PyPI for Linux (x86_64 and aarch64), macOS (x86_64 and arm64), and Windows (x86_64), so most users don't need anything else. Building from source requires a C compiler such as GCC; Cython is installed automatically as a build dependency.

## INSTALL
pyxDamerauLevenshtein is available on PyPI at https://pypi.org/project/pyxDamerauLevenshtein/.

Install using [pip](https://pypi.org/project/pip/):

    pip install pyxDamerauLevenshtein

## USING THIS CODE
The following methods are available:

* **Edit distance** (`damerau_levenshtein_distance`)
    * Compute the raw distance between two sequences (i.e., the minimum number of operations necessary to transform one sequence into the other).
    * Supports any sequence type that supports `len()` and integer indexing: `str`, `bytes`, `list`, `tuple`, `range`, and more. Elements are compared with `==`.
    * Optionally accepts a non-negative integer `max_distance` threshold. If the true distance exceeds it, `max_distance + 1` is returned instead, and the computation stops as soon as the threshold is known to be exceeded.

* **Normalized edit distance** (`normalized_damerau_levenshtein_distance`)
    * Compute the ratio of the edit distance to the length of the longer sequence (`max(len(seq1), len(seq2))`). 0.0 means that the sequences are identical, while 1.0 means that they have nothing in common. Note that this definition is the exact opposite of [`difflib.SequenceMatcher.ratio()`](https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher.ratio).

* **Edit distance against a sequence of sequences** (`damerau_levenshtein_distance_seqs`)
    * Compute the raw distances between a sequence and each sequence within an iterable of sequences (e.g., `list`, `tuple`, generator).
    * Optionally accepts a `max_distance` threshold forwarded to each individual computation.

* **Normalized edit distance against a sequence of sequences** (`normalized_damerau_levenshtein_distance_seqs`)
    * Compute the normalized distances between a sequence and each sequence within an iterable of sequences (e.g., `list`, `tuple`, generator).

Basic use:

```python
from pyxdameraulevenshtein import (
    damerau_levenshtein_distance,
    damerau_levenshtein_distance_seqs,
    normalized_damerau_levenshtein_distance,
    normalized_damerau_levenshtein_distance_seqs,
)

damerau_levenshtein_distance('smtih', 'smith')  # expected result: 1
normalized_damerau_levenshtein_distance('smtih', 'smith')  # expected result: 0.2
damerau_levenshtein_distance([1, 2, 3, 4, 5, 6], [7, 8, 9, 7, 10, 11, 4])  # expected result: 7

# max_distance short-circuits when the true distance (7) exceeds the threshold
damerau_levenshtein_distance('orange', 'pumpkin', max_distance=3)  # expected result: 4 (max_distance + 1)

array = ['test1', 'test12', 'test123']
damerau_levenshtein_distance_seqs('test', array)  # expected result: [1, 2, 3]
normalized_damerau_levenshtein_distance_seqs('test', array)  # expected result: [0.2, 0.333..., 0.428...]
```

## DIFFERENCES
Other Python DL implementations:

* [Michael Homer's native Python code](https://web.archive.org/web/20150909134357/http://mwh.geek.nz:80/2009/04/26/python-damerau-levenshtein-distance/)
* [jellyfish](https://github.com/jamesturk/jellyfish)
* [RapidFuzz](https://github.com/rapidfuzz/RapidFuzz)

When pyxDamerauLevenshtein was initially released in 2013, it was the fastest DL implementation available for Python and the only one with unicode support, and it remained that way for many years. Since then, libraries like [RapidFuzz](https://github.com/rapidfuzz/RapidFuzz) have eclipsed it in performance. pyxDamerauLevenshtein still offers respectable performance via Cython and is a solid choice if absolute maximum speed is not a requirement.
