import os
from llnl.util.filesystem import join_path, find

def post_install(spec):
    pkg = spec.package
    keep_archive = getattr(pkg, 'keep_archives', False)
    if keep_archive:
        return

    for file in find(spec.prefix.lib, '*.a', recursive=False):
        os.unlink(file)

    for file in find(spec.prefix.lib, '*.la', recursive=False):
        os.unlink(file)
