# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Glimpse(AutotoolsPackage):
    """ glimpse - search quickly through entire file systems"""

    git = "https://github.com/cms-externals/glimpse.git"

    version('4.18.7-6', commit='5426ca983218befa4aeadf21cad2305d90c84adb')

    parallel = False
