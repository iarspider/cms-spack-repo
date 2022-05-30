#!/bin/bash
if [ -f ${RPM_INSTALL_PREFIX}/etc/cmssw-wm-tools/version ] ; then
  if [ $(cat ${RPM_INSTALL_PREFIX}/etc/cmssw-wm-tools/version) -ge %{realversion} ] ; then
    exit 0
  fi
fi
mkdir -p $RPM_INSTALL_PREFIX/share/overrides ${RPM_INSTALL_PREFIX}/etc/cmssw-wm-tools
for d in bin python ; do
  rsync -a %{prefix}/$d/ $RPM_INSTALL_PREFIX/share/overrides/$d/
done
echo %{realversion} > ${RPM_INSTALL_PREFIX}/etc/cmssw-wm-tools/version
