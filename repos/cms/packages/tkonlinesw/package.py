# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

from spack import *

# import glob


def local_file(fn):
    return join_path(os.path.dirname(__file__), fn)


def local_file_url(fn):
    return "file://" + local_file(fn)


class Tkonlinesw(Package):
    """TkOnlineSw"""

    homepage = "https://www.example.com"
    url = "http://cms-trackerdaq-service.web.cern.ch/cms-trackerdaq-service/download/sources/trackerDAQ-4.2.0-1_gcc7.tgz"

    version(
        "4.2.0-1_gcc7",
        "e18649cb90d5dc867f8aedc35cd25fbd3f605e8aca86ed55c91f474d727d9d7d",
    )

    depends_on("cmake", when="platform=darwin")
    depends_on("oracle-instant-client")
    depends_on("xerces-c")
    depends_on("root")
    depends_on("gmake")

    patch("tkonlinesw-4.0-clang-hash_map.patch")
    patch("tkonlinesw-bring-pvf.patch")
    patch("tkonlinesw-2.7.0-macosx.patch", when="platform=darwin")

    resource(
        name="tkonlinesw-cmake-build.file",
        url=local_file_url("tkonlinesw-cmake-build.file"),
        sha256="cbfdb9115280c7bfbfe3e48ad7d67f4843bba43fd1c26e335747522d106b469d",
        when="platform=darwin",
        expand=False,
        placement={"tkonlinesw-cmake-build.file": "CMakeLists.txt"},
    )

    phases = ("prep", "build", "install")
    releasename = "trackerDAQ-4.2-tkonline"

    def setup_build_environment(self, env):
        ###############################################################################
        # Tracker Specific Definitions for running, should just be this ...
        ################################################################################
        env.set("ENV_TRACKER_DAQ", join_path(self.stage.source_path, "opt/trackerDAQ"))

        ################################################################################
        # Tracker Specific Definitions for compilation
        ################################################################################
        env.set(
            "XDAQ_ROOT", join_path(self.stage.source_path, "FecSoftwareV3_0", "generic")
        )
        env.set("XDAQ_RPMBUILD", "yes")
        env.set("USBFEC", "no")
        env.set("PCIFEC", "yes")
        env.set("ENV_CMS_TK_BASE", join_path(self.stage.source_path))
        env.set("ENV_CMS_TK_DIAG_ROOT", join_path(self.stage.source_path, "DiagSystem"))
        env.set(
            "ENV_CMS_TK_ONLINE_ROOT",
            join_path(self.stage.source_path, "TrackerOnline/"),
        )
        env.set(
            "ENV_CMS_TK_COMMON",
            join_path(self.stage.source_path, "TrackerOnline/2005/TrackerCommon/"),
        )
        env.set(
            "ENV_CMS_TK_XDAQ",
            join_path(self.stage.source_path, "TrackerOnline/2005/TrackerXdaq/"),
        )
        env.set(
            "ENV_CMS_TK_APVE_ROOT",
            join_path(self.stage.source_path, "TrackerOnline/APVe"),
        )
        env.set(
            "ENV_CMS_TK_FEC_ROOT", join_path(self.stage.source_path, "FecSoftwareV3_0")
        )
        env.set(
            "ENV_CMS_TK_FED9U_ROOT",
            join_path(self.stage.source_path, "TrackerOnline/Fed9U/Fed9USoftware"),
        )
        env.set(
            "ENV_CMS_TK_ICUTILS",
            join_path(
                self.stage.source_path, "TrackerOnline/2005/TrackerCommon//ICUtils"
            ),
        )
        env.set("ENV_CMS_TK_LASTGBOARD", join_path(self.stage.source_path, "LAS"))

        ################################################################################
        # Fake variables for the configure script only
        ################################################################################
        # We use an empty directory because the path neeeds to exist.
        mkdirp(self.spec.prefix.dummy.Linux.lib)
        env.set("ENV_CMS_TK_HAL_ROOT", self.spec.prefix.dummy.Linux)
        env.set("ENV_CMS_TK_CAEN_ROOT", self.spec.prefix.dummy.Linux)
        env.set("ENV_CMS_TK_SBS_ROOT", self.spec.prefix.dummy.Linux)
        env.set("ENV_CMS_TK_TTC_ROOT", self.spec.prefix.dummy.Linux)

        ################################################################################
        # External Dependencies
        ################################################################################
        if self.spec.satisfies("platform=darwin"):
            env.set("XDAQ_OS", "macosx")
        else:
            env.set("XDAQ_OS", "linux")

        env.set("XDAQ_PLATFORM", "x86_slc4")
        env.set("ENV_CMS_TK_ORACLE_HOME", self.spec["oracle-instant-client"].prefix)
        env.set("ENV_ORACLE_HOME", self.spec["oracle-instant-client"].prefix)
        env.set("XERCESCROOT", self.spec["xerces-c"].prefix)

        ################################################################################
        env.set("CPPFLAGS", "-fPIC")
        env.set("CFLAGS", "-O2 -fPIC")
        env.set("CXXFLAGS", "-O2 -fPIC")

    def build(self, spec, prefix):
        ################################################################################
        # Configure
        ################################################################################
        bash = which("bash")
        if self.spec.satisfies("platform=darwin"):
            configure_arg = ""
        else:
            configure_arg = "--with-xdaq-platform=x86_64"
        bash("./configure")
        with working_dir(join_path(self.stage.source_path, "FecSoftwareV3_0")):
            bash("./configure", configure_arg)
        with working_dir(
            join_path(self.stage.source_path, "TrackerOnline/Fed9U/Fed9USoftware")
        ):
            bash("./configure", configure_arg)

        if self.spec.satisfies("platform=darwin"):
            # We still need the old makefile to generate a few headers.
            make(
                "-C",
                "TrackerOnline/Fed9U/Fed9USoftware/Fed9UUtils include/Fed9UUtils.hh",
            )
            make(
                "-C",
                "TrackerOnline/Fed9U/Fed9USoftware Fed9UUtils/include/Fed9UVersion.inc",
            )
            # We use CMake for all the rest since the build system on macosx
            # is simply broken by circular dependencies and other linux only bits.
            make(
                "-C",
                "TrackerOnline/Fed9U/Fed9USoftware/Fed9UUtils include/Fed9UUtils.hh",
            )
            cmake(
                "-DORACLE_ROOT=" + self.spec["oracle-instant-client"].prefix,
                "-DXERCESC_ROOT=" + self.spec["xerces-c"].prefix,
                "-DXERCESC=2",
                "-DCMAKE_INSTALL_PREFIX=" + prefix,
            )
            make("-j{0}".format(self.make_jobs))
            make("install")
        else:
            make("cmssw")
            make("cmsswinstall")

    def prep(self, spec, prefix):
        shutil.rmtree(
            "TrackerOnline/Fed9U/Fed9USoftware/Fed9UUtils/2.4/slc3_ia32_gcc323",
            ignore_errors=True,
        )
        filter_file("-Werror", "", "FecSoftwareV3_0/generic/Makefile")

    def install(self, spec, prefix):
        if self.spec.satisfies("platform=darwin"):
            # Again, installing is actually done by make install on macosx.
            return

        # Option --prefix in configure is not working yet, using tar:
        install_tree("opt/trackerDAQ/include", prefix.include)
        install_tree("opt/trackerDAQ/lib", prefix.lib)
