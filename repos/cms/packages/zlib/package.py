# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

# Although zlib comes with a configure script, it does not use Autotools
# The AutotoolsPackage causes zlib to fail to build with PGI
class Zlib(Package):
    """A free, general-purpose, legally unencumbered lossless
    data-compression library.
    """

    homepage = "http://zlib.net"

    if platform.machine() == "aarch64": 
        git = "https://github.com/madler/zlib.git"
        version('1.2.11.cms', tag='v1.2.11')
    else:
        git = "https://github.com/cms-externals/zlib.git"
        version('1.2.11.cms', commit='822f7f5a8c57802faf8bbfe16266be02eff8c2e2')

    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')
    variant('shared', default=True,
            description='Enables the build of shared libraries.')
    variant('optimize', default=True,
            description='Enable -O2 for a more optimized lib')

    patch('w_patch.patch', when="@1.2.11%cce")

    @property
    def libs(self):
        shared = '+shared' in self.spec
        return find_libraries(
            ['libz'], root=self.prefix, recursive=True, shared=shared
        )

    def setup_build_environment(self, env):
        if '+pic' in self.spec:
            env.append_flags('CFLAGS', self.compiler.cc_pic_flag)
        if '+optimize' in self.spec:
            env.append_flags('CFLAGS', '-O3')

        env.append_flags('CFLAGS', '-DUSE_MMAP')
        env.append_flags('CFLAGS', '-DUNALIGNED_OK')
        env.append_flags('CFLAGS', '-D_LARGEFILE64_SOURCE=1')
        if self.spec.target.family == 'x86_64':
            env.append_flags('CFLAGS', '-msse3')

    def install(self, spec, prefix):
        config_args = []
        if '~shared' in spec:
            config_args.append('--static')
        configure('--prefix={0}'.format(prefix), *config_args)

        make()
        if self.run_tests:
            make('check')
        make('install')
