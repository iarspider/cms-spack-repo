# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Geant4Parfullcms(CMakePackage):
    """CPU benchmark test of Geant4 based on the full CMS detector"""

    homepage = "https://github.com/cms-sw/cmssw"
    url = "https://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc10/external/geant4-parfullcms/2014.01.27/ParFullCMS.2014.01.27.tar.bz2"

    version(
        "2014.01.27",
        sha256="96680b6db41951515dc4cce921b5857467543631775f2eeacff3880d0481129f",
    )

    depends_on("geant4")
    depends_on("geant4data")

    def cmake_args(self):
        args = [
            self.define("BUILD_SHARED_LIBS", False),
            self.define("BUILD_STATIC_LIBS", True),
            self.define("Geant4_USE_FILE", self.spec["geant4"].prefix),
            self.define("CMAKE_INSTALL_LIBDIR", "lib"),
        ]

        return args
