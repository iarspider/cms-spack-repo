import os
import platform
import re

import llnl.util.tty as tty

from spack import *


class Go(Package):
    """The golang compiler and build environment"""

    homepage = "https://golang.org"
    url = "https://dl.google.com/go/go1.16.6.src.tar.gz"
    git = "https://go.googlesource.com/go.git"

    extendable = True
    executables = ["^go$"]

    provides("golang")

    _versions = {
        "1.16": {
            "Linux-x86_64": (
                "013a489ebb3e24ef3d915abe5b94c3286c070dfe0818d5bca8108f1d6e8440d2",
                "https://storage.googleapis.com/golang/go1.16.linux-amd64.tar.gz",
            ),
            "Linux-aarch64": (
                "3770f7eb22d05e25fbee8fb53c2a4e897da043eb83c69b9a14f8d98562cd8098",
                "https://storage.googleapis.com/golang/go1.16.linux-arm64.tar.gz",
            ),
            "Linux-ppc64le": (
                "27a1aaa988e930b7932ce459c8a63ad5b3333b3a06b016d87ff289f2a11aacd6",
                "https://storage.googleapis.com/golang/go1.16.linux-ppc64le.tar.gz",
            ),
        }
    }

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1])

    def setup_build_environment(self, env):
        env.set("GOROOT_FINAL", self.spec.prefix)
        # We need to set CC/CXX_FOR_TARGET, otherwise cgo will use the
        # internal Spack wrappers and fail.
        env.set("CC_FOR_TARGET", self.compiler.cc)
        env.set("CXX_FOR_TARGET", self.compiler.cxx)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before go modules' install() methods.
        In most cases, extensions will only need to set GOPATH and use go::
        env['GOPATH'] = self.source_path + ':' + env['GOPATH']
        go('get', '<package>', env=env)
        install_tree('bin', prefix.bin)
        """
        #  Add a go command/compiler for extensions
        module.go = self.spec["go"].command

    def generate_path_components(self, dependent_spec):
        if os.environ.get("GOROOT", False):
            tty.warn("GOROOT is set, this is not recommended")

        # Set to include paths of dependencies
        path_components = [dependent_spec.prefix]
        for d in dependent_spec.traverse():
            if d.package.extends(self.spec):
                path_components.append(d.prefix)
        return ":".join(path_components)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # This *MUST* be first, this is where new code is installed
        env.prepend_path("GOPATH", self.generate_path_components(dependent_spec))

    def setup_dependent_run_environment(self, env, dependent_spec):
        # Allow packages to find this when using module files
        env.prepend_path("GOPATH", self.generate_path_components(dependent_spec))

    def install(self, spec, prefix):
        install_tree(".", prefix)
