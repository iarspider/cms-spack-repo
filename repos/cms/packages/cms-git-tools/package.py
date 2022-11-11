# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class CmsGitTools(Package):
    """CMS Git tools"""

    homepage = "https://www.example.com"
    git = "https://github.com/cms-sw/cms-git-tools.git"

    version("221013.0", commit="a7606ad5c207a93b603137cdd1806590f20c7d1c")
    version("220325.0", commit="8f8dca853a35fe3345639bda767b28a12bec7842")
    version("211007.0", commit="797b095ca09a955b2caa35645d00c1b9e6a93246")

    def install(self, spec, prefix):
        mkdirp(prefix.common)
        mkdirp(prefix.share.man.man1)
        install_tree(".", prefix.common)
        install(
            join_path(self.stage.source_path, "docs", "man", "man1", "*.1"),
            prefix.share.man.man1,
        )
        install(join_path(os.path.dirname(__file__), "cmspost.sh"), prefix)
        filter_file(
            "%{fakerevision}",
            str(spec.version.up_to(1)),
            join_path(prefix, "cmspost.sh"),
        )
