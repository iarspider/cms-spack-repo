# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataRecoegammaEgammaphotonproducers(CMSDataPackage):
    """ foo """

    n = 'data-RecoEgamma-EgammaPhotonProducers'
    git = "https://github.com/cms-data/{0}.git".format(n.replace('data-', ''))

    version('V00-01-00', tag='V00-01-00')
