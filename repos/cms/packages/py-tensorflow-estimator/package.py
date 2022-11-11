# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.package import *


class PyTensorflowEstimator(PythonPackage):
    """TensorFlow Estimator is a high-level TensorFlow API that greatly
    simplifies machine learning programming."""

    homepage = "https://github.com/tensorflow/estimator"
    # url = "https://github.com/tensorflow/estimator/archive/v2.2.0.tar.gz"
    url = "https://files.pythonhosted.org/packages/py2.py3/t/tensorflow-estimator/tensorflow_estimator-2.10.0-py2.py3-none-any.whl"

    maintainers = ["aweits"]

    # CMS: use wheel
    version(
        "2.10.0",
        sha256="f324ea17cd57f16e33bf188711d5077e6b2e5f5a12c328d6e01a07b23888edcd",
        expand=False,
    )

    extends("python")

    depends_on("python@3.7:", when="@2.9:", type=("build", "run"))

    # CMS: no restrictions
    depends_on("py-keras", type=("build", "run"))
    #    for ver in ["2.10", "2.9", "2.8", "2.7", "2.6"]:
    #        depends_on("py-keras@" + ver, when="@" + ver, type=("build", "run"))

    #    for ver in [
    #        "2.10",
    #        "2.9",
    #        "2.8",
    #        "2.7",
    #        "2.6",
    #        "2.5",
    #        "2.4",
    #        "2.3",
    #        "2.2",
    #        "2.1",
    #        "2.0",
    #        "1.13",
    #    ]:
    #        depends_on("py-tensorflow@" + ver, when="@" + ver, type=("build", "run"))
    # CMS: no restrictions
    depends_on("py-tensorflow", type=("build", "run"))

    depends_on("bazel@0.19.0:", type="build")
    depends_on("py-funcsigs@1.0.2:", type=("build", "run"), when="^python@:3.2")
