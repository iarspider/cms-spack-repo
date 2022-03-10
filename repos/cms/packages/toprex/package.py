# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os
import shutil
import glob

class Toprex(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/toprex/toprex-4.23-src.tgz"

    patch('toprex-4.23-macosx.patch', level=3)
    patch('toprex-4.23-archive-only.patch', level=3)

    version('4.23', sha256='304a287cf802f565d79ebef13130678898b1fb5fe1faa68970f10be562747a4c')

    depends_on('pythia6')

    keep_archives=True

    def do_stage(self, mirror_only=False):
        super().do_stage(mirror_only)
        dn = os.listdir(self.stage.source_path)[0]
        for fn in os.listdir(join_path(self.stage.source_path, dn)):
            shutil.move(join_path(self.stage.source_path, dn, fn), join_path(self.stage.source_path, fn))
        shutil.rmtree(join_path(self.stage.source_path, dn))

    def edit(self, spec, prefix):
        filter_file('-fno-globals', '', 'configure')
        filter_file('-finit-local-zero', '', 'configure')
        filter_file('-fugly-logint', '', 'configure')
        filter_file('export FC=(.*)', r'#export FC=\1', 'configure')
        filter_file('export CC=(.*)', r'#export CC=\1', 'configure')
        filter_file('export FFLAGS_OPT="-O2 -Wuninitialized"', 'export FFLAGS_OPT="-O2 -Wuninitialized -fPIC"', 'configure', string=True)
        filter_file('export CFLAGS_OPT="-O2"', 'export CFLAGS_OPT="-O2 -fPIC"', 'configure', string=True)
        filter_file('export CXXFLAGS_OPT="-O2', 'export CXXFLAGS_OPT="-O2 -fPIC ', 'configure', string=True)

        bash = which('bash')
        bash('./configure')

    def setup_build_environment(self, env):
        env.set('PYTHIA6_ROOT', self.spec['pythia6'].prefix.libs)

    def install(self, spec, prefix):
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
        for fn in glob.glob(prefix.lib.archive.join('*.a')):
            shutil.move(fn, prefix.lib)
        shutil.rmtree(prefix.lib.archive)

