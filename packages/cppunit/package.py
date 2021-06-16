# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cppunit(AutotoolsPackage):
    """Obsolete Unit testing framework for C++"""

    homepage = "https://wiki.freedesktop.org/www/Software/cppunit/"
    url = "http://dev-www.libreoffice.org/src/cppunit-1.13.2.tar.gz"
    git = "https://anongit.freedesktop.org/git/libreoffice/cppunit.git"

    version('1.15.x', commit='78e64f0edb4f3271a6ddbcdf9cba05138597bfca') # -- CMS
    version('1.14.0', sha256='3d569869d27b48860210c758c4f313082103a5e58219a7669b52bfd29d674780')
    version('1.13.2', sha256='3f47d246e3346f2ba4d7c9e882db3ad9ebd3fcbd2e8b732f946e0e3eeb9f429f')
    
    patch('cppunit-1.14-defaulted-function-deleted.patch', when='@1.15.x')
    drop_files = ['share', 'lib/*.a', 'lib/*.la']

    variant('cxxstd',
            default='default',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    def setup_build_environment(self, env):
        cxxstd = self.spec.variants['cxxstd'].value
        cxxstdflag = '' if cxxstd == 'default' else \
                     getattr(self.compiler, 'cxx{0}_flag'.format(cxxstd))
        env.append_flags('CXXFLAGS', cxxstdflag)
        
    def configure_args(self, spec, prefix):
        return ['--disable-static'] # -- CMS
