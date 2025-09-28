# ISO language expansion roadmap

This living roadmap outlines how Eloquence Threshold is expanding ISO 639 and BCP-47 coverage across Unicode scripts while keeping speech parameters, dictionary inventories, and vocal metrics aligned with NVDA's latest capabilities. It synthesises information from the repository's cached Wikipedia, NVDA, GitHub, and DataJake research snapshots.

## ISO code coverage snapshot

| ISO / tag | Script focus | Status | Notes |
| --- | --- | --- | --- |
| am | Ethiopic | Developing | Amharic phoneme deck seeded; awaiting Geez punctuation rules from NVDA alpha manuals before marking comprehensive. |
| ar, ar-EG | Arabic | Seeded | Profiles sourced from `eloquence_data/languages/world_language_seeds.json`; leverages Quranic recitation corpora for emphatic consonants. |
| bn, bn-IN | Bengali | Comprehensive | Builds on DataJake phoneme stubs and NVDA manual terminology to map inherent vowel suppression rules. |
| cs | Latin (Czech) | Established | Awaiting expanded consonant cluster rules from archived DECtalk dictionaries. |
| en-GB, en-US | Latin (English) | Comprehensive | Heritage Eloquence templates cross-referenced with GitHub-hosted pronunciation dictionaries. |
| es-ES, es-419 | Latin (Spanish) | Comprehensive | Castilian and Latin American variants mapped to NV Speech Player tone curves. |
| fa | Arabic (Persian) | Comprehensive | Integrates Ezafe articulation from Wikipedia grammar references. |
| ha | Latin (Hausa) | Developing | Pulling tonal contour data from Wikipedia and DataJake `.lex` archives to align NV Speech Player **Tone** slider defaults. |
| hi-IN | Devanagari | Established | Retroflex and breathy-voiced contrasts sourced from DataJake MBROLA inventories. |
| ja | Japanese | Developing | Kana digraph coverage linked to NVDA documentation and open-source kana-to-IPA mappings. |
| ko | Hangul | Developing | Syllable block decomposition cross-checked against NV Speech Player recordings and GitHub Hangul-to-IPA resources. |
| pt-BR | Latin (Portuguese) | Established | NVDA manuals and GitHub lexicons align sibilant and nasal vowel behaviours. |
| ru | Cyrillic (Russian) | Developing | Awaiting vowel reduction matrices from Wikipedia stress tables before graduating to "established". |
| sw | Latin (Swahili) | Comprehensive | Phoneme templates tuned to recorded DataJake archives with 48 kHz stereo metadata. |
| ta | Tamil | Developing | Script-specific vowel markers sourced from the Wikipedia-derived language index; DataJake MBROLA voices confirm retroflex weighting. |
| yo | Latin (Yoruba) | Comprehensive | Tonal metrics grounded in NVDA's tone slider plus Yoruba orthography references. |

Additional locales tracked in [`docs/language_progress.md`](language_progress.md) are being folded into this table as we verify ISO tags, scripts, and dictionary metadata. Refer to the regenerated `docs/language_coverage.md` and `docs/voice_language_matrix.md` snapshots for the full 53-profile catalogue refreshed alongside this update.

## Script and orthography priorities

1. **Ethiopic & Geez-derived scripts** – integrate Amharic, Tigrinya, and Oromo phoneme lists using the Ethiopic Extended block; align with NV Speech Player nasal resonance sliders.
2. **Canadian Aboriginal syllabics** – ingest Cree and Inuktitut corpora, leveraging GitHub lexicon projects for contextual vowel length cues.
3. **Indic minority scripts** – extend Ol Chiki (Santali), Meitei Mayek (Manipuri), and Sylheti Nagari coverage using DataJake `.lex` datasets.
4. **Vai and N'Ko** – partner with NVDA community research to map tonal diacritics and vowel harmony onto Eloquence's inflection controls.
5. **Constructed scripts** – maintain placeholders for Tengwar, Shavian, and Braille shorthands using the Wikipedia-derived catalogue so experimentation can start without editing core code.

## Speech parameter and frequency combinations

- **NV Speech Player parity** – the voice slider catalogue in `voice_parameters.py` now mirrors NV Speech Player metadata (Emphasis, Stress, Timbre, Tone, Pitch height, Vocal layers, Plosive impact, Overtones, Sibilant clarity, Subtones, Nasal balance, Vocal range, Inflection contour, Roughness, Smoothness, Whisper, Head size contour, Macro volume, Tone size, Scope depth). Each slider references the `profile["bands"]` hints so per-phoneme EQ stays aligned with target frequency ranges.
- **Frequency scaffolding** – upcoming work will import DataJake EQ captures to generate reference curves for 8 kHz, 22.05 kHz, 44.1 kHz, 48 kHz, 96 kHz, and 192 kHz playback. These will be expressed as stacked parametric bands, ensuring the phoneme customiser clamps bands to the current WASAPI sample rate.
- **Vocal metrics** – NVDA's Speech dialog now announces coverage ratios, IPA completeness, stress notes, and contextual cues from `language_profiles.py` so testers can gauge maturity while switching ISO profiles.

### Generative and contextual pronunciation layers

- **Seed + generative hybrids** – language profiles mark whether their phoneme inventories rely solely on curated dictionaries, scripted rule engines, or AI-assisted generators. The YAML/JSON seeds in `eloquence_data/languages/` now expose a `generation` block that describes how contextual variants (for example, tone sandhi or vowel harmony) are produced before NVDA renders speech.
- **Contextual overrides** – contributors can extend `phoneme_customizer.py` to flag dictionary entries that require environment-sensitive replacements (such as Yorùbá nasalisation before plosives). These overrides feed the same per-phoneme EQ clamps so resulting bands stay within the validated ±24 dB, 1 Hz–384 kHz envelope.
- **Dictionary provenance** – every imported `.dic`/`.lex` file records its source archive (DataJake URL, GitHub repository, or NVDA manual bundle) and the commit or snapshot date in `docs/archive_inventory.json`. This metadata flows into README coverage tables and supports CodeQL policy enforcement for untrusted payloads.

## Dictionary and phoneme datasets in flight

- **DataJake archive triage** – consult [`docs/archive_inventory.md`](archive_inventory.md) and [`docs/archive_code_targets.md`](archive_code_targets.md) for `.lex`, `.dic`, and MBROLA bundles staged for import. Priority targets include Eloquence, DECtalk 5.1, FonixTalk, and IBM ViaVoice lexicons.
- **Wikipedia-derived corpora** – `docs/wikipedia_language_index.md` flags Wikipedia entries tagged as language, dialect, sign-language, orthography, or status dashboards. These references guide contextual pronunciation notes and grammar hints imported into the seed profiles.
- **GitHub integrations** – open-source pronunciation datasets (for example `espeak-ng` phoneme tables or NV Speech Player JSON exports) are mirrored in `eloquence_data/` so the add-on loads them offline.
- **NVDA upstream tooling** – `docs/nvda_update_recommendations.md` and `docs/nvaccess_tree.md` help us align dictionary updates with NVDA releases, ensuring packaged manuals and lexicons match the supported builds.
- **NV Access cache discipline** – always favour the audited snapshots captured via `python tools/audit_nvaccess_downloads.py` and `python tools/compare_nvaccess_snapshots.py` before pulling fresh archives. Reusing cached data keeps our release engineering reproducible and avoids hammering NV Access mirrors during large-scale ISO imports.

## Next steps

- Refresh `tools/report_language_progress.py` outputs after each ISO/script addition so regression tracking stays accurate.
- Extend `tools/catalog_wikipedia_languages.py` to highlight missing ISO 639-3 codes and macrolanguage mappings for languages that only have partial coverage today.
- Add automated validation for dictionary imports (tests under `tests/test_archive_catalog.py`) to ensure `.dic` and `.lex` payloads surface consistent metadata before packaging.
- Continue collecting vocal metric samples (pitch range, harmonic balance, sibilance thresholds) from NV Speech Player and DECtalk recordings to inform future template tuning.
- Align upcoming CodeQL queries with the expanded dictionary ingestion workflow so any malformed phoneme metadata or unsafe archive extraction routines are flagged during CI before packaging.

Contributors can reference this roadmap when proposing pull requests so reviews focus on data provenance, ISO/script accuracy, and how the change improves Eloquence for blind and low-vision NVDA users.
