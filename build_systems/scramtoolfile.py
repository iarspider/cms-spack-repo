from collections import defaultdict, Counter
from llnl.util.filesystem import *

from spack.package import BundlePackage
from spack.build_systems.cuda import CudaPackage
from spack.directives import resource, version, depends_on
from spack.util.executable import which, Executable
import spack.user_environment as uenv
from spack.util.environment import *

import glob
import os
import re
import shutil

class ScramToolfilePackage(BundlePackage):
    build_system_class = 'ScramToolfilePackage'
    phases = ['install']

    depends_on('cmsdist', type='build')
    depends_on('scram', type='build')

    # key: spack, value: scram
    aliases = {'python': 'python3', 'bzip2': 'bz2lib', 'scram': 'SCRAMV1', 'oracle-instant-client': 'oracle',
               'util-linux-uuid': 'libuuid', 'frontier-client': 'frontier_client', 'das-client': 'das_client',
               'frontier-client': 'frontier_client', 'py-onnx-runtime': 'onnxruntime', 'fftw': 'fftw3',
               'professor': 'professor2', 'fjcontrib': 'fastjet-contrib', 'opencl-clhpp': 'opencl-cpp',
               'gosam-contrib': 'gosamcontrib', 'py-gosam': 'gosam', 'madgraph5amc': 'madgraph5amcatnlo',
               'oracle-instant-client': 'oracle', 'berkeley-db': 'db6', 'benchmark': 'google-benchmark',
               'herwig6': 'herwig', 'herwig3': 'herwig7', 'csctrackfinderemulation': 'CSCTrackFinderEmulation',
               'nlohmann-json': 'json', 'openblas': 'OpenBLAS', 'python-tools': 'python_tools', 'tauola': 'tauolapp',
               'tauola-f': 'tauola', 'intel-tbb': 'tbb', 'py-tensorflow': 'tensorflow', 'photos-f': 'photos',
               'photos': 'photospp'}

    def get_all_deps(self, spec):
        res = {}
        for dep in spec.dependencies():
            if res.get(dep.name, None) is None:
                res[dep.name] = {'prefix': dep.prefix, 'version': str(dep.version)}
                res.update(self.get_all_deps(dep))

        return res

    # Code to collect environment modifications taken from SetupScriptPackage by V. Volkl
    # https://gitlab.cern.ch/sft/sft-spack-repo/-/blob/master/packages/SetupScriptPackage/package.py
    def get_pythonpath(self, spec):
        with spack.store.db.read_transaction():
            specs = [dep for dep in spec.traverse(order='post')]

        env_mod = spack.util.environment.EnvironmentModifications()

        for _spec in specs:
            env_mod.extend(uenv.environment_modifications_for_spec(_spec))
            env_mod.prepend_path(uenv.spack_loaded_hashes_var, _spec.dag_hash())

        modifications = env_mod.group_by_name()
        new_env = {}

        pythonpath_mod = modifications['PYTHONPATH']
        for x in pythonpath_mod:
            x.execute(new_env)

        path_list = new_env.get('PYTHONPATH', '').split(":")
        pruned_path_list = prune_duplicate_paths(path_list)

        return pruned_path_list

    @property
    def site_packages_dir(self):
        return join_path('lib', 'python{0}'.format(self.spec['python'].version.up_to(2)))

    ## INCLUDE scram-tools.file/tool-env
    def setup_build_environment(self, env):
        env.set('ROOT_CXXMODULES', 0)
        # TODO: vectorization
        # compilation_flags.file
        if self.spec.satisfies('target=x86_64:'):
            env.set('COMPILER_CXXFLAGS', '-msse3')
        elif self.spec.satisfies('target=aarch64:'):
            env.set('COMPILER_CXXFLAGS', '-mtarget=armv8-a -mno-outline-atomics')
        elif self.spec.satisfies('target=ppc64le:'):
            env.set('COMPILER_CXXFLAGS', '-mcpu=power8 -mtune=power8 --param=l1-cache-size=64 --param=l1-cache-line-size=128 --param=l2-cache-size=512')

        env.set('ORACLE_ENV_ROOT', '')

        # TODO: remember, the list is different for arm vs. everything else
        if 'cuda' in self.spec:
            env.set('CUDA_FLAGS', ' '.join("'" + x + "'" for x in CudaPackage.cuda_flags(self.spec.variants['cuda_arch'].value)))
            env.set('CUDA_HOST_CXXFLAGS', CudaPackage.nvcc_stdcxx)

        # Technical variables
        env.set('SCRAMV1_ROOT', self.spec['scram'].prefix)

        python_dir = 'python{0}'.format(self.spec['python'].version.up_to(2))
        env.set('PYTHON3_LIB_SITE_PACKAGES', os.path.join('lib', python_dir, 'site-packages'))
        if self.spec.satisfies('%gcc'):
            env.set('GCC_ROOT', os.path.dirname(os.path.dirname(self.compiler.cc)))
            env.set('GCC_VERSION', str(self.compiler.real_version))

    ## INCLUDE scram-tool-conf
    def install(self, spec, prefix):
        mkdirp(prefix.tools.selected)
        mkdirp(prefix.tools.available)

        get_tools_path = join_path(spec['cmsdist'].prefix, 'scram-tools.file', 'bin', 'get_tools')
        set_executable(get_tools_path)
        get_tools = Executable(get_tools_path)
        all_deps = self.get_all_deps(spec)

        for dep_name, dep in all_deps.items():
            uctool = dep_name.upper().replace('-', '_')
            toolbase = dep['prefix']
            toolver = dep['version']
            old_dep_name = dep_name
            dep_name = self.aliases.get(dep_name, dep_name)
            if dep_name.startswith('py-'):
                dep_name = dep_name.replace('py-', 'py3-')
            tty.debug(f'SPACK {old_dep_name} -> SCRAM {dep_name}')
            get_tools(toolbase, toolver, prefix, dep_name)

        gcc_dir = os.path.dirname(os.path.dirname(self.compiler.cc))
        get_tools(gcc_dir, str(self.compiler.real_version), prefix, 'gcc')
        get_tools("", "system", prefix, "systemtools")

        # TODO: vectorization
        for tool in self.skipreqtools:
            if os.path.exists(join_path(prefix.tools.selected, tool + '.xml')):
                shutil.move(join_path(prefix.tools.selected, tool + '.xml'),
                            join_path(prefix.tools.available, tool + '.xml'))

        if os.path.exists(spec['scram'].prefix.bin.chktool):
            chktool = Executable(spec['scram'].prefix.bin.chktool)
            out = chktool(*find(prefix.tools, '*.xml'), output=str, error=str, fail_on_error=False)
            if 'ERROR:' in out:
                raise InstallError('chktool found errors\n'+out)

        ALL_PY_BIN = set()
        ALL_PY_PKGS = set()
        DUP_BIN = defaultdict(list)

        pythonpath = self.get_pythonpath(spec)
        mkdirp(join_path(prefix, self.site_packages_dir, 'site-packages'))
        with open(join_path(prefix, self.site_packages_dir, 'site-packages', 'tool-deps.pth'), 'w') as f:
            for pkg in pythonpath:
                f.write(pkg + '\n')

        with open(join_path(prefix.tools.selected, 'python-paths.xml'), 'a') as f:
            f.write('<tool name="python-paths" version="1.0">\n')
            f.write('  <runtime name="PYTHON3PATH"  value="' + join_path(prefix, self.site_packages_dir, 'site-packages')  + '" type="path"/>\n')
            f.write('</tool>\n')


        all_py_bin = []
        all_py_binpkg = defaultdict(list)
        for dep_name, dep in all_deps.items():
            if not dep_name.startswith("py-"):
                continue

            dep_version = dep['version']
            dep_name = dep_name.replace('py-', 'py3-')
            dep_name = self.aliases.get(dep_name, dep_name)

            if os.path.isfile(join_path(prefix.tools.selected, dep_name + '.xml')):
                continue

            uctool = dep_name.upper().replace('-', '_')
            with open(join_path(prefix.tools.selected, dep_name + '.xml'), 'w') as f:
                f.write(f"<tool name=\"{dep_name}\" version=\"{dep_version}\">\n")
                if os.path.exists(join_path(dep['prefix'], 'bin')):
                    for b in os.listdir(join_path(dep['prefix'], 'bin')):
                        if b == '__pycache__':
                            continue

                        all_py_bin += [b]
                        all_py_binpkg[b] += [dep_name]

                    f.write("  <client>\n")
                    f.write(f"    <environment name=\"${uctool}_BASE\" default=\"{dep['prefix']}\"/>\n")
                    f.write("  </client>\n")
                    f.write(f"  <runtime name=\"PATH\" value=\"${uctool}_BASE/bin\" type=\"path\"/>\n")
                f.write("</tool>\n")

        DUP_BIN = Counter(all_py_bin)
        msg = []
        for bin_, cnt in DUP_BIN.items():
            if cnt > 1:
                prov = ', '.join(all_py_binpkg[bin_])
                msg.append(f"{bin_}: {prov}")

        if msg:
            raise InstallError("Duplicate python binaries found. Please cleanup and make sure only one binary is available.\n" + '\n'.join(msg))
