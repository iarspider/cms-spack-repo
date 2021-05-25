import glob
import os
from llnl.util.filesystem import join_path

def post_install(spec): 
    pkg = spec.package
    keep_archive = getattr(pkg, 'keep_archive', False)
    if keep_archive:
        return
              
    for file in glob.glob(join_path(spec.prefix, 'lib', '*.a')):
        os.unlink(file)

    for file in glob.glob(join_path(spec.prefix, 'lib', '*.la')):
        os.unlink(file)
