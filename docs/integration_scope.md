# Integration scope report

This report captures the current intersection between bundled voices, language
profiles, and phoneme inventories so Eloquence Reloaded contributors can spot
gaps before publishing a new NVDA add-on build.

## Quick stats

- **Voice templates**: 28 across 11 languages.
- **Language profiles**: 11 total, 11 with character coverage.
- **Phonemes**: 136 entries spanning 20 categories and 51 distinct IPA symbols.

## Voice templates by language

| Language | Normalised | Templates | Default profile references |
| --- | --- | ---: | --- |
| en-US | en-US | 18 | `en-us-basic`<br>`en-us-heritage` |
| ↳ Templates |  |  | `dectalk-beautiful-betty`<br>`dectalk-perfect-paul`<br>`dectalk-rough-rita`<br>`dectalk-whispering-wendy`<br>`eloquence-bhp-precision`<br>`eloquence-heritage-jaws-classic`<br>`eloquence-loquence-studio`<br>`eloquence-sapi4-eloq61-studio`<br>`eloquence-sapi4-viavoice-tracy`<br>`eloquence-sapi5-codefactory-balanced`<br>`eloquence-sapi5-viavoice-paul-xl`<br>`eloquence-window-eyes-expressive`<br>`espeak-en-us-bright`<br>`espeak-variant-espeak-variants-storm`<br>`nvspeechplayer-adam`<br>`nvspeechplayer-benjamin`<br>`nvspeechplayer-caleb`<br>`nvspeechplayer-david` |
| — | — | 1 | — |
| ↳ Templates |  |  | `espeak-variant-espeak-variants-alex` |
| de-DE | de-DE | 1 | `de-de-basic` |
| ↳ Templates |  |  | `espeak-de-precision` |
| en-GB | en-GB | 1 | `en-gb-basic` |
| ↳ Templates |  |  | `espeak-en-gb-clarity` |
| es-419 | es-419 | 1 | `es-419-basic` |
| ↳ Templates |  |  | `espeak-es-latin` |
| es-ES | es-ES | 1 | `es-es-basic` |
| ↳ Templates |  |  | `espeak-es-castilian` |
| fr-FR | fr-FR | 1 | `fr-fr-basic` |
| ↳ Templates |  |  | `espeak-fr-velvet` |
| hi-IN | hi-IN | 1 | `hi-in-basic` |
| ↳ Templates |  |  | `espeak-hi-dynamic` |
| it-IT | it-IT | 1 | `it-it-basic` |
| ↳ Templates |  |  | `espeak-it-expressive` |
| ja-JP | ja-JP | 1 | `ja-jp-basic` |
| ↳ Templates |  |  | `espeak-ja-melodic` |
| pt-BR | pt-BR | 1 | `pt-br-basic` |
| ↳ Templates |  |  | `espeak-pt-br-vibrant` |

## Voice tag distribution

| Tag | Templates |
| --- | ---: |
| `english` | 18 |
| `eloquence` | 8 |
| `dectalk` | 4 |
| `espeak` | 4 |
| `legacy` | 4 |
| `nvspeechplayer` | 4 |
| `sapi4` | 3 |
| `community` | 2 |
| `heritage` | 2 |
| `ibm` | 2 |
| `male` | 2 |
| `sapi5` | 2 |
| `spanish` | 2 |
| `studio` | 2 |
| `variant` | 2 |
| `viavoice` | 2 |
| `asia` | 1 |
| `blindhelp` | 1 |
| `brazil` | 1 |
| `breathy` | 1 |
| `bright` | 1 |
| `classic` | 1 |
| `codefactory` | 1 |
| `french` | 1 |
| `german` | 1 |
| `hindi` | 1 |
| `indic` | 1 |
| `italian` | 1 |
| `japanese` | 1 |
| `jaws` | 1 |
| `lang:en-us` | 1 |
| `lang:hi` | 1 |
| `lang:ja` | 1 |
| `latin` | 1 |
| `low` | 1 |
| `modern` | 1 |
| `portuguese` | 1 |
| `spain` | 1 |
| `uk` | 1 |
| `us` | 1 |
| `window-eyes` | 1 |

## Language profiles

| Profile | Language | Characters | Linked templates | Tags |
| --- | --- | ---: | --- | --- |
| de-de-basic (German – precise articulation) | de-DE | 11 | `espeak-de-precision` | `german`, `latin` |
| en-gb-basic (English (UK) – clipped clarity) | en-GB | 6 | `dectalk-beautiful-betty`<br>`dectalk-perfect-paul`<br>`dectalk-rough-rita`<br>`dectalk-whispering-wendy`<br>`eloquence-bhp-precision`<br>`eloquence-heritage-jaws-classic`<br>`eloquence-loquence-studio`<br>`eloquence-sapi4-eloq61-studio`<br>`eloquence-sapi4-viavoice-tracy`<br>`eloquence-sapi5-codefactory-balanced`<br>`eloquence-sapi5-viavoice-paul-xl`<br>`eloquence-window-eyes-expressive`<br>`espeak-en-gb-clarity`<br>`espeak-en-us-bright`<br>`espeak-variant-espeak-variants-storm`<br>`nvspeechplayer-adam`<br>`nvspeechplayer-benjamin`<br>`nvspeechplayer-caleb`<br>`nvspeechplayer-david` | `english`, `british` |
| en-us-heritage (English (US) – Heritage Eloquence) | en-US | 13 | `dectalk-beautiful-betty`<br>`dectalk-perfect-paul`<br>`dectalk-rough-rita`<br>`dectalk-whispering-wendy`<br>`eloquence-bhp-precision`<br>`eloquence-heritage-jaws-classic`<br>`eloquence-loquence-studio`<br>`eloquence-sapi4-eloq61-studio`<br>`eloquence-sapi4-viavoice-tracy`<br>`eloquence-sapi5-codefactory-balanced`<br>`eloquence-sapi5-viavoice-paul-xl`<br>`eloquence-window-eyes-expressive`<br>`espeak-en-gb-clarity`<br>`espeak-en-us-bright`<br>`espeak-variant-espeak-variants-storm`<br>`nvspeechplayer-adam`<br>`nvspeechplayer-benjamin`<br>`nvspeechplayer-caleb`<br>`nvspeechplayer-david` | `english`, `eloquence`, `heritage` |
| en-us-basic (English (US) – tactile vowels) | en-US | 8 | `dectalk-beautiful-betty`<br>`dectalk-perfect-paul`<br>`dectalk-rough-rita`<br>`dectalk-whispering-wendy`<br>`eloquence-bhp-precision`<br>`eloquence-heritage-jaws-classic`<br>`eloquence-loquence-studio`<br>`eloquence-sapi4-eloq61-studio`<br>`eloquence-sapi4-viavoice-tracy`<br>`eloquence-sapi5-codefactory-balanced`<br>`eloquence-sapi5-viavoice-paul-xl`<br>`eloquence-window-eyes-expressive`<br>`espeak-en-gb-clarity`<br>`espeak-en-us-bright`<br>`espeak-variant-espeak-variants-storm`<br>`nvspeechplayer-adam`<br>`nvspeechplayer-benjamin`<br>`nvspeechplayer-caleb`<br>`nvspeechplayer-david` | `english`, `latin`, `community` |
| es-419-basic (Spanish (LatAm) – sonorous core) | es-419 | 7 | `espeak-es-castilian`<br>`espeak-es-latin` | `spanish`, `latin` |
| es-es-basic (Spanish (Castilian) – crisp sibilants) | es-ES | 5 | `espeak-es-castilian`<br>`espeak-es-latin` | `spanish`, `castilian` |
| fr-fr-basic (French – nasal warmth) | fr-FR | 15 | `espeak-fr-velvet` | `french`, `latin` |
| hi-in-basic (Hindi – retroflex energy) | hi-IN | 5 | `espeak-hi-dynamic` | `hindi`, `indic`, `lang:hi` |
| it-it-basic (Italian – open vowels) | it-IT | 15 | `espeak-it-expressive` | `italian`, `latin` |
| ja-jp-basic (Japanese – mora rhythmic) | ja-JP | 5 | `espeak-ja-melodic` | `japanese`, `kana`, `lang:ja` |
| pt-br-basic (Portuguese (Brazil) – vibrant vowels) | pt-BR | 18 | `espeak-pt-br-vibrant` | `portuguese`, `latin` |

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
