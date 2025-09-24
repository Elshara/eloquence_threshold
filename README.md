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
We actively follow the [NVDA source repository](https://github.com/nvaccess/nvda/) and test against stable, beta, and alpha builds. The driver now runs against NVDA alpha-52731 (`f294547a`), which finalises the jump to 64-bit Python 3.13. Contributions should call out any compatibility insights—particularly where NVDA's speech stack or Win32 bindings change—so we can keep the synthesizer usable for the wider community. Regular updates will track NVDA's development cadence so that users can rely on Eloquence throughout major platform transitions.

Because NVDA 2026 builds execute as a 64-bit process, the add-on must load a 64-bit Eloquence runtime. The driver automatically discovers architecture-specific DLLs (for example, `eloquence/x64/eci.dll` or `eloquence/arm64/eci.dll`) and falls back to the classic 32-bit build when appropriate. If a compatible library is missing the driver logs a clear error instead of silently failing, so you can populate the matching `eloquence_x86`, `eloquence_x64`, `eloquence_arm32`, or `eloquence_arm64` directories before packaging.

### Mapping the NV Access download archive for automation
To keep Eloquence Threshold validated against every public NVDA milestone we catalogue the layout of [download.nvaccess.org](https://download.nvaccess.org/). Automation scripts can crawl these predictable folders to fetch installers, controller clients, manuals, and debugging symbols without hand-editing URLs every time NVDA publishes a build.

#### Root layout
| Path | Type | Typical entries | Why it matters |
| --- | --- | --- | --- |
| `releases/` | Directory | Versioned folders such as `2025.3/` plus symlinks `stable/` and `beta/` that point at the current GA or release-candidate build. | Fetch production installers and manual bundles; watch the symlinks for promotions. |
| `snapshots/` | Directory | Rolling channels `alpha/`, `beta/`, `rc/`, and `try/` that expose development executables for every merged changeset. | Exercise upcoming NVDA changes and confirm Eloquence keeps working on nightly builds. |
| `symbols/` | Directory | Symbol stores for releases (`nvdaReleases/`), snapshots (`nvdaSnapshots/`), plus historic `python/` and `wxPython/` debug files. | Feed WinDbg or Visual Studio when diagnosing crashes against specific NVDA binaries. |
| `documentation/` | Symlink | Points to `releases/stable/documentation`, exposing the same language folders as the stable release. | Link here for manuals so URLs stay valid after each release. |

#### `releases/` directory map
Each versioned folder contains the signed installer, the remote-control SDK, and a documentation tree split by locale. Older releases also surface optional archives such as portable or source zips, so automation should probe for those names but treat them as optional.

| Path fragment | What you find | Notes for automation |
| --- | --- | --- |
| `releases/<version>/nvda_<version>.exe` | Primary installer for the release. | Download for manual testing or to seed virtual machines. |
| `releases/<version>/nvda_<version>_controllerClient.zip` | Controller client SDK for remote control or scripting. | Mirror this alongside the installer so integration tests can drive NVDA remotely. |
| `releases/<version>/documentation/` | Language folders (for example `en/`, `pt_BR/`, `zh_CN/`) with translated manuals. | Iterate through subfolders to keep track of newly translated locales. |
| `releases/<version>/documentation/<locale>/changes.html` | Release notes describing fixes and new features for that locale. | Parse these pages to understand what changed between builds—ideal for regression test planning. |
| `releases/<version>/documentation/<locale>/userGuide.html` | Full user guide for the locale. | Scrape terminology when aligning README phrasing or pronunciation hints. |
| `releases/<version>/documentation/<locale>/keyCommands.html` | Keyboard shortcut reference. | Validate that Eloquence announcements match NVDA’s documented keystrokes. |
| `releases/<version>/documentation/<locale>/styles.css` and `numberedHeadings.css` | Shared styling for manuals. | Changes here hint at documentation structure updates that could affect scraping. |
| `releases/<version>/documentation/<locale>/favicon.ico` | Icon bundled with the manual set. | Optional asset—useful when mirroring manuals verbatim. |

Symlinks `releases/stable/` and `releases/beta/` follow the most recent directories; monitor their modification timestamps to detect promotions without diffing the entire listing.

#### `snapshots/` directory map
The snapshot hierarchy exposes every in-progress build, with filenames that capture both the sequential build number and the Mercurial or Git changeset hash. Pay close attention to file sizes—brand-new uploads often appear as `0.0 B` for a few minutes while the mirror finishes syncing.

| Path | Contents | How we use it |
| --- | --- | --- |
| `snapshots/alpha/` | `nvda_snapshot_alpha-<build>,<changeset>.exe` installers for nightly development builds. | Run automated smoke tests against the next NVDA core to catch compatibility issues early. |
| `snapshots/beta/` | Executables for beta-channel builds that precede release candidates. | Validate features slated for the next minor release before they stabilise. |
| `snapshots/rc/` | Executables for release-candidate builds (mirrors the `releases/<version>rc*` folders). | Final regression runs before a build becomes `releases/stable`. |
| `snapshots/try/` | Subdirectories per experimental branch (for example `try-64bit/`, `try-chineseWordSegmentation-staging/`) each holding their own executables. | Track pull-request validation builds or platform experiments; perfect for testing architecture-specific shims. |

#### `symbols/` directory map
NV Access hosts symbols in a SymSrv-style layout so debuggers can download only the modules they need.

| Path | Contents | Notes |
| --- | --- | --- |
| `symbols/nvdaReleases/` | Subdirectories per DLL/EXE (for example `espeak.dll/`, `nvdaHelperRemote.dll/`) containing hashed folders like `68C74B2Fb7000/` with compressed binaries (`espeak.dl_`). | Point WinDbg at this path to symbolicate release crash dumps. |
| `symbols/nvdaSnapshots/` | Mirrors the release layout for snapshot builds, so nightly symbols remain accessible. | Enables debugging against alpha/beta executables shipped from `snapshots/`. |
| `symbols/python/` and `symbols/wxPython/` | Historical symbol stores for the Python and wxPython runtimes NVDA shipped with in prior years. | Useful when auditing regressions that span multiple NVDA eras. |

Because the hierarchy is deterministic, you can parametrise CI jobs to pull the latest installer (`releases/stable/nvda_<tag>.exe`) or the newest alpha build (`snapshots/alpha/nvda_snapshot_alpha-*.exe`) before launching our automated synthesis smoke tests. Recording these locations here keeps the workflow self-documenting and saves future contributors from tracing the index every time NVDA updates its infrastructure.

#### Automated snapshot and severity tracking
- Run `python tools/audit_nvaccess_downloads.py --roots releases/stable releases/2024.3 snapshots/alpha --max-depth 2 --limit-per-dir 12 --current-nvda alpha-52731 --json docs/download_nvaccess_snapshot.json --markdown docs/download_nvaccess_snapshot.md --insecure` to capture an incremental snapshot of the archive. The helper reads `manifest.ini` and `docs/validated_nvda_builds.json`, then classifies each entry by severity so we can decide whether to update, hold, or downgrade Eloquence.
- The command writes a machine-readable dataset (`docs/download_nvaccess_snapshot.json`) and a Markdown digest (`docs/download_nvaccess_snapshot.md`) sorted by modification date in descending order. Limiting each directory to a dozen entries keeps the run incremental while still surfacing the freshest installers, manuals, and nightly builds.
- When two cached snapshots exist, diff them with `python tools/compare_nvaccess_snapshots.py --old docs/download_nvaccess_snapshot.json --new path/to/fresh_snapshot.json --markdown docs/download_nvaccess_delta.md`. The diff report reuses the same severity grading so contributors can track new alphas, disappearing archives, and metadata changes without rereading the entire tree.
- Feed any cached snapshot into `python tools/report_nvda_compatibility.py --snapshot docs/download_nvaccess_snapshot.json --validated docs/validated_nvda_builds.json --markdown docs/nvda_compatibility_matrix.md --json docs/nvda_compatibility_matrix.json` to generate a descending-by-date compatibility matrix. The new helper mirrors NVDA’s alpha cadence from https://github.com/nvaccess/nvda/, reuses the audit severity grades, and publishes Markdown/JSON artefacts that CodeQL jobs or downstream automation can diff to spot risky releases quickly.
- Translate those severity grades into concrete actions with `python tools/check_nvda_updates.py --snapshot docs/download_nvaccess_snapshot.json --validated docs/validated_nvda_builds.json --manifest manifest.ini --markdown docs/nvda_update_recommendations.md --json docs/nvda_update_recommendations.json`. The CLI sorts entries by modification date, maps each release or snapshot to an "update", "monitor", "downdate", "keep", or "investigate" recommendation, and documents why that action is appropriate for the Eloquence add-on.
- Severity levels surface how urgently Eloquence must react: **high** means the entry is newer than our validated snapshot, **medium** matches the recorded baseline, **low** is older but still available for downgrades, and **info** indicates a release that remains inside the supported window. Update `docs/validated_nvda_builds.json` whenever you finish testing a new NVDA build so future audits share the same baseline.
- Use `--insecure` when the environment lacks a full certificate store (as in this development container). Production automation should omit the flag so TLS verification remains intact.

#### Track catalogue integrity automatically
- Run `python tools/report_catalog_status.py --json docs/catalog_status.json --markdown docs/catalog_status.md` after touching phoneme inventories, language profiles, or voice templates. The helper loads the bundled catalogues, verifies that every voice template references a valid language profile, and confirms that profiles point at existing templates.
- The generated Markdown digest summarises phoneme categories, locale coverage, and the templates exposed through NVDA's Speech dialog. Keep the `docs/catalog_status.md` snapshot in sync so contributors can quickly scan which languages already have keyboard-tunable voices and where new eSpeak NG, DECtalk, or NV Speech Player data is still required.
- The helper exits with a non-zero status when it detects missing references, making it suitable for automated checks or future CodeQL workflows that validate our multilingual roadmap against the latest NVDA alphas.
- Follow up with `python tools/validate_language_pronunciations.py --json docs/language_pronunciation_validation.json --markdown docs/language_pronunciation_validation.md` whenever you merge new language datasets. The validator cross-references every character's IPA sequence against the phoneme catalogue, highlighting unmatched fragments so eSpeak NG, DECtalk, NV Speech Player, and forthcoming datasets stay aligned.
- Commit the Markdown/JSON outputs to document pronunciation coverage by locale and give future CodeQL or CI jobs a machine-readable way to block regressions as we expand into additional scripts.

#### Integration scope parameter reporting
- Run `python tools/report_integration_scope.py --json docs/integration_scope.json --markdown docs/integration_scope.md --print` after touching any voice template, language profile, or phoneme dataset. The helper cross-references the bundled catalogues and records how many voices target each locale, which language profiles provide character-level hints, and how many phoneme categories feed NVDA’s picker. The command prints a quick summary to the console and refreshes both JSON/Markdown artefacts for review.
- The Markdown digest makes it easy to spot when a locale gains new templates without an accompanying pronunciation profile (or vice versa). Use it to plan incremental pull requests—for example, seed a profile first, then stage extra phoneme replacements or NVDA Speech dialog parameters in follow-up patches.
- The JSON output powers future automation: CI can watch for regressions in the number of phonemes, check that every profile retains at least one linked template, and flag when slider ranges change so we can bump release notes before packaging the add-on.
- Treat this report as the high-level map for “Eloquence Reloaded.” It shows how far the unified Eloquence/eSpeak/DECtalk/IBM catalogue has progressed towards full multilingual parity and keeps contributions aligned with NVDA’s keyboard-driven customization experience.

#### Voice and language linkage matrix
- Run `python tools/report_voice_language_matrix.py --json docs/voice_language_matrix.json --markdown docs/voice_language_matrix.md --print` whenever you update voice templates or language profiles. The helper correlates every template with its declared locale, default pronunciation profile, and tag set while checking that profiles point at real templates. The console summary quickly surfaces locales with skewed coverage so you can balance presets before packaging.
- The Markdown snapshot publishes a per-language matrix detailing template IDs, pronunciation profile identifiers, tag groupings, and default pairings. Treat it as the go-to checklist when you audit how well each locale binds speech parameters to character-level hints.
- The JSON payload mirrors that matrix for automation. Future CodeQL jobs can diff the snapshot to spot missing defaults, detect orphaned templates or profiles, and gate releases until the mismatch is resolved.

#### Voice parameter coverage snapshots
- Run `python tools/report_voice_parameters.py --json docs/voice_parameter_report.json --markdown docs/voice_parameter_report.md --print` whenever you add or tune voice templates, adjust parameter ranges, or import fresh eSpeak/DECtalk/NV Speech Player presets. The helper consolidates slider metadata, confirms that every template exposes the expected parameters, and records which locales the presets target so NVDA’s Speech dialog always surfaces a complete keyboard-driven experience.
- The Markdown output summarises the allowed range, default, and description for every slider we surface in Eloquence, then lists each template with its recommended parameter values, heritage tags, and extras. Treat the document as a quick reference when comparing how legacy ports (SAPI 4/5, FonixTalk, Code Factory, etc.) map their timbres into the modern add-on.
- The JSON payload mirrors the Markdown structure so CodeQL jobs or future automation can diff template additions, watch for accidental parameter removals, and highlight locales that still need bespoke presets before we package cross-platform releases.

#### NVDA compatibility scorecard
| Channel | Build identifier | Download URL | Severity | Recommended action |
| --- | --- | --- | --- | --- |
| Alpha snapshots | `alpha-52762,91e60c70` | `https://download.nvaccess.org/snapshots/alpha/nvda_snapshot_alpha-52762,91e60c70.exe` | High | Validate against the latest NVDA changeset and refresh Eloquence if incompatibilities appear. |
| Alpha snapshots | `alpha-52731,f294547a` | `https://download.nvaccess.org/snapshots/alpha/nvda_snapshot_alpha-52731,f294547a.exe` | Medium | Current validation baseline for Eloquence Threshold—rerun smoke tests whenever NVDA publishes a newer alpha. |
| Alpha snapshots | `alpha-52705,dc226976` | `https://download.nvaccess.org/snapshots/alpha/nvda_snapshot_alpha-52705,dc226976.exe` | Low | Previous baseline retained for downgrade testing in case newer alphas regress. |
| Stable releases | `2025.3` | `https://download.nvaccess.org/releases/stable/nvda_2025.3.exe` | Info | Supported within the current manifest window. Ship add-on updates once nightly validation passes. |
| Stable releases | `2024.3` | `https://download.nvaccess.org/releases/2024.3/nvda_2024.3.exe` | Info | Older release still inside the supported range—retain downgrade assets for users stuck on long-term deployments. |

The scorecard mirrors the generated snapshot and highlights which installers or manuals deserve immediate attention. Extend the table whenever you validate additional beta, RC, or try builds so contributors know what to test next.

## Getting started
1. Download the latest packaged add-on from the [releases page](https://github.com/pumper42nickel/eloquence_threshold/releases/latest/download/eloquence.nvda-addon), or clone this repository to build locally.
2. If you are building your own package, gather the proprietary Eloquence binaries: place the classic 32-bit runtime (for example `ECI.DLL` and the `.syn` voice data) inside an `eloquence/` directory. Add architecture-specific payloads beside it by creating `eloquence_x86/`, `eloquence_x64/`, `eloquence_arm32/`, or `eloquence_arm64/` folders containing the corresponding DLLs and voices. You can also reuse an earlier add-on as a template by dropping it next to the build script as `eloquence_original.nvda-addon` or by passing `--template /path/to/addon.nvda-addon` when building.
3. Run `python build.py` to produce `eloquence.nvda-addon` in the repository root. The builder now stages everything locally so offline or firewalled systems no longer block packaging. Supply `--no-download` if you do not want it to attempt downloading the legacy template, or point at a custom cache with `--template`.
4. Install the add-on in NVDA 2019.3 or newer on Windows 10 or Windows 11. NVDA alpha-52731 has been verified when the 64-bit runtime is available.
5. Visit NVDA's **Preferences → Speech** dialog to select Eloquence and begin exploring customization options—including the growing set of voice and phoneme parameters we surface in the dialog.

### Build script reference
- `python build.py --output dist/eloquence.nvda-addon` writes the package to a custom path.
- `python build.py --template path/to/legacy-addon.nvda-addon` reuses binaries from an existing package instead of copying from `./eloquence/`.
- `python build.py --no-download --insecure` prevents network access entirely; `--insecure` remains available for environments that must bypass TLS validation when downloading a template from a trusted mirror.

### Automated test suite
- Run `python -m unittest discover tests` to execute the bundled integrity checks. They validate that voice templates respect their slider ranges, phoneme inventories remain populated, and language profiles still expose character-level descriptions.
- The same test run also exercises our reporting utilities (`tools/report_voice_parameters.py`, `tools/report_catalog_status.py`, and `tools/validate_language_pronunciations.py`) to guarantee they continue emitting machine-readable snapshots for CI and documentation refreshes.
- Continue generating the Markdown/JSON artefacts tracked in `docs/` after you change catalogue data so the test suite, README tables, and CodeQL automation stay in sync.

## Phoneme and voice customization today
- The add-on ships with the [eSpeak NG](https://github.com/espeak-ng/espeak-ng) `phsource/phonemes` catalogue under `eloquence_data/espeak_phonemes.txt` plus community JSON extensions for DECtalk, IBM TTS, and NV Speech Player phonemes (see `eloquence_data/phonemes/`). These definitions seed NVDA's phoneme controls without requiring a separate download and now expose the frame data that `nvSpeechPlayer` used to render its classic vowels and consonants.
- Use the **Phoneme category** and **Phoneme symbol** settings in NVDA's voice dialog to focus on a single phoneme at a time. Categories mirror the groupings defined by eSpeak NG and any contributed DECtalk/FonixTalk sets, and each symbol entry announces the phoneme name alongside its descriptive comment so you can explore the inventory from the keyboard.
- Once a symbol is selected, the **Phoneme replacement** option lists the available fallbacks—example words, descriptive labels, IPA symbols, or the raw engine token. Choose a combination with arrow keys and NVDA will announce whether it is the **current** or **default** mapping.
- Activating a different replacement immediately updates Eloquence's response when NVDA emits `PhonemeCommand` sequences, so you can tailor pronunciation on the fly without leaving the dialog. Custom choices are stored per phoneme, letting you review or reset mappings at any time.
- NVDA stores those custom mappings inside its `nvda.ini` configuration (`speech/eloquence/phonemeReplacements`), ensuring your language tweaks persist across sessions. Delete that block if you want to revert every phoneme to the bundled defaults in one go.
- The **Default phoneme fallback** setting lets you decide whether Eloquence prefers sample words, descriptive text, IPA, or the engine’s raw symbol whenever you have not chosen a custom replacement. Pick the style that makes the most sense for your workflow and the driver will refresh the default mappings across the whole inventory.
- Voice templates can bundle phoneme replacement recommendations. Selecting a heritage preset seeds its preferred fallbacks—without touching any overrides you have already saved—so you immediately hear the nuances that made those classic builds distinct.
- A new pair of **Voice parameter** and **Voice parameter value** controls in the Speech dialog lets you cycle through Eloquence's core sliders (rate, pitch, inflection, head size, roughness, breathiness, and volume) and adjust them with a single keyboard-driven workflow. The driver pulls range metadata from the bundled voice catalogue so the slider automatically respects each parameter's safe bounds and preferred step size.
- As you focus the **Voice parameter value** slider, the label now echoes the active parameter name (for example, "Voice parameter value (Pitch – Primary pitch target...)") so NVDA announces which control you are editing in real time. This keeps keyboard-driven workflows oriented as you tab between sliders or switch templates.
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

| Locale / Dialect | Phoneme dataset status | Language profile status | Voice template status | Keyboard customisation | Speech fluency target | Braille hand-off status | Dictionary / corpus status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| English (US) | Bundled – eSpeak NG, NV Speech Player, heritage DECtalk mappings | Bundled – `english_us_basic.json` + `english_us_heritage.json` | Bundled – heritage, SAPI, and NV Speech Player templates | Full phoneme picker and slider controls | Conversational and rapid screen review verified | NVDA braille routing inherits pronunciations; Unified English Braille tables queued for tuning | Bundled sample corpora from NV Speech Player; literary/technical sets planned | Serves as baseline for cross-engine comparisons |
| English (GB) | Bundled – eSpeak NG phoneme set | Bundled – `english_gb_basic.json` | Shares US/heritage templates until native captures arrive | Full phoneme picker and slider controls | Conversational, proof-reading pass planned | Braille translation uses NVDA default UK tables; context harmonisation pending | Needs UK-specific corpora for spelling differences and idioms | Queueing region-specific heritage templates |
| Spanish (Castilian) | Bundled – eSpeak NG | Bundled – `spanish_castilian_basic.json` | Bundled – NV Speech Player inspired presets | Full phoneme picker and slider controls | Conversational coverage confirmed; newsreader pacing under review | NVDA braille (Spanish Grade 1) mapped; Grade 2 alignment targeted | Preparing RAE-based dictionary import and braille punctuation tables | Expanding digraph coverage for regional variants |
| Spanish (Latin American) | Bundled – eSpeak NG | Bundled – `spanish_latam_basic.json` | Bundled – NV Speech Player inspired presets | Full phoneme picker and slider controls | Conversational coverage confirmed; regional colloquialisms queued | NVDA braille (Español America Latina) inherits Latin punctuation; accent folding tests pending | Community corpora (Mexico, Colombia) requested for stress validation | Targeting Mexican and Caribbean voicing nuances |
| French (France) | Bundled – eSpeak NG | Bundled – `french_fr_basic.json` | Bundled – eSpeak variant templates | Full phoneme picker and slider controls | Conversational pacing tuned; fast dictation mode scheduled | NVDA braille (Français unifié) alignment planned with liaison hints | Launching Le Robert-based lexicon ingest for nasal vowels | Planning nasal-vowel refinement passes |
| German | Bundled – eSpeak NG | Bundled – `german_basic.json` | Bundled – eSpeak variant templates | Full phoneme picker and slider controls | Conversational; legal/technical jargon samples queued | NVDA braille (Vollschrift/Kurzschrift) linkage queued | Duden + Wiktionary corpora earmarked for compounding heuristics | Evaluating legacy DECtalk “Ursula” style formants |
| Italian | Bundled – eSpeak NG | Bundled – `italian_basic.json` | Bundled – eSpeak variant templates | Full phoneme picker and slider controls | Conversational; opera diction experiments pending | Braille (Italiano) mapping review scheduled for accentuated vowels | Treccani corpora import planned for stress and elision | Adding heritage dictionary sources for comparison |
| Portuguese (Brazil) | Bundled – eSpeak NG | Bundled – `portuguese_br_basic.json` | Bundled – eSpeak variant templates | Full phoneme picker and slider controls | Conversational; broadcast speech pacing under study | NVDA braille (Português brasileiro) works; contraction alignment pending | Preparing ABL/ABNT corpora for nasal + reduction cases | Planning European Portuguese follow-up |
| Future locales (all other eSpeak NG voices) | Planned – staged imports via `tools/refresh_espeak_phonemes.py` | Planned – contributors invited to seed `eloquence_data/languages/*.json` | Planned – automatic template generation from `.voice` files | Controls automatically available once data lands | Aim for conversational fluency first, then fast review | Require platform braille table verification per locale | Request dictionary/corpus donation when adding profiles | Prioritise high-demand locales (e.g., Hindi, Arabic, Mandarin, Russian) |
| Symbols, emoji, technical scripts | Bundled – raw Unicode passthrough; curated IPA fallbacks queued | Planned – per-script pronunciation tables | Planned – synthetic template packs for specialised domains | Phoneme picker already handles custom replacements | Focus on announcing punctuation and emoji skin-tone variants | Braille math/tech tables to follow speech mapping | Collecting Unicode data files and SMuFL symbol corpora | Encourage domain experts to contribute script- or context-specific datasets |

We tag each locale with the most advanced assets we have shipped so far. When you contribute a new language, please:

1. Import or reference the eSpeak NG phoneme block (or another public dataset) inside `eloquence_data/phonemes/`.
2. Create a language profile file under `eloquence_data/languages/` that documents characters, digraphs, stress behaviour, and grammatical notes.
3. Supply at least one voice template—either handcrafted JSON or an auto-converted `.voice` file—so NVDA users can hear the locale immediately.
4. Outline any remaining gaps (for example, “needs tone marks” or “emoji coverage pending”) so we can keep the roadmap transparent.

Short-term expansion priorities include Hindi, Arabic, Mandarin Chinese, Russian, Japanese, Korean, and the major Indic languages highlighted by Hear2Read. These locales already have mature eSpeak NG voices and large user communities eager for low-latency synthesizers.

### Generative and contextual pronunciation layers
Classic pronunciation dictionaries cannot anticipate every linguistic twist, so the project now blends curated datasets with generative logic. Each language profile documents when a phoneme is produced directly from an upstream catalogue, when a contextual rule (for example, liaison in French or lenition in Spanish) adjusts that phoneme, and when a generative model proposes alternatives. NVDA’s phoneme picker mirrors this structure: the **Phoneme category** and **Phoneme symbol** controls surface every static token, while the **Phoneme replacement** menu lists contextual and generative options alongside the legacy defaults. Contributors should flag whether a pronunciation comes from eSpeak NG, DECtalk, a heritage dataset, or a generative routine so keyboard users understand the provenance of what they hear.

Context-aware replacements support grammar- and position-sensitive tweaks. For instance, language profiles can specify different IPA hints when a consonant appears between vowels, at the end of a clause, or as part of a digraph. When NVDA announces phoneme replacements, the dialog now highlights whether the entry is **contextual** (triggered by written grammar) or **generative** (calculated at runtime). This approach lets blind users audition variations quickly and lock in the most intelligible combination.

### Toward universal script and symbol coverage
Pronunciation dictionaries alone cannot keep up with the creative ways people mix alphabets, emoji, ASCII art, mathematical notation, or braille patterns in everyday text. Eloquence Threshold therefore centres on a **phoneme, sound, and symbol customiser** that you can drive entirely from NVDA's Speech dialog:

- Every phoneme exposed by Eloquence, DECtalk, or eSpeak NG can be reassigned to words, IPA samples, or raw engine tokens, and those overrides are stored per user so the same keyboard shortcuts work across all contexts.
- Character-level language profiles describe how scripts sound—covering letters, digraphs, punctuation, and grammatical cues—so future dictionary imports can map text passages (sentences, paragraphs, essays, or book formats) directly onto phoneme sequences.
- Contributors are encouraged to add corpora-specific dictionaries (for example, math textbooks, programming languages, or lyrical content) as structured JSON so the driver can swap context-aware hints without breaking the underlying phoneme sliders.
- Because NVDA already passes through arbitrary Unicode code points, you can build replacement tables for historical scripts, emoji ZWJ sequences, or mixed-language hashtags. Share these assets in the repository so others can benefit without waiting for upstream dictionary updates.

Our aim is that any character in the Unicode standard—and any combination that writers invent—can be spoken accurately by selecting the right language profile, tweaking phoneme replacements, or loading a specialised voice template. As we fold in more eSpeak NG, DECtalk, and community archives, we will continue publishing coverage snapshots and inviting specialists to fill the remaining gaps.

### Cross-platform packaging roadmap
Eloquence Threshold remains focused on NVDA today, but the shared data catalogue is being curated so other screen readers can reuse it without redundant reverse engineering. Our packaging goals are:

- **NVDA (Windows)**: Ship `.nvda-addon` bundles containing synthesizer Python code, catalogues, and optional proprietary DLLs. The `build.py` helper documents required 32-bit and 64-bit binaries and supports offline packaging for lab deployments.
- **Narrator (Windows) and SAPI hosts**: Publish MSI installers that wrap the same voice catalogues and expose Eloquence through SAPI 5 voices. Parameter metadata will map to the registry-based slider model SAPI expects so screen readers receive identical presets.
- **Orca (Linux) / Speech Dispatcher**: Provide a Python module and `sd_module` bridge that reads the shared JSON catalogues, pairing them with platform-specific Eloquence/DECtalk libraries. Packaging will follow Flatpak or distribution-specific `.deb`/`.rpm` requirements with clear dependency lists.
- **VoiceOver (macOS/iOS/iPadOS) and TalkBack (Android)**: Deliver Swift/Kotlin wrappers that embed the shared phoneme and voice templates alongside platform-native audio backends. Distribution will leverage notarised `.pkg` installers for macOS and signed `.aab` packages for Android, with build instructions referencing Xcode/Gradle prerequisites.
- **ChromeVox (ChromeOS) and other embedded platforms (Apple TV, Android TV, watchOS)**: Export lightweight web packages or system extensions that read the JSON catalogues from a shared CDN. Documentation will explain how to script pronunciation updates so all platforms stay in sync.

Each release will document which catalogues (phonemes, language profiles, templates, generative rules) were validated on which platform, plus any braille or dictionary resources required to keep speech and tactile output aligned. Contributors interested in a new platform should open an issue outlining runtime requirements and how the existing build assets can slot into that environment.

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

### Archival scanning and extraction plan
Community mirrors like DataJake ship assets as `.exe`, `.zip`, `.7z`, `.cab`, and bespoke installer formats. To make those archives actionable inside the add-on:

1. **Inventory each directory.** Use `python tools/inventory_archives.py --roots <paths> --json docs/archive_inventory.json --markdown docs/archive_inventory.md` to crawl DataJake mirrors (or any extracted archive), capture filenames, sizes, timestamps, and previews, and produce JSON/Markdown manifests ready for review. Re-run the helper whenever new payloads are added so provenance reports stay current.
2. **Standardise extraction tooling.** Install `7z`, `unzip`, and `cabextract` (or the Python equivalents in `py7zr`/`zipfile`) before unpacking any archive. Expand every payload into a deterministic folder such as `build/extracted/<archive-name>/` so follow-up automation can diff contents without downloading the originals again.
3. **Normalise runtimes.** Move recovered `.dll`, `.syn`, `.ph`, `.dic`, and helper binaries into architecture-aware staging directories: `eloquence/` for legacy 32-bit builds, `eloquence_x86/`, `eloquence_x64/`, `eloquence_arm32/`, and `eloquence_arm64/` for platform-specific payloads. Language and phoneme data should flow into `eloquence_data/phonemes/ingest/` or a new locale folder under `eloquence_data/languages/` before conversion scripts run.
4. **Document provenance.** Record archive names, version strings, and source URLs inside the JSON metadata you produce (`extras.sourceArchive`, README tables, or automation notes) so future maintainers can validate licensing and trace changes.
5. **Automate parsing.** `AGENTS.md` tracks an open task to build a speech-data parser that converts extracted payloads into JSON catalogues, refreshes integration reports, and flags missing metadata. When you extend the inventory helper or introduce additional parsers, update both the README and the guidelines with invocation examples and expected outputs.

The Markdown table produced by `tools/inventory_archives.py` highlights the most recent additions (sorted by path depth), while the JSON payload can feed future CodeQL or CI comparisons that ensure cached datasets match the manifests developers expect.

This workflow ensures that every legacy synthesizer asset we inspect becomes a reproducible, well-documented contribution to the unified Eloquence dataset.

### Mining NV Speech Player data
- The [NV Speech Player repository](https://github.com/nvaccess/NVSpeechPlayer) is now part of our reference stack. The bundled `eloquence_data/phonemes/nvspeechplayer_core.json` file was generated directly from its `data.py` frame definitions so you can compare Eloquence’s handling of vowels and consonants with NVDA’s historical synthesizer.
- Voice presets under `eloquence_data/voices/nvspeechplayer_classics.json` approximate Adam, Benjamin, Caleb, and David. Each entry keeps the original NV Speech Player multipliers in the `extras.nvspeechPlayer` block—perfect for anyone who wants to refine the conversion or build tooling that translates presets automatically.
- When experimenting with upstream changes, pull fresh snapshots of `NVSpeechPlayer` and regenerate the JSON files before packaging. The helper at `tools/convert_nvspeechplayer.py` demonstrates how to carry over classification flags, formant targets, and amplitude settings so the NVDA voice dialog exposes the full dataset to keyboard users.

### Supplying 64-bit Eloquence binaries
- This project cannot redistribute proprietary Eloquence libraries. Extract the relevant runtime from a licensed product (for example, an updated Eloquence synthesizer package) and drop the DLLs into `eloquence_x86`, `eloquence_x64`, `eloquence_arm32`, or `eloquence_arm64` before packaging—or copy them directly into the matching `synthDrivers/eloquence/<arch>` folder after installing the add-on.
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
