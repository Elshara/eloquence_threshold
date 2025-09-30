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

Because NVDA 2026 builds execute as a 64-bit process, the add-on must load a 64-bit Eloquence runtime. The driver automatically discovers architecture-specific DLLs (for example, `eloquence/x64/eci.dll` or `eloquence/arm64/eci.dll`) and falls back to the classic 32-bit build when appropriate. The loader now walks the sibling `eloquence_x86`, `eloquence_x64`, `eloquence_arm32`, and `eloquence_arm64` directories as well as architecture subfolders inside `eloquence/`, then inspects the PE machine type so an x64 process never tries to load an ARM binary (and vice-versa). If a compatible library is missing the driver logs a clear error instead of silently failing, so you can populate the matching directories before packaging.

### File layout modernization status (October 2025)
We reshaped the repository so binaries, Python tooling, documentation, and dataset artefacts now live under `assets/<extension>/<descriptive_name>.<extension>` directories. This shallow layout makes it easier for blind and low-vision contributors to jump between related files with a screen reader, but it also means every loader must be retaught where to find voices, DLLs, and documentation. Track the migration—including outstanding speechdata cleanups and upcoming loader shims—in [`assets/md/file_structure_audit.md`](file_structure_audit.md). Regenerate the companion manifest with `python assets/py/report_speechdata_inventory.py` so [`assets/json/speechdata_inventory.json`](../json/speechdata_inventory.json) and [`assets/md/speechdata_manifest.md`](speechdata_manifest.md) stay aligned with your work. Keep those reports refreshed as you move assets so the NVDA community can follow the progress, rerun CodeQL, and rehearse the offline packaging drills without guessing where resources landed.

Runtime modules now resolve the new layout through [`assets/py/resource_paths.py`](../py/resource_paths.py). When you migrate additional payloads, extend the helper first and then update loaders or tooling to consume its lookups—this keeps the add-on working for partially migrated checkouts and streamlines follow-up CodeQL scans.

The modernization audit now tracks a remediation checklist covering loader updates, NV Speech Player dictionary moves, fixture planning, and legacy cache cleanups. Review the queue before every NVDA or CodeQL rehearsal so incremental work stays well documented and cached datasets remain reproducible for offline packaging drills.

To verify the reshuffle remains disciplined, refresh the extension inventory with `python assets/py/report_assets_layout.py --json assets/json/assets_layout_summary.json --markdown assets/md/assets_layout_summary.md --print`. The generated [`assets/md/assets_layout_summary.md`](assets_layout_summary.md) snapshot shows which buckets host binaries, documentation, JSON catalogues, or voice payloads and highlights any suffix mismatches before they break NVDA packaging or trigger CodeQL alerts.

When you need to review the legacy datasets that still depend on extensionless filenames, run `python assets/py/report_speechdata_extensionless.py`. The helper writes [`assets/json/speechdata_extensionless_inventory.json`](../json/speechdata_extensionless_inventory.json) and [`assets/md/speechdata_extensionless_inventory.md`](speechdata_extensionless_inventory.md), classifying likely WAV/OGG/ZIP/MIDI payloads and flagging text corpora that can gain `.txt` suffixes. Pair it with `python assets/py/report_speechdata_inventory.py` before every NVDA offline packaging rehearsal or CodeQL scan so reviewers can see which speechdata assets require new shims versus documentation-only updates.

### DataJake archive classification
To keep Eloquence's phoneme, lexicon, and tooling pipeline fresh we now version the entire DataJake archive manifest inside this repository. Run `python tools/catalog_datajake_archives.py` to regenerate `docs/archive_inventory.json` and the Markdown companion after updating `docs/datajake_archive_urls.txt`. The refreshed script adds extension, sample-rate, bit-depth (when detected), channel-layout, audio-fidelity tiers, `audio_signature` strings, language, BCP-47 language tags, synthesizer hints, collection families, voice-token, platform/architecture, version, category, viability, voice gender/age hints, and priority-tag summaries (plus per-entry metadata blocks and a metadata coverage rollup) so automation can spot IPA dictionaries, lexicon bundles, documentation stubs, NVDA add-ons, and direct `.dic`/`.lex` payloads without manually scanning 1,500 URLs. Cross-reference `docs/archive_code_targets.md` for examples of how these imports expand MBROLA coverage, inform CodeQL policies, and ensure our NVDA add-on ships with reusable pronunciation data across Eloquence, DECtalk/FonixTalk, IBM TTS, and RHVoice collections.

### Language expansion scorecard (refreshed)
### Global ISO/script onboarding sprint (Q4 2025 refresh)
- **New Latin clusters** – Afrikaans, Catalan, Danish, Estonian, Filipino, French, Galician, Irish, Italian, Lithuanian, Latvian, Polish, Romanian, Slovak, Slovene, and Vietnamese now carry roadmap entries in [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) with cross-links to their DataJake, Wikipedia, and NVDA provenance notes.
- **Dual-script locales** – Serbian (Cyrillic/Latin), Kazakh (Cyrillic/Latin), and Cantonese (Jyutping + Han) are tracked with mirrored tone and digraph planning, ensuring CodeQL policies surface both alphabets when regenerating lexicon payloads.
- **Tone-rich coverage** – Hausa, Yoruba, Thai, Vietnamese, Cantonese, and Mandarin now reference cached tone diagrams, lexical tone recordings, and NV Speech Player slider defaults so testers can validate contour changes while packaging.
- **Expanded morphology tooling** – GitHub-hosted finite-state transducers for Turkish, Finnish, and Hungarian are logged against the same roadmap, aligning contextual pronunciation generators with `language_profiles.py` descriptors.
- **Voice metric calibration** – Every locale snapshot references `docs/voice_parameter_report.md` so contributors can correlate NV Speech Player slider presets, EQ band groupings, and DataJake spectral captures before publishing new ISO profiles.
- **Frequency envelope atlas** – `tools/report_voice_frequency_matrix.py` now exports [`docs/voice_frequency_matrix.md`](docs/voice_frequency_matrix.md), mapping slider ranges to Hertz spans so phoneme EQ presets, NV Speech Player harmonics, and DataJake capture metadata stay aligned when calibrating new locales.
- **South Asian + Himalayan sprint** – Newly tracked Nepali (`ne`), Sinhala (`si`), Sindhi (`sd`), and Kashmiri (`ks`) pull vowel length, inherent schwa, and retroflex cues from cached Wikipedia grammar tables; DataJake `.lex` payloads and GitHub corpora are queued for CodeQL-audited imports while NVDA manuals confirm braille contractions.
- **Central and West Asian bridge** – Uzbek (`uz`), Uyghur (`ug`), and Pashto (`ps`) roadmap entries now cite dual Arabic/Latin script coverage with NVDA punctuation exports, while GitHub transliteration utilities back the switchable phoneme presets described in [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md).
- **Pan-African reinforcement** – Fula/Pulaar (`ff`), Somali (`so`), and Wolof (`wo`) dossiers log tone plateau, ATR harmony, and emphatic consonant references from DataJake lexicons; pairing them with NV Speech Player **Tone**, **Vocal range**, and **Sibilant clarity** defaults keeps the roadmap aligned with NVDA’s slider set.
- **Pacific and Caribbean pulse** – Haitian Creole (`ht`), Jamaican Patois (`jam`), Māori (`mi`), Samoan (`sm`), Tongan (`to`), Tahitian (`ty`), and Hawaiian (`haw`) roadmap entries now cite cached Wikipedia phonology tables, DataJake pronunciation archives, and NVDA braille exports so new Austronesian and Creole voices can launch with tone, nasalisation, and orthography metadata intact.
- **Heritage dictionary sweep** – Newly catalogued Wikipedia sources (see [`docs/language_research_index.md`](docs/language_research_index.md)) document high-value lexicographic corpora for Sinhala, Nepali, Somali, and Uzbek so `tools/catalog_datajake_archives.py` can flag matching `.dic`/`.lex` downloads before the next build.

### Micronesian and Polynesian revitalisation sprint (October 2025 follow-up)

- **Vanuatu–Guam corridor** – Bislama (`bi`) and Chamorro (`ch`) join the roadmap with Wikipedia phonotactic charts, DataJake broadcast lexicons, and GitHub orthography converters documented in [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md). NVDA manual exports back the braille punctuation plan so CodeQL packaging jobs can audit glottal stop handling before we seed new pronunciation profiles.
- **Palauan reef voices** – Palauan (`pau`) staging pairs DataJake civic-education corpora with NV Speech Player **Tone size**, **Vocal layers**, and **Sibilant clarity** presets; GitHub morphological analysers ensure reduplication cues sync with `language_profiles.py`, and the README build quickstart now reminds contributors to regenerate `docs/voice_frequency_matrix.md` after tuning the new sliders.
- **Niuean and Tokelauan tone ladder** – Niuean (`niu`) and Tokelauan (`tkl`) leverage cached Wikipedia vowel length studies plus NVDA braille exports to confirm macron coverage. We log the provenance trail in [`docs/language_research_index.md`](docs/language_research_index.md) and call for DataJake hymn dictionaries so the offline packaging drill captures the tonal contrast presets alongside the regenerated coverage dashboards.
- **Rapa Nui revitalisation** – Rapa Nui (`rap`) planning links GitHub revitalisation grammars with NVDA braille tables and DataJake oral-history recordings. Contributors should follow the "No-release packaging drill" below step by step—rehydrating cached reports, running `python tools/summarize_language_assets.py`, executing `python -m unittest discover tests`, and finishing with `python build.py --insecure --no-download --output dist/eloquence.nvda-addon`—to publish updated `eloquence.nvda-addon` builds without relying on public releases.

### Andean and Amazonian sprint (October 2025 follow-up)

- **Quechuan macrolanguage** – Quechua (`qu`, `quz`, `quy`) staging pulls vowel harmony and ejective consonant cues from cached Wikipedia grammar tables and DataJake `.dic` payloads. GitHub finite-state analyzers such as *qupobox* back the contextual pronunciation rules slated for `language_profiles.py`.
- **Aymara highland coverage** – Aymara (`ay`) entries prioritise uvular/velar contrasts recorded in NV Speech Player captures while NVDA punctuation exports guide braille hyphenation. CodeQL rules focus on validating glottal stop markers throughout dictionary imports.
- **Guaraní nasal harmony** – Guaraní (`gn`) roadmap updates align nasal harmony metadata from Wikipedia with DataJake lexicon inventories so NV Speech Player **Nasal balance**, **Subtones**, and **Tone size** sliders default to community expectations.
- **Mapudungun morphology** – Mapuche/Mapudungun (`arn`) datasets sourced from GitHub corpora pair with NV Access documentation caches to ensure braille exports honour rich agglutinative suffix chains. `phoneme_customizer.py` presets flag aspirated alveolar affricates for EQ calibration.
- **Shipibo-Conibo contouring** – Shipibo-Conibo (`shp`) planning references recorded tone contour research (Wikipedia + DataJake fieldwork archives) and seeds NV Speech Player **Inflection contour** defaults to keep rising/falling sequences intelligible at NVDA’s default rate.
- **Nahuatl revitalisation** – Nahuatl (`nah`) documentation cross-links DataJake audio captures, GitHub orthography normalisers, and NVDA manual punctuation tables to stage glottal stop, vowel length, and macro-morpheme cues for future pronunciation generators that the roadmap will capture in `language_profiles.py`.

### Central Eurasian Silk Road sprint (October 2025 extension)

- **Steppe vowel harmony** – Kyrgyz (`ky`) and Kazakh (`kk`) ingest cached Wikipedia vowel harmony charts alongside DataJake MBROLA lexicons and GitHub transliteration tools so dual Cyrillic/Latin presets share tone, vowel length, and apostrophe-based digraph cues. NVDA alpha manuals confirm braille behaviour before CodeQL gating.
- **Highland Persian corridor** – Tajik (`tg`) roadmap entries align Cyrillic-script resources with Persian phonology references while staging NV Speech Player **Tone**, **Vocal range**, and **Smoothness** presets. DataJake `.dic` payloads and GitHub transliteration utilities document Latin fallback mapping so offline builds bundle both scripts.
- **Uralic revitalisation** – Bashkir (`ba`), Chuvash (`cv`), and Udmurt (`udm`) dossiers log Wikipedia consonant harmony research, DataJake folk song recordings, and GitHub morphological analysers. The README workflow now calls for regenerating `docs/voice_frequency_matrix.md` and `docs/language_asset_summary.md` so NVDA sliders capture voiced/unvoiced harmony and palatalisation data before packaging.
- **Arctic Yakut tone planning** – Sakha/Yakut (`sah`) pulls vowel harmony and long consonant cues from cached Wikipedia sources, cross-references DataJake storytelling corpora, and maps NV Speech Player **Tone size**, **Scope depth**, and **Macro volume** sliders to match the recorded throat singing timbre while NVDA braille exports verify Cyrillic diacritic behaviour.
- **Silk Road provenance ledger** – [`docs/language_research_index.md`](docs/language_research_index.md) now tracks the Wikipedia dossiers for these locales, and `docs/iso_language_expansion.md` logs follow-up tasks for transliteration, dictionary extraction, and NV Speech Player preset validation so contributors can align DataJake, GitHub, and NVDA assets before staging CodeQL-audited imports.
- **Cross-source provenance** – Each locale references the regenerated dashboards in [`docs/language_progress.md`](docs/language_progress.md), [`docs/language_coverage.md`](docs/language_coverage.md), [`docs/language_maturity.md`](docs/language_maturity.md), and [`docs/voice_language_matrix.md`](docs/voice_language_matrix.md) to keep ISO coverage, speech parameters, and dictionary ingestion in sync with the README roadmap.

### Horn of Africa and Indian Ocean sprint (October 2025 extension)

- **Tigrinya and Afar onboarding** – Newly tracked Tigrinya (`ti`) and Afar (`aa`) locales in [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) combine Ethiopic script charts from Wikipedia, DataJake `.dic` inventories, and GitHub transliteration tooling with NVDA braille tables so Geez-derived punctuation and gemination cues survive offline packaging drills.
- **Somali + Malagasy tone ladder audit** – Somali (`so`) and Malagasy (`mg`) entries reference cached DataJake hymn and news corpora to tune NV Speech Player **Tone**, **Vocal range**, and **Inflection contour** sliders, while NV Access manual exports confirm comma and apostrophe handling before regenerating [`docs/voice_parameter_report.md`](docs/voice_parameter_report.md).
- **Swahili Rim support** – Kirundi (`rn`), Setswana (`tn`), Sango (`sg`), and Tsonga (`ts`) coverage uses GitHub lexical analyzers plus DataJake `.lex` payloads to map Bantu noun-class tones and prenasalised stops; README guidance now points contributors at the refreshed linkage matrix so packaging catches template/profile gaps early.
- **Cross-source research trail** – [`docs/language_research_index.md`](docs/language_research_index.md) logs the supporting Wikipedia bibliographies for this sprint and mirrors them in the JSON companion so CodeQL automation can verify every new locale cites its provenance across Wikipedia, DataJake, GitHub, and NVDA snapshots.
- **Offline validation cadence** – The sprint reiterates the `python tools/report_language_progress.py`, `python tools/report_language_coverage.py`, and `python build.py --insecure --no-download --output dist/eloquence.nvda-addon` workflow so contributors regenerate dashboards, run unit tests, and build the add-on without published releases while staging Ethiopic, Latin, and extended Latin scripts.

### Pan-Atlantic and Indian Ocean diaspora sprint (October 2025 follow-up)

- **Thaana + Devanagari bridge** – Dhivehi (`dv`) joins the roadmap with Thaana script baselines from cached Wikipedia typography studies, DataJake Qur’anic recitation lexicons, and NVDA braille tables that confirm right-to-left diacritics render correctly in offline builds. Parallel Maltese (`mt`) and Sinhala (`si`) refreshes reuse these artefacts to align consonant emphatics across the Indian Ocean corridor.
- **Lower Mekong tonal reinforcement** – Lao (`lo`) planning layers Wikipedia tone contour diagrams with GitHub IPA conversion utilities and DataJake sermon recordings so **Tone size**, **Scope depth**, and **Subtones** sliders inherit empirically tuned defaults. The sprint captures these updates in [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) alongside CodeQL notes for validating rising/falling contour generators.
- **Celtic revitalisation hooks** – Welsh (`cy`) and Breton (`br`) coverage now cite archived DECtalk dictionaries, GitHub finite-state mutation models, and NVDA braille manuals to enforce lenition/eclipsis behaviour. Contributors are pointed at `python tools/report_voice_frequency_matrix.py` so fricative emphasis bands track the consonant mutation rules recorded in the Wikipedia corpus.
- **Nilotic tone ladders** – Nuer (`nus`) documentation references DataJake scripture corpora, GitHub tone-tracking analyzers, and NV Speech Player recordings to seed nasal harmony and vowel length presets. These cues join the language maturity dashboard so testers can audit tonal accuracy before packaging.
- **Cross-source delta audit** – Regenerate the provenance suite (`python tools/summarize_language_assets.py`, `python tools/report_language_maturity.py`, and `python tools/report_voice_language_matrix.py`) after updating these locales so README metrics, the ISO roadmap, and CodeQL automation stay aligned with the latest Wikipedia/DataJake/GitHub/NVDA datasets.

### Saharan-to-Pacific bridging sprint (October 2025 continuation)

- **Tamazight and Kabyle expansion** – Central Atlas Tamazight (`tzm`) and Kabyle (`kab`) now carry roadmap entries in [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) detailing how cached [Afroasiatic research dossiers](docs/language_research_index.md) map Berber consonant emphatics to NV Speech Player **Plosive impact**, **Tone**, and **Overtones** sliders. We paired DataJake `.lex` payloads with GitHub Amazigh morphological analysers so the phoneme customiser respects tri-consonantal roots while retaining NVDA braille punctuation exports for Tifinagh ⇄ Latin workflows.
- **Sahelian corridor reinforcement** – Bambara (`bm`) progresses from an exploratory note to a staged profile with GitHub tonal corpora and DataJake scripture recordings that anchor ATR harmony and nasal vowel metadata. The regenerated [`docs/voice_parameter_report.md`](docs/voice_parameter_report.md) snapshot keeps **Nasal balance** and **Macro volume** presets aligned with Mali-based speech samples.
- **Pacific accessibility uplift** – Tok Pisin (`tpi`), Fijian (`fj`), and Marshallese (`mh`) join the roadmap with tone-neutral creole planning, vowel-length-aware frequency scaffolding, and GitHub orthography datasets catalogued in [`docs/language_research_index.md`](docs/language_research_index.md). NVDA manual exports validate punctuation and braille handling, while DataJake hymn recordings feed new EQ presets captured in [`docs/voice_frequency_matrix.md`](docs/voice_frequency_matrix.md).
- **Circumpolar Sámi bridge** – Lule Sámi (`smj`) inherits consonant gradation and vowel harmony references from cached Wikipedia phonology tables and GitHub finite-state analysers. We logged the sprint in the ISO roadmap and research index so CodeQL automation tracks the DataJake lexical payloads staged for NV Speech Player **Inflection contour** testing alongside NVDA alpha-52762 braille exports.
- **Packaging documentation refresh** – The offline quickstart workflow now highlights `python tools/report_integration_scope.py` and the updated [`docs/offline_packaging_playbook.md`](docs/offline_packaging_playbook.md) so contributors capture linkage deltas and provenance updates before building `eloquence.nvda-addon` without published releases.

### Gulf of Guinea and Great Lakes tonal sprint (October 2025 update)

- **Yoruba, Akan/Twi, and Ewe tonal ladders** – Yoruba (`yo`), Akan (`ak`), and Ewe (`ee`) now feature in [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) with tone-tier inventories sourced from cached Wikipedia phonology tables, DataJake hymn/sermon `.dic` payloads, and GitHub tonal grammar toolkits. We mapped their three-level tone ladders to NV Speech Player **Tone**, **Scope depth**, and **Subtones** sliders while logging braille punctuation checks against the NVDA alpha-52731 manual exports captured in [`docs/language_research_index.md`](docs/language_research_index.md).
- **Ga coastal resonance planning** – Ga (`gaa`) joins the roadmap with nasal vowel and glottal stop references harvested from the Wikipedia backlog and DataJake radio-broadcast corpora. The sprint ties these cues into the regenerated [`docs/voice_frequency_matrix.md`](docs/voice_frequency_matrix.md) snapshot so contributors can align **Nasal balance**, **Macro volume**, and **Overtones** presets with the new Gulf of Guinea lexicons before packaging.
- **Great Lakes contour reinforcement** – Luganda (`lg`) and Lingala (`ln`) entries highlight noun-class tone sandhi sourced from DataJake scripture collections and GitHub morphological analysers. We coordinated these updates with NVDA braille exports and CodeQL follow-ups to keep `language_profiles.py` expansion tasks aligned with [`docs/voice_language_matrix.md`](docs/voice_language_matrix.md) coverage gaps.
- **Southern Bantu tonal sweep** – Shona (`sn`) inherits downstep and whistled speech references from cached Wikipedia articles and DataJake pronunciation datasets. Contributors are now instructed to rerun `python tools/report_language_maturity.py` and `python tools/summarize_language_assets.py` after seeding new `.lex` payloads so the sprint's ISO additions surface in maturity dashboards and the offline packaging playbook.
- **Offline drill refresh** – The step-by-step build workflow below now calls out the refreshed tonal sprint artefacts alongside `python tools/report_voice_frequency_matrix.py` and `python tools/report_integration_scope.py`. Pair it with [`docs/offline_build_rehearsal.md`](docs/offline_build_rehearsal.md) and [`docs/offline_packaging_playbook.md`](docs/offline_packaging_playbook.md) when staging Yoruba/Akan/Ewe/Ga/Luganda/Lingala/Shona datasets for a no-release build validated against NVDA alpha snapshots and CodeQL policies.

### Philippine archipelago and Mainland Southeast Asia sprint (October 2025 extension)

- **Visayan and Ilokano coverage** – Cebuano (`ceb`), Hiligaynon (`hil`), and Ilocano (`ilo`) now join [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) with DataJake `.dic` hymn corpora, GitHub orthography datasets, and Wikipedia vowel harmony charts cited in [`docs/language_research_index.md`](docs/language_research_index.md). We mapped their glottal stop and vowel length cues to NV Speech Player **Tone size**, **Subtones**, and **Inflection contour** sliders so the README scorecards surface Visayan resonance requirements before packaging.
- **Waray and Kapampangan phonology bridge** – Waray-Waray (`war`) planning layers Eastern Visayan stress references from cached Wikipedia pages with DataJake scripture recordings, while Kapampangan (`pam`) staging—tracked alongside Waray in the ISO roadmap—uses GitHub orthography converters to validate Austronesian glottal marker handling inside NVDA braille exports. Contributors should rerun `python tools/report_language_progress.py` and `python tools/report_language_coverage.py` after seeding these corpora so CodeQL automation registers the expanded Central Philippines coverage.
- **Hmong-Mien tonal matrices** – Hmong Daw (`hmn`) and Mizo/Lushai (`lus`) roadmap entries log the five- to eight-level tone charts pulled from Wikipedia and DataJake oral history archives; GitHub tonal contour notebooks backstop the NV Speech Player **Tone**, **Scope depth**, and **Whisper** presets captured in [`docs/voice_frequency_matrix.md`](docs/voice_frequency_matrix.md). Regenerate the frequency atlas and [`docs/voice_parameter_report.md`](docs/voice_parameter_report.md) once new tonal samples land to keep the slider catalogue aligned with Mainland Southeast Asia datasets.
- **Offline rehearsal updates** – [`docs/offline_build_rehearsal.md`](docs/offline_build_rehearsal.md) and [`docs/offline_packaging_playbook.md`](docs/offline_packaging_playbook.md) now call out the Visayan/Hmong sprint so offline builders script DataJake archive restoration, Wikipedia provenance capture, and NVDA braille validation before running the packaging commands below.

### Adriatic and Balkan sprint (October 2025 follow-up)

- **Four-accent calibration** – Albanian (`sq`), Bosnian (`bs`), Croatian (`hr`), and Serbian (`sr`, `sr-Latn`) gain refreshed roadmap notes in [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) that tie cached Wikipedia pitch-accent charts to DataJake radio/news `.dic` payloads and GitHub morphological analysers. We aligned NV Speech Player **Inflection contour**, **Tone size**, and **Sibilant clarity** presets with the regenerated [`docs/voice_frequency_matrix.md`](docs/voice_frequency_matrix.md) snapshot so rising vs. falling patterns surface directly in NVDA’s Speech dialog.
- **Dual-script resilience** – Serbian Cyrillic/Latin toggles, plus the newly tracked Montenegrin (`cnr`) orthography reforms, are now documented alongside NVDA manual exports and CodeQL follow-ups to guarantee punctuation parity across scripts. Contributors staging DataJake `.lex` bundles should rerun `python tools/report_language_progress.py` and `python tools/report_language_maturity.py` to confirm dual-script templates stay in lockstep with the README workflow.
- **Slavic vowel reduction roadmap** – Macedonian (`mk`) and Slovene (`sl`) entries pair Wikipedia schwa/pitch-accent research with GitHub transliteration utilities and DataJake hymn corpora. Refresh [`docs/language_research_index.md`](docs/language_research_index.md) and rerun `python tools/summarize_language_assets.py` after capturing new bibliographies so provenance dashboards flag the Adriatic delta before packaging.
- **Offline packaging alignment** – The offline quickstart and packaging playbook now highlight the Adriatic sprint, reminding contributors to refresh NV Access manual audits (`python tools/audit_nvaccess_downloads.py` + `python tools/check_nvda_updates.py`) and log the run in `AGENTS.md` before producing `eloquence.nvda-addon` without a published release.

### Western Romance and Basque revitalisation sprint (October 2025 follow-up)

- **Pyrenean bridge** – Basque (`eu`) and Occitan (`oc`) gain roadmap entries in [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) that cite cached Wikipedia ergative-absolutive primers, vowel harmony notes, and troubadour-era phonology charts. We paired these sources with DataJake radio drama lexicons and GitHub Basque/Occitan morphological analysers so NV Speech Player **Inflection contour**, **Nasal balance**, and **Tone** sliders have contextual defaults before CodeQL-gated dictionary imports.
- **Rhaeto-Romance coverage** – Romansh (`rm`) and Friulian (`fur`) dossiers combine Wikipedia orthography reforms, DataJake civic-language corpora, and NVDA braille exports to map digraphs (`tg`, `gl`, `sc`) back to Eloquence phoneme bands. Contributors should regenerate `docs/voice_parameter_report.md` and `docs/voice_frequency_matrix.md` after tuning the new alveolar fricative emphasis so automation keeps the EQ atlas aligned.
- **Island and alpine dialect weave** – Sardinian (`sc`) and Corsican (`co`) roadmap updates document DataJake liturgical recordings, GitHub vowel centralisation studies, and NVDA braille punctuation tests. The README offline drill now calls out these heritage Romance dialects so builders validate **Vocal range**, **Subtones**, and **Macro volume** presets after staging `.lex` payloads.
- **Cross-border Germanic pulse** – Luxembourgish (`lb`) and West Frisian (`fy`) references blend Wikipedia digraph inventories with DataJake parliamentary corpora and GitHub spelling normalisers. Refresh [`docs/language_research_index.md`](docs/language_research_index.md) and rerun `python tools/report_language_progress.py` so NVDA’s Speech dialog surfaces the updated IPA scorecards alongside NV Speech Player **Stress**/**Sibilant clarity** defaults.
- **Astur-Leonese resonance** – Asturian (`ast`) and Walloon (`wa`) planning leans on cached Wikipedia nasal vowel research, DataJake folk song dictionaries, and NVDA braille contractions. Update the offline packaging playbook to acknowledge their palatal lateral cues, and run `python tools/summarize_language_assets.py` before packaging to log the newly paired dictionary and frequency assets.

### Circumpolar and Siberian revitalisation sprint (October 2025 continuation)

- **Uralic convergence** – Komi-Zyrian (`kpv`), Komi-Permyak (`koi`), Meadow Mari (`mhr`), and Hill Mari (`mrj`) entries now live in [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) with vowel harmony, palatalisation, and voiceless lateral data captured from cached Wikipedia grammars. We paired those notes with DataJake hymn dictionaries, GitHub finite-state analysers, and NVDA braille exports so CodeQL-audited imports keep dual Cyrillic/Latin scripts aligned before staging pronunciation profiles in `language_profiles.py`.
- **Ob River contour sweep** – Khanty (`kca`) and Mansi (`mns`) dossiers log Siberian oral history captures from the DataJake archive, GitHub morphological segmentation notebooks, and NV Speech Player **Tone size**, **Scope depth**, and **Subtones** defaults tuned from frequency-domain analyses. Contributors should rerun `python tools/report_voice_frequency_matrix.py` and `python tools/report_voice_parameters.py` after adjusting these presets so harmonic envelopes match the recorded Uralic continuum.
- **Arctic Samoyedic and Tungusic bridge** – Nenets (`yrk`), Evenki (`evn`), and Even (`eve`) roadmap rows cite nasal harmony and ejective consonant cues from cached Wikipedia fieldwork plus NVDA manual exports that document Cyrillic diacritic behaviour. We reference GitHub corpus parsers and DataJake scripture lexicons to seed NV Speech Player **Nasal balance**, **Plosive impact**, and **Whisper** defaults; regenerate the coverage dashboards via `python tools/report_language_progress.py` and `python tools/report_language_coverage.py` whenever these assets shift.
- **Trans-Bering revitalisation** – Chukchi (`ckt`), Nivkh (`niv`), Ainu (`ain`), and Aleut (`ale`) additions stitch together Wikipedia orthography tables, GitHub revitalisation grammars, DataJake narrative recordings, and NVDA braille exports so polysynthetic and ergative structures stay audible offline. `python tools/report_integration_scope.py` and `python tools/report_catalog_status.py` now surface these locales in the linkage matrix, and the README quickstart reminds builders to refresh the provenance suite before packaging `eloquence.nvda-addon` from cached mirrors.

### Global sign-language accessibility sprint (October 2025 extension)

- **North American corpus bridge** – American Sign Language (`ase`) roadmap coverage links cached Wikipedia handshape/phonology primers with DataJake ASL glossaries, GitHub SignWriting converters, and NVDA braille exports so offline builders can map manual parameters to NV Speech Player **Tone**, **Inflection contour**, and **Vocal layers** sliders before CodeQL-audited dictionary ingestion.
- **Commonwealth visual pathways** – Auslan (`asf`) and British Sign Language (`bfi`) planning pairs DataJake broadcast caption corpora with GitHub HamNoSys renderers and NVDA manual punctuation captures; contributors are instructed to rerun `python tools/report_voice_language_matrix.py` and `python tools/report_language_progress.py` after seeding dual-handed phoneme bundles so coverage dashboards record the signed-to-spoken mapping cadence.
- **Francophone sign cluster** – French Sign Language (`fsl`) sourcing leans on cached Wikipedia history and phonology timelines, DataJake bilingual lexicons, and NVDA braille contractions, ensuring **Scope depth**, **Sibilant clarity**, and **Macro volume** presets reflect paired spoken-language cues for interpreters packaging tactile-first presets.
- **Global summit harmonisation** – International Sign (`ils`) and Kenyan Sign Language (`xki`) dossiers coordinate GitHub gesture datasets, DataJake educational corpora, and NVDA alpha-52731 braille exports. The sprint adds validation checkpoints for motion-to-phoneme alignment via `python tools/validate_language_pronunciations.py` so CodeQL policies can flag gesture gloss drift before builders refresh `eloquence.nvda-addon` offline.

### Anatolian and Caspian convergence sprint (October 2025 addition)

- **Caucasus arc onboarding** – Abkhaz (`ab`), Adyghe (`ady`), Kabardian (`kbd`), and Laz (`lzz`) join [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) with cached Wikipedia ejective consonant inventories, DataJake Caucasus grammar corpora, and GitHub palatalisation analysers steering NV Speech Player **Plosive impact**, **Tone**, and **Sibilant clarity** presets. NVDA braille exports for Georgian and Cyrillic scripts anchor the dual-script fallback story while CodeQL gating tracks dictionary imports.
- **Kurdish and Caspian linkage** – Kurmanji (`kmr`), Sorani (`ckb`), and South Azerbaijani (`azb`) roadmap entries cross-reference DataJake radio glossaries, GitHub morphological generators, and NVDA manual punctuation tables to balance Perso-Arabic and Latin orthographies. The offline build workflow now calls out `python tools/validate_language_pronunciations.py` after regenerating the coverage dashboards so vowel harmony and tanwīn-style diacritics survive offline packaging.
- **Research dossier refresh** – [`docs/language_research_index.md`](docs/language_research_index.md) and its JSON companion catalogue new Wikipedia sources for Talysh (`tly`), Zazaki (`zza`), and Caspian Kurdish prosody. Pair the catalogue with `python tools/catalog_datajake_archives.py --json docs/archive_inventory.json --markdown docs/archive_inventory.md` before seeding new `.dic` archives so CodeQL automation and the offline playbook record tone sandhi, emphatic consonants, and NV Speech Player slider expectations for the sprint.

### Atlantic Sahel convergence sprint (October 2025 progression)

- **Wolof and Serer tone bridges** – Wolof (`wo`) and Serer (`srr`) rows in [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) now log cached Wikipedia ATR harmony studies, DataJake Dakar radio lexicons, GitHub nasal harmony analysers, and NVDA braille exports. The README sprint calls for recalibrating NV Speech Player **Tone**, **Scope depth**, and **Macro volume** sliders so CodeQL-audited dictionary imports capture long-vowel vs. consonant gemination cues.
- **Fulfulde and Soninke corridor** – Fula/Pulaar (`ff`) moves from *planned* to *researching* status alongside new Soninke (`snk`) coverage. We reference DataJake Qur’anic recitations, GitHub Ajami↔Latin transliteration tools, and NV Access manual punctuation exports to preserve implosive consonants and prenasalised stops. Regenerate `docs/voice_frequency_matrix.md` so frequency envelopes reflect the Sahelian bass emphasis before packaging.
- **Mooré and Bambara expansion** – Mooré (`mos`) and Bambara (`bam`) additions capture Burkina Faso and Mali corpora sourced from DataJake, cross-checking Wikipedia noun-class tone ladders and NV Speech Player **Subtones**/**Nasal balance** presets. GitHub morphological pipelines anchor affix ordering so `language_profiles.py` can expose contextual pronunciation for the Mossi and Manding families.
- **Zambezi resonance** – New Bemba (`bem`) and Lozi (`loz`) entries trace Zambia/Zimbabwe tonal corpora, DataJake hymn dictionaries, and NVDA braille exports. Contributors should refresh `docs/language_asset_summary.md` and rerun `python tools/report_voice_parameters.py` to confirm **Vocal layers**, **Plosive impact**, and **Head size contour** align with the lower-register recordings staged for this sprint.
- **Offline packaging reminder** – Before packaging these Atlantic–Sahel locales, replay the no-release drill below, then log the run in `AGENTS.md`. Pair the reports with `python tools/audit_nvaccess_downloads.py` and `python tools/check_nvda_updates.py` so NVDA alpha validations stay current while you seed new tone dictionaries from cached DataJake mirrors.

### Trans-Baikal and Oirat resonance sprint (October 2025 update)

- **Lake Baikal coverage** – Buryat (`bxr`) joins [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) with cached Wikipedia vowel harmony diagrams, DataJake steppe storytelling corpora, and GitHub morphological parsers. NVDA braille exports confirm dotted vs. umlauted vowel handling so we can stage NV Speech Player **Tone size**, **Scope depth**, and **Sibilant clarity** presets before CodeQL-audited dictionary imports.
- **Volga steppe revival** – Kalmyk/Oirat (`xal`) entries reference DataJake Buddhist scripture recordings, GitHub Kalmyk orthography converters, and NVDA manual exports that document Cyrillic vowel signs. Contributors should refresh `docs/voice_frequency_matrix.md` and `docs/voice_parameter_report.md` after tuning **Macro volume**/**Subtones** for the low-register chants.
- **Tyvan throat resonance** – Tuvan (`tyv`) planning pulls Wikipedia khoomei contour research and DataJake harmonic analyses into [`docs/language_research_index.md`](docs/language_research_index.md). Regenerate `docs/language_progress.md` and `docs/language_coverage.md` so tone layering, uvular stops, and breathy phonation presets align with NV Speech Player **Vocal layers** and **Whisper** sliders.
- **Altai and Dolgan continuum** – Southern Altay (`alt`) and Dolgan (`dlg`) roadmap rows cite GitHub Turkic finite-state analysers, DataJake dictionary scans, and NVDA braille exports to verify dotted I vs. diacritic behaviour. Update `python tools/report_language_maturity.py` outputs so mutual intelligibility planning across Turkic Siberia remains transparent to offline builders.
- **Yakutic reinforcement** – Sakha/Yakut (`sah`) gains refreshed harmonic notes comparing cached Wikipedia vowel length data with DataJake long-form storytelling archives. Contributors should re-run the no-release drill—`python tools/summarize_language_assets.py`, `python tools/report_language_progress.py`, `python tools/report_language_coverage.py`, `python -m unittest discover tests`, and `python build.py --insecure --no-download --output dist/eloquence.nvda-addon`—before logging the sprint in `AGENTS.md`.

### North Atlantic and Ligurian maritime sprint (October 2025 addition)

- **Faroe archipelago staging** – Faroese (`fo`) planning now cites cached Wikipedia vowel length and stød research, DataJake hymn lexicons, GitHub Faroese lemmatisers, and NVDA braille exports so **Tone size**, **Inflection contour**, and **Nasal balance** sliders cover insular North Germanic contrasts alongside CodeQL-audited dictionary staging.
- **Liguro-Venetian corridor** – Ligurian (`lij`) and Venetian (`vec`) coverage connects historical orthography surveys on Wikipedia with DataJake diaspora corpora and GitHub Romance revitalisation grammars. The roadmap captures how NV Speech Player **Macro volume**, **Sibilant clarity**, and **Scope depth** presets track coastal prosody while NVDA braille exports validate Ò/Ù diacritics.
- **Offline step-by-step refresh** – The cloning-and-build checklist below now calls out Faroese/Ligurian/Venetian provenance. Pair `python tools/catalog_wikipedia_languages.py`, `python tools/report_voice_parameters.py`, and the existing reporting suite with `python tools/audit_nvaccess_downloads.py --roots releases/stable snapshots/alpha --max-depth 2 --limit-per-dir 12 --insecure --json docs/download_nvaccess_snapshot.json --markdown docs/download_nvaccess_snapshot.md` to ensure offline builders validate NVDA alpha-52762 compatibility before running `python build.py --insecure --no-download --output dist/eloquence.nvda-addon`.

After each documentation or profile change, regenerate the cached coverage artefacts so pull requests reflect the current dataset without hammering upstream mirrors:

- `python tools/summarize_language_assets.py --json docs/language_asset_summary.json --markdown docs/language_asset_summary.md --print`
- `python tools/report_language_maturity.py --json docs/language_maturity.json --markdown docs/language_maturity.md --print`
- `python tools/report_language_progress.py --json docs/language_progress.json --markdown docs/language_progress.md --print`
- `python tools/report_language_coverage.py --json docs/language_coverage.json --markdown docs/language_coverage.md --print`
- `python tools/report_voice_language_matrix.py --json docs/voice_language_matrix.json --markdown docs/voice_language_matrix.md --print`
- `python tools/report_voice_frequency_matrix.py --json docs/voice_frequency_matrix.json --markdown docs/voice_frequency_matrix.md --print`
- `python tools/report_integration_scope.py --json docs/integration_scope.json --markdown docs/integration_scope.md --print`
- `python tools/report_voice_parameters.py --json docs/voice_parameter_report.json --markdown docs/voice_parameter_report.md --print`
- `python tools/report_catalog_status.py --json docs/catalog_status.json --markdown docs/catalog_status.md`
- `python tools/validate_language_pronunciations.py --json docs/language_pronunciation_validation.json --markdown docs/language_pronunciation_validation.md`

The current snapshot (53 language profiles across 70 templates) reports a 39% average IPA completion rate with Gujarati and Indonesian leading at 100%. These Markdown/JSON pairs power the tables referenced throughout `docs/iso_language_expansion.md` and surface gaps where additional phoneme dictionaries, contextual rules, or DataJake archives should be prioritised. CodeQL workflows ingest the JSON outputs to ensure new dictionary parsers or ISO ingestion scripts never regress coverage or introduce unsafe archive handling.

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
- Feed the cached snapshot into `python tools/report_nvaccess_tree.py --snapshot docs/download_nvaccess_snapshot.json --recommendations docs/nvda_update_recommendations.json --json docs/nvaccess_tree.json --markdown docs/nvaccess_tree.md` to generate a hierarchy digest. The helper tallies per-folder file and directory counts, highlights the most recent uploads, and reuses the severity grades from the recommendation report without re-crawling the server.
- When two cached snapshots exist, diff them with `python tools/compare_nvaccess_snapshots.py --old docs/download_nvaccess_snapshot.json --new path/to/fresh_snapshot.json --markdown docs/download_nvaccess_delta.md`. The diff report reuses the same severity grading so contributors can track new alphas, disappearing archives, and metadata changes without rereading the entire tree.
- Feed any cached snapshot into `python tools/report_nvda_compatibility.py --snapshot docs/download_nvaccess_snapshot.json --validated docs/validated_nvda_builds.json --markdown docs/nvda_compatibility_matrix.md --json docs/nvda_compatibility_matrix.json` to generate a descending-by-date compatibility matrix. The new helper mirrors NVDA’s alpha cadence from https://github.com/nvaccess/nvda/, reuses the audit severity grades, and publishes Markdown/JSON artefacts that CodeQL jobs or downstream automation can diff to spot risky releases quickly.
- Translate those severity grades into concrete actions with `python tools/check_nvda_updates.py --snapshot docs/download_nvaccess_snapshot.json --validated docs/validated_nvda_builds.json --manifest manifest.ini --markdown docs/nvda_update_recommendations.md --json docs/nvda_update_recommendations.json`. The CLI sorts entries by modification date, maps each release or snapshot to an "update", "monitor", "downdate", "keep", or "investigate" recommendation, and documents why that action is appropriate for the Eloquence add-on.
- Severity levels surface how urgently Eloquence must react: **high** means the entry is newer than our validated snapshot, **medium** matches the recorded baseline, **low** is older but still available for downgrades, and **info** indicates a release that remains inside the supported window. Update `docs/validated_nvda_builds.json` whenever you finish testing a new NVDA build so future audits share the same baseline.
- Use `--insecure` when the environment lacks a full certificate store (as in this development container). Production automation should omit the flag so TLS verification remains intact.

### Wikipedia research backlog
- Consult [`docs/language_research_index.md`](docs/language_research_index.md) for a curated list of Wikipedia sources covering ISO 639/15924 codes, language families, regional dashboards, constructed languages, and programming-language pronunciation needs. Each row documents usefulness, ingestion progress, and whether the page informs language, dialect, accent, or orthography planning.
- The companion JSON file (`docs/language_research_index.json`) feeds future automation that will merge ISO code data into the seed bundles at `eloquence_data/languages/world_language_seeds.json` and `eloquence_data/voices/eloquence_global_seeds.json`. Update the JSON as you convert tables into structured data so NVDA's configuration exports inherit authoritative identifiers.
- When you incorporate research from these sources, refresh the canonical Wikipedia crawl via `python tools/catalog_wikipedia_languages.py --output-json docs/wikipedia_language_index.json --output-markdown docs/wikipedia_language_index.md` and rerun the reporting helpers (`tools/report_language_coverage.py`, `tools/report_language_progress.py`, `tools/report_voice_language_matrix.py`, and `tools/report_voice_parameters.py`). This keeps NVDA's speech dialog aligned with the documented tier (language → dialect → accent) while also surfacing related buckets such as sign languages, orthographies, language families, conlangs, programming languages, and ISO standards so phoneme EQ presets can bridge spoken and technical contexts.

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

#### Language coverage milestones
- Run `python tools/report_language_coverage.py --json docs/language_coverage.json --markdown docs/language_coverage.md --print` after updating any voice template, language profile, or phoneme dataset. The helper grades how mature each locale is by counting documented characters, linked templates, and IPA coverage, then surfaces gaps that need follow-up work before packaging.
- The Markdown summary highlights locales that ship with both profiles and templates versus those that only have one or the other. Use it alongside the linkage matrix to decide where to focus new pronunciation research, slider presets, or phoneme imports from eSpeak NG, DECtalk, NV Speech Player, or DataJake archives.
- The JSON report feeds automation so CodeQL or CI jobs can watch for regressions—missing templates, shrinking IPA coverage, or locales that accidentally lose their character inventories.

#### Language progress dashboard
- Run `python tools/report_language_progress.py --json docs/language_progress.json --markdown docs/language_progress.md --print` whenever you expand a language profile, add contextual pronunciation notes, or update README tables about locale maturity. The helper cross-references the phoneme catalogue and voice templates to score each profile, highlighting IPA coverage, documented examples, structural guidance, and how many default templates already bundle the locale.
- The Markdown digest provides a sortable matrix of every language with its stage (seed, developing, established, comprehensive) alongside counts of examples, notes, and default templates. The JSON payload mirrors those values so CodeQL and CI can spot regressions or celebrate milestones automatically.
- Inside NVDA's Speech dialog the language profile picker now surfaces these metrics directly. Each entry announces its IPA coverage, stage, example count, and whether generative/contextual pronunciation layers or keyboard-friendly digraphs are available, keeping blind testers oriented while they experiment with new locales.

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

The scorecard mirrors the generated snapshot and highlights which installers or manuals deserve immediate attention. Extend the table whenever you validate additional beta, RC, or try builds so contributors know what to test next. Pair NVDA audit refreshes with updates to `docs/iso_language_expansion.md` and the cached language scorecards so cached datasets, CodeQL checks, and packaging steps stay aligned across pull requests.

## Global language expansion and ISO coverage
We are steadily expanding Eloquence to align with ISO 639/BCP-47 language tags, Unicode script metadata, and the speech parameter envelopes documented by NV Speech Player, DECtalk/FonixTalk, IBM TTS, and community archives. The latest roadmap snapshot lives in [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) and summarises:

- Which ISO 639-1/639-2 codes and companion scripts already have seeded phoneme inventories or voice templates.
- Script coverage priorities mapped from the [Wikipedia language index](docs/wikipedia_language_index.md), including planned ingestion of sign-language and orthography references.
- Speech parameter and frequency-band combinations captured from NVDA's slider catalogue, with notes on the DataJake archive items that inform EQ calibration.
- Dictionary and phoneme datasets currently staged from GitHub, NVDA upstream tooling, and archived Eloquence `.dic`/`.lex` resources.
- Vocal metrics we expose through NVDA's Speech dialog so blind users can judge cadence, timbre, range, and contextual pronunciation in real time.

The document tracks progress milestones so contributors can focus on underrepresented locales or script families (for example Ethiopic, Vai, Cherokee, Ol Chiki, Tengwar proposals, or revived Hebrew cantillation). Pair it with the generated [`docs/language_progress.md`](docs/language_progress.md) and [`docs/voice_parameter_report.md`](docs/voice_parameter_report.md) dashboards when refining phoneme datasets or adding NV Speech Player-style sliders to the voice picker.

### Wikipedia, DataJake, GitHub, and NVDA utilisation dashboard
| Source | What we mirror | Refresh helper | Latest snapshot | Next actions |
| --- | --- | --- | --- | --- |
| Wikipedia | ISO/script taxonomy, dialect flags, language family rollups, orthography research, endangered-language dashboards. | `python tools/catalog_wikipedia_languages.py --output-json docs/wikipedia_language_index.json --output-markdown docs/wikipedia_language_index.md` | `docs/wikipedia_language_index.md` (seeded via 2025-09 cache). | Add Assamese, Javanese, Maithili, Thai, and Northern Sotho macrolanguage cross-references before seeding new profiles. |
| DataJake archives | `.dic`/`.lex` lexicons, MBROLA voices, NV Speech Player captures, heritage SAPI payloads, pronunciation spreadsheets. | `python tools/catalog_datajake_archives.py --json docs/archive_inventory.json --markdown docs/archive_inventory.md` | `docs/archive_inventory.md` + `docs/archive_code_targets.md` (inventory refreshed 2025-09). | Promote high-value Assamese, Maltese, and Cree archives into `eloquence_data/` with duplicate lexeme checks in `tests/test_archive_catalog.py`. |
| GitHub | eSpeak NG phoneme tables, NV Speech Player JSON exports, open-source kana/IPA mappers, historical DECtalk dictionaries. | `git submodule update` where applicable plus manual mirrors recorded in `docs/language_research_index.md`. | `eloquence_data/` JSON bundles and README references. | Track upstream revisions and refresh `eloquence_data/espeak_phonemes.txt` + NV Speech Player captures before the next CodeQL audit. |
| NV Access | Installer/manual tree audits, nightly build metadata, severity scoring for regressions, documentation coverage. | `python tools/audit_nvaccess_downloads.py` followed by `python tools/check_nvda_updates.py` and `python tools/report_nvaccess_tree.py`. | `docs/nvda_update_recommendations.md`, `docs/nvaccess_tree.md`, `docs/download_nvaccess_snapshot.md`. | Compare the cached alpha-52762 snapshot against the next nightly once NV Access publishes fresh binaries and update severity guidance accordingly. |

Each refresh reuses cached datasets staged under `docs/` to avoid hammering upstream mirrors. When proposing ISO expansions, cite the relevant row(s) above so reviewers know which cached report informed the change and which helper command must be re-run after merge.

### Q4 coverage progress checkpoints
| Track | Highlights | Latest artefacts | Next action |
| --- | --- | --- | --- |
| **ISO + scripts** | Expanded roadmap now tracks 68 ISO codes with dual-script notes for Kazakh, Serbian, and Cantonese alongside new Afroasiatic (Tigrinya/Oromo) and Indo-Aryan (Odia/Punjabi) targets. | [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) | Validate sample wordlists for Tigrinya and Odia using cached Wikipedia inventories before seeding phoneme presets. |
| **Speech parameters** | Voice slider catalogue mirrors NV Speech Player metadata and now lists frequency scaffolds (8 kHz → 384 kHz) plus harmonic/noise band pairings for tone-heavy locales. | [`docs/voice_parameter_report.md`](docs/voice_parameter_report.md) | Import DataJake spectral captures for Hausa, Vietnamese, and Cantonese to calibrate tone and plosive presets. |
| **Phoneme datasets** | DataJake manifest audit highlights `.dic`/`.lex` payloads for Maltese, Cree, and Yupik; GitHub FST projects queued for Turkish/Hungarian contextual inflection. | [`docs/archive_inventory.md`](docs/archive_inventory.md) | Refresh `docs/archive_inventory.json` after triaging Cree/Yupik payloads so CodeQL checks inherit provenance metadata. |
| **Dictionary integrations** | README build drill references cached NVDA manuals and DataJake lexicons so offline packaging mirrors documentation used in tests. | [`docs/nvda_update_recommendations.md`](docs/nvda_update_recommendations.md) | Capture controller client deltas from the next NVDA nightly snapshot and flag severity in the recommendations report. |
| **Vocal metrics** | Voice-language matrix ties 70 voice templates to 53 locales and surfaces IPA completion percentages inside NVDA’s Speech dialog. | [`docs/voice_language_matrix.md`](docs/voice_language_matrix.md) | Extend `tools/report_voice_language_matrix.py` with tone-range annotations for Yoruba, Thai, and Vietnamese bundles. |

### Language maturity gap analysis

- **New maturity dashboard** – `python tools/report_language_maturity.py --json docs/language_maturity.json --markdown docs/language_maturity.md --print` now rolls up the cached [`docs/language_progress.json`](docs/language_progress.json), [`docs/language_coverage.json`](docs/language_coverage.json), [`docs/voice_language_matrix.json`](docs/voice_language_matrix.json), and research metadata into a single scoreboard. It highlights locales that still need coverage snapshots, voice templates, or stage annotations so contributors can prioritise the next sprint without trawling multiple reports.
- **Cross-source alignment** – The generated [`docs/language_maturity.md`](docs/language_maturity.md) file calls out gaps (for example the placeholder `unspecified` voice template that lacks a labelled profile) alongside the languages that already include DataJake dictionaries, NVDA manual provenance, and Wikipedia-derived IPA inventories. Use the JSON companion when wiring CodeQL dashboards or packaging automation that depends on these counts.
- **Workflow integration** – Pair the maturity summary with the existing `tools/summarize_language_assets.py` output before building so you validate both per-language detail and aggregate coverage against the cached Wikipedia, DataJake, GitHub, and NV Access artefacts.

### Arctic and Indigenous language surge (October 2025)

- **Inuktitut (`iu`)** – Roadmap entries now tie syllabics sourced from `docs/wikipedia_language_index.md` and the
  *Inuktitut language* article to DataJake `.lex` payloads extracted from archived NVDA community bundles.  The README scorecards
  reference newly documented CodeQL guardrails for handling right-to-left syllabic glyphs while aligning NV Speech Player
  **Tone** and **Scope depth** sliders with Inuit Broadcasting Corporation recordings preserved in DataJake archives.
- **Cherokee (`chr`)** – Added syllabary coverage backed by the *Cherokee syllabary* and *Cherokee language* Wikipedia entries
  alongside DECtalk lexicon fragments recovered from GitHub mirrors.  Packaging guidance now calls out the need to map syllabary
  characters into NVDA’s braille translation tables before shipping Giduwa voice templates.
- **Greenlandic Kalaallisut (`kl`)** – Leveraging the *Greenlandic language* Wikipedia research dossier and GitHub morphological
  analysers to seed polysynthetic inflection handling.  NVDA manual excerpts for hyphenation and punctuation have been folded
  into the roadmap so CodeQL policies can track the complex affixation pipeline.
- **Northern Athabaskan targets** – Documented research hooks for *Dena’ina* and *Gwich’in* within `docs/language_research_index.md`
  so the next sprint can align tone ladder presets, DataJake archival wordlists, and NV Speech Player **Nasal balance** sliders.

These dossiers appear throughout [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) and the refreshed
`docs/language_research_index.*` files so contributors can trace Wikipedia, GitHub, DataJake, and NVDA provenance before staging
new phoneme presets.

### Eastern Europe and Caucasus integration sprint (October 2025)

- **Bulgarian (`bg`) + Macedonian (`mk`)** – Leveraged the cached *Bulgarian phonology* and *Macedonian language* Wikipedia
  pages to refine consonant cluster, schwa deletion, and stress rules.  DataJake MBROLA payloads are mapped to NV Speech Player
  **Stress**, **Vocal layers**, and **Plosive impact** sliders so testers can validate devoicing against cached alpha NVDA
  builds.  GitHub transliteration utilities feed CodeQL-reviewed scripts that convert historical Cyrillic spellings into
  Eloquence-ready grapheme clusters.
- **Georgian (`ka`) + Armenian (`hy`)** – Documented Mkhedruli and Mesropian orthography planning, pairing DataJake `.lex`
  payloads with the *Georgian language* and *Armenian language* Wikipedia inventories.  NVDA manual excerpts on punctuation and
  braille hyphenation are folded into [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md) to keep the
  cross-script loader guidance aligned with the add-on's architecture-aware directory scan.
- **Azerbaijani (`az`) and Kazakh (`kk`) dual script** – Staged Arabic, Latin, and Cyrillic variants using GitHub transliteration
  repos plus cached NVDA documentation so we can seed tri-script pronunciation presets.  DataJake lexicons inform the
  `phoneme_customizer.py` frequency clamps, while CodeQL policies watch for unsafe archive extraction when refreshing the
  language bundles.
- **Baltic reinforcement (`lt`, `lv`)** – Logged vowel length, pitch accent, and palatalisation research from Wikipedia and
  DataJake `.dic` payloads.  The roadmap now pairs these cues with NV Speech Player **Tone size**, **Subtones**, and **Sibilant
  clarity** defaults, ready for validation via cached GitHub corpora and NVDA alpha 52762 nightly builds.

Each locale entry in the roadmap now cross-references the maturity dashboard so developers can spot gaps in dictionary imports,
phoneme completion, or voice template coverage before packaging.  See [`docs/iso_language_expansion.md`](docs/iso_language_expansion.md)
for the full matrix plus forward-looking tasks, and log follow-up findings in `docs/language_research_index.md` to keep
Wikipedia/DataJake/GitHub/NVDA provenance synchronised with CodeQL guardrails.

### Caribbean and Central American sprint (October 2025)

- **Haitian Creole (`ht`) + Jamaican Patois (`jam`)** – Built on cached *Haitian Creole* and *Jamaican Patois* Wikipedia
  phonology portals, cross-linking nasal vowel charts, creole grammar baselines, and diaspora speech corpora.  DataJake
  hymn and radio lexicons are mapped to NV Speech Player **Inflection contour**, **Nasal balance**, and **Tone** sliders
  so we can rehearse prosody before importing the dictionaries under CodeQL supervision.  GitHub transliteration scripts
  help reconcile French-orthography punctuation with NVDA braille exports staged in the packaging playbook.
- **K'iche' (`quc`) and Garifuna (`cab`)** – Cached Mayan and Arawakan Wikipedia phoneme tables anchor ejective consonant
  and nasal harmony coverage while GitHub community grammars highlight dialect branches.  DataJake scripture corpora and
  community storytelling archives underpin planned `.dic` extractions, and NVDA braille snapshots confirm glottal stop and
  saltillo handling before we ship Central American presets.
- **Papiamento (`pap`) and Miskito (`miq`)** – Leveraged DataJake call centre, education, and historical speech archives
  to capture creole vowel mergers and Miskito nasal stress placement.  Wikipedia orthography notes pair with GitHub
  transliteration utilities, while cached NVDA documentation keeps punctuation and braille expectations aligned across
  Latin-script variants.  The new roadmap rows track frequency envelope experiments so we can stage NV Speech Player
  **Overtones**/**Scope depth** presets alongside dictionary ingestion tasks.

## Getting started
1. **Clone the repository** – `git clone https://github.com/pumper42nickel/eloquence_threshold.git` (or your fork) and `cd eloquence_threshold`. This is now the canonical way to obtain the add-on source when no release archive is published.
2. **Review the bundled data snapshots** – skim [`docs/wikipedia_language_index.md`](docs/wikipedia_language_index.md), [`docs/archive_inventory.md`](docs/archive_inventory.md), and [`docs/nvda_update_recommendations.md`](docs/nvda_update_recommendations.md) to understand which Wikipedia, DataJake, GitHub, and NVDA assets have already been ingested. These reports guide the ISO/script priorities documented above.
3. **Gather proprietary Eloquence binaries** – drop the classic runtime you are licensed to redistribute into the new assets layout: copy `ECI.DLL` (and friends) into `assets/dll/` and the `.syn` voices plus `.ph/.phs` helpers into `assets/syn/`. Architecture-specific payloads can still live in `eloquence_x86/`, `eloquence_x64/`, `eloquence_arm32/`, or `eloquence_arm64/` if you prefer the legacy staging folders—the build helper now copies both locations so NVDA and CodeQL scans see consistent data. You can also reuse an earlier add-on as a template by dropping it next to the build script as `eloquence_original.nvda-addon` or by passing `--template /path/to/addon.nvda-addon` when building.
4. **Optional – create an isolated Python environment** – `python -m venv .venv` followed by `.venv\Scripts\activate` (PowerShell) or `source .venv/bin/activate` (WSL/Linux/macOS). Install build helpers with `pip install -r tools/requirements-build.txt` if you maintain a custom dependency set; the repository only relies on the Python standard library by default.
5. **Stage cached datasets** – copy refreshed Markdown/JSON artefacts from `docs/` (for example `docs/language_progress.md`, `docs/language_coverage.md`, `docs/voice_language_matrix.md`, and `docs/wikipedia_language_index.md`) into your clone so the build script embeds the latest provenance notes without re-downloading public archives. When you add or modify datasets—including the new Haitian Creole, Jamaican Patois, K'iche', Garifuna, Papiamento, and Miskito research packs—rerun:
   - `python tools/summarize_language_assets.py --json docs/language_asset_summary.json --markdown docs/language_asset_summary.md --print`
   - `python tools/report_language_maturity.py --json docs/language_maturity.json --markdown docs/language_maturity.md --print`
   - `python tools/report_language_progress.py --json docs/language_progress.json --markdown docs/language_progress.md --print`
   - `python tools/report_language_coverage.py --json docs/language_coverage.json --markdown docs/language_coverage.md --print`
   - `python tools/report_voice_language_matrix.py --json docs/voice_language_matrix.json --markdown docs/voice_language_matrix.md --print`
   - `python tools/report_voice_parameters.py --json docs/voice_parameter_report.json --markdown docs/voice_parameter_report.md --print`
   - `python tools/report_voice_frequency_matrix.py --json docs/voice_frequency_matrix.json --markdown docs/voice_frequency_matrix.md --print`
   - `python tools/audit_nvaccess_downloads.py --roots releases/stable releases/2025.3 snapshots/alpha --max-depth 2 --limit-per-dir 12 --insecure --json docs/download_nvaccess_snapshot.json --markdown docs/download_nvaccess_snapshot.md`
   - `python tools/check_nvda_updates.py --snapshot docs/download_nvaccess_snapshot.json --validated docs/validated_nvda_builds.json --manifest manifest.ini --markdown docs/nvda_update_recommendations.md --json docs/nvda_update_recommendations.json`
   - `python tools/report_nvaccess_tree.py --snapshot docs/download_nvaccess_snapshot.json --recommendations docs/nvda_update_recommendations.json --json docs/nvaccess_tree.json --markdown docs/nvaccess_tree.md`
6. **Run the test suite** – `python -m unittest discover tests`. The tests verify voice catalogues, phoneme inventories, documentation parsers, and ensure cached NVDA/Wikipedia/DataJake reports still parse correctly before you package the add-on. Add CodeQL runs when working on archive ingestion or CLI tooling.
7. **Build the add-on** – `python build.py --insecure --no-download --output dist/eloquence.nvda-addon` (for air-gapped or TLS-pinned environments) or simply `python build.py`. The command emits `eloquence.nvda-addon` in the repository root using the binaries you staged in step 3 and the latest documentation snapshots from `docs/`.
8. **Validate the output** – open the generated `.nvda-addon` (it is a ZIP archive) to confirm the `manifest.ini`, voice catalogues, and `assets/` runtime folders (especially `assets/dll/` and `assets/syn/`) are present. Cross-check the `docs/` excerpts packaged inside if you enabled documentation bundling and ensure any legacy `eloquence*/` folders you staged for compatibility also made it into the archive.
9. **Install in NVDA** – on Windows 10 or Windows 11, run NVDA 2019.3 or newer (alpha-52731 or later is our validation baseline), choose **Tools → Add-ons → Install**, and select your freshly built package.
10. **Explore and customise** – visit **Preferences → Speech** to pick Eloquence, adjust the expanded slider set (Emphasis, Stress, Timbre, Tone, Pitch height, Vocal layers, Plosive impact, Overtones, Sibilant clarity, Subtones, Nasal balance, Vocal range, Inflection contour, Roughness, Smoothness, Whisper, Head size contour, Macro volume, Tone size, Scope depth, Sample rate, and Phoneme EQ bands), and inspect the language profile picker for the ISO/script/vocal metrics you just updated.

#### Offline build quickstart (no-release scenario, October 2025 update)

> Need the narrated drill-by-drill version?  Pair this table with the new
> [`docs/offline_build_rehearsal.md`](docs/offline_build_rehearsal.md) checklist
> for a narrated walkthrough that ties every command to cached Wikipedia,
> DataJake, GitHub, and NV Access artefacts plus CodeQL follow-ups.

| Step | Command(s) | Purpose |
| --- | --- | --- |
| 1. Clone | `git clone https://github.com/pumper42nickel/eloquence_threshold.git`<br>`cd eloquence_threshold` | Pull the current `work` branch when no release ZIP exists. |
| 2. Restore caches | `cp -r /path/to/snapshots/docs/* docs/` *(or rerun the reporting helpers listed above)* | Keep Markdown/JSON provenance artefacts in sync so the builder packages language coverage without hitting external mirrors. |
| 3. Stage binaries | Populate `assets/dll/` with the `eci*.dll` runtime files and `assets/syn/` with the corresponding `.syn` voices (optionally mirror them in `eloquence*/` folders for legacy workflows). | Provide architecture-matched runtimes; the builder validates PE headers and fails fast on mismatches. |
| 4. Seed dictionaries | Drop `.dic`/`.lex` assets into `assets/dic/` (or the legacy `eloquence_data/` fallback) and rerun `python tools/catalog_datajake_archives.py --json docs/archive_inventory.json --markdown docs/archive_inventory.md`. | Catalogues imported dictionaries for CodeQL review and packaging. |
| 5. Verify metadata | Run the report suite:<br>`python tools/summarize_language_assets.py --json docs/language_asset_summary.json --markdown docs/language_asset_summary.md --print`<br>`python tools/report_language_maturity.py --json docs/language_maturity.json --markdown docs/language_maturity.md --print`<br>`python tools/report_language_progress.py --json docs/language_progress.json --markdown docs/language_progress.md --print`<br>`python tools/report_language_coverage.py --json docs/language_coverage.json --markdown docs/language_coverage.md --print`<br>`python tools/report_voice_language_matrix.py --json docs/voice_language_matrix.json --markdown docs/voice_language_matrix.md --print`<br>`python tools/report_voice_parameters.py --json docs/voice_parameter_report.json --markdown docs/voice_parameter_report.md --print`<br>`python tools/report_voice_frequency_matrix.py --json docs/voice_frequency_matrix.json --markdown docs/voice_frequency_matrix.md --print`<br>`python tools/report_integration_scope.py --json docs/integration_scope.json --markdown docs/integration_scope.md --print`<br>`python tools/audit_nvaccess_downloads.py --roots releases/stable releases/2025.3 snapshots/alpha --max-depth 2 --limit-per-dir 12 --insecure --json docs/download_nvaccess_snapshot.json --markdown docs/download_nvaccess_snapshot.md`<br>`python tools/check_nvda_updates.py --snapshot docs/download_nvaccess_snapshot.json --validated docs/validated_nvda_builds.json --manifest manifest.ini --markdown docs/nvda_update_recommendations.md --json docs/nvda_update_recommendations.json`<br>`python tools/report_nvaccess_tree.py --snapshot docs/download_nvaccess_snapshot.json --recommendations docs/nvda_update_recommendations.json --json docs/nvaccess_tree.json --markdown docs/nvaccess_tree.md` | Refresh ISO/script dashboards after editing profiles or dictionaries, align NVDA severity guidance, and capture consolidated cross-source snapshots before packaging. |
| 6. Run tests | `python -m unittest discover tests` | Ensure catalogues, phoneme inventories, and documentation parsers still pass integrity checks. |
| 7. Package | `python build.py --insecure --output dist/eloquence.nvda-addon` | Produce the add-on offline, embedding refreshed docs and cached datasets. |
| 8. Install | Use NVDA’s **Tools → Add-ons → Install** dialog and select `dist/eloquence.nvda-addon`. | Deploy the build on Windows 10/11 for validation against NVDA alpha/stable releases. |
| 9. Log run | Document the commands you executed in your pull request, append notable observations to `AGENTS.md`, and cross-reference [`docs/offline_packaging_playbook.md`](docs/offline_packaging_playbook.md). | Keeps the progress log reproducible for future offline packaging drills and ensures the playbook reflects Saharan/Pacific sprint updates. |

#### Example offline rebuild script (bash)

```bash
git clone https://github.com/pumper42nickel/eloquence_threshold.git
cd eloquence_threshold

# Optional: restore cached Markdown/JSON artefacts from a trusted mirror
rsync -a /mnt/offline-snapshots/docs/ docs/

# Stage proprietary binaries (modify the source path for your environment)
rsync -a /mnt/offline-snapshots/eloquence_runtime/ ./

# Refresh provenance dashboards
python tools/summarize_language_assets.py --json docs/language_asset_summary.json --markdown docs/language_asset_summary.md --print
python tools/report_language_maturity.py --json docs/language_maturity.json --markdown docs/language_maturity.md --print
python tools/report_language_progress.py --json docs/language_progress.json --markdown docs/language_progress.md --print
python tools/report_language_coverage.py --json docs/language_coverage.json --markdown docs/language_coverage.md --print
python tools/report_voice_language_matrix.py --json docs/voice_language_matrix.json --markdown docs/voice_language_matrix.md --print
python tools/report_voice_parameters.py --json docs/voice_parameter_report.json --markdown docs/voice_parameter_report.md --print
python tools/report_voice_frequency_matrix.py --json docs/voice_frequency_matrix.json --markdown docs/voice_frequency_matrix.md --print

# Audit NV Access mirrors to confirm compatibility before packaging
python tools/audit_nvaccess_downloads.py --roots releases/stable releases/2025.3 snapshots/alpha --max-depth 2 --limit-per-dir 12 --insecure --json docs/download_nvaccess_snapshot.json --markdown docs/download_nvaccess_snapshot.md
python tools/check_nvda_updates.py --snapshot docs/download_nvaccess_snapshot.json --validated docs/validated_nvda_builds.json --manifest manifest.ini --markdown docs/nvda_update_recommendations.md --json docs/nvda_update_recommendations.json

# Run integrity tests and build the add-on
python -m unittest discover tests
python build.py --insecure --no-download --output dist/eloquence.nvda-addon
```

#### Example offline rebuild script (PowerShell)

```powershell
git clone https://github.com/pumper42nickel/eloquence_threshold.git
Set-Location eloquence_threshold

# Optional: restore cached Markdown/JSON artefacts from a trusted snapshot
robocopy C:\offline\eloquence_docs .\docs /E

# Stage proprietary Eloquence binaries for every architecture slot
robocopy C:\offline\eloquence_runtime .\ eloquence*.* /E

# Refresh provenance dashboards so CodeQL + NVDA audits stay aligned
python tools\summarize_language_assets.py --json docs\language_asset_summary.json --markdown docs\language_asset_summary.md --print
python tools\report_language_maturity.py --json docs\language_maturity.json --markdown docs\language_maturity.md --print
python tools\report_language_progress.py --json docs\language_progress.json --markdown docs\language_progress.md --print
python tools\report_language_coverage.py --json docs\language_coverage.json --markdown docs\language_coverage.md --print
python tools\report_voice_language_matrix.py --json docs\voice_language_matrix.json --markdown docs\voice_language_matrix.md --print
python tools\report_voice_parameters.py --json docs\voice_parameter_report.json --markdown docs\voice_parameter_report.md --print
python tools\report_voice_frequency_matrix.py --json docs\voice_frequency_matrix.json --markdown docs\voice_frequency_matrix.md --print

# Audit NV Access mirrors and regenerate compatibility reports
python tools\audit_nvaccess_downloads.py --roots releases/stable releases/2025.3 snapshots/alpha --max-depth 2 --limit-per-dir 12 --insecure --json docs\download_nvaccess_snapshot.json --markdown docs\download_nvaccess_snapshot.md
python tools\check_nvda_updates.py --snapshot docs\download_nvaccess_snapshot.json --validated docs\validated_nvda_builds.json --manifest manifest.ini --markdown docs\nvda_update_recommendations.md --json docs\nvda_update_recommendations.json
python tools\report_nvaccess_tree.py --snapshot docs\download_nvaccess_snapshot.json --recommendations docs\nvda_update_recommendations.json --json docs\nvaccess_tree.json --markdown docs\nvaccess_tree.md

# Run unit tests and package the add-on without hitting the network
python -m unittest discover tests
python build.py --insecure --no-download --output dist\eloquence.nvda-addon
```

### No-release packaging drill (step-by-step)

> Looking for the full walkthrough?  See [`docs/offline_packaging_playbook.md`](docs/offline_packaging_playbook.md) for the
> October 2025 offline rebuild guide that expands on each step with CodeQL, NV Access snapshot, and DataJake cache workflows.
1. **Clone or update the repository** – on your build machine, run `git clone https://github.com/pumper42nickel/eloquence_threshold.git` (or sync your fork with `git pull`) and then execute `git submodule update --init --recursive` if you mirror optional data helpers.
2. **Rehydrate cached artefacts** – copy the Markdown/JSON reports from `docs/` into place (or regenerate them using the commands listed above) so `build.py` embeds the refreshed provenance ledger without hitting external mirrors.
3. **Verify Eloquence binaries** – confirm that each architecture folder (`eloquence/`, `eloquence_x86/`, `eloquence_x64/`, `eloquence_arm32/`, `eloquence_arm64/`) contains a matching `eci.dll`, `eci20.dll`, or equivalent runtime plus `.syn` voice data. The builder validates PE headers and will refuse to bundle mismatched architectures.
4. **Prime phoneme dictionaries** – ensure any `.dic`/`.lex` files you want packaged live under `eloquence_data/` and are referenced in `docs/archive_inventory.json`. If you add new archives, rerun `python tools/catalog_datajake_archives.py --json docs/archive_inventory.json --markdown docs/archive_inventory.md` to refresh metadata before building.
5. **Rebuild cross-source dashboards** – run the reporting helpers below so coverage, maturity, frequency, linkage, and validation artefacts reflect the sprint before packaging:
   - `python tools/summarize_language_assets.py --json docs/language_asset_summary.json --markdown docs/language_asset_summary.md --print`
   - `python tools/report_language_maturity.py --json docs/language_maturity.json --markdown docs/language_maturity.md --print`
   - `python tools/report_language_progress.py --json docs/language_progress.json --markdown docs/language_progress.md --print`
   - `python tools/report_language_coverage.py --json docs/language_coverage.json --markdown docs/language_coverage.md --print`
   - `python tools/report_voice_language_matrix.py --json docs/voice_language_matrix.json --markdown docs/voice_language_matrix.md --print`
   - `python tools/report_voice_frequency_matrix.py --json docs/voice_frequency_matrix.json --markdown docs/voice_frequency_matrix.md --print`
   - `python tools/report_integration_scope.py --json docs/integration_scope.json --markdown docs/integration_scope.md --print`
   - `python tools/report_voice_parameters.py --json docs/voice_parameter_report.json --markdown docs/voice_parameter_report.md --print`
   - `python tools/report_catalog_status.py --json docs/catalog_status.json --markdown docs/catalog_status.md`
   - `python tools/validate_language_pronunciations.py --json docs/language_pronunciation_validation.json --markdown docs/language_pronunciation_validation.md`
   - `python tools/catalog_wikipedia_languages.py --output-json docs/wikipedia_language_index.json --output-markdown docs/wikipedia_language_index.md` (captures new sign-language classifications before packaging)
6. **Run unit tests** – execute `python -m unittest discover tests` to confirm voice sliders, phoneme inventories, and documentation parsers still pass integrity checks.
7. **Build the add-on** – run `python build.py --insecure --output dist/eloquence.nvda-addon` (add `--template` if you want to reuse a prior package). The script stitches together binaries, documentation, and cached datasets without requiring an internet connection.
8. **Inspect the package** – unzip `dist/eloquence.nvda-addon` and verify that `manifest.ini`, `globalPlugins/eloquenceThreshold/` assets, the `/eloquence*/` runtimes, and any refreshed docs are present.
9. **Install into NVDA** – use NVDA's add-on manager to install the build, then confirm new language profiles or voice parameters appear and announce their coverage metrics.
10. **Document the run** – capture the commands you executed and note any regenerated artefacts in your pull request summary so future contributors can follow the same offline workflow.

### Quick clone-and-build command recap (offline safe)

```powershell
# 1. Grab the repository and optional data helpers
git clone https://github.com/pumper42nickel/eloquence_threshold.git
cd eloquence_threshold
git submodule update --init --recursive

# 2. Restore cached documentation snapshots (copy from your archive or regenerate)
python tools\summarize_language_assets.py --json docs\language_asset_summary.json --markdown docs\language_asset_summary.md --print
python tools\report_language_maturity.py --json docs\language_maturity.json --markdown docs\language_maturity.md --print
python tools\report_language_progress.py --json docs\language_progress.json --markdown docs\language_progress.md --print
python tools\report_language_coverage.py --json docs\language_coverage.json --markdown docs\language_coverage.md --print
python tools\report_voice_language_matrix.py --json docs\voice_language_matrix.json --markdown docs\voice_language_matrix.md --print
python tools\report_voice_frequency_matrix.py --json docs\voice_frequency_matrix.json --markdown docs\voice_frequency_matrix.md --print
python tools\report_integration_scope.py --json docs\integration_scope.json --markdown docs\integration_scope.md --print
python tools\report_voice_parameters.py --json docs\voice_parameter_report.json --markdown docs\voice_parameter_report.md --print
python tools\report_catalog_status.py --json docs\catalog_status.json --markdown docs\catalog_status.md
python tools\validate_language_pronunciations.py --json docs\language_pronunciation_validation.json --markdown docs\language_pronunciation_validation.md

# 3. Validate code + build the NVDA add-on without network access
python -m unittest discover tests
python build.py --insecure --no-download --output dist\eloquence.nvda-addon
```

### Offline ZIP bootstrap (alternative workflow)

If you cannot use `git clone`, download the repository ZIP from a trusted mirror, verify its checksum, and then follow these steps:

1. Extract the archive into `C:\eloquence_threshold` (or another writable path) and ensure Windows SmartScreen is satisfied with the source.
2. Restore cached Markdown/JSON artefacts into `docs/` from your offline vault or regenerate them with the commands listed above. This keeps CodeQL-ready dashboards such as `docs/language_progress.json` and `docs/voice_language_matrix.json` aligned with the sprint.
3. Copy the proprietary Eloquence binaries into the `eloquence*/` architecture slots (`eloquence/`, `eloquence_x86/`, `eloquence_x64/`, `eloquence_arm32/`, `eloquence_arm64/`). The loader validates PE headers and will refuse mismatched DLLs.
4. Open PowerShell, run `py -3 -m venv .venv` (or use an existing Python 3.11+ interpreter), activate it, and install any optional helpers you mirrored (for example, `pip install -r scripts\requirements.txt`).
5. Execute the provenance refresh commands (`python tools\summarize_language_assets.py`, `python tools\report_language_maturity.py`, `python tools\report_language_progress.py`, and companions) so NVDA-linked dashboards, DataJake inventories, and NV Speech Player slider reports reflect your cached datasets.
6. Finish with `python -m unittest discover tests` and `python build.py --insecure --no-download --output dist\eloquence.nvda-addon`. Inspect the resulting add-on to confirm the sprint artefacts—including the Sahelian frequency envelopes and updated ISO roadmap—are embedded before installing into NVDA.

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
- EQ profiles live next to those replacements (`speech/eloquence/phonemeEqProfiles`). Entries only appear once you tweak a band, and you can delete the block to fall back to neutral (flat) playback for every phoneme.
- The **Default phoneme fallback** setting lets you decide whether Eloquence prefers sample words, descriptive text, IPA, or the engine’s raw symbol whenever you have not chosen a custom replacement. Pick the style that makes the most sense for your workflow and the driver will refresh the default mappings across the whole inventory.
- Voice templates can bundle phoneme replacement recommendations. Selecting a heritage preset seeds its preferred fallbacks—without touching any overrides you have already saved—so you immediately hear the nuances that made those classic builds distinct.
- Language profiles now expose their maturity metrics throughout the Speech dialog. As you cycle through the **Language profile** control, NVDA announces the locale’s IPA coverage, stage, documented examples, and whether generative/contextual hints are present. Developers can call `describe_language_progress()` on the driver to log the active profile’s scorecard when instrumenting automated tests.
- A new pair of **Voice parameter** and **Voice parameter value** controls in the Speech dialog lets you cycle through Eloquence's core sliders (gender resonance, rate, pitch, inflection, head size, roughness, breathiness, and volume) and adjust them with a single keyboard-driven workflow. The driver pulls range metadata from the bundled voice catalogue so the slider automatically respects each parameter's safe bounds and preferred step size.
- As you focus the **Voice parameter value** slider, the label now echoes the active parameter name (for example, "Voice parameter value (Pitch – Primary pitch target...)") so NVDA announces which control you are editing in real time. This keeps keyboard-driven workflows oriented as you tab between sliders or switch templates.
- The **Sample rate (Hz)** slider now mirrors the active audio device instead of guessing. On startup (and whenever you adjust the control) Eloquence queries Windows Core Audio for the mix format, clamps it to the engine’s safe range (8 kHz–384 kHz), and automatically resamples buffers so speech always matches the hardware clock. If NVDA runs in an environment where the device cannot be interrogated, the slider falls back to the previous manual behaviour.
- Six dedicated **Phoneme EQ** controls (layer selection, low/high band edges, gain, filter type, and Q) live alongside the phoneme picker. You can stack as many parametric bands as you like per symbol, sculpt their frequency ranges in 10 Hz steps, and boost or cut ±24 dB while the driver automatically manages headroom to avoid clipping. The new filter drop-down lets you flag each layer as a peaking, shelf, pass, notch, or all-pass candidate so future Windows APO integrations can honour those intents, and the Q slider (scaled ×100 to expose two decimal places from the keyboard) tightens or widens the band while keeping the current centre frequency intact.
- Switching audio devices now recalculates every stored EQ band. As soon as the sample rate changes, the phoneme customiser reclamps global and per-phoneme filters so nothing exceeds the new Nyquist limit, keeping profiles safe whether you are on an 8 kHz telephony stack or a 384 kHz studio DAC.
- A new **Advanced NV Speech Player parameters** group brings Eloquence in line with Adam/Benjamin/Caleb/David’s historic controls. Sliders for **Emphasis**, **Stress**, **Timbre**, **Tone**, **Pitch height**, **Vocal layers**, **Plosive impact**, **Overtones**, **Sibilant clarity**, **Subtones**, **Nasal balance**, **Vocal range**, **Inflection contour**, **Roughness**, **Smoothness**, **Whisper blend**, **Head size contour**, **Macro volume**, **Tone size**, and **Scope depth** map NV Speech Player metadata onto Eloquence’s engine. Each slider announces its range (0–200) and updates the global phoneme EQ in real time so brightness, warmth, inflection cues, or whisper content shift immediately across the entire voice.
- Sibilant and plosive shaping are now first-class controls: **Sibilant clarity** brightens or softens S/SH/CH/J phonemes by lifting the 5–14 kHz noise band, while **Plosive impact** sharpens consonant bursts so P/T/K/CH/TS sounds can cut through dense mixes. Combine them with **Pitch height** and **Nasal balance** to tailor accent-friendly timbres where F/S articulations remain crisp even when regional profiles prefer softer vowels.
- Behind the scenes a new `phoneme_customizer.py` manager tracks both per-phoneme EQ bands and the global NV Speech Player style parameters. It keeps the synthesizer’s parametric bands within the 1 Hz–384 kHz window, clamps gain to ±24 dB, and exposes serialisation helpers so NVDA persists your tweaks. The manager merges user layers with voice template defaults, making it trivial to import NV Speech Player, DECtalk, or FonixTalk curves without editing Python.
- Every advanced slider feeds the **Phoneme EQ** pipeline, meaning boosts to overtones or reductions in subtones generate matching EQ bands targeted at the required kHz ranges. Whisper-heavy presets raise the 3–11 kHz band while damping the 300–900 Hz region, smooth voices cut back 4–14 kHz rasp, and tone size biases the first three formants. Because the controls draw on NV Speech Player’s amplitude/formant multipliers, NVDA users get feature parity with classic presets from other synthesizers.
- Every advanced slider feeds the **Phoneme EQ** pipeline, meaning boosts to overtones or reductions in subtones generate matching EQ bands targeted at the required kHz ranges. Whisper-heavy presets raise the 3–11 kHz band while damping the 300–900 Hz region, smooth voices cut back 4–14 kHz rasp, and tone size biases the first three formants. Because the controls draw on NV Speech Player’s amplitude/formant multipliers, NVDA users get feature parity with classic presets from other synthesizers. Contributors can retarget these ranges by editing the `profile["bands"]` metadata in `voice_parameters.py`, which defines the frequency slices and gain multipliers the manager applies.
- If you ever want to refresh the underlying catalogue with a newer upstream snapshot, run `python tools/refresh_espeak_phonemes.py /path/to/espeak-ng` to copy the latest `phsource/phonemes` definition into `eloquence_data/espeak_phonemes.txt` before rebuilding the add-on.

#### Sample rate workflow
- NVDA still remembers the last manual request in `speech/eloquence/sampleRate`, but each time the synth starts we consult the active audio endpoint first. The stored value only comes into play when Windows refuses the query (for example inside sandboxes without WASAPI access).
- Eloquence’s engine remains limited to three native modes (8 kHz, 11.025 kHz, and 22.05 kHz). After learning the device rate we choose the closest engine mode, resample in software, and rebuild NVDA’s `WavePlayer` so buffers stay aligned with the hardware clock.
- The resampler keeps continuity across buffers, meaning long Say All sessions remain smooth even while you experiment with on-the-fly rate changes. Switching outputs or devices simply triggers another device query and player rebuild.
- Ultra-low or ultra-high hardware rates are clamped to the 8 kHz–384 kHz window so Eloquence never feeds a value that the engine or NVDA’s audio stack cannot honour. If clamping occurs we log a debug note and continue with the nearest safe value.

#### Equalizer APO research notes
- The [Equalizer APO project](https://sourceforge.net/projects/equalizerapo/) documents how Windows Audio Processing Objects (APOs) can insert parametric EQ, convolution, and channel routing before audio reaches the hardware mix. Their modules demonstrate how to register custom APOs, inspect device sample rates, and stage filter coefficients using the same Core Audio APIs we now query from `_eloquence.py`.
- Studying their `config` parser and filter topology helps us plan NVDA-centric presets: we can mirror the shelving/peaking blocks Equalizer APO exposes so Eloquence’s phoneme EQ remains familiar to power users while honouring the synthesizer’s ±24 dB guardrails.
- Equalizer APO’s approach to per-device configuration (system effects registry keys and device GUID binding) is informing our roadmap for storing phoneme EQ and sample-rate overrides alongside NVDA profiles. By matching their pattern we can eventually hand off pre-mix, post-mix, or capture-stage tweaks without breaking accessibility requirements.
- Use `python tools/import_eq_apo_config.py path/to/config.txt --output-json docs/eq_apo_import.json --output-markdown docs/eq_apo_import.md --sample-rate 48000` to translate Equalizer APO presets into Eloquence-ready JSON/Markdown snapshots. The helper records device, stage, channel, and loudness metadata while approximating each peaking filter as a phoneme EQ band so NVDA dialogs can surface familiar controls across 1 Hz–384 kHz hardware.

### Build bespoke voices with community templates
- Voice templates derived from eSpeak NG live in `eloquence_data/espeak_voices.json`. Each template maps a language label (for example `en-US` or `es-419`) to Eloquence parameters such as pitch, head size, breathiness, and speaking rate.
- New NV Speech Player inspired presets ship in `eloquence_data/voices/nvspeechplayer_classics.json`. They approximate Adam, Benjamin, Caleb, and David using Eloquence's slider ranges while preserving the original frame multipliers inside the template metadata so you can iterate on the mapping.
- If you want something even more dynamic, drop eSpeak NG variant voice files (for example anything from `espeak-ng-data/voices/!v/`) into `eloquence_data/espeak_variants/`. The loader parses their pitch, speed, voicing, and consonant settings, maps them to Eloquence sliders, and exposes the result as new templates the next time NVDA starts. This automated import workflow was inspired by dynamic synthesizer projects such as [mush42/sonata-nvda](https://github.com/mush42/sonata-nvda) so contributors can experiment without hand-editing JSON.
- DECtalk starter templates are now available in `eloquence_data/dectalk_voices.json`, capturing the personality of classics like Perfect Paul, Beautiful Betty, and Rough Rita. These entries model FonixTalk-era parameter sets so you can approximate DECtalk timbres when running on top of the Eloquence engine.
- Heritage captures from JAWS, Window-Eyes, and Loquence SAPI-4 installs ship in `eloquence_data/voices/eloquence_heritage.json`. These presets toggle abbreviation dictionaries, phrase prediction, and phoneme fallbacks so modern NVDA builds inherit the feel of their legacy counterparts.
- Generative pronunciation layers sit alongside these templates: profiles that rely on contextual AI or rule-based synthesis include `generation` metadata inside their JSON seeds, and NVDA announces when a locale uses dynamic phoneme derivation so testers can audit tone sandhi, vowel harmony, or accent-sensitive alternations directly from the Speech dialog.
- Fresh SAPI-4 and SAPI-5 captures derived from the DataJake archives (`eloq61.exe`, `IBM-ViaVoice_TTS-SAPI4.zip`, and `SAPI5_IBMTTS.zip`) live in `eloquence_data/voices/eloquence_sapi.json`. Each template documents the upstream package inside its `extras.sourceArchive` field so you can cross-reference provenance while tuning.
- Select **Voice template** inside NVDA's Speech dialog to apply these presets. Eloquence will switch to the appropriate `.syn` voice, set its variant, and adjust sliders instantly. You can still tweak the individual sliders afterward; the template simply provides a faster starting point.
- Contributors can add more templates by editing the JSON files. Drop new payloads either alongside the existing `_voices.json` descriptors or inside `eloquence_data/voices/` and the loader will pick them up automatically. The metadata documents the expected ranges for each parameter so community voices stay within Eloquence's safe operating window. New synthesizer families (for example, SAPI-4 ports) can live in additional JSON descriptors alongside DECtalk and eSpeak.

### Share language-aware pronunciation profiles
- Character-level pronunciation hints load from `eloquence_data/languages/*.json`. Each profile records IPA transcriptions, spoken mnemonics, stress patterns, and grammatical notes for a particular locale. We now ship starter sets for English (US/UK), Spanish (Castilian/Latin American), French, German, Italian, Brazilian Portuguese, Hindi, and Japanese so users can explore diverse alphabets immediately. On top of those core profiles the repository now seeds 42 high-demand locales via `eloquence_data/languages/world_language_seeds.json`, spanning Arabic (Modern Standard and Egyptian), Persian, Urdu, Hebrew, Amharic, Hausa, Swahili, Yoruba, Zulu, Mandarin Chinese, Cantonese, Korean, Vietnamese, Thai, Indonesian, Malay, Filipino, Bengali, Tamil, Telugu, Malayalam, Kannada, Marathi, Gujarati, Punjabi, Sinhala, Khmer, Burmese, Lao, Nepali, Russian, Ukrainian, Polish, Czech, Turkish, Greek, Dutch, Swedish, Norwegian Bokmål, Danish, and Finnish. Each entry documents stress guidance, sentence-structure notes, and placeholder phoneme hints so the phoneme customiser has contextual data even before community recordings arrive.
- The seed locales share matching placeholder voice templates in `eloquence_data/voices/eloquence_global_seeds.json`, letting NVDA’s Speech dialog surface a starter preset for every new profile today. Contributors can regenerate or expand the bundle with `python tools/seed_language_profiles.py`, which writes both JSON files from a single curated dataset. The language loader recognises aggregated files exposing a `"profiles"` array, so staging regional batches no longer requires dozens of standalone documents.
- Run `python tools/describe_language_profile.py --list-profiles` to see which profiles are bundled, then pass `--profile english_us_basic "texto"` (or `--language es-ES`) to preview the hints Eloquence will announce for a sample word. Add `--per-character` if you want a table of every matched digraph and the fallback the driver will speak.
- Heritage spelling rules for American English captured from JAWS, Window-Eyes, and Loquence dictionaries live in `eloquence_data/languages/english_us_heritage.json`. When you select a heritage voice template the driver automatically follows this profile so single-character announcements match their legacy pronunciation.
- The **Language profile** driver setting lets you follow the active voice template automatically, force a specific profile, or turn the hints off entirely. When NVDA sends IPA fallback commands, Eloquence can announce both the unmatched symbol and the language-specific hint so you understand what the command attempted to say.
- Segments flagged with language metadata in documents (for example, HTML `lang` attributes) trigger NVDA’s `LangChangeCommand`. When your Speech settings follow the template or match the requested profile, Eloquence now switches to the best language profile automatically so pronunciation hints align with the author’s locale choices.
- To contribute a new language or extend an existing one, drop a JSON file in the `eloquence_data/languages` folder. Profiles may list default templates so NVDA automatically activates them when users pick the matching voice. Multi-character digraphs such as Italian `gli` or Portuguese `nh` are recognised by the driver, so you can document complex sounds without resorting to single-letter approximations.

### Multilingual coverage snapshot
- Linguists estimate that more than 7,000 languages are in active use worldwide, and the number continues to evolve as dialects are documented or revitalised. Our long-term plan is to make Eloquence capable of speaking every script and symbol by piggybacking on community data.
- To keep the roadmap honest we now mirror [Wikipedia’s “Lists of languages” portal](https://en.wikipedia.org/wiki/Lists_of_languages) inside `docs/wikipedia_language_index.{json,md}`. Generate the snapshot with `python tools/catalog_wikipedia_languages.py --output-json docs/wikipedia_language_index.json --output-markdown docs/wikipedia_language_index.md` whenever Wikipedia updates the underlying article. The crawler now records not just the core **language → dialect → accent** tiers but also flags for **sign-language**, **orthography**, **language family**, **constructed language**, **programming/technical language**, **standards/ISO codes**, and **status or statistical dashboards**. NVDA’s speech dialog will consume those tags to expose mutually intelligible phoneme defaults, hook phoneme EQ templates to language families, and surface auxiliary research menus (for example, contact languages, endangered/extinct inventories, and markup or ontology languages that inform pronunciation datasets).
- [eSpeak NG](https://github.com/espeak-ng/espeak-ng) already publishes phoneme inventories and voice rules for over 100 languages and variants, giving us a solid foundation for rapid expansion. As we import these datasets we track the maturity of each locale across phoneme coverage, language profiles, and keyboard-driven voice controls.

### Consolidated language asset dashboard
- Generate `docs/language_asset_summary.{json,md}` with `python tools/summarize_language_assets.py --json docs/language_asset_summary.json --markdown docs/language_asset_summary.md --print`. The summary fuses the language progress, language coverage, voice/language matrix, and research index snapshots so you can confirm Wikipedia/DataJake/GitHub/NVDA provenance lines up before committing updates.
- The Markdown view surfaces per-locale stage, IPA coverage, voice template counts, and coverage status in one table, while the JSON payload powers automation (for example, validating that every ISO seed has both a dictionary provenance trail and an NV Speech Player/Eloquence template pairing).
- Use the aggregated counts to prioritise future imports: coverage gaps indicate where fresh DataJake `.lex` dictionaries or Wikipedia pronunciation tables should be harvested next, and research classification totals show which language families still lack dedicated phoneme EQ experiments.

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
| Hindi | Bundled – eSpeak NG hi phoneme export | Bundled – `hindi_in_basic.json` | Bundled – `espeak-hi-dynamic` template | Full phoneme picker and slider controls | Conversational coverage; rapid review calibration pending | Bharati Braille harmonisation queued with Hear2Read data | Collecting Dakshina/TDIL corpora for schwa deletion and retroflex tuning | Roadmap extends to other Indic scripts via DataJake archives |
| Japanese | Bundled – eSpeak NG ja phoneme export | Bundled – `japanese_basic.json` | Bundled – `espeak-ja-melodic` template | Full phoneme picker and slider controls | Conversational pitch-accent modelling underway | Japanese Braille (JIS) verification planned alongside kana hints | Sourcing NHK pitch-accent lexicon and manga dialogue corpora | Focus on mora timing, rendaku voicing, and okurigana cues |
| Future locales (all other eSpeak NG voices) | Planned – staged imports via `tools/refresh_espeak_phonemes.py` | Planned – contributors invited to seed `eloquence_data/languages/*.json` | Planned – automatic template generation from `.voice` files | Controls automatically available once data lands | Aim for conversational fluency first, then fast review | Require platform braille table verification per locale | Request dictionary/corpus donation when adding profiles | Prioritise high-demand locales (e.g., Arabic, Mandarin, Russian, Korean) |
| Symbols, emoji, technical scripts | Bundled – raw Unicode passthrough; curated IPA fallbacks queued | Planned – per-script pronunciation tables | Planned – synthetic template packs for specialised domains | Phoneme picker already handles custom replacements | Focus on announcing punctuation and emoji skin-tone variants | Braille math/tech tables to follow speech mapping | Collecting Unicode data files and SMuFL symbol corpora | Encourage domain experts to contribute script- or context-specific datasets |

We tag each locale with the most advanced assets we have shipped so far. When you contribute a new language, please:

1. Import or reference the eSpeak NG phoneme block (or another public dataset) inside `eloquence_data/phonemes/`.
2. Create a language profile file under `eloquence_data/languages/` that documents characters, digraphs, stress behaviour, and grammatical notes.
3. Supply at least one voice template—either handcrafted JSON or an auto-converted `.voice` file—so NVDA users can hear the locale immediately.
4. Outline any remaining gaps (for example, “needs tone marks” or “emoji coverage pending”) so we can keep the roadmap transparent.

Short-term expansion priorities include Arabic, Mandarin Chinese, Russian, Korean, and the remaining Indic languages highlighted by Hear2Read. These locales already have mature eSpeak NG voices and large user communities eager for low-latency synthesizers.

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

### Curated voice scenes from DataJake archives
The new **voice scene catalog** bridges our phoneme customiser with the highest-value tooling mirrored on DataJake. Run
`python tools/export_voice_scenes.py --json docs/voice_scene_catalog.json --markdown docs/voice_scene_catalog.md --print`
after adjusting any curated scene to regenerate the Markdown/JSON bundle. Each scene pairs NVDA’s extended sliders with
phoneme EQ templates inspired by eSpeak NG clarity packs, DECtalk/Fonix warmth, or NV Speech Player hybrids so keyboard users
can audition radically different textures without leaving the Speech dialog. The catalog highlights which DataJake archives
(for example, eSpeak NG release zips, DECtalk installers, and NV Speech Player SDK snapshots) inform every preset, making it
easy to trace provenance when porting IPA tables, `.dic` lexicons, or `.syn` voices back into Eloquence.

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
