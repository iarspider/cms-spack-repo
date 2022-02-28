# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os
import shutil

class Herwig6(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "http://cern.ch/service-spi/external/MCGenerators/distribution/herwig/herwig-6.521-src.tgz"

    version('6.521', sha256='98aec5b8e5b50791af864436b13d5802b7371befac5ade5bc5773e112d2532a0')

    depends_on('lhapdf')
    depends_on('photos')

    patch('herwig-6.520-tauoladummy.patch', level=2)

    keep_archives = True

    def do_stage(self, mirror_only=False):
        super(Herwig6, self).do_stage(mirror_only)
        dn = os.listdir(self.stage.source_path)[0]
        for fn in os.listdir(join_path(self.stage.source_path, dn)):
            shutil.move(join_path(self.stage.source_path, dn, fn), join_path(self.stage.source_path, fn))
        shutil.rmtree(join_path(self.stage.source_path, dn))

    def configure_args(self):
        args = ['FFLAGS=-fPIC', '--disable-shared', '--enable-static']
        return args

    def build(self, spec, prefix):
        make('LHAPDF_ROOT=' + self.spec['lhapdf'].prefix, 'PHOTOS_ROOT=' + self.spec['photos'].prefix)
        make('check')

    @run_after('install')
    def fix_inc(self):
        target = self.spec.prefix.include.join('herwig65.inc')
        if self.spec.satisfies('platform=darwin'):
            force_symlink(self.spec.prefix.include.join('herwig6251.inc'), target)
        else:
            force_symlink(self.spec.prefix.include.join('HERWIG65.INC'), target)
