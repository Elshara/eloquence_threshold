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
| unspecified | 660 | 193.84 |

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
