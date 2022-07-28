# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pyquen(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.example.com"
    url      = "http://lokhtin.web.cern.ch/lokhtin/pyquen/pyquen-1.5.4.tar.gz"

    version('1.5.4', sha256='85a5539ae4df17700b1ff0d794a3f97a12c69477574bdd3fad7b43d036bfd037')

    depends_on('pythia6')
    depends_on('lhapdf')

    def cmake_args(self):
        return [self.define('PYTHIA6_DIR', self.spec['pythia6'].prefix)]

