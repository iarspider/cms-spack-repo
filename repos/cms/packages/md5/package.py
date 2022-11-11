# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Md5(Package):
    """Independent implementation of MD5 (RFC 1321)."""

    homepage = "http://www.ietf.org/rfc/rfc1321.txt"
    git = "https://github.com/cms-externals/md5.git"

    version(
        "1.0.0", branch="cms/1.0.0", commit="d97a571864a119cd5408d2670d095b4410e926cc"
    )

    def install(self, spec, prefix):
        gcc = Executable(spack_cc)
        suffix = "dylib" if spec.satisfies("platform=darwin") else "so"
        gcc("md5.c", "-shared", "-fPIC", "-o", "libcms-md5." + suffix)

        mkdirp(prefix.include)
        mkdirp(prefix.lib)
        install("libcms-md5.*", prefix.lib)
        install("md5.h", prefix.include)
