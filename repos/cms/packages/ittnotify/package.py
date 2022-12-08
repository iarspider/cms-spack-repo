# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ittnotify(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "https://github.com/01org/IntelSEAPI/archive/16.06.18.tar.gz"

    version(
        "16.06.18",
        sha256="5e339c1c3d95c3d5ae20e16ac9bf79140c863044a8aa1566bc3be90a8c736d8c",
    )

    keep_archives = True

    def cmake_args(self):
        args = [self.define("ARCH_64", 1)]
        return args

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        mkdirp(prefix.lib)
        install(join_path(self.stage.path, "bin", "libittnotify64.a"), prefix.lib)
        install("ittnotify/include/ittnotify.h", prefix.include)
