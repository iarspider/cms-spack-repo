# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Csctrackfinderemulation(MakefilePackage):
    homepage = "https://www.example.com"
    git      = "https://github.com/cms-externals/CSCTrackFinderEmulation.git"

    version('1.2', commit='8c0287fde4739d96fd3fd4a03e5ce5e6b986052e')

    def patch(self, spec, prefix):
        filter_file('INSTALL_DIR:=.*', 'INSTALL_DIR:={0}'.format(prefix), 'makefile')
