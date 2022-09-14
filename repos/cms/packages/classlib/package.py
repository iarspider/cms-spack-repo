# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

class Classlib(AutotoolsPackage):
    homepage = "https://www.example.com"
    git      = "https://github.com/cms-externals/classlib.git"

    version('3.1.3', commit='76cff1e3c0be6c24a2a9c02fb2a0670b7a19c444')

    depends_on('pcre')

    def configure_args(self):
        args = ['--without-zlib', '--without-bz2lib',
                '--without-lzma', '--without-lzo',
                '--with-pcre-includes={0}'.format(self.spec['pcre'].prefix.include),
                '--with-pcre-libraries={0}'.format(self.spec['pcre'].prefix.lib)]
        return args

    def setup_build_environment(self, env):
        env.append_flags('CXXFLAGS', "-Wno-error=extra -Wno-error=cpp -ansi -pedantic -W -Wall -Wno-long-long -Werror -Wno-cast-function-type")

    @run_after('configure')
    def cmspatch(self):
        filter_file('-lz '     , ' ', 'Makefile')
        filter_file('-lbz2 '   , ' ', 'Makefile')
        filter_file('-lcrypto ', ' ', 'Makefile')
        filter_file('-llzma '  , ' ', 'Makefile')
        with working_dir(self.stage.source_path):
            perl_cmd = which('perl')
            perl_cmd('-p', '-i', '-e', "s{-llzo2}{}g;!/^\S+: / && s{\S+LZO((C|Dec)ompressor|Constants|Error)\S+}{}g", 'Makefile')
