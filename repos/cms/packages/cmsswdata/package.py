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


data_versions = {'40.0': {'data-Alignment-OfflineValidation': 'V00-02-00',
          'data-CalibCalorimetry-CaloMiscalibTools': 'V01-00-00',
          'data-CalibCalorimetry-EcalTrivialCondModules': 'V00-03-00',
          'data-CalibPPS-ESProducers': 'V01-04-00',
          'data-CalibTracker-SiPixelESProducers': 'V02-02-00',
          'data-CalibTracker-SiStripDCS': 'V01-00-00',
          'data-Calibration-Tools': 'V01-00-00',
          'data-CondFormats-JetMETObjects': 'V01-00-03',
          'data-CondTools-SiPhase2Tracker': 'V00-02-00',
          'data-CondTools-SiStrip': 'V00-02-00',
          'data-Configuration-Generator': 'V01-02-00',
          'data-DQM-DTMonitorClient': 'V00-01-00',
          'data-DQM-EcalMonitorClient': 'V00-01-00',
          'data-DQM-PhysicsHWW': 'V01-00-00',
          'data-DQM-SiStripMonitorClient': 'V01-01-00',
          'data-DataFormats-PatCandidates': 'V01-01-00',
          'data-DetectorDescription-Schema': 'V02-03-00',
          'data-EgammaAnalysis-ElectronTools': 'V00-03-01',
          'data-EventFilter-L1TRawToDigi': 'V01-00-00',
          'data-FWCore-Modules': 'V00-01-00',
          'data-FastSimulation-MaterialEffects': 'V05-00-00',
          'data-FastSimulation-TrackingRecHitProducer': 'V01-00-03',
          'data-Fireworks-Geometry': 'V07-06-00',
          'data-GeneratorInterface-EvtGenInterface': 'V02-06-00',
          'data-GeneratorInterface-ReggeGribovPartonMCInterface': 'V00-00-02',
          'data-Geometry-DTGeometryBuilder': 'V00-01-00',
          'data-Geometry-TestReference': 'V00-09-00',
          'data-HLTrigger-JetMET': 'V01-00-00',
          'data-HeterogeneousCore-SonicTriton': 'V00-01-00',
          'data-IOPool-Input': 'V00-01-00',
          'data-L1Trigger-CSCTriggerPrimitives': 'V00-11-00',
          'data-L1Trigger-DTTriggerPhase2': 'V00-02-00',
          'data-L1Trigger-L1TCalorimeter': 'V01-01-00',
          'data-L1Trigger-L1TGlobal': 'V00-00-07',
          'data-L1Trigger-L1THGCal': 'V01-07-00',
          'data-L1Trigger-L1TMuon': 'V01-05-00',
          'data-L1Trigger-Phase2L1ParticleFlow': 'V00-03-00',
          'data-L1Trigger-RPCTrigger': 'V00-15-00',
          'data-L1Trigger-TrackFindingTMTT': 'V00-02-00',
          'data-L1Trigger-TrackFindingTracklet': 'V00-02-00',
          'data-L1Trigger-TrackTrigger': 'V00-01-00',
          'data-MagneticField-Engine': 'V00-01-00',
          'data-MagneticField-Interpolation': 'V01-01-00',
          'data-PhysicsTools-NanoAOD': 'V01-02-00',
          'data-PhysicsTools-PatUtils': 'V00-05-00',
          'data-RecoBTag-CTagging': 'V01-00-03',
          'data-RecoBTag-Combined': 'V01-13-00',
          'data-RecoBTag-SecondaryVertex': 'V02-00-04',
          'data-RecoBTag-SoftLepton': 'V01-00-01',
          'data-RecoCTPPS-TotemRPLocal': 'V00-02-00',
          'data-RecoEcal-EgammaClusterProducers': 'V00-01-00',
          'data-RecoEgamma-ElectronIdentification': 'V01-09-00',
          'data-RecoEgamma-PhotonIdentification': 'V01-04-00',
          'data-RecoHGCal-TICL': 'V00-02-01',
          'data-RecoHI-HiJetAlgos': 'V01-00-01',
          'data-RecoJets-JetProducers': 'V05-14-00',
          'data-RecoLocalCalo-EcalDeadChannelRecoveryAlgos': 'V01-01-00',
          'data-RecoMET-METPUSubtraction': 'V01-01-00',
          'data-RecoMTD-TimingIDTools': 'V00-01-00',
          'data-RecoMuon-MuonIdentification': 'V01-13-00',
          'data-RecoMuon-TrackerSeedGenerator': 'V00-03-00',
          'data-RecoParticleFlow-PFBlockProducer': 'V02-04-02',
          'data-RecoParticleFlow-PFProducer': 'V16-02-00',
          'data-RecoParticleFlow-PFTracking': 'V13-01-00',
          'data-RecoTauTag-TrainingFiles': 'V00-03-00',
          'data-RecoTracker-FinalTrackSelectors': 'V01-03-00',
          'data-RecoTracker-MkFit': 'V00-08-00',
          'data-RecoTracker-TkSeedGenerator': 'V00-02-00',
          'data-SLHCUpgradeSimulations-Geometry': 'V01-00-10',
          'data-SimG4CMS-Calo': 'V03-04-00',
          'data-SimG4CMS-Forward': 'V02-04-00',
          'data-SimG4CMS-HGCalTestBeam': 'V01-00-00',
          'data-SimPPS-PPSPixelDigiProducer': 'V00-00-02',
          'data-SimTracker-SiStripDigitizer': 'V01-01-00',
          'data-SimTransport-HectorProducer': 'V01-00-01',
          'data-SimTransport-PPSProtonTransport': 'V00-02-00',
          'data-SimTransport-TotemRPProtonTransportParametrization': 'V00-01-00',
          'data-Validation-Geometry': 'V00-07-00',
          'data-Validation-HGCalValidation': 'V00-02-00'}}


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
