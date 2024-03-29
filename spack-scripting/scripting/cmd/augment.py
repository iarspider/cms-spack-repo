# Origin: https://github.com/BlueBrain/spack/blob/develop/bluebrain/spack-scripting/scripting/cmd/augment.py
import os

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack.paths
import spack.repo
from spack.spec import Spec
from spack.util.editor import editor
from spack.util.naming import mod_to_class

description = "augment builtin package files in $EDITOR"
section = "packaging"
level = "short"


def setup_parser(subparser):
    subparser.add_argument(
        '-s', '--split', action="store_true",
        help="open the original package in a split window (*vim only) "
             "when creating new packages")
    subparser.add_argument(
        '-N', '--namespace', default="cms",
        help="namespace to store the augmented package")
    subparser.add_argument(
        'package', default=None, help="package name")


def augment(parser, args):
    name = args.package
    target_repo = spack.repo.path.get_repo(args.namespace)
    target_path = target_repo.filename_for_package_name(name)

    repos = spack.repo.path.repos
    namespaces = [r.namespace for r in repos]
    target_index = namespaces.index(args.namespace)
    for repo in repos[target_index:]:
        if repo.namespace == args.namespace:
            continue
        source_path = repo.filename_for_package_name(name)
        if os.path.exists(source_path):
            break
    else:
        tty.die("No package for '{0}' was found.".format(name),
                "  Use `spack create` to create a new package")
    spec = Spec(".".join([repo.namespace, name]))

    if not os.path.exists(target_path):
        mkdirp(os.path.dirname(target_path))
        with open(target_path, "w") as pkg_file:
            pkg_file.write(PACKAGE_TEMPLATE.format(
                module=spec.package_class.fullname.replace('-', '_'),
                namespace=repo.namespace.capitalize(),
                cls=mod_to_class(name)))
    if args.split:
        editor("-o", source_path, target_path)
    else:
        editor(target_path)


PACKAGE_TEMPLATE = """\
import copy

from spack import *
from spack.pkg.{module} import {cls} as {namespace}{cls}


def drop_patch(cls, fn):
    def filter_func(p):
        if isinstance(p, FilePatch):
            return p.relative_path != fn
        elif isinstance(p, UrlPatch):
            return p.url != fn

    old_patches = copy.deepcopy(cls.patches)
    new_patches = {{}}
    for spec, patches in old_patches.items():
        filtered_patches = [p for p in patches if filter_func(p)]
        if filtered_patches:
            new_patches[spec] = filtered_patches

    cls.patches = new_patches
    del old_patches
    del new_patches


def drop_dependency(cls, name):
    dependencies = {{}}
    for k, v in cls.dependencies.items():
        if k != name:
            dependencies[k] = v

    cls.dependencies = dependencies


def drop_conflicts(cls, name):
    conflicts = {{}}
    for k, v in cls.conflicts.items():
        if k != name:
            conflicts[k] = v

    cls.conflicts = conflicts


class {cls}({namespace}{cls}):
    __doc__ = {namespace}{cls}.__doc__
"""
