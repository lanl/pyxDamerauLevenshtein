"""
	Copyright (c) 2013, Los Alamos National Security, LLC
	All rights reserved.

	Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
	following conditions are met:

	* Redistributions of source code must retain the above copyright notice, this list of conditions and the following
	  disclaimer.
	* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
	  following disclaimer in the documentation and/or other materials provided with the distribution.
	* Neither the name of Los Alamos National Security, LLC nor the names of its contributors may be used to endorse or
	  promote products derived from this software without specific prior written permission.

	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
	INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
	DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
	SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
	SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
	WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
	THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from libc.stdlib cimport calloc, free

#these guys are used to index into storage inside damerau_levenshtein_distance()
cdef Py_ssize_t TWO_AGO = 0
cdef Py_ssize_t ONE_AGO = 1
cdef Py_ssize_t THIS_ROW = 2

cdef unicode to_unicode(s):
	"""
		Convert s to a proper unicode type (handles difference between Python 2 and 3). Code comes from
		https://groups.google.com/d/msg/cython-users/ofT3fo48ohs/rrf3dtbHkm4J
	"""
	if isinstance(s, bytes):
		return (<bytes>s).decode('UTF-8')
	return s

cpdef Py_ssize_t damerau_levenshtein_distance(seq1, seq2):
	"""
		Return the edit distance. This implementation is based on http://mwh.geek.nz/2009/04/26/python-damerau-levenshtein-distance/
		and runs in O(N*M) time using O(M) space. Because this returns a C Py_ssize_t, the corresponding Python data type will be long (see
		http://docs.cython.org/src/reference/language_basics.html#automatic-type-conversion for more information).

		Examples:

		>>> damerau_levenshtein_distance('smtih', 'smith')
		1
		>>> damerau_levenshtein_distance('saturday', 'sunday')
		3
		>>> damerau_levenshtein_distance('orange', 'pumpkin')
		7
	"""

	s1 = to_unicode(seq1)
	s2 = to_unicode(seq2)

	#possible short-circuit if words have a lot in common at the beginning (or are identical)
	cdef Py_ssize_t first_differing_index = 0
	while first_differing_index < len(s1) and first_differing_index < len(s2) and s1[first_differing_index] == s2[first_differing_index]:
		first_differing_index += 1
	
	s1 = s1[first_differing_index:]
	s2 = s2[first_differing_index:]

	if not s1:
		return len(s2)
	if not s2:
		return len(s1)
	
	cdef Py_ssize_t i, j
	cdef Py_ssize_t offset = len(s2) + 1
	cdef Py_ssize_t delete_cost, add_cost, subtract_cost, edit_distance

	#storage is a 3 x (len(s2) + 1) array that stores two_ago, one_ago, and this_row
	cdef Py_ssize_t *storage = <Py_ssize_t *>calloc(3 * offset, sizeof(Py_ssize_t))
	if not storage:
		raise MemoryError()

	try:
		#initialize this_row
		for i in xrange(1, offset):
			storage[THIS_ROW * offset + (i - 1)] = i
		
		for i in xrange(len(s1)):
			#swap/initialize vectors
			for j in xrange(offset):
				storage[TWO_AGO * offset + j] = storage[ONE_AGO * offset + j]
				storage[ONE_AGO * offset + j] = storage[THIS_ROW * offset + j]
			for j in xrange(len(s2)):
				storage[THIS_ROW * offset + j] = 0
			storage[THIS_ROW * offset + len(s2)] = i + 1

			#now compute costs
			for j in xrange(len(s2)):
				delete_cost = storage[ONE_AGO * offset + j] + 1
				add_cost = storage[THIS_ROW * offset + (j - 1 if j > 0 else len(s2))] + 1
				subtract_cost = storage[ONE_AGO * offset + (j - 1 if j > 0 else len(s2))] + (s1[i] != s2[j])
				storage[THIS_ROW * offset + j] = min(delete_cost, add_cost, subtract_cost)
				#deal with transpositions
				if (i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j] and s1[i] != s2[j]):
					storage[THIS_ROW * offset + j] = min(storage[THIS_ROW * offset + j], storage[TWO_AGO * offset + j - 2 if j > 1 else len(s2)] + 1)
		edit_distance = storage[THIS_ROW * offset + (len(s2) - 1)]
	finally:
		#free dynamically-allocated memory
		free(storage)

	return edit_distance

cpdef double normalized_damerau_levenshtein_distance(seq1, seq2):
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
	return float(damerau_levenshtein_distance(seq1, seq2)) / max(len(to_unicode(seq1)), len(to_unicode(seq2)))
