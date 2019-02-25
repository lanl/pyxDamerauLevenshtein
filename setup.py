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
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys

from setuptools import setup, Extension
import numpy


metadata = dict(
    name='pyxDamerauLevenshtein',
    version='1.5.3',
    description='pyxDamerauLevenshtein implements the Damerau-Levenshtein (DL) edit '
                'distance algorithm for Python in Cython for high performance.',
    long_description='pyxDamerauLevenshtein implements the Damerau-Levenshtein (DL) '
                     'edit distance algorithm for Python in Cython for high performance. '
                     'Courtesy `Wikipedia <http://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance>`_: '
                     'In information theory and computer science, the '
                     'Damerau-Levenshtein distance (named after Frederick J. Damerau and '
                     'Vladimir I. Levenshtein) is a "distance" (string metric) between '
                     'two strings, i.e., finite sequence of symbols, given by counting '
                     'the minimum number of operations needed to transform one string '
                     'into the other, where an operation is defined as an insertion, '
                     'deletion, or substitution of a single character, or a '
                     'transposition of two adjacent characters. This implementation is '
                     'based on `Michael Homer\'s pure Python implementation '
                     '<https://web.archive.org/web/20150909134357/http://mwh.geek.nz:80/2009/04/26/python-damerau-levenshtein-distance/>`_, '
                     'which implements the `optimal string alignment distance algorithm '
                     '<https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance#Optimal_string_alignment_distance>`_. '
                     'It runs in ``O(N*M)`` time using ``O(M)`` space. It supports '
                     'unicode characters. For more information on pyxDamerauLevenshtein, '
                     'visit the `GitHub project page <https://github.com/gfairchild/pyxDamerauLevenshtein>`_.',
    author='Geoffrey Fairchild',
    author_email='mail@gfairchild.com',
    maintainer='Geoffrey Fairchild',
    maintainer_email='mail@gfairchild.com',
    url='https://github.com/gfairchild/pyxDamerauLevenshtein',
    license='BSD 3-Clause License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ]
)

setup(
    install_requires=['numpy>=1.16.1'],
    ext_modules=[Extension('pyxdameraulevenshtein', ['pyxdameraulevenshtein/pyxdameraulevenshtein.c'],
                           include_dirs=[numpy.get_include()])],
    **metadata
)
