# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Meschach(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "http://www.math.uiowa.edu/~dstewart/meschach/mesch12b.tar.gz"

    version('1.2.pCMS1', sha256='8561f3a8d65e3b6850e3f5ae585e1be47304db1d5fa900508113dc10e2a2c00f',
            url='http://homepage.divms.uiowa.edu/~dstewart/meschach/mesch12b.tar.gz')

    keep_archives = True
    patch('meschach-1.2-slc4.patch', level=0)
    patch('meschach-1.2b-fPIC.patch', level=0)
    parallel = False

    def patch(self):
        if self.spec.satisfies('platform=darwin'):
            filter_file('define HAVE_MALLOC_H 1', 'undef MALLOCDECL', 'machine.h')

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        mkdirp(prefix.lib)
        make()

        install('*.h', prefix.include)
        install('meschach.a', join_path(prefix.lib, 'libmeschach.a'))
