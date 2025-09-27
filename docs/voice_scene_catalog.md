# Voice scene catalog

This catalog integrates DataJake's archive inventory with Eloquence's phoneme customiser so NVDA contributors can stage reusable presets. Each scene references eSpeak NG, DECtalk/Fonix, NV Speech Player, or similar tooling from the cache and maps them to the extended sliders documented in `AGENTS.md`.

Run `python tools/export_voice_scenes.py --json docs/voice_scene_catalog.json --markdown docs/voice_scene_catalog.md` to refresh this file after adjusting the curated scenes.

## DataJake eSpeak NG clarity bridge

Blend the eSpeak NG articulation stacks mirrored in DataJake's mirrors with Eloquence's smoother formants so NVDA users can toggle between classic and hybrid fricatives.

- **Tags:** clarity, espeak-ng, nvda, phoneme
- **Language focus:** en, multi
- **Sample rate target:** 48,000 Hz
- **Headroom:** 24,000 Hz (post WASAPI clamp)
- **DataJake archive references:**
  - docs/archive_inventory.json#eSpeak Portible With speechPlayer.zip
  - docs/archive_inventory.json#espeak-ng-1.52.0.zip

### Global NV Speech Player sliders

| Parameter | Value | Default | Delta |
| --- | ---: | ---: | ---: |
| emphasis | 132 | 100 | +32 |
| headSizeContour | 100 | 100 | ±0 |
| inflectionContour | 100 | 100 | ±0 |
| macroVolume | 100 | 100 | ±0 |
| nasalBalance | 100 | 100 | ±0 |
| overtones | 100 | 100 | ±0 |
| pitchHeight | 100 | 100 | ±0 |
| plosiveImpact | 122 | 100 | +22 |
| roughnessControl | 100 | 100 | ±0 |
| scopeDepth | 100 | 100 | ±0 |
| sibilantClarity | 148 | 100 | +48 |
| smoothness | 100 | 100 | ±0 |
| stress | 120 | 100 | +20 |
| subtones | 100 | 100 | ±0 |
| timbre | 112 | 100 | +12 |
| tone | 100 | 100 | ±0 |
| toneSize | 100 | 100 | ±0 |
| vocalLayers | 118 | 100 | +18 |
| vocalRange | 100 | 100 | ±0 |
| whisper | 100 | 100 | ±0 |

### Per-phoneme EQ guidance

| Phoneme | Band | Range (Hz) | Gain (dB) | Filter | Q |
| --- | ---: | --- | ---: | --- | ---: |
| AH | 1 | 520–1,300 | 1.60 | peaking | 0.38 |
| IY | 1 | 260–2,200 | 1.40 | peaking | 0.16 |
| S | 1 | 4,200–8,800 | 3.50 | peaking | 0.47 |
| S | 2 | 8,800–16,000 | 2.00 | highShelf | 0.70 |
| T | 1 | 1,500–4,800 | 2.80 | bandPass | 1.80 |
| Z | 1 | 3,600–7,800 | 2.40 | peaking | 0.45 |
| Z | 2 | 7,800–15,000 | 1.80 | highShelf | 0.70 |

These settings layer on top of Eloquence's existing NVDA configuration. They reference DataJake's mirrors so contributors can port phoneme rules, IPA tables, and tooling back into the synthesiser without hunting across 1,500+ archives.

## DataJake DECtalk heritage warmth

Project the warm DECtalk/Fonix formant emphasis captured in DataJake's installers onto Eloquence so NVDA readers chasing Perfect Paul or Rich Paul textures retain mellow vowels.

- **Tags:** dectalk, fonix, nvda, warmth
- **Language focus:** en, es, pt
- **Sample rate target:** 44,100 Hz
- **Headroom:** 22,050 Hz (post WASAPI clamp)
- **DataJake archive references:**
  - docs/archive_inventory.json#DECtalk English 4.61.exe
  - docs/archive_inventory.json#DECtalk v4.61 SDK.iso
  - docs/archive_inventory.json#FonixTalk-1.0.0.zip

### Global NV Speech Player sliders

| Parameter | Value | Default | Delta |
| --- | ---: | ---: | ---: |
| emphasis | 100 | 100 | ±0 |
| headSizeContour | 118 | 100 | +18 |
| inflectionContour | 100 | 100 | ±0 |
| macroVolume | 112 | 100 | +12 |
| nasalBalance | 100 | 100 | ±0 |
| overtones | 100 | 100 | ±0 |
| pitchHeight | 100 | 100 | ±0 |
| plosiveImpact | 100 | 100 | ±0 |
| roughnessControl | 86 | 100 | -14 |
| scopeDepth | 136 | 100 | +36 |
| sibilantClarity | 100 | 100 | ±0 |
| smoothness | 128 | 100 | +28 |
| stress | 100 | 100 | ±0 |
| subtones | 100 | 100 | ±0 |
| timbre | 100 | 100 | ±0 |
| tone | 94 | 100 | -6 |
| toneSize | 100 | 100 | ±0 |
| vocalLayers | 100 | 100 | ±0 |
| vocalRange | 100 | 100 | ±0 |
| whisper | 100 | 100 | ±0 |

### Per-phoneme EQ guidance

| Phoneme | Band | Range (Hz) | Gain (dB) | Filter | Q |
| --- | ---: | --- | ---: | --- | ---: |
| AA | 1 | 360–980 | 2.60 | peaking | 0.35 |
| AA | 2 | 980–2,200 | -1.20 | peaking | 0.43 |
| AO | 1 | 320–880 | 2.20 | peaking | 0.34 |
| AO | 2 | 880–2,100 | -1.00 | peaking | 0.40 |
| R | 1 | 320–1,600 | 1.20 | bandPass | 1.60 |
| UW | 1 | 260–720 | 2.00 | peaking | 0.34 |
| UW | 2 | 720–1,800 | -1.40 | peaking | 0.38 |

These settings layer on top of Eloquence's existing NVDA configuration. They reference DataJake's mirrors so contributors can port phoneme rules, IPA tables, and tooling back into the synthesiser without hunting across 1,500+ archives.

## NV Speech Player hybrid expressiveness

Fuse NV Speech Player's layered plosive and overtone curves with Eloquence so NVDA's expressiveness sliders mirror Microsoft's hybrid talker energy without abandoning Eloquence's speed.

- **Tags:** expressive, hybrid, nvda, nvspeechplayer
- **Language focus:** en, hi, zh
- **Sample rate target:** 48,000 Hz
- **Headroom:** 24,000 Hz (post WASAPI clamp)
- **DataJake archive references:**
  - docs/archive_inventory.json#NV Speech Player SDK.zip
  - docs/archive_inventory.json#NVDA Speech Player tooling.tar.gz

### Global NV Speech Player sliders

| Parameter | Value | Default | Delta |
| --- | ---: | ---: | ---: |
| emphasis | 100 | 100 | ±0 |
| headSizeContour | 100 | 100 | ±0 |
| inflectionContour | 134 | 100 | +34 |
| macroVolume | 120 | 100 | +20 |
| nasalBalance | 100 | 100 | ±0 |
| overtones | 138 | 100 | +38 |
| pitchHeight | 100 | 100 | ±0 |
| plosiveImpact | 128 | 100 | +28 |
| roughnessControl | 100 | 100 | ±0 |
| scopeDepth | 100 | 100 | ±0 |
| sibilantClarity | 100 | 100 | ±0 |
| smoothness | 100 | 100 | ±0 |
| stress | 100 | 100 | ±0 |
| subtones | 100 | 100 | ±0 |
| timbre | 100 | 100 | ±0 |
| tone | 124 | 100 | +24 |
| toneSize | 100 | 100 | ±0 |
| vocalLayers | 142 | 100 | +42 |
| vocalRange | 100 | 100 | ±0 |
| whisper | 100 | 100 | ±0 |

### Per-phoneme EQ guidance

| Phoneme | Band | Range (Hz) | Gain (dB) | Filter | Q |
| --- | ---: | --- | ---: | --- | ---: |
| CH | 1 | 2,200–6,800 | 3.40 | bandPass | 1.60 |
| ER | 1 | 360–1,600 | 1.60 | peaking | 0.23 |
| ER | 2 | 2,600–4,200 | 2.00 | peaking | 0.72 |
| K | 1 | 1,800–5,200 | 3.00 | bandPass | 1.70 |
| L | 1 | 180–820 | 1.80 | peaking | 0.23 |
| L | 2 | 1,800–3,600 | 1.40 | peaking | 0.50 |

These settings layer on top of Eloquence's existing NVDA configuration. They reference DataJake's mirrors so contributors can port phoneme rules, IPA tables, and tooling back into the synthesiser without hunting across 1,500+ archives.
