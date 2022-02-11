# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fftjet(AutotoolsPackage):
    """The purpose of the FFTJet package is reconstruction of particle jets in High Energy Physics collider data."""

    homepage = "https://fftjet.hepforge.org/"
    url      = "http://www.hepforge.org/archive/fftjet/fftjet-1.5.0.tar.gz"

    version('1.5.0', sha256='a6bc6e864822932e4220d95aff3711a62ba3710a0cfc5a80a195f87c87263f53')

    keep_archives = True  # -- CMS
    depends_on('fftw')

    def configure_args(self):
        args = ["--disable-dependency-tracking", "--enable-threads",
                "--enable-static", "--disable-shared",
                'DEPS_CFLAGS=-I' + self.spec['fftw'].prefix.include,
                'DEPS_LIBS=-L' + self.spec['fftw'].prefix.lib + ' -lfftw3']
        return args
