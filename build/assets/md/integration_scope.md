# Integration scope report

This report captures the current intersection between bundled voices, language
profiles, and phoneme inventories so Eloquence Reloaded contributors can spot
gaps before publishing a new NVDA add-on build.

## Quick stats

- **Voice templates**: 70 across 53 languages.
- **Language profiles**: 53 total, 53 with character coverage.
- **Phonemes**: 136 entries spanning 20 categories and 51 distinct IPA symbols.

## Voice templates by language

| Language | Normalised | Templates | Default profile references |
| --- | --- | ---: | --- |
| en-US | en-US | 18 | `en-us-basic`<br>`en-us-heritage` |
| ↳ Templates |  |  | `dectalk-beautiful-betty`<br>`dectalk-perfect-paul`<br>`dectalk-rough-rita`<br>`dectalk-whispering-wendy`<br>`eloquence-bhp-precision`<br>`eloquence-heritage-jaws-classic`<br>`eloquence-loquence-studio`<br>`eloquence-sapi4-eloq61-studio`<br>`eloquence-sapi4-viavoice-tracy`<br>`eloquence-sapi5-codefactory-balanced`<br>`eloquence-sapi5-viavoice-paul-xl`<br>`eloquence-window-eyes-expressive`<br>`espeak-en-us-bright`<br>`espeak-variant-espeak-variants-storm`<br>`nvspeechplayer-adam`<br>`nvspeechplayer-benjamin`<br>`nvspeechplayer-caleb`<br>`nvspeechplayer-david` |
| — | — | 1 | — |
| ↳ Templates |  |  | `espeak-variant-espeak-variants-alex` |
| am | am | 1 | `am-et-seed` |
| ↳ Templates |  |  | `eloquence-seed-am-et` |
| ar | ar | 1 | `ar-msa-seed` |
| ↳ Templates |  |  | `eloquence-seed-ar-msa` |
| ar-EG | ar-EG | 1 | `ar-eg-seed` |
| ↳ Templates |  |  | `eloquence-seed-ar-eg` |
| bn | bn | 1 | `bn-bd-seed` |
| ↳ Templates |  |  | `eloquence-seed-bn-bd` |
| cs | cs | 1 | `cs-cz-seed` |
| ↳ Templates |  |  | `eloquence-seed-cs-cz` |
| da | da | 1 | `da-dk-seed` |
| ↳ Templates |  |  | `eloquence-seed-da-dk` |
| de-DE | de-DE | 1 | `de-de-basic` |
| ↳ Templates |  |  | `espeak-de-precision` |
| el | el | 1 | `el-gr-seed` |
| ↳ Templates |  |  | `eloquence-seed-el-gr` |
| en-GB | en-GB | 1 | `en-gb-basic` |
| ↳ Templates |  |  | `espeak-en-gb-clarity` |
| es-419 | es-419 | 1 | `es-419-basic` |
| ↳ Templates |  |  | `espeak-es-latin` |
| es-ES | es-ES | 1 | `es-es-basic` |
| ↳ Templates |  |  | `espeak-es-castilian` |
| fa | fa | 1 | `fa-ir-seed` |
| ↳ Templates |  |  | `eloquence-seed-fa-ir` |
| fi | fi | 1 | `fi-fi-seed` |
| ↳ Templates |  |  | `eloquence-seed-fi-fi` |
| fil | fil | 1 | `fil-ph-seed` |
| ↳ Templates |  |  | `eloquence-seed-fil-ph` |
| fr-FR | fr-FR | 1 | `fr-fr-basic` |
| ↳ Templates |  |  | `espeak-fr-velvet` |
| gu | gu | 1 | `gu-in-seed` |
| ↳ Templates |  |  | `eloquence-seed-gu-in` |
| ha | ha | 1 | `ha-ng-seed` |
| ↳ Templates |  |  | `eloquence-seed-ha-ng` |
| he | he | 1 | `he-il-seed` |
| ↳ Templates |  |  | `eloquence-seed-he-il` |
| hi-IN | hi-IN | 1 | `hi-in-basic` |
| ↳ Templates |  |  | `espeak-hi-dynamic` |
| id | id | 1 | `id-id-seed` |
| ↳ Templates |  |  | `eloquence-seed-id-id` |
| it-IT | it-IT | 1 | `it-it-basic` |
| ↳ Templates |  |  | `espeak-it-expressive` |
| ja-JP | ja-JP | 1 | `ja-jp-basic` |
| ↳ Templates |  |  | `espeak-ja-melodic` |
| km | km | 1 | `km-kh-seed` |
| ↳ Templates |  |  | `eloquence-seed-km-kh` |
| kn | kn | 1 | `kn-in-seed` |
| ↳ Templates |  |  | `eloquence-seed-kn-in` |
| ko | ko | 1 | `ko-kr-seed` |
| ↳ Templates |  |  | `eloquence-seed-ko-kr` |
| lo | lo | 1 | `lo-la-seed` |
| ↳ Templates |  |  | `eloquence-seed-lo-la` |
| ml | ml | 1 | `ml-in-seed` |
| ↳ Templates |  |  | `eloquence-seed-ml-in` |
| mr | mr | 1 | `mr-in-seed` |
| ↳ Templates |  |  | `eloquence-seed-mr-in` |
| ms | ms | 1 | `ms-my-seed` |
| ↳ Templates |  |  | `eloquence-seed-ms-my` |
| my | my | 1 | `my-mm-seed` |
| ↳ Templates |  |  | `eloquence-seed-my-mm` |
| nb | nb | 1 | `nb-no-seed` |
| ↳ Templates |  |  | `eloquence-seed-nb-no` |
| ne | ne | 1 | `ne-np-seed` |
| ↳ Templates |  |  | `eloquence-seed-ne-np` |
| nl | nl | 1 | `nl-nl-seed` |
| ↳ Templates |  |  | `eloquence-seed-nl-nl` |
| pa | pa | 1 | `pa-in-seed` |
| ↳ Templates |  |  | `eloquence-seed-pa-in` |
| pl | pl | 1 | `pl-pl-seed` |
| ↳ Templates |  |  | `eloquence-seed-pl-pl` |
| pt-BR | pt-BR | 1 | `pt-br-basic` |
| ↳ Templates |  |  | `espeak-pt-br-vibrant` |
| ru | ru | 1 | `ru-ru-seed` |
| ↳ Templates |  |  | `eloquence-seed-ru-ru` |
| si | si | 1 | `si-lk-seed` |
| ↳ Templates |  |  | `eloquence-seed-si-lk` |
| sv | sv | 1 | `sv-se-seed` |
| ↳ Templates |  |  | `eloquence-seed-sv-se` |
| sw | sw | 1 | `sw-ke-seed` |
| ↳ Templates |  |  | `eloquence-seed-sw-ke` |
| ta | ta | 1 | `ta-in-seed` |
| ↳ Templates |  |  | `eloquence-seed-ta-in` |
| te | te | 1 | `te-in-seed` |
| ↳ Templates |  |  | `eloquence-seed-te-in` |
| th | th | 1 | `th-th-seed` |
| ↳ Templates |  |  | `eloquence-seed-th-th` |
| tr | tr | 1 | `tr-tr-seed` |
| ↳ Templates |  |  | `eloquence-seed-tr-tr` |
| uk | uk | 1 | `uk-ua-seed` |
| ↳ Templates |  |  | `eloquence-seed-uk-ua` |
| ur | ur | 1 | `ur-pk-seed` |
| ↳ Templates |  |  | `eloquence-seed-ur-pk` |
| vi | vi | 1 | `vi-vn-seed` |
| ↳ Templates |  |  | `eloquence-seed-vi-vn` |
| yo | yo | 1 | `yo-ng-seed` |
| ↳ Templates |  |  | `eloquence-seed-yo-ng` |
| yue-Hant-HK | yue-Hant-HK | 1 | `yue-hk-seed` |
| ↳ Templates |  |  | `eloquence-seed-yue-hk` |
| zh-CN | zh-CN | 1 | `zh-cn-seed` |
| ↳ Templates |  |  | `eloquence-seed-zh-cn` |
| zu | zu | 1 | `zu-za-seed` |
| ↳ Templates |  |  | `eloquence-seed-zu-za` |

## Voice tag distribution

| Tag | Templates |
| --- | ---: |
| `eloquence` | 50 |
| `seed` | 42 |
| `english` | 18 |
| `dectalk` | 4 |
| `espeak` | 4 |
| `legacy` | 4 |
| `nvspeechplayer` | 4 |
| `sapi4` | 3 |
| `arabic` | 2 |
| `community` | 2 |
| `heritage` | 2 |
| `ibm` | 2 |
| `male` | 2 |
| `sapi5` | 2 |
| `spanish` | 2 |
| `studio` | 2 |
| `variant` | 2 |
| `viavoice` | 2 |
| `amharic` | 1 |
| `asia` | 1 |
| `bengali` | 1 |
| `blindhelp` | 1 |
| `brazil` | 1 |
| `breathy` | 1 |
| `bright` | 1 |
| `burmese` | 1 |
| `cantonese` | 1 |
| `classic` | 1 |
| `codefactory` | 1 |
| `czech` | 1 |
| `danish` | 1 |
| `dutch` | 1 |
| `egyptian` | 1 |
| `filipino` | 1 |
| `finnish` | 1 |
| `french` | 1 |
| `german` | 1 |
| `greek` | 1 |
| `gujarati` | 1 |
| `hausa` | 1 |
| `hebrew` | 1 |
| `hindi` | 1 |
| `indic` | 1 |
| `indonesian` | 1 |
| `italian` | 1 |
| `japanese` | 1 |
| `jaws` | 1 |
| `kannada` | 1 |
| `khmer` | 1 |
| `korean` | 1 |
| `lang:en-us` | 1 |
| `lang:hi` | 1 |
| `lang:ja` | 1 |
| `lao` | 1 |
| `latin` | 1 |
| `low` | 1 |
| `malay` | 1 |
| `malayalam` | 1 |
| `mandarin` | 1 |
| `marathi` | 1 |
| `modern` | 1 |
| `nepali` | 1 |
| `norwegian` | 1 |
| `persian` | 1 |
| `placeholder` | 1 |
| `polish` | 1 |
| `portuguese` | 1 |
| `punjabi` | 1 |
| `russian` | 1 |
| `sinhala` | 1 |
| `spain` | 1 |
| `swahili` | 1 |
| `swedish` | 1 |
| `tamil` | 1 |
| `telugu` | 1 |
| `thai` | 1 |
| `turkish` | 1 |
| `uk` | 1 |
| `ukrainian` | 1 |
| `urdu` | 1 |
| `us` | 1 |
| `vietnamese` | 1 |
| `window-eyes` | 1 |
| `yoruba` | 1 |
| `zulu` | 1 |

## Language profiles

| Profile | Language | Characters | Linked templates | Tags |
| --- | --- | ---: | --- | --- |
| am-et-seed (Amharic – ejective cadence) | am | 3 | `eloquence-seed-am-et` | `amharic`, `seed`, `lang:am` |
| ar-msa-seed (Arabic (Modern Standard) – emphatic backbone) | ar | 3 | `eloquence-seed-ar-eg`<br>`eloquence-seed-ar-msa` | `arabic`, `msa`, `seed`, `lang:ar` |
| ar-eg-seed (Arabic (Egyptian) – colloquial glide) | ar-EG | 3 | `eloquence-seed-ar-eg`<br>`eloquence-seed-ar-msa` | `arabic`, `egyptian`, `seed`, `lang:ar` |
| bn-bd-seed (Bengali – retroflex melody) | bn | 3 | `eloquence-seed-bn-bd` | `bengali`, `seed`, `lang:bn` |
| cs-cz-seed (Czech – trill precision) | cs | 3 | `eloquence-seed-cs-cz` | `czech`, `seed`, `lang:cs` |
| da-dk-seed (Danish – stød scaffolding) | da | 3 | `eloquence-seed-da-dk` | `danish`, `seed`, `lang:da` |
| de-de-basic (German – precise articulation) | de-DE | 11 | `espeak-de-precision` | `german`, `latin` |
| el-gr-seed (Greek – consonant balance) | el | 3 | `eloquence-seed-el-gr` | `greek`, `seed`, `lang:el` |
| en-gb-basic (English (UK) – clipped clarity) | en-GB | 6 | `dectalk-beautiful-betty`<br>`dectalk-perfect-paul`<br>`dectalk-rough-rita`<br>`dectalk-whispering-wendy`<br>`eloquence-bhp-precision`<br>`eloquence-heritage-jaws-classic`<br>`eloquence-loquence-studio`<br>`eloquence-sapi4-eloq61-studio`<br>`eloquence-sapi4-viavoice-tracy`<br>`eloquence-sapi5-codefactory-balanced`<br>`eloquence-sapi5-viavoice-paul-xl`<br>`eloquence-window-eyes-expressive`<br>`espeak-en-gb-clarity`<br>`espeak-en-us-bright`<br>`espeak-variant-espeak-variants-storm`<br>`nvspeechplayer-adam`<br>`nvspeechplayer-benjamin`<br>`nvspeechplayer-caleb`<br>`nvspeechplayer-david` | `english`, `british` |
| en-us-heritage (English (US) – Heritage Eloquence) | en-US | 13 | `dectalk-beautiful-betty`<br>`dectalk-perfect-paul`<br>`dectalk-rough-rita`<br>`dectalk-whispering-wendy`<br>`eloquence-bhp-precision`<br>`eloquence-heritage-jaws-classic`<br>`eloquence-loquence-studio`<br>`eloquence-sapi4-eloq61-studio`<br>`eloquence-sapi4-viavoice-tracy`<br>`eloquence-sapi5-codefactory-balanced`<br>`eloquence-sapi5-viavoice-paul-xl`<br>`eloquence-window-eyes-expressive`<br>`espeak-en-gb-clarity`<br>`espeak-en-us-bright`<br>`espeak-variant-espeak-variants-storm`<br>`nvspeechplayer-adam`<br>`nvspeechplayer-benjamin`<br>`nvspeechplayer-caleb`<br>`nvspeechplayer-david` | `english`, `eloquence`, `heritage` |
| en-us-basic (English (US) – tactile vowels) | en-US | 8 | `dectalk-beautiful-betty`<br>`dectalk-perfect-paul`<br>`dectalk-rough-rita`<br>`dectalk-whispering-wendy`<br>`eloquence-bhp-precision`<br>`eloquence-heritage-jaws-classic`<br>`eloquence-loquence-studio`<br>`eloquence-sapi4-eloq61-studio`<br>`eloquence-sapi4-viavoice-tracy`<br>`eloquence-sapi5-codefactory-balanced`<br>`eloquence-sapi5-viavoice-paul-xl`<br>`eloquence-window-eyes-expressive`<br>`espeak-en-gb-clarity`<br>`espeak-en-us-bright`<br>`espeak-variant-espeak-variants-storm`<br>`nvspeechplayer-adam`<br>`nvspeechplayer-benjamin`<br>`nvspeechplayer-caleb`<br>`nvspeechplayer-david` | `english`, `latin`, `community` |
| es-419-basic (Spanish (LatAm) – sonorous core) | es-419 | 7 | `espeak-es-castilian`<br>`espeak-es-latin` | `spanish`, `latin` |
| es-es-basic (Spanish (Castilian) – crisp sibilants) | es-ES | 5 | `espeak-es-castilian`<br>`espeak-es-latin` | `spanish`, `castilian` |
| fa-ir-seed (Persian (Farsi) – smooth ezafe) | fa | 3 | `eloquence-seed-fa-ir` | `persian`, `farsi`, `seed`, `lang:fa` |
| fi-fi-seed (Finnish – vowel length discipline) | fi | 3 | `eloquence-seed-fi-fi` | `finnish`, `seed`, `lang:fi` |
| fil-ph-seed (Filipino – Tagalog clarity) | fil | 3 | `eloquence-seed-fil-ph` | `filipino`, `tagalog`, `seed`, `lang:fil` |
| fr-fr-basic (French – nasal warmth) | fr-FR | 15 | `espeak-fr-velvet` | `french`, `latin` |
| gu-in-seed (Gujarati – vocalic resonances) | gu | 3 | `eloquence-seed-gu-in` | `gujarati`, `seed`, `lang:gu` |
| ha-ng-seed (Hausa – vibrant glottalic stops) | ha | 3 | `eloquence-seed-ha-ng` | `hausa`, `seed`, `lang:ha` |
| he-il-seed (Hebrew – modern articulation) | he | 3 | `eloquence-seed-he-il` | `hebrew`, `seed`, `lang:he` |
| hi-in-basic (Hindi – retroflex energy) | hi-IN | 5 | `espeak-hi-dynamic` | `hindi`, `indic`, `lang:hi` |
| id-id-seed (Indonesian – archipelago clarity) | id | 3 | `eloquence-seed-id-id` | `indonesian`, `seed`, `lang:id` |
| it-it-basic (Italian – open vowels) | it-IT | 15 | `espeak-it-expressive` | `italian`, `latin` |
| ja-jp-basic (Japanese – mora rhythmic) | ja-JP | 5 | `espeak-ja-melodic` | `japanese`, `kana`, `lang:ja` |
| km-kh-seed (Khmer – diphthong radiance) | km | 3 | `eloquence-seed-km-kh` | `khmer`, `seed`, `lang:km` |
| kn-in-seed (Kannada – gentle palatals) | kn | 3 | `eloquence-seed-kn-in` | `kannada`, `seed`, `lang:kn` |
| ko-kr-seed (Korean – fortis balance) | ko | 3 | `eloquence-seed-ko-kr` | `korean`, `seed`, `lang:ko` |
| lo-la-seed (Lao – tone class guidance) | lo | 3 | `eloquence-seed-lo-la` | `lao`, `seed`, `lang:lo` |
| ml-in-seed (Malayalam – retroflex waves) | ml | 3 | `eloquence-seed-ml-in` | `malayalam`, `seed`, `lang:ml` |
| mr-in-seed (Marathi – syllabic liquids) | mr | 3 | `eloquence-seed-mr-in` | `marathi`, `seed`, `lang:mr` |
| ms-my-seed (Malay – peninsular warmth) | ms | 3 | `eloquence-seed-ms-my` | `malay`, `seed`, `lang:ms` |
| my-mm-seed (Burmese – creaky tone balance) | my | 3 | `eloquence-seed-my-mm` | `burmese`, `seed`, `lang:my` |
| nb-no-seed (Norwegian (Bokmål) – tonal balance) | nb | 3 | `eloquence-seed-nb-no` | `norwegian`, `seed`, `lang:nb` |
| ne-np-seed (Nepali – Himalayan cadence) | ne | 3 | `eloquence-seed-ne-np` | `nepali`, `seed`, `lang:ne` |
| nl-nl-seed (Dutch – diphthong clarity) | nl | 3 | `eloquence-seed-nl-nl` | `dutch`, `seed`, `lang:nl` |
| pa-in-seed (Punjabi – tonal Gurmukhi) | pa | 3 | `eloquence-seed-pa-in` | `punjabi`, `seed`, `lang:pa` |
| pl-pl-seed (Polish – sibilant contrast) | pl | 3 | `eloquence-seed-pl-pl` | `polish`, `seed`, `lang:pl` |
| pt-br-basic (Portuguese (Brazil) – vibrant vowels) | pt-BR | 18 | `espeak-pt-br-vibrant` | `portuguese`, `latin` |
| ru-ru-seed (Russian – palatal richness) | ru | 3 | `eloquence-seed-ru-ru` | `russian`, `seed`, `lang:ru` |
| si-lk-seed (Sinhala – rounded cadence) | si | 3 | `eloquence-seed-si-lk` | `sinhala`, `seed`, `lang:si` |
| sv-se-seed (Swedish – pitch accent) | sv | 3 | `eloquence-seed-sv-se` | `swedish`, `seed`, `lang:sv` |
| sw-ke-seed (Swahili – coastal clarity) | sw | 3 | `eloquence-seed-sw-ke` | `swahili`, `seed`, `lang:sw` |
| ta-in-seed (Tamil – classical resonance) | ta | 3 | `eloquence-seed-ta-in` | `tamil`, `seed`, `lang:ta` |
| te-in-seed (Telugu – lyrical aspiration) | te | 3 | `eloquence-seed-te-in` | `telugu`, `seed`, `lang:te` |
| th-th-seed (Thai – tonal glide) | th | 3 | `eloquence-seed-th-th` | `thai`, `seed`, `lang:th` |
| tr-tr-seed (Turkish – vowel harmony) | tr | 3 | `eloquence-seed-tr-tr` | `turkish`, `seed`, `lang:tr` |
| uk-ua-seed (Ukrainian – bright palatals) | uk | 3 | `eloquence-seed-uk-ua` | `ukrainian`, `seed`, `lang:uk` |
| ur-pk-seed (Urdu – poetic glide) | ur | 3 | `eloquence-seed-ur-pk` | `urdu`, `seed`, `lang:ur` |
| vi-vn-seed (Vietnamese – six-tone brilliance) | vi | 3 | `eloquence-seed-vi-vn` | `vietnamese`, `seed`, `lang:vi` |
| yo-ng-seed (Yoruba – tonal resonance) | yo | 3 | `eloquence-seed-yo-ng` | `yoruba`, `seed`, `lang:yo` |
| yue-hk-seed (Chinese (Cantonese) – six-tone contour) | yue-Hant-HK | 3 | `eloquence-seed-yue-hk` | `cantonese`, `seed`, `lang:yue` |
| zh-cn-seed (Chinese (Mandarin) – tonal baseline) | zh-CN | 1 | `eloquence-seed-zh-cn` | `mandarin`, `seed`, `lang:zh` |
| zu-za-seed (Zulu – click-rich texture) | zu | 3 | `eloquence-seed-zu-za` | `zulu`, `seed`, `lang:zu` |

## Phoneme categories

| Category | Phonemes | Distinct IPA |
| --- | ---: | ---: |
| Stress Phonemes | 20 | 0 |
| SONORANTS | 19 | 7 |
| NVSpeechPlayer vowels | 15 | 15 |
| VOICED fricatives | 13 | 5 |
| UNVOICED fricatives | 12 | 4 |
| NASAL CONSONANTS | 8 | 4 |
| UNVOICED STOPS | 8 | 1 |
| Some default vowel definitions | 7 | 1 |
| VOICED STOPS | 7 | 1 |
| These each apply to a class of vowels | 6 | 0 |
| DECtalk core inventory | 4 | 4 |
| NVSpeechPlayer voiceless consonants | 4 | 4 |
| Syllablic consonants | 3 | 3 |
| NVSpeechPlayer affricates | 2 | 2 |
| NVSpeechPlayer voiced consonants | 2 | 2 |
| NVSpeechPlayer voiced stops | 2 | 2 |
| NVSpeechPlayer liquids | 1 | 1 |
| NVSpeechPlayer nasals | 1 | 1 |
| NVSpeechPlayer voiceless stops | 1 | 1 |
| Other sounds | 1 | 0 |

## Voice templates without a matching language profile

The following templates do not currently map to a bundled language profile.
Contributors can create new profiles or extend existing ones so NVDA users
receive contextual hints while experimenting with these presets.

- `espeak-variant-espeak-variants-alex`
