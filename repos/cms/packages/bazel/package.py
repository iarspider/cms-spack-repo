from spack import *
from spack.pkg.builtin.bazel import Bazel as BuiltinBazel


class Bazel(BuiltinBazel):
    __doc__ = BuiltinBazel.__doc__

    def setup_build_environment(self, env):
        super().setup_build_environment(env)
        # -- CMS: fix building with external Java
        env.set("JAVA_HOME", "/usr/lib/jvm/java")
