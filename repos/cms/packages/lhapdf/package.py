import os

from spack import *
from spack.pkg.builtin.lhapdf import Lhapdf as BuiltinLhapdf


class Lhapdf(BuiltinLhapdf):
    __doc__ = BuiltinLhapdf.__doc__

    resource(
        name="MSTW2008nlo68cl",
        url="https://lhapdfsets.web.cern.ch/current/MSTW2008nlo68cl.tar.gz",
        destination="",
        placement="MSTW2008nlo68cl",
        sha256="98ec0541e80e223785bb6029ebf81e93ca5111da41d6565b3b5c4aa86d59bb5d",
    )

    @run_after("install")
    def install_pdfsets(self):
        # mkdir -p %{i}/share/LHAPDF
        # cd %{i}/share/LHAPDF
        # cp %{_sourcedir}/MSTW2008nlo68cl.tar.gz .
        # tar xvfz MSTW2008nlo68cl.tar.gz
        # rm -f MSTW2008nlo68cl.tar.gz
        # chmod a+x %{_sourcedir}/lhapdf_makeLinks
        # %{_sourcedir}/lhapdf_makeLinks %{setsversion}
        # rm -f pdfsets.index
        # cp -f %{_sourcedir}/lhapdf_pdfsetsindex pdfsets.index
        # cd -
        with working_dir(self.prefix.share.LHAPDF, create=True):
            res_path = join_path(self.stage.source_path, "MSTW2008nlo68cl")
            install_tree(res_path, ".")

            code_dir = os.path.dirname(__file__)
            set_executable(join_path(code_dir, "lhapdf_makeLinks.sh"))
            makeLinks = Executable(join_path(code_dir, "lhapdf_makeLinks.sh"))
            makeLinks(self.setsversion)

            os.remove("pdfsets.index")

        #        f1 = open(join_path(code_dir, 'pdfsets.index'), 'rb')
        #        f1.close()
        #        f2 = open(join_path(self.prefix.share.LHAPDF, 'pdfsets.index'), 'wb')
        #        f2.close()
        #        os.remove(join_path(self.prefix.share.LHAPDF, 'pdfsets.index'))
        #        sleep(1)
        install(join_path(code_dir, "pdfsets.index"), self.prefix.share.LHAPDF)
