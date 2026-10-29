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

import os

from Cython.Build import cythonize
from setuptools import Extension, setup

# PYXDL_COVERAGE=1 builds the extension with line tracing so that coverage.py (with the Cython.Coverage plugin) can
# measure _initialize.pyx; tracing slows the extension down considerably, so never use it for release builds
coverage = os.environ.get('PYXDL_COVERAGE') == '1'

extension = Extension(
    'pyxdameraulevenshtein._initialize',
    ['pyxdameraulevenshtein/_initialize.pyx'],
    # Cython.Coverage cannot read sys.monitoring events (Python 3.12+), so fall back to the legacy tracing API
    define_macros=[('CYTHON_TRACE_NOGIL', '1'), ('CYTHON_USE_SYS_MONITORING', '0')] if coverage else [],
)

setup(
    ext_modules=cythonize([extension], compiler_directives={'linetrace': coverage}, force=coverage),
)
