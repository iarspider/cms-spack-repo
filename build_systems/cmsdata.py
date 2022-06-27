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

        install_root = prefix

        mkdirp(join_path(install_root, data_dir))
        install_tree('.', join_path(install_root, data_dir))
        gitdirs = []
        for fn in find(install_root, '.git'):
            gitdirs.append(fn)

        for fn in gitdirs:
            if os.path.isdir(fn):
                shutil.rmtree(fn)
