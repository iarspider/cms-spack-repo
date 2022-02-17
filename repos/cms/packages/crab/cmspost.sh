#!/bin/bash
pkgrel=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
directpkgreqs="crab-prod crab-pre crab-dev"
cd ${RPM_INSTALL_PREFIX}
crab=share/cms/crab/%{ver}
mkdir -p ${crab}/bin ${crab}/lib ${crab}/etc share/etc/profile.d
for f in crab-env.csh crab-env.sh ; do
  ${pkgrel}/common_revision_script.sh ${pkgrel}/$f share/etc/profile.d/S99$f
done
for f in crab-setup.csh crab-setup.sh ; do
  ${pkgrel}/common_revision_script.sh ${pkgrel}/$f common/$f
done
${pkgrel}/common_revision_script.sh ${pkgrel}/crab.sh            ${crab}/bin/crab.sh
${pkgrel}/common_revision_script.sh ${pkgrel}/crab-proxy-package ${crab}/lib/crab-proxy-package

for pkg in $(echo ${directpkgreqs} | tr ' ' '\n') ; do
  crab_name=$(echo $pkg | cut -d/ -f2)
  crab_type=$(echo $crab_name | sed -e 's|^crab-||')
  for p in $(cat share/${pkg}/etc/crab_py_pkgs.txt); do
    mkdir -p ${crab}/lib/${crab_type}/$p
    rm -rf ${crab}/lib/${crab_type}/$p/__init__.py*
    ln -s ../../crab-proxy-package ${crab}/lib/${crab_type}/$p/__init__.py
  done
  #Find latest version of crab client
  ls -d share/cms/${crab_name}/v*/bin/crab | sed 's|/bin/crab$||;s|.*/||' | sort -n | tail -1 > ${crab}/etc/${crab_name}.latest
  ln -sf ../${crab}/bin/crab.sh common/${crab_name}
done
ln -sf crab-prod common/crab
