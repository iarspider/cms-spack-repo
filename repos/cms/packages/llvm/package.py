import glob
from os.path import dirname, join

from spack import *
from spack.pkg.builtin.llvm import Llvm as BuiltinLlvm


class Llvm(BuiltinLlvm):
    __doc__ = BuiltinLlvm.__doc__

    git = "https://github.com/cms-externals/llvm-project.git"

    version("12.0.1.cms", commit="9f4ab770e61b68d2037cc7cda1f868a8ba52da85")

    @BuiltinLlvm.libs.getter
    def libs(self):
        return LibraryList([])

    def setup_run_environment(self, env):
        super().setup_run_environment(env)
        env.prepend_path('PYTHONPATH', python_platlib.replace('/lib/', '/lib64/'))
        env.prepend_path('PYTHON3PATH', python_platlib.replace('/lib/', '/lib64/'))

    def cmake_args(self):
        args = super().cmake_args()
        args.append(self.define("LLVM_LIBDIR_SUFFIX", "64"))
        args.append(self.define("LLVM_ENABLE_PIC", True))

        compiler = Executable(self.compiler.cc)
        llvm_triple = compiler("-dumpmachine", output=str, error=str).strip()
        args.append(self.define("LLVM_HOST_TRIPLE", llvm_triple))
        args = [x for x in args if "LLVM_REQUIRES_RTTI" not in x]
        return args

    @run_after('install')
    def post_inst(self):
        BINDINGS_PATH = python_platlib.replace('/lib/', '/lib64/')
        PYTHONVERSION = self.spec['python'].version.up_to(2)

        mkdirp(BINDINGS_PATH)
        install_tree("clang/bindings/python/clang", join_path(BINDINGS_PATH, 'clang'))
        # symlink(python_platlib, BINDINGS_PATH)
        with open(join_path(python_platlib, 'clang-{0}-py{1}.egg-info'.format(self.spec.version, PYTHONVERSION)), 'w') as f:
            f.write('Metadata-Version: 1.1\nName: clang\nVersion: ' + str(self.spec.version))

        for fn in glob.glob(join_path(self.build_directory, 'clang', 'tools', 'scan-build', 'set-xcode*')):
            force_remove(fn)
