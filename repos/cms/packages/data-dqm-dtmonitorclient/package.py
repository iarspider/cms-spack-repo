# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataDqmDtmonitorclient(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-DQM-DTMonitorClient'
    url = 'https://github.com/cms-data/DQM-DTMonitorClient/archive/V00-01-00.tar.gz'
    version('V00-01-00', sha256='7f0c0c2078d084ae2abd5b3549410526259a114d9f95fa0afed474fb1aa31e46')
