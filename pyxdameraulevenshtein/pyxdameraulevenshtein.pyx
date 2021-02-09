# cython: language_level=3

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

from libc.stdlib cimport calloc, free


# these guys are used to index into storage inside damerau_levenshtein_distance()
cdef Py_ssize_t TWO_AGO = 0
cdef Py_ssize_t ONE_AGO = 1
cdef Py_ssize_t THIS_ROW = 2


cpdef unsigned long damerau_levenshtein_distance(seq1, seq2):
    """
        Return the edit distance. This implementation is based on Michael Homer's implementation
        (https://web.archive.org/web/20150909134357/http://mwh.geek.nz:80/2009/04/26/python-damerau-levenshtein-distance/)
        and runs in O(N*M) time using O(M) space. This code implements the "optimal string alignment distance"
        algorithm, as described in Wikipedia here:
        https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance#Optimal_string_alignment_distance

        Note that `seq1` and `seq2` can be any sequence type. This not only includes `str` but also includes `list`,
        `tuple`, `range`, and more.

        Examples:

        >>> damerau_levenshtein_distance('smtih', 'smith')
        1
        >>> damerau_levenshtein_distance('saturday', 'sunday')
        3
        >>> damerau_levenshtein_distance('orange', 'pumpkin')
        7
        >>> damerau_levenshtein_distance([1, 2, 3, 4, 5, 6], [7, 8, 9, 7, 10, 11, 4])
        7
    """
    # possible short-circuit if sequences have a lot in common at the beginning (or are identical)
    cdef Py_ssize_t first_differing_index = 0
    while first_differing_index < len(seq1) and \
          first_differing_index < len(seq2) and \
          seq1[first_differing_index] == seq2[first_differing_index]:
        first_differing_index += 1

    seq1 = seq1[first_differing_index:]
    seq2 = seq2[first_differing_index:]

    if seq1 is None:
        return len(seq2)
    if seq2 is None:
        return len(seq1)

    # Fix bug where the second sequence is one shorter than the first (#22).
    if len(seq2) < len(seq1):
        seq1, seq2 = seq2, seq1

    # Py_ssize_t should be used wherever we're dealing with an array index or length
    cdef Py_ssize_t i, j
    cdef Py_ssize_t offset = len(seq2) + 1
    cdef unsigned long delete_cost, add_cost, subtract_cost, edit_distance

    # storage is a 3 x (len(seq2) + 1) array that stores TWO_AGO, ONE_AGO, and THIS_ROW
    cdef unsigned long * storage = <unsigned long * >calloc(3 * offset, sizeof(unsigned long))
    if not storage:
        raise MemoryError()

    try:
        # initialize THIS_ROW
        for i in range(1, offset):
            storage[THIS_ROW * offset + (i - 1)] = i

        for i in range(len(seq1)):
            # swap/initialize vectors
            for j in range(offset):
                storage[TWO_AGO * offset + j] = storage[ONE_AGO * offset + j]
                storage[ONE_AGO * offset + j] = storage[THIS_ROW * offset + j]
            for j in range(len(seq2)):
                storage[THIS_ROW * offset + j] = 0
            storage[THIS_ROW * offset + len(seq2)] = i + 1

            # now compute costs
            for j in range(len(seq2)):
                delete_cost = storage[ONE_AGO * offset + j] + 1
                add_cost = storage[THIS_ROW * offset + (j - 1 if j > 0 else len(seq2))] + 1
                subtract_cost = storage[ONE_AGO * offset + (j - 1 if j > 0 else len(seq2))] + (seq1[i] != seq2[j])
                storage[THIS_ROW * offset + j] = min(delete_cost, add_cost, subtract_cost)
                # deal with transpositions
                if i > 0 and j > 0 and seq1[i] == seq2[j - 1] and seq1[i - 1] == seq2[j] and seq1[i] != seq2[j]:
                    storage[THIS_ROW * offset + j] = min(storage[THIS_ROW * offset + j],
                                                         storage[TWO_AGO * offset + j - 2 if j > 1 else len(seq2)] + 1)

        # compute and return the final edit distance
        return storage[THIS_ROW * offset + (len(seq2) - 1)]
    finally:
        # free dynamically-allocated memory
        free(storage)


cpdef float normalized_damerau_levenshtein_distance(seq1, seq2):
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
    # prevent division by zero for empty inputs
    n = max(len(seq1), len(seq2))
    return float(damerau_levenshtein_distance(seq1, seq2)) / max(n, 1)


cpdef list damerau_levenshtein_distance_seqs(seq, seqs):
    """
        For each sequence in `seqs`, compute the DL distance between it and `seq`. A list of distances will be
        returned, one for each element in `seqs`.

        Because this code generates a list of distances, where each element's position corresponds to the index
        of the element we encounter as we iterate through `seqs`, `seqs` must be ordered. That is, do not use
        a data structure like a `set` because order is not guaranteed.

        Example:

        >>> damerau_levenshtein_distance_list('Sjöstedt', ['Sjöstedt', 'Sjostedt', 'Söstedt', 'Sjöedt'])
        [0, 1, 1, 2]
    """
    return [damerau_levenshtein_distance(seq, x) for x in seqs]


cpdef list normalized_damerau_levenshtein_distance_seqs(seq, seqs):
    """
        For each sequence in `seqs`, compute the normalized DL distance between it and `seq`. A list of normalized
        distances will be returned, one for each element in `seqs`.

        Because this code generates a list of normalized distances, where each element's position corresponds to the
        index of the element we encounter as we iterate through `seqs`, `seqs` must be ordered. That is, do not use
        a data structure like a `set` because order is not guaranteed.

        Example:

        >>> normalized_damerau_levenshtein_distance_seqs('Sjöstedt', ['Sjöstedt', 'Sjostedt', 'Söstedt', 'Sjöedt'])
        [0.0, 0.125, 0.125, 0.25]
    """
    return [normalized_damerau_levenshtein_distance(seq, x) for x in seqs]
