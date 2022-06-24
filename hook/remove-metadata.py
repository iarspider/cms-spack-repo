import glob
import os
import shutil

from llnl.util.filesystem import join_path

def post_install(spec):
    spackdir = join_path(spec.prefix, '.spack')
    for n in os.listdir(spackdir):
        if n in ('spec.json', 'install_manifest.json'):
            continue
        if os.path.isdir(join_path(spec.prefix, '.spack', n)):
            shutil.rmtree(join_path(spec.prefix, '.spack', n))
        else:
            os.unlink(join_path(spec.prefix, '.spack', n))

