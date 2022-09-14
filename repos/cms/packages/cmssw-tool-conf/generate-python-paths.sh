#!/bin/bash
echo '<tool name="python-paths" version="1.0">' > $1/tools/selected/python-paths.xml

if [ "${PYTHONPATH}" != "" ] ; then
  py3List=`echo ${PYTHONPATH} | tr ':' '\n'`
  mkdir -p $1/${PYTHON3_LIB_SITE_PACKAGES}
  touch $1/${PYTHON3_LIB_SITE_PACKAGES}/tool-deps.pth
  for pkg in ${py3List} ; do
     echo "adding $pkg"
     echo "$pkg" >> $1/${PYTHON3_LIB_SITE_PACKAGES}/tool-deps.pth
  done
  echo '  <runtime name="PYTHONPATH"  value="$1/'${PYTHON3_LIB_SITE_PACKAGES}'" type="path"/>' >> $1/tools/selected/python-paths.xml
fi

echo '</tool>' >> $1/tools/selected/python-paths.xml
