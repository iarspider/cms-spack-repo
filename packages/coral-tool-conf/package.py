from spack import *
import re
import os
import shutil
from glob import glob
import fnmatch


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

    def install(self, spec, prefix):
        get_tools_path = join_path(os.path.dirname(__file__), '..', 'ToolfilePackage', 'bin', 'get_tools')
        set_executable(get_tools_path)
        get_tools = Executable(get_tools_path)

        with working_dir(prefix, create=True):
            mkdirp('tools/selected')
            mkdirp('tools/available')
            for dep_name, dep in self.get_all_deps(spec).items():
                uctool = dep_name.upper().replace('-', '_')
                toolbase = dep['prefix']
                toolver = dep['version']

                print(f"get_tools({toolbase}, {toolver}, {self.prefix}, {dep_name})", file=self.logfile)

                get_tools(toolbase, toolver, self.prefix, dep_name)

        get_tools("", "system", self.prefix, "systemtools")
        # TODO: vectorization

        for tool in [x.lower() for x in self.skipreqtools]:
            if os.path.isfile(join_path(prefix, "tools", "selected", x+'.xml')):
                shutil.move(join_path(prefix, "tools", "selected", x+'.xml'), join_path(prefix, "tools", "available", x+'.xml'))

        if os.path.exists(join_path(self.spec['scramv1'].prefix.bin, 'chktool')):
