# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import shutil
import fnmatch


class Openloops(Package):
    """The OpenLoops 2 program is a fully automated implementation of the
       Open Loops algorithm combined with on-the-fly reduction methods,
       which allows for the fast and stable numerical evaluation of tree
       and one-loop matrix elements for any Standard Model process
       at NLO QCD and NLO EW. """

    homepage = "https://openloops.hepforge.org/"
    git      = "https://github.com/cms-externals/openloops.git"

    tags = ['hep']

    version('2.1.2', sha256='f52575cae3d70b6b51a5d423e9cd0e076ed5961afcc015eec00987e64529a6ae')

    variant('compile_extra', default=False,
            description='Compile real radiation tree amplitudes')

    depends_on('python', type=("build", "run"))

    # NOTICE: update this line when openloops updates
    depends_on('openloops-process@2.1.2', when='@2.1.2')

    phases = ['configure', 'build', 'build_processes', 'install']

    def configure(self, spec, prefix):
        spack_env = ('PATH LD_LIBRARY_PATH CPATH C_INCLUDE_PATH' +
                     'CPLUS_INCLUDE_PATH INTEL_LICENSE_FILE').split()
        for k in env.keys():
            if k.startswith('SPACK_'):
                spack_env.append(k)

        spack_env = ' '.join(spack_env)
        is_intel = self.spec.satisfies('%intel')
        njobs = self.spec.variants['num_jobs'].value

        with open('openloops.cfg', 'w') as f:
            f.write('[OpenLoops]\n')
            f.write('import_env={0}\n'.format(spack_env))
            f.write('num_jobs = {0}\n'.format(njobs))
            f.write('process_lib_dir = {0}\n'.format(self.spec.prefix.proclib))
            f.write('cc = {0}\n'.format(env['SPACK_CC']))
            f.write('cxx = {0}\n'.format(env['SPACK_CXX']))
            f.write('fortran_compiler = {0}\n'.format(env['SPACK_FC']))
            f.write('gfortran_f_flags = -ffree-line-length-none ' +
                    '-fdollar-ok ')
            if self.spec.satisfies('%gcc@10:'):
                f.write('-fallow-invalid-boz ')
            if self.spec.target.family == 'aarch64':
                f.write('-mcmodel=small\n')
            else:
                f.write('-mcmodel=medium\n')

            f.write('generic_optimisation = -O2')
            f.write('born_optimisation = -O2')
            f.write('loop_optimisation = -O0')
            f.write('link_optimisation = -O2')
            f.write('process_download_script = download_dummy.py')

            copy(join_path(os.path.dirname(__file__), 'cms.coll'), 'cms.coll')

        copy(join_path(os.path.dirname(__file__), 'download_dummy.py'), 'download_dummy.py')

    def build(self, spec, prefix):
        ol = Executable('./openloops')
        ol('update', '--processes', 'generator=0')

    def build_processes(self, spec, prefix):
        if os.path.exists('process_src'):
            shutil.rmtree('process_src')
            
        
        copy(self.spec['openloops'].prefix.process_src, 'process_src')
        copy(self.spec['openloops'].prefix.proclib, 'proclib')
        copy(join_path(self.spec['openloops'].prefix, 'cms.coll'), '.')

        ol = Executable('./openloops')
        processes = self.spec.variants['processes'].value
        if '+compile_extra' in self.spec:
            ce = 'compile_extra=1'
        else:
            ce = ''

        ol('libinstall', ce, 'cms.coll')

    def install(self, spec, prefix):
        install_tree('lib', self.prefix)
        mkdirp(self.prefix.proclib)
        for file in os.listdir('proclib'):
            if fnmatch.fnmatch(file, '*.info') or fnmatch.fnmatch(file, '*.so'):
                install(join_path('proclib', file), self.prefix.proclib)