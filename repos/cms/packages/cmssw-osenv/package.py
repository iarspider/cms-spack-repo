# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

from spack import *


class CmsswOsenv(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.example.com"
    git      = "https://github.com/cms-sw/cmssw-osenv.git"

    version('221009.0', commit='a85902226d6107c61802d01ee1afac13a11a7eb4')
    version('220601.0', commit='ebed1aee4c08c158b4f3f33928eb52f32090710e')
    version('211125.0', commit='3a1d33d8dc9989257ec91e3543eda8250e5a3593')

    def install(self, spec, prefix):
        mkdirp(prefix.common)
        install_tree('.', prefix.common, ignore=lambda x: '.git' in x)
        install(join_path(os.path.dirname(__file__), 'cmspost.sh'), prefix)
        filter_file('^pkgname=.*', 'pkgname="'+os.path.basename(os.path.dirname(__file__))+'"', prefix.join('cmspost.sh'), backup=False, stop_at='## END CONFIG')
        filter_file('^fakerevision=.*', 'fakerevision="'+str(spec.version).split('.')[1]+'"', prefix.join('cmspost.sh'), backup=False, stop_at='## END CONFIG')
