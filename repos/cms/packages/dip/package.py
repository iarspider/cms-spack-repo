# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
import os
import shutil

from spack import *

# platform_tag = 'f41e221f8fb95830fc001dad975b4db770f5d29d'
# NB: URL must point to cmsrep for now, unitl access to git is fixed


class Dip(CMakePackage):
    """Put a proper description of your package here."""

    homepage = "https://www.example.com"
    # git      = "ssh://git@gitlab.cern.ch:7999/industrial-controls/services/dip-hq/dip.git"
    keep_archives = True
    url = "https://cmsrep.cern.ch/cmssw/download/dip/8693f00cc422b4a15858fcd84249acaeb07b6316/dip-8693f00cc422b4a15858fcd84249acaeb07b6316.tgz"

    version(
        "c8693f00cc422b4a15858fcd84249acaeb07b6316",
        sha256="bac54edf593de5b4dfabd8f9f26cb67e4bf552329a258da22b08f230259a78f6",
    )

    resource(
        name="platform",
        url="https://cmsrep.cern.ch/cmssw/download/dip/8693f00cc422b4a15858fcd84249acaeb07b6316/platform-dependent-f41e221f8fb95830fc001dad975b4db770f5d29d.tgz",
        dest="platform-dependent",
        sha256="2e5baaf7689b0aa0bcf5b067c6e386aeaf7fbbbb454dd0cb7e73d56bdf970611",
    )

    keep_archives = True
    depends_on("log4cplus")

    cms_stage = 1

    # TODO: Fix me
    def url_for_version(self, version):
        return self.url

    @property
    def root_cmakelists_dir(self):
        return "platform-dependent" if self.cms_stage == 1 else self.stage.source_path

    @property
    def build_directory(self):
        return "build/platform-dependent" if self.cms_stage == 1 else "build/dip"

    def patch(self):
        sed = which("sed")
        sed("-i", "-e", "/conanbuildinfo.cmake\|conan_basic_setup/d", "CMakeLists.txt")
        sed(
            "-i",
            "-e",
            "/conanbuildinfo.cmake\|conan_basic_setup/d",
            "platform-dependent/CMakeLists.txt",
        )
        f = FileFilter("CMakeLists.txt")
        f.filter("CONAN_PKG::", "")
        f.filter("log4cplus", "log4cplusS")

    def flag_handler(self, name, flags):
        if name == "cxxflags":
            flags.append("-I" + self.spec.prefix.include)
            flags.append("-I" + self.spec["log4cplus"].prefix.include)
            flags.append("-L" + self.spec["log4cplus"].prefix.lib64)
            flags.append("-L" + self.spec.prefix.lib)
            return (None, None, flags)

        return (None, flags, None)

    @run_after("install")
    def stage_two(self):
        spec = self.spec
        prefix = self.spec.prefix
        self.cms_stage = 2

        options = self.std_cmake_args
        options += self.cmake_args()
        options.append(os.path.abspath(self.root_cmakelists_dir))
        with working_dir(self.build_directory, create=True):
            inspect.getmodule(self).cmake(*options)

        # build stage
        with working_dir(self.build_directory):
            if self.generator == "Unix Makefiles":
                inspect.getmodule(self).make(*self.build_targets)
            elif self.generator == "Ninja":
                self.build_targets.append("-v")
                inspect.getmodule(self).ninja(*self.build_targets)

        # install stage
        with working_dir(self.build_directory):
            if self.generator == "Unix Makefiles":
                inspect.getmodule(self).make(*self.install_targets)
            elif self.generator == "Ninja":
                inspect.getmodule(self).ninja(*self.install_targets)

        shutil.rmtree(join_path(prefix, "lib", "cmake"))
