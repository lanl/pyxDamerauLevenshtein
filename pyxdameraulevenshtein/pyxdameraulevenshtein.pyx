# cython: language_level=2

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

from cpython.version cimport PY_MAJOR_VERSION
from libc.stdlib cimport calloc, free
import numpy as np
cimport numpy as np

# these guys are used to index into storage inside damerau_levenshtein_distance()
cdef Py_ssize_t TWO_AGO = 0
cdef Py_ssize_t ONE_AGO = 1
cdef Py_ssize_t THIS_ROW = 2

cdef unicode _to_unicode(s):
    """
        Convert s to a proper unicode type, handling the differences between Python 2 and 3. This code
        comes from http://docs.cython.org/src/tutorial/strings.html#accepting-strings-from-python-code.
    """
    if type(s) is unicode:
        # fast path for most common case(s)
        return <unicode>s
    elif PY_MAJOR_VERSION < 3 and isinstance(s, bytes):
        # only accept byte strings in Python 2.x, not in Py3
        return (<bytes>s).decode('UTF-8')
    elif isinstance(s, unicode):
        # this works for NumPy strings
        return unicode(s)
    raise TypeError('string [{}] has an unrecognized type of [{}]'.format(s, type(s)))


cpdef unsigned long damerau_levenshtein_distance(seq1, seq2):
    """
        Return the edit distance. This implementation is based on Michael Homer's implementation
        (https://web.archive.org/web/20150909134357/http://mwh.geek.nz:80/2009/04/26/python-damerau-levenshtein-distance/)
        and runs in O(N*M) time using O(M) space. This code implements the "optimal string alignment distance"
        algorithm, as described in Wikipedia here:
        https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance#Optimal_string_alignment_distance

        Examples:

        >>> damerau_levenshtein_distance('smtih', 'smith')
        1
        >>> damerau_levenshtein_distance('saturday', 'sunday')
        3
        >>> damerau_levenshtein_distance('orange', 'pumpkin')
        7
    """
    if isinstance(seq1, (list, tuple)) and isinstance(seq2, (list, tuple)):
        s1 = seq1
        s2 = seq2
    else:
        s1 = _to_unicode(seq1)
        s2 = _to_unicode(seq2)

    # possible short-circuit if words have a lot in common at the beginning (or are identical)
    cdef Py_ssize_t first_differing_index = 0
    while first_differing_index < len(s1) and \
          first_differing_index < len(s2) and \
          s1[first_differing_index] == s2[first_differing_index]:
        first_differing_index += 1

    s1 = s1[first_differing_index:]
    s2 = s2[first_differing_index:]

    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    # Py_ssize_t should be used wherever we're dealing with an array index or length
    cdef Py_ssize_t i, j
    cdef Py_ssize_t offset = len(s2) + 1
    cdef unsigned long delete_cost, add_cost, subtract_cost, edit_distance

    # storage is a 3 x (len(s2) + 1) array that stores TWO_AGO, ONE_AGO, and THIS_ROW
    cdef unsigned long * storage = <unsigned long * >calloc(3 * offset, sizeof(unsigned long))
    if not storage:
        raise MemoryError()

    try:
        # initialize THIS_ROW
        for i in range(1, offset):
            storage[THIS_ROW * offset + (i - 1)] = i

        for i in range(len(s1)):
            # swap/initialize vectors
            for j in range(offset):
                storage[TWO_AGO * offset + j] = storage[ONE_AGO * offset + j]
                storage[ONE_AGO * offset + j] = storage[THIS_ROW * offset + j]
            for j in range(len(s2)):
                storage[THIS_ROW * offset + j] = 0
            storage[THIS_ROW * offset + len(s2)] = i + 1

            # now compute costs
            for j in range(len(s2)):
                delete_cost = storage[ONE_AGO * offset + j] + 1
                add_cost = storage[THIS_ROW * offset + (j - 1 if j > 0 else len(s2))] + 1
                subtract_cost = storage[ONE_AGO * offset + (j - 1 if j > 0 else len(s2))] + (s1[i] != s2[j])
                storage[THIS_ROW * offset + j] = min(delete_cost, add_cost, subtract_cost)
                # deal with transpositions
                if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j] and s1[i] != s2[j]:
                    storage[THIS_ROW * offset + j] = min(storage[THIS_ROW * offset + j],
                                                         storage[TWO_AGO * offset + j - 2 if j > 1 else len(s2)] + 1)

        # compute and return the final edit distance
        return storage[THIS_ROW * offset + (len(s2) - 1)]
    finally:
        # free dynamically-allocated memory
        free(storage)


cpdef float normalized_damerau_levenshtein_distance(seq1, seq2):
    """
        Return a real number between 0.0 and 1.0, indicating the edit distance as a fraction of the longer
        string. 0.0 means that the sequences are identical, while 1.0 means they have nothing in common.

        Note that this definition is the exact opposite of difflib.SequenceMatcher.ratio(). difflib outputs
        1.0 for identical sequences and 0.0 for unlike sequences.

        Examples:

        >>> normalized_damerau_levenshtein_distance('smtih', 'smith')
        0.2
        >>> normalized_damerau_levenshtein_distance('saturday', 'sunday')
        0.375
        >>> normalized_damerau_levenshtein_distance('orange', 'pumpkin')
        1.0
    """
    if isinstance(seq1, (list, tuple)) and isinstance(seq2, (list, tuple)):
        n = max(len(seq1), len(seq2))
    else:
        n = max(len(_to_unicode(seq1)), len(_to_unicode(seq2)))

    # prevent division by zero for empty inputs
    return float(damerau_levenshtein_distance(seq1, seq2)) / max(n, 1)


cpdef np.ndarray[np.uint32_t, ndim=1] damerau_levenshtein_distance_ndarray(seq, np.ndarray array):
    """
        For each element in the array, compute the DL distance between it and seq. An array of distances will
        be returned, 1 for each element in the array.
    """
    dl = np.vectorize(damerau_levenshtein_distance, otypes=[np.uint32])
    return dl(seq, array)


cpdef np.ndarray[np.float32_t, ndim=1] normalized_damerau_levenshtein_distance_ndarray(seq, np.ndarray array):
    """
        For each element in the array, compute the normalized DL distance between it and seq. An array of
        normalized distances will be returned, 1 for each element in the array.
    """
    ndl = np.vectorize(normalized_damerau_levenshtein_distance, otypes=[np.float32])
    return ndl(seq, array)
