# pyxDamerauLevenshtein

[![Test](https://github.com/lanl/pyxDamerauLevenshtein/actions/workflows/test.yml/badge.svg)](https://github.com/lanl/pyxDamerauLevenshtein/actions/workflows/test.yml)

## LICENSE
This software is licensed under the [BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause). Please refer to the separate [LICENSE](LICENSE) file for the exact text of the license. You are obligated to give attribution if you use this code.

## ABOUT
pyxDamerauLevenshtein implements the Damerau-Levenshtein (DL) edit distance algorithm for Python in Cython for high performance. Courtesy [Wikipedia](http://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance):

> In information theory and computer science, the Damerau-Levenshtein distance (named after Frederick J. Damerau and Vladimir I. Levenshtein) is a "distance" (string metric) between two strings, i.e., finite sequence of symbols, given by counting the minimum number of operations needed to transform one string into the other, where an operation is defined as an insertion, deletion, or substitution of a single character, or a transposition of two adjacent characters.

This implementation is based on [Michael Homer's pure Python implementation](https://web.archive.org/web/20150909134357/http://mwh.geek.nz:80/2009/04/26/python-damerau-levenshtein-distance/), which implements the [optimal string alignment distance algorithm](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance#Optimal_string_alignment_distance). It runs in `O(N*M)` time using `O(M)` space. It supports unicode characters.

## REQUIREMENTS
This code requires Python 3.9+, C compiler such as GCC, and Cython.

## INSTALL
pyxDamerauLevenshtein is available on PyPI at https://pypi.org/project/pyxDamerauLevenshtein/.

Install using [pip](https://pypi.org/project/pip/):

    pip install pyxDamerauLevenshtein

Install from source:

    pip install .

## USING THIS CODE
The following methods are available:

* **Edit distance** (`damerau_levenshtein_distance`)
    * Compute the raw distance between two sequences (i.e., the minimum number of operations necessary to transform one sequence into the other).
    * Supports any sequence type: `str`, `list`, `tuple`, `range`, and more.
    * Optionally accepts a `max_distance` integer threshold. If the true distance exceeds it, `max_distance + 1` is returned immediately, avoiding unnecessary computation.

* **Normalized edit distance** (`normalized_damerau_levenshtein_distance`)
    * Compute the ratio of the edit distance to the length of `max(seq1, seq2)`. 0.0 means that the sequences are identical, while 1.0 means that they have nothing in common. Note that this definition is the exact opposite of [`difflib.SequenceMatcher.ratio()`](https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher.ratio).
    * Optionally accepts a `max_distance` float threshold. If the true normalized distance exceeds it, a value greater than `max_distance` is returned immediately.

* **Edit distance against a sequence of sequences** (`damerau_levenshtein_distance_seqs`)
    * Compute the raw distances between a sequence and each sequence within another sequence (e.g., `list`, `tuple`).
    * Optionally accepts a `max_distance` threshold forwarded to each individual computation.

* **Normalized edit distance against a sequence of sequences** (`normalized_damerau_levenshtein_distance_seqs`)
    * Compute the normalized distances between a sequence and each sequence within another sequence (e.g., `list`, `tuple`).
    * Optionally accepts a `max_distance` threshold forwarded to each individual computation.

Basic use:

```python
from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance
damerau_levenshtein_distance('smtih', 'smith')  # expected result: 1
normalized_damerau_levenshtein_distance('smtih', 'smith')  # expected result: 0.2
damerau_levenshtein_distance([1, 2, 3, 4, 5, 6], [7, 8, 9, 7, 10, 11, 4])  # expected result: 7

# max_distance short-circuits when the true distance exceeds the threshold
damerau_levenshtein_distance('saturday', 'sunday', max_distance=2)  # expected result: 3 (max_distance + 1)
normalized_damerau_levenshtein_distance('smtih', 'smith', max_distance=0.5)  # expected result: 0.2 (within threshold)

from pyxdameraulevenshtein import damerau_levenshtein_distance_seqs, normalized_damerau_levenshtein_distance_seqs
array = ['test1', 'test12', 'test123']
damerau_levenshtein_distance_seqs('test', array)  # expected result: [1, 2, 3]
normalized_damerau_levenshtein_distance_seqs('test', array)  # expected result: [0.2, 0.3333333333333333, 0.42857142857142855]
```

## DIFFERENCES
Other Python DL implementations:

* [Michael Homer's native Python code](https://web.archive.org/web/20150909134357/http://mwh.geek.nz:80/2009/04/26/python-damerau-levenshtein-distance/)
* [jellyfish](https://github.com/jamesturk/jellyfish)

pyxDamerauLevenshtein differs from other Python implementations in that it is both fast via Cython *and* supports unicode. Michael Homer's implementation is fast for Python, but it is *two orders of magnitude* slower than this Cython implementation. jellyfish provides C implementations for a variety of string comparison metrics and is sometimes faster than pyxDamerauLevenshtein.

Python's built-in [`difflib.SequenceMatcher.ratio()`](https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher.ratio) performs about an order of magnitude faster than Michael Homer's implementation but is still one order of magnitude slower than this DL implementation. difflib, however, uses a different algorithm (difflib uses the [Ratcliff/Obershelp algorithm](http://www.drdobbs.com/database/pattern-matching-the-gestalt-approach/184407970)).

Performance differences (on Intel i7-2600 running at 3.4Ghz):

    >>> import timeit
    >>> #this implementation:
    ... timeit.timeit("damerau_levenshtein_distance('e0zdvfb840174ut74j2v7gabx1 5bs', 'qpk5vei 4tzo0bglx8rl7e 2h4uei7')", 'from pyxdameraulevenshtein import damerau_levenshtein_distance', number=500000)
    7.417556047439575
    >>> #Michael Homer's native Python implementation:
    ... timeit.timeit("dameraulevenshtein('e0zdvfb840174ut74j2v7gabx1 5bs', 'qpk5vei 4tzo0bglx8rl7e 2h4uei7')", 'from dameraulevenshtein import dameraulevenshtein', number=500000)
    667.0276439189911
    >>> #difflib
    ... timeit.timeit("difflib.SequenceMatcher(None, 'e0zdvfb840174ut74j2v7gabx1 5bs', 'qpk5vei 4tzo0bglx8rl7e 2h4uei7').ratio()", 'import difflib', number=500000)
    135.41051697731018
