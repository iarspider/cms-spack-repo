# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob
import os


class Hepmc(CMakePackage):
    """The HepMC package is an object oriented, C++ event record for
       High Energy Physics Monte Carlo generators and simulation."""

    homepage = "https://hepmc.web.cern.ch/hepmc/"
    url      = "https://hepmc.web.cern.ch/hepmc/releases/hepmc2.06.11.tgz"
    git      = "https://github.com/cms-externals/hepmc.git"

    tags = ['hep']
    keep_archive = True

    version('2.06.10.cms', commit='91c4c217572ac25669e9ad8fdc0111d1d5c82289')

    variant('length', default='MM', values=('CM', 'MM'), multi=False,
            description='Unit of length')
    variant('momentum', default='GEV', values=('GEV', 'MEV'), multi=False,
            description='Unit of momentum')

    depends_on('cmake@2.8.9:', type='build')

    drop_files = ['share']

    def cmake_args(self):
        return [
            self.define_from_variant('momentum'),
            self.define_from_variant('length'),
            '-DCMAKE_CXX_FLAGS=-fPIC'
        ]


    @run_after('install')
    def post_install(self):
        prefix = self.prefix
        for fn in glob.glob(join_path(prefix.lib, '*.so')):
            os.remove(fn)
