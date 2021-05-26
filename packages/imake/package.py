# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Imake(AutotoolsPackage, XorgPackage):
    """The imake build system."""

    homepage = "http://www.snake.net/software/imake-stuff/"
    xorg_mirror_path = "util/imake-1.0.7.tar.gz"

    version('1.0.8', sha256='8178a09bfef33ad5f61cb5cb62283df7d3a5682f014507d2e7cfd922485a5c00')
    version('1.0.7', sha256='6bda266a07eb33445d513f1e3c82a61e4822ccb94d420643d58e1be5f881e5cb')

    depends_on('xproto')
    depends_on('xorg-cf-files', type='run')
    depends_on('pkgconfig', type='build')

    for dep in ['m4', 'autoconf', 'automake', 'libtool']:
        depends_on(dep, type='build', when='@1.0.8')

    # https://gitlab.freedesktop.org/xorg/util/imake/-/issues/2
    patch('imake.patch', when='@1.0.8', level=0)

    @property
    def force_autoreconf(self):
        return self.spec.satisfies('@1.0.8')

    def configure_args(self):
        args = []
        cfgdir = self.spec['xorg-cf-files'].prefix.lib.X11.config
        args.append('--with-config-dir={0}'.format(cfgdir))
        return args
