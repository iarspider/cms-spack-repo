# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect

from spack import *


class Fjcontrib(AutotoolsPackage):
    """3rd party extensions of FastJet"""

    homepage = "https://fastjet.hepforge.org/contrib/"
    git      = "https://github.com/cms-externals/fastjet-contrib.git"

    tags = ['hep']

    version('1.044.cms', branch='cms/v1.044')

    depends_on('fastjet')

    build_targets = ['all', 'fragile-shared']
    install_targets = ['install', 'fragile-shared-install']

    def configure_args(self):
        args = ['--fastjet-config=' +
                self.spec['fastjet'].prefix.bin +
                '/fastjet-config',
                "CXXFLAGS=-O3 -Wall -g " +
                self.compiler.cxx_pic_flag]
        return args

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            for target in self.build_targets:
                inspect.getmodule(self).make(target)

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            for target in self.install_targets:
                inspect.getmodule(self).make(target)
