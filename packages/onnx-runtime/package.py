# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OnnxRuntime(CMakePackage):
    """ONNX Runtime is a performance-focused complete scoring
    engine for Open Neural Network Exchange (ONNX) models, with
    an open extensible architecture to continually address the
    latest developments in AI and Deep Learning. ONNX Runtime
    stays up to date with the ONNX standard with complete
    implementation of all ONNX operators, and supports all
    ONNX releases (1.2+) with both future and backwards
    compatibility."""

    homepage = "https://github.com/microsoft/onnxruntime"
    git      = "https://github.com/cms-externals/onnxruntime.git"

    version('1.7.2.cms', branch='cms/v1.7.2')

    variant('cuda', default=False, description='Build with CUDA support')

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')
    depends_on('python', type='build')
    depends_on('protobuf')
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@16.6.6:')
    depends_on('py-wheel', type='build')
    depends_on('py-onnx')
    depends_on('zlib')
    depends_on('libpng')
    depends_on('py-pybind11')
    depends_on('cuda', when='+cuda')
    depends_on('cudnn', when='+cuda')
    
    extends('python')

    generator = 'Ninja'
    root_cmakelists_dir = 'cmake'

    def cmake_args(self):
        args = [define('onnxruntime_ENABLE_PYTHON', True),
                define('onnxruntime_BUILD_SHARED_LIB', True),
                define_from_variant('onnxruntime_USE_CUDA', 'cuda'),
                define('onnxruntime_BUILD_CSHARP', False),
                define('onnxruntime_USE_EIGEN_FOR_BLAS', True),
                define('onnxruntime_USE_OPENBLAS', False),
                define("onnxruntime_USE_MKLML", False),
                define("onnxruntime_USE_NGRAPH", False),
                define("onnxruntime_USE_OPENMP", False),
                define("onnxruntime_USE_TVM", False),
                define("onnxruntime_USE_LLVM", False),
                define("onnxruntime_ENABLE_MICROSOFT_INTERNAL", False),
                define("onnxruntime_USE_BRAINSLICE", False),
                define("onnxruntime_USE_NUPHAR", False),
                define("onnxruntime_USE_TENSORRT", False),
                define("onnxruntime_CROSS_COMPILING", False),
                define("onnxruntime_USE_FULL_PROTOBUF", True),
                define("onnxruntime_DISABLE_CONTRIB_OPS", False),
                define("onnxruntime_USE_PREINSTALLED_PROTOBUF", True),
                define("onnxruntime_PREFER_SYSTEM_LIB", True)]
                
        if self.spec.satisfies('+cuda'):
            args.extend((
                define('onnxruntime_CUDA_VERSION', str(self.spec['cuda'].version)),
                define('onnxruntime_CUDA_HOME', self.spec['cuda'].prefix),
                define('onnxruntime_CUDNN_HOME', self.spec['cudnn'].prefix),
                define('CMAKE_CUDA_FLAGS', '-cudart shared'),
                define('CMAKE_CUDA_RUNTIME_LIBRARY', 'Shared'),
                define('DCMAKE_TRY_COMPILE_PLATFORM_VARIABLES', 'CMAKE_CUDA_RUNTIME_LIBRARY')
            ))

    # copied from python build system
    def python(self, *args, **kwargs):
        py_exe = spec['python'].command.path
        py_exe(*args, **kwargs)

    def setup_py(self, *args, **kwargs):
        with working_dir(self.stage.source_path):
            self.python('-s', 'setup.py', '--no-user-cfg', *args, **kwargs)
 
    def install_args(self, spec, prefix):
        """Arguments to pass to install."""
        args = ['--prefix={0}'.format(prefix)]
        args += ['--single-version-externally-managed']

        # Get all relative paths since we set the root to `prefix`
        # We query the python with which these will be used for the lib and inc
        # directories. This ensures we use `lib`/`lib64` as expected by python.
        python = spec['python'].package.command
        command_start = 'print(distutils.sysconfig.'
        commands = ';'.join([
            'import distutils.sysconfig',
            command_start + 'get_python_lib(plat_specific=False, prefix=""))',
            command_start + 'get_python_lib(plat_specific=True, prefix=""))',
            command_start + 'get_python_inc(plat_specific=True, prefix=""))'])
        pure_site_packages_dir, plat_site_packages_dir, inc_dir = python(
            '-c', commands, output=str, error=str).strip().split('\n')

        args += ['--root=%s' % prefix,
                 '--install-purelib=%s' % pure_site_packages_dir,
                 '--install-platlib=%s' % plat_site_packages_dir,
                 '--install-scripts=bin',
                 '--install-data=',
                 '--install-headers=%s' % inc_dir
                 ]

        return args     
        
    @run_after('build')
    def build_python(self):
        """Build everything needed to install."""
        self.setup_py('build')
        
    @run_after('install')
    def install_python(self):
        spec = self.spec
        prefix = self.spec.prefix
        args = self.install_args(spec, prefix)
        
        self.setup_py('install', *args)
