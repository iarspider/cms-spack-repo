# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class TritonInferenceClient(CMakePackage, CudaPackage):
    """Triton Client Libraries and Examples"""

    homepage = "https://github.com/triton-inference-server/client"
    git = "https://github.com/triton-inference-server/client.git"

    version("2.11.0", commit="36cd3b3c839288c85b15e4df82cfe8fca3fff21b")

    depends_on("git", type="build")
    depends_on("protobuf")
    depends_on("grpc+shared")

    variant("cms", default=False, description="Apply CMS-specific changes")

    patch("cms.patch", when="+cms")

    resource(
        name="model_config.h",
        expand=False,
        sha256="6b6f5b90603195b0165430a883829e79e62cbd01961d4940e79f0ee26efd918f",
        placement={"model_config.h": "src/c++/library/model_config.h"},
        url="file://" + os.path.dirname(__file__) + "/model_config.h",
    )
    resource(
        name="model_config.cc",
        expand=False,
        sha256="44729ccd0928cc0697b94e799a479b7374c64430033ab0a9f56d35f64a35d086",
        placement={"model_config.cc": "src/c++/library/model_config.cc"},
        url="file://" + os.path.dirname(__file__) + "/model_config.cc",
    )
    resource(
        name="common",
        git="https://github.com/triton-inference-server/common.git",
        commit="249232758855cc764c78a12964c2a5c09c388d87",
        placement="repo-common",
    )

    root_cmakelists_dir = "src/c++"

    def patch(self):
        if not self.spec.satisfies("%gcc@10:"):
            return

        filter_file("Werror", "Wtype-limits", "src/c++/library/CMakeLists.txt")
        filter_file("Werror", "Wtype-limits", "repo-common/protobuf/CMakeLists.txt")

    def cmake_args(self):
        repo_common_dir = join_path(self.stage.source_path, "repo-common")

        define = self.define
        args = [
            define("CMAKE_INSTALL_LIBDIR", "lib"),
            define("TRITON_ENABLE_CC_HTTP", "OFF"),
            define("TRITON_ENABLE_CC_GRPC", "ON"),
            define("TRITON_ENABLE_PYTHON_HTTP", "OFF"),
            define("TRITON_ENABLE_PYTHON_GRPC", "OFF"),
            define("TRITON_ENABLE_PERF_ANALYZER", "OFF"),
            define("TRITON_ENABLE_EXAMPLES", "OFF"),
            define("TRITON_ENABLE_TESTS", "OFF"),
            self.define_from_variant("TRITON_ENABLE_GPU", variant="cuda"),
            define("TRITON_VERSION", "2.11.0"),
            define("FETCHCONTENT_SOURCE_DIR_REPO-COMMON", repo_common_dir),
            define("CMAKE_CXX_FLAGS", "-Wno-error -fPIC"),
        ]

        return args

    @run_after("install")
    def cms_post(self):
        prefix = self.spec.prefix
        sed = which("sed")
        sed(
            "-i",
            "/^#ifdef TRITON_ENABLE_GPU/i #define TRITON_ENABLE_GPU",
            join_path(prefix, "include", "ipc.h"),
        )
        os.unlink(join_path(prefix, "include", "triton", "common", "triton_json.h"))
