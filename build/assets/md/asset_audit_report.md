# Synthesizer asset audit

This audit reflects the NVDA community fork of ETI Eloquence 6.1 and our push to keep
classic Klatt-era synthesizers such as DECtalk and FonixTalk alive alongside eSpeak NG
and NV Speech Player voices.  By aligning editable resources with ``assets`` and pushing
bulk runtime binaries into ``speechdata`` we make it easier to ship `eloquence.nvda-addon`
while following CodeQL-friendly packaging expectations.

## Context and follow-up

- Keep README and offline packaging guides in sync with NVDA upstream (https://github.com/nvaccess/nvda/).
  Refresh cached downloads with ``python tools/audit_nvaccess_downloads.py --roots releases/stable releases/2024.3 snapshots/alpha --max-depth 2 --limit-per-dir 12 --insecure --json docs/download_nvaccess_snapshot.json --markdown docs/download_nvaccess_snapshot.md`` before running ``python build.py --insecure --no-download --output dist/eloquence.nvda-addon``.
- When updating locale templates or phoneme data, pair this inventory with ``python tools/report_language_progress.py --json docs/language_progress.json --markdown docs/language_progress.md --print`` so contributors see
  how far the 42 seeded locales (Arabic through Finnish) have progressed.
- Use ``python tools/report_voice_parameters.py --json docs/voice_parameter_report.json --markdown docs/voice_parameter_report.md --print``
  to keep slider metadata aligned with the phoneme customiser and NV Speech Player mappings.

## Synthesizer breakdown

| Synthesizer | Files | Size (MiB) |
|-------------|-------|------------|
| dectalk | 28 | 9.85 |
| eloquence | 74 | 51.69 |
| espeak-ng | 5063 | 335.53 |
| fonix | 2 | 0.36 |
| ibm tts | 2 | 1.46 |
| klatt | 1 | 0.00 |
| nv speech player | 13 | 0.51 |
| nvda | 15 | 0.32 |
| sam | 40 | 1.52 |
| svox pico | 14 | 6.50 |
| unspecified | 660 | 192.16 |

## Priority mix

| Priority | Files | Size (MiB) |
|----------|-------|------------|
| high | 4786 | 35.36 |
| medium | 679 | 10.25 |
| low | 447 | 554.30 |

## Usefulness overview

| Usefulness | Files | Size (MiB) |
|------------|-------|------------|
| archive | 21 | 6.01 |
| core-editable | 4535 | 27.39 |
| reference | 499 | 10.56 |
| runtime-binary | 857 | 555.95 |

## Action outcomes

| Action | Files | Size (MiB) |
|--------|-------|------------|
| relocate-to-assets | 4765 | 29.36 |
| relocate-to-speechdata | 21 | 6.01 |
| retain-in-assets | 269 | 8.59 |
| retain-in-speechdata | 857 | 555.95 |

## Extension footprint

The following breakdown highlights which file extensions dominate the inventory so we can
target consolidation work for editable materials before merging synthesizer code paths.

| Extension | Files | Size (MiB) |
|-----------|-------|------------|
| <no extension> | 3928 | 321.73 |
| .wav | 408 | 3.59 |
| .png | 230 | 5.17 |
| .xml | 136 | 0.34 |
| .py | 101 | 1.01 |
| .scm | 99 | 6.17 |
| .md | 93 | 1.90 |
| .dll | 63 | 28.21 |
| .txt | 63 | 0.53 |
| .ini | 62 | 0.25 |
| .h | 58 | 0.25 |
| .c | 56 | 1.74 |
| .java | 56 | 0.46 |
| .vcx | 55 | 88.49 |
| .hlp | 52 | 6.96 |
| .json | 48 | 2.92 |
| .cnt | 36 | 0.06 |
| .syn | 36 | 41.47 |
| .tts | 25 | 3.54 |
| .phm | 24 | 0.01 |
| .yml | 21 | 0.04 |
| .bin | 20 | 6.75 |
| .chm | 20 | 4.19 |
| .doc | 20 | 5.88 |
| .test | 17 | 0.11 |
| .dic | 13 | 2.63 |
| .uil | 13 | 0.95 |
| .cpp | 10 | 0.03 |
| .ssml | 10 | 0.00 |
| .cmake | 8 | 0.01 |
| .expected | 8 | 0.00 |
| .js | 8 | 0.03 |
| .properties | 7 | 0.00 |
| .sh | 6 | 0.00 |
| .html | 5 | 1.68 |
| .gradle | 4 | 0.01 |
| .svg | 4 | 0.00 |
| .ac | 3 | 0.03 |
| .am | 3 | 0.07 |
| .exe | 3 | 0.23 |
| .filters | 3 | 0.01 |
| .group | 3 | 39.19 |
| .in | 3 | 0.00 |
| .m4 | 3 | 0.01 |
| .ngrambin | 3 | 0.17 |
| .ucd | 3 | 0.01 |
| .vcxproj | 3 | 0.06 |
| .vim | 3 | 0.01 |
| .apache | 2 | 0.02 |
| .bat | 2 | 0.01 |
| .bsd2 | 2 | 0.00 |
| .dat | 2 | 14.36 |
| .def | 2 | 0.00 |
| .dtd | 2 | 0.01 |
| .ico | 2 | 0.00 |
| .idl | 2 | 0.00 |
| .jar | 2 | 0.08 |
| .jpg | 2 | 0.01 |
| .mo | 2 | 0.00 |
| .nanorc | 2 | 0.00 |
| .out | 2 | 4.87 |
| .po | 2 | 0.01 |
| .pyo | 2 | 0.01 |
| .ronn | 2 | 0.01 |
| .voice | 2 | 0.00 |
| .cjk | 1 | 0.06 |
| .cmd | 1 | 0.00 |
| .conf | 1 | 0.01 |
| .cs | 1 | 0.00 |
| .css | 1 | 0.00 |
| .csv | 1 | 0.79 |
| .diff | 1 | 0.12 |
| .el | 1 | 0.01 |
| .ent | 1 | 0.01 |
| .exc | 1 | 0.01 |
| .gram | 1 | 0.02 |
| .pdf | 1 | 1.26 |
| .poslex | 1 | 0.00 |
| .poslexr | 1 | 1.16 |
| .pyc | 1 | 0.01 |
| .rtf | 1 | 0.04 |
| .sln | 1 | 0.00 |
| .ssml2 | 1 | 0.00 |
| .sys | 1 | 0.00 |
| .wixproj | 1 | 0.00 |
| .wxs | 1 | 0.13 |
| .yaml | 1 | 0.00 |

## Consolidation targets

Editable resources currently parked under ``speechdata`` need to move into ``assets`` before
we can merge Eloquence, eSpeak NG, and NV Speech Player logic into unified modules.  Focus on
the synthesizer/category pairs below to unblock that consolidation work.

| Synthesizer | Category | Files | Size (MiB) |
|-------------|----------|-------|------------|
| eloquence | ico | 2 | 0.00 |
| eloquence | uil | 1 | 0.06 |
| espeak-ng | unknown | 3693 | 17.78 |
| espeak-ng | text | 428 | 3.54 |
| espeak-ng | png | 226 | 4.83 |
| espeak-ng | test | 17 | 0.11 |
| espeak-ng | ssml | 10 | 0.00 |
| espeak-ng | cmake | 8 | 0.01 |
| espeak-ng | expected | 8 | 0.00 |
| espeak-ng | properties | 6 | 0.00 |
| espeak-ng | gradle | 4 | 0.01 |
| espeak-ng | svg | 4 | 0.00 |
| espeak-ng | ac | 3 | 0.03 |
| espeak-ng | am | 3 | 0.07 |
| espeak-ng | filters | 3 | 0.01 |
| espeak-ng | m4 | 3 | 0.01 |
| espeak-ng | ucd | 3 | 0.01 |
| espeak-ng | vcxproj | 3 | 0.06 |
| espeak-ng | vim | 3 | 0.01 |
| espeak-ng | apache | 2 | 0.02 |
| espeak-ng | bat | 2 | 0.01 |
| espeak-ng | bsd2 | 2 | 0.00 |
| espeak-ng | idl | 2 | 0.00 |
| espeak-ng | in | 2 | 0.00 |
| espeak-ng | jar | 2 | 0.08 |
| espeak-ng | jpg | 2 | 0.01 |
| espeak-ng | nanorc | 2 | 0.00 |
| espeak-ng | ronn | 2 | 0.01 |
| espeak-ng | conf | 1 | 0.01 |
| espeak-ng | def | 1 | 0.00 |
| espeak-ng | rtf | 1 | 0.04 |
| espeak-ng | sln | 1 | 0.00 |
| espeak-ng | ssml2 | 1 | 0.00 |
| espeak-ng | wixproj | 1 | 0.00 |
| klatt | scm | 1 | 0.00 |
| nvda | mo | 2 | 0.00 |
| nvda | po | 2 | 0.01 |
| sam | text | 37 | 0.05 |
| unspecified | scm | 95 | 0.95 |
| unspecified | vcx | 50 | 0.61 |
| unspecified | text | 38 | 0.32 |
| unspecified | phm | 24 | 0.01 |
| unspecified | cnt | 20 | 0.04 |
| unspecified | tts | 17 | 0.49 |
| unspecified | unknown | 9 | 0.03 |
| unspecified | dtd | 2 | 0.01 |
| unspecified | ngrambin | 2 | 0.03 |
| unspecified | pyo | 2 | 0.01 |
| unspecified | cs | 1 | 0.00 |
| unspecified | def | 1 | 0.00 |
| unspecified | el | 1 | 0.01 |
| unspecified | ent | 1 | 0.01 |
| unspecified | exc | 1 | 0.01 |
| unspecified | gram | 1 | 0.02 |
| unspecified | in | 1 | 0.00 |
| unspecified | out | 1 | 0.01 |
| unspecified | poslex | 1 | 0.00 |
| unspecified | properties | 1 | 0.00 |
| unspecified | pyc | 1 | 0.01 |
| unspecified | sys | 1 | 0.00 |

## Duplicate payloads

Use the digest-matched entries below to deduplicate archives before packaging the NVDA add-on.
This keeps the repo lean while still capturing references for contextual voice design.

| SHA-256 | Files | Size (MiB) | Synthesizers | Example path |
|---------|-------|------------|--------------|--------------|
| `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 16 | 0.00 | espeak-ng, unspecified | `speechdata/espeak-ng-1.52.0/dictsource/chr_list` |
| `fc8d3775b57186ef5e03aa0f1ed0f7128cfc38509a63fdb1e85eb6383de1e6ce` | 14 | 0.02 | sam | `speechdata/orpheus/orpheus/sam/Dso00020.ini` |
| `2eaade658d04d2b7e2834117c45f44d21533df147542e1cb102c15f987093380` | 9 | 1.83 | unspecified | `speechdata/orpheus/orpheus/ORP00001.HLP` |
| `b7c00244002f123199dd254a4a13c0598a63272b7c2fb9986878682828ad3d54` | 9 | 1.54 | unspecified | `speechdata/orpheus/orpheus/ORP00001.CHM` |
| `7707da56806c642baa6d5f38e05b5444fb88416684bc5df592754cb20ae8e15d` | 8 | 0.01 | sam | `speechdata/orpheus/orpheus/sam/Dso00001.ini` |
| `b09eb6659480cb7e3b3fa69f47284c0ff8e1c7755749c957238a6cc5ebbdc859` | 6 | 1.58 | unspecified | `speechdata/orpheus/orpheus/docs/ORP00001.DOC` |
| `acb89e63e3e952a63e8f824705f38edd51c9619f6c4c9f37703c62cc409c9761` | 6 | 0.06 | espeak-ng | `speechdata/espeak-ng-1.52.0/dictsource/bs_list` |
| `af786a4f267db0034d3990581a6382fb1cacb962794476c9d22fc4ccb2092469` | 6 | 0.02 | espeak-ng | `speechdata/espeak-ng-1.52.0/dictsource/bs_rules` |
| `428091a6b403807b473b16d0cad27a2e7442140f3e27716a1ced7dc653013e4c` | 6 | 0.01 | unspecified | `speechdata/orpheus/orpheus/ORP00001.CNT` |
| `11a677d9093cb5e539091cd57b2c6dd13cc0d41c26abdfe535865fbab7b5bc95` | 4 | 0.09 | espeak-ng | `speechdata/espeak-ng-1.52.0/phsource/myanmar/a34` |
| `51a89071698f2006a052615a9d1172900d5f7d6f709c7b00f4a2ba697625c909` | 4 | 0.08 | espeak-ng | `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/es-la.png` |
| `494b677c2ecdf300cb807117916f48f3f4f972dd1e4b69993263b0b8eff826ba` | 4 | 0.06 | espeak-ng | `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/base.png` |
| `d626bee183cc7bdcc72fe719ac2e0c7e6b43920908e09485d07002b78d1403bb` | 4 | 0.04 | espeak-ng | `speechdata/espeak-ng-1.52.0/phsource/klatt/n_n^/n^_` |
| `91152ecb574be9cf1968b61f1eac13932cdfe8d6823092dfd76a821917144752` | 4 | 0.04 | espeak-ng | `speechdata/espeak-ng-1.52.0/phsource/klatt/n_n^/n^#_` |
| `4ee9504c418e1ade70a0ac62a1fce25559f5abcc5af9eec702cd9c6c5346801a` | 4 | 0.02 | espeak-ng | `speechdata/espeak-ng-1.52.0/phsource/ufric/x.wav` |
| `607702d3715119e62d31eb74eedbf3ed046790e2fd419c59f7542605d8cfee40` | 4 | 0.01 | espeak-ng | `speechdata/espeak-ng-1.52.0/phsource/ph_bashkir` |
| `4e78c3be0d7fa40d054f426e05e0f652abc34b6d87bbac8d26727d72d391d798` | 4 | 0.01 | espeak-ng | `speechdata/espeak-ng-1.52.0/phsource/klatt/n` |
| `f5b79aadf133029b2557be6a03e5cd3e27525e9ac443c43fdfde189cf7e8e726` | 4 | 0.01 | espeak-ng | `speechdata/espeak-ng-1.52.0/phsource/klatt/m` |
| `de2ae3eb2c372060b4f77a6f3f1770df59dde9057586e6353d3ff895fba6daad` | 4 | 0.01 | espeak-ng | `speechdata/espeak-ng-1.52.0/phsource/m/m-syl` |
| `d04c4adae7f3aea8c597694d0ab3de03009e18cf93b8f6afcd27666b3a421de9` | 4 | 0.01 | espeak-ng | `speechdata/espeak-ng-1.52.0/phsource/myanmar/t_hi.wav` |
| `5306a143bc5aba60b6f0cdbf6476a6890fe3dc90b96894f9dd72d21009ae6173` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/fi` |
| `89cafb6404c255f3176c940c0402bc407bdf01832802cd8b978e49fa5671bd43` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/phsource/n/n-syl` |
| `8cebd3cd81694646011d39354b3e3d45343a96d7858e4bd42e3fce9be381a7fe` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-ir1` |
| `62c78bd1b08a3eb2a02bf8b27aa1ddb06e82e124ec1ac64d8fd8c3590b8ac715` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/phsource/klatt/n_n^/_n^` |
| `f7f3a3ddceed4081764cfc4c3b39329ca8f9197b2204e396910949e65ff6de62` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/base` |
| `2a644b8ceb0d177f0c96eb707bdb0a66487ee75af8e7623954a2a16b64ba272f` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/es` |
| `796fc7e7cb73322dd26102e270c55d1ce754702d9f6f76ba2abf3d2397783b94` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-us3` |
| `63ea6b18456f022ae2cf80c1d0c0ec9d324575cf388eb4d6057f507b433bc669` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-us2` |
| `03b30d4c8b571c48df3be931dae2bb6f10d683821df0e0dac612ebbae351ba32` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-us1` |
| `6d6f27286476035298926ef3caf242ff37d6fdf8dda3e95d4e2b5776468d3004` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-it4` |
| `4bd9cd1244c71b583fe8279bb8c092ddaca61873ce76b19a9d78a8731b97eedc` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-vz1` |
| `ac301735de92fdf11d9f76a013eb5a25042cafa40fe7f276fe27326b1cf20f56` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-it3` |
| `4130e2c6168a5ebcb98a595e8a7c569d0d5ebb1f8da0622f07accc86894181d2` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-mx1` |
| `b20de9d7df7fd34a8f462245e78156e4b3d2fafdd3db1da04ac5d4d2e35070c4` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-mx2` |
| `a0f57dfa06053452d3cc2a343e00e2717a7de11f6ff516507e7406cba70fc277` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-tr2` |
| `1db8241a935ecd6a6b5e4ced906021a86535e68047fbbd91b20adbfbc5c68f81` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-hu1` |
| `75a3b9f171f2e6681cb6656e1b9198fee6d1a6ad5c025dc52e056b37a0b5a40e` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-sw2` |
| `351d13dee787052313d55f3762f3633b35c736348ecbb3e76914c9893f816e81` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-id1` |
| `1b092a60c374081f2c9bac3d09bdeea6f97e821d7261fbb530db161505c63783` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-pl1` |
| `42bfce7cea2a5f31e08f29a46885b741909ff2fb60badab5988b114a3bd81064` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-de3` |
| `49cf98f88639db8c000fddd24af4dc6c48da571fce063d41a39a165b02b72166` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-sw2-en` |
| `6263ef96f906154d2a4b9d7ab385239a3d48a7f929932beb8342a45e1c46aea0` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-sw1` |
| `4a36dfce2aee32e2675feddc71ef8cd253a504cbe1ea81024867a2d7de158fac` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-hu1-en` |
| `04c3b361ab3f1fda090f39e17a8b5ef7acdf9de20a3d332f30802cfc3d95877b` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-nl2` |
| `cbbcb9184cc8d2b6193e29a27b428a4860d647eeda8c04cbfb2f6b21ad2024a1` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-sw1-en` |
| `a7428804c19a26ba3340a235506341ed212ae7bdd7c87fc9a6e52a2eed7c25cf` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-nl2-en` |
| `fcbf3863ac3b6bf117145a50699138de5a3426487eb2f69535300136aa6ff6f1` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-de5-en` |
| `62ed7f850ff2871582fbcda1cf88954da64b5338ef11b325a74a2a01cefbbc3c` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-af1` |
| `b69b92a118b367edff28839e49dac2608da570ae3c9f5d670481ab1c595e1264` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-gr2-en` |
| `3b0923ea8affeaa73a7c658d7c7f44beb7f47ff32ba48be3a71fd469c69359dd` | 4 | 0.00 | espeak-ng | `speechdata/espeak-ng-1.52.0/espeak-ng-data/voices/mb/mb-ro1` |

_Showing 50 of 2029 duplicate groups.  Export the full JSON manifest for the complete list._

## Prioritised action list

Use this table to drive incremental clean-ups.  It combines relocation guidance
with usefulness scoring so we can focus on high-impact edits first.

| Path | Priority | Action | Synth | Editable | Notes |
|------|----------|--------|-------|----------|-------|
| `speechdata/espeak-ng-1.52.0/src/ucd-tools/src/scripts.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/ucd-tools/src/categories.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/ucd-tools/src/proplist.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/ucd-tools/src/case.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/festival/festival/lib/dicts/cmu/cmudict-0.4.diff` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/dictionary.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/tr_languages.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/compiledata.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/lv_rules` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/lv_rules` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vdiph/aau_4` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/vdiph/aau_4` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/eloquence/uil/ENU.UIL` | high | relocate-to-assets | eloquence | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vdiph/ai_4` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/vdiph/ai_4` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/myanmar/a2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/myanmar/a2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vwl_de/y#` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vdiph/ui_2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/vdiph/ui_2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/it_listx` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/it_listx` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/ur_list` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/ur_list` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/orpheus/orpheus/Language/00030/00030.TTS` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-1.52.0/phsource/vietnam/e_short_1` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/vietnam/e_short_1` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vdiph2/iu_3` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/vdiph2/iu_3` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/bg_listx` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/bg_listx` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vwl_no/y#` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vdiph/0i_2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/vdiph/0i_2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vdiph/ooi_2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/vdiph/ooi_2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/translate.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/vdiph2.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/vdiph2.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/orpheus/orpheus/Language/00049/00049.TTS` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-1.52.0/phsource/vdiph/oi_2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/vdiph/oi_2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/ti_emoji` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/ti_emoji` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/r2/r2@` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/r2/r2e` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/r2/r2u` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/r2/r2@` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/r2/r2e` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/r2/r2u` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/orpheus/orpheus/Language/00033/00033.TTS` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-1.52.0/phsource/vdiph/aai_2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vdiph/aai_3` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/vdiph/aai_2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/vdiph/aai_3` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/numbers.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/ucd-tools/src/include/ucd/ucd.h` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/vi.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/vi.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/smj_list` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/smj_list` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/r2/_r2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/r2/_r2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/ps_rules` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/fr_rules` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/fr_rules` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vwl_no/y` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/vi-sgn.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/vi-sgn.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/windows/data.vcxproj` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/speechplayerinespeak/espeak-ng-data/phontab` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/vi-hue.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/vi-hue.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vdiph/Vu` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/vdiph/Vu` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/android/gradle/wrapper/gradle-wrapper.jar` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/android/gradle/wrapper/gradle-wrapper.jar` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/tests/language-pronunciation.test` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/pl_list` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/pl_list` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/myanmar/a21` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/myanmar/a21` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vwl_no/i` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vwl_no/aU` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/src/com/reecedunn/espeak/test/VoiceSettingsTest.java` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/android/eSpeakTests/src/com/reecedunn/espeak/test/VoiceSettingsTest.java` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vwl_hi/l-voc` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/synthesize.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/mbrulainespeak/espeak-data/phontab` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/myanmar/a12` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/myanmar/a47` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/myanmar/a12` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/myanmar/a47` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/compiledict.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/en-us.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/en-us.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/wavegen.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vowel/aa_3` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/ca_rules` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/ca_rules` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/voices.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/yue_list` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/yue_list` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/myanmar/a50` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/myanmar/a50` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/en.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/en.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/tests/encoding.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/windows/installer/License_GPLv3.rtf` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/zh.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/zh.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/en-wm.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/en-wm.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/en-sc.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/en-sc.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/encoding.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/pt_list` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/pt_list` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/orpheus/orpheus/Language/00370/00370.TTS` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-1.52.0/phsource/vwl_no/au-` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/en-wi.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/en-wi.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/myanmar/a15` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/myanmar/a15` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/translateword.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/j2/j2a` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/l^/j2a` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/j2/j2a` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/l^/j2a` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/en-rp.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/en-rp.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/zhy.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/zhy.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/intonation.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/phonemes` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/en-n.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/en-n.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/cmn_list` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/cmn_list` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/phonemes` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vwl_es/ooi` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/festival/festival/lib/apml_kaldurtreeZ.scm` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/festival/festival/lib/tobi_rules.scm` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/af.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/af.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/festival/festival/lib/gswdurtreeZ.scm` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/festival/festival/lib/voices/english/kal_diphone/festvox/kaldurtreeZ.scm` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/festival/festival/lib/voices/english/ked_diphone/festvox/kddurtreeZ.scm` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-1.52.0/phsource/vdiph2/o@` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/vdiph2/o@` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/COPYING` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/ucd-tools/COPYING` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/COPYING` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/mbrulainespeak/espeak-data/pl_dict` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/de_rules` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/de_rules` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/festival/festival/lib/sec.ts20.quad.ngrambin` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/speechplayerinespeak/espeak-ng-data/pl_dict` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/festival/festival/lib/f2bdurtreeZ.scm` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-1.52.0/tests/language-phonemes.test` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/myanmar/a42` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/myanmar/a42` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/ro.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/ro.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/Makefile.am` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/klatt.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/orpheus/orpheus/Language/00040/00040.TTS` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-1.52.0/dictsource/af_list` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/af_list` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/pt.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/pt.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/Makefile.am` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/myanmar/a03` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/myanmar/a03` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/festival/festival/lib/tilt.scm` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-1.52.0/phsource/myanmar/a13` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/myanmar/a13` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/mt.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/mt.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/ne.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/ne.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/lt.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/lt.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/translate.h` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vdiph/i@_2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/vdiph/i@_2` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/vwl_en/ooi@` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/pt-pt.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/pt-pt.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/ssml.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/phsource/myanmar/a19` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/phsource/myanmar/a19` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/readclause.c` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/orpheus/orpheus/Language/00036/00036.TTS` | high | relocate-to-assets | unspecified | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-1.52.0/docs/phonemes/vowelcharts/fi.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/docs/phonemes/vowelcharts/fi.png` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/ur_rules` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/ur_rules` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/dictsource/pt_rules` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-master/dictsource/pt_rules` | high | relocate-to-assets | espeak-ng | yes | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |

_Showing 200 of 5912 prioritised actions.  Use ``python tools/audit_assets.py --full-json assets/md/asset_audit_full.json`` for the entire list._

## Relocation priorities

The table below only lists files whose current root directory (``assets`` or ``speechdata``)
does not match the recommended location.  Use these entries to plan incremental clean-ups
without committing the entire 50k-line manifest.

| Path | Synthesizer | Category | Editable | Suggested home |
|------|-------------|----------|----------|----------------|
| `speechdata/brailab/compiled/brailab.pyo` | unspecified | pyo | yes | assets |
| `speechdata/eloquence/ico/appldocv.ico` | eloquence | ico | yes | assets |
| `speechdata/eloquence/ico/etipad.ico` | eloquence | ico | yes | assets |
| `speechdata/eloquence/uil/ENU.UIL` | eloquence | uil | yes | assets |
| `speechdata/espeak-ng-1.52.0/.github/dependabot.yml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/.github/workflows/android.yml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/.github/workflows/autoconf.yml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/.github/workflows/ci.yml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/.github/workflows/dist.yml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/.github/workflows/fuzzing.yml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/.github/workflows/gradle-wrapper-validation.yml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/.github/workflows/windows-msbuild.yml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/.github/workflows/windows.yml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/.gitignore` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/.tx/config` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/COPYING` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/COPYING.APACHE` | espeak-ng | apache | yes | assets |
| `speechdata/espeak-ng-1.52.0/COPYING.BSD2` | espeak-ng | bsd2 | yes | assets |
| `speechdata/espeak-ng-1.52.0/COPYING.UCD` | espeak-ng | ucd | yes | assets |
| `speechdata/espeak-ng-1.52.0/ChangeLog.md` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/Makefile.am` | espeak-ng | am | yes | assets |
| `speechdata/espeak-ng-1.52.0/README.md` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/AndroidManifest.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/build.gradle` | espeak-ng | gradle | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/.classpath` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/AndroidManifest.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/project.properties` | espeak-ng | properties | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/res/drawable-hdpi/ic_launcher.png` | espeak-ng | png | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/res/drawable-ldpi/ic_launcher.png` | espeak-ng | png | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/res/drawable-mdpi/ic_launcher.png` | espeak-ng | png | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/res/drawable-xhdpi/ic_launcher.png` | espeak-ng | png | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/res/values/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/src/com/reecedunn/espeak/test/CheckVoiceDataTest.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/src/com/reecedunn/espeak/test/SpeechSynthesisTest.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/src/com/reecedunn/espeak/test/TextToSpeechServiceTest.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/src/com/reecedunn/espeak/test/TextToSpeechTest.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/src/com/reecedunn/espeak/test/TextToSpeechTestCase.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/src/com/reecedunn/espeak/test/TtsMatcher.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/src/com/reecedunn/espeak/test/VoiceData.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/src/com/reecedunn/espeak/test/VoiceSettingsTest.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/eSpeakTests/src/com/reecedunn/espeak/test/VoiceVariantTest.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/gradle.properties` | espeak-ng | properties | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/gradle/wrapper/gradle-wrapper.jar` | espeak-ng | jar | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/gradle/wrapper/gradle-wrapper.properties` | espeak-ng | properties | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/gradlew` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/gradlew.bat` | espeak-ng | bat | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/icons/launcher.svg` | espeak-ng | svg | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/icons/promo-graphic.svg` | espeak-ng | svg | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/jni/include/Log.h` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/jni/jni/eSpeakService.c` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/remove_string.sh` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/drawable/icon_foreground.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/layout/download_voice_data.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/layout/import_voice_preference.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/layout/information_view.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/layout/main.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/layout/seekbar_preference.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/layout/speak_punctuation_preference.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/layout/voice_variant_preference.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/menu/options.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/mipmap-anydpi-v26/icon.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/mipmap-hdpi/icon.png` | espeak-ng | png | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/mipmap-mdpi/icon.png` | espeak-ng | png | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/mipmap-xhdpi/icon.png` | espeak-ng | png | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/mipmap-xxhdpi/icon.png` | espeak-ng | png | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/mipmap-xxxhdpi/icon.png` | espeak-ng | png | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-af/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-am/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-ar/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-bg/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-ca/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-cs/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-da/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-de/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-el/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-en-rGB/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-es-rUS/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-es/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-fa/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-fi/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-fr/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-hi/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-hr/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-hu/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-in/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-it/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-iw/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-ja/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-ko/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-lt/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-lv/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-ms/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-nb/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-nl/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-pl/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-pt-rBR/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-pt/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-ro/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-ru/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-sk/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-sl/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-sr/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-sv/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-sw/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-th/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-tl/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-tr/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-uk/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-v21/styles.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-vi/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-zh-rCN/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-zh-rTW/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values-zu/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values/donottranslate.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values/icon_background.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values/strings.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/values/styles.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/xml/preferences.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/res/xml/tts_engine.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/settings.gradle` | espeak-ng | gradle | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/CheckVoiceData.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/DownloadVoiceData.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/EspeakApp.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/FileListAdapter.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/FileUtils.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/GetSampleText.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/InformationListAdapter.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/ResourceIdListAdapter.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/SpeechSynthesis.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/TtsService.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/TtsSettingsActivity.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/Voice.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/VoiceSettings.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/VoiceVariant.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/eSpeakActivity.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/preference/ImportVoicePreference.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/preference/SeekBarPreference.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/preference/SpeakPunctuationPreference.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/android/src/com/reecedunn/espeak/preference/VoiceVariantPreference.java` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/autogen.sh` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/cmake/data.cmake` | espeak-ng | cmake | yes | assets |
| `speechdata/espeak-ng-1.52.0/cmake/deps.cmake` | espeak-ng | cmake | yes | assets |
| `speechdata/espeak-ng-1.52.0/cmake/docs.cmake` | espeak-ng | cmake | yes | assets |
| `speechdata/espeak-ng-1.52.0/cmake/package.cmake` | espeak-ng | cmake | yes | assets |
| `speechdata/espeak-ng-1.52.0/configure.ac` | espeak-ng | ac | yes | assets |
| `speechdata/espeak-ng-1.52.0/data/annotationsEspeak/de.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/data/annotationsEspeak/en.xml` | espeak-ng | text | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/af_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/am_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/am_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/an_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/an_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/ar_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/ar_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/as_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/as_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/az_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/az_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/ba_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/ba_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/be_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/be_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/bg_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/bg_listx` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/bg_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/bn_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/bn_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/bpy_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/bpy_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/bs_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/bs_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/ca_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/chr_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/chr_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/cmn_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/cmn_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/cs_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/cs_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/cv_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/cv_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/cy_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/cy_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/de_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/de_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/el_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/el_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/eo_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/eo_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/es_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/es_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/et_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/et_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/eu_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/eu_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/fi_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/fi_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/fo_emoji` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/fo_rules` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/fr_list` | espeak-ng | unknown | yes | assets |
| `speechdata/espeak-ng-1.52.0/dictsource/fr_rules` | espeak-ng | unknown | yes | assets |

_Showing 200 of 4786 candidates.  Run ``python tools/audit_assets.py --full-json assets/md/asset_audit_full.json`` to export the complete manifest._

## Largest editable assets

The table below highlights the largest editable resources tracked under version control.
Use these entries to plan modularisation work, split oversized manifests, or migrate
language packs into shared utility modules before packaging the NVDA add-on.

| Path | Synthesizer | Size (MiB) | Notes |
|------|-------------|------------|-------|
| `assets/html/wikipedia_languages.html` | unspecified | 1.65 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/json/archive_inventory.json` | unspecified | 0.95 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/csv/wikipedia_languages.csv` | unspecified | 0.79 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/md/archive_inventory.md` | unspecified | 0.37 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/md/asset_audit_report.json` | unspecified | 0.28 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-1.52.0/src/ucd-tools/src/scripts.c` | espeak-ng | 0.26 | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `assets/json/binary_asset_index.json` | unspecified | 0.25 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/txt/building_ibm_tts.txt` | ibm tts | 0.20 |  |
| `speechdata/espeak-ng-1.52.0/src/ucd-tools/src/categories.c` | espeak-ng | 0.19 | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `assets/md/README.md` | unspecified | 0.14 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/txt/datajake_archive_urls.txt` | unspecified | 0.13 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/json/voice_parameter_report.json` | unspecified | 0.13 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/json/speechdata_extensionless_inventory.json` | unspecified | 0.13 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-1.52.0/src/ucd-tools/src/proplist.c` | espeak-ng | 0.12 | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/espeak-ng-1.52.0/src/ucd-tools/src/case.c` | espeak-ng | 0.12 | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `speechdata/festival/festival/lib/dicts/cmu/cmudict-0.4.diff` | unspecified | 0.12 | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/json/language_research_index.json` | unspecified | 0.11 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/md/iso_language_expansion.md` | unspecified | 0.09 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/json/integration_scope.json` | unspecified | 0.09 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/json/language_pronunciation_validation.json` | unspecified | 0.09 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/md/asset_audit_report.md` | unspecified | 0.09 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-1.52.0/src/libespeak-ng/dictionary.c` | espeak-ng | 0.08 | Currently in speechdata; recommend staging under assets to match audit policy. Editable resource is hidden in speechdata; move so version control can track diffs. |
| `assets/md/voice_parameter_report.md` | unspecified | 0.08 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/py/seed_language_profiles.py` | unspecified | 0.08 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `assets/json/world_language_seeds.json` | unspecified | 0.08 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |

## Largest archival payloads

These entries surface the heaviest runtime binaries or speech corpora currently staged
under ``speechdata``.  Use them to schedule extraction or recompression passes while
keeping CodeQL-friendly source assets in ``assets``.

| Path | Synthesizer | Size (MiB) | Notes |
|------|-------------|------------|-------|
| `speechdata/festival/festival/lib/voices/czech/czech_ph/group/ph.group` | unspecified | 27.97 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/espeak-ng-master/dictsource/extra/ru_listx` | espeak-ng | 22.67 |  |
| `speechdata/espeak-ng-1.52.0/dictsource/extra/ru_listx` | espeak-ng | 22.15 |  |
| `speechdata/mbrulainespeak/espeak-data/mbrola/de4` | espeak-ng | 21.24 |  |
| `speechdata/orpheus/orpheus/Language/00044/Carol.vcx` | unspecified | 18.82 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/orpheus/orpheus/Language/00001/Lucy.vcx` | unspecified | 18.80 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/orpheus/orpheus/Language/00044/Alan.vcx` | unspecified | 17.23 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/orpheus/orpheus/Language/00046/anders.vcx` | unspecified | 16.53 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/orpheus/orpheus/Language/00001/Brad.vcx` | unspecified | 16.51 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/mbrulainespeak/espeak-data/mbrola/nl2` | espeak-ng | 14.49 |  |
| `speechdata/mbrulainespeak/espeak-data/mbrola/ee1` | espeak-ng | 11.57 |  |
| `speechdata/mbrulainespeak/espeak-data/mbrola/ic1` | espeak-ng | 11.48 |  |
| `speechdata/mbrulainespeak/espeak-data/mbrola/sw1` | espeak-ng | 11.01 |  |
| `speechdata/mbrulainespeak/espeak-data/mbrola/de2` | espeak-ng | 9.96 |  |
| `speechdata/mbrulainespeak/espeak-data/mbrola/cz2` | espeak-ng | 9.36 |  |
| `speechdata/mbrulainespeak/espeak-data/mbrola/hu1` | espeak-ng | 8.51 |  |
| `speechdata/mbrulainespeak/espeak-data/mbrola/la1` | espeak-ng | 8.23 |  |
| `speechdata/mbrulainespeak/espeak-data/mbrola/af1` | espeak-ng | 7.68 |  |
| `speechdata/newfon/bin/dict.dat` | unspecified | 7.24 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/newfon/dict.dat` | unspecified | 7.12 | Synthesizer family undetected—tag the path or relocate next to known assets for clarity. |
| `speechdata/mbrulainespeak/espeak-data/mbrola/us3` | espeak-ng | 7.07 |  |
| `speechdata/mbrulainespeak/espeak-data/mbrola/us1` | espeak-ng | 6.90 |  |
| `speechdata/mbrulainespeak/espeak-data/mbrola/us2` | espeak-ng | 6.75 |  |
| `speechdata/mbrulainespeak/espeak-data/mbrola/it3` | espeak-ng | 6.47 |  |
| `speechdata/mbrulainespeak/espeak-data/mbrola/en1` | espeak-ng | 6.41 |  |

_Review the JSON manifest for the full archival list if additional triage is needed._
