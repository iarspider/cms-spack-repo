import os

from spack import *
from spack.pkg.builtin.jemalloc import Jemalloc as BuiltinJemalloc


class Jemalloc(BuiltinJemalloc):
    __doc__ = BuiltinJemalloc.__doc__
    git = "https://github.com/cms-externals/jemalloc.git"
    version('5.2.1.cms', commit="de1caefb587217f0b519eb425d7a9b3570e5ba28")

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')

    @property
    def configure_abs_path(self):
        # Absolute path to configure
        configure_abs_path = os.path.join(
            os.path.abspath(self.configure_directory), 'autogen.sh'
        )
        return configure_abs_path

    def autoreconf(self, spec, prefix):
        return

    def configure(self, spec, prefix):
        options = ['./autogen.sh']
        options += getattr(self, 'configure_flag_args', [])
        options += ['--prefix={0}'.format(prefix)]
        options += self.configure_args()
        for i, opt in enumerate(options):
            if opt.endswith('documentation'):
                options[i] = opt.replace('documentation', 'doc')

        with working_dir(self.build_directory, create=True):
            which('bash')(*options)
