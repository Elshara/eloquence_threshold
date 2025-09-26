# Voice parameter coverage

* Generated: 2025-09-26T13:39:35Z
* Templates analysed: 70
* Languages represented: 53

## Parameter ranges

| Parameter | Range | Default | Step | Tags | Description |
| --- | --- | --- | --- | --- | --- |
| breathiness | 0 – 120 | 32 | 1 | texture | Adds aspiration to soften consonants. |
| emphasis | 0 – 200 | 100 | 1 | eq, nvspeechplayer, prosody | Boost or soften consonant attacks and vowel onsets to mirror how NV Speech Player emphasises foreground syllables. |
| gender | 0 – 1 | 0 | 1 | timbre | 0 = masculine tract target, 1 = feminine tract target. |
| headSize | 70 – 160 | 100 | 1 | formant | Formant scaling comparable to vocal tract length. |
| headSizeContour | 0 – 200 | 100 | 1 | eq, formant, size | Simulates shorter or longer vocal tracts by biasing the first three formants, mirroring NV Speech Player's head size macro. |
| inflection | 0 – 100 | 50 | 1 | prosody | Amount of pitch modulation between syllables. |
| inflectionContour | 0 – 200 | 100 | 1 | eq, inflection, prosody | Emphasises rising and falling transitions by shaping low-mid fundamentals and the 2–4 kHz glide band NV Speech Player uses for syllable inflection cues. |
| macroVolume | 0 – 200 | 100 | 1 | eq, loudness, mix | Blends pre-mix gain with broadband EQ so the voice can swell or sit back without clipping, echoing NV Speech Player's volume macros. |
| overtones | 0 – 200 | 100 | 1 | brightness, eq, harmonics | Adds sparkle or dampens sibilants by shaping the 6–16 kHz band used by NV Speech Player's frication models. |
| pitch | 40 – 160 | 100 | 1 | tone | Primary pitch target controlling overall brightness. |
| rate | 40 – 150 | 100 | 1 | timing | Base speed in words per minute mapped to Eloquence's internal range. |
| roughness | 0 – 120 | 40 | 1 | texture | Noise component balancing rasp versus clarity. |
| roughnessControl | 0 – 200 | 100 | 1 | eq, roughness, texture | Adds rasp or polishes brightness by boosting or cutting the 2.6–8.2 kHz band tied to NV Speech Player's roughness tables. |
| sampleRate | 8000 – 48000 | 22050 | 50 | output, quality | Output rate in Hertz after optional resampling. |
| scopeDepth | 0 – 200 | 100 | 1 | depth, eq, warmth | Controls how deep or shallow the voice feels by reshaping the upper-bass region present in NV Speech Player formants. |
| smoothness | 0 – 200 | 100 | 1 | eq, softness, texture | Controls how much high frequency noise is removed to mimic NV Speech Player's aspiration blending. |
| stress | 0 – 200 | 100 | 1 | eq, prosody, stress | Shapes the mid-high resonances that convey linguistic stress, mirroring NV Speech Player's intensity multipliers. |
| subtones | 0 – 200 | 100 | 1 | eq, harmonics, warmth | Boost or trim the 60–400 Hz band that defines chest resonance and NV Speech Player's low frequency shaping. |
| timbre | 0 – 200 | 100 | 1 | eq, formant, timbre | Balances lower formants against upper harmonics so the voice can sound darker or brighter without losing articulation. |
| tone | 0 – 200 | 100 | 1 | eq, harmonics, tone | Highlights the harmonic band responsible for tone colour, similar to NV Speech Player's cascade/parallel formant multipliers. |
| toneSize | 0 – 200 | 100 | 1 | eq, formant, size | Simulates smaller or larger resonant cavities by biasing the first three formants—akin to NV Speech Player's head size macro. |
| vocalLayers | 0 – 200 | 100 | 1 | eq, layering, texture | Controls the balance between fundamental energy and higher partials to simulate stacked voices or thinner single voices. |
| vocalRange | 0 – 200 | 100 | 1 | prosody, range | Expands or narrows the perceived vocal range by shaping both fundamentals and upper resonances. |
| volume | 50 – 100 | 80 | 1 | loudness | Output gain applied before NVDA's volume scaling. |
| whisper | 0 – 200 | 100 | 1 | eq, texture, whisper | Introduces or removes aspiration-style whisper components across the band limited by NV Speech Player's breath tables. |

## Parameter usage

| Parameter | Templates using it | Count |
| --- | --- | ---: |
| breathiness | dectalk-beautiful-betty, dectalk-perfect-paul, dectalk-rough-rita, dectalk-whispering-wendy, eloquence-bhp-precision, eloquence-heritage-jaws-classic, eloquence-loquence-studio, eloquence-sapi4-eloq61-studio, eloquence-sapi4-viavoice-tracy, eloquence-sapi5-codefactory-balanced, eloquence-sapi5-viavoice-paul-xl, eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, eloquence-window-eyes-expressive, espeak-de-precision, espeak-en-gb-clarity, espeak-en-us-bright, espeak-es-castilian, espeak-es-latin, espeak-fr-velvet, espeak-hi-dynamic, espeak-it-expressive, espeak-ja-melodic, espeak-pt-br-vibrant, espeak-variant-espeak-variants-alex, espeak-variant-espeak-variants-storm, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 70 |
| emphasis | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| gender | eloquence-bhp-precision, eloquence-heritage-jaws-classic, eloquence-loquence-studio, eloquence-sapi4-eloq61-studio, eloquence-sapi4-viavoice-tracy, eloquence-sapi5-codefactory-balanced, eloquence-sapi5-viavoice-paul-xl, eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, eloquence-window-eyes-expressive, espeak-de-precision, espeak-en-gb-clarity, espeak-en-us-bright, espeak-es-castilian, espeak-es-latin, espeak-fr-velvet, espeak-hi-dynamic, espeak-it-expressive, espeak-ja-melodic, espeak-pt-br-vibrant, espeak-variant-espeak-variants-alex, espeak-variant-espeak-variants-storm, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 66 |
| headSize | dectalk-beautiful-betty, dectalk-perfect-paul, dectalk-rough-rita, dectalk-whispering-wendy, eloquence-bhp-precision, eloquence-heritage-jaws-classic, eloquence-loquence-studio, eloquence-sapi4-eloq61-studio, eloquence-sapi4-viavoice-tracy, eloquence-sapi5-codefactory-balanced, eloquence-sapi5-viavoice-paul-xl, eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, eloquence-window-eyes-expressive, espeak-de-precision, espeak-en-gb-clarity, espeak-en-us-bright, espeak-es-castilian, espeak-es-latin, espeak-fr-velvet, espeak-hi-dynamic, espeak-it-expressive, espeak-ja-melodic, espeak-pt-br-vibrant, espeak-variant-espeak-variants-alex, espeak-variant-espeak-variants-storm, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 70 |
| headSizeContour | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| inflection | dectalk-beautiful-betty, dectalk-perfect-paul, dectalk-rough-rita, dectalk-whispering-wendy, eloquence-bhp-precision, eloquence-heritage-jaws-classic, eloquence-loquence-studio, eloquence-sapi4-eloq61-studio, eloquence-sapi4-viavoice-tracy, eloquence-sapi5-codefactory-balanced, eloquence-sapi5-viavoice-paul-xl, eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, eloquence-window-eyes-expressive, espeak-de-precision, espeak-en-gb-clarity, espeak-en-us-bright, espeak-es-castilian, espeak-es-latin, espeak-fr-velvet, espeak-hi-dynamic, espeak-it-expressive, espeak-ja-melodic, espeak-pt-br-vibrant, espeak-variant-espeak-variants-alex, espeak-variant-espeak-variants-storm, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 70 |
| inflectionContour | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| macroVolume | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| overtones | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| pitch | dectalk-beautiful-betty, dectalk-perfect-paul, dectalk-rough-rita, dectalk-whispering-wendy, eloquence-bhp-precision, eloquence-heritage-jaws-classic, eloquence-loquence-studio, eloquence-sapi4-eloq61-studio, eloquence-sapi4-viavoice-tracy, eloquence-sapi5-codefactory-balanced, eloquence-sapi5-viavoice-paul-xl, eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, eloquence-window-eyes-expressive, espeak-de-precision, espeak-en-gb-clarity, espeak-en-us-bright, espeak-es-castilian, espeak-es-latin, espeak-fr-velvet, espeak-hi-dynamic, espeak-it-expressive, espeak-ja-melodic, espeak-pt-br-vibrant, espeak-variant-espeak-variants-alex, espeak-variant-espeak-variants-storm, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 70 |
| rate | dectalk-beautiful-betty, dectalk-perfect-paul, dectalk-rough-rita, dectalk-whispering-wendy, eloquence-bhp-precision, eloquence-heritage-jaws-classic, eloquence-loquence-studio, eloquence-sapi4-eloq61-studio, eloquence-sapi4-viavoice-tracy, eloquence-sapi5-codefactory-balanced, eloquence-sapi5-viavoice-paul-xl, eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, eloquence-window-eyes-expressive, espeak-de-precision, espeak-en-gb-clarity, espeak-en-us-bright, espeak-es-castilian, espeak-es-latin, espeak-fr-velvet, espeak-hi-dynamic, espeak-it-expressive, espeak-ja-melodic, espeak-pt-br-vibrant, espeak-variant-espeak-variants-alex, espeak-variant-espeak-variants-storm, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 70 |
| roughness | dectalk-beautiful-betty, dectalk-perfect-paul, dectalk-rough-rita, dectalk-whispering-wendy, eloquence-bhp-precision, eloquence-heritage-jaws-classic, eloquence-loquence-studio, eloquence-sapi4-eloq61-studio, eloquence-sapi4-viavoice-tracy, eloquence-sapi5-codefactory-balanced, eloquence-sapi5-viavoice-paul-xl, eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, eloquence-window-eyes-expressive, espeak-de-precision, espeak-en-gb-clarity, espeak-en-us-bright, espeak-es-castilian, espeak-es-latin, espeak-fr-velvet, espeak-hi-dynamic, espeak-it-expressive, espeak-ja-melodic, espeak-pt-br-vibrant, espeak-variant-espeak-variants-alex, espeak-variant-espeak-variants-storm, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 70 |
| roughnessControl | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| sampleRate | – | 0 |
| scopeDepth | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| smoothness | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| stress | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| subtones | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| timbre | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| tone | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| toneSize | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| vocalLayers | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| vocalRange | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |
| volume | dectalk-beautiful-betty, dectalk-perfect-paul, dectalk-rough-rita, dectalk-whispering-wendy, eloquence-bhp-precision, eloquence-heritage-jaws-classic, eloquence-loquence-studio, eloquence-sapi4-eloq61-studio, eloquence-sapi4-viavoice-tracy, eloquence-sapi5-codefactory-balanced, eloquence-sapi5-viavoice-paul-xl, eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, eloquence-window-eyes-expressive, espeak-de-precision, espeak-en-gb-clarity, espeak-en-us-bright, espeak-es-castilian, espeak-es-latin, espeak-fr-velvet, espeak-hi-dynamic, espeak-it-expressive, espeak-ja-melodic, espeak-pt-br-vibrant, espeak-variant-espeak-variants-alex, espeak-variant-espeak-variants-storm, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 70 |
| whisper | eloquence-seed-am-et, eloquence-seed-ar-eg, eloquence-seed-ar-msa, eloquence-seed-bn-bd, eloquence-seed-cs-cz, eloquence-seed-da-dk, eloquence-seed-el-gr, eloquence-seed-fa-ir, eloquence-seed-fi-fi, eloquence-seed-fil-ph, eloquence-seed-gu-in, eloquence-seed-ha-ng, eloquence-seed-he-il, eloquence-seed-id-id, eloquence-seed-km-kh, eloquence-seed-kn-in, eloquence-seed-ko-kr, eloquence-seed-lo-la, eloquence-seed-ml-in, eloquence-seed-mr-in, eloquence-seed-ms-my, eloquence-seed-my-mm, eloquence-seed-nb-no, eloquence-seed-ne-np, eloquence-seed-nl-nl, eloquence-seed-pa-in, eloquence-seed-pl-pl, eloquence-seed-ru-ru, eloquence-seed-si-lk, eloquence-seed-sv-se, eloquence-seed-sw-ke, eloquence-seed-ta-in, eloquence-seed-te-in, eloquence-seed-th-th, eloquence-seed-tr-tr, eloquence-seed-uk-ua, eloquence-seed-ur-pk, eloquence-seed-vi-vn, eloquence-seed-yo-ng, eloquence-seed-yue-hk, eloquence-seed-zh-cn, eloquence-seed-zu-za, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 46 |

## Language coverage

| Language | Templates | Count | Tags |
| --- | --- | ---: | --- |
| am | eloquence-seed-am-et | 1 | amharic, eloquence, seed |
| ar | eloquence-seed-ar-msa | 1 | arabic, eloquence, placeholder, seed |
| ar-EG | eloquence-seed-ar-eg | 1 | arabic, egyptian, eloquence, seed |
| bn | eloquence-seed-bn-bd | 1 | bengali, eloquence, seed |
| cs | eloquence-seed-cs-cz | 1 | czech, eloquence, seed |
| da | eloquence-seed-da-dk | 1 | danish, eloquence, seed |
| de-DE | espeak-de-precision | 1 | german |
| el | eloquence-seed-el-gr | 1 | eloquence, greek, seed |
| en-GB | espeak-en-gb-clarity | 1 | community, english, uk |
| en-US | dectalk-beautiful-betty, dectalk-perfect-paul, dectalk-rough-rita, dectalk-whispering-wendy, eloquence-bhp-precision, eloquence-heritage-jaws-classic, eloquence-loquence-studio, eloquence-sapi4-eloq61-studio, eloquence-sapi4-viavoice-tracy, eloquence-sapi5-codefactory-balanced, eloquence-sapi5-viavoice-paul-xl, eloquence-window-eyes-expressive, espeak-en-us-bright, espeak-variant-espeak-variants-storm, nvspeechplayer-adam, nvspeechplayer-benjamin, nvspeechplayer-caleb, nvspeechplayer-david | 18 | blindhelp, breathy, bright, classic, codefactory, community, dectalk, eloquence, english, espeak, heritage, ibm, jaws, lang:en-us, legacy, low, male, modern, nvspeechplayer, sapi4, sapi5, studio, us, variant, viavoice, window-eyes |
| es-419 | espeak-es-latin | 1 | latin, spanish |
| es-ES | espeak-es-castilian | 1 | spain, spanish |
| fa | eloquence-seed-fa-ir | 1 | eloquence, persian, seed |
| fi | eloquence-seed-fi-fi | 1 | eloquence, finnish, seed |
| fil | eloquence-seed-fil-ph | 1 | eloquence, filipino, seed |
| fr-FR | espeak-fr-velvet | 1 | french |
| gu | eloquence-seed-gu-in | 1 | eloquence, gujarati, seed |
| ha | eloquence-seed-ha-ng | 1 | eloquence, hausa, seed |
| he | eloquence-seed-he-il | 1 | eloquence, hebrew, seed |
| hi-IN | espeak-hi-dynamic | 1 | espeak, hindi, indic, lang:hi |
| id | eloquence-seed-id-id | 1 | eloquence, indonesian, seed |
| it-IT | espeak-it-expressive | 1 | italian |
| ja-JP | espeak-ja-melodic | 1 | asia, espeak, japanese, lang:ja |
| km | eloquence-seed-km-kh | 1 | eloquence, khmer, seed |
| kn | eloquence-seed-kn-in | 1 | eloquence, kannada, seed |
| ko | eloquence-seed-ko-kr | 1 | eloquence, korean, seed |
| lo | eloquence-seed-lo-la | 1 | eloquence, lao, seed |
| ml | eloquence-seed-ml-in | 1 | eloquence, malayalam, seed |
| mr | eloquence-seed-mr-in | 1 | eloquence, marathi, seed |
| ms | eloquence-seed-ms-my | 1 | eloquence, malay, seed |
| my | eloquence-seed-my-mm | 1 | burmese, eloquence, seed |
| nb | eloquence-seed-nb-no | 1 | eloquence, norwegian, seed |
| ne | eloquence-seed-ne-np | 1 | eloquence, nepali, seed |
| nl | eloquence-seed-nl-nl | 1 | dutch, eloquence, seed |
| pa | eloquence-seed-pa-in | 1 | eloquence, punjabi, seed |
| pl | eloquence-seed-pl-pl | 1 | eloquence, polish, seed |
| pt-BR | espeak-pt-br-vibrant | 1 | brazil, portuguese |
| ru | eloquence-seed-ru-ru | 1 | eloquence, russian, seed |
| si | eloquence-seed-si-lk | 1 | eloquence, seed, sinhala |
| sv | eloquence-seed-sv-se | 1 | eloquence, seed, swedish |
| sw | eloquence-seed-sw-ke | 1 | eloquence, seed, swahili |
| ta | eloquence-seed-ta-in | 1 | eloquence, seed, tamil |
| te | eloquence-seed-te-in | 1 | eloquence, seed, telugu |
| th | eloquence-seed-th-th | 1 | eloquence, seed, thai |
| tr | eloquence-seed-tr-tr | 1 | eloquence, seed, turkish |
| uk | eloquence-seed-uk-ua | 1 | eloquence, seed, ukrainian |
| unspecified | espeak-variant-espeak-variants-alex | 1 | espeak, male, variant |
| ur | eloquence-seed-ur-pk | 1 | eloquence, seed, urdu |
| vi | eloquence-seed-vi-vn | 1 | eloquence, seed, vietnamese |
| yo | eloquence-seed-yo-ng | 1 | eloquence, seed, yoruba |
| yue-Hant-HK | eloquence-seed-yue-hk | 1 | cantonese, eloquence, seed |
| zh-CN | eloquence-seed-zh-cn | 1 | eloquence, mandarin, seed |
| zu | eloquence-seed-zu-za | 1 | eloquence, seed, zulu |

## Templates

### dectalk-perfect-paul – DECtalk Perfect Paul

* Language: en-US
* Default language profile: en-us-basic
* Tags: dectalk, legacy, english
* Parameters:
  * rate: 112
  * pitch: 96
  * inflection: 42
  * headSize: 126
  * roughness: 24
  * breathiness: 18
  * volume: 90
* Extras:
  * reference: dt51
  * synthesizer: dectalk

### dectalk-beautiful-betty – DECtalk Beautiful Betty

* Language: en-US
* Default language profile: en-us-basic
* Tags: dectalk, legacy, english
* Parameters:
  * rate: 108
  * pitch: 124
  * inflection: 54
  * headSize: 110
  * roughness: 18
  * breathiness: 34
  * volume: 92
* Extras:
  * reference: FonixTalk
  * synthesizer: dectalk

### dectalk-rough-rita – DECtalk Rough Rita

* Language: en-US
* Default language profile: en-us-basic
* Tags: dectalk, legacy, english
* Parameters:
  * rate: 104
  * pitch: 92
  * inflection: 36
  * headSize: 134
  * roughness: 46
  * breathiness: 26
  * volume: 94
* Extras:
  * reference: dt51
  * synthesizer: dectalk

### dectalk-whispering-wendy – DECtalk Whispering Wendy

* Language: en-US
* Default language profile: en-us-basic
* Tags: dectalk, legacy, english
* Parameters:
  * rate: 100
  * pitch: 118
  * inflection: 48
  * headSize: 116
  * roughness: 20
  * breathiness: 44
  * volume: 88
* Extras:
  * reference: FonixTalk
  * synthesizer: dectalk

### espeak-en-us-bright – English (US) bright

* Language: en-US
* Default language profile: en-us-basic
* Tags: english, us, community
* Parameters:
  * rate: 118
  * pitch: 112
  * inflection: 56
  * headSize: 128
  * roughness: 36
  * breathiness: 28
  * volume: 90
  * gender: 0

### espeak-en-gb-clarity – English (UK) clarity

* Language: en-GB
* Default language profile: en-gb-basic
* Tags: english, uk, community
* Parameters:
  * rate: 112
  * pitch: 98
  * inflection: 48
  * headSize: 122
  * roughness: 32
  * breathiness: 24
  * volume: 92
  * gender: 0

### espeak-es-latin – Spanish (Latin America)

* Language: es-419
* Default language profile: es-419-basic
* Tags: spanish, latin
* Parameters:
  * rate: 116
  * pitch: 104
  * inflection: 64
  * headSize: 134
  * roughness: 34
  * breathiness: 26
  * volume: 88
  * gender: 0

### espeak-es-castilian – Spanish (Castilian)

* Language: es-ES
* Default language profile: es-es-basic
* Tags: spanish, spain
* Parameters:
  * rate: 108
  * pitch: 102
  * inflection: 70
  * headSize: 130
  * roughness: 30
  * breathiness: 24
  * volume: 90
  * gender: 0

### espeak-fr-velvet – French velvety

* Language: fr-FR
* Default language profile: fr-fr-basic
* Tags: french
* Parameters:
  * rate: 106
  * pitch: 96
  * inflection: 58
  * headSize: 140
  * roughness: 28
  * breathiness: 32
  * volume: 86
  * gender: 0

### espeak-de-precision – German precision

* Language: de-DE
* Default language profile: de-de-basic
* Tags: german
* Parameters:
  * rate: 114
  * pitch: 94
  * inflection: 46
  * headSize: 124
  * roughness: 26
  * breathiness: 20
  * volume: 93
  * gender: 0

### espeak-it-expressive – Italian expressive

* Language: it-IT
* Default language profile: it-it-basic
* Tags: italian
* Parameters:
  * rate: 110
  * pitch: 108
  * inflection: 66
  * headSize: 126
  * roughness: 30
  * breathiness: 34
  * volume: 89
  * gender: 0

### espeak-pt-br-vibrant – Portuguese (Brazil) vibrant

* Language: pt-BR
* Default language profile: pt-br-basic
* Tags: portuguese, brazil
* Parameters:
  * rate: 112
  * pitch: 100
  * inflection: 60
  * headSize: 132
  * roughness: 32
  * breathiness: 30
  * volume: 92
  * gender: 0

### espeak-hi-dynamic – Hindi dynamic clarity

* Language: hi-IN
* Default language profile: hi-in-basic
* Tags: hindi, lang:hi, indic, espeak
* Parameters:
  * rate: 108
  * pitch: 112
  * inflection: 60
  * headSize: 118
  * roughness: 24
  * breathiness: 34
  * volume: 92
  * gender: 0

### espeak-ja-melodic – Japanese melodic

* Language: ja-JP
* Default language profile: ja-jp-basic
* Tags: japanese, lang:ja, espeak, asia
* Parameters:
  * rate: 112
  * pitch: 126
  * inflection: 48
  * headSize: 104
  * roughness: 20
  * breathiness: 26
  * volume: 88
  * gender: 0

### eloquence-seed-ar-msa – Eloquence seed – Arabic (MSA)

* Language: ar
* Default language profile: ar-msa-seed
* Tags: eloquence, seed, arabic, placeholder
* Parameters:
  * rate: 100
  * pitch: 96
  * inflection: 60
  * headSize: 118
  * roughness: 24
  * breathiness: 18
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 108
  * tone: 96
  * vocalLayers: 104
  * overtones: 92
  * subtones: 110
  * vocalRange: 102
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-ar-eg – Eloquence seed – Arabic (Egyptian)

* Language: ar-EG
* Default language profile: ar-eg-seed
* Tags: eloquence, seed, arabic, egyptian
* Parameters:
  * rate: 106
  * pitch: 108
  * inflection: 58
  * headSize: 110
  * roughness: 20
  * breathiness: 26
  * volume: 92
  * gender: 1
  * emphasis: 112
  * stress: 100
  * timbre: 100
  * tone: 104
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 100
  * whisper: 112
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 108
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-fa-ir – Eloquence seed – Persian

* Language: fa
* Default language profile: fa-ir-seed
* Tags: eloquence, seed, persian
* Parameters:
  * rate: 98
  * pitch: 114
  * inflection: 60
  * headSize: 110
  * roughness: 20
  * breathiness: 28
  * volume: 92
  * gender: 1
  * emphasis: 100
  * stress: 100
  * timbre: 112
  * tone: 110
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 118
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-ur-pk – Eloquence seed – Urdu

* Language: ur
* Default language profile: ur-pk-seed
* Tags: eloquence, seed, urdu
* Parameters:
  * rate: 94
  * pitch: 112
  * inflection: 64
  * headSize: 116
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 116
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 100
  * subtones: 112
  * vocalRange: 100
  * smoothness: 100
  * whisper: 108
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 108
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-he-il – Eloquence seed – Hebrew

* Language: he
* Default language profile: he-il-seed
* Tags: eloquence, seed, hebrew
* Parameters:
  * rate: 104
  * pitch: 118
  * inflection: 56
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 120
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 116
  * subtones: 100
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 104
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-am-et – Eloquence seed – Amharic

* Language: am
* Default language profile: am-et-seed
* Tags: eloquence, seed, amharic
* Parameters:
  * rate: 92
  * pitch: 116
  * inflection: 68
  * headSize: 110
  * roughness: 22
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 126
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 108
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 112
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-ha-ng – Eloquence seed – Hausa

* Language: ha
* Default language profile: ha-ng-seed
* Tags: eloquence, seed, hausa
* Parameters:
  * rate: 104
  * pitch: 122
  * inflection: 70
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 124
  * stress: 100
  * timbre: 100
  * tone: 128
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 110
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-sw-ke – Eloquence seed – Swahili

* Language: sw
* Default language profile: sw-ke-seed
* Tags: eloquence, seed, swahili
* Parameters:
  * rate: 108
  * pitch: 120
  * inflection: 54
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 112
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 106
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 120
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-yo-ng – Eloquence seed – Yoruba

* Language: yo
* Default language profile: yo-ng-seed
* Tags: eloquence, seed, yoruba
* Parameters:
  * rate: 100
  * pitch: 126
  * inflection: 78
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 136
  * vocalLayers: 100
  * overtones: 100
  * subtones: 116
  * vocalRange: 118
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 124
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-zu-za – Eloquence seed – Zulu

* Language: zu
* Default language profile: zu-za-seed
* Tags: eloquence, seed, zulu
* Parameters:
  * rate: 102
  * pitch: 116
  * inflection: 68
  * headSize: 110
  * roughness: 26
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 108
  * overtones: 128
  * subtones: 100
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 120
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-zh-cn – Eloquence seed – Mandarin

* Language: zh-CN
* Default language profile: zh-cn-seed
* Tags: eloquence, seed, mandarin
* Parameters:
  * rate: 112
  * pitch: 124
  * inflection: 80
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 138
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 122
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 110
  * toneSize: 126
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-yue-hk – Eloquence seed – Cantonese

* Language: yue-Hant-HK
* Default language profile: yue-hk-seed
* Tags: eloquence, seed, cantonese
* Parameters:
  * rate: 116
  * pitch: 130
  * inflection: 88
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 142
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 112
  * toneSize: 130
  * scopeDepth: 114
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-ko-kr – Eloquence seed – Korean

* Language: ko
* Default language profile: ko-kr-seed
* Tags: eloquence, seed, korean
* Parameters:
  * rate: 108
  * pitch: 118
  * inflection: 72
  * headSize: 114
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 128
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 124
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 116
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-vi-vn – Eloquence seed – Vietnamese

* Language: vi
* Default language profile: vi-vn-seed
* Tags: eloquence, seed, vietnamese
* Parameters:
  * rate: 118
  * pitch: 134
  * inflection: 90
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 144
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 126
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 132
  * scopeDepth: 110
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-th-th – Eloquence seed – Thai

* Language: th
* Default language profile: th-th-seed
* Tags: eloquence, seed, thai
* Parameters:
  * rate: 112
  * pitch: 128
  * inflection: 84
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 140
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 112
  * toneSize: 128
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-id-id – Eloquence seed – Indonesian

* Language: id
* Default language profile: id-id-seed
* Tags: eloquence, seed, indonesian
* Parameters:
  * rate: 110
  * pitch: 118
  * inflection: 60
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 108
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 118
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-ms-my – Eloquence seed – Malay

* Language: ms
* Default language profile: ms-my-seed
* Tags: eloquence, seed, malay
* Parameters:
  * rate: 106
  * pitch: 116
  * inflection: 58
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 116
  * whisper: 112
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-fil-ph – Eloquence seed – Filipino

* Language: fil
* Default language profile: fil-ph-seed
* Tags: eloquence, seed, filipino
* Parameters:
  * rate: 108
  * pitch: 120
  * inflection: 62
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 114
  * stress: 100
  * timbre: 100
  * tone: 108
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 120
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-bn-bd – Eloquence seed – Bengali

* Language: bn
* Default language profile: bn-bd-seed
* Tags: eloquence, seed, bengali
* Parameters:
  * rate: 100
  * pitch: 122
  * inflection: 66
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 118
  * subtones: 112
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 116
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-ta-in – Eloquence seed – Tamil

* Language: ta
* Default language profile: ta-in-seed
* Tags: eloquence, seed, tamil
* Parameters:
  * rate: 94
  * pitch: 114
  * inflection: 58
  * headSize: 118
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 124
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 100
  * subtones: 118
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 120
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-te-in – Eloquence seed – Telugu

* Language: te
* Default language profile: te-in-seed
* Tags: eloquence, seed, telugu
* Parameters:
  * rate: 96
  * pitch: 118
  * inflection: 62
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 100
  * subtones: 114
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 112
  * toneSize: 100
  * scopeDepth: 116
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-ml-in – Eloquence seed – Malayalam

* Language: ml
* Default language profile: ml-in-seed
* Tags: eloquence, seed, malayalam
* Parameters:
  * rate: 92
  * pitch: 112
  * inflection: 58
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 100
  * subtones: 120
  * vocalRange: 100
  * smoothness: 120
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 122
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-kn-in – Eloquence seed – Kannada

* Language: kn
* Default language profile: kn-in-seed
* Tags: eloquence, seed, kannada
* Parameters:
  * rate: 100
  * pitch: 116
  * inflection: 60
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 108
  * vocalLayers: 100
  * overtones: 100
  * subtones: 114
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 118
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-mr-in – Eloquence seed – Marathi

* Language: mr
* Default language profile: mr-in-seed
* Tags: eloquence, seed, marathi
* Parameters:
  * rate: 100
  * pitch: 118
  * inflection: 64
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 100
  * subtones: 116
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 118
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-gu-in – Eloquence seed – Gujarati

* Language: gu
* Default language profile: gu-in-seed
* Tags: eloquence, seed, gujarati
* Parameters:
  * rate: 102
  * pitch: 120
  * inflection: 62
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 100
  * subtones: 116
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 116
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-pa-in – Eloquence seed – Punjabi

* Language: pa
* Default language profile: pa-in-seed
* Tags: eloquence, seed, punjabi
* Parameters:
  * rate: 104
  * pitch: 126
  * inflection: 70
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 132
  * vocalLayers: 100
  * overtones: 100
  * subtones: 118
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 118
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-si-lk – Eloquence seed – Sinhala

* Language: si
* Default language profile: si-lk-seed
* Tags: eloquence, seed, sinhala
* Parameters:
  * rate: 96
  * pitch: 118
  * inflection: 58
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 116
  * subtones: 114
  * vocalRange: 100
  * smoothness: 118
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-km-kh – Eloquence seed – Khmer

* Language: km
* Default language profile: km-kh-seed
* Tags: eloquence, seed, khmer
* Parameters:
  * rate: 110
  * pitch: 120
  * inflection: 62
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 112
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 118
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 112
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-my-mm – Eloquence seed – Burmese

* Language: my
* Default language profile: my-mm-seed
* Tags: eloquence, seed, burmese
* Parameters:
  * rate: 104
  * pitch: 122
  * inflection: 76
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 132
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 100
  * whisper: 116
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 120
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-lo-la – Eloquence seed – Lao

* Language: lo
* Default language profile: lo-la-seed
* Tags: eloquence, seed, lao
* Parameters:
  * rate: 110
  * pitch: 126
  * inflection: 82
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 136
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 110
  * toneSize: 122
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-ne-np – Eloquence seed – Nepali

* Language: ne
* Default language profile: ne-np-seed
* Tags: eloquence, seed, nepali
* Parameters:
  * rate: 102
  * pitch: 120
  * inflection: 66
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 120
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 100
  * subtones: 112
  * vocalRange: 100
  * smoothness: 118
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-ru-ru – Eloquence seed – Russian

* Language: ru
* Default language profile: ru-ru-seed
* Tags: eloquence, seed, russian
* Parameters:
  * rate: 104
  * pitch: 118
  * inflection: 58
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 118
  * subtones: 110
  * vocalRange: 100
  * smoothness: 112
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-uk-ua – Eloquence seed – Ukrainian

* Language: uk
* Default language profile: uk-ua-seed
* Tags: eloquence, seed, ukrainian
* Parameters:
  * rate: 106
  * pitch: 122
  * inflection: 62
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 112
  * vocalLayers: 100
  * overtones: 120
  * subtones: 100
  * vocalRange: 100
  * smoothness: 118
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-pl-pl – Eloquence seed – Polish

* Language: pl
* Default language profile: pl-pl-seed
* Tags: eloquence, seed, polish
* Parameters:
  * rate: 108
  * pitch: 118
  * inflection: 60
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 118
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 120
  * subtones: 108
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-cs-cz – Eloquence seed – Czech

* Language: cs
* Default language profile: cs-cz-seed
* Tags: eloquence, seed, czech
* Parameters:
  * rate: 106
  * pitch: 118
  * inflection: 58
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 118
  * whisper: 112
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 122
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-tr-tr – Eloquence seed – Turkish

* Language: tr
* Default language profile: tr-tr-seed
* Tags: eloquence, seed, turkish
* Parameters:
  * rate: 108
  * pitch: 120
  * inflection: 62
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 110
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 120
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 112
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-el-gr – Eloquence seed – Greek

* Language: el
* Default language profile: el-gr-seed
* Tags: eloquence, seed, greek
* Parameters:
  * rate: 104
  * pitch: 118
  * inflection: 60
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 118
  * stress: 100
  * timbre: 100
  * tone: 108
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 116
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-nl-nl – Eloquence seed – Dutch

* Language: nl
* Default language profile: nl-nl-seed
* Tags: eloquence, seed, dutch
* Parameters:
  * rate: 110
  * pitch: 116
  * inflection: 56
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 100
  * vocalLayers: 100
  * overtones: 100
  * subtones: 100
  * vocalRange: 100
  * smoothness: 114
  * whisper: 110
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 112
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-sv-se – Eloquence seed – Swedish

* Language: sv
* Default language profile: sv-se-seed
* Tags: eloquence, seed, swedish
* Parameters:
  * rate: 108
  * pitch: 124
  * inflection: 64
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 128
  * vocalLayers: 100
  * overtones: 118
  * subtones: 100
  * vocalRange: 100
  * smoothness: 100
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 120
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-nb-no – Eloquence seed – Norwegian

* Language: nb
* Default language profile: nb-no-seed
* Tags: eloquence, seed, norwegian
* Parameters:
  * rate: 104
  * pitch: 122
  * inflection: 62
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 126
  * vocalLayers: 100
  * overtones: 116
  * subtones: 100
  * vocalRange: 100
  * smoothness: 118
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-da-dk – Eloquence seed – Danish

* Language: da
* Default language profile: da-dk-seed
* Tags: eloquence, seed, danish
* Parameters:
  * rate: 102
  * pitch: 118
  * inflection: 60
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 1
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 120
  * vocalLayers: 100
  * overtones: 100
  * subtones: 110
  * vocalRange: 100
  * smoothness: 100
  * whisper: 112
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-seed-fi-fi – Eloquence seed – Finnish

* Language: fi
* Default language profile: fi-fi-seed
* Tags: eloquence, seed, finnish
* Parameters:
  * rate: 100
  * pitch: 118
  * inflection: 56
  * headSize: 110
  * roughness: 20
  * breathiness: 22
  * volume: 92
  * gender: 0
  * emphasis: 100
  * stress: 100
  * timbre: 100
  * tone: 112
  * vocalLayers: 100
  * overtones: 100
  * subtones: 116
  * vocalRange: 100
  * smoothness: 120
  * whisper: 100
  * inflectionContour: 100
  * roughnessControl: 100
  * headSizeContour: 100
  * macroVolume: 100
  * toneSize: 100
  * scopeDepth: 100
* Extras:
  * notes: ['Seed template awaiting community tuning for regional authenticity.', 'Advanced sliders stay at documented defaults unless overrides are provided.']
  * phonemeFallback: ipaFirst

### eloquence-heritage-jaws-classic – Heritage JAWS (Paul)

* Language: en-US
* Default language profile: en-us-heritage
* Tags: eloquence, heritage, jaws, english
* Parameters:
  * rate: 116
  * pitch: 102
  * inflection: 44
  * headSize: 124
  * roughness: 26
  * breathiness: 18
  * volume: 92
  * gender: 0
* Extras:
  * phonemeFallback: ipaFirst
  * phonemeReplacements: {'@': 'description', 'tS': 'example', 'dZ': 'example', 'N': 'example'}
  * settings: {'ABRDICT': True, 'backquoteVoiceTags': True}

### eloquence-loquence-studio – Loquence Studio (SAPI-4)

* Language: en-US
* Default language profile: en-us-heritage
* Tags: eloquence, sapi4, studio, english
* Parameters:
  * rate: 108
  * pitch: 130
  * inflection: 52
  * headSize: 112
  * roughness: 18
  * breathiness: 30
  * volume: 95
  * gender: 0
* Extras:
  * phonemeFallback: descriptionsFirst
  * phonemeReplacements: {'@': 'ipa', 'r': 'description', 'dZ': 'ipa'}
  * settings: {'phrasePrediction': True}

### eloquence-window-eyes-expressive – Window-Eyes Expressive

* Language: en-US
* Default language profile: en-us-heritage
* Tags: eloquence, window-eyes, heritage, english
* Parameters:
  * rate: 112
  * pitch: 96
  * inflection: 38
  * headSize: 132
  * roughness: 34
  * breathiness: 22
  * volume: 90
  * gender: 0
* Extras:
  * phonemeFallback: examplesFirst
  * phonemeReplacements: {'@': 'example', 'tS': 'ipa', 'S': 'description'}
  * settings: {'ABRDICT': True}

### eloquence-bhp-precision – Blind Help Precision

* Language: en-US
* Default language profile: en-us-heritage
* Tags: eloquence, blindhelp, modern, english
* Parameters:
  * rate: 120
  * pitch: 110
  * inflection: 45
  * headSize: 122
  * roughness: 24
  * breathiness: 20
  * volume: 94
  * gender: 0
* Extras:
  * phonemeFallback: examplesFirst
  * phonemeReplacements: {'@': 'description', 'N': 'ipa', 'r': 'example'}
  * settings: {'ABRDICT': True, 'phrasePrediction': True}

### eloquence-sapi5-viavoice-paul-xl – ViaVoice Paul XL (SAPI 5)

* Language: en-US
* Default language profile: en-us-heritage
* Tags: eloquence, ibm, viavoice, sapi5, english
* Parameters:
  * rate: 118
  * pitch: 104
  * inflection: 52
  * headSize: 126
  * roughness: 22
  * breathiness: 14
  * volume: 96
  * gender: 0
* Extras:
  * phonemeFallback: examplesFirst
  * phonemeReplacements: {'@': 'description', 'r': 'example', 'T': 'ipa', 'dZ': 'description'}
  * settings: {'ABRDICT': True, 'phrasePrediction': True}
  * sourceArchive: https://datajake.braillescreen.net/tts/sapi_voices/SAPI5_IBMTTS.zip

### eloquence-sapi4-viavoice-tracy – ViaVoice Tracy (SAPI 4)

* Language: en-US
* Default language profile: en-us-heritage
* Tags: eloquence, ibm, viavoice, sapi4, english
* Parameters:
  * rate: 112
  * pitch: 136
  * inflection: 58
  * headSize: 108
  * roughness: 16
  * breathiness: 32
  * volume: 92
  * gender: 1
* Extras:
  * phonemeFallback: ipaFirst
  * phonemeReplacements: {'@': 'ipa', 'S': 'description', 'tS': 'example', 'Z': 'description'}
  * settings: {'phrasePrediction': True}
  * sourceArchive: https://datajake.braillescreen.net/tts/sapi_voices/IBM-ViaVoice_TTS-SAPI4.zip

### eloquence-sapi4-eloq61-studio – Eloquence 6.1 Studio (SAPI 4)

* Language: en-US
* Default language profile: en-us-heritage
* Tags: eloquence, sapi4, studio, english
* Parameters:
  * rate: 110
  * pitch: 128
  * inflection: 54
  * headSize: 114
  * roughness: 18
  * breathiness: 28
  * volume: 95
  * gender: 0
* Extras:
  * phonemeFallback: descriptionsFirst
  * phonemeReplacements: {'@': 'ipa', 'A': 'example', 'N': 'description', 'tS': 'ipa'}
  * settings: {'phrasePrediction': True, 'backquoteVoiceTags': True}
  * sourceArchive: https://datajake.braillescreen.net/tts/sapi_voices/eloq61.exe

### eloquence-sapi5-codefactory-balanced – Eloquence for Windows Balanced (Code Factory)

* Language: en-US
* Default language profile: en-us-heritage
* Tags: eloquence, codefactory, sapi5, english
* Parameters:
  * rate: 116
  * pitch: 132
  * inflection: 60
  * headSize: 120
  * roughness: 20
  * breathiness: 24
  * volume: 98
  * gender: 0
* Extras:
  * phonemeFallback: examplesFirst
  * phonemeReplacements: {'@': 'ipa', '3': 'description', 'dZ': 'example', 'Z': 'ipa'}
  * settings: {'phrasePrediction': True, 'abbreviationDictionary': True}
  * sourceArchive: https://www.codefactoryglobal.com/downloads/installers/EloquenceForWindows-Setup.exe

### nvspeechplayer-adam – NV Speech Player Adam

* Language: en-US
* Default language profile: en-us-basic
* Tags: nvspeechplayer, english, classic
* Parameters:
  * rate: 104
  * pitch: 118
  * inflection: 58
  * headSize: 112
  * roughness: 18
  * breathiness: 30
  * volume: 90
  * gender: 0
  * emphasis: 118
  * stress: 112
  * timbre: 116
  * tone: 122
  * vocalLayers: 115
  * overtones: 110
  * subtones: 108
  * vocalRange: 114
  * smoothness: 104
  * whisper: 96
  * toneSize: 112
  * scopeDepth: 110
  * inflectionContour: 118
  * roughnessControl: 92
  * headSizeContour: 114
  * macroVolume: 104
* Extras:
  * nvspeechPlayer: {'cb1_mul': 1.3, 'pa6_mul': 1.3, 'fricationAmplitude_mul': 0.85}
  * phonemeFallback: examplesFirst
  * phonemeReplacements: {'S': 'example', 'Z': 'ipa', 'tS': 'ipa'}

### nvspeechplayer-benjamin – NV Speech Player Benjamin

* Language: en-US
* Default language profile: en-us-basic
* Tags: nvspeechplayer, english, bright
* Parameters:
  * rate: 108
  * pitch: 124
  * inflection: 52
  * headSize: 118
  * roughness: 16
  * breathiness: 26
  * volume: 88
  * gender: 0
  * emphasis: 130
  * stress: 118
  * timbre: 124
  * tone: 136
  * vocalLayers: 108
  * overtones: 95
  * subtones: 96
  * vocalRange: 120
  * smoothness: 94
  * whisper: 90
  * toneSize: 118
  * scopeDepth: 102
  * inflectionContour: 126
  * roughnessControl: 128
  * headSizeContour: 116
  * macroVolume: 108
* Extras:
  * nvspeechPlayer: {'cf1_mul': 1.01, 'cf2_mul': 1.02, 'cf4': 3770, 'cf5': 4100, 'cf6': 5000, 'cfNP_mul': 0.9, 'cb1_mul': 1.3, 'fricationAmplitude_mul': 0.7, 'pa6_mul': 1.3}
  * phonemeFallback: ipaFirst
  * phonemeReplacements: {'s': 'ipa', 'z': 'description', 'N': 'example'}

### nvspeechplayer-caleb – NV Speech Player Caleb

* Language: en-US
* Default language profile: en-us-basic
* Tags: nvspeechplayer, english, breathy
* Parameters:
  * rate: 92
  * pitch: 106
  * inflection: 44
  * headSize: 120
  * roughness: 28
  * breathiness: 40
  * volume: 85
  * gender: 0
  * emphasis: 96
  * stress: 88
  * timbre: 102
  * tone: 108
  * vocalLayers: 90
  * overtones: 82
  * subtones: 120
  * vocalRange: 98
  * smoothness: 140
  * whisper: 180
  * toneSize: 108
  * scopeDepth: 132
  * inflectionContour: 96
  * roughnessControl: 80
  * headSizeContour: 124
  * macroVolume: 90
* Extras:
  * nvspeechPlayer: {'aspirationAmplitude': 1, 'voiceAmplitude': 0}
  * phonemeFallback: descriptionsFirst
  * phonemeReplacements: {'h': 'description', 'f': 'example', 'T': 'ipa'}

### nvspeechplayer-david – NV Speech Player David

* Language: en-US
* Default language profile: en-us-basic
* Tags: nvspeechplayer, english, low
* Parameters:
  * rate: 100
  * pitch: 90
  * inflection: 48
  * headSize: 130
  * roughness: 22
  * breathiness: 24
  * volume: 92
  * gender: 0
  * emphasis: 92
  * stress: 100
  * timbre: 105
  * tone: 98
  * vocalLayers: 112
  * overtones: 88
  * subtones: 138
  * vocalRange: 104
  * smoothness: 110
  * whisper: 102
  * toneSize: 126
  * scopeDepth: 140
  * inflectionContour: 104
  * roughnessControl: 88
  * headSizeContour: 130
  * macroVolume: 110
* Extras:
  * nvspeechPlayer: {'voicePitch_mul': 0.75, 'endVoicePitch_mul': 0.75, 'cf1_mul': 0.75, 'cf2_mul': 0.85, 'cf3_mul': 0.85}
  * phonemeFallback: examplesFirst
  * phonemeReplacements: {'l': 'description', 'r': 'example', 'd': 'ipa'}

### espeak-variant-espeak-variants-alex – Alex

* Language: unspecified
* Default language profile: –
* Tags: espeak, variant, male
* Parameters:
  * gender: 0
  * rate: 100
  * pitch: 105
  * inflection: 69
  * headSize: 107
  * roughness: 12
  * breathiness: 0
  * volume: 75

### espeak-variant-espeak-variants-storm – Storm

* Language: en-US
* Default language profile: en-us-basic
* Tags: espeak, variant, lang:en-us, male
* Parameters:
  * gender: 0
  * rate: 100
  * pitch: 60
  * inflection: 60
  * headSize: 100
  * roughness: 0
  * breathiness: 0
  * volume: 90
