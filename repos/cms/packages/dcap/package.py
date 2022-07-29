# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import shutil


class Dcap(AutotoolsPackage):
    """dCache access protocol client library."""

    homepage = "https://github.com/dCache/dcap"
    url      = "https://github.com/cms-externals/dcap/archive/2.47.8.tar.gz"
    git      = "https://github.com/cms-externals/dcap.git"

    version('2.47.12', commit='5753eec777a47908a40de670094903ce6b13176b')
    version('2.47.8', sha256='050a8d20c241abf358d5d72586f9abc43940e61d9ec9480040ac7da52ec804ac')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('zlib',     type=('build', 'run'))

    # -- CMS hook
    strip_files = ['lib']
    drop_files = ['share']

    def patch(self):
        filter_file('library_includedir.*', r'library_includedir=$(includedir)', 'src/Makefile.am')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./bootstrap.sh')

    def configure_args(self):
        args = ['CFLAGS=-I' + self.spec['zlib'].prefix.include, 'LDFLAGS=-L' + self.spec['zlib'].prefix.lib]
        return args

    def build(self, spec, prefix):
        make('-C', 'src')

    def install(self, spec, prefix):
        make('-C', 'src', 'install')
        shutil.rmtree(join_path(prefix, 'share'))
