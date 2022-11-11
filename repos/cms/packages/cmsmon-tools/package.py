# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class CmsmonTools(Package):
    """cmsmon-tools"""

    homepage = "https://www.example.com"
    url = "https://github.com/dmwm/CMSMonitoring/releases/download/0.5.35/cmsmon-tools.tar.gz"

    linuxarch = "linux-amd64"
    arch = "amd64"
    promv = "2.31.1"
    amver = "0.23.0"
    heyver = "0.0.2"
    sternv = "1.11.0"
    apsver = "0.2.15"
    k8s_info_ver = "0.0.1"
    trivyver = "0.21.1"
    gocurlver = "0.0.4"

    version(
        "0.5.35",
        sha256="0cbdb4df3ad6c2a0481aa6bf800e6ca751d8d85c1535a68ce6bf1edddbc54d33",
    )
    resource(
        name="prometheus",
        url="https://github.com/prometheus/prometheus/releases/download/v{0}/prometheus-{0}.{1}.tar.gz".format(
            promv, linuxarch
        ),
        destination="prometheus",
        sha256="7852dc11cfaa039577c1804fe6f082a07c5eb06be50babcffe29214aedf318b3",
    )
    resource(
        name="alertmanager",
        url="https://github.com/prometheus/alertmanager/releases/download/v{0}/alertmanager-{0}.{1}.tar.gz".format(
            amver, linuxarch
        ),
        destination="alertmanager",
        sha256="77793c4d9bb92be98f7525f8bc50cb8adb8c5de2e944d5500e90ab13918771fc",
    )
    resource(
        name="hey-tools",
        url="https://github.com/vkuznet/hey/releases/download/{0}/hey-tools.tar.gz".format(
            heyver
        ),
        destination="hey-tools",
        sha256="fa807b2b52e6a9b5f4396a077ae94d60d5c652e41991537e856b4aa845135540",
    )
    resource(
        name="stern",
        url="https://github.com/wercker/stern/releases/download/{0}/stern_linux_amd64".format(
            sternv
        ),
        expand=False,
        sha256="e0b39dc26f3a0c7596b2408e4fb8da533352b76aaffdc18c7ad28c833c9eb7db",
        placement="stern",
    )
    resource(
        name="auth-proxy-server",
        url="https://github.com/vkuznet/auth-proxy-server/releases/download/{0}/auth-proxy-tools_amd64.tar.gz".format(
            apsver
        ),
        sha256="9c166172c157277b4c5b1a885766985c228b6d4c260c124dd0ab3bab8639feb8",
        destination="auth-proxy-tools",
    )
    resource(
        name="k8s_info",
        url="https://github.com/vkuznet/k8s_info/releases/download/{0}/k8s_info-tools.tar.gz".format(
            k8s_info_ver
        ),
        sha256="5a5493f3d11fcd0455ec0f2c184ee5b6a65468ead4b3aadd8bded6ef601762cd",
        destination="k8s_info",
    )
    resource(
        name="trivy",
        url="https://github.com/aquasecurity/trivy/releases/download/v{0}/trivy_{0}_Linux-64bit.tar.gz".format(
            trivyver
        ),
        sha256="4900136f41c713ce8d202e9aa055543a11e56bc280bc864719d4343dc2d3e696",
        placement="trivy",
    )
    resource(
        name="gocurl",
        url="https://github.com/vkuznet/gocurl/releases/download/{0}/gocurl-tools.tar.gz".format(
            gocurlver
        ),
        sha256="00aba5b67574fc1fdb11c5b5a6e1a0bb2486323d167f50eb8ac11b4b6a6da960",
        destination="gocurl",
    )

    def setup_build_environment(self, env):
        env.set("CGO_ENABLED", "0")
        env.set("GOCACHE", join_path(self.stage.path, "gocache"))

    def install(self, spec, prefix):
        # copy CMS monitoring tools
        for (
            cmd
        ) in (
            "monit ggus_parser alert annotationManager nats-sub nats-pub dbs_vm".split()
        ):
            install(cmd, prefix)

        # add prometheus, alertmanager tools to our install area
        install(
            join_path(
                "prometheus",
                "prometheus-{0}.{1}".format(self.promv, self.linuxarch),
                "promtool",
            ),
            prefix,
        )
        install(
            join_path(
                "prometheus",
                "prometheus-{0}.{1}".format(self.promv, self.linuxarch),
                "prometheus",
            ),
            prefix,
        )
        install(
            join_path(
                "alertmanager",
                "alertmanager-{0}.{1}".format(self.amver, self.linuxarch),
                "amtool",
            ),
            prefix,
        )

        # build hey tools
        install(
            join_path("hey-tools", "hey-tools", "hey_amd64"), join_path(prefix, "hey")
        )
        set_executable(join_path(prefix, "hey"))

        # install stern
        install(join_path("stern", "stern_linux_amd64"), join_path(prefix, "stern"))
        set_executable(join_path(prefix, "stern"))

        # install token-manager
        install(
            join_path(
                "auth-proxy-tools",
                "auth-proxy-tools_{0}".format(self.arch),
                "token-manager",
            ),
            prefix,
        )
        install(
            join_path(
                "auth-proxy-tools",
                "auth-proxy-tools_{0}".format(self.arch),
                "auth-token",
            ),
            prefix,
        )

        # install k8s_info
        install(
            join_path("k8s_info", "k8s_info-tools", "k8s_info_amd64"),
            join_path(prefix, "k8s_info"),
        )
        set_executable(join_path(prefix, "k8s_info"))

        # install stern
        install(join_path("trivy", "trivy"), prefix)
        set_executable(join_path(prefix, "trivy"))

        # install gocurl
        install(
            join_path("gocurl", "gocurl-tools", "gocurl_amd64"),
            join_path(prefix, "gocurl"),
        )
        set_executable(join_path(prefix, "gocurl"))

        # CMS scripts
        install(join_path(os.path.dirname(__file__), "*.sh"), prefix)
        install(join_path(os.path.dirname(__file__), ".cmsmon-tools"), prefix)

        shared_arch = self.spec.old_format("${ARCHITECTURE}")

        filter_file(
            "SHARED_ARCH=.*",
            f'SHARED_ARCH="{shared_arch}"',
            join_path(prefix, ".cmsmon-tools"),
        )
