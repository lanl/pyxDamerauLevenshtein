pyxDamerauLevenshtein implements the Damerau-Levenshtein (DL)
edit distance algorithm for Python in Cython for high performance.
Courtesy `Wikipedia <http://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance>`_:
In information theory and computer science, the
Damerau-Levenshtein distance (named after Frederick J. Damerau and
Vladimir I. Levenshtein) is a "distance" (string metric) between
two strings, i.e., finite sequence of symbols, given by counting
the minimum number of operations needed to transform one string
into the other, where an operation is defined as an insertion,
deletion, or substitution of a single character, or a
transposition of two adjacent characters. This implementation is
based on `Michael Homer\'s pure Python implementation
<https://web.archive.org/web/20150909134357/http://mwh.geek.nz:80/2009/04/26/python-damerau-levenshtein-distance/>`_,
which implements the `optimal string alignment distance algorithm
<https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance#Optimal_string_alignment_distance>`_.
It runs in ``O(N*M)`` time using ``O(M)`` space. It supports
unicode characters. For more information on pyxDamerauLevenshtein,
visit the `GitHub project page <https://github.com/gfairchild/pyxDamerauLevenshtein>`_.
