# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import itertools
import os
import stat
import sys
import tempfile

import llnl.util.filesystem as fs


class PyTensorflow(Package, CudaPackage):
    """TensorFlow is an Open Source Software Library for Machine Intelligence
    """

    homepage = "https://www.tensorflow.org"
    # url      = "https://github.com/tensorflow/tensorflow/archive/v2.3.1.tar.gz"
    git      = "https://github.com/cms-externals/tensorflow.git"

    maintainers = ['adamjstewart', 'aweits']
    import_modules = ['tensorflow']

    version('2.6.0.cms',  commit='719e00b6f9553de2662b6df2c353d6934e941103')
    version('2.5.0.cms',  commit='9b69eda15062cfec1b9c2d6f78c0fecbf9e67a34')

    variant('mkl', default=False, description='Build with MKL support')
    variant('jemalloc', default=False, description='Build with jemalloc as malloc support')
    variant('gcp', default=False, description='Build with Google Cloud Platform support')
    variant('hdfs', default=False, description='Build with Hadoop File System support')
    variant('aws', default=False, description='Build with Amazon AWS Platform support')
    variant('kafka', default=False, description='Build with Apache Kafka Platform support')
    variant('ignite', default=False, description='Build with Apache Ignite support')
    variant('xla', default=False, description='Build with XLA JIT support')
    variant('gdr', default=False, description='Build with GDR support')
    variant('verbs', default=False, description='Build with libverbs support')
    variant('ngraph', default=False, description='Build with Intel nGraph support')
    variant('opencl', default=False, description='Build with OpenCL SYCL support')
    variant('computecpp', default=False, description='Build with ComputeCPP support')
    variant('rocm', default=False, description='Build with ROCm support')
    variant('tensorrt', default=False, description='Build with TensorRT support')
    variant('cuda', default=sys.platform != 'darwin', description='Build with CUDA support')
    variant('nccl', default=sys.platform.startswith('linux'), description='Enable NVIDIA NCCL support')
    variant('mpi', default=False, description='Build with MPI support')
    variant('android', default=False, description='Configure for Android builds')
    variant('ios', default=False, description='Build with iOS support (macOS only)')
    variant('monolithic', default=False, description='Static monolithic build')
    variant('numa', default=False, description='Build with NUMA support')
    variant('dynamic_kernels', default=False, description='Build kernels into separate shared objects')
    variant('vectorize_flag', default='-msse3', description='Vectorization flag',
            values=('-msse3', '-march=nehalem', '-march=sandybridge', '-march=haswell',
                    '-march=skylake-avx512'))  # -- CMS
    variant('only_python', default=True, description='Only install Python wrapper')  # -- CMS

    extends('python')
    depends_on('python@3:', type=('build', 'run'), when='@2.1:')
    # python 3.8 support in tensorflow 2.2
    # see tensorflow issue #33374
    depends_on('python@:3.7', type=('build', 'run'), when='@:2.2')

    # TODO: Older versions of TensorFlow don't list the viable version range,
    # just the minimum version of bazel that will work. The latest version of
    # bazel doesn't seem to work, so for now we force them to use min version.
    # Need to investigate further.

    # See _TF_MIN_BAZEL_VERSION and _TF_MAX_BAZEL_VERSION in configure.py
    depends_on('bazel@3.1.0:3.99.0',  type='build', when='@2.3:')
    depends_on('bazel@2.0.0',         type='build', when='@2.2.0:2.2.999')
    depends_on('bazel@0.27.1:0.29.1', type='build', when='@2.1.0:2.1.999')
    depends_on('bazel@0.24.1:0.26.1', type='build', when='@1.15:2.0')
    # See call to check_bazel_version in configure.py
    depends_on('bazel@0.24.1:0.25.2', type='build', when='@1.14.0')
    depends_on('bazel@0.19.0:0.21.0', type='build', when='@1.13.0:1.13.2')
    depends_on('bazel@0.24.1:0.25.0', type='build', when='@1.12.1')
    depends_on('bazel@0.15.0',        type='build', when='@1.10:1.12.0,1.12.2:1.12.3')
    depends_on('bazel@0.10.0',        type='build', when='@1.7:1.9')
    # See call to check_version in tensorflow/workspace.bzl
    depends_on('bazel@0.5.4',         type='build', when='@1.4:1.6')
    # See MIN_BAZEL_VERSION in configure
    depends_on('bazel@0.4.5',         type='build', when='@1.2:1.3')
    # See call to check_version in WORKSPACE
    depends_on('bazel@0.4.2',         type='build', when='@1.0:1.1')
    depends_on('bazel@0.3.2',         type='build', when='@0.12.0:0.12.1')
    depends_on('bazel@0.3.0',         type='build', when='@0.11.0')
    depends_on('bazel@0.2.0',         type='build', when='@0.9:0.10')
    depends_on('bazel@0.1.4',         type='build', when='@0.7:0.8')
    depends_on('bazel@0.1.1',         type='build', when='@0.5:0.6')

    depends_on('swig', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-future', type='build', when='^python@:2')

    # Listed under REQUIRED_PACKAGES in tensorflow/tools/pip_package/setup.py
    depends_on('py-absl-py@0.10:0.999', type=('build', 'run'), when='@2.4.0:')
    depends_on('py-absl-py@0.7.0:', type=('build', 'run'), when='@1.12.1,1.14:2.3')
    depends_on('py-absl-py@0.1.6:', type=('build', 'run'), when='@1.5:1.11')

    depends_on('py-astunparse@1.6.3:1.6.999', type=('build', 'run'), when='@2.4.0:')
    depends_on('py-astunparse@1.6.3', type=('build', 'run'), when='@2.2:2.3')

    depends_on('py-astor@0.6.0:', type=('build', 'run'), when='@1.6:2.1')

    depends_on('py-backports-weakref@1.0:', type=('build', 'run'), when='@1.3: ^python@:3.3')
    depends_on('py-backports-weakref@1.0rc1', type=('build', 'run'), when='@1.2.0:1.2.1')

    depends_on('py-enum34@1.1.6:', type=('build', 'run'), when='@1.5: ^python@:3.3')
    depends_on('py-enum34@1.1.6:', type=('build', 'run'), when='@1.4.0:1.4.1')

    depends_on('py-gast@0.4.0:', type=('build', 'run'), when='@2.5.0.cms')
    #depends_on('py-gast@0.3.3', type=('build', 'run'), when='@2.2:2.4')
    #depends_on('py-gast@0.2.2', type=('build', 'run'), when='@1.15:2.1')
    #depends_on('py-gast@0.2.0:', type=('build', 'run'), when='@1.6:1.14')

    depends_on('py-google-pasta@0.2:0.999', type=('build', 'run'), when='@2.4.0:')
    depends_on('py-google-pasta@0.1.8:', type=('build', 'run'), when='@2.1:2.3')
    depends_on('py-google-pasta@0.1.6:', type=('build', 'run'), when='@1.14:2.0')
    depends_on('py-google-pasta@0.1.2:', type=('build', 'run'), when='@1.12.1')
    # propagate the mpi variant setting for h5py/hdf5 to avoid unexpected crashes
    depends_on('py-h5py@2.10.0:2.10.999+mpi', type=('build', 'run'), when='@2.2:+mpi')
    depends_on('py-h5py@2.10.0:2.10.999~mpi', type=('build', 'run'), when='@2.2:~mpi')

    depends_on('hdf5+mpi', type='build', when='@2.2:+mpi')
    depends_on('hdf5~mpi', type='build', when='@2.2:~mpi')

    depends_on('py-keras-applications@1.0.8:', type=('build', 'run'), when='@1.15:2.1')
    depends_on('py-keras-applications@1.0.6:', type=('build', 'run'), when='@1.12:1.14')
    depends_on('py-keras-applications@1.0.5:', type=('build', 'run'), when='@1.11.0:1.11.999')

    depends_on('py-keras-preprocessing@1.1.2:1.1.999', type=('build', 'run'), when='@2.4:')
    depends_on('py-keras-preprocessing@1.1.1:1.999', type=('build', 'run'), when='@2.3:2.3.999')
    depends_on('py-keras-preprocessing@1.1.0:', type=('build', 'run'), when='@2.1:2.2')
    depends_on('py-keras-preprocessing@1.0.5:', type=('build', 'run'), when='@1.12:2.0')
    depends_on('py-keras-preprocessing@1.0.3:', type=('build', 'run'), when='@1.11:1.11.999')
    # https://github.com/tensorflow/tensorflow/issues/40688
    depends_on('py-numpy@1.19.2:1.19.999',  type=('build', 'run'), when='@2.4.0:')
    depends_on('py-numpy@1.16.0:1.18',  type=('build', 'run'), when='@1.13.2,1.15:2.3')
    depends_on('py-numpy@1.14.5:1.18',  type=('build', 'run'), when='@1.12.1,1.14.0')
    depends_on('py-numpy@1.13.3:1.14.5', type=('build', 'run'), when='@1.10.0:1.10.1')
    depends_on('py-numpy@1.13.3:',       type=('build', 'run'), when='@1.6:1.9')
    depends_on('py-numpy@1.12.1:',       type=('build', 'run'), when='@1.4:1.5')
    depends_on('py-numpy@1.11.0:',       type=('build', 'run'), when='@0.11:1.3')
    depends_on('py-numpy@1.10.1:',       type=('build', 'run'), when='@0.7.1:0.7.999 platform=darwin')
    depends_on('py-numpy@1.8.2:',        type=('build', 'run'), when='@0.6:0.10')
    depends_on('py-numpy@1.9.2:',        type=('build', 'run'), when='@0.5.0')

    depends_on('py-opt-einsum@3.3.0:3.3.999', type=('build', 'run'), when='@2.4.0:')
    depends_on('py-opt-einsum@2.3.2:', type=('build', 'run'), when='@1.15:2.3')

    depends_on('py-protobuf@3.9.2:', type=('build', 'run'), when='@2.3:')
    depends_on('py-protobuf@3.8.0:', type=('build', 'run'), when='@2.1:2.2')
    depends_on('py-protobuf@3.6.1:', type=('build', 'run'), when='@1.12:2.0')
    depends_on('py-protobuf@3.6.0:', type=('build', 'run'), when='@1.10:1.11')
    depends_on('py-protobuf@3.4.0:', type=('build', 'run'), when='@1.5:1.9')
    depends_on('py-protobuf@3.3.0:', type=('build', 'run'), when='@1.3:1.4')
    depends_on('py-protobuf@3.2.0:', type=('build', 'run'), when='@1.1:1.2')
    depends_on('py-protobuf@3.1.0:', type=('build', 'run'), when='@0.12.1:1.0')
    depends_on('py-protobuf@3.1.0', type=('build', 'run'), when='@0.12.0')
    depends_on('py-protobuf@3.0.0', type=('build', 'run'), when='@0.11.0')
    depends_on('py-protobuf@3.0.0b2', type=('build', 'run'), when='@0.7.1:0.10')
    depends_on('py-protobuf@3.0.0a3', type=('build', 'run'), when='@0.6:0.7.0')

    depends_on('protobuf')

    # -- CMS: dependency type is build+link (default) dependency
    depends_on('flatbuffers+python@1.12.0:1.12.999', when='@2.4.0:', type=('build', 'link', 'run'))
    # tensorboard
    # tensorflow-estimator
    depends_on('py-termcolor@1.1.0:1.1.999', type=('build', 'run'), when='@2.4.0:')
    depends_on('py-termcolor@1.1.0:', type=('build', 'run'), when='@1.6:2.3')

    depends_on('py-wrapt@1.12.1:1.12.999', type=('build', 'run'), when='@2.4.0:')
    depends_on('py-wrapt@1.11.1:', type=('build', 'run'), when='@1.12.1,1.14:2.3')

    depends_on('py-wheel', type=('build', 'run'), when='@0.6:2.3')
    depends_on('py-wheel@0.26:', type=('build', 'run'), when='@0.6:2.3 ^python@3:')
    depends_on('py-wheel@0.35:0.999', type=('build', 'run'), when='@2.4.0: ^python@3:')

    depends_on('py-mock@2.0.0:', type=('build', 'run'), when='@0.10: ^python@:2')

    depends_on('py-functools32@3.2.3:', type=('build', 'run'), when='@1.15: ^python@:2')

    depends_on('py-six@1.15.0:1.15.999', type=('build', 'run'), when='@2.4.0:')
    depends_on('py-six@1.12.0:', type=('build', 'run'), when='@2.1:2.3')
    depends_on('py-six@1.10.0:', type=('build', 'run'), when='@:2.0')

    depends_on('py-scipy@1.2.2', type=('build', 'run'), when='@2.1.0:2.1.1,2.2.0,2.3.0 ^python@:2')
    depends_on('py-scipy@1.4.1', type=('build', 'run'), when='@2.1.0:2.1.1,2.2.0,2.3.0 ^python@3:')

    depends_on('py-typing-extensions@3.7.4:3.7.999', type=('build', 'run'), when='@2.4.0:')
    # depends_on('py-grpcio@1.8.6:', type=('build', 'run'), when='@1.6:1.7')

    if sys.byteorder == 'little':
        # Only builds correctly on little-endian machines
        depends_on('py-grpcio@1.8.6:', type=('build', 'run'), when='@1.8:2.3')
        depends_on('py-grpcio@1.32.0:', type=('build', 'run'), when='@2.4:')
        depends_on('grpc@1.35.0: +shared', type=('build', 'run'), when='@2.4.0:')

    # TODO: add packages for some of these dependencies
    depends_on('mkl', when='+mkl')
    depends_on('curl', when='+gcp')
    # depends_on('computecpp', when='+opencl+computecpp')
    # depends_on('trisycl',    when='+opencl~computepp')
    depends_on('cuda@:10.2', when='+cuda @:2.3')
    depends_on('cuda@:11.1', when='+cuda @2.4.0:')
    depends_on('cudnn', when='+cuda')
    depends_on('cudnn@6.5', when='@0.5:0.6 +cuda')
    # depends_on('tensorrt', when='+tensorrt')
    depends_on('nccl', when='+nccl')
    depends_on('mpi', when='+mpi')
    # depends_on('android-ndk@10:18', when='+android')
    # depends_on('android-sdk', when='+android')
    # -- CMS
    depends_on('py-cython')
#    depends_on('py-google-common')
    depends_on('py-pybind11')
    depends_on('eigen')
    depends_on('zlib')
    depends_on('libpng')
    depends_on('libjpeg-turbo')
    depends_on('curl')
    depends_on('pcre', when='@2.5.0.cms')
    depends_on('giflib')
    depends_on('sqlite')
    depends_on('grpc@1.35.0:')
    # -- end CMS

    # Check configure and configure.py to see when these variants are supported
    conflicts('+mkl', when='@:1.0')
    conflicts('+mkl', when='platform=darwin', msg='Darwin is not yet supported')
    conflicts('+jemalloc', when='@:0')
    conflicts('+jemalloc', when='platform=darwin', msg='Currently jemalloc is only support on Linux platform')
    conflicts('+jemalloc', when='platform=cray',   msg='Currently jemalloc is only support on Linux platform')
    conflicts('+gcp', when='@:0.8')
    conflicts('+hdfs', when='@:0.10')
    conflicts('+aws', when='@:1.3')
    conflicts('+kafka', when='@:1.5,2.1:')
    conflicts('+ignite', when='@:1.11,2.1:')
    conflicts('+xla', when='@:0')
    conflicts('+gdr', when='@:1.3')
    conflicts('+verbs', when='@:1.1')
    conflicts('+ngraph', when='@:1.10')
    conflicts('+opencl', when='@:0.11')
    conflicts('+computecpp', when='@:0.11')
    conflicts('+computecpp', when='~opencl')
    conflicts('+rocm', when='@:1.11')
    conflicts('+cuda', when='platform=darwin', msg='There is no GPU support for macOS')
    conflicts('cuda_arch=none', when='+cuda', msg='Must specify CUDA compute capabilities of your GPU, see https://developer.nvidia.com/cuda-gpus')
    conflicts('cuda_arch=20', when='@1.12.1,1.14:', msg='TensorFlow only supports compute capabilities >= 3.5')
    conflicts('cuda_arch=30', when='@1.12.1,1.14:', msg='TensorFlow only supports compute capabilities >= 3.5')
    conflicts('cuda_arch=32', when='@1.12.1,1.14:', msg='TensorFlow only supports compute capabilities >= 3.5')
    conflicts('cuda_arch=20', when='@1.4:1.12.0,1.12.2:1.12.3', msg='Only compute capabilities 3.0 or higher are supported')
    conflicts('+tensorrt', when='@:1.5')
    conflicts('+tensorrt', when='~cuda')
    conflicts('+tensorrt', when='platform=darwin', msg='Currently TensorRT is only supported on Linux platform')
    conflicts('+tensorrt', when='platform=cray',   msg='Currently TensorRT is only supported on Linux platform')
    conflicts('+nccl', when='@:1.7')
    conflicts('+nccl', when='~cuda')
    conflicts('+nccl', when='platform=darwin', msg='Currently NCCL is only supported on Linux platform')
    conflicts('+nccl', when='platform=cray',   msg='Currently NCCL is only supported on Linux platform')
    conflicts('+mpi', when='@:1.2')
    conflicts('+android', when='@:1.4')
    conflicts('+ios', when='@:1.12.0,1.12.2:1.13')
    conflicts('+ios', when='platform=linux', msg='iOS support only available on macOS')
    conflicts('+ios', when='platform=cray',  msg='iOS support only available on macOS')
    conflicts('+monolithic', when='@:1.3')
    conflicts('+numa', when='@:1.12.0,1.12.2:1.13')
    conflicts('+dynamic_kernels', when='@:1.12.0,1.12.2:1.12.3')

    # TODO: why is this needed?
    patch('url-zlib.patch',  when='@0.10.0')
    # TODO: why is this needed?
    patch('crosstool.patch', when='@0.10.0+cuda')
    # Avoid build error: "no such package '@io_bazel_rules_docker..."
    patch('io_bazel_rules_docker2.patch', when='@1.15:2.0')
    # Avoide build error: "name 'new_http_archive' is not defined"
    patch('http_archive.patch', when='@1.12.3')
    # Backport of 837c8b6b upstream
    # "Remove contrib cloud bigtable and storage ops/kernels."
    # Allows 2.0.* releases to build with '--config=nogcp'
    patch('0001-Remove-contrib-cloud-bigtable-and-storage-ops-kernel.patch',
          when='@2.0.0:2.0.999')

    # for fcc
    patch('1-1_fcc_tf_patch.patch', when='@2.1.0:2.1.99%fj')

    # do not import contrib.cloud if not available
    patch('https://github.com/tensorflow/tensorflow/commit/ed62ac8203999513dfae03498e871ea35eb60cc4.patch',
          sha256='c37d14622a86b164e2411ea45a04f756ac61b2044d251f19ab17733c508e5305', when='@1.14.0')
    # import_contrib_cloud patch for older versions
    patch('contrib_cloud_1.10.patch', when='@1.10:1.13')
    patch('contrib_cloud_1.9.patch', when='@1.9')
    patch('contrib_cloud_1.4.patch', when='@1.4:1.8')
    patch('contrib_cloud_1.1.patch', when='@1.1:1.3')

    phases = ['configure', 'build', 'install']

    # https://www.tensorflow.org/install/source
    def setup_build_environment(self, env):
        spec = self.spec

        # Please specify the location of python
        env.set('PYTHON_BIN_PATH', spec['python'].command.path)

        # Please input the desired Python library path to use
        env.set('PYTHON_LIB_PATH', site_packages_dir)

        # Ensure swig is in PATH or set SWIG_PATH
        env.set('SWIG_PATH', spec['swig'].prefix.bin.swig)

        # Do you wish to build TensorFlow with MKL support?
        if '+mkl' in spec:
            env.set('TF_NEED_MKL', '1')

            # Do you wish to download MKL LIB from the web?
            env.set('TF_DOWNLOAD_MKL', '0')

            # Please specify the location where MKL is installed
            env.set('MKL_INSTALL_PATH', spec['mkl'].prefix)
        else:
            env.set('TF_NEED_MKL', '0')

        # Do you wish to build TensorFlow with jemalloc as malloc support?
        if '+jemalloc' in spec:
            env.set('TF_NEED_JEMALLOC', '1')
        else:
            env.set('TF_NEED_JEMALLOC', '0')

        # Do you wish to build TensorFlow with Google Cloud Platform support?
        if '+gcp' in spec:
            env.set('TF_NEED_GCP', '1')
        else:
            env.set('TF_NEED_GCP', '0')

        # Do you wish to build TensorFlow with Hadoop File System support?
        if '+hdfs' in spec:
            env.set('TF_NEED_HDFS', '1')
        else:
            env.set('TF_NEED_HDFS', '0')

        # Do you wish to build TensorFlow with Amazon AWS Platform support?
        if '+aws' in spec:
            env.set('TF_NEED_AWS', '1')
            env.set('TF_NEED_S3', '1')
        else:
            env.set('TF_NEED_AWS', '0')
            env.set('TF_NEED_S3', '0')

        # Do you wish to build TensorFlow with Apache Kafka Platform support?
        if '+kafka' in spec:
            env.set('TF_NEED_KAFKA', '1')
        else:
            env.set('TF_NEED_KAFKA', '0')

        # Do you wish to build TensorFlow with Apache Ignite support?
        if '+ignite' in spec:
            env.set('TF_NEED_IGNITE', '1')
        else:
            env.set('TF_NEED_IGNITE', '0')

        # Do you wish to build TensorFlow with XLA JIT support?
        if '+xla' in spec:
            env.set('TF_ENABLE_XLA', '1')
        else:
            env.set('TF_ENABLE_XLA', '0')

        # Do you wish to build TensorFlow with GDR support?
        if '+gdr' in spec:
            env.set('TF_NEED_GDR', '1')
        else:
            env.set('TF_NEED_GDR', '0')

        # Do you wish to build TensorFlow with VERBS support?
        if '+verbs' in spec:
            env.set('TF_NEED_VERBS', '1')
        else:
            env.set('TF_NEED_VERBS', '0')

        # Do you wish to build TensorFlow with nGraph support?
        if '+ngraph' in spec:
            env.set('TF_NEED_NGRAPH', '1')
        else:
            env.set('TF_NEED_NGRAPH', '0')

        # Do you wish to build TensorFlow with OpenCL SYCL support?
        if '+opencl' in spec:
            env.set('TF_NEED_OPENCL_SYCL', '1')
            env.set('TF_NEED_OPENCL', '1')

            # Please specify which C++ compiler should be used as the host
            # C++ compiler
            env.set('HOST_CXX_COMPILER', spack_cxx)

            # Please specify which C compiler should be used as the host
            # C compiler
            env.set('HOST_C_COMPILER', spack_cc)

            # Do you wish to build TensorFlow with ComputeCPP support?
            if '+computecpp' in spec:
                env.set('TF_NEED_COMPUTECPP', '1')

                # Please specify the location where ComputeCpp is installed
                env.set('COMPUTECPP_TOOLKIT_PATH', spec['computecpp'].prefix)
            else:
                env.set('TF_NEED_COMPUTECPP', '0')

                # Please specify the location of the triSYCL include directory
                env.set('TRISYCL_INCLUDE_DIR', spec['trisycl'].prefix.include)
        else:
            env.set('TF_NEED_OPENCL_SYCL', '0')
            env.set('TF_NEED_OPENCL', '0')

        # Do you wish to build TensorFlow with ROCm support?
        if '+rocm' in spec:
            env.set('TF_NEED_ROCM', '1')
        else:
            env.set('TF_NEED_ROCM', '0')

        # Do you wish to build TensorFlow with CUDA support?
        if '+cuda' in spec:
            env.set('TF_NEED_CUDA', '1')

            # Do you want to use clang as CUDA compiler?
            env.set('TF_CUDA_CLANG', '0')

            # Please specify which gcc nvcc should use as the host compiler
            env.set('GCC_HOST_COMPILER_PATH', spack_cc)

            cuda_paths = [
                spec['cuda'].prefix,
                spec['cudnn'].prefix,
            ]

            # Do you wish to build TensorFlow with TensorRT support?
            if '+tensorrt' in spec:
                env.set('TF_NEED_TENSORRT', '1')

                cuda_paths.append(spec['tensorrt'].prefix)

                # Please specify the TensorRT version you want to use
                env.set('TF_TENSORRT_VERSION',
                        spec['tensorrt'].version.up_to(1))

                # Please specify the location where TensorRT is installed
                env.set('TENSORRT_INSTALL_PATH', spec['tensorrt'].prefix)
            else:
                env.set('TF_NEED_TENSORRT', '0')
                env.unset('TF_TENSORRT_VERSION')

            # Please specify the CUDA SDK version you want to use
            env.set('TF_CUDA_VERSION', spec['cuda'].version.up_to(2))

            # Please specify the cuDNN version you want to use
            env.set('TF_CUDNN_VERSION', spec['cudnn'].version.up_to(1))

            if '+nccl' in spec:
                cuda_paths.append(spec['nccl'].prefix)

                # Please specify the locally installed NCCL version to use
                env.set('TF_NCCL_VERSION', spec['nccl'].version.up_to(1))

                # Please specify the location where NCCL is installed
                env.set('NCCL_INSTALL_PATH', spec['nccl'].prefix)
                env.set('NCCL_HDR_PATH', spec['nccl'].prefix.include)
            else:
                env.unset('TF_NCCL_VERSION')

            # Please specify the comma-separated list of base paths to
            # look for CUDA libraries and headers
            env.set('TF_CUDA_PATHS', ','.join(cuda_paths))

            # Please specify the location where CUDA toolkit is installed
            env.set('CUDA_TOOLKIT_PATH', spec['cuda'].prefix)

            # Please specify the location where CUDNN library is installed
            env.set('CUDNN_INSTALL_PATH', spec['cudnn'].prefix)

            # Please specify a list of comma-separated CUDA compute
            # capabilities you want to build with. You can find the compute
            # capability of your device at:
            # https://developer.nvidia.com/cuda-gpus.
            # Please note that each additional compute capability significantly
            # increases your build time and binary size, and that TensorFlow
            # only supports compute capabilities >= 3.5
            capabilities = ','.join('{0:.1f}'.format(
                float(i) / 10.0) for i in spec.variants['cuda_arch'].value)
            env.set('TF_CUDA_COMPUTE_CAPABILITIES', capabilities)
        else:
            env.set('TF_NEED_CUDA', '0')

        # Do you wish to download a fresh release of clang? (Experimental)
        env.set('TF_DOWNLOAD_CLANG', '0')

        # Do you wish to build TensorFlow with MPI support?
        if '+mpi' in spec:
            env.set('TF_NEED_MPI', '1')

            # Please specify the MPI toolkit folder
            env.set('MPI_HOME', spec['mpi'].prefix)
        else:
            env.set('TF_NEED_MPI', '0')
            env.unset('MPI_HOME')

        # Please specify optimization flags to use during compilation when
        # bazel option '--config=opt' is specified
        env.set('CC_OPT_FLAGS', spec.target.optimization_flags(
            spec.compiler.name, spec.compiler.version))

        # Would you like to interactively configure ./WORKSPACE for
        # Android builds?
        if '+android' in spec:
            env.set('TF_SET_ANDROID_WORKSPACE', '1')

            # Please specify the home path of the Android NDK to use
            env.set('ANDROID_NDK_HOME', spec['android-ndk'].prefix)
            env.set('ANDROID_NDK_API_LEVEL', spec['android-ndk'].version)

            # Please specify the home path of the Android SDK to use
            env.set('ANDROID_SDK_HOME', spec['android-sdk'].prefix)
            env.set('ANDROID_SDK_API_LEVEL', spec['android-sdk'].version)

            # Please specify the Android SDK API level to use
            env.set('ANDROID_API_LEVEL', spec['android-sdk'].version)

            # Please specify an Android build tools version to use
            env.set('ANDROID_BUILD_TOOLS_VERSION', spec['android-sdk'].version)
        else:
            env.set('TF_SET_ANDROID_WORKSPACE', '0')

        # Do you wish to build TensorFlow with iOS support?
        if '+ios' in spec:
            env.set('TF_CONFIGURE_IOS', '1')
        else:
            env.set('TF_CONFIGURE_IOS', '0')

        # set tmpdir to a non-NFS filesystem
        # (because bazel uses ~/.cache/bazel)
        # TODO: This should be checked for non-nfsy filesystem, but the current
        #       best idea for it is to check
        #           subprocess.call([
        #               'stat', '--file-system', '--format=%T', tmp_path
        #       ])
        #       to not be nfs. This is only valid for Linux and we'd like to
        #       stay at least also OSX compatible
        tmp_path = tempfile.mkdtemp(prefix='spack')
        env.set('TEST_TMPDIR', tmp_path)
        env.set('TF_CMS_EXTERNALS', join_path(tmp_path, 'cms_externals.txt'))

        with open(join_path(tmp_path, 'cms_externals.txt'), "w") as f:
            f.write("png:" + self.spec["libpng"].prefix + "\n")
            f.write("libjpeg_turbo:" + self.spec["libjpeg-turbo"].prefix + "\n")
            f.write("zlib:" + self.spec["zlib"].prefix + "\n")
            f.write("eigen_archive:" + self.spec["eigen"].prefix + "\n")
            f.write("curl:" + self.spec["curl"].prefix + "\n")
            f.write("com_google_protobuf:" + self.spec["py-protobuf"].prefix + "\n")
            f.write("com_github_grpc_grpc:" + self.spec["grpc"].prefix + "\n")
            if self.spec.satisfies('@2.5.0.cms'):
                f.write("pcre:" + self.spec["pcre"].prefix + "\n")
            f.write("gif:" + self.spec["giflib"].prefix + "\n")
            f.write("org_sqlite:" + self.spec["sqlite"].prefix + "\n")
            f.write("cython:" + "\n")
            f.write("flatbuffers:" + self.spec["flatbuffers"].prefix + "\n")
            f.write("pybind11:" + self.spec["py-pybind11"].prefix + "\n")
            f.write("functools32_archive:" + "\n")
            f.write("enum34_archive:" + "\n")
            f.write("astor_archive:" + "\n")
            f.write("six_archive:" + "\n")
            f.write("absl_py:" + "\n")
            f.write("termcolor_archive:" + "\n")
            f.write("typing_extensions_archive:" + "\n")
            f.write("pasta:" + "\n")
            f.write("wrapt:" + "\n")
            f.write("gast_archive:" + "\n")
            f.write("org_python_pypi_backports_weakref:" + "\n")
            f.write("opt_einsum_archive:" + "\n")

        if self.spec.satisfies('@2.5.0.cms:'):
            env.set('TF_SYSTEM_LIBS', 'png,libjpeg_turbo,zlib,eigen_archive,curl,com_google_protobuf,com_github_grpc_grpc,pcre,gif,org_sqlite,cython,flatbuffers,functools32_archive,enum34_archive,astor_archive,six_archive,absl_py,termcolor_archive,typing_extensions_archive,pasta,wrapt,gast_archive,org_python_pypi_backports_weakref,opt_einsum_archive')
        else:
            env.set('TF_SYSTEM_LIBS', 'png,libjpeg_turbo,zlib,eigen_archive,curl,com_google_protobuf,com_github_grpc_grpc,gif,org_sqlite,cython,flatbuffers,functools32_archive,enum34_archive,astor_archive,six_archive,absl_py,termcolor_archive,typing_extensions_archive,pasta,wrapt,gast_archive,org_python_pypi_backports_weakref,opt_einsum_archive')
        # NOTE: INCLUDEDIR is not just relevant to protobuf
        # see third_party/systemlibs/jsoncpp.BUILD
        env.set('INCLUDEDIR', spec['protobuf'].prefix.include)

        # -- CMS
        env.set('GCC_HOST_COMPILER_PATH', spack_cc)
        env.set('CC_OPT_FLGCC_HOST_COMPILER_PATHAGS', '-Wno-sign-compare')

#    def patch(self):
#        if self.spec.satisfies('@2.3.0:'):
#            filter_file('deps = protodeps + well_known_proto_libs(),',
#                        'deps = protodeps,',
#                        'tensorflow/core/platform/default/build_config.bzl',
#                        string=True)
#        if self.spec.satisfies('@2.4.0:'):
#            text = '''
#def protobuf_deps():
#    pass
#'''
#            with open('third_party/systemlibs/protobuf_deps.bzl', 'w') as f:
#                f.write(text)
#            filter_file(
#                '"//third_party/systemlibs:protobuf.bzl": "protobuf.bzl",',
#                '"//third_party/systemlibs:protobuf.bzl": "protobuf.bzl",\n'
#                '"//third_party/systemlibs:protobuf_deps.bzl": "protobuf_deps.bzl",',  # noqa: E501
#                'tensorflow/workspace.bzl',
#                string=True)

    def configure(self, spec, prefix):
        # NOTE: configure script is interactive. If you set the appropriate
        # environment variables, this interactivity is skipped. If you don't,
        # Spack hangs during the configure phase. Use `spack build-env` to
        # determine which environment variables must be set for a particular
        # version.
        configure()

    @run_after('configure')
    def post_configure_fixes(self):
        spec = self.spec

        # make sure xla is actually turned off
        if spec.satisfies('~xla'):
            filter_file(r'--define with_xla_support=true',
                        r'--define with_xla_support=false',
                        '.tf_configure.bazelrc')

        if spec.satisfies('@1.5.0: ~android'):
            # env variable is somehow ignored -> brute force
            # TODO: find a better solution
            filter_file(r'if workspace_has_any_android_rule\(\)',
                        r'if True',
                        'configure.py')

        # version dependent fixes
        if spec.satisfies('@1.3.0:1.5.0'):
            # checksum for protobuf that bazel downloads (@github) changed
            filter_file(r'sha256 = "6d43b9d223ce09e5d4ce8b0060cb8a7513577a35a64c7e3dad10f0703bf3ad93"',
                        r'sha256 = "e5fdeee6b28cf6c38d61243adff06628baa434a22b5ebb7432d2a7fbabbdb13d"',
                        'tensorflow/workspace.bzl')
            # starting with tensorflow 1.3, tensorboard becomes a dependency
            # (...but is not really needed? Tensorboard should depend on
            # tensorflow, not the other way!)
            # -> remove from list of required packages
            filter_file(r"'tensorflow-tensorboard",
                        r"#'tensorflow-tensorboard",
                        'tensorflow/tools/pip_package/setup.py')
        if spec.satisfies('@1.5.0: ~gcp'):
            # google cloud support seems to be installed on default, leading
            # to boringssl error manually set the flag to false to avoid
            # installing gcp support
            # https://github.com/tensorflow/tensorflow/issues/20677#issuecomment-404634519
            filter_file(r'--define with_gcp_support=true',
                        r'--define with_gcp_support=false',
                        '.tf_configure.bazelrc')
        if spec.satisfies('@1.6.0:'):
            # tensorboard name changed
            filter_file(r"'tensorboard >=",
                        r"#'tensorboard >=",
                        'tensorflow/tools/pip_package/setup.py')
        if spec.satisfies('@1.8.0: ~opencl'):
            # 1.8.0 and 1.9.0 aborts with numpy import error during python_api
            # generation somehow the wrong PYTHONPATH is used...
            # set --distinct_host_configuration=false as a workaround
            # https://github.com/tensorflow/tensorflow/issues/22395#issuecomment-431229451
            filter_file('build --action_env TF_NEED_OPENCL_SYCL="0"',
                        'build --action_env TF_NEED_OPENCL_SYCL="0"\n'
                        'build --distinct_host_configuration=false\n'
                        'build --action_env PYTHONPATH="{0}"'.format(
                            env['PYTHONPATH']),
                        '.tf_configure.bazelrc')
        if spec.satisfies('@1.13.1'):
            # tensorflow_estimator is an API for tensorflow
            # tensorflow-estimator imports tensorflow during build, so
            # tensorflow has to be set up first
            filter_file(r"'tensorflow_estimator >=",
                        r"#'tensorflow_estimator >=",
                        'tensorflow/tools/pip_package/setup.py')
        if spec.satisfies('@2.0.0:'):
            # now it depends on the nightly versions...
            filter_file(r"'tf-estimator-nightly >=",
                        r"#'tf-estimator-nightly >=",
                        'tensorflow/tools/pip_package/setup.py')
            filter_file(r"REQUIRED_PACKAGES\[i\] = 'tb-nightly >=",
                        r"pass #REQUIRED_PACKAGES\[i\] = 'tb-nightly >=",
                        'tensorflow/tools/pip_package/setup.py')
            filter_file(r"'tb-nightly >=",
                        r"#'tb-nightly >=",
                        'tensorflow/tools/pip_package/setup.py')

        if spec.satisfies('@1.13.1 +nccl'):
            filter_file(
                r'^build --action_env NCCL_INSTALL_PATH=.*',
                r'build --action_env NCCL_INSTALL_PATH="' +
                spec['nccl'].libs.directories[0] + '"',
                '.tf_configure.bazelrc')
            filter_file(
                r'^build --action_env NCCL_HDR_PATH=.*',
                r'build --action_env NCCL_HDR_PATH="' +
                spec['nccl'].prefix.include + '"',
                '.tf_configure.bazelrc')

        # see tensorflow issue #31187 on github
        if spec.satisfies('@2.0.0:2.0.999'):
            filter_file(r'\#define RUY_DONOTUSEDIRECTLY_AVX512 1',
                        '#define RUY_DONOTUSEDIRECTLY_AVX512 0',
                        'tensorflow/lite/experimental/ruy/platform.h')

        if spec.satisfies('+cuda'):
            libs = spec['cuda'].libs.directories
            libs.extend(spec['cudnn'].libs.directories)
            if '+nccl' in spec:
                libs.extend(spec['nccl'].libs.directories)
            if '+tensorrt' in spec:
                libs.extend(spec['tensorrt'].libs.directories)
            slibs = ':'.join(libs)

            filter_file('build --action_env TF_NEED_OPENCL_SYCL="0"',
                        'build --action_env TF_NEED_OPENCL_SYCL="0"\n'
                        'build --action_env LD_LIBRARY_PATH="' + slibs + '"',
                        '.tf_configure.bazelrc')

        filter_file('build:opt --copt=-march=native', '',
                    '.tf_configure.bazelrc')
        filter_file('build:opt --host_copt=-march=native', '',
                    '.tf_configure.bazelrc')

    def build(self, spec, prefix):
        tmp_path = env['TEST_TMPDIR']

        # https://docs.bazel.build/versions/master/command-line-reference.html
        args = [
            # Don't allow user or system .bazelrc to override build settings
            '--nohome_rc',
            '--nosystem_rc',
            # Bazel does not work properly on NFS, switch to /tmp
            '--output_user_root=' + tmp_path,
            'build',
            '-s', # -- CMS
            # Spack logs don't handle colored output well
            '--color=no',
            '--jobs={0}'.format(make_jobs),
            '--config=opt',
            # Enable verbose output for failures
            '--verbose_failures',
            '--distinct_host_configuration=false', # -- CMS
            # Show (formatted) subcommands being executed
            '--subcommands=pretty_print',
            # Ask bazel to explain what it's up to
            # Needs a filename as argument
            '--explain=explainlogfile.txt',
            # Increase verbosity of explanation,
            '--verbose_explanations',
        ]

        if spec.satisfies('^bazel@:3.5'):
            # removed in bazel 3.6
            args.append('--incompatible_no_support_tools_in_action_inputs=false')

        # See .bazelrc for when each config flag is supported
        if spec.satisfies('@1.12.1:'):
            if '+mkl' in spec:
                args.append('--config=mkl')

            if '+monolithic' in spec:
                args.append('--config=monolithic')

            if '+gdr' in spec:
                args.append('--config=gdr')

            if '+verbs' in spec:
                args.append('--config=verbs')

            if '+ngraph' in spec:
                args.append('--config=ngraph')

            if '+dynamic_kernels' in spec:
                args.append('--config=dynamic_kernels')

            if '+cuda' in spec:
                args.append('--config=cuda')

            if '~aws' in spec:
                args.append('--config=noaws')

            if '~gcp' in spec:
                args.append('--config=nogcp')

            if '~hdfs' in spec:
                args.append('--config=nohdfs')

            if '~nccl' in spec:
                args.append('--config=nonccl')

        if spec.satisfies('@1.12.1:2.0'):
            if '~ignite' in spec:
                args.append('--config=noignite')

            if '~kafka' in spec:
                args.append('--config=nokafka')

        if spec.satisfies('@1.12.1,1.14:'):
            if '+numa' in spec:
                args.append('--config=numa')

        if spec.satisfies('@2:'):
            args.append('--config=v2')

        # -- CMS
        args.insert(0, '--batch')
        if self.spec.satisfies('target=x86_64:') and self.spec.variants['vectorize_flag'].value:
            args.append('--copt=' + self.spec.variants['vectorize_flag'].value)

        if self.spec.satisfies('target=ppc64le'):
            args.extend(['--copt=-mcpu=native', '--copt=-mtune=native'])
            args.extend(['--copt=--param=l1-cache-size=64', '--copt=--param=l1-cache-line-size=128', '--copt=--param=l2-cache-size=512'])

        if not (self.spec.satisfies('target=ppc64le') or self.spec.satisfies('target=x86_64:')):
            args.extend(['--copt=-mcpu=native', '--copt=-mtune=native'])

        args.append('--cxxopt=-std=c++17')
        # -- end CMS

        args.append('//tensorflow/tools/pip_package:build_pip_package')

        bazel(*args)

        if self.spec.satisfies('~only_python'):  #  -- CMS
            for target in ('//tensorflow:tensorflow', '//tensorflow:tensorflow_cc', '//tensorflow/tools/graph_transforms:transform_graph', '//tensorflow/compiler/tf2xla:tf2xla', '//tensorflow/compiler/xla:cpu_function_runtime', '//tensorflow/compiler/xla:executable_run_options', '//tensorflow/compiler/tf2xla:xla_compiled_cpu_function', '//tensorflow/core/profiler', '//tensorflow:install_headers'):
                args[-1] = target
                bazel(*args)

            protoc = which('protoc')

            for entry in glob.glob(join_path(self.stage.source_path, 'bazel-bin', 'tensorflow', 'include', '**'), recursive=True):
                if not os.path.islink(entry):
                    mode = os.stat(entry).st_mode
                    mode |= (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP |stat.S_IROTH | stat.S_IWOTH)
                    if mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
                        mode |= (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

                    os.chmod(entry, mode)
                    

            for root, dirs, files in os.walk(join_path(self.stage.source_path, 'tensorflow')):
                for fn in files:
                    if fn.endswith('.proto'):
                        protoc('--cpp_out={0}/bazel-bin/tensorflow/include'.format(self.stage.source_path),
                               '--proto_path={0}'.format(self.stage.source_path),
                               join_path(root, fn))

        build_pip_package = Executable(
            'bazel-bin/tensorflow/tools/pip_package/build_pip_package')
        buildpath = join_path(self.stage.source_path, 'spack-build')
        build_pip_package('--src', buildpath)

    def install(self, spec, prefix):
        tmp_path = env['TEST_TMPDIR']
        buildpath = join_path(self.stage.source_path, 'spack-build')

        srcdir = join_path(self.stage.source_path, 'bazel-bin', 'tensorflow')
        outdir = self.spec.prefix
        bindir = outdir.bin
        incdir = outdir.include
        libdir = outdir.lib
        mkdirp(bindir)
        mkdirp(incdir)
        mkdirp(libdir)

        for fn in glob.glob(join_path(srcdir, 'libtensorflow*.so*')):
            install(fn, libdir)

        for fn in glob.glob(join_path(srcdir, 'compiler', 'tf2xla', 'lib*.so*')):
            install(fn, libdir)

        for fn in glob.glob(join_path(srcdir, 'compiler', 'xla', 'lib*.so*')):
            install(fn, libdir)

        realversion = str(self.spec.version)
        majorversion = str(self.spec.version.up_to(1))
        for l in ('tensorflow_cc', 'tensorflow_framework', 'tensorflow'):
            if not os.path.exists(join_path(libdir, 'lib{0}.so.{1}'.format(l, realversion))):
                continue

            force_symlink(join_path(libdir, 'lib{0}.so.{1}'.format(l, realversion)), join_path(libdir, 'lib{0}.so.{1}'.format(l, majorversion)))
            force_symlink(join_path(libdir, 'lib{0}.so.{1}'.format(l, majorversion)), join_path(libdir, 'lib{0}.so'.format(l)))

        for name in ('tensorflow', 'absl', 're2', 'third_party'):
            install_tree(join_path(srcdir, 'include', name), incdir)

        def copy_headers(arg_1, arg_2):
            root_1 = arg_1.rstrip('/') + '/'
            headers = [s.replace(root_1, '') for s in fs.find(join_path(arg_1, arg_2), '*.h')]
            for header_file in headers:
                header_dir = join_path(incdir, os.path.dirname(header_file))
                mkdirp(header_dir)
                install(header_file, header_dir)

        copy_headers(self.stage.source_path, 'tensorflow/compiler')
        copy_headers(self.stage.source_path, 'tensorflow/core/profiler/internal')
        copy_headers(self.stage.source_path, 'tensorflow/core/profiler/lib')
        with working_dir(buildpath):
            setup_py('install', '--prefix={0}'.format(prefix),
                     '--single-version-externally-managed', '--root=/')

        for root, dirs, files in os.walk(tmp_path):
            for file in files:
                entry = join_path(root, file)
                if not os.path.islink(entry):
                    fmode = os.stat(entry).st_mode
                    os.chmod(entry, fmode | stat.S_IREAD | stat.S_IWRITE)
        remove_linked_tree(tmp_path)

        # -- CMS
        for fn in glob.glob(join_path(prefix.bin, 'tensorboard*')):
            os.remove(fn)


    def test(self):
        """Attempts to import modules of the installed package."""

        # Make sure we are importing the installed modules,
        # not the ones in the source directory
        for module in self.import_modules:
            self.run_test(self.spec['python'].command.path,
                          ['-c', 'import {0}'.format(module)],
                          purpose='checking import of {0}'.format(module),
                          work_dir='spack-test')
