# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Alpgen(CMakePackage):
    """A collection of codes for the generation of
       multi-parton processes in hadronic collisions."""

    homepage = "http://mlm.home.cern.ch/mlm/alpgen/"
    url      = "https://mlm.home.cern.ch/mlm/alpgen/V2.1/v214.tgz"
    
    patch('alpgen-214.patch', when='recipe=cms')
    patch('alpgen-214-Darwin-x86_84-gfortran.patch', when='platform=darwin recipe=cms')
    patch('alpgen-2.1.4-sft.patch', when='recipe=sft', level=0)
    
    variant('recipe', values=('cms', 'sft'), default='sft',
            description='Select build recipe: CMS for CMS experiment, '+
                        'SFT for ATLAS/LHCb/others.')

    version('2.1.4', sha256='2f43f7f526793fe5f81a3a3e1adeffe21b653a7f5851efc599ed69ea13985c5e')
    
    def url_for_version(self, version):
        root = url.rsplit('/', 2)[0]
        return "{0}/V{1}/{2}.tgz".format(root, version.upto(2), version.joined)

    def patch(self):
        if self.spec.satisfies('recipe=sft'):
            copy(join_path(os.path.dirname(__file__), 'CMakeLists.txt'), 'CMakeLists.txt')
            
        if self.spec.satisfies('recipe=cms'):
            filter_file('-fno-automatic', '-fno-automatic -std=legacy', 'compile.mk')

    @when('recipe=cms')
    def cmake(self, spec, prefix):
        return
        
    @when('recipe=cms')
    def build(self, spec, prefix):
        build_sh = Executable('cms_build.sh')
        build_sh()

    @when('recipe=cms')
    def install(self, spec, prefix):
        install_sh = Executable('cms_install.sh')
        install_sh(prefix)
        for root, dirs, files in os.walk(prefix):
            set_install_permissions(root)
            for file in files:
                set_install_permissions(file)
