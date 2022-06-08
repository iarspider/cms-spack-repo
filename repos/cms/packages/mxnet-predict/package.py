# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import shutil
import os
import glob


class MxnetPredict(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    git      = "https://github.com/cms-externals/incubator-mxnet.git"

    version('1.6.0', commit='b4aada51b4af56a05adc4ed17f77001bfd6943d8', submodules=True)

    # extends('python')
    depends_on('ninja', type='build')
    depends_on('openblas')
    depends_on('python')
    depends_on('py-numpy')

    def cmake_args(self):
        define = self.define
        args = [define('USE_CUDA', 'OFF'),
                define('USE_OPENCV', 'OFF'),
                define('USE_OPENMP', 'OFF'),
                define('USE_BLAS', 'open'),
                define('USE_LAPACK', 'OFF'),
                define('USE_MKL_IF_AVAILABLE', 'OFF'),
                define('USE_MKLDNN', 'OFF'),
                define('USE_F16C', 'OFF'),
                define('USE_CPP_PACKAGE', 'ON'),
                define('BUILD_CPP_EXAMPLES', 'OFF'),
                define('CMAKE_INSTALL_LIBDIR', 'lib'),
                define('CMAKE_LIBRARY_OUTPUT_DIRECTORY', self.spec.prefix),
                define('PYTHON_EXECUTABLE', str(python)),
                define('INSTALL_PYTHON_VERSIONS', str(self.spec['python'].version.up_to(2).joined)),
               ]
        return args

    @run_after("install")
    def cmspost(self):
        for fn in glob.glob(self.prefix.join('*.so')):
            os.remove(fn)
        for fn in glob.glob(self.prefix.join('python*')):
            shutil.move(fn, prefix.lib)

