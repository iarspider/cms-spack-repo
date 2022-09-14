# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libffi(AutotoolsPackage, SourcewarePackage):
    """The libffi library provides a portable, high level programming
    interface to various calling conventions. This allows a programmer
    to call any function specified by a call interface description at
    run time."""
    homepage = "https://sourceware.org/libffi/"
    url = "https://github.com/libffi/libffi/archive/refs/tags/v3.4.2.tar.gz"

    version('3.4.2',     sha256='0acbca9fd9c0eeed7e5d9460ae2ea945d3f1f3d48e13a4c54da12c7e0d23c313')
    version('3.3',       sha256='3f2f86094f5cf4c36cfe850d2fe029d01f5c2c2296619407c8ba0d8207da9a6b')
    version('3.2.1',     sha256='96d08dee6f262beea1a18ac9a3801f64018dc4521895e9198d029d6850febe23')

    patch('clang-powerpc-3.2.1.patch', when='@3.2.1%clang platform=linux')
    # ref.: https://github.com/libffi/libffi/pull/561
    patch('powerpc-3.3.patch', when='@3.3')

    drop_files = ['share']

    depends_on('autoconf', type='build', when='@3.4.2')
    depends_on('automake', type='build', when='@3.4.2')
    depends_on('libtool', type='build', when='@3.4.2')

    @property
    def headers(self):
        # The headers are probably in self.prefix.lib but we search everywhere
        return find_headers('ffi', self.prefix, recursive=True)

    def configure_args(self):
        args = ['--enable-portable-binary', '--disable-static', '--disable-dependency-tracking', '--disable-docs']  # -- CMS
        if self.spec.version >= Version('3.3'):
            # Spack adds its own target flags, so tell libffi not to
            # second-guess us
            args.append('--without-gcc-arch')
        # At the moment, build scripts accept 'aarch64-apple-darwin'
        # but not 'arm64-apple-darwin'.
        # See: https://github.com/libffi/libffi/issues/571
        if self.spec.satisfies('platform=darwin target=aarch64:'):
            args.append('--build=aarch64-apple-darwin')
        return args
