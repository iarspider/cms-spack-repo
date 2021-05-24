import glob
import os

def post_install(spec): 
    pkg = spec.package
    keep_archive = getattr(pkg, 'keep_archive', False)
    if keep_archive:
        return
              
    for file in glob.glob(join_path(spec.prefix, 'lib', '*.a')):
        shutil.unlink(file)

    for file in glob.glob(join_path(spec.prefix, 'lib', '*.la')):
        shutil.unlink(file)