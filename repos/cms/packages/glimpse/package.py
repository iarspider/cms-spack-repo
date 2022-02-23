# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


"""
debian/patches/01-cross
debian/patches/01-makefile
debian/patches/01-manpages
debian/patches/12-manpage-hyphen
debian/patches/15-manpage-url
debian/patches/20-bin-spelling
debian/patches/25-fix-double-free
debian/patches/30-manpage-spelling
"""
class Glimpse(AutotoolsPackage):
    """ glimpse - search quickly through entire file systems"""

    git = "https://github.com/cms-externals/glimpse.git"

    version('4.18.7-6', commit='5426ca983218befa4aeadf21cad2305d90c84adb')

    parallel = False

    patch('01-cross')
    patch('01-makefile')
    patch('01-manpages')
    patch('12-manpage-hyphen')
    patch('15-manpage-url')
    patch('20-bin-spelling')
    patch('25-fix-double-free')
    patch('30-manpage-spelling')

    @run_after('configure')
    def cmspatch(self):
        # Turn off this part, it causes problems for 32-bit-on-64-bit and is only
        # needed for webglimpse
        filter_file('dynfilters', '', 'Makefile')
