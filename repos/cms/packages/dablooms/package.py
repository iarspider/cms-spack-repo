# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dablooms(MakefilePackage):
    """Dablooms: A Scalable, Counting, Bloom Filter"""

    homepage = "https://github.com/bitly/dablooms/"
    url      = "https://github.com/bitly/dablooms/archive/v0.9.1.tar.gz"

    version('0.9.1', sha256='56702e212ebcf71a867a1eace90dd5a4a89ec5b7da96a899ec841aa5c6b1655a')

    def build(self, spec, prefix):
        make('all')

    def install(self, spec, prefix):
        make('install', 'prefix=' + prefix)
