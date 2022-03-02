# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os
import shutil

class Mctester(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/mctester/mctester-1.25.0a-src.tgz"

    version('1.25.0a', sha256='d84f7b14a7bf7e7f71b4fbb1af046a07bdbfd814003843f14b29e508435453f3')

    depends_on('hepmc')
    depends_on('root')

    keep_archives = True  # -- CMS

    patch('mctester-cling.patch', level=2)
    patch('mctester-root6-tbuffer.patch', level=2)

    def configure_args(self):
        args = ['--with-HepMC=' + self.spec['hepmc'].prefix, '--with-root=' + self.spec['root'].prefix]
        return args

    def do_stage(self, mirror_only=False):
        super(Mctester, self).do_stage(mirror_only)
        dn = os.listdir(self.stage.source_path)[0]
        for fn in os.listdir(join_path(self.stage.source_path, dn)):
            shutil.move(join_path(self.stage.source_path, dn, fn), join_path(self.stage.source_path, fn))
        shutil.rmtree(join_path(self.stage.source_path, dn))


