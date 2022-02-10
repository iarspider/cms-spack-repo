#!/bin/bash
cd ${RPM_INSTALL_PREFIX}
mkdir -p share/cms/${PKGNAME}/${PKGVERSION}
for dir in bin lib etc examples; do
  rsync -a ${dir}/ share/cms/${PKGNAME}/${PKGVERSION}/${dir}/
done
