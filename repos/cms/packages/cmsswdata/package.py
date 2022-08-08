# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from string import Template
from io import StringIO
import os

cmsswdata_xml = Template("""<tool name="cmsswdata" version="$v">
    <client>
      <environment name="CMSSWDATA_BASE" default="${prefix}"/>
      <environment name="CMSSW_DATA_PATH" default="$$CMSSWDATA_BASE"/>
      """)


data_versions = {'40.0': {'data-l1trigger-l1tglobal': 'V00-02-00',
						'data-recomuon-trackerseedgenerator': 'V00-04-00',
						'data-recomuon-muonidentification': 'V01-14-00',
						'data-dqm-ecalmonitorclient': 'V00-02-00',
						'data-condtools-sistrip': 'V00-02-00',
						'data-recoegamma-photonidentification': 'V01-04-00',
						'data-alignment-offlinevalidation': 'V00-02-00',
						'data-geometry-testreference': 'V00-09-00',
						'data-l1trigger-l1thgcal': 'V01-07-00',
						'data-recobtag-combined': 'V01-13-00',
						'data-recoparticleflow-pfproducer': 'V16-02-00',
						'data-recoecal-egammaclusterproducers': 'V00-01-00',
						'data-condtools-siphase2tracker': 'V00-02-00',
						'data-recotracker-finaltrackselectors': 'V01-03-00',
						'data-recotracker-mkfit': 'V00-08-00',
						'data-recoegamma-electronidentification': 'V01-09-00',
						'data-calibcalorimetry-calomiscalibtools': 'V01-00-00',
						'data-fastsimulation-materialeffects': 'V05-00-00',
						'data-l1trigger-rpctrigger': 'V00-15-00',
						'data-recoparticleflow-pfblockproducer': 'V02-04-02',
						'data-simg4cms-calo': 'V03-04-00',
						'data-validation-geometry': 'V00-07-00',
						'data-validation-hgcalvalidation': 'V00-02-00',
						'data-physicstools-nanoaod': 'V01-02-00',
						'data-recotautag-trainingfiles': 'V00-03-00',
						'data-calibpps-esproducers': 'V01-04-00',
						'data-l1trigger-csctriggerprimitives': 'V00-11-00',
						'data-dataformats-patcandidates': 'V01-01-00',
						'data-l1trigger-trackfindingtracklet': 'V00-02-00',
						'data-generatorinterface-evtgeninterface': 'V02-06-00',
						'data-detectordescription-schema': 'V02-03-00',
						'data-physicstools-patutils': 'V00-05-00',
						'data-recojets-jetproducers': 'V05-14-00',
						'data-l1trigger-l1tmuon': 'V01-05-00',
						'data-l1trigger-dttriggerphase2': 'V00-02-00',
						'data-recohgcal-ticl': 'V00-02-01',
						'data-egammaanalysis-electrontools': 'V00-03-01',
						'data-heterogeneouscore-sonictriton': 'V00-01-00',
						'data-l1trigger-tracktrigger': 'V00-01-00',
						'data-recotracker-tkseedgenerator': 'V00-02-00',
						'data-calibtracker-sipixelesproducers': 'V02-02-00',
						'data-geometry-dtgeometrybuilder': 'V00-01-00',
						'data-l1trigger-trackfindingtmtt': 'V00-02-00',
						'data-l1trigger-phase2l1particleflow': 'V00-03-00',
						'data-l1trigger-l1tcalorimeter': 'V01-01-00',
						'data-simtransport-ppsprotontransport': 'V00-02-00',
						'data-dqm-sistripmonitorclient': 'V01-01-00',
						'data-recomet-metpusubtraction': 'V01-01-00',
						'data-recomtd-timingidtools': 'V00-01-00',
						'data-configuration-generator': 'V01-02-00',
						'data-magneticfield-engine': 'V00-01-00',
						'data-magneticfield-interpolation': 'V01-01-00',
						'data-simtracker-sistripdigitizer': 'V01-01-00',
						'data-simpps-ppspixeldigiproducer': 'V00-00-02',
						'data-calibcalorimetry-ecaltrivialcondmodules': 'V00-03-00',
						'data-recolocalcalo-ecaldeadchannelrecoveryalgos': 'V01-01-00',
						'data-fwcore-modules': 'V00-01-00',
						'data-iopool-input': 'V00-01-00',
						'data-recoctpps-totemrplocal': 'V00-02-00',
						'data-slhcupgradesimulations-geometry': 'V01-00-10',
						'data-simtransport-totemrpprotontransportparametrization': 'V00-01-00',
						'data-simg4cms-hgcaltestbeam': 'V01-00-00',
						'data-fireworks-geometry': 'V07-06-00',
						'data-simg4cms-forward': 'V02-04-00',
						'data-generatorinterface-reggegribovpartonmcinterface': 'V00-00-02',
						'data-calibration-tools': 'V01-00-00',
						'data-calibtracker-sistripdcs': 'V01-00-00',
						'data-condformats-jetmetobjects': 'V01-00-03',
						'data-dqm-dtmonitorclient': 'V00-01-00',
						'data-dqm-physicshww': 'V01-00-00',
						'data-eventfilter-l1trawtodigi': 'V01-00-00',
						'data-fastsimulation-trackingrechitproducer': 'V01-00-03',
						'data-hltrigger-jetmet': 'V01-00-00',
						'data-recobtag-ctagging': 'V01-00-03',
						'data-recobtag-secondaryvertex': 'V02-00-04',
						'data-recobtag-softlepton': 'V01-00-01',
						'data-recohi-hijetalgos': 'V01-00-01',
						'data-recoparticleflow-pftracking': 'V13-01-00',
						'data-simtransport-hectorproducer': 'V01-00-01'}}


class Cmsswdata(BundlePackage):
    """CMS Data metapackage"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    phases = ['install']

    version('40.0')

    for ver, datapkgs in data_versions.items():
        for pkg, pkgver in datapkgs.items():
            depends_on(pkg.lower() + '@' + pkgver, when='@'+ver)

    def install(self, spec, prefix):
        searchpath_xml = StringIO("")
        mkdirp(prefix.etc.join('scram.d'))

        with open(join_path(prefix.etc.join('scram.d'), 'cmsswdata.xml'), 'w') as f:
            f.write(cmsswdata_xml.substitute({'v': str(spec.version), 'prefix': prefix}))

            searchpath_xml.write("    </client>\n")
            searchpath_xml.write('    <runtime name="CMSSW_DATA_PATH" value="$CMSSWDATA_BASE" type="path"/>\n')

            for pkg, pkgver in data_versions[str(spec.version)].items():
                pack = pkg.replace('data-', '').replace('-', '/')
                f.write(f"      <flags CMSSW_DATA_PACKAGE=\"{pack}/{pkgver}\"/>\n")
                searchpath_xml.write(f"    <runtime name=\"CMSSW_SEARCH_PATH\" default=\"{spec[pkg.lower()].prefix}\" type=\"path\"/>\n")

            f.write(searchpath_xml.getvalue())
            searchpath_xml.close()
            f.write("  </tool>\n")

        install(join_path(os.path.dirname(__file__), 'cmspost.sh'), prefix)
        filter_file('BaseTool=""', 'BaseTool="CMSSW_DATA"', prefix.join('cmspost.sh'), backup=False, stop_at='## END CONFIG')
        lines = []
        for k, v in data_versions[str(spec.version)].items():
            source = spec[k.lower()].prefix
            if os.environ.get('CMSSW_DATA_LINK', None) is None:
                des_path = f'cms/{k}/{v}'
            else:
                hashed_v = self.spec[k.lower()].format('{version}-{hash}')
                des_path = f'cms/{k}/{hashed_v}'
            pkg_dir = '{1}/{2}'.format(*(k.split('-')))
            pkg_data = pkg_dir.split('/', 1)[0]
            lines.append(f'if [ ! -e $RPM_INSTALL_PREFIX/share/{des_path}/{pkg_dir} ] ; then')
            lines.append(f'  rm -rf $RPM_INSTALL_PREFIX/share/{des_path}')
            lines.append(f'  mkdir -p $RPM_INSTALL_PREFIX/share/{des_path}')
            lines.append(f'  if [ -L {source}/{pkg_data} ]; then')
            lines.append(f'    ln -fs {source}/{pkg_data} $RPM_INSTALL_PREFIX/share/{des_path}/{pkg_dir}')
            lines.append(f'  else')
            lines.append(f'    echo Moving cms/{k}/{v} to share')
            lines.append(f'    rsync -aq --no-t --size-only {source}/{pkg_data}/ $RPM_INSTALL_PREFIX/share/{des_path}/{pkg_data}')
            lines.append(f'  fi')
            lines.append(f'fi')
            lines.append(f'if [ ! -L {source}/{pkg_data} ] ; then')
            lines.append(f'  rm -rf {source}/{pkg_data} && ln -fs $RPM_INSTALL_PREFIX/share/{des_path}/{pkg_data} {source}/{pkg_data}')
            lines.append(f'fi')

        with open(join_path(prefix, 'cmspost.sh'), 'a') as f:
            f.write('\n'.join(lines))
