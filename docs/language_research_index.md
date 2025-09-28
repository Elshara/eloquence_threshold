# Wikipedia-driven language research backlog

This catalogue captures the Wikipedia pages the community highlighted as
critical for expanding Eloquence's multilingual coverage.  It complements the
machine-harvested `docs/wikipedia_language_index.*` snapshots by layering
priority, ingestion progress, and the language/dialect/accent/family/status
distinctions that feed NVDA's voice selector, research sidebars, and phoneme
customiser.

The table below groups each source by research focus.  Use it when planning
phoneme data imports, NV Speech Player slider mappings, or documentation updates.
For JSON automation, see [`docs/language_research_index.json`](language_research_index.json).

## How to use this catalogue

1. **Refresh the baseline index**: run
   `python tools/catalog_wikipedia_languages.py --output-json docs/wikipedia_language_index.json --output-markdown docs/wikipedia_language_index.md`
   before adding new rows so the canonical language/dialect/accent structure is
   current.
2. **Record ingestion status**: when you convert a source into structured data
   (JSON, CSV, phoneme presets, or NVDA templates), update the *Progress*
   column.  When datasets flow into Eloquence seed bundles, rerun the reporting
   helpers listed in the repository root `AGENTS.md`.
3. **Map parameters**: note which NV Speech Player parameters, EQ bands, or
   phoneme sliders the source informs.  Accent and dialect links usually drive
   band emphasis (clarity vs. smoothness, hard vs. soft consonants), while
   script pages map to sample-rate-aware phoneme curves and orthography
   metadata.
4. **Document NVDA hooks**: whenever a source improves the Speech dialog or
   Configuration Manager exports, capture the workflow in `README.md` and the
   relevant `AGENTS` guidance so blind contributors can reproduce the setup.

## ISO and registry foundations

| Usefulness | Source | Classification | Progress | Notes |
| --- | --- | --- | --- | --- |
| Critical | [Lists of languages](https://en.wikipedia.org/wiki/Lists_of_languages) | language / dialect / accent | Indexed via tool | Primary crawler input for the cached Wikipedia index and NVDA tiered selector. |
| Critical | [List of ISO 639 language codes](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) | language / metadata | Pending structured ingestion | Anchors NVDA exports to authoritative code pairs; informs phoneme profile IDs. |
| High | [List of ISO 639-2 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes) | language / metadata | Pending structured ingestion | Differentiates bibliographic vs. terminologic bundles for packaging. |
| High | [ISO 639 macrolanguage](https://en.wikipedia.org/wiki/ISO_639_macrolanguage) | language / dialect | Pending structured ingestion | Guides dialect roll-ups inside the Speech dialog. |
| Critical | [List of ISO 639-3 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-3_codes) | language / dialect | Pending structured ingestion | Supplies scope/type flags for language profile seeding. |
| High | [ISO 639-5](https://en.wikipedia.org/wiki/ISO_639-5) | family / language | Pending structured ingestion | Establishes family-level selectors and mutual intelligibility groupings. |
| Medium | [ISO 639-6](https://en.wikipedia.org/wiki/ISO_639-6) | dialect | Pending structured ingestion | Adds historic dialect identifiers for accent presets. |
| Medium | [List of ISO 639-6 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-6_codes) | dialect | Pending structured ingestion | Archived data for granular accent selection. |
| Critical | [ISO 15924](https://en.wikipedia.org/wiki/ISO_15924) | orthography | Pending structured ingestion | Maps scripts to four-letter codes for script-aware phoneme bundles. |
| High | [List of scripts with no ISO 15924 code](https://en.wikipedia.org/wiki/List_of_scripts_with_no_ISO_15924_code) | orthography | Pending structured ingestion | Highlights gaps that require provisional script identifiers. |
| High | [ISO 15924 codes](https://en.wikipedia.org/wiki/ISO_15924#List_of_codes) | orthography | Pending structured ingestion | Numeric/alphabetic script codes feeding EQ defaults. |
| Medium | [ConScript Unicode Registry](https://en.wikipedia.org/wiki/ConScript_Unicode_Registry#Under-ConScript_Unicode_Registry) | constructed / orthography | Pending structured ingestion | Private-use scripts for fallback phoneme mapping. |
| Medium | [Medieval Unicode Font Initiative](https://en.wikipedia.org/wiki/Medieval_Unicode_Font_Initiative) | orthography / historical | Pending structured ingestion | Scribal variants for medieval phoneme shaping. |
| Critical | [IETF language tag](https://en.wikipedia.org/wiki/IETF_language_tag) | language / metadata / dialect | Pending structured ingestion | Required for BCP 47-compatible NVDA exports and variant tagging. |
| High | [Codes for constructed languages](https://en.wikipedia.org/wiki/Codes_for_constructed_languages) | constructed / language | Pending structured ingestion | Gives Esperanto/auxlang identifiers for accessible packaging. |

## Language family relationships and research indices

| Usefulness | Source | Classification | Progress | Relationship focus |
| --- | --- | --- | --- | --- |
| Critical | [Language family](https://en.wikipedia.org/wiki/Language_family) | family / language | Requires taxonomy summary | Foundation for describing genealogy and mutual intelligibility. |
| High | [List of language families](https://en.wikipedia.org/wiki/List_of_language_families) | family / language | Pending structured ingestion | Enumerates families for NVDA documentation. |
| Medium | [List of proposed language families](https://en.wikipedia.org/wiki/List_of_proposed_language_families) | family / research | Pending structured ingestion | Tracks speculative groupings for future research. |
| Medium | [Extinct language](https://en.wikipedia.org/wiki/Extinct_language) | historical / language | Requires summary integration | Captures methodology for archiving pronunciation evidence. |
| Medium | [Lists of extinct languages](https://en.wikipedia.org/wiki/Lists_of_extinct_languages) | historical / language | Pending structured ingestion | Source for archival phoneme presets. |
| Medium | [List of languages by time of extinction](https://en.wikipedia.org/wiki/List_of_languages_by_time_of_extinction) | historical / language | Pending structured ingestion | Timeline for revitalisation and archival packs. |
| Medium | [Lists of endangered languages](https://en.wikipedia.org/wiki/Lists_of_endangered_languages) | language / revitalisation | Pending structured ingestion | Highlights urgent preservation targets. |
| Medium | [List of revived languages](https://en.wikipedia.org/wiki/List_of_revived_languages) | language / revitalisation | Pending structured ingestion | Documents community-led revival datasets. |
| High | [Language isolate list](https://en.wikipedia.org/wiki/Language_isolate#List_of_language_isolates_by_continent) | language / isolates | Pending structured ingestion | Ensures isolates receive bespoke templates. |
| Medium | [Unclassified language](https://en.wikipedia.org/wiki/Unclassified_language) | language / research | Requires summary integration | Context for placeholder metadata. |
| Medium | [Ethnologue unclassified languages](https://en.wikipedia.org/wiki/List_of_unclassified_languages_according_to_the_Ethnologue) | language / research | Pending structured ingestion | Supplements Wikipedia gaps. |
| High | [Index of language articles](https://en.wikipedia.org/wiki/Index_of_language_articles) | language / research | Pending structured ingestion | High-level roadmap for niche topics. |
| Medium | [Flag icons for languages](https://en.wikipedia.org/wiki/Flag_icons_for_languages) | metadata | Pending structured ingestion | Accessibility-focused iconography guidance. |

## Family-specific coverage priorities

This set drives the next stage of phoneme seeding and NV Speech Player slider
calibration.  Use family links to model mutual intelligibility and to generate
regional presets (hard/soft consonants, tonal contours, vowel harmony).

| Usefulness | Family focus | Notes |
| --- | --- | --- |
| High | [Afroasiatic languages](https://en.wikipedia.org/wiki/Afroasiatic_languages) | Covers Semitic, Berber, Cushitic, Omotic, Chadic phonology; informs consonant emphatics and guttural EQ boosts. |
| High | [List of Austronesian languages](https://en.wikipedia.org/wiki/List_of_Austronesian_languages) | Drives Pacific/Oceania planning with nasalisation cues. |
| Critical | [List of Indo-European languages](https://en.wikipedia.org/wiki/List_of_Indo-European_languages) | Aligns with existing NV Speech Player templates; map branches to accent sliders. |
| Medium | [List of Mayan languages](https://en.wikipedia.org/wiki/List_of_Mayan_languages) | Provides ejective/glottalised consonant inventories for clarity controls. |
| Medium | [List of Mongolic languages](https://en.wikipedia.org/wiki/List_of_Mongolic_languages) | Vowel harmony defaults for Mongolic presets. |
| Medium | [List of Oto-Manguean languages](https://en.wikipedia.org/wiki/List_of_Oto-Manguean_languages) | Tonal contour data for EQ inflection sliders. |
| Medium | [Tungusic languages classification](https://en.wikipedia.org/wiki/Tungusic_languages#Classification) | Guides Siberian dialect presets. |
| High | [List of Turkic languages](https://en.wikipedia.org/wiki/List_of_Turkic_languages) | Palatal harmony and vowel frontness parameters. |
| High | [List of Uralic languages](https://en.wikipedia.org/wiki/List_of_Uralic_languages) | Agglutinative stress patterns for NVDA pitch/inflection sliders. |
| Medium | [List of lesser-known Loloish languages](https://en.wikipedia.org/wiki/List_of_lesser-known_Loloish_languages) | Spotlights endangered Sino-Tibetan branches for urgent phoneme capture. |
| Medium | [Hani languages](https://en.wikipedia.org/wiki/Hani_languages) | Dialect cluster details for Loloish coverage. |
| Medium | [Taloid languages](https://en.wikipedia.org/wiki/Taloid_languages) | Comparative tables to adjust high-frequency consonant EQ. |
| Medium | [Talodi–Heiban languages](https://en.wikipedia.org/wiki/Talodi%E2%80%93Heiban_languages) | Supports Niger–Congo expansion. |
| High | [Yupik languages](https://en.wikipedia.org/wiki/Yupik_languages) | Polysynthetic phoneme inventories for Alaska/Siberia packages. |

## Regional language dashboards

| Usefulness | Region | Notes |
| --- | --- | --- |
| High | [Languages of Africa](https://en.wikipedia.org/wiki/Languages_of_Africa) | Macro view for African bundles; align with 42-seed roadmap (Amharic, Hausa, Swahili, Yoruba, Zulu, etc.). |
| High | [Indigenous languages of the Americas](https://en.wikipedia.org/wiki/Indigenous_languages_of_the_Americas) | Framework for North/South America indigenous coverage. |
| Medium | [Native American languages acquired by children](https://en.wikipedia.org/wiki/List_of_Native_American_languages_acquired_by_children) | Tracks intergenerational transmission for prioritising phoneme capture. |
| Medium | [Languages of North America](https://en.wikipedia.org/wiki/Languages_of_North_America) | Regional overview for NVDA packaging guidance. |
| Medium | [Languages of South America](https://en.wikipedia.org/wiki/Languages_of_South_America) | Highlights Andean/Amazonian diversity. |
| Medium | [Languages of Asia](https://en.wikipedia.org/wiki/Languages_of_Asia) | Continental taxonomy for Asia-focused packs. |
| Medium | [East Asian languages](https://en.wikipedia.org/wiki/East_Asian_languages) | Sino-Tibetan, Japonic, Koreanic accent considerations. |
| Medium | [Languages of South Asia](https://en.wikipedia.org/wiki/Languages_of_South_Asia) | Indo-Aryan/Dravidian interplay for inflection sliders. |
| Medium | [Classification of Southeast Asian languages](https://en.wikipedia.org/wiki/Classification_of_Southeast_Asian_languages) | Mainland vs. Maritime typology for tonal modelling. |
| Medium | [Languages of Europe](https://en.wikipedia.org/wiki/Languages_of_Europe) | Aligns NVDA European packaging with official EU language policies. |
| Medium | [Languages of Russia](https://en.wikipedia.org/wiki/Languages_of_Russia) | Highlights Russia's multilingual landscape for script coverage. |
| Medium | [Languages of Oceania](https://en.wikipedia.org/wiki/Languages_of_Oceania) | Combines Austronesian and Papuan planning for Pacific seeds. |

## Language-specific expansion dossiers (Q4 2025 refresh)

| Usefulness | Source | Classification | Progress | Notes |
| --- | --- | --- | --- | --- |
| High | [Tigrinya language](https://en.wikipedia.org/wiki/Tigrinya_language) | language | Pending structured ingestion | Supplies gemination rules and tone plateaus for ISO `ti` roadmap entries. |
| High | [Oromo language](https://en.wikipedia.org/wiki/Oromo_language) | language | Pending structured ingestion | Captures Latin/Ethiopic orthography mapping and Gadaa dialect notes for Oromo packaging. |
| High | [Odia language](https://en.wikipedia.org/wiki/Odia_language) | language | Requires phoneme summary | Provides consonant ligatures and inherent vowel suppression cues. |
| Medium | [Punjabi language](https://en.wikipedia.org/wiki/Punjabi_language) | language | Pending structured ingestion | Differentiates Gurmukhi vs. Shahmukhi scripts for ISO `pa` coverage. |
| Medium | [Tibetan language](https://en.wikipedia.org/wiki/Tibetan_language) | language | Pending structured ingestion | Supplies stacked consonant tables and tonal contour references for ISO `bo`. |
| Medium | [Uyghur language](https://en.wikipedia.org/wiki/Uyghur_language) | language | Requires summary integration | Highlights Arabic-script vowels and Latin transliteration for ISO `ug`. |
| Medium | [Wolof language](https://en.wikipedia.org/wiki/Wolof_language) | language | Pending structured ingestion | Tone and nasal cluster references for ISO `wo` roadmaps. |
| Medium | [Igbo language](https://en.wikipedia.org/wiki/Igbo_language) | language | Pending structured ingestion | Nasal harmony, tone ladder, and syllabic nasal planning for ISO `ig`. |
| Medium | [Irish language](https://en.wikipedia.org/wiki/Irish_language) | language | Pending structured ingestion | Lenition/eclipsis scheduling to calibrate consonant hardness sliders for `ga-IE`. |
| Medium | [Georgian language](https://en.wikipedia.org/wiki/Georgian_language) | language | Pending structured ingestion | Ejective consonant frequencies and vowel harmony metadata for ISO `ka`. |
| Medium | [Mongolian language](https://en.wikipedia.org/wiki/Mongolian_language) | language | Pending structured ingestion | Captures vowel harmony and syllable timing data for ISO `mn`. |
| Medium | [Kinyarwanda](https://en.wikipedia.org/wiki/Kinyarwanda) | language | Requires phoneme summary | Plateau tone modelling and nasal prefix phonotactics for ISO `rw`. |

## Policy, usage, and priority metrics

| Usefulness | Source | Classification | Progress | NVDA planning hook |
| --- | --- | --- | --- | --- |
| Critical | [List of official languages by country and territory](https://en.wikipedia.org/wiki/List_of_official_languages_by_country_and_territory) | language / metadata | Pending structured ingestion | Guides jurisdiction-specific packaging and QA. |
| High | [List of official languages](https://en.wikipedia.org/wiki/List_of_official_languages) | language / metadata | Pending structured ingestion | Complements country-level planning. |
| Medium | [List of official languages of international organizations](https://en.wikipedia.org/wiki/List_of_official_languages_of_international_organizations) | language / metadata | Pending structured ingestion | Ensures NGO/IGO accessibility commitments. |
| High | [Lists of countries and territories by official language](https://en.wikipedia.org/wiki/Lists_of_countries_and_territories_by_official_language) | language / metadata | Pending structured ingestion | Provides per-language jurisdiction roll-ups. |
| High | [List of countries by number of languages](https://en.wikipedia.org/wiki/List_of_countries_by_number_of_languages) | language / metadata | Pending structured ingestion | Highlights multilingual hotspots for rapid phoneme expansion. |
| Medium | [Linguistic diversity index](https://en.wikipedia.org/wiki/Linguistic_diversity_index) | language / metadata | Pending structured ingestion | Quantifies impact of coverage gains. |
| High | [List of languages by total number of speakers](https://en.wikipedia.org/wiki/List_of_languages_by_total_number_of_speakers) | language / metadata | Pending structured ingestion | Prioritises mainstream coverage. |
| Medium | [Languages used on the Internet](https://en.wikipedia.org/wiki/Languages_used_on_the_Internet) | language / metadata | Pending structured ingestion | Aligns with NVDA users' online environments. |
| Medium | [List of lingua francas](https://en.wikipedia.org/wiki/List_of_lingua_francas) | language / sociolinguistics | Pending structured ingestion | Informs accent slider defaults for cross-region communication. |
| Medium | [Regional language](https://en.wikipedia.org/wiki/Regional_language) | language / policy | Requires summary integration | Clarifies legal definitions for packaging. |
| Medium | [International English](https://en.wikipedia.org/wiki/International_English) | language / accent | Requires summary integration | Supports global English presets with neutral EQ settings. |
| High | [Mutual intelligibility list](https://en.wikipedia.org/wiki/Mutual_intelligibility#List_of_mutually_intelligible_languages) | language / dialect / accent | Requires summary integration | Aligns accent/dialect tiers with user expectations. |
| Medium | [List of dictionaries by number of words](https://en.wikipedia.org/wiki/List_of_dictionaries_by_number_of_words) | lexicon / language | Pending structured ingestion | Targets corpora for phoneme and prosody modelling. |

## Constructed, mixed, and signed languages

| Usefulness | Source | Focus |
| --- | --- | --- |
| High | [List of constructed languages in fiction](https://en.wikipedia.org/wiki/List_of_constructed_languages#Languages_used_in_fiction) | Seed phoneme templates for fictional/auxiliary languages. |
| Medium | [International auxiliary language](https://en.wikipedia.org/wiki/International_auxiliary_language) | Context for auxlang prioritisation. |
| Medium | [Universal language](https://en.wikipedia.org/wiki/Universal_language) | Historical framing for universal speech projects. |
| Medium | [List of creole languages](https://en.wikipedia.org/wiki/List_of_creole_languages) | Lexifier/substrate guidance for EQ blending. |
| Medium | [Mixed language examples](https://en.wikipedia.org/wiki/Mixed_language#Examples) | Data for blended phoneme sets. |
| Medium | [Indo-European based pidgins, creoles, mixed languages, and cants](https://en.wikipedia.org/wiki/List_of_pidgins,_creoles,_mixed_languages_and_cants_based_on_Indo-European_languages) | Focused subset for English/French/Spanish derivatives. |
| Medium | [List of English-based pidgins](https://en.wikipedia.org/wiki/List_of_English-based_pidgins) | Accent slider presets for English variants. |
| High | [List of sign languages](https://en.wikipedia.org/wiki/List_of_sign_languages) | Planning dataset for sign-language phoneme proxies and NVDA iconography. |
| Medium | [List of sign languages by number of native signers](https://en.wikipedia.org/wiki/List_of_sign_languages_by_number_of_native_signers) | Prioritisation by community size. |

## Technical, programming, and modelling languages

These resources ensure Eloquence can speak developer-centric content with the
same clarity controls as natural languages.

| Usefulness | Source | Focus |
| --- | --- | --- |
| Medium | [List of programming languages](https://en.wikipedia.org/wiki/List_of_programming_languages) | Baseline for code pronunciation dictionaries. |
| Medium | [List of BASIC dialects](https://en.wikipedia.org/wiki/List_of_BASIC_dialects) | Retro computing dialect coverage. |
| Medium | [Category: Lists of computer languages](https://en.wikipedia.org/wiki/Category:Lists_of_computer_languages) | Index for specialised DSLs. |
| Medium | [Lists of programming languages](https://en.wikipedia.org/wiki/Lists_of_programming_languages) | Entry point to domain-specific subsets. |
| Medium | [Ontology language classification](https://en.wikipedia.org/wiki/Ontology_language#Classification_of_ontology_languages) | Terminology for knowledge-graph workflows. |
| Medium | [Modelling language types](https://en.wikipedia.org/wiki/Modeling_language#Type_of_modeling_languages) | UML/SysML articulation guidance. |
| Medium | [List of markup languages](https://en.wikipedia.org/wiki/List_of_markup_languages) | HTML/XML/SGML variant coverage. |
| Medium | [List of shorthand systems](https://en.wikipedia.org/wiki/List_of_shorthand_systems) | High-speed phoneme articulation references. |
| Medium | [Omniglot](https://en.wikipedia.org/wiki/Omniglot) | External audio/script samples to complement Wikipedia data. |

## Next steps

* Prioritise converting the ISO 639 and ISO 15924 tables into structured JSON so
  phoneme seed bundles can automatically inherit code metadata and script
  associations.
* Cross-link family and region pages with existing seed locales (42 languages)
  to validate mutual intelligibility assumptions and accent slider defaults.
* When importing pronunciation inventories, map consonant/vowel categories to
  the expanded NV Speech Player parameters (emphasis, stress, timbre, tone,
  vocal layers, overtones, subtones, vocal range, inflection contour, roughness,
  smoothness, whisper, head size contour, macro volume, tone size, scope depth)
  so the phoneme customiser can translate Wikipedia research directly into EQ
  and sample-rate aware presets.
* Document progress in the README and NVDA-specific guides as new datasets are
  ingested, ensuring blind contributors can locate regional voices, adjust
  phoneme EQ bands, and verify that Eloquence honours the active audio device's
  sample rate (8–384 kHz) when rendering speech.
