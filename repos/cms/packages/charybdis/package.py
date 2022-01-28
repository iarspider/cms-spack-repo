# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os, shutil, glob


class Charybdis(MakefilePackage):
    """Charybdin MC"""

    homepage = "https://www.example.com"
    url      = "http://cern.ch/service-spi/external/MCGenerators/distribution/charybdis/charybdis-1.003-src.tgz"

    version('1.003', sha256='354e19ac42cca3ec8c5a48398324c993b551d47ff64c317e466f2be02a3d1416')

    depends_on('pythia6')
    depends_on('lhapdf')
    depends_on('zlib')

    patch('charybdis-1003-macosx.patch', level=3)
    patch('charybdis-1.003-archive-only.patch', level=3, when='platform=darwin')

    def do_stage(self, mirror_only=False):
        super(Charybdis, self).do_stage(mirror_only)
        dn = os.listdir(self.stage.source_path)[0]
        for fn in os.listdir(join_path(self.stage.source_path, dn)):
            shutil.move(join_path(self.stage.source_path, dn, fn), join_path(self.stage.source_path, fn))
        shutil.rmtree(join_path(self.stage.source_path, dn))

    def setup_build_environment(self, env):
        env.set('PYTHIA6_ROOT', self.spec['pythia6'].prefix)
        env.set('LHAPDF_ROOT', self.spec['lhapdf'].prefix)
        env.set('ZLIB_ROOT', self.spec['zlib'].prefix)

    def edit(self, spec, prefix):
        filter_file('/bin/sh', '/bin/bash', 'configure')
        configure = Executable('./configure')
        configure('--lcgplatform=slc7_amd64_gcc900', '--pythia_hadronization')
        filter_file('FC = .*', 'FC = {0}'.format(self.compiler.fc), 'config.mk')
        filter_file('FFLAGS = (.*)', r'FFLAGS = \1 -fPIC', 'config.mk')

    def install(self, spec, prefix):
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
        for fn in glob.glob(prefix.lib.archive.join('*.a')):
            shutil.move(fn, prefix.lib)
        shutil.rmtree(prefix.lib.archive)