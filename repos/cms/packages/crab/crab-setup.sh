#!/bin/bash
#CMSDIST_FILE_REVISION=4
case "X$1Y" in
  XprodY|XdevY|XpreY) CRABCLIENT_TYPE="$1" ;;
  XY ) CRABCLIENT_TYPE="prod" ;;
  * ) 
    echo "ERROR: Invalid CRAB type '$1' provided, valid values are prod, pre and dev."
    echo "Usage: $0 [prod|pre|dev]"
    return 1
    ;;
esac
export CRABCLIENT_TYPE
crab_shared_dir="/root/spack/opt/spack/linux-ubuntu20.04-skylake_avx512/gcc-9.3.0/crab-1.0-oheikktep4lzqlatwz3bfgmawlhdln2e/share/cms/crab/1.0"
export PYTHONPATH="${crab_shared_dir}/lib/${CRABCLIENT_TYPE}${PYTHONPATH:+:$PYTHONPATH}"
export DBS3_CLIENT_ROOT=$(python -c 'from CRABClient import CRABInstallationPath as p; print(p)')
if [ "$(ps -p$$ -ocmd=)" = "zsh" ] ; then
  autoload -U +X compinit && compinit
  autoload -U +X bashcompinit && bashcompinit
fi
complete -F _UseCrab_${CRABCLIENT_TYPE} -o filenames crab
unset crab_shared_dir
