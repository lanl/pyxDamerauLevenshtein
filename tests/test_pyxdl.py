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

import doctest
import itertools
import random
from collections import deque

import pytest

import pyxdameraulevenshtein
from pyxdameraulevenshtein import (
    damerau_levenshtein_distance,
    damerau_levenshtein_distance_seqs,
    normalized_damerau_levenshtein_distance,
    normalized_damerau_levenshtein_distance_seqs,
)

PUBLIC_API = (
    damerau_levenshtein_distance,
    damerau_levenshtein_distance_seqs,
    normalized_damerau_levenshtein_distance,
    normalized_damerau_levenshtein_distance_seqs,
)
SEQS_API = (damerau_levenshtein_distance_seqs, normalized_damerau_levenshtein_distance_seqs)

# (seq1, seq2, expected distance, expected normalized distance)
# the normalized implementation divides in C doubles, which rounds identically to Python's true division, so exact
# float comparison against `distance / length` expressions is reliable here
CASES = [
    pytest.param('smtih', 'smith', 1, 0.2, id='transposition'),
    pytest.param('snapple', 'apple', 2, 2 / 7, id='prefix-deletion'),
    pytest.param('testing', 'testtn', 2, 2 / 7, id='common-prefix'),
    pytest.param('saturday', 'sunday', 3, 0.375, id='saturday-sunday'),
    pytest.param('gifts', 'profit', 5, 5 / 6, id='gifts-profit'),
    pytest.param('Saturday', 'saturday', 1, 0.125, id='case-sensitive'),
    pytest.param('orange', 'pumpkin', 7, 1.0, id='nothing-in-common'),
    pytest.param('Sjöstedt', 'Sjostedt', 1, 0.125, id='unicode'),
    pytest.param('tt', 't', 1, 0.5, id='second-shorter'),
    pytest.param('abc', 'abc', 0, 0.0, id='identical'),
    pytest.param('', '', 0, 0.0, id='both-empty'),
    pytest.param('', 'abc', 3, 1.0, id='first-empty'),
    pytest.param('abc', '', 3, 1.0, id='second-empty'),
    pytest.param('ba', 'ab', 1, 0.5, id='transposition-at-start'),
    pytest.param('abcd', 'abdc', 1, 0.25, id='transposition-at-end'),
    pytest.param('abcdef', 'badcfe', 3, 0.5, id='multiple-transpositions'),
    # optimal string alignment forbids editing a transposed substring again, so this is 3 (true DL would give 2)
    pytest.param('ca', 'abc', 3, 1.0, id='osa-not-unrestricted-dl'),
    pytest.param('abcdef', 'abcxyz', 3, 0.5, id='shared-prefix-then-differs'),
    pytest.param('abc', 'abcdef', 3, 0.5, id='first-is-prefix-of-second'),
    pytest.param('abcdef', 'abc', 3, 0.5, id='second-is-prefix-of-first'),
    pytest.param('a' * 1000 + 'x', 'a' * 1000 + 'y', 1, 1 / 1001, id='long-shared-prefix'),
    pytest.param('a' * 500, 'b' * 500, 500, 1.0, id='long-nothing-in-common'),
    pytest.param([1, 2, 3], [1, 3, 2], 1, 1 / 3, id='list'),
    pytest.param((1, 2, 3), (1, 3, 2), 1, 1 / 3, id='tuple'),
    pytest.param((1, 2, 3), [1, 3, 2], 1, 1 / 3, id='tuple-and-list'),
    pytest.param([], [], 0, 0.0, id='empty-lists'),
    pytest.param(range(10), range(1, 11), 2, 0.2, id='range'),
    pytest.param(b'abc', b'acb', 1, 1 / 3, id='bytes'),
    # a deque supports len() and indexing but not slicing
    pytest.param(deque('abcd'), deque('abdc'), 1, 0.25, id='deque-with-common-prefix'),
    pytest.param([1, 2, 3, 4, 5, 6], [7, 8, 9, 7, 10, 11, 4], 7, 1.0, id='integers-nothing-in-common'),
    pytest.param([1, 'a', None], [1, None, 'a'], 1, 1 / 3, id='mixed-element-types'),
    pytest.param([[1], {2: 3}], [{2: 3}, [1]], 1, 0.5, id='unhashable-elements'),
    pytest.param([1, 2.0], [1.0, 2], 0, 0.0, id='elements-compared-by-equality'),
]


def osa_distance(seq1, seq2):
    """Straightforward full-matrix optimal string alignment distance, used as a reference implementation."""
    rows = [[0] * (len(seq2) + 1) for _ in range(len(seq1) + 1)]
    for i in range(len(seq1) + 1):
        rows[i][0] = i
    for j in range(len(seq2) + 1):
        rows[0][j] = j
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            rows[i][j] = min(
                rows[i - 1][j] + 1,
                rows[i][j - 1] + 1,
                rows[i - 1][j - 1] + (seq1[i - 1] != seq2[j - 1]),
            )
            if i > 1 and j > 1 and seq1[i - 1] == seq2[j - 2] and seq1[i - 2] == seq2[j - 1]:
                rows[i][j] = min(rows[i][j], rows[i - 2][j - 2] + 1)
    return rows[-1][-1]


def random_string_pairs(count, alphabet, max_len, seed):
    rng = random.Random(seed)
    for _ in range(count):
        seq1 = ''.join(rng.choices(alphabet, k=rng.randint(0, max_len)))
        seq2 = ''.join(rng.choices(alphabet, k=rng.randint(0, max_len)))
        yield seq1, seq2


class TestDamerauLevenshteinDistance:
    @pytest.mark.parametrize(('seq1', 'seq2', 'expected', 'expected_normalized'), CASES)
    def test_distance(self, seq1, seq2, expected, expected_normalized):
        assert damerau_levenshtein_distance(seq1, seq2) == expected

    @pytest.mark.parametrize(('seq1', 'seq2', 'expected', 'expected_normalized'), CASES)
    def test_commutative(self, seq1, seq2, expected, expected_normalized):
        assert damerau_levenshtein_distance(seq2, seq1) == expected

    def test_returns_int(self):
        assert type(damerau_levenshtein_distance('abc', 'abd')) is int

    def test_matches_reference_exhaustively(self):
        # every pair of strings up to length 4 over a 3-letter alphabet covers all transposition/prefix interactions
        strings = [''.join(chars) for n in range(5) for chars in itertools.product('abc', repeat=n)]
        mismatches = [
            (seq1, seq2)
            for seq1 in strings
            for seq2 in strings
            if damerau_levenshtein_distance(seq1, seq2) != osa_distance(seq1, seq2)
        ]
        assert mismatches == []

    def test_matches_reference_randomly(self):
        mismatches = [
            (seq1, seq2)
            for seq1, seq2 in random_string_pairs(count=2000, alphabet='abcd', max_len=20, seed=0)
            if damerau_levenshtein_distance(seq1, seq2) != osa_distance(seq1, seq2)
        ]
        assert mismatches == []


class TestDamerauLevenshteinDistanceMaxDistance:
    @pytest.mark.parametrize(
        ('seq1', 'seq2', 'max_distance', 'expected'),
        [
            pytest.param('smtih', 'smith', 2, 1, id='within'),
            pytest.param('smtih', 'smith', 1, 1, id='at-threshold'),
            pytest.param('saturday', 'sunday', 3, 3, id='at-threshold-longer'),
            pytest.param('saturday', 'sunday', 2, 3, id='exceeds'),
            pytest.param('orange', 'pumpkin', 3, 4, id='exceeds-early'),
            pytest.param('abc', 'abc', 0, 0, id='zero-identical'),
            pytest.param('abc', 'abd', 0, 1, id='zero-different'),
            pytest.param('', '', 0, 0, id='zero-both-empty'),
            pytest.param('', 'abc', 1, 2, id='first-empty-exceeds'),
            pytest.param('abc', '', 1, 2, id='second-empty-exceeds'),
            pytest.param('ab', 'abcdef', 2, 3, id='length-difference-exceeds'),
            pytest.param('abcdef', 'ab', 2, 3, id='length-difference-exceeds-swapped'),
            # the row minimum (1) never exceeds the threshold, so only the final-cell check catches this
            pytest.param('b', 'abc', 1, 2, id='exceeds-only-at-final-cell'),
            # after stripping the common prefix the shorter sequence is empty, so no rows are computed at all
            pytest.param('abc', 'abcd', 0, 1, id='exceeds-after-prefix-strip'),
            pytest.param('abc', 'xyz', 100, 3, id='larger-than-lengths'),
            pytest.param([1, 2, 3], [1, 3, 2], 1, 1, id='list-at-threshold'),
            pytest.param([1, 2, 3], [1, 3, 2], 0, 1, id='list-exceeds'),
        ],
    )
    def test_max_distance(self, seq1, seq2, max_distance, expected):
        assert damerau_levenshtein_distance(seq1, seq2, max_distance=max_distance) == expected

    def test_none_means_unbounded(self):
        assert damerau_levenshtein_distance('orange', 'pumpkin', max_distance=None) == 7

    def test_positional_argument(self):
        assert damerau_levenshtein_distance('orange', 'pumpkin', 3) == 4

    def test_matches_reference_randomly(self):
        mismatches = []
        for seq1, seq2 in random_string_pairs(count=1000, alphabet='ab', max_len=15, seed=1):
            true_distance = osa_distance(seq1, seq2)
            for max_distance in range(8):
                expected = true_distance if true_distance <= max_distance else max_distance + 1
                if damerau_levenshtein_distance(seq1, seq2, max_distance=max_distance) != expected:
                    mismatches.append((seq1, seq2, max_distance))
        assert mismatches == []

    def test_negative_raises(self):
        with pytest.raises(ValueError, match='max_distance must be non-negative, got -1'):
            damerau_levenshtein_distance('abc', 'abd', max_distance=-1)

    @pytest.mark.parametrize('max_distance', ['1', 1.5, 1.0])
    def test_non_integer_raises(self, max_distance):
        with pytest.raises(TypeError):
            damerau_levenshtein_distance('abc', 'abd', max_distance=max_distance)

    def test_huge_value_is_unbounded(self):
        assert damerau_levenshtein_distance('orange', 'pumpkin', max_distance=2**100) == 7

    def test_seqs_negative_raises(self):
        with pytest.raises(ValueError, match='max_distance must be non-negative'):
            damerau_levenshtein_distance_seqs('abc', ['abd'], max_distance=-1)


class TestNormalizedDamerauLevenshteinDistance:
    @pytest.mark.parametrize(('seq1', 'seq2', 'expected', 'expected_normalized'), CASES)
    def test_normalized_distance(self, seq1, seq2, expected, expected_normalized):
        assert normalized_damerau_levenshtein_distance(seq1, seq2) == expected_normalized

    @pytest.mark.parametrize(('seq1', 'seq2', 'expected', 'expected_normalized'), CASES)
    def test_commutative(self, seq1, seq2, expected, expected_normalized):
        assert normalized_damerau_levenshtein_distance(seq2, seq1) == expected_normalized

    @pytest.mark.parametrize(('seq1', 'seq2'), [('abc', 'abd'), ('', ''), ('abc', 'abc')])
    def test_returns_float(self, seq1, seq2):
        assert type(normalized_damerau_levenshtein_distance(seq1, seq2)) is float

    def test_within_unit_interval(self):
        for seq1, seq2 in random_string_pairs(count=500, alphabet='abc', max_len=10, seed=2):
            assert 0.0 <= normalized_damerau_levenshtein_distance(seq1, seq2) <= 1.0


class TestDamerauLevenshteinDistanceSeqs:
    def test_strings(self):
        seqs = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        assert damerau_levenshtein_distance_seqs('Saturday', seqs) == [3, 5, 5, 6, 4, 5, 0]

    def test_unicode(self):
        seqs = ['Sjöstedt', 'Sjostedt', 'Söstedt', 'Sjöedt']
        assert damerau_levenshtein_distance_seqs('Sjöstedt', seqs) == [0, 1, 1, 2]

    def test_empty_seqs(self):
        assert damerau_levenshtein_distance_seqs('abc', []) == []

    def test_non_string_sequences(self):
        assert damerau_levenshtein_distance_seqs([1, 2, 3], [[1, 2, 3], [1, 3, 2], []]) == [0, 1, 3]

    def test_tuple_of_seqs(self):
        assert damerau_levenshtein_distance_seqs('abc', ('abc', 'acb', '')) == [0, 1, 3]

    def test_generator_of_seqs(self):
        assert damerau_levenshtein_distance_seqs('abc', (s for s in ['abc', 'acb', ''])) == [0, 1, 3]

    def test_matches_single_distance(self):
        seqs = ['', 'a', 'ab', 'ba', 'abc', 'cab', 'xyz']
        assert damerau_levenshtein_distance_seqs('abc', seqs) == [damerau_levenshtein_distance('abc', s) for s in seqs]

    def test_max_distance(self):
        seqs = ['Sunday', 'Monday', 'Saturday']
        assert damerau_levenshtein_distance_seqs('Saturday', seqs, max_distance=3) == [3, 4, 0]

    def test_max_distance_positional(self):
        assert damerau_levenshtein_distance_seqs('Saturday', ['Sunday', 'Monday'], 3) == [3, 4]


class TestNormalizedDamerauLevenshteinDistanceSeqs:
    def test_strings(self):
        seqs = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        expected = [0.375, 0.625, 0.625, 2 / 3, 0.5, 0.625, 0.0]
        assert normalized_damerau_levenshtein_distance_seqs('Saturday', seqs) == expected

    def test_unicode(self):
        seqs = ['Sjöstedt', 'Sjostedt', 'Söstedt', 'Sjöedt']
        assert normalized_damerau_levenshtein_distance_seqs('Sjöstedt', seqs) == [0.0, 0.125, 0.125, 0.25]

    def test_empty_seqs(self):
        assert normalized_damerau_levenshtein_distance_seqs('abc', []) == []

    def test_non_string_sequences(self):
        assert normalized_damerau_levenshtein_distance_seqs([1, 2, 3], [[1, 2, 3], [1, 3, 2]]) == [0.0, 1 / 3]

    def test_generator_of_seqs(self):
        assert normalized_damerau_levenshtein_distance_seqs('abc', (s for s in ['abc', 'ab'])) == [0.0, 1 / 3]


class TestInvalidInputs:
    @pytest.mark.parametrize('func', [damerau_levenshtein_distance, normalized_damerau_levenshtein_distance])
    @pytest.mark.parametrize(
        ('seq1', 'seq2', 'message'),
        [
            pytest.param(None, 'abc', 'seq1 must be a sequence, got None', id='seq1-none'),
            pytest.param('abc', None, 'seq2 must be a sequence, got None', id='seq2-none'),
            pytest.param(None, None, 'seq1 must be a sequence, got None', id='both-none'),
        ],
    )
    def test_none(self, func, seq1, seq2, message):
        with pytest.raises(TypeError, match=message):
            func(seq1, seq2)

    @pytest.mark.parametrize('func', PUBLIC_API)
    def test_seq_none(self, func):
        with pytest.raises(TypeError, match='seq1 must be a sequence, got None'):
            func(None, ['abc'])

    @pytest.mark.parametrize('func', SEQS_API)
    def test_seqs_none(self, func):
        with pytest.raises(TypeError, match='not iterable'):
            func('abc', None)

    @pytest.mark.parametrize('func', SEQS_API)
    def test_seqs_element_none(self, func):
        with pytest.raises(TypeError, match='seq2 must be a sequence, got None'):
            func('abc', ['abc', None])

    @pytest.mark.parametrize('func', [damerau_levenshtein_distance, normalized_damerau_levenshtein_distance])
    @pytest.mark.parametrize(
        ('seq1', 'seq2'),
        [
            pytest.param(1, 'abc', id='int'),
            pytest.param(iter('abc'), 'abc', id='iterator'),
            pytest.param({1, 2}, [1, 2], id='set'),
        ],
    )
    def test_non_sequence(self, func, seq1, seq2):
        with pytest.raises(TypeError):
            func(seq1, seq2)


class TestPublicApi:
    def test_exports(self):
        public_names = {name for name in dir(pyxdameraulevenshtein) if not name.startswith('_')}
        assert public_names == {func.__name__ for func in PUBLIC_API}

    def test_docstring_examples(self):
        results = doctest.testmod(pyxdameraulevenshtein._initialize)
        assert results.attempted > 0
        assert results.failed == 0
