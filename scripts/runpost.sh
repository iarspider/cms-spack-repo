#!/bin/bash -xe
find $RPM_INSTALL_PREFIX/$SCRAM_ARCH -name 'cmspost.sh' -exec bash -xe {} \;
