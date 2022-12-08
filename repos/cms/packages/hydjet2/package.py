# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack import *


class Hydjet2(CMakePackage):
    """Hydjet++"""

    homepage = "https://www.example.com"
    url = "http://cern.ch/lokhtin/hydjet++/hydjet2-2.4.3.tar.gz"

    version(
        "2.4.3",
        sha256="361641acb18b70d125b94c2551f79d53db32dc58740f0d089ec5778279d3e640",
    )

    depends_on("pythia6")
    depends_on("pyquen")
    depends_on("lhapdf")
    depends_on("root")

    @run_after("install")
    def move_data(self):
        mkdirp(self.spec.prefix.data.externals.hydjet2)
        os.rename(self.spec.prefix.share, self.spec.prefix.data.externals.hydjet2)
