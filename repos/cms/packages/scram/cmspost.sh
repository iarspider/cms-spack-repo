#!/bin/bash
pkgrel=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
pkgrel=$(echo $pkgrel | sed -e "s#$RPM_INSTALL_PREFIX/##g")
cmsplatf='ChAnGeMe'
realversion=""
#############################################################################
SCRAM_ALL_VERSIONS='V[0-9][0-9]*_[0-9][0-9]*_[0-9][0-9]*'
SCRAM_REL_MINOR=$(echo ${realversion} | grep "${SCRAM_ALL_VERSIONS}" | sed 's|^\(V[0-9][0-9]*_[0-9][0-9]*\)_.*|\1|')
SCRAM_REL_MAJOR=$(echo ${realversion} | sed 's|^\(V[0-9][0-9]*\)_.*|\1|')
pkgdir="lcg/scram/${realversion}"
pkgcategory="lcg"
pkgname="scram"

sed -i -e "s|^BASEPATH = .*|BASEPATH = '$RPM_INSTALL_PREFIX'|" ${pkgrel}/SCRAM/__init__.py
echo "SCRAMV1_ROOT='$RPM_INSTALL_PREFIX/${pkgrel}'" > ${pkgrel}/etc/profile.d/init.sh
echo "SCRAMV1_VERSION='${realversion}'" >> ${pkgrel}/etc/profile.d/init.sh
echo "set SCRAMV1_ROOT='$RPM_INSTALL_PREFIX/${pkgrel}'" > ${pkgrel}/etc/profile.d/init.csh
echo "set SCRAMV1_VERSION='${realversion}'" >> ${pkgrel}/etc/profile.d/init.csh

if [ ! -d $RPM_INSTALL_PREFIX/etc/scramrc ] ; then
  mkdir -p $RPM_INSTALL_PREFIX/etc/scramrc
  touch $RPM_INSTALL_PREFIX/etc/scramrc/links.db
  echo 'CMSSW=$SCRAM_ARCH/cmssw/CMSSW_*'       > $RPM_INSTALL_PREFIX/etc/scramrc/cmssw.map
  echo 'CMSSW=$SCRAM_ARCH/cmssw-patch/CMSSW_*' > $RPM_INSTALL_PREFIX/etc/scramrc/cmssw-patch.map
  echo 'CORAL=$SCRAM_ARCH/coral/CORAL_*'       > $RPM_INSTALL_PREFIX/etc/scramrc/coral.map
  # TODO [ ! -f $RPM_INSTALL_PREFIX/%{OldDB} ] || grep '%{OldDB} *$' $RPM_INSTALL_PREFIX/%{OldDB} | awk '{print $2}' | sed 's|%{OldDB}.*||' > $RPM_INSTALL_PREFIX/etc/scramrc/links.db
fi

touch $RPM_INSTALL_PREFIX/etc/scramrc/site.cfg

mkdir -p $RPM_INSTALL_PREFIX/share/etc/default-scram
##
## prob not needed for spack -- Shahzad
### BackwardCompatibilityVersionPolicy
##touch $RPM_INSTALL_PREFIX/share/etc/default-scram/${SCRAM_REL_MINOR}
##for ver in `find etc/default-scram -maxdepth 1 -mindepth 1 -name "${SCRAM_REL_MAJOR}_[0-9]*" -type f |  xargs -I '{}' basename '{}' | grep 'V[0-9][0-9]*_[0-9][0-9]*$' `; do
##  if [ -f etc/default-scram/${SCRAM_REL_MAJOR} ] ; then
##    cp etc/default-scram/${SCRAM_REL_MAJOR} etc/default-scram/$ver
##  else
##    rm -f etc/default-scram/$ver
##  fi
##done

#Create a shared copy of this version
if [ ! -d $RPM_INSTALL_PREFIX/share/${pkgdir} ] ; then
  mkdir -p $RPM_INSTALL_PREFIX/share/${pkgdir}
  rsync --links --ignore-existing --recursive --exclude='etc/' --exclude '.spack/'  ${pkgrel}/ $RPM_INSTALL_PREFIX/share/${pkgdir}
  for f in `rsync --links --ignore-existing --recursive --itemize-changes ${pkgrel}/etc $RPM_INSTALL_PREFIX/share/${pkgdir} | grep '^>f' | sed -e 's|.* ||'` ; do
    sed -i -e "s|/${pkgrel}|/share/${pkgdir}|g" $RPM_INSTALL_PREFIX/share/${pkgdir}/$f
  done
fi

cd $RPM_INSTALL_PREFIX/share
VERSION_REGEXP="${SCRAM_ALL_VERSIONS}" ; VERSION_FILE=default-scramv1-version          #; {SetLatestVersion}

vers=""
for ver in `find ${pkgcategory}/${pkgname} -maxdepth 2 -mindepth 2 -name "bin" -type d | sed 's|/bin$||' | xargs -I '{}' basename '{}' | grep "$VERSION_REGEXP" `; do
  ver_str=`echo $ver | sed 's|-.\+$||' | tr '_' '\n' | sed 's|V\([0-9]\)$|V0\1|;s|^\([0-9]\)$|0\1|' | tr '\n' '_'`
  vers="${ver_str}zzz:${ver} ${vers}"
done
echo $vers | tr ' ' '\n' | grep -v '^$' | sort  | tail -1 | sed 's|.*:||' > etc/$VERSION_FILE
[ -s etc/$VERSION_FILE ] || rm -f etc/$VERSION_FILE

VERSION_REGEXP="${SCRAM_REL_MAJOR}_"   ; VERSION_FILE=default-scram/${SCRAM_REL_MAJOR} #; {SetLatestVersion}

vers=""
for ver in `find ${pkgcategory}/${pkgname} -maxdepth 2 -mindepth 2 -name "bin" -type d | sed 's|/bin$||' | xargs -I '{}' basename '{}' | grep "$VERSION_REGEXP" `; do
  ver_str=`echo $ver | sed 's|-.\+$||' | tr '_' '\n' | sed 's|V\([0-9]\)$|V0\1|;s|^\([0-9]\)$|0\1|' | tr '\n' '_'`
  vers="${ver_str}zzz:${ver} ${vers}"
done
echo $vers | tr ' ' '\n' | grep -v '^$' | sort  | tail -1 | sed 's|.*:||' > etc/$VERSION_FILE
[ -s etc/$VERSION_FILE ] || rm -f etc/$VERSION_FILE

if [ `cat $RPM_INSTALL_PREFIX/share/etc/default-scramv1-version` == "${realversion}" ] ; then
  mkdir -p $RPM_INSTALL_PREFIX/share/man/man1
  cp -f $RPM_INSTALL_PREFIX/share/${pkgdir}/docs/man/man1/scram.1 ${RPM_INSTALL_PREFIX}/share/man/man1/scram.1
fi
