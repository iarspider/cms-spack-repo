# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import os
import shutil


class Cascade(AutotoolsPackage):
    """Cascade"""

    homepage = "https://www.example.com"
    url      = "http://cern.ch/service-spi/external/MCGenerators/distribution/cascade/cascade-2.2.04-src.tgz"

    version('2.2.04', sha256='9f1891cea7d79541f4dfc516207bfc0b197db822779203a1efbfd60e36d7a601')

    depends_on('lhapdf')
    depends_on('pythia6')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    patch('cascade-2.2.0-nomanual.patch', level=1)
    patch('cascade-2.2.04-getenv.patch', level=1)
    patch('cascade-2.2.04-drop-dcasrn.patch', level=0)

    keep_archives = True
    install_libtool_archives = True
    configure_directory = '2.2.04'

    def setup_build_environment(self, env):
        if self.spec.satisfies('%gcc@10:'):
            env.set('F77', "{0} -fPIC -fallow-argument-mismatch".format(self.compiler.fc))
        else:
            env.set('F77', "{0} -fPIC".format(self.compiler.fc))

    def configure_args(self):
        args = ['--with-pythia6=' + self.spec['pythia6'].prefix,
                '--with-lhapdf=' + self.spec['lhapdf'].prefix,
                '--enable-static', '--disable-shared']
        return args

    @run_after('install')
    def merge_archives(self):
        ar = which('ar', required=True)
        with working_dir(self.prefix.lib):
            for fn in glob.glob('*.a'):
                ar('-x', fn)
            ofiles = list(glob.glob('*.o'))
            ar('rcs', 'libcascade_merged.a', *ofiles)
            for fn in ofiles:
                os.remove(fn)