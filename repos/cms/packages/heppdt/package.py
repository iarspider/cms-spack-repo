from spack import *
from spack.pkg.builtin.heppdt import Heppdt as BuiltinHeppdt


class Heppdt(BuiltinHeppdt):
    __doc__ = BuiltinHeppdt.__doc__

    git = "https://github.com/cms-externals/heppdt.git"
    keep_archives = True

    version("3.04.01.cms", commit="2b499cfb4302d48d1fd91911fddec88e94219a44")

    depends_on("intel-tbb")

    # CMS: intel-tbb dependency
    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == "cxxflags":
            flags.extend(("-O2", "-std=c++17", "-ltbb"))

        return (None, None, flags)
