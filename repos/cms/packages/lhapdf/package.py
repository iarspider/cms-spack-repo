# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Lhapdf(AutotoolsPackage):
    """LHAPDF is a general purpose C++ interpolator,
       used for evaluating PDFs from discretised data files. """

    homepage = "https://lhapdf.hepforge.org/"
    url      = "https://lhapdf.hepforge.org/downloads/?f=LHAPDF-6.2.3.tar.gz"

    tags = ['hep']

    setsversion = '6.4.0e'

    version('6.4.0', sha256='7d2f0267e2d65b0ddee048553b342d7c893a6dbabe1e326cad62de0010dd810c')
    version('6.3.0', sha256='ed4d8772b7e6be26d1a7682a13c87338d67821847aa1640d78d67d2cef8b9b5d')
    version('6.2.3', sha256='d6e63addc56c57b6286dc43ffc56d901516f4779a93a0f1547e14b32cfd82dd1')

    resource(
       name='MSTW2008nlo68cl',
       url='https://lhapdfsets.web.cern.ch/current/MSTW2008nlo68cl.tar.gz',
       destination='',
       placement='MSTW2008nlo68cl',
       sha256='98ec0541e80e223785bb6029ebf81e93ca5111da41d6565b3b5c4aa86d59bb5d'
    )

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('python',        type=('build', 'run'))
    depends_on('py-cython',     type='build')
    depends_on('py-setuptools', type='build')

    depends_on('tar', type='build')
    depends_on('zlib', type='build')

    extends('python')
    keep_archives = True

    def configure_args(self):
        args = ['FCFLAGS=-O3', 'CFLAGS=-O3', 'CXXFLAGS=-O3', '--enable-python']
        return args

    @run_after('install')
    def install_pdfsets(self):
        # mkdir -p %{i}/share/LHAPDF
        # cd %{i}/share/LHAPDF
        # cp %{_sourcedir}/MSTW2008nlo68cl.tar.gz .
        # tar xvfz MSTW2008nlo68cl.tar.gz
        # rm -f MSTW2008nlo68cl.tar.gz
        # chmod a+x %{_sourcedir}/lhapdf_makeLinks
        # %{_sourcedir}/lhapdf_makeLinks %{setsversion}
        # rm -f pdfsets.index
        # cp -f %{_sourcedir}/lhapdf_pdfsetsindex pdfsets.index
        # cd -
        with working_dir(self.prefix.share.LHAPDF, create=True):
            res_path = join_path(self.stage.source_path, 'MSTW2008nlo68cl')
            install_tree(res_path, '.')

            code_dir = os.path.dirname(__file__)
            set_executable(join_path(code_dir, 'lhapdf_makeLinks.sh'))
            makeLinks = Executable(join_path(code_dir, 'lhapdf_makeLinks.sh'))
            makeLinks(self.setsversion)

            os.remove('pdfsets.index')

#        f1 = open(join_path(code_dir, 'pdfsets.index'), 'rb')
#        f1.close()
#        f2 = open(join_path(self.prefix.share.LHAPDF, 'pdfsets.index'), 'wb')
#        f2.close()
#        os.remove(join_path(self.prefix.share.LHAPDF, 'pdfsets.index'))
#        sleep(1)
        install(join_path(code_dir, 'pdfsets.index'), self.prefix.share.LHAPDF)
