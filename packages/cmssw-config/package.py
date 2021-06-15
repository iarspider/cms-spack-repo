from spack import *

class CmsswConfig(Package):
    url      = "http://www.example.com/example-1.2.3.tar.gz"

    version('V06-02-12', git='https://github.com/cms-sw/cmssw-config.git', tag='V06-02-12')


    def install(self, spec, prefix):

        install_tree(self.stage.source_path,prefix.bin)
