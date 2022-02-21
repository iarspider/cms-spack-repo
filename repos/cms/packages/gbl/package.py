# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gbl(CMakePackage):
    """General Broken Lines: Advanced track fitting library"""

    homepage = "https://www.desy.de/~kleinwrt/GBL/doc/cpp/html/"
    git      = "https://gitlab.desy.de/claus.kleinwort/general-broken-lines.git"

    version('V02-01-03', tag="V02-01-03")

    depends_on('eigen', type=('build', 'link'))

    root_cmakelists_dir = 'cpp'

    def cmake_args(self):
        args = [self.define('EIGEN3_INCLUDE_DIR', self.spec['eigen'].prefix.include.eigen3),
                self.define('SUPPORT_ROOT', False)]
        return args
