# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import shutil
import glob


class Madgraph5amc(Package):
    """MadGraph5_aMC@NLO is a framework that aims at providing
       all the elements necessary for SM and BSM phenomenology,
       such as the computations of cross sections, the generation
       of hard events and their matching with event generators,
       and the use of a variety of tools relevant to
       event manipulation and analysis. """

    homepage = "https://launchpad.net/mg5amcnlo"
    url      = "https://launchpad.net/mg5amcnlo/2.0/2.7.x/+download/MG5_aMC_v2.7.3.tar.gz"

    tags = ['hep']

    version('2.8.1', sha256='acda34414beba201e529b8c03f87f4893fb3f99ed2956a131d60a387e76c5b8c',
            url="https://launchpad.net/mg5amcnlo/2.0/2.8.x/+download/MG5_aMC_v2.8.1.tar.gz")
    version('2.8.0', sha256='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            url="https://launchpad.net/mg5amcnlo/2.0/2.8.x/+download/MG5_aMC_v2.8.0.tar.gz")
    version('2.7.3.py3', sha256='400c26f9b15b07baaad9bd62091ceea785c2d3a59618fdc27cad213816bc7225')
    version('2.7.3.py2', sha256='0b665356f4d9359e6e382e0f408dc11db594734567c6b2f0ec0e0697f2dbe099',
            url="https://launchpad.net/mg5amcnlo/2.0/2.7.x/+download/MG5_aMC_v2.7.3.tar.gz")

    variant('atlas', default=False, description='Apply changes requested by ' +
            "the ATLAS experimenent on LHC")
    variant('ninja', default=False, description='Use external installation' +
            " of Ninja")
    variant('collier', default=False, description='Use external installation' +
            ' of Collier')
    variant('golem', default=False, description='Use external installation' +
            ' of Golem')
    variant('syscalc', default=True, description='Use external installation' +
            'of SysCalc')
    variant('cms', default=False, description='Apply changes requested by ' +
            'the CMS experimenent on LHC')
    variant('nb_core', default=0, description='Number of cores to use. Default (0) ' +
            ' - use all available cores')
    variant('thepeg', default=False)
    variant('root', default=False)

    conflicts('%gcc@10:', when='@2.7.3 ~cms')

    depends_on('syscalc', when='+syscalc')
    depends_on('gosam-contrib', when='+ninja')
    depends_on('gosam-contrib', when='+golem')
    depends_on('collier', when='+collier')
    depends_on('lhapdf')
    depends_on('fastjet')
    depends_on('py-six', when='@2.7.3.py3,2.8.0:', type=('build', 'run'))
    depends_on('hepmc', when='+thepeg')
    depends_on('root', when='+root')
    depends_on('thepeg', when='+thepeg')

    depends_on('python@2.7.0:2.8.0', when='@2.7.3.py2', type=('build', 'run'))
    depends_on('python@3.7:', when='@2.7.3.py3', type=('build', 'run'))
    depends_on('python@2.7.0:2.8.0,3.7:', when='@2.8.0:', type=('build', 'run'))

    patch('madgraph5amc.patch', level=0)
    patch('madgraph5amc-2.7.3.atlas.patch', level=0, when='@2.7.3.py2+atlas')
    patch('madgraph5amc-2.7.3.atlas.patch', level=0, when='@2.7.3.py3+atlas')
    patch('madgraph5amc-2.8.0.atlas.patch', level=0, when='@2.8.0+atlas')
    patch('madgraph5amc-2.8.0.atlas.patch', level=0, when='@2.8.1+atlas')

    patch('madgraph5amcatnlo-py39.patch', level=1, when='@2.7.3.py3 ^python@3.9:')

    phases = ['edit', 'build', 'install']

    def edit(self, spec, prefix):
        def set_parameter(name, value):
            config_files.filter('^#?[ ]*' + name + '[ ]*=.*$',
                                name + ' = ' + value,
                                ignore_absent=True)

        config_files = FileFilter(join_path("input",
                                            ".mg5_configuration_default.txt"),
                                  join_path("input", "mg5_configuration.txt"))

        set_parameter('fortran_compiler', self.compiler.fc)
        set_parameter('cpp_compiler', self.compiler.cxx)
        set_parameter('timeout', "0")
        set_parameter('autoupdate', "0")
        set_parameter('automatic_html_opening', 'False')
        set_parameter('notification_center', 'False')
        set_parameter('output_dependencies', 'internal')

        if '+syscalc' in self.spec:
            set_parameter('syscalc_path', spec['syscalc'].prefix.bin)

        if '+ninja' in spec:
            set_parameter('ninja', spec['gosam-contrib'].prefix)
        else:
            set_parameter('ninja', spec.prefix.HEPTools.lib)

        if '+collier' in spec:
            set_parameter('collier', spec['collier'].prefix.lib)
        else:
            set_parameter('collier', spec.prefix.HEPTools.lib)

        if '+golem' in spec:
            set_parameter('golem', spec['gosam-contrib'].prefix)

        set_parameter('output_dependencies', 'internal')
        set_parameter('fastjet', join_path(spec['fastjet'].prefix.bin,
                                           'fastjet-config'))


        if '+pythia8' in spec:
            set_parameter('pythia8_path', spec['pythia8'].prefix)
            set_parameter('mg5amc_py8_interface_path', spec.prefix.HEPTools.MG5aMC_PY8_interface)

        if '+thepeg' in spec:
            set_parameter('thepeg_path', spec['thepeg'].prefix)
            set_parameter('hepmc_path', spec['hepmc'].prefix)

        if '+lhapdf' in spec:
            set_parameter('lhapdf_py2', join_path(spec['lhapdf'].prefix.bin, 'lhapdf-config'))
            set_parameter('lhapdf_py3', join_path(spec['lhapdf'].prefix.bin, 'lhapdf-config'))

        if '+cms' in spec:
            set_parameter('run_mode', "1")
            set_parameter('cluster_type', 'lsf')
            set_parameter('cluster_queue', '1nh')
            set_parameter('cluster_size', "150")
            set_parameter('pjfry', 'None')

        filter_file("SHFLAG = -fPIC", "SHFLAG = -fPIC -fcommon", join_path(self.stage.source_path, 'vendor/StdHEP/src/stdhep_arch'))

    def build(self, spec, prefix):
        if '+atlas' in spec:
            if os.path.exists(join_path('bin', 'compile.py')):
                compile_py = Executable(join_path('bin', 'compile.py'))
            else:
                compile_py = Executable(join_path('bin', '.compile.py'))

            compile_py()

        if '~cms' in spec:
            with working_dir(join_path('vendor', 'CutTools')):
                make(parallel=False)

            with working_dir(join_path('vendor', 'StdHEP')):
                make(parallel=False)

            shutil.copy('input/mg5_configuration.txt', 'input/mg5_configuration_patched.txt')
            # compile_py = Executable(join_path('bin', 'compile.py'))
            py = which('python')
            py(join_path('bin', 'compile.py'))
            # compile_py()
            os.remove(join_path('bin', 'compile.py'))
            shutil.move('input/mg5_configuration_patched.txt', 'input/mg5_configuration.txt')

    @when('+cms')
    def install(self, spec, prefix):
        for fn in glob.glob(join_path(prefix, '**', '*.tgz')):
            os.remove(fn)

        install_tree('.', prefix)

    @when('~cms')
    def install(self, spec, prefix):
        def installdir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        def installfile(filename):
            install(filename, join_path(prefix, filename))

        for p in os.listdir(self.stage.source_path):
            if os.path.isdir(p):
                installdir(p)
            else:
                if p != 'doc.tgz':
                    installfile(p)
                else:
                    mkdirp(prefix.share)
                    install(p, join_path(prefix.share, p))

        install(join_path('Template', 'LO', 'Source', '.make_opts'),
                join_path(prefix, 'Template', 'LO',
                          'Source', 'make_opts'))

    @run_after('install')
    def generate_nlo(self):
        if self.spec.satisfies('~cms'):
            return

        with open(join_path(self.prefix, 'basiceventgeneration.txt'), 'w') as f:
            print("generate p p > t t~ [QCD]", file=f)
            print("output basiceventgeneration", file=f)
            print("launch", file=f)
            print("set nevents 5", file=f)

        mg5 = Executable(join_path(self.prefix.bin, 'mg5_aMC'))
        mg5(join_path(self.prefix, 'basiceventgeneration.txt'))
        os.remove(join_path(self.prefix, 'basiceventgeneration.txt'))
