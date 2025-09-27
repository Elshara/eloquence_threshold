"""Curated voice scenes that integrate DataJake archives with Eloquence customisation."""
from __future__ import annotations

from typing import Dict, Iterable, List

from phoneme_customizer import VoiceScene, build_scene_snapshot


def _phoneme(*entries: Dict[str, float]) -> List[Dict[str, float]]:
    return [dict(entry) for entry in entries]


VOICE_SCENES: tuple[VoiceScene, ...] = (
    VoiceScene(
        name="DataJake eSpeak NG clarity bridge",
        description=(
            "Blend the eSpeak NG articulation stacks mirrored in DataJake's mirrors with Eloquence's "
            "smoother formants so NVDA users can toggle between classic and hybrid fricatives."
        ),
        sample_rate_hz=48000.0,
        global_parameters={
            "emphasis": 132,
            "stress": 120,
            "timbre": 112,
            "sibilantClarity": 148,
            "vocalLayers": 118,
            "plosiveImpact": 122,
        },
        phoneme_overrides={
            "S": _phoneme(
                {"lowHz": 4200.0, "highHz": 8800.0, "gainDb": 3.5, "filterType": "peaking", "q": 1.15},
                {"lowHz": 8800.0, "highHz": 16000.0, "gainDb": 2.0, "filterType": "highShelf", "q": 0.7},
            ),
            "Z": _phoneme(
                {"lowHz": 3600.0, "highHz": 7800.0, "gainDb": 2.4, "filterType": "peaking", "q": 1.05},
                {"lowHz": 7800.0, "highHz": 15000.0, "gainDb": 1.8, "filterType": "highShelf", "q": 0.7},
            ),
            "T": _phoneme(
                {"lowHz": 1500.0, "highHz": 4800.0, "gainDb": 2.8, "filterType": "bandPass", "q": 1.8},
            ),
            "AH": _phoneme(
                {"lowHz": 520.0, "highHz": 1300.0, "gainDb": 1.6, "filterType": "peaking", "q": 1.2},
            ),
            "IY": _phoneme(
                {"lowHz": 260.0, "highHz": 2200.0, "gainDb": 1.4, "filterType": "peaking", "q": 1.1},
            ),
        },
        tags=("espeak-ng", "phoneme", "clarity", "nvda"),
        archive_sources=(
            "docs/archive_inventory.json#eSpeak Portible With speechPlayer.zip",
            "docs/archive_inventory.json#espeak-ng-1.52.0.zip",
        ),
        language_focus=("en", "multi"),
    ),
    VoiceScene(
        name="DataJake DECtalk heritage warmth",
        description=(
            "Project the warm DECtalk/Fonix formant emphasis captured in DataJake's installers onto Eloquence "
            "so NVDA readers chasing Perfect Paul or Rich Paul textures retain mellow vowels."
        ),
        sample_rate_hz=44100.0,
        global_parameters={
            "scopeDepth": 136,
            "tone": 94,
            "smoothness": 128,
            "roughnessControl": 86,
            "macroVolume": 112,
            "headSizeContour": 118,
        },
        phoneme_overrides={
            "AA": _phoneme(
                {"lowHz": 360.0, "highHz": 980.0, "gainDb": 2.6, "filterType": "peaking", "q": 1.0},
                {"lowHz": 980.0, "highHz": 2200.0, "gainDb": -1.2, "filterType": "peaking", "q": 1.4},
            ),
            "AO": _phoneme(
                {"lowHz": 320.0, "highHz": 880.0, "gainDb": 2.2, "filterType": "peaking", "q": 1.2},
                {"lowHz": 880.0, "highHz": 2100.0, "gainDb": -1.0, "filterType": "peaking", "q": 1.4},
            ),
            "UW": _phoneme(
                {"lowHz": 260.0, "highHz": 720.0, "gainDb": 2.0, "filterType": "peaking", "q": 1.2},
                {"lowHz": 720.0, "highHz": 1800.0, "gainDb": -1.4, "filterType": "peaking", "q": 1.3},
            ),
            "R": _phoneme(
                {"lowHz": 320.0, "highHz": 1600.0, "gainDb": 1.2, "filterType": "bandPass", "q": 1.6},
            ),
        },
        tags=("dectalk", "fonix", "warmth", "nvda"),
        archive_sources=(
            "docs/archive_inventory.json#DECtalk English 4.61.exe",
            "docs/archive_inventory.json#FonixTalk-1.0.0.zip",
            "docs/archive_inventory.json#DECtalk v4.61 SDK.iso",
        ),
        language_focus=("en", "pt", "es"),
    ),
    VoiceScene(
        name="NV Speech Player hybrid expressiveness",
        description=(
            "Fuse NV Speech Player's layered plosive and overtone curves with Eloquence so NVDA's expressiveness "
            "sliders mirror Microsoft's hybrid talker energy without abandoning Eloquence's speed."
        ),
        sample_rate_hz=48000.0,
        global_parameters={
            "vocalLayers": 142,
            "overtones": 138,
            "plosiveImpact": 128,
            "inflectionContour": 134,
            "tone": 124,
            "macroVolume": 120,
        },
        phoneme_overrides={
            "K": _phoneme(
                {"lowHz": 1800.0, "highHz": 5200.0, "gainDb": 3.0, "filterType": "bandPass", "q": 1.7},
            ),
            "CH": _phoneme(
                {"lowHz": 2200.0, "highHz": 6800.0, "gainDb": 3.4, "filterType": "bandPass", "q": 1.6},
            ),
            "L": _phoneme(
                {"lowHz": 180.0, "highHz": 820.0, "gainDb": 1.8, "filterType": "peaking", "q": 1.1},
                {"lowHz": 1800.0, "highHz": 3600.0, "gainDb": 1.4, "filterType": "peaking", "q": 1.3},
            ),
            "ER": _phoneme(
                {"lowHz": 360.0, "highHz": 1600.0, "gainDb": 1.6, "filterType": "peaking", "q": 1.2},
                {"lowHz": 2600.0, "highHz": 4200.0, "gainDb": 2.0, "filterType": "peaking", "q": 1.2},
            ),
        },
        tags=("nvspeechplayer", "expressive", "nvda", "hybrid"),
        archive_sources=(
            "docs/archive_inventory.json#NV Speech Player SDK.zip",
            "docs/archive_inventory.json#NVDA Speech Player tooling.tar.gz",
        ),
        language_focus=("en", "hi", "zh"),
    ),
)


def iter_scene_snapshots() -> List[Dict[str, object]]:
    """Return rendered snapshots for all curated scenes."""

    return [build_scene_snapshot(scene) for scene in VOICE_SCENES]


__all__ = ["VOICE_SCENES", "iter_scene_snapshots"]
