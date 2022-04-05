# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack import *


class CudaCompatibleRuntime(Package):
    """Test for cuda-compatible runtime"""

    homepage = "https://github.com/cms-patatrack/cuda-compatible-runtime"
    url      = "https://raw.githubusercontent.com/cms-patatrack/cuda-compatible-runtime/master/test.cu"

    version('1.0', sha256='4addf7b86a973c7663906f38c332dc76df54209c1df784d1ef04a08303c79ddc',
            expand=False)

    depends_on('cuda')

    variant('cuda_arch',
            description='CUDA architecture',
            values=spack.variant.any_combination_of(*CudaPackage.cuda_arch_values))

    def install(self, spec, prefix):
        mkdirp('build')
        mkdirp(prefix.test)
        nvcc = which('nvcc', required=True)
        cuda_flags_4 = CudaPacakge.cuda_flags_4(self.spec.variant['cuda_arch'].value)
        try:
            nvcc(CudaPackage.nvcc_stdcxx, '-O2', '-g', *cuda_flags_4, 'test.cu', '-I', spec['cuda'].prefix.include,
                 '-L', spec['cuda'].prefix.lib64, '-L', spec['cuda'].prefix.lib64.stubs, '--cudart', 'static',
                 '-ldl', '-lrt', '--compiler-options', '-Wall -pthread', '-o', join_path('build', 'cuda-compatible-runtime'))
        except ProcessError:
            install(join_path(os.path.dirname(__file__), 'cuda-compatible-runtime'), prefix.test.join('cuda-compatible-runtime'))
        else:
            install(join_path('build', 'cuda-compatible-runtime'), prefix.test.join('cuda-compatible-runtime'))
