# Speechdata binary index

Generated on 2025-10-01T03:06:23.122397+00:00 to document which binaries live under `speechdata/` and which NVDA loaders still consume them.

## bestspeech
Legacy Taiwanese driver kept for provenance research.

**Loader modules:** assets/py/bestspeech.py

2 files | 2 binary | 0 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| **dll/B32_TTS.DLL** | .dll | 603648 | binary |  |
| **dll/b32_wrapper.dll** | .dll | 39936 | binary |  |

## brailab
Hungarian BraiLab+ runtime pending Python 3.13 rebuild.

**Loader modules:** assets/py/brailab.py

2 files | 2 binary | 0 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| **compiled/brailab.pyo** | .pyo | 4091 | binary |  |
| **dll/TTS.dll** | .dll | 69632 | binary |  |

## captain
Captain synthesizer bridge awaiting modern audio validation.

**Loader modules:** assets/py/captain.py

1 files | 1 binary | 0 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| **dll/captain.dll** | .dll | 165888 | binary |  |

## dectalk
Classic DECtalk runtime retained for heritage voice research and interoperability testing.

**Loader modules:** assets/py/_dectalk.py

18 files | 18 binary | 0 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| **dll/dectalk441.dll** | .dll | 438272 | binary |  |
| **dll/dectalk451.dll** | .dll | 279552 | binary |  |
| **dll/dectalk460.dll** | .dll | 454656 | binary |  |
| **dll/dectalk460oem.dll** | .dll | 454656 | binary |  |
| **dll/dectalk4611.dll** | .dll | 483328 | binary |  |
| **dll/dectalk500.dll** | .dll | 499712 | binary |  |
| **dll/dectalk51.dll** | .dll | 1912933 | binary |  |
| **dll/dtalk_ch.dll** | .dll | 503910 | binary |  |
| **dll/dtalk_fr.dll** | .dll | 393318 | binary |  |
| **dll/dtalk_gr.dll** | .dll | 925798 | binary |  |
| **dll/dtalk_hb.dll** | .dll | 327782 | binary |  |
| **dll/dtalk_it.dll** | .dll | 1052774 | binary |  |
| **dll/dtalk_jp.dll** | .dll | 491622 | binary |  |
| **dll/dtalk_kr.dll** | .dll | 495718 | binary |  |
| **dll/dtalk_la.dll** | .dll | 356454 | binary |  |
| **dll/dtalk_sp.dll** | .dll | 356454 | binary |  |
| **dll/dtalk_uk.dll** | .dll | 409702 | binary |  |
| **dll/dtalk_us.dll** | .dll | 471142 | binary |  |

## eloquence
Primary Eloquence runtime shipped to NVDA users; DLLs and .SYN voices are required for 32-bit compatibility during alpha packaging drills.

**Loader modules:** assets/py/Eloquence.py

70 files | 70 binary | 0 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| **dll/CW3220MT.DLL** | .dll | 249856 | binary |  |
| **dll/ECI.DLL** | .dll | 180224 | binary |  |
| **dll/ELOQSRVR.DLL** | .dll | 266240 | binary |  |
| **dll/TIBASE32.DLL** | .dll | 79872 | binary |  |
| **dll/TIENG32.DLL** | .dll | 324608 | binary |  |
| **dll/TISPAN32.DLL** | .dll | 66560 | binary |  |
| **dll/chsrom.dll** | .dll | 822832 | binary |  |
| **dll/jpnrom.dll** | .dll | 2534960 | binary |  |
| **dll/korrom.dll** | .dll | 282160 | binary |  |
| **dll/original_ECI.DLL** | .dll | 176128 | binary |  |
| **dll/sapi_ECI32D.DLL** | .dll | 124416 | binary |  |
| **dll/sapi_chsrom.dll** | .dll | 815104 | binary |  |
| **dll/sapi_eci.dll** | .dll | 180224 | binary |  |
| **dll/sapi_ecid.dll** | .dll | 176128 | binary |  |
| **dll/sapi_etisvr.dll** | .dll | 356352 | binary |  |
| **dll/sapi_jpnrom.dll** | .dll | 2527232 | binary |  |
| **dll/sapi_korrom.dll** | .dll | 274432 | binary |  |
| **exe/elocutor_demo.exe** | .exe | 147456 | binary |  |
| **exe/eloqtalk.exe** | .exe | 49152 | binary |  |
| **ico/appldocv.ico** | .ico | 1086 | binary |  |
| **ico/etipad.ico** | .ico | 326 | binary |  |
| **syn/DEU.SYN** | .syn | 1134592 | binary |  |
| **syn/ENG.SYN** | .syn | 1785856 | binary |  |
| **syn/ENU.SYN** | .syn | 1744896 | binary |  |
| **syn/ESM.SYN** | .syn | 794624 | binary |  |
| **syn/ESP.SYN** | .syn | 798720 | binary |  |
| **syn/FIN.SYN** | .syn | 1085440 | binary |  |
| **syn/FRA.SYN** | .syn | 1146880 | binary |  |
| **syn/FRC.SYN** | .syn | 1224704 | binary |  |
| **syn/ITA.SYN** | .syn | 827392 | binary |  |
| **syn/PTB.SYN** | .syn | 794624 | binary |  |
| **syn/chs.syn** | .syn | 2014768 | binary |  |
| **syn/jpn.syn** | .syn | 429616 | binary |  |
| **syn/kor.syn** | .syn | 2231856 | binary |  |
| **syn/original_DEU.SYN** | .syn | 1134592 | binary |  |
| **syn/original_ENG.SYN** | .syn | 1785856 | binary |  |
| **syn/original_ENU.SYN** | .syn | 1744896 | binary |  |
| **syn/original_ESM.SYN** | .syn | 794624 | binary |  |
| **syn/original_ESP.SYN** | .syn | 798720 | binary |  |
| **syn/original_FIN.SYN** | .syn | 1085440 | binary |  |
| **syn/original_FRA.SYN** | .syn | 1146880 | binary |  |
| **syn/original_FRC.SYN** | .syn | 1224704 | binary |  |
| **syn/original_ITA.SYN** | .syn | 827392 | binary |  |
| **syn/original_PTB.SYN** | .syn | 794624 | binary |  |
| **syn/sapi_ENU.SYN** | .syn | 1882112 | binary |  |
| **syn/sapi_chs.syn** | .syn | 2007040 | binary |  |
| **syn/sapi_deu.syn** | .syn | 1134592 | binary |  |
| **syn/sapi_eng.syn** | .syn | 1785856 | binary |  |
| **syn/sapi_esm.syn** | .syn | 794624 | binary |  |
| **syn/sapi_esp.syn** | .syn | 798720 | binary |  |
| **syn/sapi_fin.syn** | .syn | 1085440 | binary |  |
| **syn/sapi_fra.syn** | .syn | 1146880 | binary |  |
| **syn/sapi_frc.syn** | .syn | 1224704 | binary |  |
| **syn/sapi_ita.syn** | .syn | 827392 | binary |  |
| **syn/sapi_jpn.syn** | .syn | 421888 | binary |  |
| **syn/sapi_kor.syn** | .syn | 2224128 | binary |  |
| **syn/sapi_ptb.syn** | .syn | 794624 | binary |  |
| **uil/ENU.UIL** | .uil | 61440 | binary |  |
| **uil/chs.uil** | .uil | 73728 | binary |  |
| **uil/deu.uil** | .uil | 77824 | binary |  |
| **uil/eng.uil** | .uil | 77824 | binary |  |
| **uil/esm.uil** | .uil | 77824 | binary |  |
| **uil/esp.uil** | .uil | 77824 | binary |  |
| **uil/fin.uil** | .uil | 77824 | binary |  |
| **uil/fra.uil** | .uil | 77824 | binary |  |
| **uil/frc.uil** | .uil | 77824 | binary |  |
| **uil/ita.uil** | .uil | 77824 | binary |  |
| **uil/jpn.uil** | .uil | 77824 | binary |  |
| **uil/kor.uil** | .uil | 77824 | binary |  |
| **uil/ptb.uil** | .uil | 77824 | binary |  |

## festival
**Loader modules:** _None_ (pending migration)

128 files | 4 binary | 124 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| festival/lib/Sable.v0_2.dtd | .dtd | 6447 | text |  |
| festival/lib/Singing.v0_1.dtd | .dtd | 872 | text |  |
| festival/lib/apml.scm | .scm | 17381 | text |  |
| festival/lib/apml_f2bf0lr.scm | .scm | 26037 | text |  |
| festival/lib/apml_kaldurtreeZ.scm | .scm | 35956 | text |  |
| festival/lib/cap-signalization.scm | .scm | 2662 | text |  |
| festival/lib/cart_aux.scm | .scm | 6269 | text |  |
| festival/lib/clunits.scm | .scm | 10517 | text |  |
| festival/lib/clunits_build.scm | .scm | 16120 | text |  |
| festival/lib/cmusphinx2_phones.scm | .scm | 5271 | text |  |
| festival/lib/cslush.scm | .scm | 3969 | text |  |
| festival/lib/cstr.scm | .scm | 4431 | text |  |
| festival/lib/czech-debug.scm | .scm | 5609 | text |  |
| festival/lib/czech-lexicon.out | .out | 9593 | text |  |
| festival/lib/czech-lexicon.scm | .scm | 10734 | text |  |
| festival/lib/czech-mbrola.scm | .scm | 3303 | text |  |
| festival/lib/czech-unisyn.scm | .scm | 2589 | text |  |
| festival/lib/czech.scm | .scm | 78268 | text |  |
| festival/lib/darpa_phones.scm | .scm | 5329 | text |  |
| festival/lib/dicts/COPYING.poslex | .poslex | 2662 | text |  |
| festival/lib/dicts/cmu/COPYING | (none) | 2258 | text |  |
| festival/lib/dicts/cmu/allowables.scm | .scm | 2078 | text |  |
| festival/lib/dicts/cmu/cmu2ft | (none) | 536 | text |  |
| festival/lib/dicts/cmu/cmu_lts_rules.scm | .scm | 1648811 | text |  |
| festival/lib/dicts/cmu/cmudict-0.4.diff | .diff | 120798 | text |  |
| festival/lib/dicts/cmu/cmudict-0.4.out | .out | 5097125 | text |  |
| festival/lib/dicts/cmu/cmudict-0.4.scm | .scm | 3745651 | text |  |
| festival/lib/dicts/cmu/cmudict_extensions.scm | .scm | 20204 | text |  |
| festival/lib/dicts/cmu/cmulex.scm | .scm | 10864 | text |  |
| festival/lib/dicts/wsj.wp39.poslexR | .poslexr | 1220512 | text |  |
| festival/lib/dicts/wsj.wp39.tri.ngrambin | .ngrambin | 143569 | binary | No active loader references. |
| festival/lib/display.scm | .scm | 3823 | text |  |
| festival/lib/duration.scm | .scm | 7484 | text |  |
| festival/lib/email-mode.scm | .scm | 4197 | text |  |
| festival/lib/engmorph.scm | .scm | 5925 | text |  |
| festival/lib/engmorphsyn.scm | .scm | 5960 | text |  |
| festival/lib/etc/email_filter | (none) | 3169 | text |  |
| festival/lib/events.scm | .scm | 12599 | text |  |
| festival/lib/f2bdurtreeZ.scm | .scm | 34155 | text |  |
| festival/lib/f2bf0lr.scm | .scm | 11795 | text |  |
| festival/lib/festdoc.scm | .scm | 7638 | text |  |
| festival/lib/festival.el | .el | 11103 | text |  |
| festival/lib/festival.scm | .scm | 24167 | text |  |
| festival/lib/festlib_helper.scm | .scm | 1624 | text |  |
| festival/lib/festtest.scm | .scm | 3642 | text |  |
| festival/lib/fileio.scm | .scm | 2863 | text |  |
| festival/lib/fringe.scm | .scm | 3901 | text |  |
| festival/lib/gswdurtreeZ.scm | .scm | 35377 | text |  |
| festival/lib/holmes_phones.scm | .scm | 5447 | text |  |
| festival/lib/hts.scm | .scm | 17785 | text |  |
| festival/lib/init.scm | .scm | 5905 | text |  |
| festival/lib/intonation.scm | .scm | 7922 | text |  |
| festival/lib/java.scm | .scm | 2563 | text |  |
| festival/lib/klatt_durs.scm | .scm | 3273 | text |  |
| festival/lib/languages.scm | .scm | 4720 | text |  |
| festival/lib/lexicons.scm | .scm | 10306 | text |  |
| festival/lib/lts.scm | .scm | 7788 | text |  |
| festival/lib/lts_build.scm | .scm | 20599 | text |  |
| festival/lib/mbrola.scm | .scm | 4713 | text |  |
| festival/lib/mettree.scm | .scm | 3811 | text |  |
| festival/lib/module_description.scm | .scm | 4557 | text |  |
| festival/lib/mrpa_allophones.scm | .scm | 4965 | text |  |
| festival/lib/mrpa_durs.scm | .scm | 3943 | text |  |
| festival/lib/mrpa_phones.scm | .scm | 4906 | text |  |
| festival/lib/multisyn/multisyn.scm | .scm | 7595 | text |  |
| festival/lib/multisyn/multisyn_pauses.scm | .scm | 4974 | text |  |
| festival/lib/multisyn/radio_phones_multisyn.scm | .scm | 6021 | text |  |
| festival/lib/multisyn/send_xwaves.scm | .scm | 10629 | text |  |
| festival/lib/multisyn/target_cost.scm | .scm | 13164 | text |  |
| festival/lib/multiwave.scm | .scm | 2558 | text |  |
| festival/lib/nopauses.scm | .scm | 1361 | text |  |
| festival/lib/ogimarkup-mode.scm | .scm | 7974 | text |  |
| festival/lib/oo.scm | .scm | 5592 | text |  |
| festival/lib/pauses.scm | .scm | 8759 | text |  |
| festival/lib/phoneset.scm | .scm | 5345 | text |  |
| festival/lib/phrase.scm | .scm | 6881 | text |  |
| festival/lib/pos.scm | .scm | 9241 | text |  |
| festival/lib/postlex.scm | .scm | 21596 | text |  |
| festival/lib/prosody-param.scm | .scm | 8969 | text |  |
| festival/lib/punctuation.scm | .scm | 6229 | text |  |
| festival/lib/radio_phones.scm | .scm | 5494 | text |  |
| festival/lib/recode.scm | .scm | 1686 | text |  |
| festival/lib/sable-latin.ent | .ent | 8118 | text |  |
| festival/lib/sable-mode.scm | .scm | 20993 | text |  |
| festival/lib/scfg.scm | .scm | 3255 | text |  |
| festival/lib/scfg_wsj_wp20.gram | .gram | 16192 | text |  |
| festival/lib/sec.B.hept.ngrambin | .ngrambin | 545 | binary | No active loader references. |
| festival/lib/sec.ts20.quad.ngrambin | .ngrambin | 34376 | binary | No active loader references. |
| festival/lib/singing-mode.scm | .scm | 16452 | text |  |
| festival/lib/siod.scm | .scm | 17488 | text |  |
| festival/lib/siteinit.scm | .scm | 3187 | text |  |
| festival/lib/soleml-mode.scm | .scm | 12479 | text |  |
| festival/lib/speech-dispatcher.scm | .scm | 7666 | text |  |
| festival/lib/speech.properties | .properties | 88 | text |  |
| festival/lib/spell-mode.scm | .scm | 1850 | text |  |
| festival/lib/ssml-mode.scm | .scm | 23060 | text |  |
| festival/lib/synthesis.scm | .scm | 14827 | text |  |
| festival/lib/tilt.scm | .scm | 31534 | text |  |
| festival/lib/tobi.scm | .scm | 23342 | text |  |
| festival/lib/tobi_rules.scm | .scm | 35439 | text |  |
| festival/lib/token.scm | .scm | 23404 | text |  |
| festival/lib/tokenize.scm | .scm | 5872 | text |  |
| festival/lib/tokenpos.scm | .scm | 10060 | text |  |
| festival/lib/tts.scm | .scm | 11179 | text |  |
| festival/lib/unilex_phones.scm | .scm | 7914 | text |  |
| festival/lib/util.scm | .scm | 6587 | text |  |
| festival/lib/voice-select.scm | .scm | 6909 | text |  |
| festival/lib/voices/czech/czech_ph/COPYING | (none) | 17992 | text |  |
| festival/lib/voices/czech/czech_ph/INSTALL | (none) | 1381 | text |  |
| festival/lib/voices/czech/czech_ph/Makefile | (none) | 2664 | text |  |
| festival/lib/voices/czech/czech_ph/README | (none) | 1799 | text |  |
| festival/lib/voices/czech/czech_ph/README.cs | .cs | 988 | text |  |
| festival/lib/voices/czech/czech_ph/festvox/czech_ph.scm | .scm | 400 | text |  |
| festival/lib/voices/czech/czech_ph/festvox/czech_ph.scm.in | .in | 354 | text |  |
| festival/lib/voices/czech/czech_ph/group/ph.group | .group | 29328186 | text |  |
| festival/lib/voices/english/kal_diphone/COPYING | (none) | 2630 | text |  |
| festival/lib/voices/english/kal_diphone/festvox/kal_diphone.scm | .scm | 10639 | text |  |
| festival/lib/voices/english/kal_diphone/festvox/kaldurtreeZ.scm | .scm | 35371 | text |  |
| festival/lib/voices/english/kal_diphone/group/kallpc16k.group | .group | 6136911 | text |  |
| festival/lib/voices/english/ked_diphone/COPYING | (none) | 2504 | text |  |
| festival/lib/voices/english/ked_diphone/festvox/kddurtreeZ.scm | .scm | 35332 | text |  |
| festival/lib/voices/english/ked_diphone/festvox/ked_diphone.scm | .scm | 10362 | text |  |
| festival/lib/voices/english/ked_diphone/group/kedlpc16k.group | .group | 5630192 | text |  |
| festival/lib/voices.scm | .scm | 13431 | text |  |
| festival/lib/wave.scm | .scm | 2470 | text |  |
| festival/lib/web.scm | .scm | 3886 | text |  |
| festival/lib/word-mapping.scm | .scm | 1936 | text |  |
| festlib.dll | .dll | 2277376 | binary | No active loader references. |

## gregor
Orpheus/Gregor hybrid runtime archived for compatibility tests.

**Loader modules:** assets/py/gregor.py

3 files | 3 binary | 0 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| **compiled/gregor.pyc** | .pyc | 7687 | binary |  |
| **compiled/gregor.pyo** | .pyo | 7687 | binary |  |
| **dll/libsyntgregor.dll** | .dll | 89088 | binary |  |

## legacy
Unclassified speech archives awaiting provenance research before promotion into engine-specific buckets.

**Loader modules:** _None_ (pending migration)

8 files | 8 binary | 0 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| bin/BINADATA.BIN | .bin | 61984 | binary | No active loader references. |
| bin/BINAHANK.BIN | .bin | 4358 | binary | No active loader references. |
| bin/adrlong.bin | .bin | 21168 | binary | No active loader references. |
| bin/dane.bin | .bin | 10584 | binary | No active loader references. |
| bin/daneshort.bin | .bin | 489740 | binary | No active loader references. |
| bin/dlugkaj.bin | .bin | 10584 | binary | No active loader references. |
| bin/intershort.bin | .bin | 10584 | binary | No active loader references. |
| bin/lenkaj.bin | .bin | 10584 | binary | No active loader references. |

## mbrulainespeak
**Loader modules:** _None_ (pending migration)

200 files | 143 binary | 57 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| _mbrolaInEspeak.py | .py | 8111 | text |  |
| espeak-data/af_dict | (none) | 82372 | binary | No active loader references. |
| espeak-data/am_dict | (none) | 3334 | binary | No active loader references. |
| espeak-data/an_dict | (none) | 6696 | binary | No active loader references. |
| espeak-data/as_dict | (none) | 5024 | binary | No active loader references. |
| espeak-data/az_dict | (none) | 2135 | binary | No active loader references. |
| espeak-data/bg_dict | (none) | 27006 | binary | No active loader references. |
| espeak-data/bn_dict | (none) | 9774 | binary | No active loader references. |
| espeak-data/ca_dict | (none) | 4153 | binary | No active loader references. |
| espeak-data/cs_dict | (none) | 7565 | binary | No active loader references. |
| espeak-data/cy_dict | (none) | 3467 | binary | No active loader references. |
| espeak-data/da_dict | (none) | 208497 | binary | No active loader references. |
| espeak-data/de_dict | (none) | 21821 | binary | No active loader references. |
| espeak-data/el_dict | (none) | 8435 | binary | No active loader references. |
| espeak-data/en_dict | (none) | 126921 | binary | No active loader references. |
| espeak-data/eo_dict | (none) | 4677 | binary | No active loader references. |
| espeak-data/es_dict | (none) | 6290 | binary | No active loader references. |
| espeak-data/et_dict | (none) | 6767 | binary | No active loader references. |
| espeak-data/eu_dict | (none) | 4193 | binary | No active loader references. |
| espeak-data/fa_dict | (none) | 233021 | binary | No active loader references. |
| espeak-data/fi_dict | (none) | 5120 | binary | No active loader references. |
| espeak-data/fr_dict | (none) | 21422 | binary | No active loader references. |
| espeak-data/ga_dict | (none) | 8917 | binary | No active loader references. |
| espeak-data/gd_dict | (none) | 3794 | binary | No active loader references. |
| espeak-data/grc_dict | (none) | 3429 | binary | No active loader references. |
| espeak-data/gu_dict | (none) | 5324 | binary | No active loader references. |
| espeak-data/hbs_dict | (none) | 7721 | binary | No active loader references. |
| espeak-data/hi_dict | (none) | 9006 | binary | No active loader references. |
| espeak-data/hu_dict | (none) | 113340 | binary | No active loader references. |
| espeak-data/hy_dict | (none) | 3400 | binary | No active loader references. |
| espeak-data/ia_dict | (none) | 2081 | binary | No active loader references. |
| espeak-data/id_dict | (none) | 3082 | binary | No active loader references. |
| espeak-data/intonations | (none) | 1224 | binary | No active loader references. |
| espeak-data/is_dict | (none) | 5400 | binary | No active loader references. |
| espeak-data/it_dict | (none) | 86280 | binary | No active loader references. |
| espeak-data/jbo_dict | (none) | 2057 | binary | No active loader references. |
| espeak-data/ka_dict | (none) | 3138 | binary | No active loader references. |
| espeak-data/kl_dict | (none) | 2645 | binary | No active loader references. |
| espeak-data/kn_dict | (none) | 5515 | binary | No active loader references. |
| espeak-data/ko_dict | (none) | 6462 | binary | No active loader references. |
| espeak-data/ku_dict | (none) | 2268 | binary | No active loader references. |
| espeak-data/la_dict | (none) | 3817 | binary | No active loader references. |
| espeak-data/lfn_dict | (none) | 2870 | binary | No active loader references. |
| espeak-data/lt_dict | (none) | 5171 | binary | No active loader references. |
| espeak-data/lv_dict | (none) | 12293 | binary | No active loader references. |
| espeak-data/mbrola/af1 | (none) | 8057988 | binary | No active loader references. |
| espeak-data/mbrola/br1 | (none) | 5457022 | binary | No active loader references. |
| espeak-data/mbrola/br4 | (none) | 5117251 | binary | No active loader references. |
| espeak-data/mbrola/cr1 | (none) | 3515376 | binary | No active loader references. |
| espeak-data/mbrola/cz2 | (none) | 9812385 | binary | No active loader references. |
| espeak-data/mbrola/de2 | (none) | 10447243 | binary | No active loader references. |
| espeak-data/mbrola/de4 | (none) | 22267458 | binary | No active loader references. |
| espeak-data/mbrola/ee1 | (none) | 12129415 | binary | No active loader references. |
| espeak-data/mbrola/en1 | (none) | 6716280 | binary | No active loader references. |
| espeak-data/mbrola/es1 | (none) | 2831137 | binary | No active loader references. |
| espeak-data/mbrola/fr1 | (none) | 5080000 | binary | No active loader references. |
| espeak-data/mbrola/hu1 | (none) | 8925695 | binary | No active loader references. |
| espeak-data/mbrola/ic1 | (none) | 12037945 | binary | No active loader references. |
| espeak-data/mbrola/id1 | (none) | 5544972 | binary | No active loader references. |
| espeak-data/mbrola/ir1 | (none) | 5948960 | binary | No active loader references. |
| espeak-data/mbrola/it3 | (none) | 6779935 | binary | No active loader references. |
| espeak-data/mbrola/it4 | (none) | 6157513 | binary | No active loader references. |
| espeak-data/mbrola/la1 | (none) | 8627910 | binary | No active loader references. |
| espeak-data/mbrola/mx1 | (none) | 2294129 | binary | No active loader references. |
| espeak-data/mbrola/mx2 | (none) | 4240683 | binary | No active loader references. |
| espeak-data/mbrola/nl2 | (none) | 15192776 | binary | No active loader references. |
| espeak-data/mbrola/pl1 | (none) | 4745551 | binary | No active loader references. |
| espeak-data/mbrola/ro1 | (none) | 3822298 | binary | No active loader references. |
| espeak-data/mbrola/sw1 | (none) | 11545528 | binary | No active loader references. |
| espeak-data/mbrola/sw2 | (none) | 6574729 | binary | No active loader references. |
| espeak-data/mbrola/tr1 | (none) | 4694632 | binary | No active loader references. |
| espeak-data/mbrola/us1 | (none) | 7238094 | binary | No active loader references. |
| espeak-data/mbrola/us2 | (none) | 7080251 | binary | No active loader references. |
| espeak-data/mbrola/us3 | (none) | 7410252 | binary | No active loader references. |
| espeak-data/mbrola/vz1 | (none) | 2893218 | binary | No active loader references. |
| espeak-data/mbrola_ph/af1_phtrans | (none) | 1636 | binary | No active loader references. |
| espeak-data/mbrola_ph/ca1_phtrans | (none) | 1372 | binary | No active loader references. |
| espeak-data/mbrola_ph/cr1_phtrans | (none) | 2164 | binary | No active loader references. |
| espeak-data/mbrola_ph/cs_phtrans | (none) | 580 | binary | No active loader references. |
| espeak-data/mbrola_ph/de2_phtrans | (none) | 1540 | binary | No active loader references. |
| espeak-data/mbrola_ph/de4_phtrans | (none) | 1660 | binary | No active loader references. |
| espeak-data/mbrola_ph/de6_phtrans | (none) | 1276 | binary | No active loader references. |
| espeak-data/mbrola_ph/ee1_phtrans | (none) | 1444 | binary | No active loader references. |
| espeak-data/mbrola_ph/en1_phtrans | (none) | 796 | binary | No active loader references. |
| espeak-data/mbrola_ph/es_phtrans | (none) | 1708 | binary | No active loader references. |
| espeak-data/mbrola_ph/fr1_phtrans | (none) | 1972 | binary | No active loader references. |
| espeak-data/mbrola_ph/gr2_phtrans | (none) | 2212 | binary | No active loader references. |
| espeak-data/mbrola_ph/grc-de6_phtrans | (none) | 484 | binary | No active loader references. |
| espeak-data/mbrola_ph/hn1_phtrans | (none) | 532 | binary | No active loader references. |
| espeak-data/mbrola_ph/hu1_phtrans | (none) | 1444 | binary | No active loader references. |
| espeak-data/mbrola_ph/ic1_phtrans | (none) | 1132 | binary | No active loader references. |
| espeak-data/mbrola_ph/id1_phtrans | (none) | 892 | binary | No active loader references. |
| espeak-data/mbrola_ph/in1_phtrans | (none) | 1444 | binary | No active loader references. |
| espeak-data/mbrola_ph/ir1_phtrans | (none) | 5812 | binary | No active loader references. |
| espeak-data/mbrola_ph/it3_phtrans | (none) | 892 | binary | No active loader references. |
| espeak-data/mbrola_ph/la1_phtrans | (none) | 748 | binary | No active loader references. |
| espeak-data/mbrola_ph/lt1_phtrans | (none) | 1060 | binary | No active loader references. |
| espeak-data/mbrola_ph/lt2_phtrans | (none) | 1060 | binary | No active loader references. |
| espeak-data/mbrola_ph/mx1_phtrans | (none) | 1804 | binary | No active loader references. |
| espeak-data/mbrola_ph/mx2_phtrans | (none) | 1828 | binary | No active loader references. |
| espeak-data/mbrola_ph/nl_phtrans | (none) | 1684 | binary | No active loader references. |
| espeak-data/mbrola_ph/pl1_phtrans | (none) | 1564 | binary | No active loader references. |
| espeak-data/mbrola_ph/pt1_phtrans | (none) | 2092 | binary | No active loader references. |
| espeak-data/mbrola_ph/pt_phtrans | (none) | 2092 | binary | No active loader references. |
| espeak-data/mbrola_ph/ptbr4_phtrans | (none) | 2356 | binary | No active loader references. |
| espeak-data/mbrola_ph/ptbr_phtrans | (none) | 2500 | binary | No active loader references. |
| espeak-data/mbrola_ph/ro1_phtrans | (none) | 2164 | binary | No active loader references. |
| espeak-data/mbrola_ph/sv2_phtrans | (none) | 1588 | binary | No active loader references. |
| espeak-data/mbrola_ph/sv_phtrans | (none) | 1588 | binary | No active loader references. |
| espeak-data/mbrola_ph/tr1_phtrans | (none) | 364 | binary | No active loader references. |
| espeak-data/mbrola_ph/us3_phtrans | (none) | 1108 | binary | No active loader references. |
| espeak-data/mbrola_ph/us_phtrans | (none) | 1156 | binary | No active loader references. |
| espeak-data/mbrola_ph/vz_phtrans | (none) | 2284 | binary | No active loader references. |
| espeak-data/mk_dict | (none) | 4945 | binary | No active loader references. |
| espeak-data/ml_dict | (none) | 4159 | binary | No active loader references. |
| espeak-data/ms_dict | (none) | 12248 | binary | No active loader references. |
| espeak-data/nci_dict | (none) | 1534 | binary | No active loader references. |
| espeak-data/ne_dict | (none) | 10817 | binary | No active loader references. |
| espeak-data/nl_dict | (none) | 27197 | binary | No active loader references. |
| espeak-data/no_dict | (none) | 4178 | binary | No active loader references. |
| espeak-data/or_dict | (none) | 4765 | binary | No active loader references. |
| espeak-data/pa_dict | (none) | 6346 | binary | No active loader references. |
| espeak-data/pap_dict | (none) | 2128 | binary | No active loader references. |
| espeak-data/phondata | (none) | 450420 | binary | No active loader references. |
| espeak-data/phondata-manifest | (none) | 18636 | text |  |
| espeak-data/phonindex | (none) | 26166 | binary | No active loader references. |
| espeak-data/phontab | (none) | 41636 | binary | No active loader references. |
| espeak-data/pl_dict | (none) | 34924 | binary | No active loader references. |
| espeak-data/pt_dict | (none) | 26527 | binary | No active loader references. |
| espeak-data/ro_dict | (none) | 25205 | binary | No active loader references. |
| espeak-data/ru_dict | (none) | 1958608 | binary | No active loader references. |
| espeak-data/si_dict | (none) | 4143 | binary | No active loader references. |
| espeak-data/sk_dict | (none) | 9161 | binary | No active loader references. |
| espeak-data/sl_dict | (none) | 3965 | binary | No active loader references. |
| espeak-data/sq_dict | (none) | 3199 | binary | No active loader references. |
| espeak-data/sv_dict | (none) | 9676 | binary | No active loader references. |
| espeak-data/sw_dict | (none) | 3029 | binary | No active loader references. |
| espeak-data/ta_dict | (none) | 117470 | binary | No active loader references. |
| espeak-data/te_dict | (none) | 3556 | binary | No active loader references. |
| espeak-data/tr_dict | (none) | 6052 | binary | No active loader references. |
| espeak-data/ur_dict | (none) | 25149 | binary | No active loader references. |
| espeak-data/vi_dict | (none) | 7438 | binary | No active loader references. |
| espeak-data/voices/mb/mb-af1 | (none) | 88 | text |  |
| espeak-data/voices/mb/mb-af1-en | (none) | 83 | text |  |
| espeak-data/voices/mb/mb-br1 | (none) | 115 | text |  |
| espeak-data/voices/mb/mb-br3 | (none) | 115 | text |  |
| espeak-data/voices/mb/mb-br4 | (none) | 119 | text |  |
| espeak-data/voices/mb/mb-cr1 | (none) | 126 | text |  |
| espeak-data/voices/mb/mb-cz2 | (none) | 82 | text |  |
| espeak-data/voices/mb/mb-de2 | (none) | 83 | text |  |
| espeak-data/voices/mb/mb-de3 | (none) | 99 | text |  |
| espeak-data/voices/mb/mb-de4 | (none) | 85 | text |  |
| espeak-data/voices/mb/mb-de4-en | (none) | 79 | text |  |
| espeak-data/voices/mb/mb-de5 | (none) | 192 | text |  |
| espeak-data/voices/mb/mb-de5-en | (none) | 90 | text |  |
| espeak-data/voices/mb/mb-de6 | (none) | 78 | text |  |
| espeak-data/voices/mb/mb-de6-grc | (none) | 83 | text |  |
| espeak-data/voices/mb/mb-de7 | (none) | 106 | text |  |
| espeak-data/voices/mb/mb-ee1 | (none) | 95 | text |  |
| espeak-data/voices/mb/mb-en1 | (none) | 113 | text |  |
| espeak-data/voices/mb/mb-es1 | (none) | 97 | text |  |
| espeak-data/voices/mb/mb-es2 | (none) | 91 | text |  |
| espeak-data/voices/mb/mb-fr1 | (none) | 150 | text |  |
| espeak-data/voices/mb/mb-fr1-en | (none) | 103 | text |  |
| espeak-data/voices/mb/mb-fr4 | (none) | 111 | text |  |
| espeak-data/voices/mb/mb-fr4-en | (none) | 106 | text |  |
| espeak-data/voices/mb/mb-gr2 | (none) | 94 | text |  |
| espeak-data/voices/mb/mb-gr2-en | (none) | 88 | text |  |
| espeak-data/voices/mb/mb-hu1 | (none) | 102 | text |  |
| espeak-data/voices/mb/mb-hu1-en | (none) | 97 | text |  |
| espeak-data/voices/mb/mb-ic1 | (none) | 86 | text |  |
| espeak-data/voices/mb/mb-id1 | (none) | 101 | text |  |
| espeak-data/voices/mb/mb-ir1 | (none) | 753 | text |  |
| espeak-data/voices/mb/mb-ir2 | (none) | 768 | text |  |
| espeak-data/voices/mb/mb-it3 | (none) | 142 | text |  |
| espeak-data/voices/mb/mb-it4 | (none) | 145 | text |  |
| espeak-data/voices/mb/mb-la1 | (none) | 83 | text |  |
| espeak-data/voices/mb/mb-mx1 | (none) | 120 | text |  |
| espeak-data/voices/mb/mb-mx2 | (none) | 120 | text |  |
| espeak-data/voices/mb/mb-nl2 | (none) | 96 | text |  |
| espeak-data/voices/mb/mb-nl2-en | (none) | 91 | text |  |
| espeak-data/voices/mb/mb-pl1 | (none) | 99 | text |  |
| espeak-data/voices/mb/mb-pl1-en | (none) | 82 | text |  |
| espeak-data/voices/mb/mb-pt1 | (none) | 114 | text |  |
| espeak-data/voices/mb/mb-ro1 | (none) | 87 | text |  |
| espeak-data/voices/mb/mb-ro1-en | (none) | 81 | text |  |
| espeak-data/voices/mb/mb-sw1 | (none) | 98 | text |  |
| espeak-data/voices/mb/mb-sw1-en | (none) | 93 | text |  |
| espeak-data/voices/mb/mb-sw2 | (none) | 102 | text |  |
| espeak-data/voices/mb/mb-sw2-en | (none) | 99 | text |  |
| espeak-data/voices/mb/mb-tr1 | (none) | 85 | text |  |
| espeak-data/voices/mb/mb-tr2 | (none) | 114 | text |  |
| espeak-data/voices/mb/mb-us1 | (none) | 170 | text |  |
| espeak-data/voices/mb/mb-us2 | (none) | 178 | text |  |
| espeak-data/voices/mb/mb-us3 | (none) | 180 | text |  |
| espeak-data/voices/mb/mb-vz1 | (none) | 144 | text |  |
| espeak-data/zh_dict | (none) | 1066907 | binary | No active loader references. |
| espeak-data/zhy_dict | (none) | 481709 | binary | No active loader references. |
| espeak.dll | .dll | 455680 | binary | No active loader references. |
| mbrolaInEspeak.py | .py | 5194 | text |  |

## newfon
**Loader modules:** _None_ (pending migration)

26 files | 11 binary | 15 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| __init__.py | .py | 15666 | text |  |
| bin/dict.dat | .dat | 7593984 | binary | No active loader references. |
| bin/dictdb.dll | .dll | 405504 | binary | No active loader references. |
| bin/libsamplerate.dll | .dll | 1500160 | binary | No active loader references. |
| bin/ndict.dll | .dll | 33280 | binary | No active loader references. |
| bin/newfon_nvda.dll | .dll | 121344 | binary | No active loader references. |
| dict.dat | .dat | 7462912 | binary | No active loader references. |
| dict.dll | .dll | 34304 | binary | No active loader references. |
| languages/__init__.py | .py | 0 | text |  |
| languages/en.py | .py | 1769 | text |  |
| languages/hr.py | .py | 3480 | text |  |
| languages/pl.py | .py | 4558 | text |  |
| languages/pl_numbers.py | .py | 12191 | text |  |
| languages/ru.py | .py | 3149 | text |  |
| languages/sh_numbers.py | .py | 12585 | text |  |
| languages/sr.py | .py | 3285 | text |  |
| languages/uk.py | .py | 3617 | text |  |
| locale/ru/LC_MESSAGES/nvda.mo | .mo | 1873 | binary | No active loader references. |
| locale/ru/LC_MESSAGES/nvda.po | .po | 3045 | text |  |
| locale/ru/manifest.ini | .ini | 166 | text |  |
| locale/uk/LC_MESSAGES/nvda.mo | .mo | 1638 | binary | No active loader references. |
| locale/uk/LC_MESSAGES/nvda.po | .po | 2524 | text |  |
| locale/uk/manifest.ini | .ini | 166 | text |  |
| newfon.py | .py | 8698 | text |  |
| newfon_nvda.dll | .dll | 143872 | binary | No active loader references. |
| sdrvxpdb.dll | .dll | 335872 | binary | No active loader references. |

## nv_speech_player
Modern NV Speech Player bridge that backs NVDA's bundled voices; binaries must match upstream NV Access releases.

**Loader modules:** assets/py/speechPlayer.py, assets/py/old_speechPlayer.py, assets/py/smpsoft.py

3 files | 3 binary | 0 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| **dll/SMPRenderer.dll** | .dll | 360552 | binary |  |
| **dll/old_speechPlayer.dll** | .dll | 164864 | binary |  |
| **dll/speechPlayer.dll** | .dll | 199168 | binary |  |

## orpheus
Alias of Gregor runtime assets staged for potential future driver restoration.

**Loader modules:** assets/py/gregor.py

287 files | 182 binary | 105 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| __init__.py | .py | 9829 | text |  |
| **orpheus/DolABF.dll** | .dll | 28672 | binary |  |
| **orpheus/DolDSF.dll** | .dll | 32768 | binary |  |
| orpheus/Language/00001/00001.phm | .phm | 852 | text |  |
| **orpheus/Language/00001/00001.tts** | .tts | 616212 | binary |  |
| **orpheus/Language/00001/Brad.vcx** | .vcx | 17310386 | binary |  |
| **orpheus/Language/00001/Lucy.vcx** | .vcx | 19716346 | binary |  |
| **orpheus/Language/00001/synth.vcx** | .vcx | 12772 | binary |  |
| **orpheus/Language/00001/synth2.vcx** | .vcx | 12772 | binary |  |
| **orpheus/Language/00030/00030.TTS** | .tts | 57440 | binary |  |
| orpheus/Language/00030/00030.phm | .phm | 497 | text |  |
| **orpheus/Language/00030/synth.vcx** | .vcx | 13496 | binary |  |
| **orpheus/Language/00030/synth2.vcx** | .vcx | 13496 | binary |  |
| **orpheus/Language/00031/00031.TTS** | .tts | 98756 | binary |  |
| orpheus/Language/00031/00031.phm | .phm | 528 | text |  |
| **orpheus/Language/00031/synth.vcx** | .vcx | 13944 | binary |  |
| **orpheus/Language/00031/synth2.vcx** | .vcx | 13944 | binary |  |
| **orpheus/Language/00033/00033.TTS** | .tts | 51368 | binary |  |
| orpheus/Language/00033/00033.phm | .phm | 490 | text |  |
| **orpheus/Language/00033/synth.vcx** | .vcx | 9416 | binary |  |
| **orpheus/Language/00033/synth2.vcx** | .vcx | 9416 | binary |  |
| **orpheus/Language/00034/00034.TTS** | .tts | 23088 | binary |  |
| orpheus/Language/00034/00034.phm | .phm | 399 | text |  |
| **orpheus/Language/00034/Synth.vcx** | .vcx | 13320 | binary |  |
| **orpheus/Language/00034/Synth2.vcx** | .vcx | 13320 | binary |  |
| **orpheus/Language/00036/00036.TTS** | .tts | 29888 | binary |  |
| orpheus/Language/00036/00036.phm | .phm | 516 | text |  |
| **orpheus/Language/00036/synth.vcx** | .vcx | 13652 | binary |  |
| **orpheus/Language/00036/synth2.vcx** | .vcx | 13652 | binary |  |
| **orpheus/Language/00038/00038.TTS** | .tts | 508460 | binary |  |
| orpheus/Language/00038/00038.phm | .phm | 439 | text |  |
| **orpheus/Language/00038/synth.vcx** | .vcx | 13452 | binary |  |
| **orpheus/Language/00038/synth2.vcx** | .vcx | 13452 | binary |  |
| **orpheus/Language/00039/00039.TTS** | .tts | 66100 | binary |  |
| orpheus/Language/00039/00039.phm | .phm | 410 | text |  |
| **orpheus/Language/00039/synth.vcx** | .vcx | 8884 | binary |  |
| **orpheus/Language/00039/synth2.vcx** | .vcx | 8884 | binary |  |
| **orpheus/Language/00040/00040.TTS** | .tts | 32888 | binary |  |
| orpheus/Language/00040/00040.phm | .phm | 508 | text |  |
| **orpheus/Language/00040/synth.vcx** | .vcx | 12728 | binary |  |
| **orpheus/Language/00040/synth2.vcx** | .vcx | 12728 | binary |  |
| **orpheus/Language/00042/00042.TTS** | .tts | 25764 | binary |  |
| orpheus/Language/00042/00042.phm | .phm | 496 | text |  |
| **orpheus/Language/00042/synth.vcx** | .vcx | 13672 | binary |  |
| **orpheus/Language/00042/synth2.vcx** | .vcx | 13672 | binary |  |
| orpheus/Language/00044/00044.phm | .phm | 797 | text |  |
| **orpheus/Language/00044/00044.tts** | .tts | 618352 | binary |  |
| **orpheus/Language/00044/Alan.vcx** | .vcx | 18065554 | binary |  |
| **orpheus/Language/00044/Carol.vcx** | .vcx | 19729092 | binary |  |
| **orpheus/Language/00044/synth.vcx** | .vcx | 13144 | binary |  |
| **orpheus/Language/00044/synth2.vcx** | .vcx | 13144 | binary |  |
| **orpheus/Language/00045/00045.TTS** | .tts | 14352 | binary |  |
| orpheus/Language/00045/00045.phm | .phm | 420 | text |  |
| **orpheus/Language/00045/synth.vcx** | .vcx | 13672 | binary |  |
| **orpheus/Language/00045/synth2.vcx** | .vcx | 13672 | binary |  |
| orpheus/Language/00046/00046.phm | .phm | 920 | text |  |
| **orpheus/Language/00046/00046.tts** | .tts | 92452 | binary |  |
| **orpheus/Language/00046/anders.vcx** | .vcx | 17330590 | binary |  |
| **orpheus/Language/00046/synth.vcx** | .vcx | 11664 | binary |  |
| **orpheus/Language/00046/synth2.vcx** | .vcx | 11664 | binary |  |
| **orpheus/Language/00047/00047.TTS** | .tts | 25612 | binary |  |
| orpheus/Language/00047/00047.phm | .phm | 436 | text |  |
| **orpheus/Language/00047/synth.vcx** | .vcx | 12356 | binary |  |
| **orpheus/Language/00047/synth2.vcx** | .vcx | 12356 | binary |  |
| **orpheus/Language/00048/00048.TTS** | .tts | 23904 | binary |  |
| orpheus/Language/00048/00048.phm | .phm | 491 | text |  |
| **orpheus/Language/00048/synth.vcx** | .vcx | 13472 | binary |  |
| **orpheus/Language/00048/synth2.vcx** | .vcx | 13472 | binary |  |
| **orpheus/Language/00049/00049.TTS** | .tts | 52208 | binary |  |
| orpheus/Language/00049/00049.phm | .phm | 675 | text |  |
| **orpheus/Language/00049/synth.vcx** | .vcx | 9936 | binary |  |
| **orpheus/Language/00049/synth2.vcx** | .vcx | 9936 | binary |  |
| **orpheus/Language/00052/00052.TTS** | .tts | 22432 | binary |  |
| orpheus/Language/00052/00052.phm | .phm | 399 | text |  |
| **orpheus/Language/00052/synth.vcx** | .vcx | 13320 | binary |  |
| **orpheus/Language/00052/synth2.vcx** | .vcx | 13320 | binary |  |
| **orpheus/Language/00055/00055.TTS** | .tts | 24300 | binary |  |
| orpheus/Language/00055/00055.phm | .phm | 496 | text |  |
| **orpheus/Language/00055/synth.vcx** | .vcx | 13628 | binary |  |
| **orpheus/Language/00055/synth2.vcx** | .vcx | 13628 | binary |  |
| **orpheus/Language/00060/00060.TTS** | .tts | 19756 | binary |  |
| orpheus/Language/00060/00060.phm | .phm | 446 | text |  |
| **orpheus/Language/00060/synth.vcx** | .vcx | 13456 | binary |  |
| **orpheus/Language/00060/synth2.vcx** | .vcx | 13456 | binary |  |
| **orpheus/Language/00086/00086.TTS** | .tts | 769808 | binary |  |
| orpheus/Language/00086/00086.phm | .phm | 1229 | text |  |
| **orpheus/Language/00086/Synth2.vcx** | .vcx | 13532 | binary |  |
| **orpheus/Language/00086/synth.vcx** | .vcx | 13688 | binary |  |
| **orpheus/Language/00351/00351.TTS** | .tts | 25384 | binary |  |
| orpheus/Language/00351/00351.phm | .phm | 494 | text |  |
| **orpheus/Language/00351/synth.vcx** | .vcx | 13744 | binary |  |
| **orpheus/Language/00351/synth2.vcx** | .vcx | 13744 | binary |  |
| **orpheus/Language/00358/00358.TTS** | .tts | 24880 | binary |  |
| orpheus/Language/00358/00358.phm | .phm | 571 | text |  |
| **orpheus/Language/00358/synth.vcx** | .vcx | 10588 | binary |  |
| **orpheus/Language/00358/synth2.vcx** | .vcx | 10588 | binary |  |
| **orpheus/Language/00370/00370.TTS** | .tts | 37588 | binary |  |
| orpheus/Language/00370/00370.phm | .phm | 488 | text |  |
| **orpheus/Language/00370/synth.vcx** | .vcx | 12164 | binary |  |
| **orpheus/Language/00370/synth2.vcx** | .vcx | 12164 | binary |  |
| **orpheus/Language/10044/10044.TTS** | .tts | 27632 | binary |  |
| orpheus/Language/10044/10044.phm | .phm | 439 | text |  |
| **orpheus/Language/10044/synth.vcx** | .vcx | 13416 | binary |  |
| **orpheus/Language/10044/synth2.vcx** | .vcx | 13416 | binary |  |
| **orpheus/Language/10086/10086.TTS** | .tts | 424164 | binary |  |
| **orpheus/Language/10086/Synth2.vcx** | .vcx | 13904 | binary |  |
| **orpheus/Language/10086/synth.vcx** | .vcx | 14060 | binary |  |
| **orpheus/ORP00001.CHM** | .chm | 179395 | binary |  |
| orpheus/ORP00001.CNT | .cnt | 1977 | text |  |
| **orpheus/ORP00001.HLP** | .hlp | 213157 | binary |  |
| orpheus/ORP00001.INI | .ini | 6437 | text |  |
| **orpheus/ORP00007.CHM** | .chm | 179395 | binary |  |
| orpheus/ORP00007.CNT | .cnt | 1977 | text |  |
| **orpheus/ORP00007.HLP** | .hlp | 213157 | binary |  |
| orpheus/ORP00007.INI | .ini | 6437 | text |  |
| **orpheus/ORP00020.CHM** | .chm | 179395 | binary |  |
| orpheus/ORP00020.CNT | .cnt | 1977 | text |  |
| **orpheus/ORP00020.HLP** | .hlp | 213157 | binary |  |
| orpheus/ORP00020.INI | .ini | 6413 | text |  |
| **orpheus/ORP00031.CHM** | .chm | 226493 | binary |  |
| orpheus/ORP00031.CNT | .cnt | 2155 | text |  |
| **orpheus/ORP00031.HLP** | .hlp | 219085 | binary |  |
| orpheus/ORP00031.INI | .ini | 6947 | text |  |
| **orpheus/ORP00033.CHM** | .chm | 303538 | binary |  |
| orpheus/ORP00033.CNT | .cnt | 2206 | text |  |
| **orpheus/ORP00033.HLP** | .hlp | 362027 | binary |  |
| orpheus/ORP00033.INI | .ini | 7092 | text |  |
| **orpheus/ORP00034.CHM** | .chm | 181741 | binary |  |
| orpheus/ORP00034.CNT | .cnt | 2143 | text |  |
| **orpheus/ORP00034.HLP** | .hlp | 217552 | binary |  |
| orpheus/ORP00034.INI | .ini | 7077 | text |  |
| **orpheus/ORP00039.CHM** | .chm | 278199 | binary |  |
| orpheus/ORP00039.CNT | .cnt | 2020 | text |  |
| **orpheus/ORP00039.HLP** | .hlp | 190939 | binary |  |
| orpheus/ORP00039.INI | .ini | 6944 | text |  |
| **orpheus/ORP00042.CHM** | .chm | 179395 | binary |  |
| orpheus/ORP00042.CNT | .cnt | 1977 | text |  |
| **orpheus/ORP00042.HLP** | .hlp | 213157 | binary |  |
| orpheus/ORP00042.INI | .ini | 6993 | text |  |
| **orpheus/ORP00044.CHM** | .chm | 258751 | binary |  |
| orpheus/ORP00044.CNT | .cnt | 2594 | text |  |
| **orpheus/ORP00044.HLP** | .hlp | 203296 | binary |  |
| orpheus/ORP00044.INI | .ini | 6445 | text |  |
| **orpheus/ORP00045.CHM** | .chm | 179395 | binary |  |
| orpheus/ORP00045.CNT | .cnt | 1977 | text |  |
| **orpheus/ORP00045.HLP** | .hlp | 213157 | binary |  |
| orpheus/ORP00045.INI | .ini | 6445 | text |  |
| **orpheus/ORP00046.CHM** | .chm | 179841 | binary |  |
| orpheus/ORP00046.CNT | .cnt | 1869 | text |  |
| **orpheus/ORP00046.HLP** | .hlp | 231383 | binary |  |
| orpheus/ORP00046.INI | .ini | 6801 | text |  |
| **orpheus/ORP00047.CHM** | .chm | 205105 | binary |  |
| orpheus/ORP00047.CNT | .cnt | 1910 | text |  |
| **orpheus/ORP00047.HLP** | .hlp | 213158 | binary |  |
| orpheus/ORP00047.INI | .ini | 6615 | text |  |
| **orpheus/ORP00048.CHM** | .chm | 179395 | binary |  |
| orpheus/ORP00048.CNT | .cnt | 1977 | text |  |
| **orpheus/ORP00048.HLP** | .hlp | 213157 | binary |  |
| orpheus/ORP00048.INI | .ini | 6406 | text |  |
| **orpheus/ORP00049.CHM** | .chm | 313530 | binary |  |
| orpheus/ORP00049.CNT | .cnt | 2051 | text |  |
| **orpheus/ORP00049.HLP** | .hlp | 379112 | binary |  |
| orpheus/ORP00049.INI | .ini | 7190 | text |  |
| **orpheus/ORP00055.CHM** | .chm | 179395 | binary |  |
| orpheus/ORP00055.CNT | .cnt | 1977 | text |  |
| **orpheus/ORP00055.HLP** | .hlp | 213157 | binary |  |
| orpheus/ORP00055.INI | .ini | 6406 | text |  |
| **orpheus/ORP00090.CHM** | .chm | 258751 | binary |  |
| orpheus/ORP00090.CNT | .cnt | 2594 | text |  |
| **orpheus/ORP00090.HLP** | .hlp | 203296 | binary |  |
| orpheus/ORP00090.INI | .ini | 6445 | text |  |
| **orpheus/ORP00351.CHM** | .chm | 179395 | binary |  |
| orpheus/ORP00351.CNT | .cnt | 1977 | text |  |
| **orpheus/ORP00351.HLP** | .hlp | 213157 | binary |  |
| orpheus/ORP00351.INI | .ini | 6406 | text |  |
| **orpheus/ORP00358.CHM** | .chm | 312685 | binary |  |
| orpheus/ORP00358.CNT | .cnt | 1992 | text |  |
| **orpheus/ORP00358.HLP** | .hlp | 367513 | binary |  |
| orpheus/ORP00358.INI | .ini | 6504 | text |  |
| **orpheus/ORP10042.CHM** | .chm | 179395 | binary |  |
| orpheus/ORP10042.CNT | .cnt | 1977 | text |  |
| **orpheus/ORP10042.HLP** | .hlp | 213157 | binary |  |
| orpheus/ORP10042.INI | .ini | 6437 | text |  |
| **orpheus/ORP10044.CHM** | .chm | 257377 | binary |  |
| orpheus/ORP10044.CNT | .cnt | 2510 | text |  |
| **orpheus/ORP10044.HLP** | .hlp | 208921 | binary |  |
| orpheus/ORP10044.INI | .ini | 6893 | text |  |
| orpheus/VER.INI | .ini | 20 | text |  |
| **orpheus/a3s.dll** | .dll | 626688 | binary |  |
| **orpheus/a3sexn.dll** | .dll | 65536 | binary |  |
| **orpheus/amd64/dolcbar2.dll** | .dll | 384512 | binary |  |
| **orpheus/docs/ORP00001.DOC** | .doc | 275456 | binary |  |
| **orpheus/docs/ORP00007.DOC** | .doc | 268800 | binary |  |
| **orpheus/docs/ORP00020.DOC** | .doc | 275456 | binary |  |
| **orpheus/docs/ORP00031.DOC** | .doc | 295936 | binary |  |
| **orpheus/docs/ORP00033.DOC** | .doc | 406528 | binary |  |
| **orpheus/docs/ORP00034.DOC** | .doc | 276992 | binary |  |
| **orpheus/docs/ORP00039.DOC** | .doc | 248832 | binary |  |
| **orpheus/docs/ORP00042.DOC** | .doc | 275456 | binary |  |
| **orpheus/docs/ORP00044.DOC** | .doc | 268800 | binary |  |
| **orpheus/docs/ORP00045.DOC** | .doc | 275456 | binary |  |
| **orpheus/docs/ORP00046.DOC** | .doc | 299008 | binary |  |
| **orpheus/docs/ORP00047.DOC** | .doc | 275968 | binary |  |
| **orpheus/docs/ORP00048.DOC** | .doc | 275456 | binary |  |
| **orpheus/docs/ORP00049.DOC** | .doc | 417792 | binary |  |
| **orpheus/docs/ORP00055.DOC** | .doc | 417792 | binary |  |
| **orpheus/docs/ORP00090.DOC** | .doc | 268800 | binary |  |
| **orpheus/docs/ORP00351.DOC** | .doc | 417792 | binary |  |
| **orpheus/docs/ORP00358.DOC** | .doc | 385536 | binary |  |
| **orpheus/docs/ORP10042.DOC** | .doc | 275456 | binary |  |
| **orpheus/docs/ORP10044.DOC** | .doc | 264192 | binary |  |
| **orpheus/dolcbar2.dll** | .dll | 266240 | binary |  |
| orpheus/hook.cpp | .cpp | 1358 | text |  |
| orpheus/hook.def | .def | 41 | text |  |
| **orpheus/hook.dll** | .dll | 279040 | binary |  |
| **orpheus/oconfig.exe** | .exe | 49152 | binary |  |
| **orpheus/orpheus.sys** | .sys | 804 | binary |  |
| orpheus/sam/DSO00031.INI | .ini | 1355 | text |  |
| orpheus/sam/DSO00039.INI | .ini | 1371 | text |  |
| orpheus/sam/DSO00048.INI | .ini | 1243 | text |  |
| orpheus/sam/DSO00049.INI | .ini | 1439 | text |  |
| orpheus/sam/DSO00358.INI | .ini | 1349 | text |  |
| orpheus/sam/Dso00001.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00007.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00020.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00030.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00033.ini | .ini | 1367 | text |  |
| orpheus/sam/Dso00034.ini | .ini | 1361 | text |  |
| orpheus/sam/Dso00038.ini | .ini | 1510 | text |  |
| orpheus/sam/Dso00040.ini | .ini | 1898 | text |  |
| orpheus/sam/Dso00042.ini | .ini | 1898 | text |  |
| orpheus/sam/Dso00044.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00045.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00046.ini | .ini | 1368 | text |  |
| orpheus/sam/Dso00047.ini | .ini | 1325 | text |  |
| orpheus/sam/Dso00052.ini | .ini | 1361 | text |  |
| orpheus/sam/Dso00055.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00081.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00086.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00090.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00091.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00351.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00354.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00370.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00372.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00386.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso00972.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso01086.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso10034.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso10042.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso10044.ini | .ini | 1305 | text |  |
| orpheus/sam/Dso10086.ini | .ini | 1305 | text |  |
| **orpheus/sam/dolosam.dll** | .dll | 36864 | binary |  |
| orpheus/sam/dolosam.txt | .txt | 1879 | text |  |
| **orpheus/settings/00044.exc** | .exc | 5692 | binary |  |
| **orpheus/sfx/BEEP02.WAV** | .wav | 2244 | binary |  |
| **orpheus/sfx/BEEP03.WAV** | .wav | 2070 | binary |  |
| **orpheus/sfx/BEEP04.WAV** | .wav | 2070 | binary |  |
| **orpheus/sfx/Beep05.wav** | .wav | 8044 | binary |  |
| **orpheus/sfx/Beep06.wav** | .wav | 6444 | binary |  |
| **orpheus/sfx/Beep07.wav** | .wav | 8236 | binary |  |
| **orpheus/sfx/Beep08.wav** | .wav | 1044 | binary |  |
| **orpheus/sfx/Beep09.wav** | .wav | 1200 | binary |  |
| **orpheus/sfx/Beep10.wav** | .wav | 2876 | binary |  |
| **orpheus/sfx/Beep11.wav** | .wav | 14768 | binary |  |
| **orpheus/sfx/Beep12.wav** | .wav | 1340 | binary |  |
| **orpheus/sfx/Beep13.wav** | .wav | 940 | binary |  |
| **orpheus/sfx/Beep14.wav** | .wav | 1708 | binary |  |
| **orpheus/sfx/Beep15.wav** | .wav | 3180 | binary |  |
| **orpheus/sfx/Beep16.wav** | .wav | 2644 | binary |  |
| **orpheus/sfx/Beep17.wav** | .wav | 3820 | binary |  |
| **orpheus/sfx/Beep18.wav** | .wav | 2024 | binary |  |
| **orpheus/sfx/Beep19.wav** | .wav | 1684 | binary |  |
| **orpheus/sfx/Beep20.wav** | .wav | 1852 | binary |  |
| **orpheus/sfx/Beep21.wav** | .wav | 1844 | binary |  |
| **orpheus/sfx/Beep22.wav** | .wav | 2284 | binary |  |
| **orpheus/sfx/Beep23.wav** | .wav | 2344 | binary |  |
| **orpheus/sfx/Beep24.wav** | .wav | 2344 | binary |  |
| **orpheus/sfx/Beep25.wav** | .wav | 4844 | binary |  |
| **orpheus/sfx/Beep26.wav** | .wav | 10224 | binary |  |
| **orpheus/sfx/Beep27.wav** | .wav | 3884 | binary |  |
| **orpheus/sfx/Beep28.wav** | .wav | 1344 | binary |  |
| **orpheus/sfx/Beep29.wav** | .wav | 844 | binary |  |
| **orpheus/sfx/Beep30.wav** | .wav | 1324 | binary |  |
| **orpheus/sfx/beep01.wav** | .wav | 4454 | binary |  |
| **orpheus/unicows.dll** | .dll | 237936 | binary |  |
| orpheus.py | .py | 698 | text |  |

## pico
SVOX Pico offline engine used for lightweight language coverage during NVDA smoketests.

**Loader modules:** assets/py/pico.py

13 files | 13 binary | 0 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| **dll/svox-pico.dll** | .dll | 351744 | binary |  |
| **svox-pico-data/de-DE_gl0_sg.bin** | .bin | 634996 | binary |  |
| **svox-pico-data/de-DE_ta.bin** | .bin | 440732 | binary |  |
| **svox-pico-data/en-GB_kh0_sg.bin** | .bin | 584436 | binary |  |
| **svox-pico-data/en-GB_ta.bin** | .bin | 412248 | binary |  |
| **svox-pico-data/en-US_lh0_sg.bin** | .bin | 777396 | binary |  |
| **svox-pico-data/en-US_ta.bin** | .bin | 650668 | binary |  |
| **svox-pico-data/es-ES_ta.bin** | .bin | 256744 | binary |  |
| **svox-pico-data/es-ES_zl0_sg.bin** | .bin | 605280 | binary |  |
| **svox-pico-data/fr-FR_nk0_sg.bin** | .bin | 833236 | binary |  |
| **svox-pico-data/fr-FR_ta.bin** | .bin | 381936 | binary |  |
| **svox-pico-data/it-IT_cm0_sg.bin** | .bin | 628268 | binary |  |
| **svox-pico-data/it-IT_ta.bin** | .bin | 252044 | binary |  |

## sam
SAM (Software Automatic Mouth) samples preserved for testing.

**Loader modules:** assets/py/old_speechPlayer.py

1 files | 0 binary | 1 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| sam.py | .py | 5253 | text |  |

## speechplayerinespeak
**Loader modules:** _None_ (pending migration)

295 files | 83 binary | 212 text

| File | Extension | Size (bytes) | Classification | Notes |
| --- | --- | ---: | --- | --- |
| _speechPlayerInEspeak.py | .py | 8132 | text |  |
| espeak-ng-data/af_dict | (none) | 82495 | binary | No active loader references. |
| espeak-ng-data/am_dict | (none) | 3334 | binary | No active loader references. |
| espeak-ng-data/an_dict | (none) | 6696 | binary | No active loader references. |
| espeak-ng-data/as_dict | (none) | 5024 | binary | No active loader references. |
| espeak-ng-data/az_dict | (none) | 2135 | binary | No active loader references. |
| espeak-ng-data/bg_dict | (none) | 27006 | binary | No active loader references. |
| espeak-ng-data/bn_dict | (none) | 9774 | binary | No active loader references. |
| espeak-ng-data/ca_dict | (none) | 4153 | binary | No active loader references. |
| espeak-ng-data/cs_dict | (none) | 7565 | binary | No active loader references. |
| espeak-ng-data/cy_dict | (none) | 3467 | binary | No active loader references. |
| espeak-ng-data/da_dict | (none) | 208497 | binary | No active loader references. |
| espeak-ng-data/de_dict | (none) | 21821 | binary | No active loader references. |
| espeak-ng-data/el_dict | (none) | 10144 | binary | No active loader references. |
| espeak-ng-data/en_dict | (none) | 129636 | binary | No active loader references. |
| espeak-ng-data/eo_dict | (none) | 4677 | binary | No active loader references. |
| espeak-ng-data/es_dict | (none) | 6673 | binary | No active loader references. |
| espeak-ng-data/et_dict | (none) | 6767 | binary | No active loader references. |
| espeak-ng-data/eu_dict | (none) | 4628 | binary | No active loader references. |
| espeak-ng-data/fa_dict | (none) | 237908 | binary | No active loader references. |
| espeak-ng-data/fi_dict | (none) | 5120 | binary | No active loader references. |
| espeak-ng-data/fr_dict | (none) | 21552 | binary | No active loader references. |
| espeak-ng-data/ga_dict | (none) | 8917 | binary | No active loader references. |
| espeak-ng-data/gd_dict | (none) | 3794 | binary | No active loader references. |
| espeak-ng-data/gn_dict | (none) | 3157 | binary | No active loader references. |
| espeak-ng-data/grc_dict | (none) | 3429 | binary | No active loader references. |
| espeak-ng-data/gu_dict | (none) | 5324 | binary | No active loader references. |
| espeak-ng-data/hbs_dict | (none) | 7788 | binary | No active loader references. |
| espeak-ng-data/hi_dict | (none) | 9094 | binary | No active loader references. |
| espeak-ng-data/hu_dict | (none) | 113312 | binary | No active loader references. |
| espeak-ng-data/hy_dict | (none) | 3400 | binary | No active loader references. |
| espeak-ng-data/ia_dict | (none) | 2081 | binary | No active loader references. |
| espeak-ng-data/id_dict | (none) | 3091 | binary | No active loader references. |
| espeak-ng-data/intonations | (none) | 1768 | binary | No active loader references. |
| espeak-ng-data/is_dict | (none) | 5400 | binary | No active loader references. |
| espeak-ng-data/it_dict | (none) | 104966 | binary | No active loader references. |
| espeak-ng-data/jbo_dict | (none) | 2057 | binary | No active loader references. |
| espeak-ng-data/ka_dict | (none) | 3138 | binary | No active loader references. |
| espeak-ng-data/kl_dict | (none) | 2645 | binary | No active loader references. |
| espeak-ng-data/kn_dict | (none) | 5519 | binary | No active loader references. |
| espeak-ng-data/ko_dict | (none) | 6462 | binary | No active loader references. |
| espeak-ng-data/ku_dict | (none) | 2268 | binary | No active loader references. |
| espeak-ng-data/ky_dict | (none) | 2098 | binary | No active loader references. |
| espeak-ng-data/la_dict | (none) | 3817 | binary | No active loader references. |
| espeak-ng-data/lfn_dict | (none) | 2870 | binary | No active loader references. |
| espeak-ng-data/lt_dict | (none) | 5171 | binary | No active loader references. |
| espeak-ng-data/lv_dict | (none) | 17396 | binary | No active loader references. |
| espeak-ng-data/mk_dict | (none) | 4945 | binary | No active loader references. |
| espeak-ng-data/ml_dict | (none) | 4159 | binary | No active loader references. |
| espeak-ng-data/mr_dict | (none) | 5681 | binary | No active loader references. |
| espeak-ng-data/ms_dict | (none) | 12248 | binary | No active loader references. |
| espeak-ng-data/mt_dict | (none) | 4384 | binary | No active loader references. |
| espeak-ng-data/my_dict | (none) | 1300 | binary | No active loader references. |
| espeak-ng-data/nci_dict | (none) | 1534 | binary | No active loader references. |
| espeak-ng-data/ne_dict | (none) | 10817 | binary | No active loader references. |
| espeak-ng-data/nl_dict | (none) | 27201 | binary | No active loader references. |
| espeak-ng-data/no_dict | (none) | 4178 | binary | No active loader references. |
| espeak-ng-data/om_dict | (none) | 2302 | binary | No active loader references. |
| espeak-ng-data/or_dict | (none) | 4765 | binary | No active loader references. |
| espeak-ng-data/pa_dict | (none) | 6346 | binary | No active loader references. |
| espeak-ng-data/pap_dict | (none) | 2128 | binary | No active loader references. |
| espeak-ng-data/phondata | (none) | 453916 | binary | No active loader references. |
| espeak-ng-data/phondata-manifest | (none) | 19020 | text |  |
| espeak-ng-data/phonindex | (none) | 28688 | binary | No active loader references. |
| espeak-ng-data/phontab | (none) | 44196 | binary | No active loader references. |
| espeak-ng-data/pl_dict | (none) | 34269 | binary | No active loader references. |
| espeak-ng-data/pt_dict | (none) | 26527 | binary | No active loader references. |
| espeak-ng-data/ro_dict | (none) | 25205 | binary | No active loader references. |
| espeak-ng-data/ru_dict | (none) | 1958608 | binary | No active loader references. |
| espeak-ng-data/si_dict | (none) | 4143 | binary | No active loader references. |
| espeak-ng-data/sk_dict | (none) | 9161 | binary | No active loader references. |
| espeak-ng-data/sl_dict | (none) | 3965 | binary | No active loader references. |
| espeak-ng-data/sq_dict | (none) | 3199 | binary | No active loader references. |
| espeak-ng-data/sv_dict | (none) | 9676 | binary | No active loader references. |
| espeak-ng-data/sw_dict | (none) | 3029 | binary | No active loader references. |
| espeak-ng-data/ta_dict | (none) | 120287 | binary | No active loader references. |
| espeak-ng-data/te_dict | (none) | 3556 | binary | No active loader references. |
| espeak-ng-data/tn_dict | (none) | 3072 | binary | No active loader references. |
| espeak-ng-data/tr_dict | (none) | 6080 | binary | No active loader references. |
| espeak-ng-data/tt_dict | (none) | 2121 | binary | No active loader references. |
| espeak-ng-data/ur_dict | (none) | 25149 | binary | No active loader references. |
| espeak-ng-data/vi_dict | (none) | 7438 | binary | No active loader references. |
| espeak-ng-data/voices/!v/Andy | (none) | 330 | text |  |
| espeak-ng-data/voices/!v/Annie | (none) | 298 | text |  |
| espeak-ng-data/voices/!v/AnxiousAndy | (none) | 370 | text |  |
| espeak-ng-data/voices/!v/Denis | (none) | 286 | text |  |
| espeak-ng-data/voices/!v/Gene | (none) | 264 | text |  |
| espeak-ng-data/voices/!v/Gene2 | (none) | 266 | text |  |
| espeak-ng-data/voices/!v/Jacky | (none) | 250 | text |  |
| espeak-ng-data/voices/!v/Lee | (none) | 332 | text |  |
| espeak-ng-data/voices/!v/Mario | (none) | 253 | text |  |
| espeak-ng-data/voices/!v/Michael | (none) | 256 | text |  |
| espeak-ng-data/voices/!v/Mr serious | (none) | 3144 | text |  |
| espeak-ng-data/voices/!v/Storm | (none) | 397 | text |  |
| espeak-ng-data/voices/!v/Tweaky | (none) | 3140 | text |  |
| espeak-ng-data/voices/!v/aunty | (none) | 368 | text |  |
| espeak-ng-data/voices/!v/boris | (none) | 209 | text |  |
| espeak-ng-data/voices/!v/croak | (none) | 93 | text |  |
| espeak-ng-data/voices/!v/edward | (none) | 151 | text |  |
| espeak-ng-data/voices/!v/f1 | (none) | 324 | text |  |
| espeak-ng-data/voices/!v/f2 | (none) | 357 | text |  |
| espeak-ng-data/voices/!v/f3 | (none) | 375 | text |  |
| espeak-ng-data/voices/!v/f4 | (none) | 350 | text |  |
| espeak-ng-data/voices/!v/f5 | (none) | 425 | text |  |
| espeak-ng-data/voices/!v/iven | (none) | 262 | text |  |
| espeak-ng-data/voices/!v/iven2 | (none) | 280 | text |  |
| espeak-ng-data/voices/!v/iven3 | (none) | 263 | text |  |
| espeak-ng-data/voices/!v/john | (none) | 3137 | text |  |
| espeak-ng-data/voices/!v/kaukovalta | (none) | 346 | text |  |
| espeak-ng-data/voices/!v/klatt | (none) | 38 | text |  |
| espeak-ng-data/voices/!v/klatt2 | (none) | 38 | text |  |
| espeak-ng-data/voices/!v/klatt3 | (none) | 39 | text |  |
| espeak-ng-data/voices/!v/klatt4 | (none) | 39 | text |  |
| espeak-ng-data/voices/!v/linda | (none) | 369 | text |  |
| espeak-ng-data/voices/!v/m1 | (none) | 335 | text |  |
| espeak-ng-data/voices/!v/m2 | (none) | 264 | text |  |
| espeak-ng-data/voices/!v/m3 | (none) | 300 | text |  |
| espeak-ng-data/voices/!v/m4 | (none) | 290 | text |  |
| espeak-ng-data/voices/!v/m5 | (none) | 262 | text |  |
| espeak-ng-data/voices/!v/m6 | (none) | 188 | text |  |
| espeak-ng-data/voices/!v/m7 | (none) | 254 | text |  |
| espeak-ng-data/voices/!v/max | (none) | 210 | text |  |
| espeak-ng-data/voices/!v/michel | (none) | 382 | text |  |
| espeak-ng-data/voices/!v/norbert | (none) | 3140 | text |  |
| espeak-ng-data/voices/!v/quincy | (none) | 334 | text |  |
| espeak-ng-data/voices/!v/rob | (none) | 248 | text |  |
| espeak-ng-data/voices/!v/robert | (none) | 257 | text |  |
| espeak-ng-data/voices/!v/steph | (none) | 364 | text |  |
| espeak-ng-data/voices/!v/steph2 | (none) | 367 | text |  |
| espeak-ng-data/voices/!v/steph3 | (none) | 377 | text |  |
| espeak-ng-data/voices/!v/travis | (none) | 360 | text |  |
| espeak-ng-data/voices/!v/whisper | (none) | 186 | text |  |
| espeak-ng-data/voices/!v/whisperf | (none) | 392 | text |  |
| espeak-ng-data/voices/!v/zac | (none) | 260 | text |  |
| espeak-ng-data/voices/aav/vi | (none) | 59 | text |  |
| espeak-ng-data/voices/aav/vi-VN-x-central | (none) | 211 | text |  |
| espeak-ng-data/voices/aav/vi-VN-x-south | (none) | 209 | text |  |
| espeak-ng-data/voices/art/eo | (none) | 53 | text |  |
| espeak-ng-data/voices/art/ia | (none) | 29 | text |  |
| espeak-ng-data/voices/art/jbo | (none) | 69 | text |  |
| espeak-ng-data/voices/art/lfn | (none) | 139 | text |  |
| espeak-ng-data/voices/axm/hy | (none) | 38 | text |  |
| espeak-ng-data/voices/axm/hy-arevmda | (none) | 328 | text |  |
| espeak-ng-data/voices/azc/nci | (none) | 124 | text |  |
| espeak-ng-data/voices/bnt/sw | (none) | 53 | text |  |
| espeak-ng-data/voices/bnt/tn | (none) | 54 | text |  |
| espeak-ng-data/voices/ccs/ka | (none) | 26 | text |  |
| espeak-ng-data/voices/cel/cy | (none) | 49 | text |  |
| espeak-ng-data/voices/cel/ga | (none) | 65 | text |  |
| espeak-ng-data/voices/cel/gd | (none) | 49 | text |  |
| espeak-ng-data/voices/cus/om | (none) | 39 | text |  |
| espeak-ng-data/voices/default | (none) | 38 | text |  |
| espeak-ng-data/voices/dra/kn | (none) | 55 | text |  |
| espeak-ng-data/voices/dra/ml | (none) | 69 | text |  |
| espeak-ng-data/voices/dra/ta | (none) | 63 | text |  |
| espeak-ng-data/voices/dra/te | (none) | 70 | text |  |
| espeak-ng-data/voices/esx/kl | (none) | 30 | text |  |
| espeak-ng-data/voices/gmq/da | (none) | 57 | text |  |
| espeak-ng-data/voices/gmq/is | (none) | 40 | text |  |
| espeak-ng-data/voices/gmq/no | (none) | 65 | text |  |
| espeak-ng-data/voices/gmq/sv | (none) | 38 | text |  |
| espeak-ng-data/voices/gmw/af | (none) | 67 | text |  |
| espeak-ng-data/voices/gmw/de | (none) | 38 | text |  |
| espeak-ng-data/voices/gmw/en | (none) | 136 | text |  |
| espeak-ng-data/voices/gmw/en-029 | (none) | 359 | text |  |
| espeak-ng-data/voices/gmw/en-GB-scotland | (none) | 300 | text |  |
| espeak-ng-data/voices/gmw/en-GB-x-gbclan | (none) | 264 | text |  |
| espeak-ng-data/voices/gmw/en-GB-x-gbcwmd | (none) | 208 | text |  |
| espeak-ng-data/voices/gmw/en-GB-x-rp | (none) | 257 | text |  |
| espeak-ng-data/voices/gmw/en-US | (none) | 281 | text |  |
| espeak-ng-data/voices/gmw/nl | (none) | 35 | text |  |
| espeak-ng-data/voices/grk/el | (none) | 37 | text |  |
| espeak-ng-data/voices/grk/grc | (none) | 110 | text |  |
| espeak-ng-data/voices/inc/as | (none) | 42 | text |  |
| espeak-ng-data/voices/inc/bn | (none) | 37 | text |  |
| espeak-ng-data/voices/inc/gu | (none) | 42 | text |  |
| espeak-ng-data/voices/inc/hi | (none) | 35 | text |  |
| espeak-ng-data/voices/inc/mr | (none) | 41 | text |  |
| espeak-ng-data/voices/inc/ne | (none) | 49 | text |  |
| espeak-ng-data/voices/inc/or | (none) | 39 | text |  |
| espeak-ng-data/voices/inc/pa | (none) | 25 | text |  |
| espeak-ng-data/voices/inc/si | (none) | 55 | text |  |
| espeak-ng-data/voices/inc/ur | (none) | 53 | text |  |
| espeak-ng-data/voices/ine/sq | (none) | 115 | text |  |
| espeak-ng-data/voices/ira/fa | (none) | 362 | text |  |
| espeak-ng-data/voices/ira/fa-Latn | (none) | 267 | text |  |
| espeak-ng-data/voices/ira/fa-en-us | (none) | 287 | text |  |
| espeak-ng-data/voices/ira/ku | (none) | 52 | text |  |
| espeak-ng-data/voices/itc/la | (none) | 298 | text |  |
| espeak-ng-data/voices/ko | (none) | 63 | text |  |
| espeak-ng-data/voices/mb/mb-af1 | (none) | 88 | text |  |
| espeak-ng-data/voices/mb/mb-af1-en | (none) | 83 | text |  |
| espeak-ng-data/voices/mb/mb-br1 | (none) | 115 | text |  |
| espeak-ng-data/voices/mb/mb-br2 | (none) | 119 | text |  |
| espeak-ng-data/voices/mb/mb-br3 | (none) | 115 | text |  |
| espeak-ng-data/voices/mb/mb-br4 | (none) | 119 | text |  |
| espeak-ng-data/voices/mb/mb-cr1 | (none) | 126 | text |  |
| espeak-ng-data/voices/mb/mb-cz2 | (none) | 82 | text |  |
| espeak-ng-data/voices/mb/mb-de1 | (none) | 99 | text |  |
| espeak-ng-data/voices/mb/mb-de1-en | (none) | 96 | text |  |
| espeak-ng-data/voices/mb/mb-de2 | (none) | 83 | text |  |
| espeak-ng-data/voices/mb/mb-de2-en | (none) | 80 | text |  |
| espeak-ng-data/voices/mb/mb-de3 | (none) | 99 | text |  |
| espeak-ng-data/voices/mb/mb-de3-en | (none) | 96 | text |  |
| espeak-ng-data/voices/mb/mb-de4 | (none) | 85 | text |  |
| espeak-ng-data/voices/mb/mb-de4-en | (none) | 81 | text |  |
| espeak-ng-data/voices/mb/mb-de5 | (none) | 192 | text |  |
| espeak-ng-data/voices/mb/mb-de5-en | (none) | 90 | text |  |
| espeak-ng-data/voices/mb/mb-de6 | (none) | 78 | text |  |
| espeak-ng-data/voices/mb/mb-de6-en | (none) | 74 | text |  |
| espeak-ng-data/voices/mb/mb-de6-grc | (none) | 83 | text |  |
| espeak-ng-data/voices/mb/mb-de7 | (none) | 106 | text |  |
| espeak-ng-data/voices/mb/mb-ee1 | (none) | 95 | text |  |
| espeak-ng-data/voices/mb/mb-en1 | (none) | 113 | text |  |
| espeak-ng-data/voices/mb/mb-es1 | (none) | 97 | text |  |
| espeak-ng-data/voices/mb/mb-es2 | (none) | 91 | text |  |
| espeak-ng-data/voices/mb/mb-fr1 | (none) | 150 | text |  |
| espeak-ng-data/voices/mb/mb-fr1-en | (none) | 103 | text |  |
| espeak-ng-data/voices/mb/mb-fr4 | (none) | 111 | text |  |
| espeak-ng-data/voices/mb/mb-fr4-en | (none) | 106 | text |  |
| espeak-ng-data/voices/mb/mb-gr2 | (none) | 94 | text |  |
| espeak-ng-data/voices/mb/mb-gr2-en | (none) | 88 | text |  |
| espeak-ng-data/voices/mb/mb-hu1 | (none) | 102 | text |  |
| espeak-ng-data/voices/mb/mb-hu1-en | (none) | 97 | text |  |
| espeak-ng-data/voices/mb/mb-ic1 | (none) | 86 | text |  |
| espeak-ng-data/voices/mb/mb-id1 | (none) | 101 | text |  |
| espeak-ng-data/voices/mb/mb-ir1 | (none) | 753 | text |  |
| espeak-ng-data/voices/mb/mb-ir2 | (none) | 768 | text |  |
| espeak-ng-data/voices/mb/mb-it3 | (none) | 142 | text |  |
| espeak-ng-data/voices/mb/mb-it4 | (none) | 145 | text |  |
| espeak-ng-data/voices/mb/mb-la1 | (none) | 83 | text |  |
| espeak-ng-data/voices/mb/mb-lt1 | (none) | 88 | text |  |
| espeak-ng-data/voices/mb/mb-lt2 | (none) | 88 | text |  |
| espeak-ng-data/voices/mb/mb-mx1 | (none) | 120 | text |  |
| espeak-ng-data/voices/mb/mb-mx2 | (none) | 120 | text |  |
| espeak-ng-data/voices/mb/mb-nl2 | (none) | 96 | text |  |
| espeak-ng-data/voices/mb/mb-nl2-en | (none) | 91 | text |  |
| espeak-ng-data/voices/mb/mb-pl1 | (none) | 99 | text |  |
| espeak-ng-data/voices/mb/mb-pl1-en | (none) | 82 | text |  |
| espeak-ng-data/voices/mb/mb-pt1 | (none) | 114 | text |  |
| espeak-ng-data/voices/mb/mb-ro1 | (none) | 87 | text |  |
| espeak-ng-data/voices/mb/mb-ro1-en | (none) | 81 | text |  |
| espeak-ng-data/voices/mb/mb-sw1 | (none) | 98 | text |  |
| espeak-ng-data/voices/mb/mb-sw1-en | (none) | 93 | text |  |
| espeak-ng-data/voices/mb/mb-sw2 | (none) | 102 | text |  |
| espeak-ng-data/voices/mb/mb-sw2-en | (none) | 99 | text |  |
| espeak-ng-data/voices/mb/mb-tr1 | (none) | 85 | text |  |
| espeak-ng-data/voices/mb/mb-tr2 | (none) | 114 | text |  |
| espeak-ng-data/voices/mb/mb-us1 | (none) | 170 | text |  |
| espeak-ng-data/voices/mb/mb-us2 | (none) | 178 | text |  |
| espeak-ng-data/voices/mb/mb-us3 | (none) | 180 | text |  |
| espeak-ng-data/voices/mb/mb-vz1 | (none) | 144 | text |  |
| espeak-ng-data/voices/poz/id | (none) | 146 | text |  |
| espeak-ng-data/voices/poz/ms | (none) | 457 | text |  |
| espeak-ng-data/voices/roa/an | (none) | 39 | text |  |
| espeak-ng-data/voices/roa/ca | (none) | 38 | text |  |
| espeak-ng-data/voices/roa/es | (none) | 70 | text |  |
| espeak-ng-data/voices/roa/es-419 | (none) | 182 | text |  |
| espeak-ng-data/voices/roa/fr | (none) | 82 | text |  |
| espeak-ng-data/voices/roa/fr-BE | (none) | 94 | text |  |
| espeak-ng-data/voices/roa/it | (none) | 122 | text |  |
| espeak-ng-data/voices/roa/pap | (none) | 62 | text |  |
| espeak-ng-data/voices/roa/pt-BR | (none) | 106 | text |  |
| espeak-ng-data/voices/roa/pt-PT | (none) | 96 | text |  |
| espeak-ng-data/voices/roa/ro | (none) | 40 | text |  |
| espeak-ng-data/voices/sai/gn | (none) | 48 | text |  |
| espeak-ng-data/voices/sem/am | (none) | 41 | text |  |
| espeak-ng-data/voices/sem/mt | (none) | 41 | text |  |
| espeak-ng-data/voices/sit/cmn | (none) | 611 | text |  |
| espeak-ng-data/voices/sit/my | (none) | 25 | text |  |
| espeak-ng-data/voices/sit/yue | (none) | 210 | text |  |
| espeak-ng-data/voices/trk/az | (none) | 45 | text |  |
| espeak-ng-data/voices/trk/ky | (none) | 43 | text |  |
| espeak-ng-data/voices/trk/tr | (none) | 38 | text |  |
| espeak-ng-data/voices/trk/tt | (none) | 35 | text |  |
| espeak-ng-data/voices/urj/et | (none) | 27 | text |  |
| espeak-ng-data/voices/urj/fi | (none) | 38 | text |  |
| espeak-ng-data/voices/urj/hu | (none) | 73 | text |  |
| espeak-ng-data/voices/xaq/eu | (none) | 40 | text |  |
| espeak-ng-data/voices/xaq/lt | (none) | 42 | text |  |
| espeak-ng-data/voices/xaq/lv | (none) | 235 | text |  |
| espeak-ng-data/voices/zls/bg | (none) | 110 | text |  |
| espeak-ng-data/voices/zls/bs | (none) | 257 | text |  |
| espeak-ng-data/voices/zls/cs | (none) | 36 | text |  |
| espeak-ng-data/voices/zls/hr | (none) | 290 | text |  |
| espeak-ng-data/voices/zls/mk | (none) | 41 | text |  |
| espeak-ng-data/voices/zls/pl | (none) | 50 | text |  |
| espeak-ng-data/voices/zls/ru | (none) | 71 | text |  |
| espeak-ng-data/voices/zls/sk | (none) | 37 | text |  |
| espeak-ng-data/voices/zls/sl | (none) | 43 | text |  |
| espeak-ng-data/voices/zls/sr | (none) | 277 | text |  |
| espeak-ng-data/zh_dict | (none) | 1067075 | binary | No active loader references. |
| espeak-ng-data/zhy_dict | (none) | 481709 | binary | No active loader references. |
| espeak.dll | .dll | 529920 | binary | No active loader references. |
| speechPlayerInEspeak.py | .py | 7278 | text |  |

