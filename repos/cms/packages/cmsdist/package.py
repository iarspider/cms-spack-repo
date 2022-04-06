# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cmsdist(Package):
    """Toolfile scripts from CMSDIST repo"""

    homepage = "https://www.example.com"
    git      = "https://github.com/cms-sw/cmsdist.git"

    version('12_4_X', commit='ec8cd99')

    def install(self, spec, prefix):
        install_tree('scram-tools.file', prefix)
