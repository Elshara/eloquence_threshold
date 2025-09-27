# DataJake code reuse targets

This overview highlights the DataJake archives that contain portable source code or NVDA driver modules we can adapt while
modernising Eloquence for Windows 10/11. Pair this guide with the generated manifest in `docs/archive_inventory.md` to locate
exact download links, viability tiers, and the new documentation stubs flagged by the cataloguing script.

## eSpeak NG and MBROLA crossovers

- [`espeak-1.16-source.zip`](https://datajake.braillescreen.net/tts/espeak/espeak-1.16-source.zip) and subsequent source
  releases carry eSpeak's C code, phoneme rules, and dictionary compilers. Reusing these tables accelerates our IPA expansion
  and helps align NVDA's phoneme picker with Eloquence's new generative layers.
- Platform builds such as [`espeak-1.17-linux.zip`](https://datajake.braillescreen.net/tts/espeak/espeak-1.17-linux.zip) and
  [`espeak-1.16-riscos.zip`](https://datajake.braillescreen.net/tts/espeak/espeak-1.16-riscos.zip) demonstrate cross-platform
  build flags. Porting those build scripts informs our CodeQL coverage and keeps Eloquence's packaging ready for NVDA alpha
  releases on multiple architectures.
- [`espeak-data-mbrola.zip`](https://datajake.braillescreen.net/tts/espeak/espeak-data-mbrola.zip) bundles MBROLA voices and
  phoneme conversions that we can import into `phoneme_catalog.py` to seed additional language templates.

## NVDA synthesizer add-ons

- [`BeSTspeech.nvda-addon`](https://datajake.braillescreen.net/tts/synthesizers%20for%20nvda/BeSTspeech.nvda-addon) and
  [`Brailab%20PC%20Driver.nvda-addon`](https://datajake.braillescreen.net/tts/synthesizers%20for%20nvda/Brailab%20PC%20Driver.nvda-addon)
  provide Python bridge layers that demonstrate how legacy synthesizers expose configuration dialogs and WASAPI buffers within
  NVDA. Studying their module layout informs our own add-on structure and CodeQL hardening.
- [`Festival.nvda-addon`](https://datajake.braillescreen.net/tts/synthesizers%20for%20nvda/Festival.nvda-addon) shows how to
  orchestrate external synthesis pipelines; its IPC helpers guide Eloquence's long-term plan to mix neural and Klatt engines.
- [`JTalk.nvda-addon`](https://datajake.braillescreen.net/tts/synthesizers%20for%20nvda/JTalk.nvda-addon) includes kana/kanji
  tokenisation scripts that we can adapt when expanding Eloquence's Japanese language profile.

## DECtalk toolchain and ANSI-C sources

- [`microdectalk.zip`](https://datajake.braillescreen.net/tts/DECtalk%20source%20code%20archive/microdectalk.zip) and
  [`tools.zip`](https://datajake.braillescreen.net/tts/DECtalk%20source%20code%20archive/tools.zip) expose DECtalk's modular C
  implementation. Cross-referencing their phoneme tables keeps Eloquence's classic presets faithful for NVDA users migrating
  from DECtalk add-ons.
- Toolchain bundles such as [`HW_Build_Toolchain.7z`](https://datajake.braillescreen.net/tts/DECtalk%20Build%20Tools/HW_Build_Toolchain.7z)
  and [`eMbedded_Visual_Tools_3.0.7z`](https://datajake.braillescreen.net/tts/DECtalk%20Build%20Tools/eMbedded_Visual_Tools_3.0.7z)
  document the original MSVC environments required to compile DECtalk. Their build scripts guide our compatibility layer when we
  update the Eloquence loader for 32-bit, x64, and ARM64 add-on packaging.

## SAPI bridge layers

- [`SAPI5_IBMTTS.zip`](https://datajake.braillescreen.net/tts/sapi_voices/SAPI5_IBMTTS.zip) and
  [`IBM-ViaVoice_TTS-SAPI4.zip`](https://datajake.braillescreen.net/tts/sapi_voices/IBM-ViaVoice_TTS-SAPI4.zip) include the glue
  code and lexicons used to surface IBM TTS voices through Microsoft's APIs. Analysing their dictionaries informs how we load
  IBM-derived phoneme sets inside `language_profiles.py`.
- [`RHVoice-SAPI5.zip`](https://datajake.braillescreen.net/tts/sapi_voices/RHVoice-SAPI5.zip) demonstrates a modern open-source
  SAPI bridge whose configuration can be mirrored when expanding Eloquence's NV Speech Player style sliders.
- [`RealSpeak Solo.7z`](https://datajake.braillescreen.net/tts/sapi_voices/RealSpeak%20Solo.7z) exposes Nuance lexicons that help
  us cross-validate stress and emphasis controls across English dialects.

## Legacy Eloquence and Fonix assets

- [`eloquence.7z`](https://datajake.braillescreen.net/tts/old_software_synths/eloquence.7z) and
  [`eloquence%20samples%20in%20wav%20format.7z`](https://datajake.braillescreen.net/tts/misc/eloquence%20samples%20in%20wav%20format.7z)
  contain historical voices and sample exports useful for regression tests of our phoneme EQ pipeline.
- [`monologue16 with full 22 khz voice font.7z`](https://datajake.braillescreen.net/tts/old_software_synths/monologue16%20with%20full%2022%20khz%20voice%20font.7z)
  captures FonixTalk voice fonts that can seed our slider defaults for smoothness, nasal balance, and tone range.
- [`DECtalk%204.621.zip`](https://datajake.braillescreen.net/tts/dectalk%20software%20and%20manual/DECtalk%204.621.zip) includes
  sample dictionaries and executables that clarify pronunciation fallback rules when importing DECtalk lexicons.

## Next actions

1. Mirror high-priority archives into a secure cache, then record extraction scripts next to the manifest.
2. Port reusable code into `eloquence_data` or the NVDA add-on once licensing is confirmed, updating CodeQL configuration as we
   introduce new modules.
3. Note integration progress in `docs/archive_inventory.md` and reference the relevant NVDA issues so testers can follow along.
4. Use the new metadata summaries (`summaries.extensions`, `summaries.sample_rates`, `summaries.bit_depths`, `summaries.audio_fidelity`, `summaries.languages`, `summaries.language_tags`, `summaries.synth_hints`, `summaries.families`, `summaries.voice_hints`, `summaries.platforms`, `summaries.versions`, `summaries.categories`, `summaries.viability`, `summaries.gender_hints`, `summaries.age_hints`, and `summaries.metadata_flags`) in `docs/archive_inventory.json` to queue phoneme imports, language template work, and cross-platform tooling audits before mirroring lower-priority demo audio. The per-record metadata now exposes `audio_signature` strings alongside lexicon and tooling hints so EQ calibration can focus on clean stereo captures first.
