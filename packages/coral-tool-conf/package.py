from spack import *

import fnmatch
import os
import re
import shutil
import spack.user_environment as uenv

from glob import glob
from collections import Counter, defaultdict
from  spack.util.environment import *


class CoralToolConf(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../ToolfilePackage/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)

    depends_on('pcre')
    depends_on('python')
    depends_on('expat')
    depends_on('boost')
    depends_on('frontier-client')
    depends_on('sqlite')
    depends_on('util-linux-uuid')
    depends_on('zlib')
    depends_on('bzip2')
    depends_on('xerces-c')
    depends_on('oracle-instant-client', when='arch=amd64')

    depends_on('scramv1', type='build')

    skipreqtools = ['jcompiler']

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

        path_list = new_env['PYTHONPATH'].split(":")
        pruned_path_list = prune_duplicate_paths(path_list)

        return pruned_path_list

    @property
    def site_packages_dir(self):
        return join_path('lib', 'python{0}'.format(self.spec['python'].version.up_to(2)), 'site-packages')

    def setup_build_environment(self, env):
        env.set('SCRAMV1_ROOT', self.spec['scramv1'].prefix)

    def install(self, spec, prefix):
        get_tools_path = join_path(os.path.dirname(__file__), '..', 'ToolfilePackage', 'bin', 'get_tools')
        set_executable(get_tools_path)
        get_tools = Executable(get_tools_path)
        all_deps = self.get_all_deps(spec)

        with working_dir(prefix, create=True):
            mkdirp('tools/selected')
            mkdirp('tools/available')
            for dep_name, dep in all_deps.items():
                uctool = dep_name.upper().replace('-', '_')
                toolbase = dep['prefix']
                toolver = dep['version']

                print(f"get_tools({toolbase}, {toolver}, {self.prefix}, {dep_name})", file=self.logfile)

                get_tools(toolbase, toolver, prefix, dep_name)

        get_tools("", "system", self.prefix, "systemtools")
        # TODO: vectorization

        for tool in [x.lower() for x in self.skipreqtools]:
            if os.path.isfile(join_path(prefix, "tools", "selected", x+'.xml')):
                shutil.move(join_path(prefix, "tools", "selected", x+'.xml'), join_path(prefix, "tools", "available", x+'.xml'))

        if os.path.exists(join_path(self.spec['scramv1'].prefix.bin, 'chktool')):
            bash = which('bash')
            bash(join_path(os.path.dirname(__file__), 'run_chktool.sh'), prefix)

        pythonpath = self.get_pythonpath(spec)
        mkdirp(join_path(prefix, self.site_packages_dir, 'site-packages'))
        with open(join_path(prefix, self.site_packages_dir, 'site-packages', 'tool-deps.pth'), 'w') as f:
            for pkg in pythonpath:
                f.write(pkg + '\n')

        with open(join_path(prefix.tools.selected, 'python-paths.xml'), 'a') as f:
            f.write('  <runtime name="PYTHON3PATH"  value="' + join_path(prefix, self.site_packages_dir, 'site-packages')  + '" type="path"/>\n')
            f.write('</tool>\n')

        all_py_bin = []
        all_py_binpkg = defaultdict(list)
        for dep_name, dep in all_deps.items():
            if not dep_name.startswith("py-"):
                continue

            pk_name = dep_name.upper()

            if os.path.isfile(join_path(prefix.tools.selected, pkname + '.xml')):
                continue

            uctool = pkname.replace('-', '_')
            with open(join_path(prefix.tools.selected, pkname + '.xml'), 'w') as f:
                f.write(f"<tool name=\"{pk_name}\" version=\"{dep['version']}\">\n")
                if os.path.exists(join_path(dep['prefix'], 'bin')):
                    for b in os.listdir(join_path(dep['prefix'], 'bin')):
                        if b == '__pycache__':
                            continue

                        all_py_bin += [b]
                        all_py_binpkg[b] += [pk_name]

                    f.write("  <client>\n")
                    f.write(f"    <environment name=\"${uctool}_BASE\" default=\"{dep['prefix']}\"/>\n")
                    f.write("  </client>\n")
                    f.write(f"  <runtime name=\"PATH\" value=\"${uctool}_BASE/bin\" type=\"path\"/>\n")
                f.write("</tool>\n")

            DUP_BIN = Counter(all_py_bin)
            msg = []
            for bin, cnt in DUP_BIN.items():
                if cnt > 1:
                    prov = ', '.join(all_py_binpkg[bin])
                    msg.append(f"{bin}: {prov}")
                    
            if msg:
                raise InstallError("Duplicate python binaries found. Please cleanup and make sure only one binary is available.\n" + '\n'.join(msg))