from spack import *
from spack.pkg.builtin.herwig3 import Herwig3 as BuiltinHerwig3


class Herwig3(BuiltinHerwig3):
    __doc__ = BuiltinHerwig3.__doc__

    depends_on("hepmc", type=("build", "link"))
    depends_on("yoda", type=("build", "link", "run"))
    depends_on("openblas", type=("build", "link"))

    # Remove python version restricion
    drop_dependency("py-gosam")
    depends_on("py-gosam", type=("build", "run"))

    # Drop openloops dependency for ppc64le
    drop_dependency("openloops")
    depends_on("openloops", when="target=aarch64:")
    depends_on("openloops", when="target	=x86_64:")

    drop_dependency("vbfnlo")
    drop_dependency("njet")

    patch("herwig_Matchbox_mg_py3.patch")
    patch("herwig7-fxfx-fix.patch")

    def patch(self):
        filter_file("-lgslcblas", "-lopenblas", "configure")

    def flag_handler(self, name, flags):
        if name in ("cflags", "cppflags", "cxxflags"):
            flags.append(self.compiler.cc_pic_flag)

        if name == "fcflags" and self.spec.satisfies("%gcc@10:"):
            flags.append("-fno-range-check")

        return (None, None, flags)

    def setup_build_environment(self, env):
        env.set("LHAPDF_DATA_PATH", self.spec["lhapdf"].prefix.share.LHAPDF)

    # NB: we can't use super().configure, since
    # `spec["njet"]` will fail due to dropped dependency
    def configure_args(self):
        args = ["--with-gsl=system", "--enable-shared", "--disable-static",
                "--with-thepeg=" + self.spec["thepeg"].prefix,
                "--with-thepeg-headers=" + self.spec["thepeg"].prefix.include,
                "--with-fastjet=" + self.spec["fastjet"].prefix,
                "--with-boost=" + self.spec["boost"].prefix,
                "--with-madgraph=" + self.spec["madgraph5amc"].prefix,
                "--with-gosam-contrib=" + self.spec["gosam-contrib"].prefix,
                "--with-gosam=" + self.spec["gosam"].prefix,
                "--with-hepmc=" + self.spec["hepmc"].prefix]

        if self.spec.satisfies("^openloops"):
            args.append("--with-openloops=" + self.spec["openloops"].prefix)

        return args

    # CMS: we don't use FxFx, no need to build/install it
    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make("install")

    @run_after("install")
    def cms_wrapper(self):
        shutil.move(join_path(self.prefix.bin, "Herwig"), join_path(self.prefix.bin, "Herwig-cms"))
        install(join_path(os.path.dirname(__file__), "Herwig"), join_path(self.prefix.bin, "Herwig"))
