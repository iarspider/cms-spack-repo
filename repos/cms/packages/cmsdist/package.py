# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


def local_file(fn):
    return join_path(os.path.dirname(__file__), fn)


def local_file_url(fn):
    return "file://" + local_file(fn)


class Cmsdist(Package):
    """Toolfile scripts from CMSDIST repo"""

    homepage = "https://www.example.com"
    git = "https://github.com/cms-sw/cmsdist.git"

    version("IB-CMSSW_12_6_X-g11", branch="IB/CMSSW_12_6_X/g11")

    def patch(self):
        def add_toolfile(name, dirname=None):
            if dirname is None:
                dirname = name

            mkdirp(join_path(prefix, "scram-tools.file", "tools", dirname))
            install(
                local_file(name + ".xml"),
                join_path(prefix, "scram-tools.file", "tools", dirname),
            )

        prefix = self.stage.source_path
        filter_file(
            "export GCC_ROOT=.*",
            "export GCC_ROOT=" + os.path.dirname(os.path.dirname(self.compiler.cc)),
            join_path(prefix, "scram-tools.file", "tools", "llvm", "env.sh"),
            string=True,
        )

#        filter_file(
#            '<environment name="CXX" value="$GCC_CXXCOMPILER_BASE/bin/c++@COMPILER_NAME_SUFFIX@"/>',
#            '<environment name="CXX" value="' + spack_cxx + '"/>',
#            join_path(prefix, "scram-tools.file", "tools", "gcc", "gcc-cxxcompiler.xml"),
#            string=True,
#        )
#
#        filter_file(
#            '<environment name="CC" value="$GCC_CCOMPILER_BASE/bin/gcc@COMPILER_NAME_SUFFIX@"/>',
#            '<environment name="CC" value="' + spack_cc + '"/>',
#            join_path(prefix, "scram-tools.file", "tools", "gcc", "gcc-ccompiler.xml"),
#            string=True,
#        )
#
#        filter_file(
#            '<environment name="FC" default="$GCC_F77COMPILER_BASE/bin/gfortran"/>',
#            '<environment name="FC" default="' + spack_fc + '"/>',
#            join_path(prefix, "scram-tools.file", "tools", "gcc", "gcc-f77compiler.xml"),
#            string=True,
#        )

        if self.spec.satisfies("@12.4.0.pre3"):
            add_toolfile("abseil-cpp")
            add_toolfile("c-ares")

        add_toolfile("re2")
        filter_file(
            "</tool>",
            '  <use name="abseil-cpp"/>\n  <use name="c-ares"/>\n  <use name="re2"/>\n</tool>',
            join_path(prefix, "scram-tools.file", "tools", "grpc", "grpc.xml"),
            string=True,
        )

        add_toolfile("veccore")
        filter_file(
            "</tool>",
            '  <use name="veccore"/>\n</tool>',
            join_path(prefix, "scram-tools.file", "tools", "vecgeom", "vecgeom.xml"),
        )

        filter_file(
            "if grep VECGEOM_ROOT ${TOOL_ROOT}/etc/profile.d/dependencies-setup.sh >/dev/null 2>&1  ; then",
            'if [ "x$GEANT4_HAS_VECGEOM" != "x" ]; then',
            join_path(prefix, "scram-tools.file", "tools", "geant4", "env.sh"),
            string=True,
        )

    def install(self, spec, prefix):
        mkdir(prefix.join("scram-tools.file"))
        install_tree("scram-tools.file", prefix.join("scram-tools.file"))
