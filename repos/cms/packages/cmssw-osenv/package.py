# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import shutil

class CmsswOsenv(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.example.com"
    git      = "https://github.com/cms-sw/cmssw-osenv.git"

    version('211125.0', commit='3a1d33d8dc9989257ec91e3543eda8250e5a3593')

    def install(self, spec, prefix):
        mkdirp(prefix.common)
        # shutil.rmtree('.git')
        install_tree('.', prefix.common)
        install(join_path(os.path.dirname(__file__), 'cmspost.sh'), prefix)
        filter_file('^pkgname=.*', 'pkgname="'+os.path.basename(os.path.dirname(__file__))+'"', prefix.join('cmspost.sh'), backup=False, stop_at='## END CONFIG')
        filter_file('^fakerevision=.*', 'fakerevision="'+str(spec.version).split('.')[1]+'"', prefix.join('cmspost.sh'), backup=False, stop_at='## END CONFIG')
