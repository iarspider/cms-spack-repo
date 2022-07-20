import os
from llnl.util.filesystem import join_path, force_remove, touch
from spack.util.executable import which


def post_install(spec):
    if not os.environ.get('RUN_CMSPOST', None):
        return

    if not os.path.exists(join_path(spec.prefix, 'cmspost.sh')):
        return

    if os.path.exists(join_path(spec.prefix, '.cmspost_done')):
        return

    bash = which('bash')
    bash('-xe', join_path(spec.prefix, 'cmspost.sh'))
    touch(join_path(spec.prefix, '.cmspost_done'))
