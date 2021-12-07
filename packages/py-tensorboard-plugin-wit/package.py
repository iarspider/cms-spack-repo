# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile


class PyTensorboardPluginWit(Package):
    """The What-If Tool makes it easy to efficiently and
       intuitively explore up to two models' performance
       on a dataset. Investigate model performances for
       a range of features in your dataset, optimization
       strategies and even manipulations to individual
       datapoint values. All this and more, in a visual way
       that requires minimal code."""

    homepage = "https://pypi.org/project/tensorboard-plugin-wit/"
    url      = "https://github.com/PAIR-code/what-if-tool/archive/v1.7.0.tar.gz"
    git      = "https://github.com/pair-code/what-if-tool.git"

    maintainers = ['aweits']

    version('master', branch='master')
    version('1.8.0', sha256='2a80d1c551d741e99b2f197bb915d8a133e24adb8da1732b840041860f91183a', expand=False,
            url='https://files.pythonhosted.org/packages/1a/c1/499e600ba0c618b451cd9c425ae1c177249940a2086316552fee7d86c954/tensorboard_plugin_wit-1.8.0-py3-none-any.whl',
            )

    depends_on('python@2.7:2.8,3.2:', type=('build', 'run'))
    depends_on('py-wheel', type='build')
    depends_on('py-pip', type='build')

    extends('python')

    # copied from py-azureml-core
    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', '--no-deps', self.stage.archive_file, '--prefix={0}'.format(prefix))
