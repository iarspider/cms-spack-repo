# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataRecoecalEgammaclusterproducers(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-RecoEcal-EgammaClusterProducers'
    git = "https://github.com/cms-data/{0}.git".format(n.replace('data-', ''))

    version('V00-02-00', tag='V00-02-00')
    version('V00-01-00', tag='V00-01-00')
