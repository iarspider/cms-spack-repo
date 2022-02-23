# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class DasClient(Package):
    """Data Aggregation System (DAS)"""

    homepage = "https://github.com/dmwm/DAS"
    git = "https://github.com/dmwm/DAS.git"

    version("v03.01.00", tag="v03.01.00")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('src/python/DAS/tools/das_client.py', prefix.bin)
        install(join_path(os.path.dirname(__file__), 'das_clinet'), join_path(prefix.etc, 'das_client'))
        filter_file('%v', str(spec.version), join_path(prefix.etc, 'das_client'))
