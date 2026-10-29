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

from operator import index

from libc.stdlib cimport calloc, free

__all__ = [
    'damerau_levenshtein_distance',
    'damerau_levenshtein_distance_seqs',
    'normalized_damerau_levenshtein_distance',
    'normalized_damerau_levenshtein_distance_seqs',
]


cpdef Py_ssize_t damerau_levenshtein_distance(seq1, seq2, max_distance=None) except -1:
    """
        Return the edit distance. This implementation is based on Michael Homer's implementation
        (https://web.archive.org/web/20150909134357/http://mwh.geek.nz:80/2009/04/26/python-damerau-levenshtein-distance/)
        and runs in O(N*M) time using O(M) space. This code implements the "optimal string alignment distance"
        algorithm, as described in Wikipedia here:
        https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance#Optimal_string_alignment_distance

        Note that `seq1` and `seq2` can be any sequence type that supports `len()` and integer indexing. This not only
        includes `str` but also includes `bytes`, `list`, `tuple`, `range`, and more. Elements are compared with `==`.

        If `max_distance` is provided and the true distance exceeds it, `max_distance + 1` is returned instead. The
        computation stops as soon as the threshold is known to be exceeded, which avoids computing the full distance
        when only a threshold check is needed. `max_distance` must be a non-negative integer.

        Examples:

        >>> damerau_levenshtein_distance('smtih', 'smith')
        1
        >>> damerau_levenshtein_distance('saturday', 'sunday')
        3
        >>> damerau_levenshtein_distance('orange', 'pumpkin')
        7
        >>> damerau_levenshtein_distance([1, 2, 3, 4, 5, 6], [7, 8, 9, 7, 10, 11, 4])
        7
        >>> damerau_levenshtein_distance('orange', 'pumpkin', max_distance=3)
        4
    """
    if seq1 is None:
        raise TypeError('seq1 must be a sequence, got None')
    if seq2 is None:
        raise TypeError('seq2 must be a sequence, got None')

    cdef Py_ssize_t seq1_len = len(seq1)
    cdef Py_ssize_t seq2_len = len(seq2)

    # a threshold at or above the longer length can never be exceeded, so it is equivalent to no threshold (this also
    # keeps arbitrarily large Python ints from overflowing a C integer)
    cdef bint has_max_distance = False
    cdef Py_ssize_t limit = 0
    if max_distance is not None:
        max_distance = index(max_distance)
        if max_distance < 0:
            raise ValueError(f'max_distance must be non-negative, got {max_distance}')
        if max_distance < max(seq1_len, seq2_len):
            has_max_distance = True
            limit = max_distance

    # possible short-circuit if sequences have a lot in common at the beginning (or are identical); the common prefix is
    # skipped by offsetting indices rather than slicing to avoid copying
    cdef Py_ssize_t start = 0
    while start < seq1_len and start < seq2_len and seq1[start] == seq2[start]:
        start += 1

    # ensure seq2 is the longer sequence so that the row buffer is never empty while rows remain to be computed
    if seq2_len < seq1_len:
        seq1, seq2 = seq2, seq1
        seq1_len, seq2_len = seq2_len, seq1_len

    cdef Py_ssize_t n = seq1_len - start
    cdef Py_ssize_t m = seq2_len - start

    # the distance is at least the length difference, which is exactly the distance when seq1 has been exhausted
    if has_max_distance and m - n > limit:
        return limit + 1
    if n == 0:
        return m

    # three rolling rows of m + 1 entries each; the extra entry at index m holds the value for "column -1" (i.e., the
    # cost of deleting every element of seq1 seen so far), so j - 1 and j - 2 wrap around to it at the left edge
    cdef Py_ssize_t * storage = <Py_ssize_t *> calloc(3 * (m + 1), sizeof(Py_ssize_t))
    if not storage:
        raise MemoryError()  # pragma: no cover
    cdef Py_ssize_t * two_ago = storage
    cdef Py_ssize_t * one_ago = storage + (m + 1)
    cdef Py_ssize_t * this_row = storage + 2 * (m + 1)
    cdef Py_ssize_t * tmp

    cdef Py_ssize_t i, j, cost, best, row_min
    cdef object a, b, a_prev = None, b_prev = None

    try:
        # this_row represents the cost of transforming an empty seq1 into each prefix of seq2 (pure insertions)
        for j in range(m):
            this_row[j] = j + 1

        for i in range(n):
            # rotate rows: this_row becomes one_ago, one_ago becomes two_ago, and two_ago is reused as this_row
            tmp = two_ago
            two_ago = one_ago
            one_ago = this_row
            this_row = tmp
            this_row[m] = i + 1

            a = seq1[start + i]
            row_min = this_row[m]
            for j in range(m):
                b = seq2[start + j]
                cost = 0 if a == b else 1

                # take the cheapest of substitution, deletion, and insertion
                best = one_ago[j - 1 if j > 0 else m] + cost
                if one_ago[j] + 1 < best:
                    best = one_ago[j] + 1
                if this_row[j - 1 if j > 0 else m] + 1 < best:
                    best = this_row[j - 1 if j > 0 else m] + 1

                # deal with transpositions of adjacent elements
                if cost and i > 0 and j > 0 and a == b_prev and a_prev == b:
                    if two_ago[j - 2 if j > 1 else m] + 1 < best:
                        best = two_ago[j - 2 if j > 1 else m] + 1

                this_row[j] = best
                if best < row_min:
                    row_min = best
                b_prev = b
            a_prev = a

            # early termination: row minimums never decrease, so if this row's minimum already exceeds max_distance,
            # the final distance will also exceed it
            if has_max_distance and row_min > limit:
                return limit + 1

        # compute and return the final edit distance
        best = this_row[m - 1]
        if has_max_distance and best > limit:
            return limit + 1
        return best
    finally:
        # free dynamically-allocated memory (Cython's line tracing never reports this line, even though it always runs)
        free(storage)  # pragma: no cover


cpdef double normalized_damerau_levenshtein_distance(seq1, seq2):
    """
        Return a real number between 0.0 and 1.0, indicating the edit distance as a fraction of the longer sequence.
        0.0 means that the sequences are identical, while 1.0 means they have nothing in common.

        Note that this definition is the exact opposite of `difflib.SequenceMatcher.ratio()`. `difflib` outputs 1.0
        for identical sequences and 0.0 for unlike sequences.

        Examples:

        >>> normalized_damerau_levenshtein_distance('smtih', 'smith')
        0.2
        >>> normalized_damerau_levenshtein_distance('saturday', 'sunday')
        0.375
        >>> normalized_damerau_levenshtein_distance('orange', 'pumpkin')
        1.0
        >>> normalized_damerau_levenshtein_distance([1, 2, 3, 4, 5, 6], [7, 8, 9, 7, 10, 11, 4])
        1.0
    """
    if seq1 is None:
        raise TypeError('seq1 must be a sequence, got None')
    if seq2 is None:
        raise TypeError('seq2 must be a sequence, got None')

    # prevent division by zero for empty inputs
    cdef Py_ssize_t n = max(len(seq1), len(seq2))
    if n == 0:
        return 0.0
    return <double> damerau_levenshtein_distance(seq1, seq2) / n


cpdef list damerau_levenshtein_distance_seqs(seq, seqs, max_distance=None):
    """
        For each sequence in `seqs`, compute the DL distance between it and `seq`. A list of distances will be
        returned, one for each element in `seqs`.

        `seqs` can be any iterable of sequences (including a generator). Each element's position in the returned list
        corresponds to the order in which it is encountered while iterating through `seqs`, so `seqs` should be
        ordered. That is, do not use a data structure like a `set` because order is not guaranteed.

        If `max_distance` is provided, it is forwarded to each individual distance computation. See
        `damerau_levenshtein_distance` for details on its behavior.

        Examples:

        >>> damerau_levenshtein_distance_seqs('Sjöstedt', ['Sjöstedt', 'Sjostedt', 'Söstedt', 'Sjöedt'])
        [0, 1, 1, 2]
    """
    return [damerau_levenshtein_distance(seq, x, max_distance) for x in seqs]


cpdef list normalized_damerau_levenshtein_distance_seqs(seq, seqs):
    """
        For each sequence in `seqs`, compute the normalized DL distance between it and `seq`. A list of normalized
        distances will be returned, one for each element in `seqs`.

        `seqs` can be any iterable of sequences (including a generator). Each element's position in the returned list
        corresponds to the order in which it is encountered while iterating through `seqs`, so `seqs` should be
        ordered. That is, do not use a data structure like a `set` because order is not guaranteed.

        Examples:

        >>> normalized_damerau_levenshtein_distance_seqs('Sjöstedt', ['Sjöstedt', 'Sjostedt', 'Söstedt', 'Sjöedt'])
        [0.0, 0.125, 0.125, 0.25]
    """
    return [normalized_damerau_levenshtein_distance(seq, x) for x in seqs]
