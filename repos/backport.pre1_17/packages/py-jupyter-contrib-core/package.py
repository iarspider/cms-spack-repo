# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterContribCore(PythonPackage):
    """Common utilities for jupyter-contrib projects."""

    homepage = "https://github.com/jupyter-contrib/jupyter_contrib_core"
    pypi     = "jupyter_contrib_core/jupyter_contrib_core-0.3.3.tar.gz"

    version('0.3.3', sha256='e65bc0e932ff31801003cef160a4665f2812efe26a53801925a634735e9a5794')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-jupyter-core', type=('build', 'run'))
    depends_on('py-notebook@4.0:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-traitlets', type=('build', 'run'))
    depends_on('py-tornado', type=('build', 'run'))
