# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack import *


class CudaCompatibleRuntime(Package):
    """Test for cuda-compatible runtime"""

    homepage = "https://github.com/cms-patatrack/cuda-compatible-runtime"
    git = "https://github.com/cms-patatrack/cuda-compatible-runtime.git"

    version("1.0", commit="dcedd95392c092795b443a10c82c26a995e6dfc0")

    depends_on("cuda")

    variant(
        "cuda_arch",
        description="CUDA architecture",
        values=spack.variant.any_combination_of(*CudaPackage.cuda_arch_values),
    )

    def install(self, spec, prefix):
        mkdirp("build")
        mkdirp(prefix.test)
        nvcc = which("nvcc", required=True)
        cuda_flags_4 = CudaPackage.cuda_flags_4(self.spec.variants["cuda_arch"].value)
        try:
            args = [
                CudaPackage.nvcc_stdcxx,
                "-O2",
                "-g",
                *cuda_flags_4,
                "test.cu",
                "-I",
                str(spec["cuda"].prefix.include),
                "-L",
                str(spec["cuda"].prefix.lib64),
                "-L",
                str(spec["cuda"].prefix.lib64.stubs),
                "--cudart",
                "static",
                "-ldl",
                "-lrt",
                "--compiler-options",
                "-Wall",
                "-pthread",
                "-o",
                join_path("build", "cuda-compatible-runtime"),
            ]
            nvcc(*args)
        except ProcessError:
            install(
                join_path(os.path.dirname(__file__), "cuda-compatible-runtime"),
                prefix.test.join("cuda-compatible-runtime"),
            )
        else:
            install(
                join_path("build", "cuda-compatible-runtime"),
                prefix.test.join("cuda-compatible-runtime"),
            )
        set_executable(prefix.test.join("cuda-compatible-runtime"))
