#!/bin/sh -e

#PDF sets list is made for:
export lhapdf6setsVersion=6.3.0f

if [ x$1 != x$lhapdf6setsVersion ]; then
  echo lhapdf_makeLinks: lhapdf6sets versions do not coincide
  echo please create this script by running lhapdf_makeScript.sh with correct version
  exit 1
fi

export cvmfspath=/cvmfs/cms.cern.ch/lhapdf/pdfsets/$1
export pdflist="abkm09_3_nlo abkm09_3_nnlo abkm09_4_nlo abkm09_4_nnlo abkm09_5_nlo abkm09_5_nnlo abm11_3n_nlo abm11_3n_nnlo abm11_4n_nlo abm11_4n_nnlo abm11_5n_as_nlo abm11_5n_as_nnlo abm11_5n_nlo abm11_5n_nnlo abm12lhc_3_nnlo abm12lhc_4_nnlo abm12lhc_5_nnlo ABMP15_3_nnlo ABMP15_4_nnlo ABMP15_5_nnlo ABMP16_3_nlo ABMP16_3_nnlo ABMP16_4_nlo ABMP16_4_nnlo ABMP16_5_nlo ABMP16_5_nnlo ABMP16als112_5_nnlo ABMP16als113_5_nnlo ABMP16als114_5_nlo ABMP16als114_5_nnlo ABMP16als115_5_nlo ABMP16als115_5_nnlo ABMP16als116_5_nlo ABMP16als116_5_nnlo ABMP16als117_5_nlo ABMP16als117_5_nnlo ABMP16als118_5_nlo ABMP16als118_5_nnlo ABMP16als119_5_nlo ABMP16als119_5_nnlo ABMP16als120_5_nlo ABMP16als120_5_nnlo ABMP16als121_5_nlo ABMP16als122_5_nlo ABMP16als123_5_nlo ABMP16free_3_nlo ABMP16free_4_nlo ABMP16free_5_nlo ATLAS-epWZ12-EIG ATLAS-epWZ12-VAR ATLAS-epWZ16-EIG ATLAS-epWZ16-THEO ATLAS-epWZ16-VAR ATLAS-epWZtop18-EIG ATLAS-epWZtop18-VAR CJ12max CJ12mid CJ12min CJ15lo CJ15nlo CSKK_nnlo_EIG CSKK_nnlo_THEO CSKK_nnlo_VAR CT09MC1 CT09MC2 CT09MCS CT10 CT10as CT10f3 CT10f4 CT10nlo CT10nlo_as_0112 CT10nlo_as_0113 CT10nlo_as_0114 CT10nlo_as_0115 CT10nlo_as_0116 CT10nlo_as_0117 CT10nlo_as_0118 CT10nlo_as_0119 CT10nlo_as_0120 CT10nlo_as_0121 CT10nlo_as_0122 CT10nlo_as_0123 CT10nlo_as_0124 CT10nlo_as_0125 CT10nlo_as_0126 CT10nlo_as_0127 CT10nlo_nf3 CT10nlo_nf4 CT10nnlo CT10nnlo_as_0110 CT10nnlo_as_0111 CT10nnlo_as_0112 CT10nnlo_as_0113 CT10nnlo_as_0114 CT10nnlo_as_0115 CT10nnlo_as_0116 CT10nnlo_as_0117 CT10nnlo_as_0118 CT10nnlo_as_0119 CT10nnlo_as_0120 CT10nnlo_as_0121 CT10nnlo_as_0122 CT10nnlo_as_0123 CT10nnlo_as_0124 CT10nnlo_as_0125 CT10nnlo_as_0126 CT10nnlo_as_0127 CT10nnlo_as_0128 CT10nnlo_as_0129 CT10nnlo_as_0130 CT10w CT10was CT10wf3 CT10wf4 CT10wnlo CT10wnlo_as_0112 CT10wnlo_as_0113 CT10wnlo_as_0114 CT10wnlo_as_0115 CT10wnlo_as_0116 CT10wnlo_as_0117 CT10wnlo_as_0118 CT10wnlo_as_0119 CT10wnlo_as_0120 CT10wnlo_as_0121 CT10wnlo_as_0122 CT10wnlo_as_0123 CT10wnlo_as_0124 CT10wnlo_as_0125 CT10wnlo_as_0126 CT10wnlo_as_0127 CT10wnlo_nf3 CT10wnlo_nf4 CT14llo CT14llo_NF3 CT14llo_NF4 CT14llo_NF6 CT14lo CT14lo_NF3 CT14lo_NF4 CT14lo_NF6 CT14MC1nlo CT14MC1nnlo CT14MC2nlo CT14MC2nnlo CT14nlo CT14nlo_as_0111 CT14nlo_as_0112 CT14nlo_as_0113 CT14nlo_as_0114 CT14nlo_as_0115 CT14nlo_as_0116 CT14nlo_as_0117 CT14nlo_as_0118 CT14nlo_as_0119 CT14nlo_as_0120 CT14nlo_as_0121 CT14nlo_as_0122 CT14nlo_as_0123 CT14nlo_NF3 CT14nlo_NF4 CT14nlo_NF6 CT14nnlo CT14nnlo_as_0111 CT14nnlo_as_0112 CT14nnlo_as_0113 CT14nnlo_as_0114 CT14nnlo_as_0115 CT14nnlo_as_0116 CT14nnlo_as_0117 CT14nnlo_as_0118 CT14nnlo_as_0119 CT14nnlo_as_0120 CT14nnlo_as_0121 CT14nnlo_as_0122 CT14nnlo_as_0123 CT14nnloIC CT14nnlo_NF3 CT14nnlo_NF4 CT14nnlo_NF6 CT14qed_inc_neutron CT14qed_inc_proton CT14qed_neutron CT14qed_proton CT18ANLO CT18ANLO_as_0110 CT18ANLO_as_0111 CT18ANLO_as_0112 CT18ANLO_as_0113 CT18ANLO_as_0114 CT18ANLO_as_0115 CT18ANLO_as_0116 CT18ANLO_as_0117 CT18ANLO_as_0118 CT18ANLO_as_0119 CT18ANLO_as_0120 CT18ANLO_as_0121 CT18ANLO_as_0122 CT18ANLO_as_0123 CT18ANLO_as_0124 CT18ANNLO CT18ANNLO_as_0110 CT18ANNLO_as_0111 CT18ANNLO_as_0112 CT18ANNLO_as_0113 CT18ANNLO_as_0114 CT18ANNLO_as_0115 CT18ANNLO_as_0116 CT18ANNLO_as_0117 CT18ANNLO_as_0118 CT18ANNLO_as_0119 CT18ANNLO_as_0120 CT18ANNLO_as_0121 CT18ANNLO_as_0122 CT18ANNLO_as_0123 CT18ANNLO_as_0124 CT18NLO CT18NLO_as_0110 CT18NLO_as_0111 CT18NLO_as_0112 CT18NLO_as_0113 CT18NLO_as_0114 CT18NLO_as_0115 CT18NLO_as_0116 CT18NLO_as_0117 CT18NLO_as_0118 CT18NLO_as_0119 CT18NLO_as_0120 CT18NLO_as_0121 CT18NLO_as_0122 CT18NLO_as_0123 CT18NLO_as_0124 CT18NNLO CT18NNLO_as_0110 CT18NNLO_as_0111 CT18NNLO_as_0112 CT18NNLO_as_0113 CT18NNLO_as_0114 CT18NNLO_as_0115 CT18NNLO_as_0116 CT18NNLO_as_0117 CT18NNLO_as_0118 CT18NNLO_as_0119 CT18NNLO_as_0120 CT18NNLO_as_0121 CT18NNLO_as_0122 CT18NNLO_as_0123 CT18NNLO_as_0124 CT18XNLO CT18XNLO_as_0110 CT18XNLO_as_0111 CT18XNLO_as_0112 CT18XNLO_as_0113 CT18XNLO_as_0114 CT18XNLO_as_0115 CT18XNLO_as_0116 CT18XNLO_as_0117 CT18XNLO_as_0118 CT18XNLO_as_0119 CT18XNLO_as_0120 CT18XNLO_as_0121 CT18XNLO_as_0122 CT18XNLO_as_0123 CT18XNLO_as_0124 CT18XNNLO CT18XNNLO_as_0110 CT18XNNLO_as_0111 CT18XNNLO_as_0112 CT18XNNLO_as_0113 CT18XNNLO_as_0114 CT18XNNLO_as_0115 CT18XNNLO_as_0116 CT18XNNLO_as_0117 CT18XNNLO_as_0118 CT18XNNLO_as_0119 CT18XNNLO_as_0120 CT18XNNLO_as_0121 CT18XNNLO_as_0122 CT18XNNLO_as_0123 CT18XNNLO_as_0124 CT18ZNLO CT18ZNLO_as_0110 CT18ZNLO_as_0111 CT18ZNLO_as_0112 CT18ZNLO_as_0113 CT18ZNLO_as_0114 CT18ZNLO_as_0115 CT18ZNLO_as_0116 CT18ZNLO_as_0117 CT18ZNLO_as_0118 CT18ZNLO_as_0119 CT18ZNLO_as_0120 CT18ZNLO_as_0121 CT18ZNLO_as_0122 CT18ZNLO_as_0123 CT18ZNLO_as_0124 CT18ZNNLO CT18ZNNLO_as_0110 CT18ZNNLO_as_0111 CT18ZNNLO_as_0112 CT18ZNNLO_as_0113 CT18ZNNLO_as_0114 CT18ZNNLO_as_0115 CT18ZNNLO_as_0116 CT18ZNNLO_as_0117 CT18ZNNLO_as_0118 CT18ZNNLO_as_0119 CT18ZNNLO_as_0120 CT18ZNNLO_as_0121 CT18ZNNLO_as_0122 CT18ZNNLO_as_0123 CT18ZNNLO_as_0124 cteq61 cteq66 cteq6l1 EPPS16nlo_CT14nlo_Ag108 EPPS16nlo_CT14nlo_Al27 EPPS16nlo_CT14nlo_Au197 EPPS16nlo_CT14nlo_Be9 EPPS16nlo_CT14nlo_C12 EPPS16nlo_CT14nlo_Ca40 EPPS16nlo_CT14nlo_Cu64 EPPS16nlo_CT14nlo_Fe56 EPPS16nlo_CT14nlo_He4 EPPS16nlo_CT14nlo_Li6 EPPS16nlo_CT14nlo_Pb208 EPPS16nlo_CT14nlo_Pt195 EPPS16nlo_CT14nlo_Sn119 EPPS16nlo_CT14nlo_W184 GKG18_DPDF_FitA_LO GKG18_DPDF_FitA_NLO GKG18_DPDF_FitB_LO GKG18_DPDF_FitB_NLO GRVPI0 GRVPI1 H1PDF2017 HERAPDF15LO_EIG HERAPDF15NLO_ALPHAS HERAPDF15NLO_EIG HERAPDF15NLO_VAR HERAPDF15NNLO_ALPHAS HERAPDF15NNLO_EIG HERAPDF15NNLO_VAR HERAPDF20_AG_NLO_EIG HERAPDF20_AG_NNLO_EIG HERAPDF20_HiQ2_NLO_EIG HERAPDF20_HiQ2_NLO_VAR HERAPDF20_HiQ2_NNLO_EIG HERAPDF20_HiQ2_NNLO_VAR HERAPDF20_Jets_NLO_EIG HERAPDF20_Jets_NLO_VAR_Duv HERAPDF20_Jets_NLO_VAR_fsdn HERAPDF20_Jets_NLO_VAR_fshdn HERAPDF20_Jets_NLO_VAR_fshup HERAPDF20_Jets_NLO_VAR_fsup HERAPDF20_Jets_NLO_VAR_haddn HERAPDF20_Jets_NLO_VAR_hadup HERAPDF20_Jets_NLO_VAR_mbdn HERAPDF20_Jets_NLO_VAR_mbup HERAPDF20_Jets_NLO_VAR_mcdn HERAPDF20_Jets_NLO_VAR_mcup HERAPDF20_Jets_NLO_VAR_q0dn HERAPDF20_Jets_NLO_VAR_q0up HERAPDF20_Jets_NLO_VAR_q2mdn HERAPDF20_Jets_NLO_VAR_q2mup HERAPDF20_LO_EIG HERAPDF20_NLO_ALPHAS_110 HERAPDF20_NLO_ALPHAS_111 HERAPDF20_NLO_ALPHAS_112 HERAPDF20_NLO_ALPHAS_113 HERAPDF20_NLO_ALPHAS_114 HERAPDF20_NLO_ALPHAS_115 HERAPDF20_NLO_ALPHAS_116 HERAPDF20_NLO_ALPHAS_117 HERAPDF20_NLO_ALPHAS_118 HERAPDF20_NLO_ALPHAS_119 HERAPDF20_NLO_ALPHAS_120 HERAPDF20_NLO_ALPHAS_121 HERAPDF20_NLO_ALPHAS_122 HERAPDF20_NLO_ALPHAS_123 HERAPDF20_NLO_ALPHAS_124 HERAPDF20_NLO_ALPHAS_125 HERAPDF20_NLO_ALPHAS_126 HERAPDF20_NLO_ALPHAS_127 HERAPDF20_NLO_ALPHAS_128 HERAPDF20_NLO_ALPHAS_129 HERAPDF20_NLO_ALPHAS_130 HERAPDF20_NLO_EIG HERAPDF20_NLO_FF3A_EIG HERAPDF20_NLO_FF3A_VAR HERAPDF20_NLO_FF3B_EIG HERAPDF20_NLO_FF3B_VAR HERAPDF20_NLO_VAR HERAPDF20_NNLO_ALPHAS_110 HERAPDF20_NNLO_ALPHAS_111 HERAPDF20_NNLO_ALPHAS_112 HERAPDF20_NNLO_ALPHAS_113 HERAPDF20_NNLO_ALPHAS_114 HERAPDF20_NNLO_ALPHAS_115 HERAPDF20_NNLO_ALPHAS_116 HERAPDF20_NNLO_ALPHAS_117 HERAPDF20_NNLO_ALPHAS_118 HERAPDF20_NNLO_ALPHAS_119 HERAPDF20_NNLO_ALPHAS_120 HERAPDF20_NNLO_ALPHAS_121 HERAPDF20_NNLO_ALPHAS_122 HERAPDF20_NNLO_ALPHAS_123 HERAPDF20_NNLO_ALPHAS_124 HERAPDF20_NNLO_ALPHAS_125 HERAPDF20_NNLO_ALPHAS_126 HERAPDF20_NNLO_ALPHAS_127 HERAPDF20_NNLO_ALPHAS_128 HERAPDF20_NNLO_ALPHAS_129 HERAPDF20_NNLO_ALPHAS_130 HERAPDF20_NNLO_EIG HERAPDF20_NNLO_VAR JAM19FF_kaon_nlo JAM19FF_pion_nlo JAM19PDF_proton_nlo JAM20-SIDIS_FF_hadron_nlo JAM20-SIDIS_FF_kaon_nlo JAM20-SIDIS_FF_pion_nlo JAM20-SIDIS_PDF_proton_nlo JR14NLO08FF JR14NLO08VF JR14NNLO08FF JR14NNLO08VF JR14NNLO20FF JR14NNLO20VF LUXlep-NNPDF31_nlo_as_0118_luxqed LUXqed17_plus_PDF4LHC15_nnlo_100 LUXqed17_plus_PDF4LHC15_nnlo_30 LUXqed_plus_PDF4LHC15_nnlo_100 MAPFF10NLOPIm MAPFF10NLOPIp MAPFF10NLOPIsum METAv10LHC METAv10LHCas0116 METAv10LHCas0120 METAv10LHCH METAv10LHCHfull MMHT2014lo68cl MMHT2014lo_asmzsmallrange MMHT2014nlo68cl MMHT2014nlo68clas118 MMHT2014nlo68clas118_nf3 MMHT2014nlo68clas118_nf4 MMHT2014nlo68clas118_nf4as5 MMHT2014nlo68cl_nf3 MMHT2014nlo68cl_nf4 MMHT2014nlo68cl_nf4as5 MMHT2014nloas118_mbrange_nf3 MMHT2014nloas118_mbrange_nf4 MMHT2014nloas118_mbrange_nf5 MMHT2014nloas118_mcrange_nf3 MMHT2014nloas118_mcrange_nf4 MMHT2014nloas118_mcrange_nf5 MMHT2014nlo_asmzlargerange MMHT2014nlo_asmzsmallrange MMHT2014nlo_asmzsmallrange_nf3 MMHT2014nlo_asmzsmallrange_nf4 MMHT2014nlo_mbrange_nf3 MMHT2014nlo_mbrange_nf4 MMHT2014nlo_mbrange_nf5 MMHT2014nlo_mcrange_nf3 MMHT2014nlo_mcrange_nf4 MMHT2014nlo_mcrange_nf5 MMHT2014nnlo68cl MMHT2014nnlo68cl_nf3 MMHT2014nnlo68cl_nf4 MMHT2014nnlo68cl_nf4as5 MMHT2014nnlo_asmzlargerange MMHT2014nnlo_asmzsmallrange MMHT2014nnlo_asmzsmallrange_nf3 MMHT2014nnlo_asmzsmallrange_nf4 MMHT2014nnlo_mbrange_nf3 MMHT2014nnlo_mbrange_nf4 MMHT2014nnlo_mbrange_nf5 MMHT2014nnlo_mcrange_nf3 MMHT2014nnlo_mcrange_nf4 MMHT2014nnlo_mcrange_nf5 MMHT2015qed_nlo MMHT2015qed_nlo_elastic MMHT2015qed_nlo_inelastic MMHT2015qed_nnlo MMHT2015qed_nnlo_elastic MMHT2015qed_nnlo_inelastic MRST2004qed_neutron MRST2004qed_proton MRST2007lomod MRSTMCal MSHT20lo_as130 MSHT20nlo_as118 MSHT20nlo_as120 MSHT20nlo_as_smallrange MSHT20nnlo_as118 MSHT20nnlo_as_smallrange MSTW2008CPdeutnlo68cl MSTW2008CPdeutnnlo68cl MSTW2008lo68cl MSTW2008lo68cl_nf3 MSTW2008lo68cl_nf4 MSTW2008lo68cl_nf4as5 MSTW2008lo90cl MSTW2008lo90cl_nf3 MSTW2008lo90cl_nf4 MSTW2008lo90cl_nf4as5 MSTW2008nlo68cl MSTW2008nlo68cl_asmz-68cl MSTW2008nlo68cl_asmz+68cl MSTW2008nlo68cl_asmz-68clhalf MSTW2008nlo68cl_asmz+68clhalf MSTW2008nlo68cl_nf3 MSTW2008nlo68cl_nf4 MSTW2008nlo68cl_nf4as5 MSTW2008nlo90cl MSTW2008nlo90cl_asmz-90cl MSTW2008nlo90cl_asmz+90cl MSTW2008nlo90cl_asmz-90clhalf MSTW2008nlo90cl_asmz+90clhalf MSTW2008nlo90cl_nf3 MSTW2008nlo90cl_nf4 MSTW2008nlo90cl_nf4as5 MSTW2008nlo_asmzrange MSTW2008nlo_mbrange MSTW2008nlo_mbrange_nf4 MSTW2008nlo_mcrange MSTW2008nlo_mcrange_fixasmz MSTW2008nlo_mcrange_fixasmz_nf3 MSTW2008nlo_mcrange_nf3 MSTW2008nnlo68cl MSTW2008nnlo68cl_asmz-68cl MSTW2008nnlo68cl_asmz+68cl MSTW2008nnlo68cl_asmz-68clhalf MSTW2008nnlo68cl_asmz+68clhalf MSTW2008nnlo68cl_nf3 MSTW2008nnlo68cl_nf4 MSTW2008nnlo68cl_nf4as5 MSTW2008nnlo90cl MSTW2008nnlo90cl_asmz-90cl MSTW2008nnlo90cl_asmz+90cl MSTW2008nnlo90cl_asmz-90clhalf MSTW2008nnlo90cl_asmz+90clhalf MSTW2008nnlo90cl_nf3 MSTW2008nnlo90cl_nf4 MSTW2008nnlo90cl_nf4as5 MSTW2008nnlo_asmzrange MSTW2008nnlo_mbrange MSTW2008nnlo_mbrange_nf4 MSTW2008nnlo_mcrange MSTW2008nnlo_mcrange_fixasmz MSTW2008nnlo_mcrange_fixasmz_nf3 MSTW2008nnlo_mcrange_nf3 nCTEQ15_108_54 nCTEQ15_1_1 nCTEQ15_119_59 nCTEQ15_12_6 nCTEQ15_131_54 nCTEQ15_14_7 nCTEQ15_184_74 nCTEQ15_197_79 nCTEQ15_197_98 nCTEQ15_20_10 nCTEQ15_207_103 nCTEQ15_208_82 nCTEQ15_27_13 nCTEQ15_3_2 nCTEQ15_40_18 nCTEQ15_40_20 nCTEQ15_4_2 nCTEQ15_56_26 nCTEQ15_6_3 nCTEQ15_64_32 nCTEQ15_7_3 nCTEQ15_84_42 nCTEQ15_9_4 nCTEQ15FullNuc_108_54 nCTEQ15FullNuc_1_1 nCTEQ15FullNuc_119_59 nCTEQ15FullNuc_12_6 nCTEQ15FullNuc_131_54 nCTEQ15FullNuc_14_7 nCTEQ15FullNuc_184_74 nCTEQ15FullNuc_197_79 nCTEQ15FullNuc_197_98 nCTEQ15FullNuc_20_10 nCTEQ15FullNuc_207_103 nCTEQ15FullNuc_208_82 nCTEQ15FullNuc_27_13 nCTEQ15FullNuc_3_2 nCTEQ15FullNuc_40_18 nCTEQ15FullNuc_40_20 nCTEQ15FullNuc_4_2 nCTEQ15FullNuc_56_26 nCTEQ15FullNuc_6_3 nCTEQ15FullNuc_64_32 nCTEQ15FullNuc_7_3 nCTEQ15FullNuc_84_42 nCTEQ15FullNuc_9_4 nCTEQ15np_108_54 nCTEQ15np_1_1 nCTEQ15np_119_59 nCTEQ15np_12_6 nCTEQ15np_131_54 nCTEQ15np_14_7 nCTEQ15np_184_74 nCTEQ15np_197_79 nCTEQ15np_197_98 nCTEQ15np_20_10 nCTEQ15np_207_103 nCTEQ15np_208_82 nCTEQ15np_27_13 nCTEQ15np_3_2 nCTEQ15np_40_18 nCTEQ15np_40_20 nCTEQ15np_4_2 nCTEQ15np_56_26 nCTEQ15np_6_3 nCTEQ15np_64_32 nCTEQ15np_7_3 nCTEQ15np_84_42 nCTEQ15np_9_4 nCTEQ15npFullNuc_108_54 nCTEQ15npFullNuc_1_1 nCTEQ15npFullNuc_119_59 nCTEQ15npFullNuc_12_6 nCTEQ15npFullNuc_131_54 nCTEQ15npFullNuc_14_7 nCTEQ15npFullNuc_184_74 nCTEQ15npFullNuc_197_79 nCTEQ15npFullNuc_197_98 nCTEQ15npFullNuc_20_10 nCTEQ15npFullNuc_207_103 nCTEQ15npFullNuc_208_82 nCTEQ15npFullNuc_27_13 nCTEQ15npFullNuc_3_2 nCTEQ15npFullNuc_40_18 nCTEQ15npFullNuc_40_20 nCTEQ15npFullNuc_4_2 nCTEQ15npFullNuc_56_26 nCTEQ15npFullNuc_6_3 nCTEQ15npFullNuc_64_32 nCTEQ15npFullNuc_7_3 nCTEQ15npFullNuc_84_42 nCTEQ15npFullNuc_9_4 NNFF10_KAm_lo NNFF10_KAm_nlo NNFF10_KAm_nnlo NNFF10_KAp_lo NNFF10_KAp_nlo NNFF10_KAp_nnlo NNFF10_KAsum_lo NNFF10_KAsum_nlo NNFF10_KAsum_nnlo NNFF10_PIm_lo NNFF10_PIm_nlo NNFF10_PIm_nnlo NNFF10_PIp_lo NNFF10_PIp_nlo NNFF10_PIp_nnlo NNFF10_PIsum_lo NNFF10_PIsum_nlo NNFF10_PIsum_nnlo NNFF10_PRm_lo NNFF10_PRm_nlo NNFF10_PRm_nnlo NNFF10_PRp_lo NNFF10_PRp_nlo NNFF10_PRp_nnlo NNFF10_PRsum_lo NNFF10_PRsum_nlo NNFF10_PRsum_nnlo NNFF11_HadronSum_nlo nNNPDF10_nlo_as_0118_Ag108 nNNPDF10_nlo_as_0118_Al27 nNNPDF10_nlo_as_0118_Au197 nNNPDF10_nlo_as_0118_Be9 nNNPDF10_nlo_as_0118_C12 nNNPDF10_nlo_as_0118_Ca40 nNNPDF10_nlo_as_0118_Cu64 nNNPDF10_nlo_as_0118_D2 nNNPDF10_nlo_as_0118_Fe56 nNNPDF10_nlo_as_0118_He4 nNNPDF10_nlo_as_0118_Li6 nNNPDF10_nlo_as_0118_N1 nNNPDF10_nlo_as_0118_N14 nNNPDF10_nlo_as_0118_Pb208 nNNPDF10_nlo_as_0118_Sn119 nNNPDF10_nlo_as_0118_Xe131 nNNPDF10_nnlo_as_0118_Ag108 nNNPDF10_nnlo_as_0118_Al27 nNNPDF10_nnlo_as_0118_Au197 nNNPDF10_nnlo_as_0118_Be9 nNNPDF10_nnlo_as_0118_C12 nNNPDF10_nnlo_as_0118_Ca40 nNNPDF10_nnlo_as_0118_Cu64 nNNPDF10_nnlo_as_0118_D2 nNNPDF10_nnlo_as_0118_Fe56 nNNPDF10_nnlo_as_0118_He4 nNNPDF10_nnlo_as_0118_Li6 nNNPDF10_nnlo_as_0118_N1 nNNPDF10_nnlo_as_0118_N14 nNNPDF10_nnlo_as_0118_Pb208 nNNPDF10_nnlo_as_0118_Sn119 nNNPDF10_nnlo_as_0118_Xe131 nNNPDF20_nlo_as_0118_Ag108 nNNPDF20_nlo_as_0118_Al27 nNNPDF20_nlo_as_0118_Au197 nNNPDF20_nlo_as_0118_Be9 nNNPDF20_nlo_as_0118_C12 nNNPDF20_nlo_as_0118_Ca40 nNNPDF20_nlo_as_0118_Cu64 nNNPDF20_nlo_as_0118_D2 nNNPDF20_nlo_as_0118_Fe56 nNNPDF20_nlo_as_0118_He4 nNNPDF20_nlo_as_0118_Li6 nNNPDF20_nlo_as_0118_N1 nNNPDF20_nlo_as_0118_N14 nNNPDF20_nlo_as_0118_O16 nNNPDF20_nlo_as_0118_Pb208 nNNPDF20_nlo_as_0118_Sn119 nNNPDF20_nlo_as_0118_W184 nNNPDF20_nlo_as_0118_Xe131 NNPDF21_lo_as_0119_100 NNPDF21_lo_as_0130_100 NNPDF21_lostar_as_0119_100 NNPDF21_lostar_as_0130_100 NNPDF23_lo_as_0119_qed NNPDF23_lo_as_0130_qed NNPDF23_nlo_as_0114 NNPDF23_nlo_as_0115 NNPDF23_nlo_as_0116 NNPDF23_nlo_as_0116_mc NNPDF23_nlo_as_0117 NNPDF23_nlo_as_0117_mc NNPDF23_nlo_as_0117_qed NNPDF23_nlo_as_0117_qed_neutron NNPDF23_nlo_as_0118 NNPDF23_nlo_as_0118_mc NNPDF23_nlo_as_0118_qed NNPDF23_nlo_as_0118_qed_neutron NNPDF23_nlo_as_0119 NNPDF23_nlo_as_0119_mc NNPDF23_nlo_as_0119_qed NNPDF23_nlo_as_0119_qed_mc NNPDF23_nlo_as_0119_qed_neutron NNPDF23_nlo_as_0120 NNPDF23_nlo_as_0120_mc NNPDF23_nlo_as_0121 NNPDF23_nlo_as_0122 NNPDF23_nlo_as_0123 NNPDF23_nlo_as_0124 NNPDF23_nlo_collider_as_0116 NNPDF23_nlo_collider_as_0117 NNPDF23_nlo_collider_as_0118 NNPDF23_nlo_collider_as_0119 NNPDF23_nlo_collider_as_0120 NNPDF23_nlo_FFN_NF4_as_0116 NNPDF23_nlo_FFN_NF4_as_0116_mc NNPDF23_nlo_FFN_NF4_as_0117 NNPDF23_nlo_FFN_NF4_as_0117_mc NNPDF23_nlo_FFN_NF4_as_0118 NNPDF23_nlo_FFN_NF4_as_0118_mc NNPDF23_nlo_FFN_NF4_as_0119 NNPDF23_nlo_FFN_NF4_as_0119_mc NNPDF23_nlo_FFN_NF4_as_0120 NNPDF23_nlo_FFN_NF4_as_0120_mc NNPDF23_nlo_FFN_NF5_as_0116 NNPDF23_nlo_FFN_NF5_as_0116_mc NNPDF23_nlo_FFN_NF5_as_0117 NNPDF23_nlo_FFN_NF5_as_0117_mc NNPDF23_nlo_FFN_NF5_as_0118 NNPDF23_nlo_FFN_NF5_as_0118_mc NNPDF23_nlo_FFN_NF5_as_0119 NNPDF23_nlo_FFN_NF5_as_0119_mc NNPDF23_nlo_FFN_NF5_as_0120 NNPDF23_nlo_FFN_NF5_as_0120_mc NNPDF23_nlo_noLHC_as_0116 NNPDF23_nlo_noLHC_as_0117 NNPDF23_nlo_noLHC_as_0118 NNPDF23_nlo_noLHC_as_0119 NNPDF23_nlo_noLHC_as_0120 NNPDF23_nnlo_as_0114 NNPDF23_nnlo_as_0115 NNPDF23_nnlo_as_0116 NNPDF23_nnlo_as_0117 NNPDF23_nnlo_as_0117_qed NNPDF23_nnlo_as_0117_qed_neutron NNPDF23_nnlo_as_0118 NNPDF23_nnlo_as_0118_qed NNPDF23_nnlo_as_0118_qed_neutron NNPDF23_nnlo_as_0119 NNPDF23_nnlo_as_0119_qed NNPDF23_nnlo_as_0119_qed_mc NNPDF23_nnlo_as_0119_qed_neutron NNPDF23_nnlo_as_0120 NNPDF23_nnlo_as_0121 NNPDF23_nnlo_as_0122 NNPDF23_nnlo_as_0123 NNPDF23_nnlo_as_0124 NNPDF23_nnlo_collider_as_0116 NNPDF23_nnlo_collider_as_0117 NNPDF23_nnlo_collider_as_0118 NNPDF23_nnlo_collider_as_0119 NNPDF23_nnlo_collider_as_0120 NNPDF23_nnlo_FFN_NF4_as_0116 NNPDF23_nnlo_FFN_NF4_as_0117 NNPDF23_nnlo_FFN_NF4_as_0118 NNPDF23_nnlo_FFN_NF4_as_0119 NNPDF23_nnlo_FFN_NF4_as_0120 NNPDF23_nnlo_FFN_NF5_as_0116 NNPDF23_nnlo_FFN_NF5_as_0117 NNPDF23_nnlo_FFN_NF5_as_0118 NNPDF23_nnlo_FFN_NF5_as_0119 NNPDF23_nnlo_FFN_NF5_as_0120 NNPDF23_nnlo_noLHC_as_0116 NNPDF23_nnlo_noLHC_as_0117 NNPDF23_nnlo_noLHC_as_0118 NNPDF23_nnlo_noLHC_as_0119 NNPDF23_nnlo_noLHC_as_0120 NNPDF30_lo_as_0118 NNPDF30_lo_as_0118_nf_3 NNPDF30_lo_as_0118_nf_4 NNPDF30_lo_as_0118_nf_6 NNPDF30_lo_as_0130 NNPDF30_lo_as_0130_nf_3 NNPDF30_lo_as_0130_nf_4 NNPDF30_lo_as_0130_nf_6 NNPDF30_nlo_as_0115 NNPDF30_nlo_as_0115_nf_3 NNPDF30_nlo_as_0115_nf_4 NNPDF30_nlo_as_0115_nf_6 NNPDF30_nlo_as_0117 NNPDF30_nlo_as_0117_atlas NNPDF30_nlo_as_0117_cms NNPDF30_nlo_as_0117_cons NNPDF30_nlo_as_0117_hera NNPDF30_nlo_as_0117_nf_3 NNPDF30_nlo_as_0117_nf_4 NNPDF30_nlo_as_0117_nf_6 NNPDF30_nlo_as_0117_nojet NNPDF30_nlo_as_0117_nolhc NNPDF30_nlo_as_0118 NNPDF30_nlo_as_0118_1000 NNPDF30_nlo_as_0118_atlas NNPDF30_nlo_as_0118_cms NNPDF30_nlo_as_0118_cons NNPDF30_nlo_as_0118_hera NNPDF30_nlo_as_0118_hera_1000 NNPDF30_nlo_as_0118_hessian NNPDF30_nlo_as_0118_mc NNPDF30_nlo_as_0118_nf_3 NNPDF30_nlo_as_0118_nf_4 NNPDF30_nlo_as_0118_nf_6 NNPDF30_nlo_as_0118_nojet NNPDF30_nlo_as_0118_nolhc NNPDF30_nlo_as_0118_nolhc_1000 NNPDF30_nlo_as_0119 NNPDF30_nlo_as_0119_atlas NNPDF30_nlo_as_0119_cms NNPDF30_nlo_as_0119_cons NNPDF30_nlo_as_0119_hera NNPDF30_nlo_as_0119_nf_3 NNPDF30_nlo_as_0119_nf_4 NNPDF30_nlo_as_0119_nf_6 NNPDF30_nlo_as_0119_nojet NNPDF30_nlo_as_0119_nolhc NNPDF30_nlo_as_0121 NNPDF30_nlo_as_0121_nf_3 NNPDF30_nlo_as_0121_nf_4 NNPDF30_nlo_as_0121_nf_6 NNPDF30_nlo_nf_4_pdfas NNPDF30_nlo_nf_5_pdfas NNPDF30_nnlo_as_0115 NNPDF30_nnlo_as_0115_nf_3 NNPDF30_nnlo_as_0115_nf_4 NNPDF30_nnlo_as_0115_nf_6 NNPDF30_nnlo_as_0117 NNPDF30_nnlo_as_0117_atlas NNPDF30_nnlo_as_0117_cms NNPDF30_nnlo_as_0117_cons NNPDF30_nnlo_as_0117_hera NNPDF30_nnlo_as_0117_nf_3 NNPDF30_nnlo_as_0117_nf_4 NNPDF30_nnlo_as_0117_nf_6 NNPDF30_nnlo_as_0117_nojet NNPDF30_nnlo_as_0117_nolhc NNPDF30_nnlo_as_0118 NNPDF30_nnlo_as_0118_1000 NNPDF30_nnlo_as_0118_atlas NNPDF30_nnlo_as_0118_cms NNPDF30_nnlo_as_0118_cons NNPDF30_nnlo_as_0118_hera NNPDF30_nnlo_as_0118_hera_1000 NNPDF30_nnlo_as_0118_hessian NNPDF30_nnlo_as_0118_mc NNPDF30_nnlo_as_0118_nf_3 NNPDF30_nnlo_as_0118_nf_4 NNPDF30_nnlo_as_0118_nf_6 NNPDF30_nnlo_as_0118_nojet NNPDF30_nnlo_as_0118_nolhc NNPDF30_nnlo_as_0118_nolhc_1000 NNPDF30_nnlo_as_0119 NNPDF30_nnlo_as_0119_atlas NNPDF30_nnlo_as_0119_cms NNPDF30_nnlo_as_0119_cons NNPDF30_nnlo_as_0119_hera NNPDF30_nnlo_as_0119_nf_3 NNPDF30_nnlo_as_0119_nf_4 NNPDF30_nnlo_as_0119_nf_6 NNPDF30_nnlo_as_0119_nojet NNPDF30_nnlo_as_0119_nolhc NNPDF30_nnlo_as_0121 NNPDF30_nnlo_as_0121_nf_3 NNPDF30_nnlo_as_0121_nf_4 NNPDF30_nnlo_as_0121_nf_6 NNPDF30_nnlo_nf_4_pdfas NNPDF30_nnlo_nf_5_pdfas NNPDF31_lo_as_0118 NNPDF31_lo_as_0130 NNPDF31_lo_pch_as_0118 NNPDF31_lo_pch_as_0130 NNPDF31_nlo_as_0116 NNPDF31_nlo_as_0118 NNPDF31_nlo_as_0118_1000 NNPDF31_nlo_as_0118_C1p6 NNPDF31_nlo_as_0118_hessian NNPDF31_nlo_as_0118_luxqed NNPDF31_nlo_as_0118_mc NNPDF31_nlo_as_0118_nf_4 NNPDF31_nlo_as_0118_nf_6 NNPDF31_nlo_as_0120 NNPDF31_nlo_hessian_pdfas NNPDF31_nlo_pch_as_0116 NNPDF31_nlo_pch_as_0118 NNPDF31_nlo_pch_as_0118_1000 NNPDF31_nlo_pch_as_0118_hessian NNPDF31_nlo_pch_as_0118_mc NNPDF31_nlo_pch_as_0118_nf_3 NNPDF31_nlo_pch_as_0118_nf_4 NNPDF31_nlo_pch_as_0118_nf_6 NNPDF31_nlo_pch_as_0120 NNPDF31_nlo_pch_hessian_pdfas NNPDF31_nlo_pch_pdfas NNPDF31_nlo_pdfas NNPDF31_nnlo_as_0108 NNPDF31_nnlo_as_0110 NNPDF31_nnlo_as_0112 NNPDF31_nnlo_as_0114 NNPDF31_nnlo_as_0116 NNPDF31_nnlo_as_0117 NNPDF31_nnlo_as_0118 NNPDF31_nnlo_as_0118_1000 NNPDF31_nnlo_as_0118_CMSW1 NNPDF31_nnlo_as_0118_CMSW1_hessian_100 NNPDF31_nnlo_as_0118_CMSW2 NNPDF31_nnlo_as_0118_CMSW2_hessian_100 NNPDF31_nnlo_as_0118_CMSW3 NNPDF31_nnlo_as_0118_CMSW3_hessian_100 NNPDF31_nnlo_as_0118_CMSW4 NNPDF31_nnlo_as_0118_CMSW4_hessian_100 NNPDF31_nnlo_as_0118_collider NNPDF31_nnlo_as_0118_hessian NNPDF31_nnlo_as_0118_luxqed NNPDF31_nnlo_as_0118_mc NNPDF31_nnlo_as_0118_mc_138 NNPDF31_nnlo_as_0118_mc_164 NNPDF31_nnlo_as_0118_mc_hessian_pdfas NNPDF31_nnlo_as_0118_nf_4 NNPDF31_nnlo_as_0118_nf_4_mc_hessian NNPDF31_nnlo_as_0118_nf_6 NNPDF31_nnlo_as_0118_nojets NNPDF31_nnlo_as_0118_noLHC NNPDF31_nnlo_as_0118_notop NNPDF31_nnlo_as_0118_noZpt NNPDF31_nnlo_as_0118_proton NNPDF31_nnlo_as_0118_wEMC NNPDF31_nnlo_as_0119 NNPDF31_nnlo_as_0120 NNPDF31_nnlo_as_0122 NNPDF31_nnlo_as_0124 NNPDF31_nnlo_hessian_pdfas NNPDF31_nnlo_pch_as_0116 NNPDF31_nnlo_pch_as_0118 NNPDF31_nnlo_pch_as_0118_1000 NNPDF31_nnlo_pch_as_0118_hessian NNPDF31_nnlo_pch_as_0118_mc NNPDF31_nnlo_pch_as_0118_mc_138 NNPDF31_nnlo_pch_as_0118_mc_164 NNPDF31_nnlo_pch_as_0118_nf_3 NNPDF31_nnlo_pch_as_0118_nf_4 NNPDF31_nnlo_pch_as_0118_nf_6 NNPDF31_nnlo_pch_as_0120 NNPDF31_nnlo_pch_hessian_pdfas NNPDF31_nnlo_pch_pdfas NNPDF31_nnlo_pdfas NNPDFpol10_100 NNPDFpol11_100 PDF4LHC15_nlo_100 PDF4LHC15_nlo_100_pdfas PDF4LHC15_nlo_30 PDF4LHC15_nlo_30_pdfas PDF4LHC15_nlo_asvar PDF4LHC15_nlo_mc PDF4LHC15_nlo_mc_pdfas PDF4LHC15_nlo_nf4_30 PDF4LHC15_nnlo_100 PDF4LHC15_nnlo_100_pdfas PDF4LHC15_nnlo_30 PDF4LHC15_nnlo_30_pdfas PDF4LHC15_nnlo_asvar PDF4LHC15_nnlo_mc PDF4LHC15_nnlo_mc_pdfas pdfsets.index sets TUJU19_nlo_1_1 TUJU19_nlo_119_50 TUJU19_nlo_12_6 TUJU19_nlo_131_54 TUJU19_nlo_197_79 TUJU19_nlo_208_82 TUJU19_nlo_2_1 TUJU19_nlo_27_13 TUJU19_nlo_3_2 TUJU19_nlo_40_20 TUJU19_nlo_4_2 TUJU19_nlo_56_26 TUJU19_nlo_64_29 TUJU19_nlo_7_3 TUJU19_nnlo_1_1 TUJU19_nnlo_119_50 TUJU19_nnlo_12_6 TUJU19_nnlo_131_54 TUJU19_nnlo_197_79 TUJU19_nnlo_208_82 TUJU19_nnlo_2_1 TUJU19_nnlo_27_13 TUJU19_nnlo_3_2 TUJU19_nnlo_40_20 TUJU19_nnlo_4_2 TUJU19_nnlo_56_26 TUJU19_nnlo_64_29 TUJU19_nnlo_7_3 xFitterPI_NLO_EIG xFitterPI_NLO_VAR"
for pdf in ${pdflist} ; do
  if [ ! -d "${pdf}" ] ; then
    echo missing pdf: ${pdf} ---
    echo making soft link to cvmfs
    ln -fs ${cvmfspath}/${pdf} ${pdf}
  fi
done