# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hector(MakefilePackage):
    """Hector"""

    homepage = "https://www.example.com"
    git      = "https://github.com/cms-externals/hector.git"

    version('1.3.4.patch1', commit='566e76718059fde2bf044579a2010a482b52a04a')

    depends_on('root')

    def edit(self, spec, prefix):
        mkdirp('obj')
        mkdirp('lib')
        makefile = FileFilter('Makefile')
        if spec.satisfies('platform=darwin'):
            makefile.filter('-rdynamic', '')
        makefile.filter('@g++', '$(CXX) $(CXXFLAGS)', string=True)

    def install(self, spec, prefix):
        install_tree('.', prefix)
