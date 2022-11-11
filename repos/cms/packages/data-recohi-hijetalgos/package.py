# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataRecohiHijetalgos(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""

    n = "data-RecoHI-HiJetAlgos"
    url = "https://github.com/cms-data/RecoHI-HiJetAlgos/archive/V01-00-01.tar.gz"
    version(
        "V01-00-01",
        sha256="8105409156f367a9dc9270d0a66ebb66d4a31860cf5724064173b1cd3301847d",
    )

    def url_for_version(self, version):
        url = self.url.rsplit("/", 1)[0]
        return url + "/" + str(version) + ".tar.gz"
