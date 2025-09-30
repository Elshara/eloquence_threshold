# ISO language expansion roadmap

This living roadmap outlines how Eloquence Threshold is expanding ISO 639 and BCP-47 coverage across Unicode scripts while keeping speech parameters, dictionary inventories, and vocal metrics aligned with NVDA's latest capabilities. It synthesises information from the repository's cached Wikipedia, NVDA, GitHub, and DataJake research snapshots.

## ISO code coverage snapshot

| ISO / tag | Script focus | Status | Notes |
| --- | --- | --- | --- |
| aa | Ethiopic & Latin (Afar) | Researching | Wikipedia phonology notes paired with DataJake `.dic` inventories; GitHub transliteration tools tracked to balance Ethiopic and Latin orthography with NVDA braille tables. |
| ab | Cyrillic & Latin (Abkhaz) | Researching | Cached Wikipedia ejective consonant inventories and DataJake Abkhaz grammar corpora align with GitHub palatalisation analysers; NVDA braille exports validate Abkhaz-specific diacritics before CodeQL-audited dictionary imports. |
| ady | Cyrillic (Adyghe) | Researching | Wikipedia phonotactics and ejective consonant charts merged with DataJake Caucasus field recordings and GitHub morphology analysers; NVDA braille exports confirm soft sign placement and glottal stop punctuation prior to CodeQL-reviewed dictionary seeding. |
| af | Latin (Afrikaans) | Planned | Wikipedia vowel length tables ingested; DataJake `.dic` backlog queued to confirm guttural G handling. |
| ak | Latin (Akan/Twi) | Researching | Cached Wikipedia tone ladders combined with DataJake sermon lexicons and GitHub Akan NLP tools; NVDA manual exports confirm apostrophe tone markers before CodeQL-audited `.dic` ingestion. |
| ain | Katakana & Latin (Ainu) | Researching | Wikipedia syllabary ⇄ Latin transcription tables paired with DataJake oral-history recordings and GitHub revitalisation grammars; NVDA braille exports validate macron and sokuon handling prior to CodeQL dictionary seeding. |
| ale | Latin & Cyrillic (Aleut) | Planned | Cached Aleut dictionaries from Wikipedia and DataJake missionary corpora staged with GitHub orthography converters; NVDA manual exports confirm glottal stop punctuation before packaging dual-script presets. |
| am | Ethiopic | Developing | Amharic phoneme deck seeded; awaiting Geez punctuation rules from NVDA alpha manuals before marking comprehensive. |
| bo | Tibetan | Planned | Wikipedia tone contour and stackable consonant charts staged; DataJake archives searched for Wylie transliteration lexicons. |
| bs | Latin (Bosnian) | Researching | Cached Wikipedia accentuation charts paired with DataJake Sarajevo news lexicons; GitHub Bosnian diacritic normalisers queued so NVDA braille exports keep č/ć/đ distinctions intact. |
| ar, ar-EG | Arabic | Seeded | Profiles sourced from `eloquence_data/languages/world_language_seeds.json`; leverages Quranic recitation corpora for emphatic consonants. |
| as | Bengali-Assamese | Planned | Wikipedia-derived consonant inventory staged; awaiting Assamese-specific schwa deletion tests via NVDA nightly builds. |
| ast | Latin (Asturian) | Planned | Cached Wikipedia nasal vowel and palatal lateral research combined with DataJake folk song dictionaries and NVDA braille contractions to guide **Inflection contour** presets prior to CodeQL dictionary ingestion. |
| az | Latin (Azeri) | Planned | GitHub transliteration utilities catalogued; NVDA docs scanned for glottal stop punctuation cues. |
| azb | Perso-Arabic & Latin (South Azerbaijani) | Researching | DataJake radio glossaries and Wikipedia vowel harmony tables paired with GitHub morphology generators; NVDA manual punctuation exports confirm hamza and macron handling across scripts before packaging. |
| ba | Cyrillic & Latin (Bashkir) | Researching | Cached Wikipedia vowel harmony/velarisation tables paired with DataJake folk song corpora and GitHub transliteration tools; NVDA braille exports confirm Bashkir-specific diacritics before EQ tuning. |
| bam | Latin & N’Ko (Bambara) | Researching | Wikipedia Manding tone ladder research and DataJake radio sermon corpora align with GitHub Bambara morphological parsers; NVDA braille exports verify nasal vowel diacritics before CodeQL-reviewed dictionary imports tune **Subtones**/**Nasal balance** presets. |
| bem | Latin (Bemba) | Researching | Cached Wikipedia Zambian tone studies plus DataJake hymn dictionaries pair with GitHub tonal segmentation notebooks; NVDA braille exports confirm prenasalised consonant markers ahead of NV Speech Player **Vocal layers**/**Head size contour** calibration. |
| bg | Cyrillic (Bulgarian) | Developing | DataJake MBROLA payloads flagged for vowel reduction heuristics; Wikipedia stress matrices under review. |
| bi | Latin (Bislama) | Planned | Cached Wikipedia phonotactic notes and DataJake Radio Vanuatu lexicons align with GitHub orthography converters; NVDA manual exports confirm apostrophe punctuation before CodeQL profile seeding. |
| bn, bn-IN | Bengali | Comprehensive | Builds on DataJake phoneme stubs and NVDA manual terminology to map inherent vowel suppression rules. |
| ca | Latin (Catalan) | Planned | Language index cross-references DECtalk lexicons for liaison; CodeQL follow-up recorded for 2025-Q4. |
| cab | Latin (Garifuna) | Researching | Cached Wikipedia Garifuna phonology and orthography charts paired with DataJake community radio `.dic` inventories; GitHub revitalisation grammars and NVDA braille exports confirm apostrophe tone markers prior to EQ tuning. |
| ckb | Perso-Arabic & Latin (Sorani Kurdish) | Researching | Wikipedia vowel harmony and tanwīn-style diacritic notes cross-referenced with DataJake civic-language corpora and GitHub Sorani analysers; NVDA braille tables reviewed for double-dot punctuation before CodeQL gating. |
| ceb | Latin (Cebuano) | Researching | DataJake hymn `.dic` payloads catalogued alongside GitHub orthography converters; cached Wikipedia vowel harmony notes guide NV Speech Player **Tone size** and **Subtones** defaults prior to CodeQL-audited profile seeding. |
| ch | Latin (Chamorro) | Planned | Wikipedia glottal stop guidance matched with DataJake Guam civic-language corpora and GitHub Chamorro spelling reform scripts; NVDA braille tables referenced to validate geminate consonant dots. |
| ckt | Cyrillic & Latin (Chukchi) | Researching | Cached Siberian fieldwork from Wikipedia paired with DataJake narrative recordings and GitHub polysynthetic morphology parsers; NVDA braille exports track apostrophe ejective markers prior to CodeQL gating. |
| cv | Cyrillic & Latin (Chuvash) | Researching | DataJake hymn recordings catalogued alongside Wikipedia vowel harmony and palatalisation notes; GitHub morphology projects feed CodeQL-audited dictionary staging with NVDA braille exports for diacritics. |
| co | Latin (Corsican) | Planned | Wikipedia vowel centralisation charts paired with DataJake liturgical corpora and GitHub dialect surveys; NVDA braille exports confirm grave-accent punctuation before tuning NV Speech Player **Vocal range** presets. |
| chr | Cherokee syllabary | Researching | Wikipedia syllabary tables mirrored; GitHub DECtalk lexicon fragments staged for syllable-to-phoneme mapping prior to NVDA braille export integration. |
| cs | Latin (Czech) | Established | Awaiting expanded consonant cluster rules from archived DECtalk dictionaries. |
| da | Latin (Danish) | Developing | NVDA documentation snapshot provides stød examples; DataJake lexicons mapped to vowel reduction slider defaults. |
| de-DE | Latin (German) | Developing | GitHub lexicon merges capture final devoicing; DataJake `.lex` payloads queued for rounding rules. |
| el | Greek | Developing | Wikipedia diphthong stress tables incorporated; NVDA manuals inform punctuation and braille alignments. |
| en-GB, en-US | Latin (English) | Comprehensive | Heritage Eloquence templates cross-referenced with GitHub-hosted pronunciation dictionaries. |
| es-ES, es-419 | Latin (Spanish) | Comprehensive | Castilian and Latin American variants mapped to NV Speech Player tone curves. |
| et | Latin (Estonian) | Planned | Partial vowel harmony patterns mirrored from Wikipedia; DataJake archives scanned for palatal consonant cues. |
| eu | Latin (Basque) | Researching | Ergative-absolutive grammar primers and sibilant harmony charts cached from Wikipedia; DataJake news dictionaries plus GitHub Euskara analyzers feed NV Speech Player **Inflection contour**/**Sibilant clarity** presets before CodeQL ingestion. |
| ee | Latin (Ewe) | Researching | Wikipedia ATR harmony charts, DataJake hymn `.dic` payloads, and GitHub tone sandhi analysers guide NV Speech Player **Tone**/**Subtones** presets; NVDA braille exports validate digraph punctuation. |
| eve | Cyrillic (Even) | Planned | Wikipedia phonotactics and glottal consonant notes aligned with DataJake scripture lexicons and GitHub orthography converters; NVDA braille exports validate diacritic usage ahead of pronunciation profile seeding. |
| evn | Cyrillic & Latin (Evenki) | Researching | Cached Tungusic vowel harmony studies combined with DataJake storytelling archives and GitHub morphological analysers; NVDA manuals confirm apostrophe ejective marks before CodeQL-reviewed dictionary imports. |
| fa | Arabic (Persian) | Comprehensive | Integrates Ezafe articulation from Wikipedia grammar references. |
| ff | Latin (Fula/Pulaar) | Researching | Wikipedia ATR harmony tables combined with DataJake Qur’anic recitations, GitHub Ajami↔Latin transliteration tools, and NVDA punctuation exports so CodeQL-audited dictionaries preserve implosive and prenasalised consonants. |
| fil | Latin (Filipino) | Seeded | NVDA manual extracts processed; awaiting morphological corpora from GitHub to tune affix pronunciation. |
| ga-IE | Latin (Irish Gaelic) | Planned | Adds BCP 47 regional tag; lenition/eclipsis roadmaps tie into NV Speech Player consonant hardness sliders. |
| fr | Latin (French) | Developing | DataJake `.dic` payloads assigned to nasal vowel validation; NVDA manual punctuation tables mirrored. |
| fur | Latin (Friulian) | Planned | Wikipedia orthography reforms and DataJake civic-language corpora paired with NVDA braille exports; NV Speech Player **Tone size** presets tuned for alveolar affricates prior to template seeding. |
| fy | Latin (West Frisian) | Planned | Cached Wikipedia vowel harmony notes, DataJake parliamentary transcripts, and GitHub spelling normalisers underpin **Stress**/**Sibilant clarity** slider defaults and upcoming dictionary imports. |
| ga | Latin (Irish) | Planned | Wikipedia mutation schedules recorded; NVDA docs referenced for braille grade 2 interplay. |
| gaa | Latin (Ga) | Researching | Cached Wikipedia nasal vowel inventories tied to DataJake broadcast corpora and GitHub orthography datasets; informs **Nasal balance**/**Macro volume** presets and NVDA punctuation regression tests. |
| gwi | Latin (Gwich’in) | Researching | Wikipedia tone/accent notes linked with DataJake lexicon scans; NVDA braille tables flagged for apostrophe tone markers. |
| gl | Latin (Galician) | Planned | Cross-referencing Spanish/Portuguese templates; GitHub accent dictionaries in review for gheada handling. |
| ha | Latin (Hausa) | Developing | Pulling tonal contour data from Wikipedia and DataJake `.lex` archives to align NV Speech Player **Tone** slider defaults. |
| haw | Latin (ʻŌlelo Hawaiʻi) | Planned | Wikipedia phonology tables and `ʻokina`/kahakō orthography guides staged; DataJake hymn corpora queued to map macron vowels and NVDA braille exports to diacritic rules. |
| ig | Latin (Igbo) | Planned | Tone ladder and nasal harmony cues catalogued; GitHub finite-state resources queued for vowel alternation. |
| ilo | Latin (Ilocano) | Researching | DataJake radio news corpora and GitHub orthography datasets logged to validate glottal stop markers; Wikipedia vowel length notes align NV Speech Player **Tone size**/**Subtones** presets with Ilokano stress patterns. |
| iu | Canadian Aboriginal syllabics & Latin (Inuktitut) | Researching | DataJake `.lex` payloads catalogued alongside Wikipedia syllabics charts; NVDA manual punctuation tables queued for mixed-script fallback validation. |
| he | Hebrew | Seeded | Masoretic vowel points mirrored from NV Access documentation snapshots; DataJake lexicons flagged for cantillation cues. |
| hi-IN | Devanagari | Established | Retroflex and breathy-voiced contrasts sourced from DataJake MBROLA inventories. |
| hil | Latin (Hiligaynon) | Researching | Cached Wikipedia stress and glottal stop notes combine with DataJake liturgical lexicons; GitHub syllable tokenisers drive NV Speech Player **Inflection contour** presets awaiting profile ingestion. |
| hmn | Latin & Pahawh (Hmong Daw) | Researching | Wikipedia tone contour charts and GitHub tonal analysis notebooks paired with DataJake oral history recordings; NV Speech Player **Tone**, **Scope depth**, and **Whisper** sliders queued for validation via `docs/voice_frequency_matrix.md`. |
| hr | Latin (Croatian) | Researching | Wikipedia digraph and accent tables mirrored; DataJake radio drama `.dic` payloads staged alongside GitHub prosody corpora so NV Speech Player **Inflection contour** defaults capture rising tone contrasts. |
| ht | Latin (Haitian Creole) | Planned | Cached Wikipedia nasalisation charts paired with DataJake pronunciation dictionaries; NVDA braille tables referenced for French-derived punctuation cues before seeding lexicons. |
| id | Latin (Indonesian) | Comprehensive | Wikipedia phonotactic notes merged with GitHub syllabification scripts; 100% IPA coverage confirmed in `docs/language_coverage.md`. |
| is | Latin (Icelandic) | Planned | NVDA manual punctuation cues archived; GitHub pronunciation datasets queued for vowel length calibration. |
| it | Latin (Italian) | Developing | DataJake lexicons confirm open/closed E and O patterns; Wikipedia entries mapped to NV Speech Player inflection curves. |
| ja | Japanese | Developing | Kana digraph coverage linked to NVDA documentation and open-source kana-to-IPA mappings. |
| jam | Latin (Jamaican Patois) | Researching | Wikipedia grammar portal mirrored; DataJake reggae narration lexicons flagged to map creole vowel mergers and NV Speech Player **Inflection contour** defaults. |
| ka | Georgian (Mkhedruli) | Planned | Wikipedia ejective consonant inventory stored; NV Speech Player presets targeted for uvular EQ boosts. |
| kbd | Cyrillic (Kabardian) | Researching | DataJake Kabardian dictionaries and Wikipedia consonant harmony notes paired with GitHub finite-state morphology scripts; NVDA braille exports confirm soft sign usage for affricates ahead of pronunciation profile seeding. |
| kca | Cyrillic & Latin (Khanty) | Researching | Wikipedia consonant gradation charts merged with DataJake oral-history lexicons and GitHub morphological analysers; NVDA braille exports confirm diacritic handling prior to CodeQL-reviewed dictionary imports. |
| kl | Latin (Kalaallisut) | Researching | Greenlandic polysynthetic morphology mapped from Wikipedia; GitHub analysers referenced for suffix stacking during phoneme generation. |
| ks | Perso-Arabic & Sharada (Kashmiri) | Planned | Dual-script roadmap logged; NVDA braille tables and GitHub transliteration utilities referenced for voiceless aspirate handling. |
| ky | Cyrillic & Latin (Kyrgyz) | Researching | Wikipedia vowel harmony charts and DataJake MBROLA lexicons align with GitHub transliteration utilities; NV Speech Player **Tone**/**Vocal range** presets staged pending dual-script validation in NVDA manuals. |
| lb | Latin (Luxembourgish) | Planned | Cached Wikipedia digraph inventories, DataJake parliamentary corpora, and GitHub G Lëtzebuergesch spelling normalisers guide **Stress**/**Sibilant clarity** presets and NVDA braille hyphenation tests. |
| lzz | Georgian & Latin (Laz) | Researching | Wikipedia Laz orthography primers and DataJake Black Sea dialect corpora paired with GitHub Georgian↔Latin converters; NVDA braille exports validate ejective apostrophe usage prior to CodeQL-reviewed dictionary imports. |
| jv | Latin (Javanese) | Planned | Script variants (Latin/Hanacaraka) catalogued in the Wikipedia index; awaiting dictionary ingestion to resolve vowel length cues. |
| kk | Cyrillic (Kazakh) | Planned | Cyrillic/Latin dual-script corpora tagged; NVDA docset scanned for apostrophe-based digraph hints. |
| km | Khmer | Planned | Unicode dependent vowel tables mirrored; DataJake MBROLA seeds under review for diphthong contours. |
| kmr | Latin (Kurmanji Kurdish) | Researching | Cached Wikipedia phonotactics and DataJake broadcast lexicons tie into GitHub Latin-script morphology generators; NV Speech Player **Tone size** and **Scope depth** presets tuned for vowel harmony before NVDA braille regression tests. |
| ko | Hangul | Developing | Syllable block decomposition cross-checked against NV Speech Player recordings and GitHub Hangul-to-IPA resources. |
| koi | Cyrillic (Komi-Permyak) | Researching | Cached Wikipedia vowel harmony and palatalisation notes aligned with DataJake folk-song lexicons and GitHub Uralic finite-state analysers; NVDA braille exports validate diacritics before CodeQL-ingested dictionaries. |
| kpv | Cyrillic (Komi-Zyrian) | Researching | Wikipedia ergative alignment primers combined with DataJake archival recordings and GitHub morphological segmenters; NVDA manuals confirm soft sign handling ahead of pronunciation profile staging. |
| lg | Latin (Luganda) | Researching | Wikipedia noun-class tone tables paired with DataJake scripture `.dic` payloads and GitHub Luganda morphological analysers; NVDA braille exports capture prenasalised digraph rules prior to CodeQL review. |
| ln | Latin (Lingala) | Researching | DataJake radio/scripture archives and GitHub tone sandhi scripts drive Lingala contour presets; NVDA punctuation snapshots validate French-derived quotation marks before packaging. |
| loz | Latin (Lozi) | Researching | Cached Wikipedia Lozi tone/accent guides merged with DataJake Barotseland hymn corpora and GitHub tonal morphology projects; NVDA braille exports validate diacritics while **Plosive impact**/**Macro volume** sliders capture baritone delivery. |
| lt | Latin (Lithuanian) | Planned | Stress accent reports collated from Wikipedia; DataJake archives triaged for pitch contour metadata. |
| lus | Latin (Mizo/Lushai) | Researching | Cached Wikipedia tone registers and GitHub tonal classifier notebooks paired with DataJake hymn archives; NV Speech Player **Tone**, **Scope depth**, and **Nasal balance** presets flagged for Mainland Southeast Asia validation. |
| mg | Latin (Malagasy) | Planned | DataJake news corpora catalogued for tone/stress guidance; Wikipedia phonotactics and NVDA manual punctuation exports cross-referenced to seed NV Speech Player **Inflection contour** defaults. |
| mhr | Cyrillic & Latin (Meadow Mari) | Researching | Cached vowel harmony and geminate consonant charts from Wikipedia paired with DataJake choral lexicons and GitHub Mari finite-state analysers; NVDA braille exports validate diacritic permutations before CodeQL ingestion. |
| miq | Latin (Miskito) | Planned | Wikipedia nasal stress notes cross-checked with DataJake scripture corpora; GitHub orthography converters and NVDA braille exports validate accent markers ahead of NV Speech Player **Scope depth** presets. |
| mi | Latin (Māori) | Planned | Wikipedia vowel length and wh/ng consonant inventories staged; DataJake hymn recordings tagged for nasal resonance to drive **Nasal balance** presets alongside NVDA braille exports. |
| niu | Latin (Niuean) | Planned | Cached Wikipedia vowel length + stress tables paired with DataJake hymn dictionaries; NVDA braille exports and GitHub Niuean orthography projects confirm macron rendering for offline packaging. |
| niv | Cyrillic & Latin (Nivkh) | Researching | Wikipedia orthography comparisons catalogued alongside DataJake fishing narrative recordings and GitHub revitalisation grammars; NVDA braille exports validate apostrophe ejective marks before CodeQL ingestion. |
| mn | Cyrillic (Mongolian) | Planned | NVDA manuals document vowel harmony; GitHub morphological analysers tagged for contextual suffixes. |
| mos | Latin (Mooré) | Researching | Wikipedia Mossi noun-class tone ladders cross-referenced with DataJake news lexicons and GitHub finite-state analysers; NV Speech Player **Tone**/**Scope depth** defaults tuned alongside NVDA braille exports before packaging. |
| mrj | Cyrillic & Latin (Hill Mari) | Researching | Cached Wikipedia palatalisation notes merged with DataJake liturgical corpora and GitHub Mari morphological toolkits; NVDA braille exports ensure soft sign and umlaut coverage before CodeQL review. |
| mns | Cyrillic & Latin (Mansi) | Researching | Wikipedia consonant gradation and vowel harmony notes cross-referenced with DataJake oral history recordings and GitHub segmentation notebooks; NVDA manuals confirm diacritic placement prior to pronunciation seeding. |
| lv | Latin (Latvian) | Planned | Phoneme coverage flagged for tonal accent validation; NVDA manual quotes stored for macron handling. |
| mai | Devanagari (Maithili) | Planned | ISO 639-3 entry added via Wikipedia crawler; DataJake archives searched for `.lex` payloads before seeding. |
| mr | Devanagari (Marathi) | Planned | DataJake dictionaries surfaced via archive audit; Wikipedia schwa deletion tables queued for validation. |
| ne | Devanagari (Nepali) | Planned | Cached Wikipedia vowel length charts staged; GitHub corpora tagged for schwa deletion and tone neutralisation checks prior to CodeQL validation. |
| mt | Latin (Maltese) | Planned | NVDA manuals highlight Semitic roots; GitHub lexicons queued to validate emphatic consonants. |
| nso | Latin (Northern Sotho) | Planned | Bantu tone tiers mapped; DataJake references under review for alveolar click representations. |
| oc | Latin (Occitan) | Planned | Troubadour phonology, DataJake poetry corpora, and GitHub Occitan normalisers coordinate NV Speech Player **Nasal balance** presets with NVDA braille diacritic tests. |
| om | Ethiopic & Latin (Oromo) | Planned | Wikipedia Gadaa dialect splits recorded; NVDA documentation scanned for Latin orthography fallback. |
| or | Odia (Oriya) | Planned | Script-specific ligatures inventoried; DataJake `.lex` search queued for inherent vowel suppression rules. |
| pa, pa-Arab | Gurmukhi & Shahmukhi (Punjabi) | Planned | Dual-script packaging references NVDA manual samples; DataJake `.dic` payloads tagged for tone and retroflex calibration. |
| pam | Latin (Kapampangan) | Planned | GitHub orthography converters and Wikipedia phonotactics underpin NVDA braille punctuation tests; DataJake bilingual hymn corpora logged to confirm glottal stop markers before generating Visayan-aligned profiles. |
| pap | Latin (Papiamento) | Researching | Cached Caribbean creole phonology articles mapped to DataJake tourism and education lexicons; NV Speech Player **Tone size** presets staged while GitHub transliteration utilities and NVDA braille exports reconcile diacritics. |
| pau | Latin (Palauan) | Planned | DataJake civic-education transcripts catalogued with Wikipedia phonology research and GitHub reduplication analysers; NV Speech Player **Tone size**/**Vocal layers** defaults queued pending braille punctuation validation. |
| ps | Pashto (Perso-Arabic) | Planned | Wikipedia retroflex/aspirate notes mirrored; GitHub romanisation tools catalogued to align dual-script presets and NVDA punctuation exports. |
| pl | Latin (Polish) | Developing | Soft consonant palatalisation traces pulled from GitHub; NVDA manuals confirm punctuation spacing. |
| pt-BR | Latin (Portuguese) | Established | NVDA manuals and GitHub lexicons align sibilant and nasal vowel behaviours. |
| quc | Latin (K'iche') | Researching | Wikipedia Mayan phoneme tables staged with DataJake scripture lexicons; GitHub community grammars and NVDA braille exports validate ejective consonant markers ahead of CodeQL-audited dictionary imports. |
| rap | Latin (Rapa Nui) | Planned | GitHub revitalisation grammars and DataJake oral-history recordings document glottal stop and vowel length cues; NVDA braille tables mapped to confirm Polynesian macron coverage prior to slider tuning. |
| ro | Latin (Romanian) | Planned | DECtalk lexicon ancestry catalogued; Wikipedia sources list vowel centralisation heuristics pending validation. |
| rm | Latin (Romansh) | Planned | Wikipedia orthography reforms, DataJake canton education corpora, and NVDA braille exports align digraph handling with NV Speech Player **Tone size**/**Inflection contour** presets ahead of template tuning. |
| ru | Cyrillic (Russian) | Developing | Awaiting vowel reduction matrices from Wikipedia stress tables before graduating to "established". |
| rn | Latin (Kirundi) | Planned | GitHub morphological analyzers catalogued; DataJake `.lex` payloads queued to document Bantu noun-class tones alongside NVDA punctuation exports. |
| rw | Latin (Kinyarwanda) | Planned | Tone plateau heuristics sourced from Wikipedia; NV Speech Player pitch defaults mapped for nasal prefix handling. |
| sk | Latin (Slovak) | Planned | Stress-on-first-syllable rules confirmed; DataJake `.dic` payloads awaited for rhythmic length tuning. |
| sl | Latin (Slovene) | Researching | Wikipedia pitch-accent contours combined with DataJake hymn lexicons; GitHub Slovene lemmatisers logged to map tonemic diacritics before refreshing NVDA braille exports. |
| sq | Latin (Albanian) | Researching | Cached Wikipedia vowel reduction and stress tables coupled with DataJake diaspora lexicons; GitHub Albanian morphological analysers logged so NV Speech Player **Tone**/**Sibilant clarity** presets balance Gheg/Tosk contrasts. |
| sm | Latin (Samoan) | Planned | Glottal stop (`ʻeta`) usage catalogued from Wikipedia; DataJake scripture datasets mapped to vowel length for EQ calibration and NVDA braille hyphenation. |
| sd | Arabic (Sindhi) | Planned | Arabic-derived vowel marks and Sindhi-specific consonants tracked; NVDA braille tables referenced for implosive consonant cues. |
| sg | Latin (Sango) | Researching | DataJake scripture corpora inventoried; Wikipedia tonal reduction studies combined with NVDA manual punctuation exports to calibrate **Macro volume** and **Tone** sliders. |
| sah | Cyrillic (Sakha/Yakut) | Researching | Cached Wikipedia vowel harmony and long consonant cues paired with DataJake storytelling archives; NV Speech Player **Tone size**/**Scope depth** presets tuned while NVDA braille exports verify Cyrillic diacritics. |
| sc | Latin (Sardinian) | Planned | DataJake liturgical recordings, Wikipedia Logudorese/Campidanese phonology tables, and NVDA braille exports coordinate **Macro volume**/**Subtones** presets before importing community dictionaries. |
| sn | Latin (Shona) | Researching | Wikipedia downstep/whistled speech studies cross-referenced with DataJake pronunciation datasets and GitHub prosody corpora; NVDA manual exports confirm tone apostrophe behaviour before CodeQL gating. |
| sr, sr-Latn | Cyrillic & Latin (Serbian) | Researching | Cached Wikipedia palatalisation notes plus Serbian National Corpus samples funnel into DataJake `.lex` payload triage; NVDA manual exports confirm Cyrillic/Latin punctuation parity ahead of CodeQL-audited template seeding. |
| cnr | Latin (Montenegrin) | Planned | Wikipedia dual-accent overview staged; GitHub Montenegrin corpus snippets aligned with Serbian/Bosnian templates to validate ś/ź phoneme coverage. |
| yo | Latin (Yoruba) | Researching | Tone ladder charts and vowel harmony metadata from Wikipedia feed DataJake `.lex` payload seeding; NV Speech Player **Tone size**/**Scope depth** presets tuned alongside NVDA braille exports and CodeQL dictionary validation. |
| yrk | Cyrillic & Latin (Nenets) | Researching | Cached Wikipedia nasal harmony tables merged with DataJake scripture corpora and GitHub Nenets morphological toolkits; NVDA braille exports confirm superscript diacritics before CodeQL-audited pronunciation staging. |
| zza | Perso-Arabic & Latin (Zazaki) | Researching | Wikipedia vowel harmony and stress analyses plus DataJake liturgical recordings guide NV Speech Player **Inflection contour** presets; GitHub Kurdish–Zaza converters and NVDA braille exports confirm diacritic mapping across scripts. |
| so | Latin (Somali) | Planned | Wikipedia ATR harmony and emphatic consonant notes catalogued; DataJake `.lex` archives queued to tune NV Speech Player **Tone** and **Sibilant clarity** sliders. |
| srr | Latin (Serer) | Researching | Wikipedia Serer ATR harmony research combined with DataJake Dakar radio corpora and GitHub nasal harmony analysers; NVDA braille exports confirm apostrophe tone markers before NV Speech Player **Macro volume**/**Subtones** tuning. |
| sw | Latin (Swahili) | Comprehensive | Phoneme templates tuned to recorded DataJake archives with 48 kHz stereo metadata. |
| si | Sinhala | Planned | Sinhala script stroke order and inherent vowel data mirrored; NV Speech Player contour presets targeted for murmur handling and DataJake lexicons flagged for geminate consonants. |
| snk | Latin & Ajami (Soninke) | Researching | Cached Wikipedia Soninke phonology paired with DataJake Sahelian scripture lexicons and GitHub Ajami transliteration notebooks; NVDA punctuation exports inform tone/apostrophe handling prior to CodeQL dictionary seeding. |
| tfn | Latin (Dena’ina) | Researching | Wikipedia dialect dossier ingested; DataJake archival wordlists tagged for tone plateau modelling and NV Speech Player **Nasal balance** presets. |
| tg | Cyrillic & Perso-Arabic (Tajik) | Researching | Wikipedia phonology articles linked with DataJake Persian/Tajik dictionaries; GitHub transliteration pipelines staged so NV Speech Player presets cover both scripts ahead of CodeQL review. |
| ti | Ethiopic (Tigrinya) | Researching | Ethiopic gemination charts captured from Wikipedia; DataJake lexicons and NVDA braille exports queued to validate Ge’ez punctuation while GitHub finite-state resources inform verb template planning. |
| tly | Perso-Arabic & Latin (Talysh) | Researching | Cached Wikipedia vowel harmony and nasalisation studies combined with DataJake Caspian corpora and GitHub transliteration tools; NV Speech Player **Nasal balance** presets tuned before NVDA punctuation regression tests. |
| tkl | Latin (Tokelauan) | Planned | Cached Wikipedia vowel length contour data merged with DataJake hymn lexicons and GitHub Tokelauan spelling checkers; NVDA braille exports validate macron and glottal stop behaviour ahead of CodeQL packaging checks. |
| tn | Latin (Setswana) | Planned | DataJake `.lex` payloads mapped to alveolar click coverage; NV Speech Player **Vocal range** slider defaults tuned using GitHub phonology datasets and NVDA hyphenation samples. |
| ts | Latin (Tsonga) | Planned | Bantu prenasalised stop inventories catalogued; DataJake recordings cross-checked with NVDA braille exports and GitHub prosody studies for tone calibration. |
| ta | Tamil | Developing | Script-specific vowel markers sourced from the Wikipedia-derived language index; DataJake MBROLA voices confirm retroflex weighting. |
| th | Thai | Planned | Wikipedia tone contour data collected; NV Speech Player slider mappings drafted to capture mid-level tone neutrality. |
| to | Latin (Tongan) | Planned | Cached Wikipedia stress placement rules and prenasalised stops inventoried; DataJake hymnal corpora queued to calibrate **Tone size**/**Vocal range** sliders with NVDA braille exports. |
| tr | Latin (Turkish) | Established | GitHub dictionaries confirm vowel harmony; NVDA manuals referenced for dotted capital I edge cases. |
| ty | Latin (Tahitian) | Planned | Wikipedia phonology notes mirrored; DataJake lexicons queued for glottal stop handling while NVDA documentation guides apostrophe-based braille entries. |
| uk | Cyrillic (Ukrainian) | Seeded | Stress data mirrored from Wikipedia tables; DataJake archives flagged for palatalisation pairs. |
| vi | Latin (Vietnamese) | Developing | Tone sandhi heuristics pulled from Wikipedia; DataJake lexical tone recordings assigned to frequency matrix planning. |
| war | Latin (Waray-Waray) | Planned | Wikipedia stress and vowel length charts combined with DataJake scripture recordings; GitHub syllabifiers queued to validate glottal stop notation before refreshing NVDA braille exports. |
| wa | Latin (Walloon) | Planned | Cached Wikipedia nasal vowel inventories, DataJake folk song lexicons, and NVDA braille contraction tables align Walloon diphthongs with NV Speech Player **Nasal balance** presets prior to dictionary ingestion. |
| wo | Latin (Wolof) | Researching | Wikipedia ATR harmony and nasalisation studies linked with DataJake Dakar radio lexicons and GitHub Wolof finite-state grammars; NVDA braille exports validate apostrophe tone markers before calibrating **Tone**/**Scope depth** presets. |
| zh-Hans | Han (Simplified Chinese) | Developing | NVDA dictionary extracts and GitHub Pinyin to IPA datasets align; DataJake tone recordings queued for 4-tone verification. |
| zh-Hant | Han (Traditional Chinese) | Planned | Wikipedia-based bopomofo mapping added; awaiting DataJake lexicons for Hakka/Min overlays. |
| udm | Cyrillic (Udmurt) | Researching | DataJake folk song corpora queued with Wikipedia consonant harmony notes; GitHub finite-state analysers guide NV Speech Player **Sibilant clarity**/**Smoothness** sliders and NVDA braille exports confirm diacritics. |
| ug | Arabic & Latin (Uyghur) | Planned | Wikipedia vowel harmony notes stored; GitHub Latinisation datasets and NVDA punctuation exports staged for dual-script packaging. |
| uz | Latin & Cyrillic (Uzbek) | Planned | Script switcher seeded using GitHub transliteration rules; DataJake `.dic` inventory queued to verify vowel harmony and stress. |
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

## Eastern Europe and Caucasus integration sprint (October 2025)

| ISO / tag | Script focus | Status | Notes |
| --- | --- | --- | --- |
| bg | Cyrillic (Bulgarian) | Developing | Cached *Bulgarian phonology* Wikipedia stress/voicing notes merged with DataJake MBROLA payloads; NVDA manual punctuation cues align with the loader’s Cyrillic handling. |
| mk | Cyrillic (Macedonian) | Researching | Wikipedia vowel reduction datasets staged; GitHub transliteration scripts under CodeQL review before importing DataJake lexicon fragments. |
| ka | Georgian (Mkhedruli) | Researching | Mkhedruli inventory catalogued; NVDA manual hyphenation tables queued to validate syllable segmentation prior to braille export support. |
| hy | Armenian (Mesropian) | Researching | Leveraging Wikipedia digraph tables and DataJake `.dic` payloads; voice templates will mirror NV Speech Player **Tone size** defaults for pitch accent cues. |
| az | Latin / Cyrillic / Arabic (Azerbaijani) | Planned | Tri-script transliteration utilities from GitHub staged; DataJake lexicons flagged for vowel harmony checks across script variants. |
| kk | Cyrillic / Latin (Kazakh) | Planned | Wikipedia vowel harmony and ejective consonant data paired with NVDA documentation; DataJake archives under review for new `.dic` payloads. |
| lt | Latin (Lithuanian) | Researching | Pitch accent metadata from Wikipedia combined with DataJake `.dic` payloads; NV Speech Player **Subtones** slider earmarked for calibration. |
| lv | Latin (Latvian) | Researching | Tone/length tables from Wikipedia and NVDA punctuation exports staged; DataJake lexicons flagged for palatalisation heuristics. |

### Frequency, phoneme, and speech parameter backlog

- Harvest DataJake MBROLA captures for Bulgarian and Macedonian to calibrate NV Speech Player **Stress**, **Vocal layers**, and **Plosive impact** slider defaults; document comparisons in `docs/voice_parameter_report.md` after regenerating the report.
- Feed Armenian and Georgian vowel/consonant length metadata into `phoneme_customizer.py` presets, ensuring 8–384 kHz frequency clamps align with the WASAPI-aware EQ handling recorded in [`docs/voice_parameter_report.md`](docs/voice_parameter_report.md).
- Build pitch-accent validation scripts for Lithuanian and Latvian that leverage GitHub morphological corpora while exposing the derived bands to CodeQL so automation can detect missing slider annotations.

### Dictionary and corpus integration tasks

- Expand `docs/language_research_index.md` with the cached Wikipedia bibliographies used above and link each to the relevant DataJake `.dic` payload once extracted; refresh the index via `tools/summarize_language_assets.py` so provenance stays aligned.
- Stage Azerbaijani and Kazakh lexicons from DataJake archives under `eloquence_data/` and run `python tools/report_language_maturity.py` to surface script-specific coverage gaps before packaging.
- Coordinate NVDA manual updates for Mkhedruli, Armenian, and Cyrillic punctuation tables so the offline packaging playbook can reference consistent braille/hyphenation guidance.

### Testing and packaging checkpoints

- Validate the new locales against NVDA alpha-52762 nightly builds and `2025.3` stable installers using the cached audit reports.
- Update `AGENTS.md` after each sprint to log the NVDA build numbers, CodeQL findings, and DataJake/GitHub/Wikipedia artefacts referenced when refreshing the Eastern Europe and Caucasus roadmap entries.

## Andean and Amazonian integration sprint (October 2025 follow-up)

| ISO / tag | Script focus | Status | Notes |
| --- | --- | --- | --- |
| qu / quz / quy | Latin (Quechuan macrolanguage) | Researching | Cached Wikipedia corpora covering Cusco and Ayacucho Quechua supply vowel harmony and ejective stops; DataJake `.dic` payloads mapped via GitHub’s `qupobox` analyser power contextual suffix selection for `language_profiles.py`. |
| ay | Latin (Aymara) | Researching | NV Speech Player recordings document uvular–velar contrasts, while NVDA documentation caches provide braille hyphenation cues; DataJake lexicons under CodeQL review to confirm glottal stop markers. |
| gn | Latin (Guaraní) | Developing | Nasal harmony inventories (Wikipedia + DataJake) align with NV Speech Player **Nasal balance** defaults; GitHub morphological generators inform dictionary segmentation before packaging. |
| arn | Latin (Mapudungun) | Planned | GitHub morphological corpora and NV Access manual exports guide agglutinative suffix handling; DataJake archives flagged for aspirated affricate recordings feeding EQ presets. |
| shp | Latin (Shipibo-Conibo) | Planned | Fieldwork tone contour datasets (Wikipedia citations + DataJake audio) stage NV Speech Player **Inflection contour** defaults; NVDA punctuation exports pending for braille validation. |
| nah | Latin (Nahuatl macro-language) | Researching | GitHub orthography normalisers paired with DataJake recordings capture vowel length/glottal stops; NV Access documentation caches highlight punctuation conventions for future dictionary imports. |

### Frequency, phoneme, and speech parameter backlog

- Merge Shipibo-Conibo contour archives into `docs/voice_parameter_report.md` after regenerating the report so **Inflection contour**, **Tone size**, and **Subtones** sliders mirror recorded tone ladders.
- Stage Aymara uvular consonant EQ presets in `phoneme_customizer.py`, clamping boosts to the 1–3 kHz band while validating 8–384 kHz safety via the WASAPI-aware resampler described in `AGENTS.md`.
- Add Quechuan ejective/plosive comparisons to the DataJake utilisation dashboard by rerunning `python tools/summarize_language_assets.py --json docs/language_asset_summary.json --markdown docs/language_asset_summary.md --print`.
- Regenerate `docs/voice_language_matrix.md` and `docs/language_maturity.md` after seeding each locale so CodeQL jobs can track the maturity delta and ensure slider presets reference existing profiles.

### Dictionary and corpus integration tasks

- Inventory Guaraní `.dic`/`.lex` assets via `python tools/catalog_datajake_archives.py --json docs/archive_inventory.json --markdown docs/archive_inventory.md` and link them to the roadmap entries once CodeQL checks confirm consistent nasal harmony markers.
- Update `docs/language_research_index.md` / `.json` with the Wikipedia sources cited above (tone contour archives, orthography guides, and corpus references) so future contributors can follow the provenance trail.
- Coordinate with NVDA documentation maintainers to capture Mapudungun, Quechua, and Nahuatl punctuation tables in `docs/nvda_update_recommendations.md` after refreshing the NV Access audit snapshot.
- Extend `tests/test_cli_reports.py` with fixtures representing nasal harmony and ejective consonant metadata once the dictionaries land, ensuring the reporting helpers summarise the new fields correctly.

### Testing and packaging checkpoints

- Validate the Andean/Amazonian locales against NVDA alpha-52762 and `2025.3` installers mirrored via `python tools/audit_nvaccess_downloads.py` before staging a release candidate.
- Capture unit test and build logs in the pull request body (see the offline build rehearsal checklist) so blind/low-vision reviewers can replay the commands without leaving the terminal.
- Refresh the README sprint summary and `AGENTS.md` after each iteration to highlight the cross-source artefacts consumed during the expansion.

## Central Eurasian Silk Road sprint (October 2025 extension)

| ISO / tag | Script focus | Status | Notes |
| --- | --- | --- | --- |
| ky | Cyrillic & Latin (Kyrgyz) | Researching | Wikipedia vowel harmony charts aligned with DataJake MBROLA lexicons and GitHub transliteration utilities; NVDA braille exports confirm apostrophe-based digraphs before seeding dual-script presets. |
| kk | Cyrillic & Latin (Kazakh) | Researching | Cached vowel harmony and ejective consonant data reused from the global roadmap now includes DataJake news corpora and NVDA punctuation audits to stage NV Speech Player **Tone**/**Macro volume** defaults. |
| tg | Cyrillic & Perso-Arabic (Tajik) | Researching | Persian phonology references matched with Tajik Cyrillic orthography; GitHub Latinisation pipelines and DataJake `.dic` payloads document dual-script packaging tasks ahead of CodeQL review. |
| ba | Cyrillic & Latin (Bashkir) | Researching | DataJake folk song recordings paired with Wikipedia velarisation notes and GitHub transliteration tools; NVDA braille exports confirm Bashkir diacritics before EQ calibration. |
| cv | Cyrillic & Latin (Chuvash) | Researching | Wikipedia vowel harmony and consonant palatalisation metadata staged with DataJake hymn corpora; GitHub morphological analysers drive CodeQL-audited dictionary imports. |
| sah | Cyrillic (Sakha/Yakut) | Researching | Cached vowel harmony, long consonant, and throat-singing timbre notes from Wikipedia cross-referenced with DataJake storytelling corpora to tune NV Speech Player **Tone size**/**Scope depth** presets. |
| udm | Cyrillic (Udmurt) | Researching | DataJake folk song lexicons and GitHub finite-state analysers stage consonant harmony coverage; NVDA braille exports validate diacritic handling before packaging. |

### Frequency, phoneme, and speech parameter backlog

- Regenerate `docs/voice_frequency_matrix.md` after capturing Kyrgyz and Bashkir vowel harmony EQ envelopes so **Tone**, **Vocal range**, and **Sibilant clarity** sliders reflect Central Eurasian spectral data.
- Map Tajik dual-script vowel inventories into `phoneme_customizer.py`, clamping frequency boosts to the 1–8 kHz band for Cyrillic vowels while verifying 8–384 kHz safety against the WASAPI-aware EQ engine recorded in `AGENTS.md`.
- Extend NV Speech Player presets with Sakha throat-singing overtone metadata by running `python tools/report_voice_parameters.py --json docs/voice_parameter_report.json --markdown docs/voice_parameter_report.md --print` after staging DataJake corpora.

### Dictionary and corpus integration tasks

- Audit DataJake archives for Bashkir, Chuvash, and Udmurt `.dic`/`.lex` payloads with `python tools/catalog_datajake_archives.py --json docs/archive_inventory.json --markdown docs/archive_inventory.md` and tag the findings in `docs/language_research_index.md` / `.json`.
- Capture GitHub transliteration utilities for Kyrgyz, Kazakh, and Tajik (Cyrillic ⇄ Latin/Perso-Arabic) in the research index so CodeQL policies can track dual-script pipelines before import.
- Coordinate NVDA manual snapshot refreshes via `python tools/audit_nvaccess_downloads.py` and `python tools/check_nvda_updates.py` whenever new Cyrillic/Latin documentation surfaces, then update `docs/nvda_update_recommendations.md` with the severity notes.

### Testing and packaging checkpoints

- Run `python tools/summarize_language_assets.py`, `python tools/report_language_maturity.py`, and `python tools/report_language_progress.py` after ingesting any Central Eurasian dictionaries so coverage dashboards log the dual-script deltas.
- Validate the updated locales against NVDA alpha-52762 nightly builds plus the cached `2025.3` stable installer, capturing logs in README/AGENTS updates for offline reproducibility.
- Exercise `python build.py --insecure --no-download --output dist/eloquence.nvda-addon` once the dashboards refresh to confirm the add-on packages new presets without accessing external mirrors.

## Circumpolar and Siberian revitalisation sprint (October 2025 continuation)

| ISO / tag | Script focus | Status | Notes |
| --- | --- | --- | --- |
| ain | Katakana & Latin (Ainu) | Researching | Wikipedia syllabary/Latin correspondence tables combined with DataJake oral-history recordings and GitHub revitalisation grammars; NVDA braille exports confirm macron and sokuon handling before CodeQL dictionary ingestion. |
| ale | Latin & Cyrillic (Aleut) | Planned | Dual-script hymn dictionaries from DataJake paired with Wikipedia orthography notes and GitHub transliteration helpers; NVDA manual exports verify glottal stop punctuation before packaging. |
| ckt | Cyrillic & Latin (Chukchi) | Researching | Cached Siberian fieldwork corpora mapped to DataJake narrative audio and GitHub polysynthetic morphology parsers; NVDA braille exports validate ejective apostrophes while CodeQL monitors archive extraction. |
| eve | Cyrillic (Even) | Planned | Wikipedia phonotactics, DataJake scripture lexicons, and GitHub orthography converters align Even consonant clusters; NVDA braille exports check diacritic placement ahead of pronunciation seeding. |
| evn | Cyrillic & Latin (Evenki) | Researching | Tungusic vowel harmony charts from Wikipedia merged with DataJake storytelling corpora and GitHub morphological analysers; NVDA manuals confirm apostrophe ejective markers before dictionary imports. |
| kca | Cyrillic & Latin (Khanty) | Researching | DataJake oral-history lexicons tied to Wikipedia consonant gradation notes and GitHub finite-state analysers; NVDA braille exports validate dotted vowels before CodeQL-reviewed profile staging. |
| koi | Cyrillic (Komi-Permyak) | Researching | Cached Wikipedia palatalisation metadata combined with DataJake folk-song dictionaries and GitHub Uralic analyzers; NVDA manuals confirm diacritics prior to transliteration tooling. |
| kpv | Cyrillic (Komi-Zyrian) | Researching | Ergative alignment primers from Wikipedia, DataJake archival recordings, and GitHub segmentation notebooks underpin the roadmap; NVDA braille exports guard soft sign handling before packaging. |
| mhr | Cyrillic & Latin (Meadow Mari) | Researching | DataJake choral lexicons paired with Wikipedia vowel harmony tables and GitHub Mari finite-state tooling; NVDA braille exports ensure umlaut permutations survive offline builds. |
| mrj | Cyrillic & Latin (Hill Mari) | Researching | Cached Wikipedia palatalisation notes cross-referenced with DataJake liturgical corpora and GitHub morphological toolkits; NVDA documentation validates diacritics for CodeQL-audited imports. |
| mns | Cyrillic & Latin (Mansi) | Researching | Wikipedia consonant gradation data aligned with DataJake oral-history recordings and GitHub segmentation notebooks; NVDA manuals confirm diacritic placement before pronunciation profile staging. |
| niv | Cyrillic & Latin (Nivkh) | Researching | Orthography comparison tables from Wikipedia merged with DataJake fishing narratives and GitHub revitalisation grammars; NVDA braille exports validate ejective markers while CodeQL tracks archive provenance. |
| yrk | Cyrillic & Latin (Nenets) | Researching | Wikipedia nasal harmony studies backed by DataJake scripture corpora and GitHub Nenets morphology projects; NVDA braille exports confirm superscript diacritics before dictionary seeding. |

### Frequency, phoneme, and speech parameter backlog

- Regenerate `docs/voice_frequency_matrix.md` and `docs/voice_parameter_report.md` after tuning NV Speech Player **Tone size**, **Scope depth**, **Subtones**, **Nasal balance**, and **Whisper** presets for Ainu, Khanty, Mansi, Nenets, and Evenki corpora; capture the delta in the README sprint summary.
- Extend `phoneme_customizer.py` with Tungusic ejective and long vowel presets sourced from GitHub morphological datasets while respecting the 1 Hz–384 kHz EQ clamps documented in `AGENTS.md`.
- Run `python tools/report_language_maturity.py`, `python tools/report_language_progress.py`, and `python tools/report_language_coverage.py` after merging new dictionary artefacts so CodeQL and README dashboards register the circumpolar deltas.

### Dictionary and corpus integration tasks

- Catalogue DataJake `.dic`/`.lex` payloads for Khanty, Mansi, Komi, and Mari using `python tools/catalog_datajake_archives.py --json docs/archive_inventory.json --markdown docs/archive_inventory.md`, then link the findings in `docs/language_research_index.md` / `.json`.
- Mirror GitHub revitalisation grammars (Ainu, Aleut, Nivkh, Chukchi) into the research index and stage transliteration utilities so CodeQL can monitor dual-script converters.
- Refresh NVDA manual caches for Nenets and Evenki braille tables via `python tools/audit_nvaccess_downloads.py` followed by `python tools/check_nvda_updates.py`; record severity shifts in `docs/nvda_update_recommendations.md`.

### Testing and packaging checkpoints

- Execute the reporting suite (`python tools/summarize_language_assets.py`, `python tools/report_integration_scope.py`, `python tools/report_catalog_status.py`, `python tools/report_voice_language_matrix.py`, `python tools/validate_language_pronunciations.py`) after staging new circumpolar assets so linkage, catalogue integrity, and pronunciation validation stay in sync.
- Run `python -m unittest discover tests` and `python build.py --insecure --no-download --output dist/eloquence.nvda-addon` to confirm offline packaging succeeds with the expanded datasets and frequency presets.
- Update `AGENTS.md` with the sprint summary, citing NVDA build numbers and CodeQL findings alongside the refreshed README guidance.

## Horn of Africa and Indian Ocean integration sprint (October 2025 extension)

| ISO / tag | Script focus | Status | Notes |
| --- | --- | --- | --- |
| ti | Ethiopic (Tigrinya) | Researching | Cached Wikipedia phonology charts and Ge’ez punctuation guides inform DataJake lexicon extraction; GitHub verb morphology analyzers will feed contextual generators before NVDA braille exports are regenerated. |
| aa | Ethiopic & Latin (Afar) | Researching | Balances Ethiopic gemination with Latinised fieldwork transcriptions; NVDA braille tables and DataJake `.dic` payloads align punctuation while CodeQL tracks transliteration helpers. |
| so | Latin (Somali) | Planned | ATR harmony datasets from Wikipedia merge with DataJake hymn corpora to calibrate NV Speech Player **Tone** and **Vocal range** defaults; NV Access manual exports confirm apostrophe handling for tone marks. |
| mg | Latin (Malagasy) | Planned | DataJake news archives highlight stress placement; GitHub morphology tools and NVDA hyphenation tables guide syllable segmentation before seeding voice templates. |
| rn | Latin (Kirundi) | Planned | Bantu noun-class tones recorded via DataJake `.lex` payloads; GitHub analyzers and NV Speech Player **Inflection contour** presets keep prenasalisation audible. |
| sg | Latin (Sango) | Researching | Wikipedia tonal reduction studies pair with DataJake scripture corpora; NVDA punctuation exports ensure French-derived digraphs pronounce correctly in offline builds. |
| tn | Latin (Setswana) | Planned | DataJake `.lex` inventories capture alveolar click metadata; GitHub phonology resources inform **Vocal range** and **Plosive impact** slider defaults validated against NVDA hyphenation samples. |
| ts | Latin (Tsonga) | Planned | Recorded DataJake narratives highlight prenasalised consonants; NVDA manual exports and GitHub prosody studies confirm tone + syllable timing before templates are generated. |

### Frequency, phoneme, and speech parameter backlog

- Regenerate [`docs/voice_parameter_report.md`](docs/voice_parameter_report.md) after importing Somali/Malagasy recordings so **Tone**, **Vocal range**, and **Inflection contour** slider defaults reflect DataJake spectral captures.
- Capture Ethiopic gemination frequency sweeps for Afar and Tigrinya via `python tools/report_voice_frequency_matrix.py` to ensure consonant bursts respect the 1 Hz–384 kHz clamps enforced by the WASAPI-aware EQ engine.
- Extend `phoneme_customizer.py` presets with Bantu prenasalisation cues (Kirundi, Setswana, Tsonga) and validate them by rerunning `python tools/report_language_progress.py --json docs/language_progress.json --markdown docs/language_progress.md --print`.

### Dictionary and corpus integration tasks

- Run `python tools/catalog_datajake_archives.py --json docs/archive_inventory.json --markdown docs/archive_inventory.md` after staging Afar, Somali, Kirundi, Setswana, Tsonga, and Sango `.dic`/`.lex` payloads so CodeQL can audit tone and gemination metadata.
- Update [`docs/language_research_index.md`](docs/language_research_index.md) and the JSON companion with the new Wikipedia bibliographies for Ge’ez orthography, Somali ATR harmony, Malagasy stress, and Bantu noun-class research; rerun `python tools/summarize_language_assets.py` to surface the provenance delta.
- Coordinate NVDA documentation snapshots for Ethiopic punctuation and Bantu hyphenation tables, then refresh `docs/nvda_update_recommendations.md` so offline builders reference the latest compatibility advice.

### Testing and packaging checkpoints

- Validate the Horn of Africa / Indian Ocean locales against NVDA alpha-52762 and `2025.3` stable builds mirrored via `python tools/audit_nvaccess_downloads.py` to confirm Ethiopic braille and Bantu tone cues read correctly.
- Capture unit test (`python -m unittest discover tests`) and offline build (`python build.py --insecure --no-download --output dist/eloquence.nvda-addon`) logs in pull requests to keep reproducibility high for contributors without release archives.
- Log sprint outcomes in `AGENTS.md`, noting which DataJake, Wikipedia, GitHub, and NVDA assets were consumed so future CodeQL or packaging drills can replay the integration without ambiguity.

## Pan-Atlantic and Indian Ocean diaspora sprint (October 2025 follow-up)

| ISO / tag | Script focus | Status | Notes |
| --- | --- | --- | --- |
| dv | Thaana (Dhivehi) | Researching | Wikipedia orthography diagrams, DataJake Qur’anic recitation dictionaries, and NVDA braille tables confirm right-to-left diacritics; GitHub transliteration helpers queued for Thaana ⇄ Latin toggles. |
| mt | Latin (Maltese) | Planned | Cached NVDA manual punctuation exports and DECtalk lexicons document emphatic consonants; DataJake `.lex` payloads staged to calibrate **Plosive impact** and **Tone size** sliders. |
| lo | Lao | Researching | Tone contour charts from Wikipedia pair with GitHub IPA converters and DataJake sermon recordings; NV Speech Player presets earmarked for five-level tone bands. |
| cy | Latin (Welsh) | Planned | Archived DECtalk mutation dictionaries and GitHub finite-state morphers guide lenition/eclipsis scheduling; NVDA braille manuals referenced for contracted forms. |
| br | Latin (Breton) | Planned | Wikipedia nasalisation notes and DataJake liturgical corpora align with GitHub stress analyzers to seed vowel harmony presets. |
| nus | Latin (Nuer) | Researching | DataJake scripture corpora, GitHub tone-tracking notebooks, and NV Speech Player captures map ATR harmony and breathy vowels; NVDA punctuation exports confirm apostrophe tone markers. |

### Frequency, phoneme, and speech parameter backlog

- Regenerate [`docs/voice_frequency_matrix.md`](voice_frequency_matrix.md) after staging Dhivehi and Lao spectral captures so Thaana plosives and Lao tone tiers map to WASAPI-clamped frequency bands.
- Add Celtic consonant mutation emphasis bands to `phoneme_customizer.py`, then rerun `python tools/report_language_progress.py --json docs/language_progress.json --markdown docs/language_progress.md --print` to surface lenition/eclipsis presets in the dashboards.
- Feed Nuer ATR harmony data into `voice_parameters.py` presets and validate the **Tone size**, **Scope depth**, and **Nasal balance** sliders by regenerating [`docs/voice_parameter_report.md`](voice_parameter_report.md).

### Dictionary and corpus integration tasks

- Update [`docs/language_research_index.md`](language_research_index.md) / `.json` with Dhivehi Thaana studies, Lao tone diagrams, Welsh/Breton mutation references, and Nuer tone research; rerun `python tools/summarize_language_assets.py --json docs/language_asset_summary.json --markdown docs/language_asset_summary.md --print` afterward.
- Stage Dhivehi `.dic`, Lao sermon lexicons, and Celtic mutation datasets in `eloquence_data/`, then re-run `python tools/catalog_datajake_archives.py --json docs/archive_inventory.json --markdown docs/archive_inventory.md` so CodeQL sees the provenance delta.
- Coordinate NV Access documentation audits for Thaana, Lao, Welsh, and Maltese manuals via `python tools/audit_nvaccess_downloads.py` followed by `python tools/check_nvda_updates.py` to keep punctuation guidance synchronised with packaging.

### Testing and packaging checkpoints

- Execute `python -m unittest discover tests` after seeding Thaana/Lao/Celtic assets to ensure the CLI reports and phoneme catalogues ingest the new metadata cleanly.
- Run `python build.py --insecure --no-download --output dist/eloquence.nvda-addon` to verify the add-on bundles right-to-left Thaana data and tone contour presets without internet access.
- Document each offline drill in `AGENTS.md`, including the refreshed Wikipedia/DataJake/GitHub/NVDA artefacts and regenerated Markdown/JSON reports.

## Saharan-to-Pacific bridging sprint (October 2025 continuation)

| ISO / tag | Script focus | Status | Notes |
| --- | --- | --- | --- |
| kab | Tifinagh & Latin (Kabyle) | Researching | Wikipedia consonant emphasis and vowel harmony data align with DataJake `.lex` payloads; GitHub Amazigh morphological analysers staged to map tri-consonantal roots while NVDA braille exports verify mixed-script punctuation. |
| tzm | Tifinagh & Latin (Central Atlas Tamazight) | Planned | Cached Afroasiatic family dossiers capture emphatic consonants and vowel centralisation; NV Speech Player presets queued to tune **Plosive impact** and **Tone** sliders before CodeQL-audited profile seeding. |
| bm | Latin (Bambara) | Researching | DataJake scripture recordings and GitHub tonal corpora inform ATR harmony and nasal vowel defaults; cross-reference [`docs/voice_parameter_report.md`](voice_parameter_report.md) for **Nasal balance**/**Macro volume** calibration. |
| tpi | Latin (Tok Pisin) | Planned | Wikipedia orthography and creole structure notes paired with DataJake sermon corpora; NVDA punctuation exports confirm English-derived digraph handling for tone-neutral presets. |
| fj | Latin (Fijian) | Researching | GitHub vowel-length datasets and DataJake hymn recordings guide frequency envelopes; NV Speech Player **Inflection contour** defaults validated against NVDA braille manuals. |
| mh | Latin (Marshallese) | Planned | Cached Wikipedia consonant inventory (including voiceless vowels) merged with GitHub orthography tables; DataJake hymn samples staged to map resonant frequency bands before packaging. |
| smj | Latin (Lule Sámi) | Researching | Wikipedia consonant gradation tables and GitHub finite-state analysers align with DataJake lexical payloads; NVDA alpha-52762 braille exports confirm diacritic handling. |

### Frequency, phoneme, and speech parameter backlog

- Regenerate [`docs/voice_frequency_matrix.md`](voice_frequency_matrix.md) after staging Fijian and Marshallese spectral captures to keep vowel length and glottal resonance aligned with NV Speech Player harmonics.
- Extend `phoneme_customizer.py` presets with Kabyle/Tamazight emphatic consonant cues and Bambara nasal harmony, then rerun `python tools/report_language_progress.py --json docs/language_progress.json --markdown docs/language_progress.md --print` to surface the new sliders in the dashboards.
- Update [`docs/voice_parameter_report.md`](voice_parameter_report.md) to reflect Bambara **Nasal balance**/**Macro volume** defaults and the creole tone-neutral presets queued for Tok Pisin.

### Dictionary and corpus integration tasks

- Append Kabyle, Tamazight, Bambara, Tok Pisin, Fijian, Marshallese, and Lule Sámi bibliographies to [`docs/language_research_index.md`](language_research_index.md) and rerun `python tools/summarize_language_assets.py --json docs/language_asset_summary.json --markdown docs/language_asset_summary.md --print` to record the provenance delta.
- Refresh `docs/archive_inventory.json` via `python tools/catalog_datajake_archives.py` after staging the new `.dic`/`.lex` payloads and hymn corpora so CodeQL automation validates sampling metadata and viability tags.
- Coordinate NV Access manual audits for Kabyle/Tamazight (French/Arabic translations), Bambara, and Tok Pisin by running `python tools/audit_nvaccess_downloads.py` followed by `python tools/check_nvda_updates.py` to keep punctuation and braille expectations synchronised with validated builds.

### Testing and packaging checkpoints

- Execute `python -m unittest discover tests` and `python tools/report_integration_scope.py --json docs/integration_scope.json --markdown docs/integration_scope.md --print` after updating these locales to ensure linkage matrices reflect the new profiles.
- Build with `python build.py --insecure --no-download --output dist/eloquence.nvda-addon` to confirm Tifinagh ⇄ Latin assets, creole frequency presets, and Sámi consonant gradation data package correctly without live downloads.
- Record sprint outcomes in `AGENTS.md`, referencing the refreshed Wikipedia/DataJake/GitHub/NVDA artefacts and regenerated dashboards so future offline drills can replay the Saharan/Pacific workflow.

## Philippine archipelago and Mainland Southeast Asia sprint (October 2025 extension)

| ISO / tag | Script focus | Status | Notes |
| --- | --- | --- | --- |
| ceb | Latin (Cebuano) | Researching | DataJake hymn `.dic` payloads catalogued alongside GitHub orthography converters; cached Wikipedia vowel harmony notes guide NV Speech Player **Tone size**/**Subtones** defaults before CodeQL-audited profile seeding. |
| hil | Latin (Hiligaynon) | Researching | Wikipedia stress and glottal stop notes combine with DataJake liturgical lexicons; GitHub syllable tokenisers drive NV Speech Player **Inflection contour** presets awaiting profile ingestion. |
| ilo | Latin (Ilocano) | Researching | DataJake radio news corpora and GitHub orthography datasets logged to validate glottal stop markers; Wikipedia vowel length notes align NV Speech Player **Tone size**/**Subtones** presets with Ilokano stress patterns. |
| pam | Latin (Kapampangan) | Planned | GitHub orthography converters and Wikipedia phonotactics underpin NVDA braille punctuation tests; DataJake bilingual hymn corpora logged to confirm glottal stop markers before generating Visayan-aligned profiles. |
| war | Latin (Waray-Waray) | Planned | Wikipedia stress and vowel length charts combined with DataJake scripture recordings; GitHub syllabifiers queued to validate glottal stop notation before refreshing NVDA braille exports. |
| hmn | Latin & Pahawh (Hmong Daw) | Researching | Wikipedia tone contour charts and GitHub tonal analysis notebooks paired with DataJake oral history recordings; NV Speech Player **Tone**, **Scope depth**, and **Whisper** sliders queued for validation via `docs/voice_frequency_matrix.md`. |
| lus | Latin (Mizo/Lushai) | Researching | Cached Wikipedia tone registers and GitHub tonal classifier notebooks paired with DataJake hymn archives; NV Speech Player **Tone**, **Scope depth**, and **Nasal balance** presets flagged for Mainland Southeast Asia validation. |

### Frequency, phoneme, and speech parameter backlog

- Rerun `python tools/report_voice_frequency_matrix.py --json docs/voice_frequency_matrix.json --markdown docs/voice_frequency_matrix.md --print` after staging Visayan and Hmong spectral captures so tone-level sliders reflect the newly catalogued vowel and nasal resonance cues.
- Update `voice_parameters.py` with Hmong/Mizo **Tone**, **Whisper**, and **Nasal balance** presets, then regenerate [`docs/voice_parameter_report.md`](voice_parameter_report.md) to surface the Mainland Southeast Asia defaults alongside existing African and Pacific additions.
- Extend `phoneme_customizer.py` presets with Visayan glottal stop emphasis bands and Mainland tone register annotations; validate the updates by running `python tools/report_language_progress.py --json docs/language_progress.json --markdown docs/language_progress.md --print`.

### Dictionary and corpus integration tasks

- Harvest Cebuano, Hiligaynon, Ilocano, Kapampangan, Waray, Hmong, and Mizo references from cached Wikipedia bibliographies into [`docs/language_research_index.md`](language_research_index.md) / `.json`, then rerun `python tools/summarize_language_assets.py --json docs/language_asset_summary.json --markdown docs/language_asset_summary.md --print` so provenance dashboards flag the new locales.
- Stage DataJake hymn/scripture `.dic` payloads for each locale in `eloquence_data/` and refresh `docs/archive_inventory.json` via `python tools/catalog_datajake_archives.py --json docs/archive_inventory.json --markdown docs/archive_inventory.md` so CodeQL notes audio-fidelity and viability tags.
- Mirror NVDA manual exports for Filipino, Cebuano, Kapampangan, and Waray documentation using `python tools/audit_nvaccess_downloads.py --roots releases/stable releases/2025.3 snapshots/alpha --max-depth 2 --limit-per-dir 12 --insecure --json docs/download_nvaccess_snapshot.json --markdown docs/download_nvaccess_snapshot.md`, then translate the delta into [`docs/nvda_update_recommendations.md`](nvda_update_recommendations.md).

### Testing and packaging checkpoints

- Execute `python -m unittest discover tests` after seeding the Visayan/Hmong datasets to confirm CLI reports absorb the expanded tone metadata.
- Build the add-on with `python build.py --insecure --no-download --output dist/eloquence.nvda-addon` to validate that glottal stop and tone register metadata package cleanly without live downloads.
- Append sprint notes to `AGENTS.md`, referencing refreshed Wikipedia/DataJake/GitHub/NVDA artefacts and regenerated dashboards so offline contributors can replay the Philippine/Mainland workflow.

## Adriatic and Balkan sprint (October 2025 follow-up)

| ISO / tag | Script focus | Status | Notes |
| --- | --- | --- | --- |
| sq | Latin (Albanian) | Researching | Wikipedia stress/vowel reduction tables cross-checked with GitHub Albanian morphological analysers and DataJake diaspora dictionaries; NVDA braille exports confirm ë/ç handling for both Gheg and Tosk presets. |
| bs | Latin (Bosnian) | Researching | Sarajevo news corpora from DataJake mirror Wikipedia pitch-accent research while GitHub lemmatisers validate ijekavian vs. ekavian toggles for NV Speech Player **Inflection contour** presets. |
| hr | Latin (Croatian) | Researching | Wikipedia four-way accent inventory paired with DataJake drama recordings and GitHub rhyme dictionaries to stage long/short falling patterns before regenerating frequency envelopes. |
| sr, sr-Latn | Cyrillic & Latin (Serbian) | Researching | Serbian National Corpus extracts align with Wikipedia palatalisation tables; DataJake `.lex` payloads and NVDA manuals anchor punctuation parity ahead of CodeQL-audited dual-script templates. |
| cnr | Latin (Montenegrin) | Planned | Cached Wikipedia orthography reforms merge with GitHub Montenegrin corpora to track ś/ź/ź́ phoneme demand; DataJake accent samples queued for validation. |
| sl | Latin (Slovene) | Researching | Wikipedia tonemic diacritic charts plus DataJake hymn inventories feed GitHub accent analyzers so NV Speech Player **Tone size** defaults capture circumflex vs. acute contrasts. |
| mk | Cyrillic (Macedonian) | Researching | Cached Wikipedia vowel reduction + schwa data align with DataJake broadcast lexicons; GitHub transliteration scripts under CodeQL review ensure Latin fallback mappings stay reversible. |

### Frequency, phoneme, and speech parameter backlog

- Re-run `python tools/report_voice_frequency_matrix.py --json docs/voice_frequency_matrix.json --markdown docs/voice_frequency_matrix.md --print` after capturing Bosnian/Croatian/Serbian vowel length recordings so NV Speech Player harmonics reflect four-accent contrasts.
- Extend `voice_parameters.py` with Albanian **Sibilant clarity** and Slovene **Tone size** presets, then regenerate [`docs/voice_parameter_report.md`](voice_parameter_report.md) to expose the Adriatic defaults alongside existing tone-rich locales.
- Update `phoneme_customizer.py` with palatalised alveolar cues for Serbian/Montenegrin and alveolo-palatal affricates for Slovene; validate via `python tools/report_language_progress.py --json docs/language_progress.json --markdown docs/language_progress.md --print`.

### Dictionary and corpus integration tasks

- Append Albanian, Bosnian, Croatian, Serbian, Montenegrin, Slovene, and Macedonian bibliographies to [`docs/language_research_index.md`](language_research_index.md) / `.json`, then rerun `python tools/summarize_language_assets.py --json docs/language_asset_summary.json --markdown docs/language_asset_summary.md --print` so provenance dashboards log the new ISO coverage.
- Stage DataJake `.dic`/`.lex` payloads for each locale in `eloquence_data/` and refresh `docs/archive_inventory.json` through `python tools/catalog_datajake_archives.py --json docs/archive_inventory.json --markdown docs/archive_inventory.md` to capture updated viability and audio-fidelity tags.
- Audit NV Access manuals for Macedonian, Serbian, Croatian, and Slovene using `python tools/audit_nvaccess_downloads.py --roots releases/stable releases/2025.3 snapshots/alpha --max-depth 2 --limit-per-dir 12 --insecure --json docs/download_nvaccess_snapshot.json --markdown docs/download_nvaccess_snapshot.md`, then translate severity changes via `python tools/check_nvda_updates.py --snapshot docs/download_nvaccess_snapshot.json --validated docs/validated_nvda_builds.json --manifest manifest.ini --markdown docs/nvda_update_recommendations.md --json docs/nvda_update_recommendations.json`.

### Testing and packaging checkpoints

- Execute `python -m unittest discover tests` once the Adriatic datasets land to confirm CLI dashboards absorb the four-accent logic.
- Build the add-on with `python build.py --insecure --no-download --output dist/eloquence.nvda-addon` so dual-script Serbian assets and Montenegrin diacritics package correctly without new releases.
- Log sprint outcomes in `AGENTS.md`, referencing refreshed Wikipedia/DataJake/GitHub/NVDA artefacts plus regenerated dashboards to preserve provenance for future offline drills.

