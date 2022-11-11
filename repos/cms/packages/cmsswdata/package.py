# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from io import StringIO
from string import Template

from spack import *

cmsswdata_xml = Template(
    """<tool name="cmsswdata" version="$v">
    <client>
      <environment name="CMSSWDATA_BASE" default="${prefix}"/>
      <environment name="CMSSW_DATA_PATH" default="$$CMSSWDATA_BASE"/>
      """
)


class Cmsswdata(BundlePackage):
    """CMS Data metapackage"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    phases = ["install"]

    version("40.0")

    depends_on("data-l1trigger-csctriggerprimitives")
    depends_on("data-recomet-metpusubtraction")
    depends_on("data-recoegamma-photonidentification")
    depends_on("data-recobtag-combined")
    depends_on("data-magneticfield-interpolation")
    depends_on("data-recoecal-egammaclusterproducers")
    depends_on("data-l1trigger-tracktrigger")
    depends_on("data-recoegamma-electronidentification")
    depends_on("data-l1trigger-l1tglobal")
    depends_on("data-recotautag-trainingfiles")
    depends_on("data-validation-hgcalvalidation")
    depends_on("data-l1trigger-l1tmuon")
    depends_on("data-recoegamma-egammaphotonproducers")
    depends_on("data-l1triggerconfig-l1tconfigproducers")
    depends_on("data-dqm-integration")
    depends_on("data-recotracker-mkfit")
    depends_on("data-recomuon-trackerseedgenerator")
    depends_on("data-recomuon-muonidentification")
    depends_on("data-dqm-ecalmonitorclient")
    depends_on("data-condtools-sistrip")
    depends_on("data-alignment-offlinevalidation")
    depends_on("data-geometry-testreference")
    depends_on("data-l1trigger-l1thgcal")
    depends_on("data-recoparticleflow-pfproducer")
    depends_on("data-condtools-siphase2tracker")
    depends_on("data-recotracker-finaltrackselectors")
    depends_on("data-calibcalorimetry-calomiscalibtools")
    depends_on("data-fastsimulation-materialeffects")
    depends_on("data-l1trigger-rpctrigger")
    depends_on("data-recoparticleflow-pfblockproducer")
    depends_on("data-simg4cms-calo")
    depends_on("data-validation-geometry")
    depends_on("data-physicstools-nanoaod")
    depends_on("data-calibpps-esproducers")
    depends_on("data-dataformats-patcandidates")
    depends_on("data-l1trigger-trackfindingtracklet")
    depends_on("data-generatorinterface-evtgeninterface")
    depends_on("data-detectordescription-schema")
    depends_on("data-physicstools-patutils")
    depends_on("data-recojets-jetproducers")
    depends_on("data-l1trigger-dttriggerphase2")
    depends_on("data-recohgcal-ticl")
    depends_on("data-egammaanalysis-electrontools")
    depends_on("data-heterogeneouscore-sonictriton")
    depends_on("data-recotracker-tkseedgenerator")
    depends_on("data-calibtracker-sipixelesproducers")
    depends_on("data-geometry-dtgeometrybuilder")
    depends_on("data-l1trigger-trackfindingtmtt")
    depends_on("data-l1trigger-phase2l1particleflow")
    depends_on("data-l1trigger-l1tcalorimeter")
    depends_on("data-simtransport-ppsprotontransport")
    depends_on("data-dqm-sistripmonitorclient")
    depends_on("data-recomtd-timingidtools")
    depends_on("data-configuration-generator")
    depends_on("data-magneticfield-engine")
    depends_on("data-simtracker-sistripdigitizer")
    depends_on("data-simpps-ppspixeldigiproducer")
    depends_on("data-calibcalorimetry-ecaltrivialcondmodules")
    depends_on("data-recolocalcalo-ecaldeadchannelrecoveryalgos")
    depends_on("data-fwcore-modules")
    depends_on("data-iopool-input")
    depends_on("data-recoctpps-totemrplocal")
    depends_on("data-slhcupgradesimulations-geometry")
    depends_on("data-simtransport-totemrpprotontransportparametrization")
    depends_on("data-simg4cms-hgcaltestbeam")
    depends_on("data-fireworks-geometry")
    depends_on("data-simg4cms-forward")
    depends_on("data-generatorinterface-reggegribovpartonmcinterface")
    depends_on("data-calibration-tools")
    depends_on("data-calibtracker-sistripdcs")
    depends_on("data-condformats-jetmetobjects")
    depends_on("data-dqm-dtmonitorclient")
    depends_on("data-dqm-physicshww")
    depends_on("data-eventfilter-l1trawtodigi")
    depends_on("data-fastsimulation-trackingrechitproducer")
    depends_on("data-hltrigger-jetmet")
    depends_on("data-recobtag-ctagging")
    depends_on("data-recobtag-secondaryvertex")
    depends_on("data-recobtag-softlepton")
    depends_on("data-recohi-hijetalgos")
    depends_on("data-recoparticleflow-pftracking")
    depends_on("data-simtransport-hectorproducer")

    def install(self, spec, prefix):
        searchpath_xml = StringIO("")
        mkdirp(prefix.etc.join("scram.d"))

        with open(join_path(prefix.etc.join("scram.d"), "cmsswdata.xml"), "w") as f:
            f.write(
                cmsswdata_xml.substitute({"v": str(spec.version), "prefix": prefix})
            )

            searchpath_xml.write("    </client>\n")
            searchpath_xml.write(
                '    <runtime name="CMSSW_DATA_PATH" value="$CMSSWDATA_BASE" type="path"/>\n'
            )

            for dep in spec.dependencies():
                pkg = dep.package.n
                pkgver = str(dep.version)
                pack = pkg.replace("data-", "").replace("-", "/")
                f.write(f'      <flags CMSSW_DATA_PACKAGE="{pack}/{pkgver}"/>\n')
                searchpath_xml.write(
                    f'    <runtime name="CMSSW_SEARCH_PATH" default="{dep.prefix}" type="path"/>\n'
                )

            f.write(searchpath_xml.getvalue())
            searchpath_xml.close()
            f.write("  </tool>\n")

        install(join_path(os.path.dirname(__file__), "cmspost.sh"), prefix)
        filter_file(
            'BaseTool=""',
            'BaseTool="CMSSW_DATA"',
            prefix.join("cmspost.sh"),
            backup=False,
            stop_at="## END CONFIG",
        )
        lines = []
        for dep in spec.dependencies():
            k = dep.package.n
            v = str(dep.version)
            source = dep.prefix
            if os.environ.get("CMSSW_DATA_LINK", None) is None:
                des_path = f"{k}/{v}"
            else:
                hashed_v = self.spec[k.lower()].format("{version}-{hash}")
                des_path = f"{k}/{hashed_v}"
            pkg_dir = "{1}/{2}".format(*(k.split("-")))
            pkg_data = pkg_dir.split("/", 1)[0]
            lines.append(
                f"if [ ! -e $RPM_INSTALL_PREFIX/share/{des_path}/{pkg_dir} ] ; then"
            )
            lines.append(f"  rm -rf $RPM_INSTALL_PREFIX/share/{des_path}")
            lines.append(f"  mkdir -p $RPM_INSTALL_PREFIX/share/{des_path}")
            lines.append(f"  if [ -L {source}/{pkg_data} ]; then")
            lines.append(
                f"    ln -fs {source}/{pkg_data} $RPM_INSTALL_PREFIX/share/{des_path}/{pkg_dir}"
            )
            lines.append(f"  else")
            lines.append(f"    echo Moving cms/{k}/{v} to share")
            lines.append(
                f"    rsync -aq --no-t --size-only {source}/{pkg_data}/ $RPM_INSTALL_PREFIX/share/{des_path}/{pkg_data}"
            )
            lines.append(f"  fi")
            lines.append(f"fi")
            lines.append(f"if [ ! -L {source}/{pkg_data} ] ; then")
            lines.append(
                f"  rm -rf {source}/{pkg_data} && ln -fs $RPM_INSTALL_PREFIX/share/{des_path}/{pkg_data} {source}/{pkg_data}"
            )
            lines.append(f"fi")

        with open(join_path(prefix, "cmspost.sh"), "a") as f:
            f.write("\n".join(lines))
