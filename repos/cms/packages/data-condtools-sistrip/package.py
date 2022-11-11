# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataCondtoolsSistrip(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""

    n = "data-CondTools-SiStrip"
    git = "https://github.com/cms-data/CondTools-SiStrip.git"
    version("V00-02-00", tag="V00-02-00")
