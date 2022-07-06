from spack import *
from spack.pkg.builtin.dd4hep import Dd4hep as BuiltinDd4hep


class Dd4hep(BuiltinDd4hep):
    __doc__ = BuiltinDd4hep.__doc__

    keep_archives = True
    cms_stage = 1

    version('1.19x', commit='cc335b34e9eb2825ab18e20c531be813a92d141f')

    def flag_handler(self, name, flags):
        if name == 'cxxflags':
            flags.append('-fPIC')
        return (None, None, flags)

    # -- CMS: build static version of DDG4
    @run_after('install')
    def install_static(self):
        spec = self.spec
        prefix = self.spec.prefix
        self.cms_stage = 2
        self.spec.variants['shared'].value = False
        self.spec.variants['geant4'].value = True

        # cmake stage: Runs ``cmake`` in the build directory
        options = self.std_cmake_args
        options += self.cmake_args()
        options.append(os.path.abspath(self.root_cmakelists_dir))
        with working_dir(self.build_directory, create=True):
            inspect.getmodule(self).cmake(*options)

        # build stage: Make the build targets
        with working_dir(self.build_directory):
            if self.generator == 'Unix Makefiles':
                inspect.getmodule(self).make(*self.build_targets)
            elif self.generator == 'Ninja':
                self.build_targets.append("-v")
                inspect.getmodule(self).ninja(*self.build_targets)

        # custom install stage
        for fn in glob.glob(join_path(self.build_directory, 'lib', 'libDDG4*.a')):
            libname = os.path.basename(fn)
            install(fn, join_path(prefix, 'lib', libname[:-2] + '-static.a'))

        install_tree(join_path(self.stage.source_path, 'DDG4', 'include', 'DDG4'), prefix.include.DDG4)

    @property
    def build_dirname(self):
        """Returns the directory name to use when building the package
        :return: name of the subdirectory for building the package
        """
        return 'spack-build-%s' % self.spec.dag_hash(7) + '-cms' + str(self.cms_stage)
