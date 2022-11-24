from spack import *
from spack.pkg.builtin.zlib import Zlib as BuiltinZlib
from spack.pkg.builtin.zlib import SetupEnvironment as BuiltinSetupEnvironment


class Zlib(BuiltinZlib):
    __doc__ = BuiltinZlib.__doc__

    if platform.machine() == "x86_64":
        git = "https://github.com/cms-externals/zlib.git"
        version("1.2.11.cms", commit="822f7f5a8c57802faf8bbfe16266be02eff8c2e2")
    else:
	git = "https://github.com/madler/zlib.git"
        version("1.2.11.cms", tag="v1.2.11")


class SetupEnvironment(BuiltinSetupEnvironment):
    def setup_build_environment(self, env):
        super().setup_build_environment(env)

        env.append_flags("CFLAGS", "-DUSE_MMAP")
        env.append_flags("CFLAGS", "-DUNALIGNED_OK")
        env.append_flags("CFLAGS", "-D_LARGEFILE64_SOURCE=1")
        if self.spec.target.family == "x86_64":
            env.append_flags("CFLAGS", "-msse3")


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder, SetupEnvironment):
    pass
