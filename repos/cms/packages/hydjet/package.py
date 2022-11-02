# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hydjet(CMakePackage):
    """Hydjet Monte-Carlo generator"""

    homepage = "https://lokhtin.web.cern.ch/lokhtin/hydro/hydjet.html"
    url      = "http://cern.ch/lokhtin/hydro/hydjet-1.9.1.tar.gz"

    depends_on("pyquen")
    depends_on("pythia6")
    depends_on("lhapdf")

    version("1.9.3", sha256="6a7361854da58c6502e59f63c9afa934b6f3252556717bc080f202d5966cf767")
    version("1.9.1", sha256="902ffc19825b4d19edf3c8751456db9cee113d855096112b13d29f5129d203eb")
