# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import glob
import os
import re

class CrabDev(CrabPackage):
    """crab-dev"""

    homepage = "https://www.example.com"
    url = "file://" + os.path.dirname(__file__) + '/junk.xml'

    wmcore_version = '1.5.3'
    crab_client_version = 'v3.220204'
    crab_client_revision = '00'
    crab_server_version = 'v3.220107'
    dbs_version = '3.14.0'

    @run_after('install')
    def copy_cmspost(self):
        install(join_path(os.path.dirname(__file__), 'cmspost.sh'), prefix)
        filter_file('%{ver}', str(spec.version), join_path(prefix, 'cmspost.sh'))
        set_executable(join_path(prefix, 'cmspost.sh'))

