# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataSimg4cmsForward(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""

    n = "data-SimG4CMS-Forward"
    url = "http://cmsrep.cern.ch/cmssw/download/data/SimG4CMS-Forward.tar.gz"
    version(
        "V02-04-00",
        sha256="d37c14b80eff463da59250b72524eaf87e47d0534150e6861346b7fd7302b239",
    )

    def url_for_version(self, version):
        return self.url
