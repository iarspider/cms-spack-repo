#!/bin/bash
cd ${RPM_INSTALL_PREFIX}
pkgrel=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

mkdir -p share/cms/crab-dev/%{ver}
for dir in bin lib etc examples; do
  rsync -a ${pkgrel}/${dir}/ share/cms/crab-dev/%{ver}/${dir}/
done
