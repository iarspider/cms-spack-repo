# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ktjet(AutotoolsPackage):
    """KtJet is a C++ implementation of the Kt jet algorithm"""

    homepage = "https://ktjet.hepforge.org"
    url      = "http://www.hepforge.org/archive/ktjet/KtJet-1.06.tar.gz"

    version('1.06', sha256='e972ae739d2f373d9b1148bba6c4f97bb5dd74d417526388813ced6e991e3a92')
    patch('ktjet-1.0.6-nobanner.patch')

    depends_on('clhep')

    def configure_args(self):
        args = ['--with-clhep=' + self.spec['clhep'].prefix]
        return args
