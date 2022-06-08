# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import glob

from spack import *


class TauolaF(MakefilePackage):
    """TAUOLA - a library of Monte Carlo programs to simulate decays of polarized tau leptons"""

    homepage = "http://wasm.home.cern.ch/wasm/f77.html"
    url      = "http://cern.ch/service-spi/external/MCGenerators/distribution/tauola/tauola-27.121.5-src.tgz"

    version('27.121.5', sha256='906c3ccffcf6f02f48de2469adffffad5026ca78d98e77da99a6ee2d6ca3633f')

    depends_on('pythia6')
    depends_on('photos-f')

    patch('tauola-27.121-gfortran-tauola-srs.patch', level=2)
    patch('tauola-27.121.5-configure-makefile-update.patch', level=2)
    patch('tauola-27.121.5-gfortran-taueta.patch', level=2)

    keep_archives = True

    def do_stage(self, mirror_only=False):
        super(TauolaF, self).do_stage(mirror_only)
        dn = os.listdir(self.stage.source_path)[0]
        for fn in os.listdir(join_path(self.stage.source_path, dn)):
            shutil.move(join_path(self.stage.source_path, dn, fn), join_path(self.stage.source_path, fn))
        shutil.rmtree(join_path(self.stage.source_path, dn))

    def setup_build_environment(self, env):
        env.set('PHOTOS_ROOT', self.spec['photos-f'].prefix.libs)

    def edit(self, spec, prefix):
        filter_file('export FC=g77', '#export FC=g77', 'configure')
        filter_file('export CC=g77', '#export CC=g77', 'configure')
        filter_file('export FFLAGS_OPT="-O2 -Wuninitialized"', 'export FFLAGS_OPT="-O2 -Wuninitialized -fPIC"', 'configure', string=True)
        filter_file('export CFLAGS_OPT="-O2"', 'export CFLAGS_OPT="-O2 -fPIC"', 'configure', string=True)
        bash = which('bash')
        bash('./configure', '--with-pythia6libs=' + self.spec['pythia6'].prefix.libs)

    def install(self, spec, prefix):
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
        for fn in glob.glob(prefix.lib.archive.join('*.a')):
            shutil.move(fn, prefix.lib)
        shutil.rmtree(prefix.lib.archive)
