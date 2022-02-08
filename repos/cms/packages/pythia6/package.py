# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import numbers
import os

from six import iteritems
from six.moves.urllib.parse import urlparse

from spack import *


def _is_integral(x):
    """Accepts only integral values."""
    try:
        return isinstance(int(x), numbers.Integral) and \
            (not isinstance(x, bool))
    except ValueError:
        return False


class Pythia6(AutotoolsPackage):
    """PYTHIA is a program for the generation of high-energy physics events,
    i.e. for the description of collisions at high energies between elementary
    particles such as e+, e-, p and pbar in various combinations.

    PYTHIA6 is a Fortran package which is no longer maintained: new
    prospective users should use Pythia8 instead.

    This recipe includes patches required to interoperate with Root.
    """

    homepage = 'https://pythiasix.hepforge.org/'
    url = 'https://pythia.org/download/pythia6/pythia6428-split.tgz'

    tags = ['hep']

    maintainers = ['gartung', 'chissg']

    version('6.4.26', url='https://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/pythia6/pythia6-426-src.tgz',
            sha256='4dd75f551b7660c35f817c063abd74ca91b70259c0987905a06ebb2d21bcdf26')

    # install_libtool_archives = True
    keep_archive = True
    configure_directory = '426'

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    # The maximum number of particles (NMXHEP) supported by the arrays
    # in the /HEPEVT/ COMMON block may need tweaking if pythia6 is
    # intended to be used with other code with different requirements.
    variant('nmxhep', default=4000, values=_is_integral, description='Extent of particle arrays in the /HEPEVT/ COMMON block.')

    def setup_build_environment(self, env):
        if self.spec.satisfies('%gcc@10:'):
            env.append_flags('CFLAGS', '-fcommon')
            env.append_flags('FFLAGS', '-fcommon')

    def configure_args(self):
        mkdirp(self.stage.path, 'temp_prefix')
        args = ['--with-hepevt=4000', '--prefix=' + join_path(self.stage.path, 'temp_prefix'), '--disable-shared', '--enable-static']
        if self.spec.satisfies('platform=darwin'):
            args.append('LDFLAGS=-Wl,-commons,use_dylibs -Wl,-flat_namespace')

        return args

    @run_after('configure')
    def patch_libtool(self):
        filter_file('^CC=.*$', 'CC="gcc -fPIC"', join_path(self.configure_directory, 'libtool'))

    def build(self, spec, prefix):
        with working_dir(self.configure_directory):
            make('all', 'CFLAGS=-fPIC -fcommon')
            make('install')

    def install(self, spec, prefix):
        install_tree(join_path(self.stage.path, 'temp_prefix', 'lib'), prefix.lib)
        install_tree(join_path(self.stage.path, 'temp_prefix', 'include'), prefix.include)
