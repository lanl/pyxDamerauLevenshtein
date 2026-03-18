# -*- coding: utf-8 -*-

"""
    Copyright (c) 2013, Triad National Security, LLC
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following
      disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
      following disclaimer in the documentation and/or other materials provided with the distribution.
    * Neither the name of Triad National Security, LLC nor the names of its contributors may be used to endorse or
      promote products derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import unittest
import math
import pytest

from pyxdameraulevenshtein import damerau_levenshtein_distance
from pyxdameraulevenshtein import damerau_levenshtein_distance_seqs
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance_seqs


class TestDamerauLevenshtien(unittest.TestCase):
    def test_damerau_levenshtein_distance(self):
        # basic string examples
        assert damerau_levenshtein_distance('smtih', 'smith') == 1
        assert damerau_levenshtein_distance('snapple', 'apple') == 2
        assert damerau_levenshtein_distance('testing', 'testtn') == 2
        assert damerau_levenshtein_distance('saturday', 'sunday') == 3
        assert damerau_levenshtein_distance('gifts', 'profit') == 5

        # case sensitivity
        assert damerau_levenshtein_distance('Saturday', 'saturday') == 1

        # completely different strings (distance equals length of longer sequence)
        assert damerau_levenshtein_distance('orange', 'pumpkin') == 7

        # unicode
        assert damerau_levenshtein_distance('Sjöstedt', 'Sjostedt') == 1

        # second sequence shorter than first (exercises internal swap logic)
        assert damerau_levenshtein_distance('tt', 't') == 1

        # identical non-empty sequences
        assert damerau_levenshtein_distance('abc', 'abc') == 0

        # one empty, one non-empty (both argument orderings)
        assert damerau_levenshtein_distance('', 'abc') == 3
        assert damerau_levenshtein_distance('abc', '') == 3

        # commutativity
        assert damerau_levenshtein_distance('saturday', 'sunday') == damerau_levenshtein_distance('sunday', 'saturday')
        assert damerau_levenshtein_distance('smtih', 'smith') == damerau_levenshtein_distance('smith', 'smtih')

        # non-string sequence types (list, tuple, mixed, range)
        assert damerau_levenshtein_distance([1, 2, 3], [1, 3, 2]) == 1
        assert damerau_levenshtein_distance((1, 2, 3), (1, 3, 2)) == 1
        assert damerau_levenshtein_distance((1, 2, 3), [1, 3, 2]) == 1
        assert damerau_levenshtein_distance([], []) == 0
        assert damerau_levenshtein_distance(range(10), range(1, 11)) == 2
        assert damerau_levenshtein_distance([1, 2, 3, 4, 5, 6], [7, 8, 9, 7, 10, 11, 4]) == 7

    def test_normalized_damerau_levenshtein_distance(self):
        # note: the normalized functions use a 32-bit C float (cpdef float in Cython), not a Python float
        # (64-bit). some expected values look unusual (e.g., 0.20000000298023224 instead of 0.2) due to
        # IEEE 754 float32 representation — this is intentional and expected.

        # basic string examples
        assert normalized_damerau_levenshtein_distance('smtih', 'smith') == 0.20000000298023224
        assert normalized_damerau_levenshtein_distance('snapple', 'apple') == 0.2857142984867096
        assert normalized_damerau_levenshtein_distance('testing', 'testtn') == 0.2857142984867096
        assert normalized_damerau_levenshtein_distance('saturday', 'sunday') == 0.375
        assert normalized_damerau_levenshtein_distance('gifts', 'profit') == 0.8333333134651184

        # case sensitivity
        assert normalized_damerau_levenshtein_distance('Saturday', 'saturday') == 0.125

        # completely different strings (normalized to 1.0)
        assert normalized_damerau_levenshtein_distance('orange', 'pumpkin') == 1.0

        # unicode
        assert normalized_damerau_levenshtein_distance('Sjöstedt', 'Sjostedt') == 0.125

        # second sequence shorter than first (exercises internal swap logic)
        assert normalized_damerau_levenshtein_distance('tt', 't') == 0.5

        # both empty (guards against division by zero)
        assert normalized_damerau_levenshtein_distance('', '') == 0

        # identical non-empty sequences
        assert normalized_damerau_levenshtein_distance('abc', 'abc') == 0.0

        # one empty, one non-empty
        assert normalized_damerau_levenshtein_distance('', 'abc') == 1.0
        assert normalized_damerau_levenshtein_distance('abc', '') == 1.0

        # non-string sequence types (list, range)
        assert math.isclose(normalized_damerau_levenshtein_distance([1, 2, 3], [1, 3, 2]), 1.0 / 3.0, rel_tol=1e-05)
        assert normalized_damerau_levenshtein_distance([], []) == 0.0
        assert math.isclose(normalized_damerau_levenshtein_distance(range(10), range(1, 11)), 0.2, rel_tol=1e-05)
        assert normalized_damerau_levenshtein_distance([1, 2, 3, 4, 5, 6], [7, 8, 9, 7, 10, 11, 4]) == 1.0

    def test_damerau_levenshtein_distance_seqs(self):
        # basic string examples including identical match (distance 0) at end
        assert damerau_levenshtein_distance_seqs(
            'Saturday', ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        ) == [3, 5, 5, 6, 4, 5, 0]

        # unicode
        assert damerau_levenshtein_distance_seqs(
            'Sjöstedt', ['Sjöstedt', 'Sjostedt', 'Söstedt', 'Sjöedt']
        ) == [0, 1, 1, 2]

        # empty seqs list
        assert damerau_levenshtein_distance_seqs('abc', []) == []

        # non-string sequences
        assert damerau_levenshtein_distance_seqs([1, 2, 3], [[1, 2, 3], [1, 3, 2], []]) == [0, 1, 3]

    def test_normalized_damerau_levenshtein_distance_seqs(self):
        # basic string examples including identical match (0.0) at end
        assert normalized_damerau_levenshtein_distance_seqs(
            'Saturday', ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        ) == [0.375, 0.625, 0.625, 0.6666666865348816, 0.5, 0.625, 0.0]

        # unicode
        assert normalized_damerau_levenshtein_distance_seqs(
            'Sjöstedt', ['Sjöstedt', 'Sjostedt', 'Söstedt', 'Sjöedt']
        ) == [0.0, 0.125, 0.125, 0.25]

        # empty seqs list
        assert normalized_damerau_levenshtein_distance_seqs('abc', []) == []

        # non-string sequences
        assert normalized_damerau_levenshtein_distance_seqs([1, 2, 3], [[1, 2, 3], [1, 3, 2]]) == [0.0, pytest.approx(1.0 / 3.0, rel=1e-5)]

    def test_damerau_levenshtein_distance_max_distance(self):
        # distance within threshold returns exact distance
        assert damerau_levenshtein_distance('smtih', 'smith', max_distance=2) == 1
        assert damerau_levenshtein_distance('saturday', 'sunday', max_distance=3) == 3

        # distance at threshold returns exact distance
        assert damerau_levenshtein_distance('smtih', 'smith', max_distance=1) == 1

        # distance exceeds threshold returns max_distance + 1
        assert damerau_levenshtein_distance('saturday', 'sunday', max_distance=2) == 3
        assert damerau_levenshtein_distance('orange', 'pumpkin', max_distance=3) == 4

        # max_distance=0 with identical sequences
        assert damerau_levenshtein_distance('abc', 'abc', max_distance=0) == 0

        # max_distance=0 with non-identical sequences
        assert damerau_levenshtein_distance('abc', 'abd', max_distance=0) == 1

        # non-string sequences
        assert damerau_levenshtein_distance([1, 2, 3], [1, 3, 2], max_distance=1) == 1
        assert damerau_levenshtein_distance([1, 2, 3], [1, 3, 2], max_distance=0) == 1

    def test_normalized_damerau_levenshtein_distance_max_distance(self):
        # distance within threshold returns exact normalized distance
        assert normalized_damerau_levenshtein_distance('smtih', 'smith', max_distance=0.5) == 0.20000000298023224

        # distance exceeds threshold: n=8, int_max=1, raw returns 2, result=2/8=0.25
        assert normalized_damerau_levenshtein_distance('saturday', 'sunday', max_distance=0.2) == 0.25
        # distance exceeds threshold: n=7, int_max=3, raw returns 4, result=4/7
        assert math.isclose(normalized_damerau_levenshtein_distance('orange', 'pumpkin', max_distance=0.5), 4.0 / 7.0, rel_tol=1e-05)

    def test_damerau_levenshtein_distance_seqs_max_distance(self):
        # distances within threshold return exact values; those exceeding return max_distance + 1
        # 'saturday' vs 'sunday'=3, 'monday'=5, 'saturday'=0
        assert damerau_levenshtein_distance_seqs(
            'Saturday', ['Sunday', 'Monday', 'Saturday'], max_distance=3
        ) == [3, 4, 0]

    def test_normalized_damerau_levenshtein_distance_seqs_max_distance(self):
        # distance within threshold returns exact value; distance exceeding returns value > max_distance
        results = normalized_damerau_levenshtein_distance_seqs(
            'Saturday', ['Saturday', 'Sunday', 'Monday'], max_distance=0.2
        )
        assert results[0] == 0.0   # identical, within threshold
        assert results[1] > 0.2   # exceeds threshold
        assert results[2] > 0.2   # exceeds threshold


if __name__ == '__main__':
    unittest.main()
