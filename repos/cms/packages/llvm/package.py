# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import fnmatch
import glob
import os
import os.path
import re
import sys

import llnl.util.tty as tty

import spack.build_environment
import spack.util.executable


class Llvm(CMakePackage, CudaPackage):
    """The LLVM Project is a collection of modular and reusable compiler and
       toolchain technologies. Despite its name, LLVM has little to do
       with traditional virtual machines, though it does provide helpful
       libraries that can be used to build them. The name "LLVM" itself
       is not an acronym; it is the full name of the project.
    """

    homepage = "https://llvm.org/"
    git = "https://github.com/cms-externals/llvm-project.git"
    maintainers = ['trws', 'haampie']

    tags = ['e4s']

    generator = 'Ninja'

    family = "compiler"  # Used by lmod

    # fmt: off
    version("12.0.1.cms", commit="9f4ab770e61b68d2037cc7cda1f868a8ba52da85")
    resource(
        name='iwys',
        git='https://github.com/include-what-you-use/include-what-you-use.git',
        commit='5db414ac448004fe019871c977905cb7c2cff23f',
        destination='clang/tools'
    )
    # fmt: on

    build_targets = ['all', 'check-clang-tools']

    # NOTE: The debug version of LLVM is an order of magnitude larger than
    # the release version, and may take up 20-30 GB of space. If you want
    # to save space, build with `build_type=Release`.

    extends("python")

    # Build dependency
    depends_on("cmake@3.4.3:", type="build")
    depends_on('cmake@3.13.4:', type='build', when='@12:')
    depends_on("ninja", type="build")
    depends_on("binutils")

    # Universal dependency
    depends_on("python@2.7:2.8", when="@:4")
    depends_on("python", when="@5:")

    depends_on('zlib')
    depends_on('cuda', when='+cuda')

    variant('cuda', default=False)
    variant('cuda_arch', default='foo')

    # LLVM bug https://bugs.llvm.org/show_bug.cgi?id=48234
    # CMake bug: https://gitlab.kitware.com/cmake/cmake/-/issues/21469
    # Fixed in upstream versions of both
    conflicts('^cmake@3.19.0', when='@6.0.0:11.0.0')

    # The functions and attributes below implement external package
    # detection for LLVM. See:
    #
    # https://spack.readthedocs.io/en/latest/packaging_guide.html#making-a-package-discoverable-with-spack-external-find
    executables = ['clang', 'flang', 'ld.lld', 'lldb']

    def patch(self):
        filter_file("add_clang_subdirectory(libclang)", "add_clang_subdirectory(libclang)\nadd_subdirectory(include-what-you-use)", "clang/CMakeLists.txt")

    @property
    def cc(self):
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('c', None)
        result = None
        result = os.path.join(self.spec.prefix.bin, 'clang')
        return result

    @property
    def cxx(self):
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('cxx', None)
        result = None
        result = os.path.join(self.spec.prefix.bin, 'clang++')
        return result

    @property
    def fc(self):
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('fc', None)
        result = None
        return result

    @property
    def f77(self):
        msg = "cannot retrieve Fortran 77 compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('f77', None)
        result = None
        return result

    def flag_handler(self, name, flags):
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
            return(None, flags, None)
        elif name == 'ldflags' and self.spec.satisfies('%intel'):
            flags.append('-shared-intel')
            return(None, flags, None)
        return(flags, None, None)

    def setup_build_environment(self, env):
        """When using %clang, add only its ld.lld-$ver and/or ld.lld to our PATH"""
        if self.compiler.name in ['clang', 'apple-clang']:
            for lld in 'ld.lld-{0}'.format(self.compiler.version.version[0]), 'ld.lld':
                bin = os.path.join(os.path.dirname(self.compiler.cc), lld)
                sym = os.path.join(self.stage.path, 'ld.lld')
                if os.path.exists(bin) and not os.path.exists(sym):
                    mkdirp(self.stage.path)
                    os.symlink(bin, sym)
            env.prepend_path('PATH', self.stage.path)

    def setup_run_environment(self, env):
        if "+clang" in self.spec:
            env.set("CC", join_path(self.spec.prefix.bin, "clang"))
            env.set("CXX", join_path(self.spec.prefix.bin, "clang++"))

    root_cmakelists_dir = "llvm"

    def cmake_args(self):
        spec = self.spec
        define = CMakePackage.define
        from_variant = self.define_from_variant

        gcc = which("gcc")
        host_triple = gcc("-dumpmachine", output=str).strip()

        python = spec['python']
        cmake_args = [
            define("LLVM_ENABLE_PROJECTS", "clang;clang-tools-extra;compiler-rt;lld;openmp"),
            define("LLVM_LIBDIR_SUFFIX", "64"),
            define("LLVM_BINUTILS_INCDIR", self.spec['binutils'].prefix.include),
            define("LLVM_BUILD_LLVM_DYLIB", True),
            define("LLVM_LINK_LLVM_DYLIB", True),
            define("LLVM_ENABLE_EH", True),
            define("LLVM_ENABLE_PIC", True),
            define("LLVM_ENABLE_RTTI", True),
            define("LLVM_HOST_TRIPLE", host_triple),
            define("LLVM_TARGETS_TO_BUILD", "X86;PowerPC;AArch64;NVPTX"),
            define("LIBOMPTARGET_NVPTX_ALTERNATE_HOST_COMPILER", "/usr/bin/gcc"),
            define("LIBOMPTARGET_NVPTX_COMPUTE_CAPABILITIES", self.spec.variants['cuda_arch'].value),
            define("CMAKE_REQUIRED_INCLUDES", self.spec['zlib'].prefix.include),
            define("CMAKE_PREFIX_PATH", self.spec['zlib'].prefix)
        ]

        return cmake_args

    @run_after('build')
    def clang_t(self):
        build = self.build_directory
        ct = Executable(join_path(build, 'bin', 'clang-tidy'))
        out = ct('--checks=*','--list-checks', output=str.split)
        if 'cms-handle' not in out:
            raise RuntimeError("cms-handle not found")

    @run_after('install')
    def post_inst(self):
        # install_tree("llvm/bindings/python", site_packages_dir)
        install_tree("clang/bindings/python", site_packages_dir)

        for fn in glob.glob(join_path(self.build_directory, 'clang', 'tools', 'scan-build', 'set-xcode*')):
            force_remove(fn)

# TODO: is this needed?
#        install("clang/tools/scan-build", prefix.bin)
#        install("clang/tools/scan-view", prefix.bin)
        # Remove compiled AppleScript scripts, otherwise install_name_tool from
        # DEFAULT_INSTALL_POSTAMBLE will fail. These are non-object files.
        force_remove(join_path(prefix.bin, 'FileRadar.scpt'))
        force_remove(join_path(prefix.bin, 'GetRadarVersion.scpt'))
        # Avoid dependency on /usr/bin/python, Darwin + Xcode specific
        force_remove(join_path(prefix.bin, 'set-xcode-analyzer'))

        for fn in glob.glob(prefix.lib64.join('*.a')):
            if fnmatch.fnmatch('libomptarget-*.a', fn):
                continue
            force_remove(fn)
