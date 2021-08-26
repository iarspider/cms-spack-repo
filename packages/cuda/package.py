# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from glob import glob
from llnl.util.filesystem import LibraryList
import os
import re
import platform
import shutil
import tempfile
import llnl.util.tty as tty

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
    '11.2.2': {
        'Linux-aarch64': ('878cbd36c5897468ef28f02da50b2f546af0434a8a89d1c724a4d2013d6aa993', 'https://developer.download.nvidia.com/compute/cuda/11.2.2/local_installers/cuda_11.2.2_460.32.03_linux_sbsa.run'),
        'Linux-x86_64': ('0a2e477224af7f6003b49edfd2bfee07667a8148fe3627cfd2765f6ad72fa19d', 'https://developer.download.nvidia.com/compute/cuda/11.2.2/local_installers/cuda_11.2.2_460.32.03_linux.run'),
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

        if os.path.exists('/tmp/cuda-installer.log'):
            try:
                os.remove('/tmp/cuda-installer.log')
            except OSError:
                if spec.satisfies('@10.1:'):
                    tty.die("The cuda installer will segfault due to the "
                            "presence of /tmp/cuda-installer.log "
                            "please remove the file and try again ")
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

        # package only the runtime static library
        install(join_path(prefix.build.lib64, 'libcudadevrt.a'), prefix.lib64)
        for fn in glob(join_path(prefix.build.lib64, 'lib*.a')):
            force_remove(fn)

        # package only the CUDA driver and NVML library stub
        install(join_path(prefix.build.lib64.stubs, 'libcuda.so'), prefix.lib64.stubs)
        install(join_path(prefix.build.lib64.stubs, 'libnvidia-ml.so'), prefix.lib64.stubs)
        shutil.rmtree(join_path(prefix.build.lib64.stubs))

        # do not package the OpenCL libraries
        #rm -f %_builddir/build/lib64/libOpenCL.*
        for fn in glob(join_path(prefix.build.lib64, 'libOpenCL.*')):
            force_remove(fn)

        # package the dynamic libraries
        for fn in glob(join_path(prefix.build.lib64, '*.so')):
            install(fn, prefix.lib64)

        # package the includes
        for fn in glob(join_path(prefix.build.include, '*.h*')):
            install(fn, prefix.include)

        # package the CUDA Profiling Tools Interface includes and libraries
        for fn in glob(join_path(prefix.build.extras.CUPTI.lib64, '*.so')):
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
        with working_dir(prefix):
            force_symlink(join_path('drivers', 'libcuda.so.{0}'.format(driver_version)), 'libcuda.so.1')
            force_symlink(join_path('drivers', 'libcuda.so.1'), 'libcuda.so')
            force_symlink(join_path('drivers', 'libnvidia-ptxjitcompiler.so.{0}'.format(driver_version)), 'libnvidia-ptxjitcompiler.so.1')
            force_symlink(join_path('drivers', 'libnvidia-ptxjitcompiler.so.1'), 'libnvidia-ptxjitcompiler.so')

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
