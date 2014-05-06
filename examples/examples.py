#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance
import random
import string
import timeit

print('#edit distances (low edit distance means words are similar):')
print("damerau_levenshtein_distance('%s', '%s') = %d" % ('smtih', 'smith', damerau_levenshtein_distance('smtih', 'smith')))
print("damerau_levenshtein_distance('%s', '%s') = %d" % ('snapple', 'apple', damerau_levenshtein_distance('snapple', 'apple')))
print("damerau_levenshtein_distance('%s', '%s') = %d" % ('testing', 'testtn', damerau_levenshtein_distance('testing', 'testtn')))
print("damerau_levenshtein_distance('%s', '%s') = %d" % ('saturday', 'sunday', damerau_levenshtein_distance('saturday', 'sunday')))
print("damerau_levenshtein_distance('%s', '%s') = %d" % ('Saturday', 'saturday', damerau_levenshtein_distance('Saturday', 'saturday')))
print("damerau_levenshtein_distance('%s', '%s') = %d" % ('orange', 'pumpkin', damerau_levenshtein_distance('orange', 'pumpkin')))
print("damerau_levenshtein_distance('%s', '%s') = %d #unicode example\n" % ('Sjöstedt', 'Sjostedt', damerau_levenshtein_distance('Sjöstedt', 'Sjostedt'))) #unicode example

print('#normalized edit distances (low ratio means words are similar):')
print("normalized_damerau_levenshtein_distance('%s', '%s') = %f" % ('smtih', 'smith', normalized_damerau_levenshtein_distance('smtih', 'smith')))
print("normalized_damerau_levenshtein_distance('%s', '%s') = %f" % ('snapple', 'apple', normalized_damerau_levenshtein_distance('snapple', 'apple')))
print("normalized_damerau_levenshtein_distance('%s', '%s') = %f" % ('testing', 'testtn', normalized_damerau_levenshtein_distance('testing', 'testtn')))
print("normalized_damerau_levenshtein_distance('%s', '%s') = %f" % ('saturday', 'sunday', normalized_damerau_levenshtein_distance('saturday', 'sunday')))
print("normalized_damerau_levenshtein_distance('%s', '%s') = %f" % ('Saturday', 'saturday', normalized_damerau_levenshtein_distance('Saturday', 'saturday')))
print("normalized_damerau_levenshtein_distance('%s', '%s') = %f" % ('orange', 'pumpkin', normalized_damerau_levenshtein_distance('orange', 'pumpkin')))
print("normalized_damerau_levenshtein_distance('%s', '%s') = %f #unicode example\n" % ('Sjöstedt', 'Sjostedt', normalized_damerau_levenshtein_distance('Sjöstedt', 'Sjostedt'))) #unicode example

print('#performance testing:')

#random words will be comprised of ascii letters, numbers, and spaces
chars = string.ascii_letters + string.digits + ' '
word1 = ''.join([random.choice(chars) for i in range(30)]) #generate a random string of characters of length 30
word2 = ''.join([random.choice(chars) for i in range(30)]) #and another
print("""timeit.timeit("damerau_levenshtein_distance('%s', '%s')", 'from pyxdameraulevenshtein import damerau_levenshtein_distance', number=500000) = %f seconds""" % \
	(word1, word2, timeit.timeit("damerau_levenshtein_distance('%s', '%s')" % (word1, word2), 'from pyxdameraulevenshtein import damerau_levenshtein_distance', number=500000)))
print("""timeit.timeit("damerau_levenshtein_distance('%s', '%s')", 'from pyxdameraulevenshtein import damerau_levenshtein_distance', number=500000) = %f seconds #short-circuit makes this faster""" % \
	(word1, word1, timeit.timeit("damerau_levenshtein_distance('%s', '%s')" % (word1, word1), 'from pyxdameraulevenshtein import damerau_levenshtein_distance', number=500000)))
