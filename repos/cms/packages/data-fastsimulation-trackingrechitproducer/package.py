# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataFastsimulationTrackingrechitproducer(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""

    n = "data-FastSimulation-TrackingRecHitProducer"
    url = "https://github.com/cms-data/FastSimulation-TrackingRecHitProducer/archive/V01-00-03.tar.gz"
    version(
        "V01-00-03",
        sha256="4c0d67f91cf5d95a75a673a68db577eb208ea3667be0b5a029e5ee87469821d7",
    )

    def url_for_version(self, version):
        url = self.url.rsplit("/", 1)[0]
        return url + "/" + str(version) + ".tar.gz"
