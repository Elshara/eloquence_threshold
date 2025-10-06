# Speechdata extensionless audit

This report lists every file under ``speechdata/`` without an extension. Use it alongside [`assets/md/speechdata_manifest.md`](speechdata_manifest.md) when planning migrations so NVDA packaging drills and CodeQL scans retain access to cached datasets.

## Summary by top-level subtree

| Subtree | Files | Size |
| --- | ---: | ---: |
| `festival` | 9 | 34.1 KiB |
| `mbrulainespeak` | 197 | 218.2 MiB |
| `speechplayerinespeak` | 292 | 5.4 MiB |

## Summary by classification

| Classification | Files | Size | Suggested extension |
| --- | ---: | ---: | --- |
| `binary/unknown` | 225 | 223.4 MiB | — |
| `text/unknown` | 7 | 13.1 KiB | `txt` |
| `text/utf-8` | 265 | 107.0 KiB | `txt` |
| `text/utf-8-bom` | 1 | 256 B | `txt` |

## File-level detail

| Path | Size | Classification | Suggested extension | Notes |
| --- | ---: | --- | --- | --- |
| `festival/festival/lib/dicts/cmu/COPYING` | 2.2 KiB | `text/utf-8` | `txt` | UTF-8 text |
| `festival/festival/lib/dicts/cmu/cmu2ft` | 536 B | `text/utf-8` | `txt` | UTF-8 text |
| `festival/festival/lib/etc/email_filter` | 3.1 KiB | `text/utf-8` | `txt` | UTF-8 text |
| `festival/festival/lib/voices/czech/czech_ph/COPYING` | 17.6 KiB | `text/utf-8` | `txt` | UTF-8 text |
| `festival/festival/lib/voices/czech/czech_ph/INSTALL` | 1.3 KiB | `text/utf-8` | `txt` | UTF-8 text |
| `festival/festival/lib/voices/czech/czech_ph/Makefile` | 2.6 KiB | `text/utf-8` | `txt` | UTF-8 text |
| `festival/festival/lib/voices/czech/czech_ph/README` | 1.8 KiB | `text/utf-8` | `txt` | UTF-8 text |
| `festival/festival/lib/voices/english/kal_diphone/COPYING` | 2.6 KiB | `text/utf-8` | `txt` | UTF-8 text |
| `festival/festival/lib/voices/english/ked_diphone/COPYING` | 2.4 KiB | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/af_dict` | 80.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/am_dict` | 3.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/an_dict` | 6.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/as_dict` | 4.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/az_dict` | 2.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/bg_dict` | 26.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/bn_dict` | 9.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/ca_dict` | 4.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/cs_dict` | 7.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/cy_dict` | 3.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/da_dict` | 203.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/de_dict` | 21.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/el_dict` | 8.2 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/en_dict` | 123.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/eo_dict` | 4.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/es_dict` | 6.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/et_dict` | 6.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/eu_dict` | 4.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/fa_dict` | 227.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/fi_dict` | 5.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/fr_dict` | 20.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/ga_dict` | 8.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/gd_dict` | 3.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/grc_dict` | 3.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/gu_dict` | 5.2 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/hbs_dict` | 7.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/hi_dict` | 8.8 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/hu_dict` | 110.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/hy_dict` | 3.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/ia_dict` | 2.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/id_dict` | 3.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/intonations` | 1.2 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/is_dict` | 5.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/it_dict` | 84.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/jbo_dict` | 2.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/ka_dict` | 3.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/kl_dict` | 2.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/kn_dict` | 5.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/ko_dict` | 6.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/ku_dict` | 2.2 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/la_dict` | 3.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/lfn_dict` | 2.8 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/lt_dict` | 5.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/lv_dict` | 12.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/af1` | 7.7 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/br1` | 5.2 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/br4` | 4.9 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/cr1` | 3.4 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/cz2` | 9.4 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/de2` | 10.0 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/de4` | 21.2 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/ee1` | 11.6 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/en1` | 6.4 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/es1` | 2.7 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/fr1` | 4.8 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/hu1` | 8.5 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/ic1` | 11.5 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/id1` | 5.3 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/ir1` | 5.7 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/it3` | 6.5 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/it4` | 5.9 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/la1` | 8.2 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/mx1` | 2.2 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/mx2` | 4.0 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/nl2` | 14.5 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/pl1` | 4.5 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/ro1` | 3.6 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/sw1` | 11.0 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/sw2` | 6.3 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/tr1` | 4.5 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/us1` | 6.9 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/us2` | 6.8 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/us3` | 7.1 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola/vz1` | 2.8 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/af1_phtrans` | 1.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/ca1_phtrans` | 1.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/cr1_phtrans` | 2.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/cs_phtrans` | 580 B | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/de2_phtrans` | 1.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/de4_phtrans` | 1.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/de6_phtrans` | 1.2 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/ee1_phtrans` | 1.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/en1_phtrans` | 796 B | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/es_phtrans` | 1.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/fr1_phtrans` | 1.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/gr2_phtrans` | 2.2 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/grc-de6_phtrans` | 484 B | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/hn1_phtrans` | 532 B | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/hu1_phtrans` | 1.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/ic1_phtrans` | 1.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/id1_phtrans` | 892 B | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/in1_phtrans` | 1.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/ir1_phtrans` | 5.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/it3_phtrans` | 892 B | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/la1_phtrans` | 748 B | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/lt1_phtrans` | 1.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/lt2_phtrans` | 1.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/mx1_phtrans` | 1.8 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/mx2_phtrans` | 1.8 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/nl_phtrans` | 1.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/pl1_phtrans` | 1.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/pt1_phtrans` | 2.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/pt_phtrans` | 2.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/ptbr4_phtrans` | 2.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/ptbr_phtrans` | 2.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/ro1_phtrans` | 2.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/sv2_phtrans` | 1.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/sv_phtrans` | 1.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/tr1_phtrans` | 364 B | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/us3_phtrans` | 1.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/us_phtrans` | 1.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mbrola_ph/vz_phtrans` | 2.2 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/mk_dict` | 4.8 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/ml_dict` | 4.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/ms_dict` | 12.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/nci_dict` | 1.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/ne_dict` | 10.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/nl_dict` | 26.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/no_dict` | 4.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/or_dict` | 4.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/pa_dict` | 6.2 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/pap_dict` | 2.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/phondata` | 439.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/phondata-manifest` | 18.2 KiB | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/phonindex` | 25.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/phontab` | 40.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/pl_dict` | 34.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/pt_dict` | 25.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/ro_dict` | 24.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/ru_dict` | 1.9 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/si_dict` | 4.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/sk_dict` | 8.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/sl_dict` | 3.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/sq_dict` | 3.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/sv_dict` | 9.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/sw_dict` | 3.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/ta_dict` | 114.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/te_dict` | 3.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/tr_dict` | 5.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/ur_dict` | 24.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/vi_dict` | 7.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/voices/mb/mb-af1` | 88 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-af1-en` | 83 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-br1` | 115 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-br3` | 115 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-br4` | 119 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-cr1` | 126 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-cz2` | 82 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-de2` | 83 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-de3` | 99 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-de4` | 85 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-de4-en` | 79 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-de5` | 192 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-de5-en` | 90 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-de6` | 78 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-de6-grc` | 83 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-de7` | 106 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-ee1` | 95 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-en1` | 113 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-es1` | 97 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-es2` | 91 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-fr1` | 150 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-fr1-en` | 103 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-fr4` | 111 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-fr4-en` | 106 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-gr2` | 94 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-gr2-en` | 88 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-hu1` | 102 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-hu1-en` | 97 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-ic1` | 86 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-id1` | 101 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-ir1` | 753 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-ir2` | 768 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-it3` | 142 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-it4` | 145 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-la1` | 83 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-mx1` | 120 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-mx2` | 120 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-nl2` | 96 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-nl2-en` | 91 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-pl1` | 99 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-pl1-en` | 82 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-pt1` | 114 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-ro1` | 87 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-ro1-en` | 81 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-sw1` | 98 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-sw1-en` | 93 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-sw2` | 102 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-sw2-en` | 99 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-tr1` | 85 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-tr2` | 114 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-us1` | 170 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-us2` | 178 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-us3` | 180 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/voices/mb/mb-vz1` | 144 B | `text/utf-8` | `txt` | UTF-8 text |
| `mbrulainespeak/espeak-data/zh_dict` | 1.0 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `mbrulainespeak/espeak-data/zhy_dict` | 470.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/af_dict` | 80.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/am_dict` | 3.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/an_dict` | 6.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/as_dict` | 4.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/az_dict` | 2.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/bg_dict` | 26.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/bn_dict` | 9.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/ca_dict` | 4.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/cs_dict` | 7.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/cy_dict` | 3.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/da_dict` | 203.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/de_dict` | 21.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/el_dict` | 9.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/en_dict` | 126.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/eo_dict` | 4.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/es_dict` | 6.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/et_dict` | 6.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/eu_dict` | 4.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/fa_dict` | 232.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/fi_dict` | 5.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/fr_dict` | 21.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/ga_dict` | 8.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/gd_dict` | 3.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/gn_dict` | 3.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/grc_dict` | 3.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/gu_dict` | 5.2 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/hbs_dict` | 7.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/hi_dict` | 8.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/hu_dict` | 110.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/hy_dict` | 3.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/ia_dict` | 2.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/id_dict` | 3.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/intonations` | 1.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/is_dict` | 5.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/it_dict` | 102.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/jbo_dict` | 2.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/ka_dict` | 3.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/kl_dict` | 2.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/kn_dict` | 5.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/ko_dict` | 6.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/ku_dict` | 2.2 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/ky_dict` | 2.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/la_dict` | 3.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/lfn_dict` | 2.8 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/lt_dict` | 5.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/lv_dict` | 17.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/mk_dict` | 4.8 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/ml_dict` | 4.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/mr_dict` | 5.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/ms_dict` | 12.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/mt_dict` | 4.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/my_dict` | 1.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/nci_dict` | 1.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/ne_dict` | 10.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/nl_dict` | 26.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/no_dict` | 4.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/om_dict` | 2.2 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/or_dict` | 4.7 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/pa_dict` | 6.2 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/pap_dict` | 2.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/phondata` | 443.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/phondata-manifest` | 18.6 KiB | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/phonindex` | 28.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/phontab` | 43.2 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/pl_dict` | 33.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/pt_dict` | 25.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/ro_dict` | 24.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/ru_dict` | 1.9 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/si_dict` | 4.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/sk_dict` | 8.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/sl_dict` | 3.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/sq_dict` | 3.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/sv_dict` | 9.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/sw_dict` | 3.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/ta_dict` | 117.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/te_dict` | 3.5 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/tn_dict` | 3.0 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/tr_dict` | 5.9 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/tt_dict` | 2.1 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/ur_dict` | 24.6 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/vi_dict` | 7.3 KiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/voices/!v/Andy` | 330 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/Annie` | 298 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/AnxiousAndy` | 370 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/Denis` | 286 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/Gene` | 264 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/Gene2` | 266 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/Jacky` | 250 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/Lee` | 332 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/Mario` | 253 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/Michael` | 256 B | `text/utf-8-bom` | `txt` | UTF-8 text with BOM |
| `speechplayerinespeak/espeak-ng-data/voices/!v/Mr serious` | 3.1 KiB | `text/unknown` | `txt` | Text-like but not UTF-8 |
| `speechplayerinespeak/espeak-ng-data/voices/!v/Storm` | 397 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/Tweaky` | 3.1 KiB | `text/unknown` | `txt` | Text-like but not UTF-8 |
| `speechplayerinespeak/espeak-ng-data/voices/!v/aunty` | 368 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/boris` | 209 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/croak` | 93 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/edward` | 151 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/f1` | 324 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/f2` | 357 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/f3` | 375 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/f4` | 350 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/f5` | 425 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/iven` | 262 B | `text/unknown` | `txt` | Text-like but not UTF-8 |
| `speechplayerinespeak/espeak-ng-data/voices/!v/iven2` | 280 B | `text/unknown` | `txt` | Text-like but not UTF-8 |
| `speechplayerinespeak/espeak-ng-data/voices/!v/iven3` | 263 B | `text/unknown` | `txt` | Text-like but not UTF-8 |
| `speechplayerinespeak/espeak-ng-data/voices/!v/john` | 3.1 KiB | `text/unknown` | `txt` | Text-like but not UTF-8 |
| `speechplayerinespeak/espeak-ng-data/voices/!v/kaukovalta` | 346 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/klatt` | 38 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/klatt2` | 38 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/klatt3` | 39 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/klatt4` | 39 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/linda` | 369 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/m1` | 335 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/m2` | 264 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/m3` | 300 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/m4` | 290 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/m5` | 262 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/m6` | 188 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/m7` | 254 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/max` | 210 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/michel` | 382 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/norbert` | 3.1 KiB | `text/unknown` | `txt` | Text-like but not UTF-8 |
| `speechplayerinespeak/espeak-ng-data/voices/!v/quincy` | 334 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/rob` | 248 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/robert` | 257 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/steph` | 364 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/steph2` | 367 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/steph3` | 377 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/travis` | 360 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/whisper` | 186 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/whisperf` | 392 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/!v/zac` | 260 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/aav/vi` | 59 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/aav/vi-VN-x-central` | 211 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/aav/vi-VN-x-south` | 209 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/art/eo` | 53 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/art/ia` | 29 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/art/jbo` | 69 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/art/lfn` | 139 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/axm/hy` | 38 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/axm/hy-arevmda` | 328 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/azc/nci` | 124 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/bnt/sw` | 53 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/bnt/tn` | 54 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/ccs/ka` | 26 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/cel/cy` | 49 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/cel/ga` | 65 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/cel/gd` | 49 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/cus/om` | 39 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/default` | 38 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/dra/kn` | 55 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/dra/ml` | 69 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/dra/ta` | 63 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/dra/te` | 70 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/esx/kl` | 30 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/gmq/da` | 57 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/gmq/is` | 40 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/gmq/no` | 65 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/gmq/sv` | 38 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/gmw/af` | 67 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/gmw/de` | 38 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/gmw/en` | 136 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/gmw/en-029` | 359 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/gmw/en-GB-scotland` | 300 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/gmw/en-GB-x-gbclan` | 264 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/gmw/en-GB-x-gbcwmd` | 208 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/gmw/en-GB-x-rp` | 257 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/gmw/en-US` | 281 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/gmw/nl` | 35 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/grk/el` | 37 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/grk/grc` | 110 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/inc/as` | 42 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/inc/bn` | 37 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/inc/gu` | 42 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/inc/hi` | 35 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/inc/mr` | 41 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/inc/ne` | 49 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/inc/or` | 39 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/inc/pa` | 25 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/inc/si` | 55 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/inc/ur` | 53 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/ine/sq` | 115 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/ira/fa` | 362 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/ira/fa-Latn` | 267 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/ira/fa-en-us` | 287 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/ira/ku` | 52 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/itc/la` | 298 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/ko` | 63 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-af1` | 88 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-af1-en` | 83 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-br1` | 115 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-br2` | 119 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-br3` | 115 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-br4` | 119 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-cr1` | 126 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-cz2` | 82 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-de1` | 99 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-de1-en` | 96 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-de2` | 83 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-de2-en` | 80 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-de3` | 99 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-de3-en` | 96 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-de4` | 85 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-de4-en` | 81 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-de5` | 192 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-de5-en` | 90 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-de6` | 78 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-de6-en` | 74 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-de6-grc` | 83 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-de7` | 106 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-ee1` | 95 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-en1` | 113 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-es1` | 97 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-es2` | 91 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-fr1` | 150 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-fr1-en` | 103 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-fr4` | 111 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-fr4-en` | 106 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-gr2` | 94 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-gr2-en` | 88 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-hu1` | 102 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-hu1-en` | 97 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-ic1` | 86 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-id1` | 101 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-ir1` | 753 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-ir2` | 768 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-it3` | 142 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-it4` | 145 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-la1` | 83 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-lt1` | 88 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-lt2` | 88 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-mx1` | 120 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-mx2` | 120 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-nl2` | 96 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-nl2-en` | 91 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-pl1` | 99 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-pl1-en` | 82 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-pt1` | 114 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-ro1` | 87 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-ro1-en` | 81 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-sw1` | 98 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-sw1-en` | 93 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-sw2` | 102 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-sw2-en` | 99 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-tr1` | 85 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-tr2` | 114 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-us1` | 170 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-us2` | 178 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-us3` | 180 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/mb/mb-vz1` | 144 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/poz/id` | 146 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/poz/ms` | 457 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/roa/an` | 39 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/roa/ca` | 38 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/roa/es` | 70 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/roa/es-419` | 182 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/roa/fr` | 82 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/roa/fr-BE` | 94 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/roa/it` | 122 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/roa/pap` | 62 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/roa/pt-BR` | 106 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/roa/pt-PT` | 96 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/roa/ro` | 40 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/sai/gn` | 48 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/sem/am` | 41 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/sem/mt` | 41 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/sit/cmn` | 611 B | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/voices/sit/my` | 25 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/sit/yue` | 210 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/trk/az` | 45 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/trk/ky` | 43 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/trk/tr` | 38 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/trk/tt` | 35 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/urj/et` | 27 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/urj/fi` | 38 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/urj/hu` | 73 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/xaq/eu` | 40 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/xaq/lt` | 42 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/xaq/lv` | 235 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/zls/bg` | 110 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/zls/bs` | 257 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/zls/cs` | 36 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/zls/hr` | 290 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/zls/mk` | 41 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/zls/pl` | 50 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/zls/ru` | 71 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/zls/sk` | 37 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/zls/sl` | 43 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/voices/zls/sr` | 277 B | `text/utf-8` | `txt` | UTF-8 text |
| `speechplayerinespeak/espeak-ng-data/zh_dict` | 1.0 MiB | `binary/unknown` | — | Binary payload (no known signature) |
| `speechplayerinespeak/espeak-ng-data/zhy_dict` | 470.4 KiB | `binary/unknown` | — | Binary payload (no known signature) |

Regenerate this snapshot with ``python assets/py/report_speechdata_extensionless.py`` after migrating files. Pair it with ``python build.py --insecure --no-download --output dist/eloquence.nvda-addon`` to confirm the NVDA add-on still stages every dataset.
