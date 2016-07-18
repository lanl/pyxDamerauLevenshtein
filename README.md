# pyxDamerauLevenshtein

## AUTHOR
Geoffrey Fairchild
* [http://www.gfairchild.com/](http://www.gfairchild.com/)
* [https://github.com/gfairchild](https://github.com/gfairchild)
* [http://www.linkedin.com/in/gfairchild/](http://www.linkedin.com/in/gfairchild/)

## LICENSE
This software is licensed under the [BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause). Please refer to the separate [LICENSE.txt](LICENSE.txt) file for the exact text of the license. You are obligated to give attribution if you use this code.

## ABOUT
pyxDamerauLevenshtein implements the Damerau-Levenshtein (DL) edit distance algorithm for Python in Cython for high performance. Courtesy [Wikipedia](http://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance):

> In information theory and computer science, the Damerau-Levenshtein distance (named after Frederick J. Damerau and Vladimir I. Levenshtein) is a "distance" (string metric) between two strings, i.e., finite sequence of symbols, given by counting the minimum number of operations needed to transform one string into the other, where an operation is defined as an insertion, deletion, or substitution of a single character, or a transposition of two adjacent characters.

This implementation is based on [Michael Homer's pure Python implementation](http://mwh.geek.nz/2009/04/26/python-damerau-levenshtein-distance/), which implements the [optimal string alignment distance algorithm](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance#Optimal_string_alignment_distance). It runs in `O(N*M)` time using `O(M)` space. It supports unicode characters.

## REQUIREMENTS
This code requires Python 2.4+ (including Python 3), [NumPy](http://www.numpy.org/), and a C compiler such as GCC. Although the code was written in Cython, Cython is not required for installation.

## INSTALL
pyxDamerauLevenshtein is available on PyPI at https://pypi.python.org/pypi/pyxDamerauLevenshtein.

Install using [pip](http://www.pip-installer.org/):

    pip install pyxDamerauLevenshtein

Install from source:

    python setup.py install

## USING THIS CODE
The code is called directly from Python as in [examples.py](examples/examples.py):
    
    > python examples.py
    # edit distances (low edit distance means words are more similar):
    damerau_levenshtein_distance('smtih', 'smith') = 1
    damerau_levenshtein_distance('snapple', 'apple') = 2
    damerau_levenshtein_distance('testing', 'testtn') = 2
    damerau_levenshtein_distance('saturday', 'sunday') = 3
    damerau_levenshtein_distance('Saturday', 'saturday') = 1
    damerau_levenshtein_distance('orange', 'pumpkin') = 7
    damerau_levenshtein_distance('gifts', 'profit') = 5
    damerau_levenshtein_distance('Sjöstedt', 'Sjostedt') = 1  # unicode example

    # normalized edit distances (low ratio means words are similar):
    normalized_damerau_levenshtein_distance('smtih', 'smith') = 0.20000000298023224
    normalized_damerau_levenshtein_distance('snapple', 'apple') = 0.2857142984867096
    normalized_damerau_levenshtein_distance('testing', 'testtn') = 0.2857142984867096
    normalized_damerau_levenshtein_distance('saturday', 'sunday') = 0.375
    normalized_damerau_levenshtein_distance('Saturday', 'saturday') = 0.125
    normalized_damerau_levenshtein_distance('orange', 'pumpkin') = 1.0
    normalized_damerau_levenshtein_distance('gifts', 'profit') = 0.8333333134651184
    normalized_damerau_levenshtein_distance('Sjöstedt', 'Sjostedt') = 0.125  # unicode example

    # edit distances for a single sequence against an array of sequences
    damerau_levenshtein_distance_ndarray('Saturday', '['Sunday' 'Monday' 'Tuesday' 'Wednesday' 'Thursday' 'Friday' 'Saturday']') = [3 5 5 6 4 5 0]
    normalized_damerau_levenshtein_distance_ndarray('Saturday', '['Sunday' 'Monday' 'Tuesday' 'Wednesday' 'Thursday' 'Friday' 'Saturday']') = [ 0.375       0.625       0.625       0.66666669  0.5         0.625       0.        ]

    # normalized edit distances for a single sequence against an array of sequences - unicode
    damerau_levenshtein_distance_ndarray('Sjöstedt', '['Sjöstedt' 'Sjostedt' 'Söstedt' 'Sjöedt']') = [0 1 1 2]
    normalized_damerau_levenshtein_distance_ndarray('Sjöstedt', '['Sjöstedt' 'Sjostedt' 'Söstedt' 'Sjöedt']') = [ 0.     0.125  0.125  0.25 ]

    # performance testing:
    timeit.timeit("damerau_levenshtein_distance('4dWdCKSEgeeYiGxn0hkXp4eC1ssorp', 'fzLv 8GIQaJ0L7BntQtcYcGW4zfEHB')", 'from pyxdameraulevenshtein import damerau_levenshtein_distance', number=500000) = 5.656925692001096 seconds
    timeit.timeit("damerau_levenshtein_distance('4dWdCKSEgeeYiGxn0hkXp4eC1ssorp', '4dWdCKSEgeeYiGxn0hkXp4eC1ssorp')", 'from pyxdameraulevenshtein import damerau_levenshtein_distance', number=500000) = 0.11744023199935327 seconds  # short-circuit makes this faster

Two values can be computed:

* **Edit distance** (`damerau_levenshtein_distance`)
 - Compute the raw distance between two strings (i.e., the minumum number of operations necessary to transform one string into the other).

* **Normalized edit distance** (`normalized_damerau_levenshtein_distance`)
 - Compute the ratio of the edit distance to the length of `max(string1, string2)`. 0.0 means that the sequences are identical, while 1.0 means that they have nothing in common. Note that this definition is the exact opposite of [`difflib.SequenceMatcher.ratio()`](http://docs.python.org/2/library/difflib.html#difflib.SequenceMatcher.ratio).

* **Edit distance against an array** (`damerau_levenshtein_distance_ndarray`)
 - Compute the raw distance between a reference string and a NumPy array of strings.

* **Normalized edit distance against an array** (`normalized_damerau_levenshtein_distance_ndarray`)
 - Compute the normalized distance between a reference string and a NumPy array of strings.

Basic use:

```python
from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance
damerau_levenshtein_distance('smtih', 'smith')  # expected result: 1
normalized_damerau_levenshtein_distance('smtih', 'smith')  # expected result: 0.2

from pyxdameraulevenshtein import damerau_levenshtein_distance_ndarray, normalized_damerau_levenshtein_distance_ndarray
import numpy as np
array = np.array(['test1', 'test12', 'test123'])
damerau_levenshtein_distance_ndarray('test', array)  # expected result: [1, 2, 3]
normalized_damerau_levenshtein_distance_ndarray('test', array)  # expected result: [0.2, 0.33333334, 0.42857143]
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
    ... timeit.timeit("damerau_levenshtein_distance('e0zdvfb840174ut74j2v7gabx1 5bs', 'qpk5vei 4tzo0bglx8rl7e 2h4uei7')", 'from pyxdameraulevenshtein import damerau_levenshtein_distance', number=500000)
    7.417556047439575
    >>> #Michael Homer's native Python implementation:
    ... timeit.timeit("dameraulevenshtein('e0zdvfb840174ut74j2v7gabx1 5bs', 'qpk5vei 4tzo0bglx8rl7e 2h4uei7')", 'from dameraulevenshtein import dameraulevenshtein', number=500000)
    667.0276439189911
    >>> #difflib
    ... timeit.timeit("difflib.SequenceMatcher(None, 'e0zdvfb840174ut74j2v7gabx1 5bs', 'qpk5vei 4tzo0bglx8rl7e 2h4uei7').ratio()", 'import difflib', number=500000)
    135.41051697731018
