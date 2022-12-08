from spack import *
from spack.pkg.builtin.bazel import Bazel as BuiltinBazel


class Bazel(BuiltinBazel):
    __doc__ = BuiltinBazel.__doc__

    patch('bazel-3.7.0-patches.patch', when='@3.7.0:')  # -- CMS
    # patch('bazel-3.7.2-gcc11.patch', when='@3.7.0:')  # included upstream

    def setup_build_environment(self, env):
        super().setup_build_environment(env)
        # -- CMS: fix building with external Java
        env.set("JAVA_HOME", "/usr/lib/jvm/java")
