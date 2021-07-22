# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class TensorflowSources(Package):
    """Prepare Tensorflow sources"""

    homepage = "https://github.com/cms-externals/tensorflow"
    git      = "https://github.com/cms-externals/tensorflow.git"

    version('2.4.1', branch='2.4.1')

    depends_on('bazel', type='build')
    depends_on('java', type='build')
    
    variant('build_type', default='opt')
    variant('pythonOnly', default=False)
    variant('vectorize_flag', default='-msse3')
    
    def install(self, spec, prefix):
Requires: python3 py3-numpy py3-mock py3-wheel py3-typing py3-typing_extensions
Requires: py3-keras-applications py3-keras-preprocessing py3-future py3-wrapt py3-gast py3-setuptools
Requires: py3-cython py3-googlePackages py3-astor py3-six py3-termcolor py3-absl-py
Requires: py3-opt-einsum py3-flatbuffers
Requires: eigen protobuf zlib libpng libjpeg-turbo curl pcre giflib sqlite grpc flatbuffers 
