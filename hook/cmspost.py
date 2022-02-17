import os
from llnl.util.filesystem import join_path, force_remove


def post_install(spec):
    if not os.environ.get('RPM_INSTALL_PREFIX', ''):
        return

    if not os.path.exists(join_path(spec.prefix, 'cmspost.sh')):
        return

    bash = which('bash')
    bash('-xe', join_path(spec.prefix, 'cmspost.sh'))