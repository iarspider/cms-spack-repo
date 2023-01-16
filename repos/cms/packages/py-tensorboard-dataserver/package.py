# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import platform


class PyTensorboardDataserver(Package):
    """Fast data loading for TensorBoard"""

    homepage = "https://github.com/tensorflow/tensorboard"
    url = (
        "https://github.com/tensorflow/tensorboard/tree/master/tensorboard/data/server"
    )

    maintainers = ["aweits"]
    if sys.platform == "darwin":
        version(
            "0.6.1",
            expand=False,
            sha256="fa8cef9be4fcae2f2363c88176638baf2da19c5ec90addb49b1cde05c95c88ee",
            url="https://files.pythonhosted.org/packages/3e/48/dd135dbb3cf16bfb923720163493cab70e7336db4b5f3103d49efa730404/tensorboard_data_server-0.6.1-py3-none-macosx_10_9_x86_64.whl",
        )
    elif platform.machine() == "ppc64le" or platform.machine() == 'aarch64':
        version('0.6.1', expand=False, sha256='809fe9887682d35c1f7d1f54f0f40f98bb1f771b14265b453ca051e2ce58fca7',
                url='https://files.pythonhosted.org/packages/74/69/5747a957f95e2e1d252ca41476ae40ce79d70d38151d2e494feb7722860c/tensorboard_data_server-0.6.1-py3-none-any.whl')
    else:
        version(
            "0.6.1",
            expand=False,
            sha256="d8237580755e58eff68d1f3abefb5b1e39ae5c8b127cc40920f9c4fb33f4b98a",
            url="https://files.pythonhosted.org/packages/60/f9/802efd84988bffd9f644c03b6e66fde8e76c3aa33db4279ddd11c5d61f4b/tensorboard_data_server-0.6.1-py3-none-manylinux2010_x86_64.whl",
        )

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-wheel@0.26:", type="build")
    depends_on("py-pip", type="build")

    extends("python")

    # copied from py-azureml-core
    def install(self, spec, prefix):
        pip = which("pip")
        pip(
            "install",
            "--no-deps",
            self.stage.archive_file,
            "--prefix={0}".format(prefix),
        )
