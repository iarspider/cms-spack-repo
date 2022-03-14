#!/bin/bash -e
vanilla_root="/home/razumov/Work/_CMS/vanilla_spack/var/spack/repos/builtin/packages"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd $(dirname $SCRIPT_DIR)
[ $# -lt 1 ] && (echo "Usage: backport.sh <package> [<package> ...]"; exit 1)
for pname in "$@"
do
    [ ! -d ${vanilla_root}/${pname} -o ! -f ${vanilla_root}/${pname}/package.py ] && (echo "Can't find recipe for $pname"; exit 2)
    cp -rf ${vanilla_root}/${pname} repos/backport/packages
    cp -rf repos/backport/packages/${pname} spack/var/spack/repos/builtin/packages
done
