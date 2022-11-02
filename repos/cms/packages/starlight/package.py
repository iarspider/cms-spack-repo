# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Starlight(CMakePackage):
    """STARlight is a Monte Carlo that simulates two-photon
        and photon-Pomeron interactions between relativistic nuclei and protons."""

    homepage = "https://www.example.com"
    git      = "https://github.com/cms-externals/starlight.git"

    version("r193", commit="689c0da91bacd5591d85d71db0fc7cc6fec0b919")

    depends_on("clhep")
    drop_files = ["lib/archive"]
    patch("starlight-r193-allow-setting-CMAKE_CXX_FLAGS.patch")

    def setup_build_environment(self, env):
        env.set("CLHEP_PARAM_PATH", self.spec["clhep"].prefix)

    def cmake_args(self):
        define = self.define
        cxxflags = ["-Wno-error=deprecated-declarations"]
        if self.spec.satisfies("%gcc@9:"):
            cxxflags.append("-Wno-error=deprecated-copy")

        args = [define("ENABLE_CLHEP", "ON"),
                define("CPP11", "ON"),
                define("CMAKE_CXX_FLAGS", " ".join(cxxflags))]
        return args
