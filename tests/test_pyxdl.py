#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    def test_normalized_damerau_levenshtein_distance(self):
        assert normalized_damerau_levenshtein_distance('smtih', 'smith') == 0.20000000298023224
        assert normalized_damerau_levenshtein_distance('snapple', 'apple') == 0.2857142984867096
        assert normalized_damerau_levenshtein_distance('testing', 'testtn') == 0.2857142984867096
        assert normalized_damerau_levenshtein_distance('saturday', 'sunday') == 0.375
        assert normalized_damerau_levenshtein_distance('Saturday', 'saturday') == 0.125
        assert normalized_damerau_levenshtein_distance('orange', 'pumpkin') == 1.0
        assert normalized_damerau_levenshtein_distance('gifts', 'profit') == 0.8333333134651184
        assert normalized_damerau_levenshtein_distance('Sjöstedt', 'Sjostedt') == 0.125

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
