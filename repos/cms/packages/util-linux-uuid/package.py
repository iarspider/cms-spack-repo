# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from glob import glob

from spack import *


class UtilLinuxUuid(AutotoolsPackage):
    """Util-linux is a suite of essential utilities for any Linux system."""

    homepage = "https://github.com/karelzak/util-linux"
    url = "https://www.kernel.org/pub/linux/utils/util-linux/v2.29/util-linux-2.29.2.tar.gz"
    list_url = "https://www.kernel.org/pub/linux/utils/util-linux"
    list_depth = 1

    version(
        "2.36.2",
        sha256="f5dbe79057e7d68e1a46fc04083fc558b26a49499b1b3f50e4f4893150970463",
    )
    version(
        "2.36",
        sha256="82942cd877a989f6d12d4ce2c757fb67ec53d8c5cd9af0537141ec5f84a2eea3",
    )
    version(
        "2.34",
        sha256="b62c92e5e1629642113cd41cec1ee86d1ee7e36b8ffe8ec3ac89c11797e9ac25",
    )

    depends_on("pkgconfig", type="build")

    provides("uuid")
    keep_archives = True

    def url_for_version(self, version):
        url = "https://www.kernel.org/pub/linux/utils/util-linux/v{0}/util-linux-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    @property
    def libs(self):
        return find_libraries("libuuid", self.prefix, recursive=True)

    @property
    def headers(self):
        return find_headers("uuid", self.prefix, recursive=True)

    def configure_args(self):
        # -- CMS
        config_args = [
            "--disable-use-tty-group",
            "--disable-makeinstall-chown",
            "--without-systemd",
            "--disable-tls",
            "--disable-libblkid",
            "--disable-libmount",
            "--disable-mount",
            "--disable-losetup",
            "--disable-fsck",
            "--disable-partx",
            "--disable-mountpoint",
            "--disable-fallocate",
            "--disable-unshare",
            "--disable-eject",
            "--disable-agetty",
            "--disable-cramfs",
            "--disable-wdctl",
            "--disable-switch_root",
            "--disable-pivot_root",
            "--disable-kill",
            "--disable-utmpdump",
            "--disable-rename",
            "--disable-login",
            "--disable-sulogin",
            "--disable-su",
            "--disable-schedutils",
            "--disable-wall",
            "--disable-makeinstall-setuid",
            "--without-ncurses",
            "--enable-libuuid",
            "--disable-bash-completion",
        ]
        return config_args

    # -- CMS
    def build(self, spec, prefix):
        make("uuidd")

    # -- CMS
    def install(self, spec, prefix):
        # make('install', parallel=False)
        mkdirp(prefix.lib64)
        for fn in glob(join_path(self.stage.source_path, ".libs", "libuuid.a*")):
            install(join_path(self.stage.source_path, ".libs", fn), prefix.lib64)
        for fn in glob(join_path(self.stage.source_path, ".libs", "libuuid.so*")):
            install(join_path(self.stage.source_path, ".libs", fn), prefix.lib64)
        mkdirp(prefix.include)
        make("install-uuidincHEADERS")
