from spack import *

class CmsswConfig(Package):
    git = 'https://github.com/cms-sw/cmssw-config.git'

    version('V06-02-15', tag='V06-02-15')


    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)
