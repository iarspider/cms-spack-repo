import os

from llnl.util.filesystem import *

from spack.package import PackageBase


class CMSDataPackage(PackageBase):
    build_system_class = 'CMSDataPackage'
    phases = ['install']

    def install(self, spec, prefix):
        data = getattr(self, 'data', None) or "data"
        n = self.n
        data_repo = getattr(self, 'data_repo', n.replace('data-', ''))
        data_dir = getattr(self, 'data_dir', None)
        data_dir = data_dir or join_path(data_repo.replace('-', '/'), data)

        if os.environ.get('RPM_INSTALL_PREFIX', None):
            install_root = join_path(os.environ.get('RPM_INSTALL_PREFIX'),
                                     'share', 'cms', n, str(spec.version))
            if os.path.exists(join_path(install_root, data_dir)):
                touch(join_path(prefix, '.already_installed'))
                return
        else:
            install_root = prefix

        mkdirp(join_path(install_root, data_dir))
        install_tree('.', join_path(install_root, data_dir))
        gitdirs = []
        for fn in find(install_root, '.git'):
            gitdirs.append(fn)

        for fn in gitdirs:
            if os.path.isdir(fn):
                shutil.rmtree(fn)
