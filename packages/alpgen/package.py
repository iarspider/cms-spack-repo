# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Alpgen(Package):
    """A collection of codes for the generation of
       multi-parton processes in hadronic collisions."""

    homepage = "http://mlm.home.cern.ch/mlm/alpgen/"
    url      = "https://mlm.home.cern.ch/mlm/alpgen/V2.1/v214.tgz"

    version('214', sha256='2f43f7f526793fe5f81a3a3e1adeffe21b653a7f5851efc599ed69ea13985c5e')

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make('install')
