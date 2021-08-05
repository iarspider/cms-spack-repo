# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Re2(CMakePackage):
    """RE2 is a fast, safe, thread-friendly alternative to backtracking
    regular expression engines like those used in PCRE, Perl, and Python."""

    homepage = "https://github.com/google/re2"
    url      = "https://github.com/google/re2/archive/2020-08-01.tar.gz"

    version('2021-06-01', sha256='26155e050b10b5969e986dab35654247a3b1b295e0532880b5a9c13c0a700ceb')
    version('2020-08-01', sha256='6f4c8514249cd65b9e85d3e6f4c35595809a63ad71c5d93083e4d1dcdf9e0cd6')
    version('2020-04-01', sha256='98794bc5416326817498384a9c43cbb5a406bab8da9f84f83c39ecad43ed5cea')

    variant('shared', default=False,
            description='Build shared instead of static libraries')

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS:Bool={0}'.format(
            'ON' if '+shared' in self.spec else 'OFF')]

        return args
