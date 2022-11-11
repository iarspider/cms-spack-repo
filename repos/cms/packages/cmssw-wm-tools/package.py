# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class CmsswWmTools(Package):
    """Release independent tools to glue together cmssw,
    wmagent, and wmcontrol for workflow submission use cases"""

    homepage = "https://github.com/cms-sw/cmssw-wm-tools"
    git = "https://github.com/cms-sw/cmssw-wm-tools.git"

    version("211210", commit="aa1626fb2d2fdbde6b3259e4b44828220883a809")

    def install(self, spec, prefix):
        install_tree(".", prefix)
        install(join_path(os.path.dirname(__file__), "cmspost.sh"), prefix)
        filter_file(
            "%{realversion}",
            str(self.spec.version),
            join_path(prefix, "cmspost.sh"),
            backup=False,
            string=True,
        )
        filter_file(
            "%{prefix}",
            prefix,
            join_path(prefix, "cmspost.sh"),
            backup=False,
            string=True,
        )
