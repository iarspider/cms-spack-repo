import glob
import os

def post_install(spec): 
    pkg = spec.package
    strip_files = getattr(pkg, 'strip_files', None)
    if strip_files is None:
        return
        
    strip = which('strip')
    if not isinstance(strip_files, (list, tuple)):
        strip_files = (strip_files, )
        
    for dir in strip_files:
        path = join_path(spec.prefix, dir)
        if not os.path.exists(path):
            continue
            
        for file in find(path, '*'):
            if is_exe(file):
                strip('--strip-unneeded', file)