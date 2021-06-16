# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
from spack.util.environment import is_system_path
import sys


class Root(CMakePackage):
    """ROOT is a data analysis framework."""

    homepage = "https://root.cern.ch"
    git      = "https://github.com/cms-sw/root.git"

    executables = ['^root$', '^root-config$']

    tags = ['hep']

    maintainers = ['chissg', 'HadrienG2', 'drbenmorgan', 'vvolkl']

    # ###################### Versions ##########################

    # Master branch
    version('master', branch='master')

    version('6.22.00.patches_cms_a15e883', branch='cms/v6-22-00-patches/a15e883')

    # ###################### Variants ##########################
    # See README.md for specific notes about what ROOT configuration
    # options are or are not supported, and why.

    variant('aqua', default=False,
            description='Enable Aqua interface')
    variant('davix', default=True,
            description='Compile with external Davix')
    variant('dcache', default=False,
            description='Enable support for dCache')
    variant('emacs', default=False,
            description='Enable Emacs support')
    variant('examples', default=True,
            description='Install examples')
    variant('fftw', default=False,
            description='Enable Fast Fourier Transform support')
    variant('fits', default=False,
            description='Enable support for images and data from FITS files')
    variant('fortran', default=False,
            description='Enable the Fortran components of ROOT')
    variant('graphviz', default=False,
            description='Enable graphviz support')
    variant('gdml', default=True,
            description='Enable GDML writer and reader')
    variant('gminimal', default=True,
            description='Ignore most of Root\'s feature defaults except for '
            'basic graphic options')
    variant('gsl', default=True,
            description='Enable linking against shared libraries for GSL')
    variant('http', default=False,
            description='Enable HTTP server support')
    variant('jemalloc', default=False,
            description='Enable using the jemalloc allocator')
    variant('math', default=True,
            description='Build the new libMathMore extended math library')
    variant('memstat', default=False,
            description='Enable a memory stats utility to detect memory leaks')
    # Minuit must not be installed as a dependency of root
    # otherwise it crashes with the internal minuit library
    variant('minuit', default=True,
            description='Automatically search for support libraries')
    variant('mlp', default=False,
            description="Enable support for TMultilayerPerceptron "
            "classes' federation")
    variant('mysql', default=False)
    variant('opengl', default=True,
            description='Enable OpenGL support')
    variant('oracle', default=False,
            description='Enable support for Oracle databases')
    variant('postgres', default=False,
            description='Enable postgres support')
    variant('pythia6', default=False,
            description='Enable pythia6 support')
    variant('pythia8', default=False,
            description='Enable pythia8 support')
    variant('python', default=True,
            description='Enable Python ROOT bindings')
    variant('qt4', default=False,
            description='Enable Qt graphics backend')
    variant('r', default=False,
            description='Enable R ROOT bindings')
    variant('rpath', default=True,
            description='Enable RPATH')
    variant('roofit', default=True,
            description='Build the libRooFit advanced fitting package')
    variant('root7', default=False,
            description='Enable ROOT 7 support')
    variant('shadow', default=False,
            description='Enable shadow password support')
    variant('spectrum', default=False,
            description='Enable support for TSpectrum')
    variant('sqlite', default=False,
            description='Enable SQLite support')
    variant('ssl', default=False,
            description='Enable SSL encryption support')
    variant('table', default=False,
            description='Build libTable contrib library')
    variant('tbb', default=True,
            description='TBB multi-threading support')
    variant('threads', default=True,
            description='Enable using thread library')
    variant('tmva', default=False,
            description='Build TMVA multi variate analysis library')
    variant('unuran', default=True,
            description='Use UNURAN for random number generation')
    variant('vc', default=False,
            description='Enable Vc for adding new types for SIMD programming')
    variant('vdt', default=True,
            description='Enable set of fast and vectorisable math functions')
    variant('veccore', default=False,
            description='Enable support for VecCore SIMD abstraction library')
    variant('vmc', default=False,
            description='Enable the Virtual Monte Carlo interface')
    variant('x', default=True,
            description='Enable set of graphical options')
    variant('xml', default=True,
            description='Enable XML parser interface')
    variant('xrootd', default=False,
            description='Build xrootd file server and its client')

    # ###################### Compiler variants ########################

    variant('cxxstd',
            default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    # ###################### Dependencies ######################

    depends_on('cmake@3.4.3:', type='build', when='@:6.16.99')
    depends_on('cmake@3.9:', type='build', when='@6.18.00:')
    depends_on('pkgconfig', type='build')

    depends_on('blas')
    depends_on('freetype')
    depends_on('jpeg')
    depends_on('libice')
    depends_on('libpng')
    depends_on('lz4', when='@6.13.02:')  # See cmake_args, below.
    depends_on('ncurses')
    depends_on('nlohmann-json', when='@6.24:')
    depends_on('pcre')
    depends_on('xxhash', when='@6.13.02:')  # See cmake_args, below.
    depends_on('xz')
    depends_on('zlib')
    depends_on('zstd', when='@6.20:')

    # X-Graphics
    depends_on('libx11',  when="+x")
    depends_on('libxext', when="+x")
    depends_on('libxft',  when="+x")
    depends_on('libxpm',  when="+x")
    depends_on('libsm',   when="+x")

    # OpenGL
    depends_on('ftgl@2.4.0:',  when="+x+opengl")
    depends_on('glew',  when="+x+opengl")
    depends_on('gl',    when="+x+opengl")
    depends_on('glu',   when="+x+opengl")
    depends_on('gl2ps', when="+x+opengl")

    # Qt4
    depends_on('qt@:4.999', when='+qt4')

    # Python
    depends_on('python@2.7:', when='+python', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'), when='+tmva')
    # This numpy dependency was not intended and will hopefully
    # be fixed in 6.20.06.
    # See: https://sft.its.cern.ch/jira/browse/ROOT-10626
    depends_on('py-numpy', type=('build', 'run'),
               when='@6.20.00:6.20.05 +python')

    # Optional dependencies
    depends_on('davix @0.7.1:', when='+davix')
    depends_on('dcap',      when='+dcache')
    depends_on('cfitsio',   when='+fits')
    depends_on('fftw',      when='+fftw')
    depends_on('graphviz',  when='+graphviz')
    depends_on('gsl',       when='+gsl')
    depends_on('jemalloc',  when='+jemalloc')
    depends_on('mysql-client',   when='+mysql')
    depends_on('openssl',   when='+ssl')
    depends_on('openssl',   when='+davix')  # Also with davix
    depends_on('oracle-instant-client', when='+oracle @:6.24.01')
    depends_on('postgresql', when='+postgres')
    depends_on('pythia6+root', when='+pythia6')
    depends_on('pythia8',   when='+pythia8')
    depends_on('r',         when='+r', type=('build', 'run'))
    depends_on('r-rcpp',    when='+r', type=('build', 'run'))
    depends_on('r-rinside', when='+r', type=('build', 'run'))
    depends_on('readline',  when='+r')
    depends_on('shadow',    when='+shadow')
    depends_on('sqlite',    when='+sqlite')
    depends_on('tbb',       when='+tbb')
    # See: https://github.com/root-project/root/issues/6933
    # -- CMS: fixed in -patches branch
    #conflicts('^intel-tbb@2021.1:', when='@:6.22',
    #          msg='Please use an older intel-tbb version')
    #conflicts('^intel-oneapi-tbb@2021.1:', when='@:6.22',
    #          msg='Please use an older intel-tbb/intel-oneapi-tbb version')
    # depends_on('intel-tbb@:2021.0', when='@:6.22 ^intel-tbb')
    depends_on('unuran',    when='+unuran')
    depends_on('vc',        when='+vc')
    depends_on('vdt',       when='+vdt')
    depends_on('veccore',   when='+veccore')
    depends_on('libxml2',   when='+xml')
    depends_on('xrootd',          when='+xrootd')
    depends_on('xrootd@:4.99.99', when='@:6.22.03 +xrootd')

    # ###################### Conflicts ######################

    # I was unable to build root with any Intel compiler
    # See https://sft.its.cern.ch/jira/browse/ROOT-7517
    conflicts('%intel')

    # ROOT <6.08 was incompatible with the GCC 5+ ABI
    conflicts('%gcc@5.0.0:', when='@:6.07.99')

    # The version of Clang featured in ROOT <6.12 fails to build with
    # GCC 9.2.1, which we can safely extrapolate to the GCC 9 series.
    conflicts('%gcc@9.0.0:', when='@:6.11.99')

    # ROOT <6.14 was incompatible with Python 3.7+
    conflicts('^python@3.7:', when='@:6.13.99 +python')

    # See README.md
    conflicts('+http',
              msg='HTTP server currently unsupported due to dependency issues')

    # Incompatible variants
    conflicts('+opengl', when='~x', msg='OpenGL requires X')
    conflicts('+tmva', when='~gsl', msg='TVMA requires GSL')
    conflicts('+tmva', when='~mlp', msg='TVMA requires MLP')
    conflicts('cxxstd=11', when='+root7', msg='root7 requires at least C++14')

    # Feature removed in 6.18:
    for pkg in ('memstat', 'qt4', 'table'):
        conflicts('+' + pkg, when='@6.18.00:',
                  msg='Obsolete option +{0} selected.'.format(pkg))

    @classmethod
    def filter_detected_exes(cls, prefix, exes_in_prefix):
        result = []
        for exe in exes_in_prefix:
            # no need to check the root executable itself
            # we can get all information from root-config
            if exe.endswith('root'):
                continue
            result.append(exe)
        return result

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        # turn the output of root-config --version
        # (something like 6.22/06)
        # into the format used in this recipe (6.22.06)
        return output.strip().replace('/', '.')

    def cmake_args(self):
        spec = self.spec
        define = self.define
        define_from_variant = self.define_from_variant
        options = []

        # ###################### Boolean Options ######################
        # For option list format see _process_opts(), below.

        # Options controlling gross build / config behavior.
        options += [
            define('cxxmodules', False),
            define('exceptions', True),
            define('explicitlink', True),
            define('fail-on-missing', True),
            define_from_variant('fortran'),
            define_from_variant('gminimal'),
            define('gnuinstall', False),
            define('libcxx', False),
            define('pch', True),
            define('roottest', False),
            define_from_variant('rpath'),
            define('runtime_cxxmodules', False),
            define('shared', True),
            define('soversion', True),
            define('testing', self.run_tests),
            define_from_variant('thread', 'threads'),
            # The following option makes sure that Cling will call the compiler
            # it was compiled with at run time; see #17488, #18078 and #23886
            define('CLING_CXX_PATH', self.compiler.cxx)
        ]

        # Options related to ROOT's ability to download and build its own
        # dependencies. Per Spack convention, this should generally be avoided.
        options += [
            define_from_variant('builtin_afterimage', 'x'),
            define('builtin_cfitsio', False),
            define('builtin_davix', False),
            define('builtin_fftw3', False),
            define('builtin_freetype', False),
            # CMS: Use builtins for ftgl, glew, gl2ps
            define('builtin_ftgl', True),
            define('builtin_gl2ps', True),
            define('builtin_glew', True),
            define('builtin_gsl', False),
            define('builtin_llvm', True),
            define('builtin_lz4', False),
            define('builtin_lzma', False),
            define('builtin_nlohmannjson', False),
            define('builtin_openssl', False),
            define('builtin_pcre', False),
            define('builtin_tbb', False),
            define('builtin_unuran', False),
            define('builtin_vc', False),
            define('builtin_vdt', False),
            define('builtin_veccore', False),
            define('builtin_xrootd', False),
            define('builtin_xxhash', True),
            define('builtin_zlib', False)
        ]

        # Features
        options += [
            define('afdsmrgd', False),
            define('afs', False),
            define('alien', False),
            define('arrow', False),
            define('asimage', True),
            define('astiff', True),
            define('bonjour', False),
            define('castor', False),
            define('ccache', False),
            define('chirp', False),
            define('cling', True),
            define_from_variant('cocoa', 'aqua'),
            define('dataframe', True),
            define_from_variant('davix'),
            define_from_variant('dcache'),
            define_from_variant('fftw3', 'fftw'),
            define_from_variant('fitsio', 'fits'),
            define_from_variant('ftgl', 'opengl'),
            define_from_variant('gdml'),
            define_from_variant('genvector', 'math'),
            define('geocad', False),
            define('gfal', False),
            define_from_variant('gl2ps', 'opengl'),
            define('glite', False),
            define('globus', False),
            define_from_variant('gsl_shared', 'gsl'),
            define_from_variant('gviz', 'graphviz'),
            define('hdfs', False),
            define_from_variant('http'),  # See conflicts
            define_from_variant('imt', 'tbb'),
            define_from_variant('jemalloc'),
            define('krb5', False),
            define('ldap', False),
            define_from_variant('mathmore', 'math'),
            define_from_variant('memstat'),  # See conflicts
            define('minimal', False),
            define_from_variant('minuit'),
            define_from_variant('minuit2', 'minuit'),
            define_from_variant('mlp'),
            define('monalisa', False),
            define_from_variant('mysql'),
            define('odbc', False),
            define_from_variant('opengl'),
            define_from_variant('oracle'),
            define_from_variant('pgsql', 'postgres'),
            define_from_variant('pythia6'),
            define_from_variant('pythia8'),
            define_from_variant('qt', 'qt4'),  # See conflicts
            define_from_variant('qtgsi', 'qt4'),  # See conflicts
            define_from_variant('r'),
            define('rfio', False),
            define_from_variant('roofit'),
            define_from_variant('root7'),  # See conflicts
            define('ruby', False),
            define('sapdb', False),
            define_from_variant('shadowpw', 'shadow'),
            define_from_variant('spectrum'),
            define_from_variant('sqlite'),
            define('srp', False),
            define_from_variant('ssl'),
            define_from_variant('table'),
            define_from_variant('tbb'),
            define('tcmalloc', False),
            define_from_variant('tmva'),
            define_from_variant('unuran'),
            define_from_variant('vc'),
            define_from_variant('vdt'),
            define_from_variant('veccore'),
            define_from_variant('vmc'),
            define_from_variant('webui', 'root7'),  # requires root7
            define_from_variant('x11', 'x'),
            define_from_variant('xft', 'x'),
            define_from_variant('xml'),
            define_from_variant('xrootd')
        ]

        # Some special features
        if self.spec.satisfies('@6.20.02:'):
            options.append(define_from_variant('pyroot', 'python'))
        else:
            options.append(define_from_variant('python'))

        # #################### Compiler options ####################

        if sys.platform == 'darwin' and self.compiler.cc == 'gcc':
            cflags = '-D__builtin_unreachable=__builtin_trap'
            options.extend([
                define('CMAKE_C_FLAGS', cflags),
                define('CMAKE_CXX_FLAGS', cflags),
            ])

        # Method for selecting C++ standard depends on ROOT version
        if self.spec.satisfies('@6.18.00:'):
            options.append(define_from_variant('CMAKE_CXX_STANDARD', 'cxxstd'))
        else:
            options.append(define('cxx' + self.spec.variants['cxxstd'].value,
                                  True))

        if '+x+opengl' in self.spec:
            ftgl_prefix = self.spec['ftgl'].prefix
            options.append(define('FTGL_ROOT_DIR', ftgl_prefix))
            options.append(define('FTGL_INCLUDE_DIR', ftgl_prefix.include))
        if '+python' in self.spec:
            # See https://github.com/spack/spack/pull/11579
            options.append(define('PYTHON_EXECUTABLE',
                                  spec['python'].command.path))

        return options

    def setup_build_environment(self, env):
        spec = self.spec

        if 'lz4' in spec:
            env.append_path('CMAKE_PREFIX_PATH', spec['lz4'].prefix)

        # This hack is made necessary by a header name collision between
        # asimage's "import.h" and Python's "import.h" headers...
        env.set('SPACK_INCLUDE_DIRS', '', force=True)

        # ...but it breaks header search for any ROOT dependency which does not
        # use CMake. To resolve this, we must bring back those dependencies's
        # include paths into SPACK_INCLUDE_DIRS.
        #
        # But in doing so, we must be careful not to inject system header paths
        # into SPACK_INCLUDE_DIRS, even in a deprioritized form, because some
        # system/compiler combinations don't like having -I/usr/include around.
        def add_include_path(dep_name):
            include_path = spec[dep_name].prefix.include
            if not is_system_path(include_path):
                env.append_path('SPACK_INCLUDE_DIRS', include_path)

        # With that done, let's go fixing those deps
        if spec.satisfies('@:6.12.99'):
            add_include_path('zlib')
        if '+x' in spec:
            if spec.satisfies('@:6.08.99') or spec.satisfies('@6.22:'):
                add_include_path('xextproto')
            add_include_path('fontconfig')
            add_include_path('libx11')
            add_include_path('xproto')
        if '+opengl' in spec:
            add_include_path('glew')
            add_include_path('mesa-glu')

    def setup_run_environment(self, env):
        env.set('ROOTSYS', self.prefix)
        env.set('ROOT_VERSION', 'v{0}'.format(self.version.up_to(1)))
        env.prepend_path('PYTHONPATH', self.prefix.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('ROOTSYS', self.prefix)
        env.set('ROOT_VERSION', 'v{0}'.format(self.version.up_to(1)))
        env.prepend_path('PYTHONPATH', self.prefix.lib)
        env.prepend_path('PATH', self.prefix.bin)
        env.append_path('CMAKE_MODULE_PATH', self.prefix.cmake)
        if "+rpath" not in self.spec:
            env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set('ROOTSYS', self.prefix)
        env.set('ROOT_VERSION', 'v{0}'.format(self.version.up_to(1)))
        env.prepend_path('PYTHONPATH', self.prefix.lib)
        env.prepend_path('PATH', self.prefix.bin)
        if "+rpath" not in self.spec:
            env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)
