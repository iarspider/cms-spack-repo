import copy

from spack import *
from spack.pkg.builtin.git import Git as BuiltinGit


class Git(BuiltinGit):
    __doc__ = BuiltinGit.__doc__

    drop_dependency("gettext")
    drop_dependency("libidn2")
    depends_on("python")

    drop_files = ["share/man"]

    # -- CMS
    patch("git-2.19.0-runtime.patch", when="@2.19.0:")

    def setup_build_environment(self, env):
        super().setup_build_environment(env)
        env.set("NO_LIBPCRE1_JIT", "1")

    def configure_args(self):
        args = super().configure_args()
        args.append("--with-python={0}".format(spec["python"].prefix))
        return args

    def build(self, spec, prefix):
        # -- CMS; in spack this list is empty
        args = [
            "NO_R_TO_GCC_LINKER=1",
            "RUNTIME_PREFIX=1",
            "V=1",
            "NO_CROSS_DIRECTORY_HARDLINK=1",
            "NO_INSTALL_HARDLINKS=1",
        ]

        if "~nls" in self.spec:
            args.append("NO_GETTEXT=1")
        make(*args)

        # -- CMS: generate ca-bundle
        mkdirp(join_path(self.stage.source_path, "ca-bundle"))
        shutil.copy(
            join_path(os.path.dirname(__file__), "mk-ca-bundle.pl"),
            join_path(self.stage.source_path, "ca-bundle"),
        )
        perl = which("perl")
        with working_dir(join_path(self.stage.source_path, "ca-bundle")):
            perl("mk-ca-bundle.pl")

    def install(self, spec, prefix):
        args = [
            "V=1",
            "NO_CROSS_DIRECTORY_HARDLINK=1",
            "NO_INSTALL_HARDLINKS=1",
            "install",
        ]
        if "~nls" in self.spec:
            args.append("NO_GETTEXT=1")

        make(*args)

        # -- CMS: install ca-bundle
        mkdirp(join_path(prefix.share.ssl.certs))
        install(
            join_path(self.stage.source_path, "ca-bundle", "ca-bundle.crt"),
            join_path(prefix.share.ssl.certs),
        )

    def setup_run_environment(self, env):
        super().setup_run_environment(env)

        # -- CMS: set more env variables
        env.prepend_path("PATH", join_path(self.prefix.libexec, "git-core"))
        env.set(
            "GIT_TEMPLATE_DIR", join_path(self.prefix.share, "git-core", "templates")
        )
        env.set("GIT_SSL_CAINFO", join_path(prefix.share.ssl.certs, "ca-bundle.crt"))
        env.set("GIT_EXEC_PATH", join_path(self.prefix.libexec, "git-core"))
