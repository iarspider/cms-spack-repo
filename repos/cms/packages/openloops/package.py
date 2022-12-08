# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import fnmatch
import os
import shutil

from spack import *


class Openloops(Package):
    """The OpenLoops 2 program is a fully automated implementation of the
    Open Loops algorithm combined with on-the-fly reduction methods,
    which allows for the fast and stable numerical evaluation of tree
    and one-loop matrix elements for any Standard Model process
    at NLO QCD and NLO EW."""

    homepage = "https://openloops.hepforge.org/"
    git = "https://github.com/cms-externals/openloops.git"

    tags = ["hep"]

    version("2.1.2", branch="cms/v2.1.2")

    variant(
        "compile_extra",
        default=False,
        description="Compile real radiation tree amplitudes",
    )

    depends_on("python", type=("build", "run"))

    keep_archives = True

    # NOTICE: update this line when openloops updates
    depends_on("openloops-process@2.1.2", when="@2.1.2")

    phases = ["configure", "build", "install"]

    def configure(self, spec, prefix):
        spack_env = (
            "PATH LD_LIBRARY_PATH CPATH C_INCLUDE_PATH"
            + "CPLUS_INCLUDE_PATH INTEL_LICENSE_FILE"
        ).split()
        for k in env.keys():
            if k.startswith("SPACK_"):
                spack_env.append(k)

        spack_env = " ".join(spack_env)
        is_intel = self.spec.satisfies("%intel")

        with open("openloops.cfg", "w") as f:
            f.write("[OpenLoops]\n")
            f.write("import_env={0}\n".format(spack_env))
            f.write("num_jobs = 4\n")
            f.write("process_lib_dir = {0}\n".format(self.spec.prefix.proclib))
            f.write("cc = {0}\n".format(env["SPACK_CC"]))
            f.write("cxx = {0}\n".format(env["SPACK_CXX"]))
            f.write("fortran_compiler = {0}\n".format(env["SPACK_FC"]))
            f.write("gfortran_f_flags = -ffree-line-length-none " + "-fdollar-ok ")
            if self.spec.satisfies("%gcc@10:"):
                f.write("-fallow-invalid-boz ")
            if self.spec.target.family == "aarch64":
                f.write("-mcmodel=small\n")
            else:
                f.write("-mcmodel=medium\n")

            f.write("generic_optimisation = -O2\n")
            f.write("born_optimisation = -O2\n")
            f.write("loop_optimisation = -O0\n")
            f.write("link_optimisation = -O2\n")
            f.write("process_download_script = download_dummy.py\n")

        self.coll_file = (
            "tiny.coll"
            if spec["openloops-process"].variants["tiny"].value
            else "cms.coll"
        )
        copy(
            join_path(spec["openloops-process"].prefix, self.coll_file), self.coll_file
        )

        copy(
            join_path(os.path.dirname(__file__), "download_dummy.py"),
            "download_dummy.py",
        )

    def build(self, spec, prefix):
        ol = Executable("./openloops")
        ol("update", "--processes", "generator=0")

        if os.path.exists("process_src"):
            shutil.rmtree("process_src")

        install_tree(self.spec["openloops-process"].prefix.process_src, "process_src")
        install_tree(self.spec["openloops-process"].prefix.proclib, "proclib")
        install(
            join_path(self.spec["openloops-process"].prefix, self.coll_file),
            self.coll_file,
        )

        ol = Executable("./openloops")
        if "+compile_extra" in self.spec:
            ce = "compile_extra=1"
        else:
            ce = ""

        ol("libinstall", ce, self.coll_file)

    def install(self, spec, prefix):
        install_tree("lib", self.prefix.lib)
        mkdirp(self.prefix.proclib)
        for file in os.listdir("proclib"):
            if fnmatch.fnmatch(file, "*.info") or fnmatch.fnmatch(file, "*.so"):
                install(join_path("proclib", file), self.prefix.proclib)
