# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Icx(BundlePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"

    version("2022")

    def install(self, spec, prefix):
        force_symlink(
            f"/cvmfs/projects.cern.ch/intelsw/oneAPI/linux/x86_64/{spec.version}/compiler/latest/linux/",
            prefix.installation,
        )
