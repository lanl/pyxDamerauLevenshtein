# pyxDamerauLevenshtein

## AUTHOR
Geoffrey Fairchild
* [http://www.gfairchild.com/](http://www.gfairchild.com/)
* [https://github.com/gfairchild](https://github.com/gfairchild)
* [http://www.linkedin.com/in/gfairchild/](http://www.linkedin.com/in/gfairchild/)

## LICENSE
This software is licensed under the [BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause). Please refer to the separate LICENSE.txt file for the exact text of the license. You are obligated to give attribution if you use this code.

## ABOUT
pyxDamerauLevenshtein implements the Damerau-Levenshtein (DL) edit distance algorithm for Python in Cython for high performance. Courtesy [Wikipedia](http://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance):

> In information theory and computer science, the Damerau-Levenshtein distance (named after Frederick J. Damerau and Vladimir I. Levenshtein) is a "distance" (string metric) between two strings, i.e., finite sequence of symbols, given by counting the minimum number of operations needed to transform one string into the other, where an operation is defined as an insertion, deletion, or substitution of a single character, or a transposition of two adjacent characters.

This implementation is based on [Michael Homer's pure Python implementation](http://mwh.geek.nz/2009/04/26/python-damerau-levenshtein-distance/). It runs in `O(N*M)` time using `O(M)` space. It supports unicode characters.

## REQUIREMENTS
This code requires Python 2.4+ (including Python 3) and a C compiler such as GCC. Although the code was written in Cython, Cython is not required for installation.

## INSTALL
pyxDamerauLevenshtein is available on PyPI at https://pypi.python.org/pypi/pyxDamerauLevenshtein.

Install using [pip](http://www.pip-installer.org/):

	pip install pyxDamerauLevenshtein

Install from source:

	python setup.py install

## USING THIS CODE
The code is called directly from Python as in examples.py:
	
	> python examples.py
	#edit distances (low edit distance means words are similar):
	damerau_levenshtein_distance('smtih', 'smith') = 1
	damerau_levenshtein_distance('snapple', 'apple') = 2
	damerau_levenshtein_distance('testing', 'testtn') = 2
	damerau_levenshtein_distance('saturday', 'sunday') = 3
	damerau_levenshtein_distance('Saturday', 'saturday') = 1
	damerau_levenshtein_distance('orange', 'pumpkin') = 7
	damerau_levenshtein_distance('Sjöstedt', 'Sjostedt') = 1 #unicode example

	#normalized edit distances (low ratio means words are similar):
	normalized_damerau_levenshtein_distance('smtih', 'smith') = 0.200000
	normalized_damerau_levenshtein_distance('snapple', 'apple') = 0.285714
	normalized_damerau_levenshtein_distance('testing', 'testtn') = 0.285714
	normalized_damerau_levenshtein_distance('saturday', 'sunday') = 0.375000
	normalized_damerau_levenshtein_distance('Saturday', 'saturday') = 0.125000
	normalized_damerau_levenshtein_distance('orange', 'pumpkin') = 1.000000
	normalized_damerau_levenshtein_distance('Sjöstedt', 'Sjostedt') = 0.125000 #unicode example

	#performance testing:
	timeit.timeit("damerau_levenshtein_distance('P tcTpUUu2TvwH8f0RbXqgruPLwn1U', 'bhHyeluw9nh8 egCCzNJgp Snh0 Wg')", 'from pyxdameraulevenshtein import damerau_levenshtein_distance', number=500000) = 3.567970 seconds
	timeit.timeit("damerau_levenshtein_distance('P tcTpUUu2TvwH8f0RbXqgruPLwn1U', 'P tcTpUUu2TvwH8f0RbXqgruPLwn1U')", 'from pyxdameraulevenshtein import damerau_levenshtein_distance', number=500000) = 0.888284 seconds #short-circuit makes this faster

Two values can be computed:

* **Edit Distance** (`damerau_levenshtein_distance`)
 - Compute the raw distance between two strings (i.e., the minumum number of operations necessary to transform one string into the other).
* **Normalized Edit Distance** (`normalized_damerau_levenshtein_distance`)
 - Compute the ratio of the edit distance to the length of max(string1, string2). 0.0 means that the sequences are identical, while 1.0 means that they have nothing in common. Note that this definition is the exact opposite of [`difflib.SequenceMatcher.ratio()`](http://docs.python.org/2/library/difflib.html#difflib.SequenceMatcher.ratio).

Basic use:

```python
from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance
damerau_levenshtein_distance('smtih', 'smith')
normalized_damerau_levenshtein_distance('smtih', 'smith')
```

## DIFFERENCES
Other Python DL implementations:

* [Michael Homer's native Python code](http://mwh.geek.nz/2009/04/26/python-damerau-levenshtein-distance/)
* [jellyfish](https://github.com/sunlightlabs/jellyfish)

pyxDamerauLevenshtein differs from other Python implementations in that it is both fast via Cython *and* supports unicode. Michael Homer's implementation is fast for Python, but it is *two orders of magnitude* slower than this Cython implementation. jellyfish provides C implementations for a variety of string comparison metrics, but [it is unlikely to support unicode in the near future](https://github.com/sunlightlabs/jellyfish/issues/1).

Python's built-in [`difflib.SequenceMatcher.ratio()`](http://docs.python.org/2/library/difflib.html#difflib.SequenceMatcher.ratio) performs about an order of magnitude faster than Michael Homer's implementation but is still one order of magnitude slower than this DL implementation. difflib, however, uses a different algorithm (difflib uses the [Ratcliff/Obershelp algorithm](http://www.drdobbs.com/database/pattern-matching-the-gestalt-approach/184407970)).

Performance differences (on Intel i7-2600 running at 3.4Ghz):

	>>> import timeit
	>>> #this implementation:
	... timeit.timeit("damerau_levenshtein_distance('e0zdvfb840174ut74j2v7gabx1 5bs', 'qpk5vei 4tzo0bglx8rl7e 2h4uei7')", 'from damerau_levenshtein_distance import damerau_levenshtein_distance', number=500000)
	7.417556047439575
	>>> #Michael Homer's native Python implementation:
	... timeit.timeit("dameraulevenshtein('e0zdvfb840174ut74j2v7gabx1 5bs', 'qpk5vei 4tzo0bglx8rl7e 2h4uei7')", 'from dameraulevenshtein import dameraulevenshtein', number=500000)
	667.0276439189911
	>>> #difflib
	... timeit.timeit("difflib.SequenceMatcher(None, 'e0zdvfb840174ut74j2v7gabx1 5bs', 'qpk5vei 4tzo0bglx8rl7e 2h4uei7').ratio()", 'import difflib', number=500000)
	135.41051697731018
