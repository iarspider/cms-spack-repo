# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob
import os

from spack import *


class G4hepem(CMakePackage):
    """The G4HepEm R&D project was initiated by the Electromagnetic Physics
       Working Group of the Geant4 collaboration as part of looking for
       solutions to reduce the computing performance bottleneck experienced
       by the High Energy Physics (HEP) detector simulation applications."""

    homepage = "https://github.com/mnovak42/g4hepem"
    git      = "https://github.com/mnovak42/g4hepem.git"

    version("20221014", tag="20221014")

    depends_on("geant4")

    def cmake_args(self):
        args = [self.define("Geant4_DIR", self.spec["geant4"].prefix)]
        return args

    @run_after("install")
    def make_static(self):
        ar = which("gcc-ar", required=True)
        mkdirp(self.prefix.lib64.archive)
        with working_dir(self.prefix.lib64.archive):
            for fn in find(self.prefix.lib64, "*.a"):
                ar("x", fn)
            ar("rcs", "libg4hepem-static.a", *glob.glob("*.o"))
            for fn in glob.glob("*.o"):
                os.remove(fn)
