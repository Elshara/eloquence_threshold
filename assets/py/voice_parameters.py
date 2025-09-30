"""Shared definitions for extended Eloquence voice parameters.

The classic Eloquence engine exposes eight voice parameters.  Modern synths
such as NV Speech Player, DECtalk, and FonixTalk expose a richer collection of
controls that let users tune emphasis, consonant clarity, harmonic content, and
the perceived depth of a voice.  This module centralises metadata for those
extended parameters so the loader, synthesiser driver, and documentation
generators stay aligned.

Each entry mirrors the structure consumed by :mod:`voice_catalog`:

``label``
    Human readable name announced by NVDA.
``description``
    Short hint describing how the control affects speech.
``min`` / ``max`` / ``default`` / ``step``
    Numeric range surfaced to users.  Values follow the 0–200 convention used
    by other Eloquence sliders so keyboard workflows remain predictable.
``tags``
    Loose descriptors that documentation and reporting tools can use to group
    related controls.
``profile``
    Optional hints describing how the slider maps onto the global parametric
    EQ managed by :mod:`phoneme_customizer`.  Profiles may expose ``bands`` – a
    sequence of ``{"range": (low, high), "gainMultiplier": float}`` mappings –
    so helpers can scale multiple frequency regions from a single slider.  When
    omitted the helpers fall back to the legacy ``range``/``ranges`` metadata.

Additional hints (for example ``profile`` and ``nvspeechExtras``) document how
the parameter maps to NV Speech Player data.  The synthesiser does not consume
those fields directly yet, but keeping them alongside the range metadata helps
tooling reason about provenance and future automation.
"""
from __future__ import annotations

from typing import Dict, Mapping


def _default_tags(*values: str) -> tuple[str, ...]:
    return tuple(sorted({value for value in values if value}))


ADVANCED_VOICE_PARAMETER_SPECS: Dict[str, Mapping[str, object]] = {
    "emphasis": {
        "label": "Emphasis shaping",
        "description": (
            "Boost or soften consonant attacks and vowel onsets to mirror how "
            "NV Speech Player emphasises foreground syllables."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("prosody", "nvspeechplayer", "eq"),
        "profile": {
            "kind": "band",
            "range": (2200, 5200),
            "gain": 6.0,
            "bands": (
                {"range": (2200, 5200)},
            ),
        },
        "nvspeechExtras": ("fricationAmplitude_mul", "aspirationAmplitude"),
    },
    "stress": {
        "label": "Stress contour",
        "description": (
            "Shapes the mid-high resonances that convey linguistic stress, "
            "mirroring NV Speech Player's intensity multipliers."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("prosody", "stress", "eq"),
        "profile": {
            "kind": "band",
            "range": (1800, 4000),
            "gain": 6.5,
            "bands": (
                {"range": (1800, 4000)},
            ),
        },
        "nvspeechExtras": ("voicePitch_mul", "endVoicePitch_mul"),
    },
    "timbre": {
        "label": "Timbre focus",
        "description": (
            "Balances lower formants against upper harmonics so the voice can "
            "sound darker or brighter without losing articulation."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("timbre", "formant", "eq"),
        "profile": {
            "kind": "band",
            "range": (500, 1900),
            "gain": 8.0,
            "bands": (
                {"range": (500, 1900)},
            ),
        },
        "nvspeechExtras": ("cf1_mul", "cf2_mul", "cb1_mul"),
    },
    "tone": {
        "label": "Tone colour",
        "description": (
            "Highlights the harmonic band responsible for tone colour, similar "
            "to NV Speech Player's cascade/parallel formant multipliers."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("tone", "eq", "harmonics"),
        "profile": {
            "kind": "band",
            "range": (1400, 3200),
            "gain": 7.5,
            "bands": (
                {"range": (1400, 3200)},
            ),
        },
        "nvspeechExtras": ("pf3", "pf4", "parallelBypass"),
    },
    "pitchHeight": {
        "label": "Pitch height",
        "description": (
            "Raises or lowers the perceived pitch centre by reshaping the "
            "fundamental energy band without affecting speaking rate."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("pitch", "prosody", "eq"),
        "profile": {
            "kind": "band",
            "range": (70, 260),
            "gain": 9.0,
            "bands": (
                {"range": (70, 140), "gainMultiplier": 1.1},
                {"range": (140, 260)},
            ),
        },
        "nvspeechExtras": ("voicePitch", "voicePitch_mul", "startPitch"),
    },
    "vocalLayers": {
        "label": "Vocal layering",
        "description": (
            "Controls the balance between fundamental energy and higher "
            "partials to simulate stacked voices or thinner single voices."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("texture", "layering", "eq"),
        "profile": {
            "kind": "dual-band",
            "ranges": ((120, 380), (2400, 5200)),
            "gain": 5.5,
            "bands": (
                {"range": (120, 380), "gainMultiplier": 0.7},
                {"range": (2400, 5200)},
            ),
        },
        "nvspeechExtras": ("voiceAmplitude", "parallelBypass"),
    },
    "plosiveImpact": {
        "label": "Plosive impact",
        "description": (
            "Accentuates consonant bursts (P, T, K, CH) by boosting the "
            "1–4 kHz transient band where plosive energy peaks."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("consonant", "attack", "eq"),
        "profile": {
            "kind": "band",
            "range": (900, 3600),
            "gain": 7.2,
            "bands": (
                {"range": (900, 2200), "gainMultiplier": 1.1},
                {"range": (2200, 3600)},
            ),
        },
        "nvspeechExtras": ("consonantAttack", "transientEmphasis"),
    },
    "overtones": {
        "label": "Overtone brilliance",
        "description": (
            "Adds sparkle or dampens sibilants by shaping the 6–16 kHz band "
            "used by NV Speech Player's frication models."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("harmonics", "brightness", "eq"),
        "profile": {
            "kind": "shelf-high",
            "range": (5800, 16000),
            "gain": 12.0,
            "bands": (
                {"range": (5800, 16000)},
            ),
        },
        "nvspeechExtras": ("fricationAmplitude_mul",),
    },
    "sibilantClarity": {
        "label": "Sibilant clarity",
        "description": (
            "Clarifies S/SH/CH/J style phonemes by shaping the 5–14 kHz "
            "sibilant noise band referenced by NV Speech Player."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("consonant", "sibilant", "eq"),
        "profile": {
            "kind": "band",
            "range": (5200, 14000),
            "gain": 8.2,
            "bands": (
                {"range": (5200, 9000)},
                {"range": (9000, 14000), "gainMultiplier": 0.7},
            ),
        },
        "nvspeechExtras": ("fricationBandwidth", "fricationAmplitude_mul"),
    },
    "subtones": {
        "label": "Subtone weight",
        "description": (
            "Boost or trim the 60–400 Hz band that defines chest resonance and "
            "NV Speech Player's low frequency shaping."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("harmonics", "warmth", "eq"),
        "profile": {
            "kind": "shelf-low",
            "range": (60, 420),
            "gain": 12.0,
            "bands": (
                {"range": (60, 420)},
            ),
        },
        "nvspeechExtras": ("voiceAmplitude", "cbN0"),
    },
    "nasalBalance": {
        "label": "Nasal balance",
        "description": (
            "Controls nasal resonance cues so voices can favour open or "
            "pinched pronunciations without muting clarity."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("nasal", "resonance", "eq"),
        "profile": {
            "kind": "dual-band",
            "ranges": ((260, 520), (980, 1600)),
            "gain": 6.8,
            "bands": (
                {"range": (260, 520)},
                {"range": (980, 1600), "gainMultiplier": 0.8},
            ),
        },
        "nvspeechExtras": ("nasalPole", "nasalZero"),
    },
    "vocalRange": {
        "label": "Vocal range spread",
        "description": (
            "Expands or narrows the perceived vocal range by shaping both "
            "fundamentals and upper resonances."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("range", "prosody"),
        "profile": {
            "kind": "dual-band",
            "ranges": ((100, 320), (3600, 7200)),
            "gain": 6.0,
            "bands": (
                {"range": (100, 320), "gainMultiplier": 0.6},
                {"range": (3600, 7200)},
            ),
        },
        "nvspeechExtras": ("voicePitch_mul", "endVoicePitch_mul", "cfNP"),
    },
    "smoothness": {
        "label": "Smoothness",
        "description": (
            "Controls how much high frequency noise is removed to mimic NV "
            "Speech Player's aspiration blending."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("texture", "softness", "eq"),
        "profile": {
            "kind": "band",
            "range": (4200, 14000),
            "gain": 8.0,
            "bands": (
                {"range": (4200, 14000), "gainMultiplier": -1.0},
            ),
        },
        "nvspeechExtras": ("aspirationAmplitude", "copyAdjacent"),
    },
    "whisper": {
        "label": "Whisper blend",
        "description": (
            "Introduces or removes aspiration-style whisper components across "
            "the band limited by NV Speech Player's breath tables."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("texture", "whisper", "eq"),
        "profile": {
            "kind": "dual-band",
            "ranges": ((300, 900), (3600, 11000)),
            "gain": 10.0,
            "bands": (
                {"range": (3600, 11000)},
                {"range": (300, 900), "gainMultiplier": -0.4},
            ),
        },
        "nvspeechExtras": ("aspirationAmplitude",),
    },
    "inflectionContour": {
        "label": "Inflection contour",
        "description": (
            "Emphasises rising and falling transitions by shaping low-mid "
            "fundamentals and the 2–4 kHz glide band NV Speech Player uses "
            "for syllable inflection cues."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("prosody", "inflection", "eq"),
        "profile": {
            "kind": "dual-band",
            "ranges": ((110, 320), (2200, 4200)),
            "gain": 5.0,
            "bands": (
                {"range": (110, 320), "gainMultiplier": 0.55},
                {"range": (2200, 4200)},
            ),
        },
        "nvspeechExtras": ("voicePitch_mul", "endVoicePitch_mul", "inflection"),
    },
    "roughnessControl": {
        "label": "Roughness",
        "description": (
            "Adds rasp or polishes brightness by boosting or cutting the "
            "2.6–8.2 kHz band tied to NV Speech Player's roughness tables."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("texture", "roughness", "eq"),
        "profile": {
            "kind": "band",
            "range": (2600, 8200),
            "gain": 7.0,
            "bands": (
                {"range": (2600, 8200)},
            ),
        },
        "nvspeechExtras": ("roughness", "fricationAmplitude_mul"),
    },
    "headSizeContour": {
        "label": "Head size contour",
        "description": (
            "Simulates shorter or longer vocal tracts by biasing the first "
            "three formants, mirroring NV Speech Player's head size macro."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("formant", "size", "eq"),
        "profile": {
            "kind": "triple-band",
            "ranges": ((260, 520), (820, 1500), (2200, 3200)),
            "gain": 6.5,
            "bands": (
                {"range": (260, 520), "gainMultiplier": 0.65},
                {"range": (820, 1500)},
                {"range": (2200, 3200), "gainMultiplier": -0.4},
            ),
        },
        "nvspeechExtras": ("headSize", "cb1_mul", "cf2_mul", "cf3_mul"),
    },
    "macroVolume": {
        "label": "Macro volume envelope",
        "description": (
            "Blends pre-mix gain with broadband EQ so the voice can swell or "
            "sit back without clipping, echoing NV Speech Player's volume "
            "macros."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("loudness", "mix", "eq"),
        "profile": {
            "kind": "shelf-wide",
            "range": (90, 12000),
            "gain": 4.5,
            "bands": (
                {"range": (90, 12000)},
            ),
        },
        "nvspeechExtras": ("volume", "voiceAmplitude"),
    },
    "toneSize": {
        "label": "Tone size",
        "description": (
            "Simulates smaller or larger resonant cavities by biasing the "
            "first three formants—akin to NV Speech Player's head size macro."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("formant", "size", "eq"),
        "profile": {
            "kind": "band",
            "range": (700, 2500),
            "gain": 7.0,
            "bands": (
                {"range": (700, 2500)},
            ),
        },
        "nvspeechExtras": ("cb1_mul", "cf3_mul"),
    },
    "scopeDepth": {
        "label": "Scope depth",
        "description": (
            "Controls how deep or shallow the voice feels by reshaping the "
            "upper-bass region present in NV Speech Player formants."
        ),
        "min": 0,
        "max": 200,
        "default": 100,
        "step": 1,
        "tags": _default_tags("depth", "warmth", "eq"),
        "profile": {
            "kind": "band",
            "range": (200, 820),
            "gain": 6.5,
            "bands": (
                {"range": (200, 820)},
            ),
        },
        "nvspeechExtras": ("cbNP", "caNP"),
    },
}


def advanced_parameter_defaults() -> Dict[str, int]:
    """Return default values for every extended voice parameter."""

    return {name: int(spec.get("default", 100)) for name, spec in ADVANCED_VOICE_PARAMETER_SPECS.items()}

