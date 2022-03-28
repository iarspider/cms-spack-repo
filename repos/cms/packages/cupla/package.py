# Copyright 20131-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil

from spack import *


class Cupla(Package, CudaPackage):
    """C++ User interface for the Platform independent Library Alpaka"""

    homepage = "https://github.com/alpaka-group/cupla"
    git      = "https://github.com/alpaka-group/cupla.git"
    url      = "https://github.com/alpaka-group/cupla/archive/refs/tags/0.3.0.tar.gz"

    maintainers = ['vvolkl']

    version('develop', branch='dev')
    version('master', branch='master')
    version('0.3.0', sha256='035512517167967697e73544c788453de5e3f0bc4e8d4864b41b2e287365cbaf')

    depends_on('alpaka@0.6.0:')
    depends_on('intel-tbb')

    def install(self, spec, prefix):
        # remove the version of Alpaka bundled with Cupla
        shutil.rmtree('alpaka')

        mkdirp('build')
        mkdirp('lib')

        files = find(self.stage.source_path, '*.cpp', recursive=True)
#        if self.spec.satisfies('~cuda'):
#            files = [fn for fn in files if 'CUDASamples' not in fn]

        CXXFLAGS=["-DALPAKA_DEBUG=0"]
        for dep in ('cuda', 'intel-tbb', 'boost', 'alpaka'):
            if dep in self.spec:
                CXXFLAGS.append("-I{0}".format(self.spec[dep].prefix.include))
            CXXFLAGS.append("-I{0}".format(join_path(self.stage.source_path, 'example/CUDASamples/common')))

        CXXFLAGS.append("-Iinclude")

        HOST_FLAGS = ["-std=c++17", "-O2", "-pthread", "-fPIC", "-Wall", "-Wextra"]
        NVCC_FLAGS = self.cuda_flags

        gpp = Executable(self.compiler.cxx)
        nvcc = self.spec['cuda'].prefix.bin.nvcc if spec.satisfies('+cuda') else ''

        # build the serial CPU backend
        mkdirp('build/serial')
        for File in files:
            fn = os.path.basename(File)
            gpp('-DALPAKA_ACC_CPU_B_SEQ_T_SEQ_ENABLED', '-DCUPLA_STREAM_ASYNC_ENABLED=0', *CXXFLAGS, *HOST_FLAGS, '-c', File, '-o', 'build/serial/' + fn + '.o')
        gpp(*CXXFLAGS, *HOST_FLAGS, 'build/serial/*.o', '-shared',  '-o', 'lib/libcupla-serial.so')

        # build the TBB CPU backend
        mkdirp('build/tbb')
        for File in files:
            fn = os.path.basename(File)
            gpp('-DALPAKA_ACC_CPU_B_TBB_T_SEQ_ENABLED', '-DCUPLA_STREAM_ASYNC_ENABLED=1', *CXXFLAGS, *HOST_FLAGS, '-c', File, '-o', 'build/tbb/' + fn + '.o')
        gpp(*CXXFLAGS, *HOST_FLAGS, 'build/tbb/*.o', '-L' + self.spec['intel-tbb'].prefix.lib, '-ltbb', '-shared',  '-o', 'lib/libcupla-tbb.so')

        if spec.satisfies('+cuda'):
            mkdirp('build/cuda')
            for File in files:
                fn = os.path.basename(File)
                nvcc('-DALPAKA_ACC_GPU_CUDA_ENABLED', '-DCUPLA_STREAM_ASYNC_ENABLED=1', *CXXFLAGS, *NVCC_FLAGS, '-Xcompiler', ' '.join(HOST_FLAGS), '-x', 'cu', '-c', File, '-o', 'build/cuda/' + fn + '.o')
            gpp(*CXXFLAGS, *HOST_FLAGS, 'build/cuda/*.o', '-L' + self.spec['cuda'].prefix.lib64, '-lcudart', '-shared', '-o', 'lib/libcupla-cuda.so')

        mkdirp(prefix.include)
        mkdirp(prefix.lib)
        install_tree('include', prefix.include)
        install_tree('lib', prefix.lib)

    def setup_run_environment(self, env):
        env.set("CUPLA_ROOT", self.prefix)
        env.prepend_path("CMAKE_PREFIX_PATH", self.prefix)
        env.set("CUPLA", self.prefix.share.cupla)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("CUPLA_ROOT", self.prefix)
        env.prepend_path("CMAKE_PREFIX_PATH", self.prefix)
        env.set("CUPLA", self.prefix.share.cupla)
