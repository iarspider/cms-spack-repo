# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os
import shutil

class Jimmy(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.example.com"
    url      = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/jimmy/jimmy-4.2-src.tgz"

    version('4.2', sha256='8fad71b9ce355f7def8f380ea2c72a47f1e39b6afb810a5322cf3226151c05c7')

    depends_on('herwig6')
    patch('jimmy-4.2-configure-update.patch', level=2)
    keep_archives = True

    phases = ['configure', 'build', 'install']

    def patch(self):
        filter_file('#!/bin/sh', '#!/bin/bash', 'configure', string=True)

    def configure(self, spec, prefix):
        args = ['--with-herwig=' + self.spec['herwig6'].prefix]
        configure_ = Executable('./configure')
        configure_(*args)

    def build(self, spec, prefix):
        make("HERWIG_ROOT={0}".format(spec['herwig6'].prefix), 'FFLAGS=-std=legacy', 'lib_archive')

    def install(self, spec, prefix):
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
        for libname in find(prefix.lib.archive, '*.a'):
            install(libname, prefix.lib)
        shutil.rmtree(prefix.lib.archive)

    def do_stage(self, mirror_only=False):
        super(Jimmy, self).do_stage(mirror_only)
        dn = os.listdir(self.stage.source_path)[0]
        for fn in os.listdir(join_path(self.stage.source_path, dn)):
            shutil.move(join_path(self.stage.source_path, dn, fn), join_path(self.stage.source_path, fn))
        shutil.rmtree(join_path(self.stage.source_path, dn))
