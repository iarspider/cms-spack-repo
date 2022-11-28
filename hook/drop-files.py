import glob
import os
import shutil
from llnl.util.filesystem import join_path, force_remove

def rm_rf(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        force_remove(path)


def post_install(spec):
    if spec.external:
        return

    pkg = spec.package
    drop_files = getattr(pkg, 'drop_files', None)
    if drop_files is None:
        return

    if not isinstance(drop_files, (list, tuple)):
        drop_files = (drop_files, )

    for mask in drop_files:
        for path in glob.glob(join_path(spec.prefix, mask)):
            rm_rf(path)
