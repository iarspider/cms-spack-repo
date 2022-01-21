# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import os

from six import iteritems


class Rust(Package):
    """The Rust programming language toolchain

    This package can bootstrap any version of the Rust compiler since Rust
    1.23. It does this by downloading the platform-appropriate binary
    distribution of the desired version of the rust compiler, and then building
    that compiler from source.
    """

    homepage = "https://www.rust-lang.org"
    url = "https://github.com/rust-lang/rust/archive/refs/tags/1.57.0.tar.gz"
    git = "https://github.com/rust-lang/rust.git"

    maintainers = ["AndrewGaspar"]

    phases = ['configure', 'build', 'install']

    extendable = True
    cargo_dir = ''

    depends_on('python@2.7:', type='build')
    depends_on('llvm', type=('build', 'run'))

    version('1.57.0', sha256='0ed7a28619b4b77dfd80239bc30d92f3e7da29029b3a5dac0ea10aa5ed9a5cba')

    # This dictionary maps Rust target architectures to Spack constraints that
    # match that target.
    rust_archs = {
        'x86_64-unknown-linux-gnu': [
            {'platform': 'linux', 'target': 'x86_64:'},
            {'platform': 'cray', 'target': 'x86_64:'}
        ],
        'powerpc64le-unknown-linux-gnu': [
            {'platform': 'linux', 'target': 'ppc64le:'},
            {'platform': 'cray', 'target': 'ppc64le:'}
        ],
        'aarch64-unknown-linux-gnu': [
            {'platform': 'linux', 'target': 'aarch64:'},
            {'platform': 'cray', 'target': 'aarch64:'}
        ],
        'x86_64-apple-darwin': [
            {'platform': 'darwin', 'target': 'x86_64:'}
        ]
    }

    executables = ['^rustc$']

    @classmethod
    def determine_version(csl, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.match(r'rustc (\S+)', output)
        return match.group(1) if match else None

    # This routine returns the target architecture we intend to build for.
    def get_rust_target(self):
        if 'platform=linux' in self.spec or 'platform=cray' in self.spec:
            if 'target=x86_64:' in self.spec:
                return 'x86_64-unknown-linux-gnu'
            elif 'target=ppc64le:' in self.spec:
                return 'powerpc64le-unknown-linux-gnu'
            elif 'target=aarch64:' in self.spec:
                return 'aarch64-unknown-linux-gnu'
        elif 'platform=darwin target=x86_64:' in self.spec:
            return 'x86_64-apple-darwin'

        raise InstallError(
            "rust is not supported for '{0}'".format(
                self.spec.architecture
            ))

    def configure(self, spec, prefix):
        rust_arch = self.get_rust_target()
        with open('config.toml', 'w') as out_file:
            out_file.write("""\
[llvm]
link-shared = true
 
[build]
docs = false
extend = true
build = "{rust_arch}"

[rust]
channel = "stable"
rpath = true
codegen-tests = false

[target.{rust_arch}]
llvm-config = {llvm_config}

[install]
prefix = "{prefix}"
sysconfdir = "etc"
""".format(
                rust_arch=rust_arch,
                prefix=prefix,
                llvm_config=os.path.join(self.spec['llvm'].prefix.bin, 'llvm-config')
            )
            )

    def build(self, spec, prefix):
        python('./x.py', 'build', '-vv', '--exclude', 'src/tools/mri', '-j', str(self.make_jobs))

    def install(self, spec, prefix):
        python('./x.py', 'install', '-vv', '--exclude', 'src/tools/mri', '-j', str(self.make_jobs), extra_env={'RUSTUP_HOME': prefix})

    def setup_build_environment(self, env):
        self.cargo_dir = join_path(self.stage.path, 'cargo_home')
        env.set('CARGO_HOME', self.cargo_dir)