#!/bin/bash
cd ${RPM_INSTALL_PREFIX}
mkdir -p share/cms/crab-prod/%{ver}
for dir in bin lib etc examples; do
  rsync -a ${dir}/ share/cms/crab-prod/%{ver}/${dir}/
done
