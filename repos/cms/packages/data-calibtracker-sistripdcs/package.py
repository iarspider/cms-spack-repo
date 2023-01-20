# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataCalibtrackerSistripdcs(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""

    n = "data-CalibTracker-SiStripDCS"
    url = "https://github.com/cms-data/CalibTracker-SiStripDCS/archive/V01-00-00.tar.gz"
    version("V01-01-00", sha256="574c6aca516e1ace3cf6230685e567198c93b11b6e9b1aaa74087a37e9c0b4aa")
    version(
        "V01-00-00",
        sha256="b416fac88a28f6f08ae0da3f748d531a0cb83705c38a9eff6b8df7e4a6f84063",
    )

    def url_for_version(self, version):
        url = self.url.rsplit("/", 1)[0]
        return url + "/" + str(version) + ".tar.gz"
