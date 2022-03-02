# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install cms-md5
#
# You can edit this file again by typing:
#
#     spack edit cms-md5
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class CmsMd5(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    git      = "https://github.com/cms-externals/md5.git"

    version("1.0.0", branch="cms/1.0.0", commit="d97a571864a119cd5408d2670d095b4410e926cc")

    def install(self, spec, prefix):
        gcc = Executable(spack_cc)
        suffix = 'dylib' if spec.satisfies('platform=darwin') else 'so'
        gcc('md5.c', '-shared', '-fPIC', '-o', 'libcms-md5.' + suffix)

        mkdirp(prefix.include)
        mkdirp(prefix.lib)
        install('libcms-md5.*', prefix.lib)
        install('md5.h', prefix.include)
