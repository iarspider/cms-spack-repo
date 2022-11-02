import copy

from spack import *
from spack.pkg.builtin.hepmc import Hepmc as BuiltinHepmc


class Hepmc(BuiltinHepmc):
    __doc__ = BuiltinHepmc.__doc__

   keep_archives = True
   drop_files = ["share"]

   def flag_handler(self, name, flags):
       if name == "cxxflags":
           flags.append(self.compiler.cxx_pic_flag)

       return (None, None, flags)

    @run_after("install")
    def post_install(self):
        prefix = self.prefix
        for fn in glob.glob(join_path(prefix.lib, "*.so")):
            os.remove(fn)
