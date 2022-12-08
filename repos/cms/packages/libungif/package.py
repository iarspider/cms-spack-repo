# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libungif(AutotoolsPackage, SourceforgePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.example.com"
    sourceforge_mirror_path = "giflib/libungif-4.1.4.tar.gz"

    version(
        "4.1.4",
        sha256="5e65e1e5deacd0cde489900dbf54c6c2ee2ebc818199e720dbad685d87abda3d",
    )

    # -- CMS
    drop_files = ["bin/*"]
    strip_files = ["lib/*"]
