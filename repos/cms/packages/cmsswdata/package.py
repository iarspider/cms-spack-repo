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

class Cmsswdata(BundlePackage):
    """CMS Data metapackage"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    phases = ['install']

    version('40.0')

    depends_on("data-alignment-offlinevalidation")
    depends_on("data-calibcalorimetry-calomiscalibtools")
    depends_on("data-calibcalorimetry-ecaltrivialcondmodules")
    depends_on("data-calibpps-esproducers")
    depends_on("data-calibtracker-sipixelesproducers")
    depends_on("data-calibtracker-sistripdcs")
    depends_on("data-calibration-tools")
    depends_on("data-condformats-jetmetobjects")
    depends_on("data-condtools-siphase2tracker")
    depends_on("data-condtools-sistrip")
    depends_on("data-configuration-generator")
    depends_on("data-dqm-dtmonitorclient")
    depends_on("data-dqm-ecalmonitorclient")
    depends_on("data-dqm-physicshww")
    depends_on("data-dqm-sistripmonitorclient")
    depends_on("data-dataformats-patcandidates")
    depends_on("data-detectordescription-schema")
    depends_on("data-egammaanalysis-electrontools")
    depends_on("data-eventfilter-l1trawtodigi")
    depends_on("data-fwcore-modules")
    depends_on("data-fastsimulation-materialeffects")
    depends_on("data-fastsimulation-trackingrechitproducer")
    depends_on("data-fireworks-geometry")
    depends_on("data-generatorinterface-evtgeninterface")
    depends_on("data-generatorinterface-reggegribovpartonmcinterface")
    depends_on("data-geometry-dtgeometrybuilder")
    depends_on("data-geometry-testreference")
    depends_on("data-hltrigger-jetmet")
    depends_on("data-heterogeneouscore-sonictriton")
    depends_on("data-iopool-input")
    depends_on("data-l1trigger-csctriggerprimitives")
    depends_on("data-l1trigger-dttriggerphase2")
    depends_on("data-l1trigger-l1tcalorimeter")
    depends_on("data-l1trigger-l1tglobal")
    depends_on("data-l1trigger-l1thgcal")
    depends_on("data-l1trigger-l1tmuon")
    depends_on("data-l1trigger-phase2l1particleflow")
    depends_on("data-l1trigger-rpctrigger")
    depends_on("data-l1trigger-trackfindingtmtt")
    depends_on("data-l1trigger-trackfindingtracklet")
    depends_on("data-l1trigger-tracktrigger")
    depends_on("data-magneticfield-engine")
    depends_on("data-magneticfield-interpolation")
    depends_on("data-physicstools-nanoaod")
    depends_on("data-physicstools-patutils")
    depends_on("data-recobtag-ctagging")
    depends_on("data-recobtag-combined")
    depends_on("data-recobtag-secondaryvertex")
    depends_on("data-recobtag-softlepton")
    depends_on("data-recoctpps-totemrplocal")
    depends_on("data-recoecal-egammaclusterproducers")
    depends_on("data-recoegamma-electronidentification")
    depends_on("data-recoegamma-photonidentification")
    depends_on("data-recohgcal-ticl")
    depends_on("data-recohi-hijetalgos")
    depends_on("data-recojets-jetproducers")
    depends_on("data-recolocalcalo-ecaldeadchannelrecoveryalgos")
    depends_on("data-recomet-metpusubtraction")
    depends_on("data-recomtd-timingidtools")
    depends_on("data-recomuon-muonidentification")
    depends_on("data-recomuon-trackerseedgenerator")
    depends_on("data-recoparticleflow-pfblockproducer")
    depends_on("data-recoparticleflow-pfproducer")
    depends_on("data-recoparticleflow-pftracking")
    depends_on("data-recotautag-trainingfiles")
    depends_on("data-recotracker-finaltrackselectors")
    depends_on("data-recotracker-mkfit")
    depends_on("data-recotracker-tkseedgenerator")
    depends_on("data-slhcupgradesimulations-geometry")
    depends_on("data-simg4cms-calo")
    depends_on("data-simg4cms-forward")
    depends_on("data-simg4cms-hgcaltestbeam")
    depends_on("data-simpps-ppspixeldigiproducer")
    depends_on("data-simtracker-sistripdigitizer")
    depends_on("data-simtransport-hectorproducer")
    depends_on("data-simtransport-ppsprotontransport")
    depends_on("data-simtransport-totemrpprotontransportparametrization")
    depends_on("data-validation-geometry")
    depends_on("data-validation-hgcalvalidation")

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
