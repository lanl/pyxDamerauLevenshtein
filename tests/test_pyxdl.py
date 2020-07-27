#!/usr/bin/env python
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

import numpy as np

from pyxdameraulevenshtein import damerau_levenshtein_distance
from pyxdameraulevenshtein import damerau_levenshtein_distance_ndarray
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance_ndarray


class TestDamerauLevenshtien(unittest.TestCase):
    def test_damerau_levenshtein_distance(self):
        assert damerau_levenshtein_distance('smtih', 'smith') == 1
        assert damerau_levenshtein_distance('snapple', 'apple') == 2
        assert damerau_levenshtein_distance('testing', 'testtn') == 2
        assert damerau_levenshtein_distance('saturday', 'sunday') == 3
        assert damerau_levenshtein_distance('Saturday', 'saturday') == 1
        assert damerau_levenshtein_distance('orange', 'pumpkin') == 7
        assert damerau_levenshtein_distance('gifts', 'profit') == 5
        assert damerau_levenshtein_distance('Sjöstedt', 'Sjostedt') == 1
        assert damerau_levenshtein_distance('tt', 't') == 1

        assert damerau_levenshtein_distance([1, 2, 3], [1, 3, 2]) == 1
        assert damerau_levenshtein_distance((1, 2, 3), (1, 3, 2)) == 1
        assert damerau_levenshtein_distance((1, 2, 3), [1, 3, 2]) == 1
        assert damerau_levenshtein_distance([], []) == 0
        assert damerau_levenshtein_distance(list(range(10)), list(range(1, 11))) == 2
        assert damerau_levenshtein_distance([1, 2, 3, 4, 5, 6], [7, 8, 9, 7, 10, 11, 4]) == 7

        assert damerau_levenshtein_distance(np.array([1, 2, 3]), np.array([1, 3, 2])) == 1
        assert damerau_levenshtein_distance(np.array((1, 2, 3)), np.array((1, 3, 2))) == 1
        assert damerau_levenshtein_distance(np.array((1, 2, 3)), ([1, 3, 2])) == 1
        assert damerau_levenshtein_distance(np.array([]), np.array([])) == 0
        assert damerau_levenshtein_distance(np.fromiter(range(10),dtype="int"), np.fromiter(range(1, 11),dtype="int")) == 2
        assert damerau_levenshtein_distance(np.array([1, 2, 3, 4, 5, 6]), np.array([7, 8, 9, 7, 10, 11, 4])) == 7

    def test_normalized_damerau_levenshtein_distance(self):
        assert normalized_damerau_levenshtein_distance('smtih', 'smith') == 0.20000000298023224
        assert normalized_damerau_levenshtein_distance('', '') == 0
        assert normalized_damerau_levenshtein_distance('snapple', 'apple') == 0.2857142984867096
        assert normalized_damerau_levenshtein_distance('testing', 'testtn') == 0.2857142984867096
        assert normalized_damerau_levenshtein_distance('saturday', 'sunday') == 0.375
        assert normalized_damerau_levenshtein_distance('Saturday', 'saturday') == 0.125
        assert normalized_damerau_levenshtein_distance('orange', 'pumpkin') == 1.0
        assert normalized_damerau_levenshtein_distance('gifts', 'profit') == 0.8333333134651184
        assert normalized_damerau_levenshtein_distance('Sjöstedt', 'Sjostedt') == 0.125
        assert normalized_damerau_levenshtein_distance('tt','t') == 0.5

        assert np.isclose(normalized_damerau_levenshtein_distance([1, 2, 3], [1, 3, 2]), 1.0 / 3.0)
        assert normalized_damerau_levenshtein_distance([], []) == 0.0
        assert np.isclose(normalized_damerau_levenshtein_distance(list(range(10)), list(range(1, 11))), 0.2)
        assert normalized_damerau_levenshtein_distance([1, 2, 3, 4, 5, 6], [7, 8, 9, 7, 10, 11, 4]) == 1.0

        assert np.isclose(normalized_damerau_levenshtein_distance(np.array([1, 2, 3]), np.array([1, 3, 2])), 1.0 / 3.0)
        assert normalized_damerau_levenshtein_distance(np.array([]), np.array([])) == 0.0
        assert np.isclose(normalized_damerau_levenshtein_distance(np.fromiter(range(10),dtype="int"), np.fromiter(range(1, 11),dtype="int")), 0.2)
        assert normalized_damerau_levenshtein_distance(np.array([1, 2, 3, 4, 5, 6]), np.array([7, 8, 9, 7, 10, 11, 4])) == 1.0

    def test_damerau_levenshtein_distance_ndarray(self):
        assert damerau_levenshtein_distance_ndarray(
            'Saturday', np.array(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
        ).tolist() == [3, 5, 5, 6, 4, 5, 0]

        assert damerau_levenshtein_distance_ndarray(
            'Sjöstedt', np.array(['Sjöstedt', 'Sjostedt', 'Söstedt', 'Sjöedt'])
        ).tolist() == [0, 1, 1, 2]

    def test_normalized_damerau_levenshtein_distance_ndarray(self):
        assert normalized_damerau_levenshtein_distance_ndarray(
            'Saturday', np.array(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
        ).tolist() == [0.375, 0.625, 0.625, 0.6666666865348816, 0.5, 0.625, 0.0]

        assert normalized_damerau_levenshtein_distance_ndarray(
            'Sjöstedt', np.array(['Sjöstedt', 'Sjostedt', 'Söstedt', 'Sjöedt'])
        ).tolist() == [0.0, 0.125, 0.125, 0.25]


if __name__ == '__main__':
    unittest.main()
