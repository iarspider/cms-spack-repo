# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os

class CmsGitTools(Package):
    """CMS Git tools"""

    homepage = "https://www.example.com"
    git      = "https://github.com/cms-sw/cms-git-tools.git"

    version('211007.0', commit='797b095ca09a955b2caa35645d00c1b9e6a93246')

    def install(self, spec, prefix):
        mkdirp(prefix.common)
        mkdirp(prefix.share.man.man1)
        install_tree('.', prefix.common)
        install(join_path(self.stage.source_path, 'docs', 'man', 'man1', '*.1'), prefix.share.man.man1)
        install(join_path(os.path.dirname(__file__), 'cmspost.sh'), prefix)
        filter_file('%{fakerevision}', str(spec.version.upto(1)), join_path(prefix, 'cmspost.sh'))
