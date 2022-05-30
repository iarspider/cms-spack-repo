#!/bin/bash
pkgrel=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd ${RPM_INSTALL_PREFIX}
mkdir -p share/cms/crab-prod/%{ver}
for dir in bin lib etc examples; do
  rsync -a ${pkgrel}/${dir}/ share/cms/crab-prod/%{ver}/${dir}/
done
