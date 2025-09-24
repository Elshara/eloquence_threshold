# Eloquence Threshold for NVDA

Eloquence Threshold keeps the beloved ETI Eloquence 6.1 speech synthesizer alive for blind and low-vision users who rely on the NonVisual Desktop Access (NVDA) screen reader on Windows 10 and Windows 11. By preserving the ultra-low latency performance of this Klatt-based engine—similar to classic voices such as DECtalk, FonixTalk, and the IBM TTS family—we deliver responsive speech output that remains essential for efficient navigation.

## Why this fork exists
This project builds on the long-standing community work at [pumper42nickel/eloquence_threshold](https://github.com/pumper42nickel/eloquence_threshold). NVDA's evolving add-on policies and frequent Python version shifts have created ongoing incompatibilities for legacy builds, so this fork provides a modern, continuously maintained alternative. Our goal is to keep Eloquence aligned with NVDA's latest expectations while honouring the workflow of both underground and mainstream add-on developers. The repository now serves as the staging ground for a unified Klatt synthesizer bundle that will eventually ship Eloquence, eSpeak NG-inspired profiles, DECtalk/FonixTalk voices, and IBM TTS assets inside a single NVDA add-on.

## Vision for 2026 and beyond
- Expand Eloquence beyond the historic eight preset voices so users can craft speech that reflects their preferences and cultural context.
- Offer deep phoneme customization directly inside NVDA's voice settings dialog, enabling keyboard-driven tweaks to cadence, articulation, and intonation without external tooling.
- Import phoneme and voice data from projects like [eSpeak NG](https://github.com/espeak-ng/espeak-ng), [NV Speech Player](https://github.com/nvaccess/NVSpeechPlayer), [RetroBunn/dt51](https://github.com/RetroBunn/dt51) (DECtalk 5.1), [davidacm/NVDA-IBMTTS-Driver](https://github.com/davidacm/NVDA-IBMTTS-Driver), and community FonixTalk archives so that Eloquence, DECtalk, and IBM TTS heritage voices can coexist and cross-pollinate.
- Future-proof the synthesizer against rapid advances in AI and accessibility tech, ensuring that Windows users continue to benefit from dependable, low-latency speech.

## Staying current with NVDA
We actively follow the [NVDA source repository](https://github.com/nvaccess/nvda/) and test against stable, beta, and alpha builds. The driver now runs against NVDA alpha-52705 (`dc226976`), which finalises the jump to 64-bit Python 3.13. Contributions should call out any compatibility insights—particularly where NVDA's speech stack or Win32 bindings change—so we can keep the synthesizer usable for the wider community. Regular updates will track NVDA's development cadence so that users can rely on Eloquence throughout major platform transitions.

Because NVDA 2026 builds execute as a 64-bit process, the add-on must load a 64-bit Eloquence runtime. The driver automatically discovers architecture-specific DLLs (for example, `eloquence/x64/eci.dll`) and falls back to the classic 32-bit build when appropriate. If a compatible library is missing the driver logs a clear error instead of silently failing.

## Getting started
1. Download the latest packaged add-on from the [releases page](https://github.com/pumper42nickel/eloquence_threshold/releases/latest/download/eloquence.nvda-addon), or clone this repository to build locally.
2. If you are building your own package, gather the proprietary Eloquence binaries: place the classic 32-bit runtime (for example `ECI.DLL` and the `.syn` voice data) inside an `eloquence/` directory, and optionally add a 64-bit runtime under `eloquence_x64/`. You can also reuse an earlier add-on as a template by dropping it next to the build script as `eloquence_original.nvda-addon` or by passing `--template /path/to/addon.nvda-addon` when building.
3. Run `python build.py` to produce `eloquence.nvda-addon` in the repository root. The builder now stages everything locally so offline or firewalled systems no longer block packaging. Supply `--no-download` if you do not want it to attempt downloading the legacy template, or point at a custom cache with `--template`.
4. Install the add-on in NVDA 2019.3 or newer on Windows 10 or Windows 11. NVDA alpha-52705 has been verified when the 64-bit runtime is available.
5. Visit NVDA's **Preferences → Speech** dialog to select Eloquence and begin exploring customization options—including the growing set of voice and phoneme parameters we surface in the dialog.

### Build script reference
- `python build.py --output dist/eloquence.nvda-addon` writes the package to a custom path.
- `python build.py --template path/to/legacy-addon.nvda-addon` reuses binaries from an existing package instead of copying from `./eloquence/`.
- `python build.py --no-download --insecure` prevents network access entirely; `--insecure` remains available for environments that must bypass TLS validation when downloading a template from a trusted mirror.

## Phoneme and voice customization today
- The add-on ships with the [eSpeak NG](https://github.com/espeak-ng/espeak-ng) `phsource/phonemes` catalogue under `eloquence_data/espeak_phonemes.txt` plus community JSON extensions for DECtalk, IBM TTS, and NV Speech Player phonemes (see `eloquence_data/phonemes/`). These definitions seed NVDA's phoneme controls without requiring a separate download and now expose the frame data that `nvSpeechPlayer` used to render its classic vowels and consonants.
- Use the **Phoneme category** and **Phoneme symbol** settings in NVDA's voice dialog to focus on a single phoneme at a time. Categories mirror the groupings defined by eSpeak NG and any contributed DECtalk/FonixTalk sets, and each symbol entry announces the phoneme name alongside its descriptive comment so you can explore the inventory from the keyboard.
- Once a symbol is selected, the **Phoneme replacement** option lists the available fallbacks—example words, descriptive labels, IPA symbols, or the raw engine token. Choose a combination with arrow keys and NVDA will announce whether it is the **current** or **default** mapping.
- Activating a different replacement immediately updates Eloquence's response when NVDA emits `PhonemeCommand` sequences, so you can tailor pronunciation on the fly without leaving the dialog. Custom choices are stored per phoneme, letting you review or reset mappings at any time.
- NVDA stores those custom mappings inside its `nvda.ini` configuration (`speech/eloquence/phonemeReplacements`), ensuring your language tweaks persist across sessions. Delete that block if you want to revert every phoneme to the bundled defaults in one go.
- The **Default phoneme fallback** setting lets you decide whether Eloquence prefers sample words, descriptive text, IPA, or the engine’s raw symbol whenever you have not chosen a custom replacement. Pick the style that makes the most sense for your workflow and the driver will refresh the default mappings across the whole inventory.
- Voice templates can bundle phoneme replacement recommendations. Selecting a heritage preset seeds its preferred fallbacks—without touching any overrides you have already saved—so you immediately hear the nuances that made those classic builds distinct.
- A new pair of **Voice parameter** and **Voice parameter value** controls in the Speech dialog lets you cycle through Eloquence's core sliders (rate, pitch, inflection, head size, roughness, breathiness, and volume) and adjust them with a single keyboard-driven workflow. The driver pulls range metadata from the bundled voice catalogue so the slider automatically respects each parameter's safe bounds and preferred step size.
- If you ever want to refresh the underlying catalogue with a newer upstream snapshot, run `python tools/refresh_espeak_phonemes.py /path/to/espeak-ng` to copy the latest `phsource/phonemes` definition into `eloquence_data/espeak_phonemes.txt` before rebuilding the add-on.

### Build bespoke voices with community templates
- Voice templates derived from eSpeak NG live in `eloquence_data/espeak_voices.json`. Each template maps a language label (for example `en-US` or `es-419`) to Eloquence parameters such as pitch, head size, breathiness, and speaking rate.
- New NV Speech Player inspired presets ship in `eloquence_data/voices/nvspeechplayer_classics.json`. They approximate Adam, Benjamin, Caleb, and David using Eloquence's slider ranges while preserving the original frame multipliers inside the template metadata so you can iterate on the mapping.
- If you want something even more dynamic, drop eSpeak NG variant voice files (for example anything from `espeak-ng-data/voices/!v/`) into `eloquence_data/espeak_variants/`. The loader parses their pitch, speed, voicing, and consonant settings, maps them to Eloquence sliders, and exposes the result as new templates the next time NVDA starts. This automated import workflow was inspired by dynamic synthesizer projects such as [mush42/sonata-nvda](https://github.com/mush42/sonata-nvda) so contributors can experiment without hand-editing JSON.
- DECtalk starter templates are now available in `eloquence_data/dectalk_voices.json`, capturing the personality of classics like Perfect Paul, Beautiful Betty, and Rough Rita. These entries model FonixTalk-era parameter sets so you can approximate DECtalk timbres when running on top of the Eloquence engine.
- Heritage captures from JAWS, Window-Eyes, and Loquence SAPI-4 installs ship in `eloquence_data/voices/eloquence_heritage.json`. These presets toggle abbreviation dictionaries, phrase prediction, and phoneme fallbacks so modern NVDA builds inherit the feel of their legacy counterparts.
- Fresh SAPI-4 and SAPI-5 captures derived from the DataJake archives (`eloq61.exe`, `IBM-ViaVoice_TTS-SAPI4.zip`, and `SAPI5_IBMTTS.zip`) live in `eloquence_data/voices/eloquence_sapi.json`. Each template documents the upstream package inside its `extras.sourceArchive` field so you can cross-reference provenance while tuning.
- Select **Voice template** inside NVDA's Speech dialog to apply these presets. Eloquence will switch to the appropriate `.syn` voice, set its variant, and adjust sliders instantly. You can still tweak the individual sliders afterward; the template simply provides a faster starting point.
- Contributors can add more templates by editing the JSON files. Drop new payloads either alongside the existing `_voices.json` descriptors or inside `eloquence_data/voices/` and the loader will pick them up automatically. The metadata documents the expected ranges for each parameter so community voices stay within Eloquence's safe operating window. New synthesizer families (for example, SAPI-4 ports) can live in additional JSON descriptors alongside DECtalk and eSpeak.

### Share language-aware pronunciation profiles
- Character-level pronunciation hints load from `eloquence_data/languages/*.json`. Each profile records IPA transcriptions, spoken mnemonics, stress patterns, and grammatical notes for a particular locale. We now ship starter sets for English (US/UK), Spanish (Castilian/Latin American), French, German, Italian, and Brazilian Portuguese so users can explore diverse alphabets immediately.
- Run `python tools/describe_language_profile.py --list-profiles` to see which profiles are bundled, then pass `--profile english_us_basic "texto"` (or `--language es-ES`) to preview the hints Eloquence will announce for a sample word. Add `--per-character` if you want a table of every matched digraph and the fallback the driver will speak.
- Heritage spelling rules for American English captured from JAWS, Window-Eyes, and Loquence dictionaries live in `eloquence_data/languages/english_us_heritage.json`. When you select a heritage voice template the driver automatically follows this profile so single-character announcements match their legacy pronunciation.
- The **Language profile** driver setting lets you follow the active voice template automatically, force a specific profile, or turn the hints off entirely. When NVDA sends IPA fallback commands, Eloquence can announce both the unmatched symbol and the language-specific hint so you understand what the command attempted to say.
- Segments flagged with language metadata in documents (for example, HTML `lang` attributes) trigger NVDA’s `LangChangeCommand`. When your Speech settings follow the template or match the requested profile, Eloquence now switches to the best language profile automatically so pronunciation hints align with the author’s locale choices.
- To contribute a new language or extend an existing one, drop a JSON file in the `eloquence_data/languages` folder. Profiles may list default templates so NVDA automatically activates them when users pick the matching voice. Multi-character digraphs such as Italian `gli` or Portuguese `nh` are recognised by the driver, so you can document complex sounds without resorting to single-letter approximations.

### Multilingual coverage snapshot
- Linguists estimate that more than 7,000 languages are in active use worldwide, and the number continues to evolve as dialects are documented or revitalised. Our long-term plan is to make Eloquence capable of speaking every script and symbol by piggybacking on community data.
- [eSpeak NG](https://github.com/espeak-ng/espeak-ng) already publishes phoneme inventories and voice rules for over 100 languages and variants, giving us a solid foundation for rapid expansion. As we import these datasets we track the maturity of each locale across phoneme coverage, language profiles, and keyboard-driven voice controls.

| Locale / Dialect | Phoneme dataset status | Language profile status | Voice template status | Keyboard customisation | Notes |
| --- | --- | --- | --- | --- | --- |
| English (US) | Bundled – eSpeak NG, NV Speech Player, heritage DECtalk mappings | Bundled – `english_us_basic.json` + `english_us_heritage.json` | Bundled – heritage, SAPI, and NV Speech Player templates | Full phoneme picker and slider controls | Serves as baseline for cross-engine comparisons |
| English (GB) | Bundled – eSpeak NG phoneme set | Bundled – `english_gb_basic.json` | Shares US/heritage templates until native captures arrive | Full phoneme picker and slider controls | Queueing region-specific heritage templates |
| Spanish (Castilian) | Bundled – eSpeak NG | Bundled – `spanish_castilian_basic.json` | Bundled – NV Speech Player inspired presets | Full phoneme picker and slider controls | Expanding digraph coverage for regional variants |
| Spanish (Latin American) | Bundled – eSpeak NG | Bundled – `spanish_latam_basic.json` | Bundled – NV Speech Player inspired presets | Full phoneme picker and slider controls | Targeting Mexican and Caribbean voicing nuances |
| French (France) | Bundled – eSpeak NG | Bundled – `french_fr_basic.json` | Bundled – eSpeak variant templates | Full phoneme picker and slider controls | Planning nasal-vowel refinement passes |
| German | Bundled – eSpeak NG | Bundled – `german_basic.json` | Bundled – eSpeak variant templates | Full phoneme picker and slider controls | Evaluating legacy DECtalk “Ursula” style formants |
| Italian | Bundled – eSpeak NG | Bundled – `italian_basic.json` | Bundled – eSpeak variant templates | Full phoneme picker and slider controls | Adding heritage dictionary sources for comparison |
| Portuguese (Brazil) | Bundled – eSpeak NG | Bundled – `portuguese_br_basic.json` | Bundled – eSpeak variant templates | Full phoneme picker and slider controls | Planning European Portuguese follow-up |
| Future locales (all other eSpeak NG voices) | Planned – staged imports via `tools/refresh_espeak_phonemes.py` | Planned – contributors invited to seed `eloquence_data/languages/*.json` | Planned – automatic template generation from `.voice` files | Controls automatically available once data lands | Prioritise high-demand locales (e.g., Hindi, Arabic, Mandarin, Russian) |
| Symbols, emoji, technical scripts | Bundled – raw Unicode passthrough; curated IPA fallbacks queued | Planned – per-script pronunciation tables | Planned – synthetic template packs for specialised domains | Phoneme picker already handles custom replacements | Encourage domain experts to contribute script- or context-specific datasets |

We tag each locale with the most advanced assets we have shipped so far. When you contribute a new language, please:

1. Import or reference the eSpeak NG phoneme block (or another public dataset) inside `eloquence_data/phonemes/`.
2. Create a language profile file under `eloquence_data/languages/` that documents characters, digraphs, stress behaviour, and grammatical notes.
3. Supply at least one voice template—either handcrafted JSON or an auto-converted `.voice` file—so NVDA users can hear the locale immediately.
4. Outline any remaining gaps (for example, “needs tone marks” or “emoji coverage pending”) so we can keep the roadmap transparent.

Short-term expansion priorities include Hindi, Arabic, Mandarin Chinese, Russian, Japanese, Korean, and the major Indic languages highlighted by Hear2Read. These locales already have mature eSpeak NG voices and large user communities eager for low-latency synthesizers.

### Toward universal script and symbol coverage
Pronunciation dictionaries alone cannot keep up with the creative ways people mix alphabets, emoji, ASCII art, mathematical notation, or braille patterns in everyday text. Eloquence Threshold therefore centres on a **phoneme, sound, and symbol customiser** that you can drive entirely from NVDA's Speech dialog:

- Every phoneme exposed by Eloquence, DECtalk, or eSpeak NG can be reassigned to words, IPA samples, or raw engine tokens, and those overrides are stored per user so the same keyboard shortcuts work across all contexts.
- Character-level language profiles describe how scripts sound—covering letters, digraphs, punctuation, and grammatical cues—so future dictionary imports can map text passages (sentences, paragraphs, essays, or book formats) directly onto phoneme sequences.
- Contributors are encouraged to add corpora-specific dictionaries (for example, math textbooks, programming languages, or lyrical content) as structured JSON so the driver can swap context-aware hints without breaking the underlying phoneme sliders.
- Because NVDA already passes through arbitrary Unicode code points, you can build replacement tables for historical scripts, emoji ZWJ sequences, or mixed-language hashtags. Share these assets in the repository so others can benefit without waiting for upstream dictionary updates.

Our aim is that any character in the Unicode standard—and any combination that writers invent—can be spoken accurately by selecting the right language profile, tweaking phoneme replacements, or loading a specialised voice template. As we fold in more eSpeak NG, DECtalk, and community archives, we will continue publishing coverage snapshots and inviting specialists to fill the remaining gaps.

### Preparing DECtalk and IBM TTS assets
- We are actively researching how to bundle DECtalk 5.1 (see [RetroBunn/dt51](https://github.com/RetroBunn/dt51)) alongside Eloquence. Community FonixTalk packages such as `FonixTalk.nvda-addon` provide compatible voice files; place extracted `.dic` and `.ph` assets under `synthDrivers/dectalk` to experiment.
- The [NVDA-IBMTTS-Driver](https://github.com/davidacm/NVDA-IBMTTS-Driver) demonstrates how IBM TTS integrates with NVDA. We plan to reuse its 64-bit shims and data layout when we incorporate additional Klatt voices.
- DataJake's SAPI voice mirrors include [SAPI 5 ViaVoice/IBMTTS](https://datajake.braillescreen.net/tts/sapi_voices/SAPI5_IBMTTS.zip), [SAPI 4 ViaVoice](https://datajake.braillescreen.net/tts/sapi_voices/IBM-ViaVoice_TTS-SAPI4.zip), and the [Eloquence 6.1 Studio port](https://datajake.braillescreen.net/tts/sapi_voices/eloq61.exe). Extract their `*.dll`, `*.syn`, and `*.dat` files for parameter research or to seed additional NVDA-ready templates. The broader archive at [datajake.braillescreen.net/tts/](https://datajake.braillescreen.net/tts/) also hosts DECtalk and FonixTalk snapshots worth cataloguing.
- [Code Factory's Eloquence for Windows](https://www.codefactoryglobal.com/downloads/installers/EloquenceForWindows-Setup.exe) provides a commercial SAPI 5 build with refreshed Studio voicing. Install the package in a test VM, capture its `.syn` and `.dll` assets, and compare against the DataJake archives when tuning presets or validating phoneme behaviour on modern Windows releases.
- Legacy archives hosted by the Blind Help Project (for example, the IBMTTS V25 package and high-fidelity SAPI-4 Eloquence ports) offer excellent reference material for tuning parameters and matching pronunciation tables. Keep local notes on provenance so we can document redistribution requirements clearly.

### Additional voice and phoneme archives worth mining
- [Hear2Read's NVDA add-ons and tutorials](https://hear2read.org/NVDA_Addon) ([tutorials](https://hear2read.org/tutorials), [original package](https://hear2read.org/Original_NVDA_Addon)) expose Indic languages with detailed phoneme tables that map cleanly onto our template-driven workflow.
- [IDC Multilingual resources](https://www.idc-mn.info/) and [Newfon releases](https://github.com/DraganRatkovich/newfon/releases/latest) ([NVDA add-on](https://addons.nvda-project.org/addons/newfon.en.html)) provide Klatt-derived parameter sets that can be transcribed into our JSON catalogues.
- [RHVoice](https://rhvoice.org/) and its [developer wiki](https://github.com/Olga-Yakovleva/RHVoice/wiki) document language models, prosody controls, and lexical data that align well with the character-by-character pronunciation profiles we ship.
- [OHF-Voice/piper1-gpl](https://github.com/OHF-Voice/piper1-gpl) demonstrates modern neural techniques but still surfaces rich phoneme metadata that we can translate into Eloquence-friendly fallbacks.
- [mush42/sonata-nvda releases](https://github.com/mush42/sonata-nvda/releases/latest) and the [SpeechPlayer in eSpeak add-on](https://addons.nvda-project.org/addons/speechPlayerInEspeak.en.html) highlight dynamic synthesizer pipelines we can borrow from when wiring new sliders or presets.
- NV Access curated add-ons such as [Festival](http://files.nvaccess.org/nvda-addons/festivalTts-2.0.nvda-addon), [Svox Pico](http://files.nvaccess.org/nvda-addons/svox-pico-2.0.nvda-addon), [Phonetic Punctuation](https://addons.nvda-project.org/addons/phoneticPunctuation.en.html), [Audio Themes](https://addons.nvda-project.org/addons/AudioThemes.en.html), [Dual Voice](https://addons.nvda-project.org/addons/dualvoice.en.html), and [audioScreen](https://github.com/nvaccess/audioScreen) showcase UI patterns for exposing multiple speech engines from the keyboard.
- The [DataJake speech archive](https://datajake.braillescreen.net/tts/) spans CircumReality, DECtalk (including [version 4.99](https://datajake.braillescreen.net/tts/DECtalk%204.99/) and [build tools](https://datajake.braillescreen.net/tts/DECtalk%20Build%20Tools/)), FonixTalk, RealSpeak, MBROLA databases, Microsoft Speech Platform voices, and additional NVDA synthesizer bundles. These collections are ideal for extracting provenance notes, `.syn` and `.dic` assets, and reference recordings while we continue expanding the catalogue.

### Mining NV Speech Player data
- The [NV Speech Player repository](https://github.com/nvaccess/NVSpeechPlayer) is now part of our reference stack. The bundled `eloquence_data/phonemes/nvspeechplayer_core.json` file was generated directly from its `data.py` frame definitions so you can compare Eloquence’s handling of vowels and consonants with NVDA’s historical synthesizer.
- Voice presets under `eloquence_data/voices/nvspeechplayer_classics.json` approximate Adam, Benjamin, Caleb, and David. Each entry keeps the original NV Speech Player multipliers in the `extras.nvspeechPlayer` block—perfect for anyone who wants to refine the conversion or build tooling that translates presets automatically.
- When experimenting with upstream changes, pull fresh snapshots of `NVSpeechPlayer` and regenerate the JSON files before packaging. The helper at `tools/convert_nvspeechplayer.py` demonstrates how to carry over classification flags, formant targets, and amplitude settings so the NVDA voice dialog exposes the full dataset to keyboard users.

### Supplying 64-bit Eloquence binaries
- This project cannot redistribute proprietary Eloquence libraries. Extract the 64-bit runtime from a licensed product (for example, an updated Eloquence synthesizer package) and drop the DLLs into `eloquence_x64` before packaging, or copy them directly into `synthDrivers/eloquence/x64` after installing the add-on.
- Dictionaries (`*.dic`) and voice data (`*.syn`) may stay in the legacy `synthDrivers/eloquence` directory—the driver will automatically reference them from either location.
- When distributing builds to other NVDA users, document how you sourced the binaries so that future maintainers can keep their installations in good standing.

## Roadmap highlights
- Iterative releases that surface new phoneme and voice parameters in NVDA's voice dialog.
- Research into importing phoneme rule sets from eSpeak NG, DECtalk, FonixTalk, and IBM TTS to cover more languages and dialects without sacrificing speed.
- Progressive modernization of the code base to meet accessibility expectations for 2026 and beyond.
- Ship a packaged add-on that merges Eloquence, DECtalk, and eSpeak voice data so contributors can build or swap voices without juggling multiple downloads.

## Contributing
We welcome issues, discussions, and pull requests from screen reader users, speech enthusiasts, and developers. Please:
- Describe your NVDA build (including alpha snapshots when relevant) and Windows version when reporting bugs or sharing feedback.
- Help us validate voice and phoneme updates across diverse locales. Keyboard accessibility is the top priority—every phoneme replacement and voice parameter should remain adjustable without leaving NVDA's dialogs.
- Note that we rely on CodeQL for automated security and quality analysis; contributions should keep CodeQL warnings in mind.
- Link to upstream resources or archives when proposing new DECtalk/FonixTalk or IBM TTS assets so we can track provenance.

If something feels off or you have an idea to extend Eloquence further, open an issue or start a discussion—we are growing this project together with the community.
