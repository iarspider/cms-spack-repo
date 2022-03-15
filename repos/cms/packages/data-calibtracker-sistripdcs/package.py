# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataCalibtrackerSistripdcs(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-CalibTracker-SiStripDCS'
    url = 'https://github.com/cms-data/CalibTracker-SiStripDCS/archive/V01-00-00.tar.gz'
    version('V01-00-00', sha256='b416fac88a28f6f08ae0da3f748d531a0cb83705c38a9eff6b8df7e4a6f84063')
