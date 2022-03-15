# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataRecoparticleflowPftracking(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-RecoParticleFlow-PFTracking'
    url = 'https://github.com/cms-data/RecoParticleFlow-PFTracking/archive/V13-01-00.tar.gz'
    version('V13-01-00', sha256='03d37944268bdfe971ea8489eed3fdb23f00e5464294fa24f56c7b0310bddf2e')
