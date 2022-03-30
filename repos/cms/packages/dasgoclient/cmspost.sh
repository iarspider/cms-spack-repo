#!/bin/bash
# copy wrapper script into common if latest version is same as this version
mkdir -p $RPM_INSTALL_PREFIX/common
if [ "`find ${RPM_INSTALL_PREFIX}/ -wholename '*/etc/dasgoclient' | sed 's|.*/dasgoclient-\(v.*\?\)-.*/\?|\1|' | sort | tail -1`" = "%v" ] ; then
  /bin/cp -f %{PREFIX}/etc/dasgoclient $RPM_INSTALL_PREFIX/common/dasgoclient.tmp
  mv $RPM_INSTALL_PREFIX/common/dasgoclient.tmp $RPM_INSTALL_PREFIX/common/dasgoclient
fi

# make das_client point to dasgoclient in overrides/bin area
mkdir -p $RPM_INSTALL_PREFIX/share/overrides/bin
[ -e $RPM_INSTALL_PREFIX/share/overrides/bin/das_client ] || ln -sf ../../../common/dasgoclient $RPM_INSTALL_PREFIX/share/overrides/bin/das_client
