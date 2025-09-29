# Voice frequency matrix

This matrix outlines the frequency coverage of Eloquence's advanced voice parameters. Each slider shapes the phoneme EQ bands documented in `voice_parameters.py`, giving NVDA users and tooling a reproducible way to align NV Speech Player metadata with Eloquence's parametric filters.

*Generated:* `2025-09-29T23:35:56Z`

## Parameter coverage

| Parameter | Range (0–200) | Frequency focus | Bands | Tags | Gain hint |
| --- | --- | --- | --- | --- | --- |
| Emphasis shaping | 0–200 | 2200.00–5200.00 Hz | 2 | eq, nvspeechplayer, prosody | 6.00 dB |
| Head size contour | 0–200 | 260.00–3200.00 Hz | 3 | eq, formant, size | 6.50 dB |
| Inflection contour | 0–200 | 110.00–4200.00 Hz | 2 | eq, inflection, prosody | 5.00 dB |
| Macro volume envelope | 0–200 | 90.00–12000.00 Hz | 2 | eq, loudness, mix | 4.50 dB |
| Nasal balance | 0–200 | 260.00–1600.00 Hz | 2 | eq, nasal, resonance | 6.80 dB |
| Overtone brilliance | 0–200 | 5800.00–16000.00 Hz | 2 | brightness, eq, harmonics | 12.00 dB |
| Pitch height | 0–200 | 70.00–260.00 Hz | 3 | eq, pitch, prosody | 9.00 dB |
| Plosive impact | 0–200 | 900.00–3600.00 Hz | 3 | attack, consonant, eq | 7.20 dB |
| Roughness | 0–200 | 2600.00–8200.00 Hz | 2 | eq, roughness, texture | 7.00 dB |
| Scope depth | 0–200 | 200.00–820.00 Hz | 2 | depth, eq, warmth | 6.50 dB |
| Sibilant clarity | 0–200 | 5200.00–14000.00 Hz | 3 | consonant, eq, sibilant | 8.20 dB |
| Smoothness | 0–200 | 4200.00–14000.00 Hz | 2 | eq, softness, texture | 8.00 dB |
| Stress contour | 0–200 | 1800.00–4000.00 Hz | 2 | eq, prosody, stress | 6.50 dB |
| Subtone weight | 0–200 | 60.00–420.00 Hz | 2 | eq, harmonics, warmth | 12.00 dB |
| Timbre focus | 0–200 | 500.00–1900.00 Hz | 2 | eq, formant, timbre | 8.00 dB |
| Tone colour | 0–200 | 1400.00–3200.00 Hz | 2 | eq, harmonics, tone | 7.50 dB |
| Tone size | 0–200 | 700.00–2500.00 Hz | 2 | eq, formant, size | 7.00 dB |
| Vocal layering | 0–200 | 120.00–5200.00 Hz | 2 | eq, layering, texture | 5.50 dB |
| Vocal range spread | 0–200 | 100.00–7200.00 Hz | 2 | prosody, range | 6.00 dB |
| Whisper blend | 0–200 | 300.00–11000.00 Hz | 2 | eq, texture, whisper | 10.00 dB |

## Tag frequency envelopes

| Tag | Parameters | Frequency span |
| --- | --- | --- |
| attack | plosiveImpact | 900.00–3600.00 Hz |
| brightness | overtones | 5800.00–16000.00 Hz |
| consonant | plosiveImpact, sibilantClarity | 900.00–14000.00 Hz |
| depth | scopeDepth | 200.00–820.00 Hz |
| eq | emphasis, headSizeContour, inflectionContour, macroVolume, nasalBalance, overtones, pitchHeight, plosiveImpact, roughnessControl, scopeDepth, sibilantClarity, smoothness, stress, subtones, timbre, tone, toneSize, vocalLayers, whisper | 60.00–16000.00 Hz |
| formant | headSizeContour, timbre, toneSize | 260.00–3200.00 Hz |
| harmonics | overtones, subtones, tone | 60.00–16000.00 Hz |
| inflection | inflectionContour | 110.00–4200.00 Hz |
| layering | vocalLayers | 120.00–5200.00 Hz |
| loudness | macroVolume | 90.00–12000.00 Hz |
| mix | macroVolume | 90.00–12000.00 Hz |
| nasal | nasalBalance | 260.00–1600.00 Hz |
| nvspeechplayer | emphasis | 2200.00–5200.00 Hz |
| pitch | pitchHeight | 70.00–260.00 Hz |
| prosody | emphasis, inflectionContour, pitchHeight, stress, vocalRange | 70.00–7200.00 Hz |
| range | vocalRange | 100.00–7200.00 Hz |
| resonance | nasalBalance | 260.00–1600.00 Hz |
| roughness | roughnessControl | 2600.00–8200.00 Hz |
| sibilant | sibilantClarity | 5200.00–14000.00 Hz |
| size | headSizeContour, toneSize | 260.00–3200.00 Hz |
| softness | smoothness | 4200.00–14000.00 Hz |
| stress | stress | 1800.00–4000.00 Hz |
| texture | roughnessControl, smoothness, vocalLayers, whisper | 120.00–14000.00 Hz |
| timbre | timbre | 500.00–1900.00 Hz |
| tone | tone | 1400.00–3200.00 Hz |
| warmth | scopeDepth, subtones | 60.00–820.00 Hz |
| whisper | whisper | 300.00–11000.00 Hz |

