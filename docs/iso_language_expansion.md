# ISO language expansion roadmap

This living roadmap outlines how Eloquence Threshold is expanding ISO 639 and BCP-47 coverage across Unicode scripts while keeping speech parameters, dictionary inventories, and vocal metrics aligned with NVDA's latest capabilities. It synthesises information from the repository's cached Wikipedia, NVDA, GitHub, and DataJake research snapshots.

## ISO code coverage snapshot

| ISO / tag | Script focus | Status | Notes |
| --- | --- | --- | --- |
| af | Latin (Afrikaans) | Planned | Wikipedia vowel length tables ingested; DataJake `.dic` backlog queued to confirm guttural G handling. |
| am | Ethiopic | Developing | Amharic phoneme deck seeded; awaiting Geez punctuation rules from NVDA alpha manuals before marking comprehensive. |
| bo | Tibetan | Planned | Wikipedia tone contour and stackable consonant charts staged; DataJake archives searched for Wylie transliteration lexicons. |
| ar, ar-EG | Arabic | Seeded | Profiles sourced from `eloquence_data/languages/world_language_seeds.json`; leverages Quranic recitation corpora for emphatic consonants. |
| as | Bengali-Assamese | Planned | Wikipedia-derived consonant inventory staged; awaiting Assamese-specific schwa deletion tests via NVDA nightly builds. |
| az | Latin (Azeri) | Planned | GitHub transliteration utilities catalogued; NVDA docs scanned for glottal stop punctuation cues. |
| bg | Cyrillic (Bulgarian) | Developing | DataJake MBROLA payloads flagged for vowel reduction heuristics; Wikipedia stress matrices under review. |
| bn, bn-IN | Bengali | Comprehensive | Builds on DataJake phoneme stubs and NVDA manual terminology to map inherent vowel suppression rules. |
| ca | Latin (Catalan) | Planned | Language index cross-references DECtalk lexicons for liaison; CodeQL follow-up recorded for 2025-Q4. |
| cs | Latin (Czech) | Established | Awaiting expanded consonant cluster rules from archived DECtalk dictionaries. |
| da | Latin (Danish) | Developing | NVDA documentation snapshot provides stød examples; DataJake lexicons mapped to vowel reduction slider defaults. |
| de-DE | Latin (German) | Developing | GitHub lexicon merges capture final devoicing; DataJake `.lex` payloads queued for rounding rules. |
| el | Greek | Developing | Wikipedia diphthong stress tables incorporated; NVDA manuals inform punctuation and braille alignments. |
| en-GB, en-US | Latin (English) | Comprehensive | Heritage Eloquence templates cross-referenced with GitHub-hosted pronunciation dictionaries. |
| es-ES, es-419 | Latin (Spanish) | Comprehensive | Castilian and Latin American variants mapped to NV Speech Player tone curves. |
| et | Latin (Estonian) | Planned | Partial vowel harmony patterns mirrored from Wikipedia; DataJake archives scanned for palatal consonant cues. |
| fa | Arabic (Persian) | Comprehensive | Integrates Ezafe articulation from Wikipedia grammar references. |
| fil | Latin (Filipino) | Seeded | NVDA manual extracts processed; awaiting morphological corpora from GitHub to tune affix pronunciation. |
| ga-IE | Latin (Irish Gaelic) | Planned | Adds BCP 47 regional tag; lenition/eclipsis roadmaps tie into NV Speech Player consonant hardness sliders. |
| fr | Latin (French) | Developing | DataJake `.dic` payloads assigned to nasal vowel validation; NVDA manual punctuation tables mirrored. |
| ga | Latin (Irish) | Planned | Wikipedia mutation schedules recorded; NVDA docs referenced for braille grade 2 interplay. |
| gl | Latin (Galician) | Planned | Cross-referencing Spanish/Portuguese templates; GitHub accent dictionaries in review for gheada handling. |
| ha | Latin (Hausa) | Developing | Pulling tonal contour data from Wikipedia and DataJake `.lex` archives to align NV Speech Player **Tone** slider defaults. |
| ig | Latin (Igbo) | Planned | Tone ladder and nasal harmony cues catalogued; GitHub finite-state resources queued for vowel alternation. |
| he | Hebrew | Seeded | Masoretic vowel points mirrored from NV Access documentation snapshots; DataJake lexicons flagged for cantillation cues. |
| hi-IN | Devanagari | Established | Retroflex and breathy-voiced contrasts sourced from DataJake MBROLA inventories. |
| hr | Latin (Croatian) | Planned | Wikipedia digraph rules recorded; DECtalk dictionaries referenced for stress alignment. |
| id | Latin (Indonesian) | Comprehensive | Wikipedia phonotactic notes merged with GitHub syllabification scripts; 100% IPA coverage confirmed in `docs/language_coverage.md`. |
| is | Latin (Icelandic) | Planned | NVDA manual punctuation cues archived; GitHub pronunciation datasets queued for vowel length calibration. |
| it | Latin (Italian) | Developing | DataJake lexicons confirm open/closed E and O patterns; Wikipedia entries mapped to NV Speech Player inflection curves. |
| ja | Japanese | Developing | Kana digraph coverage linked to NVDA documentation and open-source kana-to-IPA mappings. |
| ka | Georgian (Mkhedruli) | Planned | Wikipedia ejective consonant inventory stored; NV Speech Player presets targeted for uvular EQ boosts. |
| jv | Latin (Javanese) | Planned | Script variants (Latin/Hanacaraka) catalogued in the Wikipedia index; awaiting dictionary ingestion to resolve vowel length cues. |
| kk | Cyrillic (Kazakh) | Planned | Cyrillic/Latin dual-script corpora tagged; NVDA docset scanned for apostrophe-based digraph hints. |
| km | Khmer | Planned | Unicode dependent vowel tables mirrored; DataJake MBROLA seeds under review for diphthong contours. |
| ko | Hangul | Developing | Syllable block decomposition cross-checked against NV Speech Player recordings and GitHub Hangul-to-IPA resources. |
| lt | Latin (Lithuanian) | Planned | Stress accent reports collated from Wikipedia; DataJake archives triaged for pitch contour metadata. |
| mn | Cyrillic (Mongolian) | Planned | NVDA manuals document vowel harmony; GitHub morphological analysers tagged for contextual suffixes. |
| lv | Latin (Latvian) | Planned | Phoneme coverage flagged for tonal accent validation; NVDA manual quotes stored for macron handling. |
| mai | Devanagari (Maithili) | Planned | ISO 639-3 entry added via Wikipedia crawler; DataJake archives searched for `.lex` payloads before seeding. |
| mr | Devanagari (Marathi) | Planned | DataJake dictionaries surfaced via archive audit; Wikipedia schwa deletion tables queued for validation. |
| mt | Latin (Maltese) | Planned | NVDA manuals highlight Semitic roots; GitHub lexicons queued to validate emphatic consonants. |
| nso | Latin (Northern Sotho) | Planned | Bantu tone tiers mapped; DataJake references under review for alveolar click representations. |
| om | Ethiopic & Latin (Oromo) | Planned | Wikipedia Gadaa dialect splits recorded; NVDA documentation scanned for Latin orthography fallback. |
| or | Odia (Oriya) | Planned | Script-specific ligatures inventoried; DataJake `.lex` search queued for inherent vowel suppression rules. |
| pa, pa-Arab | Gurmukhi & Shahmukhi (Punjabi) | Planned | Dual-script packaging references NVDA manual samples; DataJake `.dic` payloads tagged for tone and retroflex calibration. |
| pl | Latin (Polish) | Developing | Soft consonant palatalisation traces pulled from GitHub; NVDA manuals confirm punctuation spacing. |
| pt-BR | Latin (Portuguese) | Established | NVDA manuals and GitHub lexicons align sibilant and nasal vowel behaviours. |
| ro | Latin (Romanian) | Planned | DECtalk lexicon ancestry catalogued; Wikipedia sources list vowel centralisation heuristics pending validation. |
| ru | Cyrillic (Russian) | Developing | Awaiting vowel reduction matrices from Wikipedia stress tables before graduating to "established". |
| rw | Latin (Kinyarwanda) | Planned | Tone plateau heuristics sourced from Wikipedia; NV Speech Player pitch defaults mapped for nasal prefix handling. |
| sk | Latin (Slovak) | Planned | Stress-on-first-syllable rules confirmed; DataJake `.dic` payloads awaited for rhythmic length tuning. |
| sl | Latin (Slovene) | Planned | Dual accent system tracked via Wikipedia; NV Speech Player tone slider mapping drafted. |
| sr, sr-Latn | Cyrillic & Latin (Serbian) | Planned | Paired alphabets flagged in Wikipedia crawler; DataJake MBROLA voices aligned for digraph/dzh handling. |
| sw | Latin (Swahili) | Comprehensive | Phoneme templates tuned to recorded DataJake archives with 48 kHz stereo metadata. |
| ta | Tamil | Developing | Script-specific vowel markers sourced from the Wikipedia-derived language index; DataJake MBROLA voices confirm retroflex weighting. |
| ti | Ethiopic (Tigrinya) | Planned | Wikipedia consonant gemination notes captured; NV Speech Player contour presets drafted for subject agreement suffixes. |
| th | Thai | Planned | Wikipedia tone contour data collected; NV Speech Player slider mappings drafted to capture mid-level tone neutrality. |
| tr | Latin (Turkish) | Established | GitHub dictionaries confirm vowel harmony; NVDA manuals referenced for dotted capital I edge cases. |
| ug | Arabic (Uyghur) | Planned | Arabic script inventory paired with Latin transliteration; DataJake archives earmarked for vowel harmony plus tone smoothing. |
| uk | Cyrillic (Ukrainian) | Seeded | Stress data mirrored from Wikipedia tables; DataJake archives flagged for palatalisation pairs. |
| vi | Latin (Vietnamese) | Developing | Tone sandhi heuristics pulled from Wikipedia; DataJake lexical tone recordings assigned to frequency matrix planning. |
| wo | Latin (Wolof) | Planned | High/low tone orthography referenced; GitHub language models queued for nasal cluster coverage. |
| yo | Latin (Yoruba) | Comprehensive | Tonal metrics grounded in NVDA's tone slider plus Yoruba orthography references. |
| zh-Hans | Han (Simplified Chinese) | Developing | NVDA dictionary extracts and GitHub Pinyin to IPA datasets align; DataJake tone recordings queued for 4-tone verification. |
| zh-Hant | Han (Traditional Chinese) | Planned | Wikipedia-based bopomofo mapping added; awaiting DataJake lexicons for Hakka/Min overlays. |
| yue | Han (Traditional, Cantonese) | Planned | Jyutping corpora catalogued; NV Speech Player tone slider clones targeted at six-tone sets. |

Additional locales tracked in [`docs/language_progress.md`](language_progress.md) are being folded into this table as we verify ISO tags, scripts, and dictionary metadata. Refer to the regenerated `docs/language_coverage.md` and `docs/voice_language_matrix.md` snapshots for the full 53-profile catalogue refreshed alongside this update.

## Script and orthography priorities

1. **Ethiopic & Geez-derived scripts** – integrate Amharic, Tigrinya, and Oromo phoneme lists using the Ethiopic Extended block; align with NV Speech Player nasal resonance sliders.
2. **Canadian Aboriginal syllabics** – ingest Cree and Inuktitut corpora, leveraging GitHub lexicon projects for contextual vowel length cues.
3. **Indic minority scripts** – extend Ol Chiki (Santali), Meitei Mayek (Manipuri), and Sylheti Nagari coverage using DataJake `.lex` datasets.
4. **Vai and N'Ko** – partner with NVDA community research to map tonal diacritics and vowel harmony onto Eloquence's inflection controls.
5. **Constructed scripts** – maintain placeholders for Tengwar, Shavian, and Braille shorthands using the Wikipedia-derived catalogue so experimentation can start without editing core code.
6. **Historic orthographies** – queue Fraktur (de-DE-1901), Ottoman Turkish (ar-Latn-x-ottoman), and Old Church Slavonic (cu) from the Wikipedia index so phoneme converters can surface diachronic voice packs.
7. **Extended Latin digraph sets** – polish entries for Hausa, Yoruba, and Vietnamese by aligning tone diacritics with NV Speech Player contour sliders and CodeQL metadata hooks.

## Speech parameter and frequency combinations

- **NV Speech Player parity** – the voice slider catalogue in `voice_parameters.py` now mirrors NV Speech Player metadata (Emphasis, Stress, Timbre, Tone, Pitch height, Vocal layers, Plosive impact, Overtones, Sibilant clarity, Subtones, Nasal balance, Vocal range, Inflection contour, Roughness, Smoothness, Whisper, Head size contour, Macro volume, Tone size, Scope depth). Each slider references the `profile["bands"]` hints so per-phoneme EQ stays aligned with target frequency ranges.
- **Frequency scaffolding** – upcoming work will import DataJake EQ captures to generate reference curves for 8 kHz, 22.05 kHz, 44.1 kHz, 48 kHz, 96 kHz, and 192 kHz playback. These will be expressed as stacked parametric bands, ensuring the phoneme customiser clamps bands to the current WASAPI sample rate.
- **Sample-rate provenance ledger** – cached NVDA manual audio metadata and DataJake `audio_signature` notes are now logged per locale so contributors can align EQ presets with historically recorded sample rates before pushing new seeds.
- **Harmonic + noise band pairing** – queued research maps Wikipedia-formant data and DataJake spectral captures into paired harmonic/noise filters so vowel formants (F1–F4) and consonant fricatives receive independent gain automation.
- **Vocal metrics** – NVDA's Speech dialog now announces coverage ratios, IPA completeness, stress notes, and contextual cues from `language_profiles.py` so testers can gauge maturity while switching ISO profiles.
- **Temporal dynamics** – GitHub-hosted articulatory datasets (for example, TIMIT derivatives) will seed consonant release/closure duration tables, giving the timing engine more granular defaults when switching between ISO profiles.
- **Cross-archive calibration** – NV Speech Player, DataJake MBROLA recordings, and NVDA manual formant charts are now cross-referenced so tone, timbre, and plosive sliders align even when a locale pulls assets from multiple archives.
- **Regional preset overlays** – Yoruba, Hausa, Igbo, and Wolof tone plans map NV Speech Player sliders to DataJake crest frequency captures, while Irish Gaelic and Scottish Gaelic voice presets will inherit consonant hardness curves from archived DECtalk corpora.

### Generative and contextual pronunciation layers

- **Seed + generative hybrids** – language profiles mark whether their phoneme inventories rely solely on curated dictionaries, scripted rule engines, or AI-assisted generators. The YAML/JSON seeds in `eloquence_data/languages/` now expose a `generation` block that describes how contextual variants (for example, tone sandhi or vowel harmony) are produced before NVDA renders speech.
- **Contextual overrides** – contributors can extend `phoneme_customizer.py` to flag dictionary entries that require environment-sensitive replacements (such as Yorùbá nasalisation before plosives). These overrides feed the same per-phoneme EQ clamps so resulting bands stay within the validated ±24 dB, 1 Hz–384 kHz envelope.
- **Predictive phoneme fallbacks** – CodeQL-backed checks will watch for dictionary entries missing fallback tokens and request generation via Wikipedia/Corpus heuristics before the add-on ships an incomplete locale.
- **Dictionary provenance** – every imported `.dic`/`.lex` file records its source archive (DataJake URL, GitHub repository, or NVDA manual bundle) and the commit or snapshot date in `docs/archive_inventory.json`. This metadata flows into README coverage tables and supports CodeQL policy enforcement for untrusted payloads.
- **Morphology-aware synthesis** – planned generators incorporate GitHub-derived finite-state transducers for agglutinative languages (Turkish, Finnish, Hungarian) so Eloquence can synthesise unseen forms while preserving pitch accent metadata.
- **NVDA manual alignment** – packaging guidance now references the latest audited NVDA manual snapshots (`docs/nvda_update_recommendations.md` and `docs/nvaccess_tree.md`) so punctuation, braille, and speech examples packaged with new locales match the validated builds.

## Dictionary and phoneme datasets in flight

- **DataJake archive triage** – consult [`docs/archive_inventory.md`](archive_inventory.md) and [`docs/archive_code_targets.md`](archive_code_targets.md) for `.lex`, `.dic`, and MBROLA bundles staged for import. Priority targets include Eloquence, DECtalk 5.1, FonixTalk, IBM ViaVoice lexicons, and RHVoice voice banks for tone-rich languages.
- **Wikipedia-derived corpora** – `docs/wikipedia_language_index.md` flags Wikipedia entries tagged as language, dialect, sign-language, orthography, or status dashboards. These references guide contextual pronunciation notes and grammar hints imported into the seed profiles.
- **GitHub integrations** – open-source pronunciation datasets (for example `espeak-ng` phoneme tables or NV Speech Player JSON exports) are mirrored in `eloquence_data/` so the add-on loads them offline.
- **NVDA upstream tooling** – `docs/nvda_update_recommendations.md` and `docs/nvaccess_tree.md` help us align dictionary updates with NVDA releases, ensuring packaged manuals and lexicons match the supported builds.
- **NV Access cache discipline** – always favour the audited snapshots captured via `python tools/audit_nvaccess_downloads.py` and `python tools/compare_nvaccess_snapshots.py` before pulling fresh archives. Reusing cached data keeps our release engineering reproducible and avoids hammering NV Access mirrors during large-scale ISO imports.
- **Cross-project provenance ledger** – `docs/language_research_index.md` now lists which NVDA manuals, GitHub repositories, and Wikipedia references fed each ISO code so compliance reviews can confirm licensing compatibility before shipping.
- **Dictionary validation harness** – expand `tests/test_archive_catalog.py` with checks for duplicate lexeme IDs, conflicting phoneme tags, and missing metadata before accepting new archives into `eloquence_data/`.
- **Pronunciation sandbox** – `docs/language_research_index.md` and `docs/iso_language_expansion.md` jointly track experimental locales (for example, constructed languages or community-contributed orthographies) so contributions follow a reproducible research trail.
- **Release rehearsal ledger** – README’s no-release drill, AGENTS progress log, and cached `docs/` artefacts now document every packaging rehearsal so the community can replay successful offline builds while staging new ISO coverage.

## Cross-source utilisation dashboard

| Data source | Cached artefact | How the roadmap uses it |
| --- | --- | --- |
| Wikipedia | `docs/wikipedia_language_index.md` | Supplies ISO/script metadata, tone diagrams, and orthography notes for new locale seeds. |
| DataJake archives | `docs/archive_inventory.json` / `.md` | Flags `.dic`/`.lex` payloads, MBROLA voices, and frequency captures that fill phoneme gaps and EQ calibration tables. |
| GitHub | `docs/language_research_index.json` | Records pronunciation datasets, finite-state morphology tools, and NV Speech Player exports that extend contextual generators. |
| NV Access | `docs/nvda_update_recommendations.json` / `.md` | Ensures packaging targets the validated NVDA alpha/stable releases and aligns dictionary updates with manual revisions. |
| Voice metrics | `docs/voice_parameter_report.md` | Tracks slider ranges, EQ bands, and tone mappings so ISO additions reuse harmonised presets. |

## Next steps

- Refresh `tools/report_language_progress.py` outputs after each ISO/script addition so regression tracking stays accurate.
- Extend `tools/catalog_wikipedia_languages.py` to highlight missing ISO 639-3 codes and macrolanguage mappings for languages that only have partial coverage today.
- Add automated validation for dictionary imports (tests under `tests/test_archive_catalog.py`) to ensure `.dic` and `.lex` payloads surface consistent metadata before packaging.
- Continue collecting vocal metric samples (pitch range, harmonic balance, sibilance thresholds) from NV Speech Player and DECtalk recordings to inform future template tuning.
- Align upcoming CodeQL queries with the expanded dictionary ingestion workflow so any malformed phoneme metadata or unsafe archive extraction routines are flagged during CI before packaging.
- Publish quarterly progress digests in `docs/language_research_index.md` summarising new ISO additions, scripts, and datasets so README scorecards can cite an authoritative changelog.
- Build conversion helpers that map NVDA manual punctuation notes into per-language symbol tables, unlocking faster seeding for over 120 ISO codes captured in the Wikipedia index.

Contributors can reference this roadmap when proposing pull requests so reviews focus on data provenance, ISO/script accuracy, and how the change improves Eloquence for blind and low-vision NVDA users.
