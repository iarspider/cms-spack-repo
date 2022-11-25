from spack import *

import fnmatch
import os
import re
import shutil
import spack.user_environment as uenv

from glob import glob
from collections import Counter, defaultdict
from  spack.util.environment import *


class CoralToolConf(ScramToolfilePackage, CudaPackage):
    """SCRAM toolfile for CORAL"""

    homepage = "https://github.com/cms-sw/cmsdist"
    version('10.0')

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
    depends_on('oracle-instant-client', when='target=x86_64:')

    depends_on('scram', type='build')

    skipreqtools = ['jcompiler']
