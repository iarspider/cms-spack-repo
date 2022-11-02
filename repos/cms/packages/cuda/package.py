# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import re
import shutil
import tempfile
from glob import glob

import llnl.util.tty as tty
from llnl.util.filesystem import LibraryList

from spack import *

# FIXME Remove hack for polymorphic versions
# This package uses a ugly hack to be able to dispatch, given the same
# version, to different binary packages based on the platform that is
# running spack. See #13827 for context.
# If you need to add a new version, please be aware that:
#  - versions in the following dict are automatically added to the package
#  - version tuple must be in the form (checksum, url)
#  - checksum must be sha256
#  - package key must be in the form '{os}-{arch}' where 'os' is in the
#    format returned by platform.system() and 'arch' by platform.machine()

_versions = {
    '11.5.2': {
        'Linux-aarch64': ('31337c8bdc224fa1bd07bc4b6a745798392428118cc8ea0fa4446ee4ad47dd30', 'https://developer.download.nvidia.com/compute/cuda/11.5.2/local_installers/cuda_11.5.2_495.29.05_linux_sbsa.run'),
        'Linux-x86_64':  ('74959abf02bcba526f0a3aae322c7641b25da040ccd6236d07038f81997b73a6', 'https://developer.download.nvidia.com/compute/cuda/11.5.2/local_installers/cuda_11.5.2_495.29.05_linux.run'),
        'Linux-ppc64le': ('45c468f430436b3e95d5e485a6ba0ec1fa2b23dc6c551c1307b79996ecf0a7ed', 'https://developer.download.nvidia.com/compute/cuda/11.5.2/local_installers/cuda_11.5.2_495.29.05_linux_ppc64le.run')},
    '11.4.2': {
        'Linux-aarch64': ('f2c4a52e06329606c8dfb7c5ea3f4cb4c0b28f9d3fdffeeb734fcc98daf580d8', 'https://developer.download.nvidia.com/compute/cuda/11.4.2/local_installers/cuda_11.4.2_470.57.02_linux_sbsa.run'),
        'Linux-x86_64':  ('bbd87ca0e913f837454a796367473513cddef555082e4d86ed9a38659cc81f0a', 'https://developer.download.nvidia.com/compute/cuda/11.4.2/local_installers/cuda_11.4.2_470.57.02_linux.run'),
        'Linux-ppc64le': ('a917c2e53dc13fdda7def71fd40920bf3809d5a2caa3e9acfe377fb9fb22f12d', 'https://developer.download.nvidia.com/compute/cuda/11.4.2/local_installers/cuda_11.4.2_470.57.02_linux_ppc64le.run')},
    '11.4.1': {
        'Linux-aarch64': ('8efa725a41dfd3c0c0f453c2dd535d149154102bf2b791718859417b4f84f922', 'https://developer.download.nvidia.com/compute/cuda/11.4.1/local_installers/cuda_11.4.1_470.57.02_linux_sbsa.run'),
        'Linux-x86_64':  ('dd6c339a719989d2518f5d54eeac1ed707d0673f8664ba0c4d4b2af7c3ba0005', 'https://developer.download.nvidia.com/compute/cuda/11.4.1/local_installers/cuda_11.4.1_470.57.02_linux.run'),
        'Linux-ppc64le': ('dd92ca04f76ad938da3480e2901c0e52dbff6028ada63c09071ed9e3055dc361', 'https://developer.download.nvidia.com/compute/cuda/11.4.1/local_installers/cuda_11.4.1_470.57.02_linux_ppc64le.run')},
    '11.2.2': {
        'Linux-aarch64': ('878cbd36c5897468ef28f02da50b2f546af0434a8a89d1c724a4d2013d6aa993', 'https://developer.download.nvidia.com/compute/cuda/11.2.2/local_installers/cuda_11.2.2_460.32.03_linux_sbsa.run'),
        'Linux-x86_64':  ('0a2e477224af7f6003b49edfd2bfee07667a8148fe3627cfd2765f6ad72fa19d', 'https://developer.download.nvidia.com/compute/cuda/11.2.2/local_installers/cuda_11.2.2_460.32.03_linux.run'),
        'Linux-ppc64le': ('2304ec235fe5d1f8bf75f00dc2c2d11473759dc23428dbbd5fb5040bc8c757e3', 'https://developer.download.nvidia.com/compute/cuda/11.2.2/local_installers/cuda_11.2.2_460.32.03_linux_ppc64le.run')}
}


class Cuda(Package):
    """CUDA is a parallel computing platform and programming model invented
    by NVIDIA. It enables dramatic increases in computing performance by
    harnessing the power of the graphics processing unit (GPU).

    Note: This package does not currently install the drivers necessary
    to run CUDA. These will need to be installed manually. See:
    https://docs.nvidia.com/cuda/ for details."""

    homepage = "https://developer.nvidia.com/cuda-zone"

    maintainers = ['ax3l', 'Rombur']
    executables = ['^nvcc$']

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1], expand=False)

    # macOS Mojave drops NVIDIA graphics card support -- official NVIDIA
    # drivers do not exist for Mojave. See
    # https://devtalk.nvidia.com/default/topic/1043070/announcements/faq-about-macos-10-14-mojave-nvidia-drivers/
    # Note that a CUDA Toolkit installer does exist for macOS Mojave at
    # https://developer.nvidia.com/compute/cuda/10.1/Prod1/local_installers/cuda_10.1.168_mac.dmg,
    # but support for Mojave is dropped in later versions, and none of the
    # macOS NVIDIA drivers at
    # https://www.nvidia.com/en-us/drivers/cuda/mac-driver-archive/ mention
    # Mojave support -- only macOS High Sierra 10.13 is supported.
    conflicts('arch=darwin-mojave-x86_64')

    depends_on('libxml2', when='@10.1.243:')
    depends_on('python@2.7:')

    # Required for newer (post-0.17.0) Spack versions
    variant('allow-unsupported-compilers', default=False,
        description='Allow unsupported host compiler and CUDA version combinations')


    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'Cuda compilation tools, release .*?, V(\S+)',
                          output)
        return match.group(1) if match else None

    def setup_build_environment(self, env):
        if self.spec.satisfies('@10.1.243:'):
            libxml2_home = self.spec['libxml2'].prefix
            env.set('LIBXML2HOME', libxml2_home)
            env.append_path('LD_LIBRARY_PATH', libxml2_home.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('CUDAHOSTCXX', dependent_spec.package.compiler.cxx)

    def setup_run_environment(self, env):
        env.set('CUDA_HOME', self.prefix)

    def install(self, spec, prefix):
        mkdirp(prefix.build)
        mkdirp(prefix.tmp)

#        if os.path.exists('/tmp/cuda-installer.log'):
#            try:
#                os.remove('/tmp/cuda-installer.log')
#            except OSError:
#                if spec.satisfies('@10.1:'):
#                    tty.die("The cuda installer will segfault due to the "
#                            "presence of /tmp/cuda-installer.log "
#                            "please remove the file and try again ")
        runfile = glob(join_path(self.stage.source_path, 'cuda*_linux*'))[0]
        driver_version = os.path.basename(runfile).split('_')[2]

        install_shell = which('sh')
        arguments = [
            runfile,
            "--silent",
            "--override",
            "--tmpdir={0}".format(prefix.tmp),
            "--installpath={0}".format(prefix.build),
            "--toolkit",
            "--keep"
        ]

        # extract and repackage the CUDA runtime
        install_shell(*arguments)

        # create target directory structure
        mkdirp(prefix.include)
        mkdirp(prefix.lib64)
        mkdirp(prefix.lib64.stubs)

        # package only the runtime static libraries
        install(join_path(prefix.build.lib64, 'libcudadevrt.a'), prefix.lib64)
        install(join_path(prefix.build.lib64, 'libcudart_static.a'), prefix.lib64)
        for fn in glob(join_path(prefix.build.lib64, 'lib*.a')):
            force_remove(fn)

        # package only the CUDA driver and NVML library stub
        install(join_path(prefix.build.lib64.stubs, 'libcuda.so'), prefix.lib64.stubs)
        os.symlink(join_path(prefix.lib64.stubs, 'libcuda.so'), join_path(prefix.lib64.stubs, 'libcuda.so.1'))
        install(join_path(prefix.build.lib64.stubs, 'libnvidia-ml.so'), prefix.lib64.stubs)
        os.symlink(join_path(prefix.lib64.stubs, 'libnvidia-ml.so'), join_path(prefix.lib64.stubs, 'libnvidia-ml.so.1'))
        shutil.rmtree(join_path(prefix.build.lib64.stubs))

        # do not package the OpenCL libraries
        #rm -f %_builddir/build/lib64/libOpenCL.*
        for fn in glob(join_path(prefix.build.lib64, 'libOpenCL.*')):
            force_remove(fn)

        # package the dynamic libraries
        install_tree(prefix.build.lib64, prefix.lib64)

        # package the includes
        install_tree(prefix.build.include, prefix.include)

        # package the CUDA Profiling Tools Interface includes and libraries
        for fn in glob(join_path(prefix.build.extras.CUPTI.lib64, '*.so*')):
            install(fn, prefix.lib64)

        for fn in glob(join_path(prefix.build.extras.CUPTI.include, '*.h')):
            install(fn, prefix.include)

        # leave out the Nsight and NVVP graphical tools, and package the other binaries
        force_remove(join_path(prefix.build.bin, 'computeprof'))
        force_remove(join_path(prefix.build.bin, 'cuda-uninstaller'))
        for fn in glob(join_path(prefix.build.bin, 'ncu*')):
            force_remove(fn)

        for fn in glob(join_path(prefix.build.bin, 'nsight*')):
            force_remove(fn)

        for fn in glob(join_path(prefix.build.bin, 'nsys*')):
            force_remove(fn)

        for fn in glob(join_path(prefix.build.bin, 'nv-nsight*')):
            force_remove(fn)

        force_remove(join_path(prefix.build.bin, 'nvpp'))

        install_tree(prefix.build.bin, prefix.bin)

        # package the cuda-gdb support files, and rename the binary to use it via a wrapper
        install_tree(join_path(prefix.build.share), prefix.share)
        shutil.move(join_path(prefix.bin, 'cuda-gdb'), join_path(prefix.bin, 'cuda-gdb.real'))
        with open(join_path(prefix.bin, 'cuda-gdb'), 'w') as f:
            print('#! /bin/bash', file=f)
            print('export PYTHONHOME=' + self.spec['python'].prefix, file=f)
            print('exec {0} "$@"'.format(join_path(prefix.bin, 'cuda-gdb.real')), file=f)

        set_executable(join_path(prefix.bin, 'cuda-gdb'))

        # package the Compute Sanitizer, and replace the wrapper with a symlink
        shutil.move(join_path(prefix.build, 'compute-sanitizer'), prefix)
        force_remove(join_path(prefix.bin, 'compute-sanitizer'))
        force_symlink('../compute-sanitizer/compute-sanitizer', join_path(prefix.bin, 'compute-sanitizer'))

        # package the NVVM compiler (cicc), library (libnvvm.so), device library (libdevice.10.bc) and samples
        install_tree(join_path(prefix.build, 'nvvm'), prefix.nvvm)

        # extract and repackage the NVIDIA libraries needed by the CUDA runtime
        runfile = glob(join_path('pkg', 'builds', '*.run'))[0]
        arguments = [
            runfile,
            '--silent',
            '--extract-only',
            '--tmpdir={0}'.format(prefix.tmp),
            '--target={0}'.format(prefix.build.drivers)
        ]

        install_shell(*arguments)
        # --target is ignored for some reason, so move things by hand
        nvidia_dir = glob('NVIDIA*')[0]
        shutil.move(nvidia_dir, prefix.build.drivers)

        mkdirp(prefix.drivers)
        install(join_path(prefix.build.drivers, 'libcuda.so.{0}'.format(driver_version)), prefix.drivers)
        install(join_path(prefix.build.drivers, 'libnvidia-ptxjitcompiler.so.{0}'.format(driver_version)), prefix.drivers)
        install(join_path(prefix.nvvm.lib64, 'libnvvm.so.4.0.0'), prefix.drivers)
        with working_dir(prefix):
            force_symlink('libcuda.so.{0}'.format(driver_version), join_path('drivers', 'libcuda.so.1'))
            force_symlink('libcuda.so.1', join_path('drivers', 'libcuda.so'))
            force_symlink('libnvidia-ptxjitcompiler.so.{0}'.format(driver_version), join_path('drivers', 'libnvidia-ptxjitcompiler.so.1'))
            force_symlink('libnvidia-ptxjitcompiler.so.1', join_path('drivers', 'libnvidia-ptxjitcompiler.so'))
        with working_dir(prefix.drivers):
            force_symlink('libnvvm.so.4.0.0', 'libnvvm.so.4')
            force_symlink('libnvvm.so.4', 'libnvvm.so')

        filter_file(r'\$(_HERE_)', '$(TOP)/bin', join_path(prefix, 'bin', 'nvcc.profile'))
        filter_file(r'/\$(_TARGET_DIR_)', '', join_path(prefix, 'bin', 'nvcc.profile'))
        filter_file(r'\$(_TARGET_SIZE_)', '64', join_path(prefix, 'bin', 'nvcc.profile'))

        shutil.rmtree(prefix.build)
        shutil.rmtree(prefix.tmp)

    @property
    def libs(self):
        libs = find_libraries('libcudart', root=self.prefix, shared=True,
                              recursive=True)

        filtered_libs = []
        # CUDA 10.0 provides Compatability libraries for running newer versions
        # of CUDA with older drivers. These do not work with newer drivers.
        for lib in libs:
            parts = lib.split(os.sep)
            if 'compat' not in parts and 'stubs' not in parts:
                filtered_libs.append(lib)
        return LibraryList(filtered_libs)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.append_path('LD_LIBRARY_PATH', self.spec.prefix.lib64.stubs)
