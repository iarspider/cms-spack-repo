# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyTensorboard(Package):
    """TensorBoard is a suite of web applications for
    inspecting and understanding your TensorFlow runs and
    graphs."""

    homepage = "https://github.com/tensorflow/tensorboard"
    url      = "https://pypi.io/packages/py3/t/tensorboard/tensorboard-2.6.0-py3-none-any.whl"

    maintainers = ['aweits']

    version('2.6.0', expand=False,
            sha256='f7dac4cdfb52d14c9e3f74585ce2aaf8e6203620a864e51faf84988b09f7bbdb')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@41.0.0:', type=('build', 'run'))
    depends_on('py-absl-py@0.4:', type=('build', 'run'))
    depends_on('py-grpcio@1.24.3:', type=('build', 'run'))
    depends_on('py-google-auth@1.6.3:1', type=('build', 'run'), when='@2.6.0:')
    depends_on('py-google-auth-oauthlib@0.4.1:0.4', type=('build', 'run'))
    depends_on('py-markdown@2.6.8:', type=('build', 'run'))
    depends_on('py-numpy@1.12.0:', type=('build', 'run'))
    depends_on('py-protobuf@3.6.0:', type=('build', 'run'))
    depends_on('py-requests@2.21.0:2', type=('build', 'run'))
    depends_on('py-setuptools@41.0.0:', type=('build', 'run'))
    depends_on('py-tensorboard-dataserver@0.6.0:0.6', type=('build', 'run'))
    depends_on('py-tensorboard-plugin-wit@1.6.0:', type=('build', 'run'))
    depends_on('py-werkzeug@0.11.15:', type=('build', 'run'))
    depends_on('py-wheel@0.26:', type='build')
    depends_on('py-pip', type='build')

    extends('python')

    # copied from py-azureml-core
    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', '--no-deps', self.stage.archive_file, '--prefix={0}'.format(prefix))
