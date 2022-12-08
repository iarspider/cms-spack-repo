# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataHltriggerJetmet(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""

    n = "data-HLTrigger-JetMET"
    url = "https://github.com/cms-data/HLTrigger-JetMET/archive/V01-00-00.tar.gz"
    version(
        "V01-00-00",
        sha256="6f67298771ca1c402316ae0d767bd68099a798da1fc1b0aa9d22b59ed17124f8",
    )

    def url_for_version(self, version):
        url = self.url.rsplit("/", 1)[0]
        return url + "/" + str(version) + ".tar.gz"
