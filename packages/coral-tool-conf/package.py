from spack import *
import re
import os
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

    def install(self, spec, prefix):
        logfile = open('/build/razumov/cms-spack-repo/spack/tool.log', 'w')
        try:
            get_tools_path = join_path(os.path.dirname(__file__), '..', 'ToolfilePackage', 'bin', 'get_tools')
            set_executable(get_tools_path)
            get_tools = Executable(get_tools_path)
            
            with working_dir(prefix, create=True):
                mkdirp('tools/selected')
                mkdirp('tools/available')
                for dep in spec.dependencies():
                    uctool = dep.name.upper().replace('-', '_')
                    toolbase = dep.prefix
                    toolver = dep.version
                    
                    print(f"get_tools({toolbase}, {toolver}, {self.prefix}, {dep.name})", file=logfile)
                    
                    get_tools(toolbase, toolver, self.prefix, dep.name)

            get_tools("", "system", self.prefix, "systemtools")
            # TODO: vectorization
        except Exception as e:
            logfile.close()
            raise e
