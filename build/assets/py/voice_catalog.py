"""Voice template catalogue backed by community metadata.

This module provides a structured view of voice definitions that help Eloquence
mimic eSpeak NG, DECtalk/FonixTalk, and related Klatt synthesizer presets.
Templates map high level descriptors (language, variant, gender, provenance) to
concrete Eloquence parameters so users can build new voices directly from
NVDA's settings dialog.
"""
from __future__ import annotations

import json
import logging
import os
import re
from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Optional, Set, Tuple

import resource_paths
from voice_parameters import ADVANCED_VOICE_PARAMETER_SPECS

LOG = logging.getLogger(__name__)

_VOICE_DATA_ROOT = os.path.abspath(str(resource_paths.assets_root()))
_VOICE_DIRECTORIES = [
    os.path.abspath(str(path)) for path in resource_paths.voice_data_directories()
]
if not _VOICE_DIRECTORIES:
    _VOICE_DIRECTORIES = [os.path.join(_VOICE_DATA_ROOT, "json")]
_ESPEAK_VARIANT_DIR = os.path.abspath(str(resource_paths.asset_dir("voice")))


def _iter_voice_data_files() -> Iterator[Tuple[str, str]]:
    """Yield ``(source_id, path)`` pairs for bundled voice catalog files."""

    seen: Set[str] = set()

    def register(path: str) -> Optional[Tuple[str, str]]:
        absolute = os.path.abspath(path)
        if absolute in seen:
            return None
        seen.add(absolute)
        source_id = _source_id_from_path(absolute)
        return source_id, absolute

    for directory in _VOICE_DIRECTORIES:
        if not os.path.isdir(directory):
            continue
        for root, _dirs, files in os.walk(directory):
            for name in sorted(files):
                if not name.lower().endswith(".json"):
                    continue
                path = os.path.join(root, name)
                if not os.path.isfile(path):
                    continue
                result = register(path)
                if result:
                    yield result


def _source_id_from_path(path: str) -> str:
    relative = os.path.relpath(path, _VOICE_DATA_ROOT)
    stem = os.path.splitext(relative)[0]
    normalized = re.sub(r"[^0-9a-zA-Z]+", "-", stem).strip("-")
    return normalized or "voice-data"


@dataclass(frozen=True)
class VoiceParameterRange:
    """Describes the allowed range for a configurable Eloquence parameter."""

    name: str
    label: str
    minimum: int
    maximum: int
    default: int
    step: int
    description: str
    tags: Tuple[str, ...]

    def clamp(self, value: int) -> int:
        """Clamp *value* into the supported range for this parameter."""

        if value < self.minimum:
            return self.minimum
        if value > self.maximum:
            return self.maximum
        return value


@dataclass
class VoiceTemplate:
    """Concrete set of Eloquence parameters inspired by an eSpeak voice."""

    id: str
    name: str
    language: Optional[str]
    description: str
    tags: Tuple[str, ...]
    base_voice: Optional[str]
    variant: Optional[str]
    parameters: "OrderedDict[str, int]"
    default_language_profile: Optional[str]
    source_voice: Optional[str]
    extras: Dict[str, object]

    def display_label(self) -> str:
        pieces: List[str] = [self.name]
        if self.language:
            pieces.append(self.language)
        if self.description:
            pieces.append(self.description)
        return " – ".join(piece for piece in pieces if piece)

    def parameter_items(self) -> Iterator[Tuple[str, int]]:
        return self.parameters.items()


@dataclass
class EspeakVariant:
    """Lightweight representation of an eSpeak NG variant voice file."""

    id: str
    path: str
    name: str
    languages: Tuple[str, ...]
    gender: Optional[str]
    numbers: Dict[str, Tuple[float, ...]]
    comments: Tuple[str, ...]


_VARIANT_PARAMETER_ORDER = (
    "gender",
    "rate",
    "pitch",
    "inflection",
    "headSize",
    "roughness",
    "breathiness",
    "volume",
)

_BASE_PARAMETER_RANGE_SPECS: Dict[str, Dict[str, object]] = {
    "gender": {
        "label": "Gender resonance",
        "description": "0 = masculine tract target, 1 = feminine tract target.",
        "min": 0,
        "max": 1,
        "default": 0,
        "step": 1,
        "tags": ("timbre",),
    },
    "rate": {
        "label": "Speaking rate",
        "description": "Base speed in words per minute mapped to Eloquence's internal range.",
        "min": 40,
        "max": 150,
        "default": 100,
        "step": 1,
        "tags": ("timing",),
    },
    "pitch": {
        "label": "Pitch",
        "description": "Primary pitch target controlling overall brightness.",
        "min": 40,
        "max": 160,
        "default": 100,
        "step": 1,
        "tags": ("tone",),
    },
    "inflection": {
        "label": "Inflection",
        "description": "Amount of pitch modulation between syllables.",
        "min": 0,
        "max": 100,
        "default": 50,
        "step": 1,
        "tags": ("prosody",),
    },
    "headSize": {
        "label": "Head size",
        "description": "Formant scaling comparable to vocal tract length.",
        "min": 70,
        "max": 160,
        "default": 100,
        "step": 1,
        "tags": ("formant",),
    },
    "roughness": {
        "label": "Roughness",
        "description": "Noise component balancing rasp versus clarity.",
        "min": 0,
        "max": 120,
        "default": 40,
        "step": 1,
        "tags": ("texture",),
    },
    "breathiness": {
        "label": "Breathiness",
        "description": "Adds aspiration to soften consonants.",
        "min": 0,
        "max": 120,
        "default": 32,
        "step": 1,
        "tags": ("texture",),
    },
    "volume": {
        "label": "Volume",
        "description": "Output gain applied before NVDA's volume scaling.",
        "min": 50,
        "max": 100,
        "default": 80,
        "step": 1,
        "tags": ("loudness",),
    },
    "sampleRate": {
        "label": "Sample rate",
        "description": "Output rate in Hertz after optional resampling.",
        "min": 8000,
        "max": 48000,
        "default": 22050,
        "step": 50,
        "tags": ("output", "quality"),
    },
}

_DEFAULT_PARAMETER_RANGE_SPECS: Dict[str, Dict[str, object]] = {
    **_BASE_PARAMETER_RANGE_SPECS,
    **{name: dict(spec) for name, spec in ADVANCED_VOICE_PARAMETER_SPECS.items()},
}

_LANGUAGE_PROFILE_MAP = {
    "en": "en-us-basic",
    "en-us": "en-us-basic",
    "en-gb": "en-gb-basic",
    "es": "es-es-basic",
    "es-es": "es-es-basic",
    "es-419": "es-419-basic",
    "fr": "fr-fr-basic",
    "fr-fr": "fr-fr-basic",
    "de": "de-de-basic",
    "de-de": "de-de-basic",
    "it": "it-it-basic",
    "it-it": "it-it-basic",
    "pt": "pt-br-basic",
    "pt-br": "pt-br-basic",
    "hi": "hi-in-basic",
    "hi-in": "hi-in-basic",
    "ja": "ja-jp-basic",
    "ja-jp": "ja-jp-basic",
}


class VoiceCatalog:
    """Collection of :class:`VoiceTemplate` objects."""

    def __init__(
        self,
        parameter_ranges: Dict[str, VoiceParameterRange],
        templates: Iterable[VoiceTemplate],
        default_template_id: Optional[str] = None,
        metadata: Optional[Dict[str, object]] = None,
    ) -> None:
        self._parameter_ranges = dict(parameter_ranges)
        _ensure_default_parameter_ranges(self._parameter_ranges)
        self._templates: "OrderedDict[str, VoiceTemplate]" = OrderedDict()
        for template in templates:
            if not template.id:
                continue
            if template.id in self._templates:
                LOG.debug("Duplicate voice template identifier '%s' ignored", template.id)
                continue
            self._templates[template.id] = template
        self._default_template_id = default_template_id
        self.metadata = metadata or {}

    @property
    def is_empty(self) -> bool:
        return not self._templates

    def parameter_range(self, name: str) -> Optional[VoiceParameterRange]:
        return self._parameter_ranges.get(name)

    def parameter_ranges(self) -> Dict[str, VoiceParameterRange]:
        """Return a copy of the known parameter ranges."""

        return dict(self._parameter_ranges)

    def get(self, template_id: str) -> Optional[VoiceTemplate]:
        return self._templates.get(template_id)

    def __iter__(self) -> Iterator[VoiceTemplate]:
        return iter(self._templates.values())

    def templates(self) -> List[VoiceTemplate]:
        return list(self._templates.values())

    def default_template(self) -> Optional[VoiceTemplate]:
        if self._default_template_id:
            template = self.get(self._default_template_id)
            if template is not None:
                return template
        return next(iter(self._templates.values()), None)


def load_default_voice_catalog() -> VoiceCatalog:
    """Load the bundled voice catalogue shipping with the add-on."""

    payloads = []
    for source_id, path in _iter_voice_data_files():
        payload = _load_voice_payload(path)
        if payload is None:
            continue
        payloads.append((source_id, path, payload))
    if not payloads:
        LOG.info("No voice catalogue data found under %s", _VOICE_DATA_ROOT)
        return VoiceCatalog({}, [])

    parameter_ranges: Dict[str, VoiceParameterRange] = {}
    templates: List[VoiceTemplate] = []
    metadata: Dict[str, object] = {}
    source_metadata: List[Dict[str, object]] = []
    default_template_id: Optional[str] = None

    for source_id, path, payload in payloads:
        ranges = _parse_parameter_ranges(payload.get("parameters"))
        for name, range_info in ranges.items():
            parameter_ranges.setdefault(name, range_info)
        combined_ranges = dict(parameter_ranges)
        combined_ranges.update(ranges)
        raw_templates = payload.get("templates")
        if not isinstance(raw_templates, (list, tuple)):
            raw_templates = []
        templates.extend(_parse_templates(raw_templates, combined_ranges))

        meta_entry: Dict[str, object] = {}
        raw_metadata = payload.get("metadata")
        if isinstance(raw_metadata, dict):
            meta_entry.update(raw_metadata)
        meta_entry.setdefault("id", source_id)
        meta_entry.setdefault("file", os.path.relpath(path, _VOICE_DATA_ROOT))
        source_metadata.append(meta_entry)

        defaults = payload.get("defaults", {}) or {}
        if default_template_id is None and isinstance(defaults, dict):
            candidate = defaults.get("template")
            if candidate:
                default_template_id = candidate

    variant_templates, variant_metadata = _load_espeak_variants(parameter_ranges)
    if variant_templates:
        templates.extend(variant_templates)
    if variant_metadata:
        source_metadata.append(variant_metadata)

    if source_metadata:
        metadata["sources"] = source_metadata

    return VoiceCatalog(parameter_ranges, templates, default_template_id, metadata=metadata)


def _load_voice_payload(path: str) -> Optional[Dict[str, object]]:
    if not os.path.exists(path):
        LOG.debug("Voice catalogue file not found: %s", path)
        return None
    try:
        with open(path, "r", encoding="utf-8") as source:
            payload = json.load(source)
    except (OSError, json.JSONDecodeError):
        LOG.exception("Unable to read voice data from %s", path)
        return None
    if not isinstance(payload, dict):
        LOG.debug("Voice catalogue payload in %s is not an object", path)
        return None
    if not any(key in payload for key in ("templates", "variants", "parameters")):
        LOG.debug("Skipping %s because it does not contain voice template data", path)
        return None
    return payload


def _parse_parameter_ranges(raw: Optional[Dict[str, object]]) -> Dict[str, VoiceParameterRange]:
    ranges: Dict[str, VoiceParameterRange] = {}
    if not isinstance(raw, dict):
        if raw not in (None, {}):
            LOG.debug("Ignoring parameter payload because it is not a mapping: %r", raw)
        return ranges
    for name, data in raw.items():
        if not isinstance(data, dict):
            LOG.warning("Ignoring malformed parameter description for '%s'", name)
            continue
        try:
            minimum = int(data.get("min", 0))
            maximum = int(data.get("max", 0))
        except (TypeError, ValueError):
            LOG.warning("Parameter bounds for '%s' are invalid", name)
            continue
        if maximum < minimum:
            minimum, maximum = maximum, minimum
        try:
            default = int(data.get("default", minimum))
        except (TypeError, ValueError):
            default = minimum
        try:
            step = int(data.get("step", 1))
        except (TypeError, ValueError):
            step = 1
        tags: Tuple[str, ...]
        raw_tags = data.get("tags", ())
        if isinstance(raw_tags, (list, tuple)):
            tags = tuple(str(tag) for tag in raw_tags)
        elif isinstance(raw_tags, str):
            tags = (raw_tags,)
        else:
            tags = ()
        range_obj = VoiceParameterRange(
            name=name,
            label=str(data.get("label", name.title())),
            minimum=minimum,
            maximum=maximum,
            default=default,
            step=step,
            description=str(data.get("description", "")),
            tags=tags,
        )
        ranges[name] = range_obj
    return ranges


def _parse_templates(
    raw_templates: Iterable[object],
    parameter_ranges: Dict[str, VoiceParameterRange],
) -> List[VoiceTemplate]:
    templates: List[VoiceTemplate] = []
    for entry in raw_templates:
        if not isinstance(entry, dict):
            LOG.warning("Skipping malformed template description: %r", entry)
            continue
        template_id = entry.get("id")
        if not template_id:
            LOG.warning("Voice template without an identifier ignored: %r", entry)
            continue
        parameters = OrderedDict()
        raw_parameters = entry.get("parameters", {})
        if isinstance(raw_parameters, dict):
            for name, raw_value in raw_parameters.items():
                if isinstance(raw_value, (int, float)):
                    value = int(raw_value)
                elif isinstance(raw_value, str):
                    try:
                        value = int(raw_value.strip())
                    except ValueError:
                        LOG.debug("Parameter '%s' on template '%s' is not numeric", name, template_id)
                        continue
                else:
                    continue
                range_info = parameter_ranges.get(name)
                if range_info is not None:
                    value = range_info.clamp(value)
                parameters[name] = value
        tags: Tuple[str, ...]
        raw_tags = entry.get("tags", ())
        if isinstance(raw_tags, (list, tuple)):
            tags = tuple(str(tag) for tag in raw_tags)
        elif isinstance(raw_tags, str):
            tags = (raw_tags,)
        else:
            tags = ()
        template = VoiceTemplate(
            id=str(template_id),
            name=str(entry.get("name", template_id)),
            language=entry.get("language"),
            description=str(entry.get("description", "")),
            tags=tags,
            base_voice=entry.get("baseVoice"),
            variant=str(entry["variant"]) if "variant" in entry else None,
            parameters=parameters,
            default_language_profile=entry.get("defaultLanguageProfile"),
            source_voice=entry.get("sourceVoice"),
            extras=entry.get("extras", {}),
        )
        templates.append(template)
    return templates


def _load_espeak_variants(
    parameter_ranges: Dict[str, VoiceParameterRange]
) -> Tuple[List[VoiceTemplate], Optional[Dict[str, object]]]:
    if not os.path.isdir(_ESPEAK_VARIANT_DIR):
        return [], None

    _ensure_default_parameter_ranges(parameter_ranges)

    templates: List[VoiceTemplate] = []
    failed = 0
    for variant_id, path in _iter_espeak_variant_files():
        variant = _parse_espeak_variant(variant_id, path)
        if variant is None:
            failed += 1
            continue
        template = _build_template_from_variant(variant, parameter_ranges)
        if template is None:
            failed += 1
            continue
        templates.append(template)

    metadata: Optional[Dict[str, object]] = None
    if templates or failed:
        metadata = {
            "id": "espeak-variants",
            "file": os.path.relpath(_ESPEAK_VARIANT_DIR, _VOICE_DATA_ROOT),
            "count": len(templates),
            "notes": "Imported from eSpeak NG variant voice definitions",
        }
        if failed:
            metadata["failed"] = failed
    return templates, metadata


def _iter_espeak_variant_files() -> Iterator[Tuple[str, str]]:
    if not os.path.isdir(_ESPEAK_VARIANT_DIR):
        return
    seen: Set[str] = set()

    def register(path: str) -> Optional[Tuple[str, str]]:
        absolute = os.path.abspath(path)
        if absolute in seen:
            return None
        seen.add(absolute)
        variant_id = _source_id_from_path(absolute)
        return variant_id, absolute

    for root, _dirs, files in os.walk(_ESPEAK_VARIANT_DIR):
        for name in sorted(files):
            if name.startswith("."):
                continue
            path = os.path.join(root, name)
            if not os.path.isfile(path):
                continue
            result = register(path)
            if result:
                yield result


def _parse_espeak_variant(variant_id: str, path: str) -> Optional[EspeakVariant]:
    try:
        with open(path, "r", encoding="utf-8") as source:
            languages: List[str] = []
            gender: Optional[str] = None
            numbers: Dict[str, Tuple[float, ...]] = {}
            comments: List[str] = []
            name = variant_id
            for raw_line in source:
                stripped = raw_line.strip()
                if not stripped:
                    continue
                if stripped.startswith("//"):
                    comment = stripped.lstrip("/").strip()
                    if comment:
                        comments.append(comment)
                    continue
                if stripped.startswith("#") or stripped.startswith(";"):
                    continue
                parts = stripped.split()
                if not parts:
                    continue
                key = parts[0].lower()
                values = parts[1:]
                if key == "name":
                    if len(parts) > 1:
                        name = stripped.split(None, 1)[1].strip()
                    continue
                if key == "language":
                    if values:
                        token = values[0]
                        if token.lower() != "variant":
                            normalized = _normalize_language_tag(token)
                            if normalized and normalized not in languages:
                                languages.append(normalized)
                    continue
                if key == "gender":
                    gender_value = " ".join(values).strip()
                    gender = gender_value or gender
                    continue
                numeric_values: List[float] = []
                convertible = True
                for value in values:
                    try:
                        numeric_values.append(float(value))
                    except ValueError:
                        convertible = False
                        break
                if convertible and numeric_values:
                    numbers[key] = tuple(numeric_values)
            return EspeakVariant(
                id=variant_id,
                path=path,
                name=name or variant_id,
                languages=tuple(languages),
                gender=gender,
                numbers=numbers,
                comments=tuple(comments),
            )
    except OSError:
        LOG.exception("Unable to read eSpeak variant data from %s", path)
    return None


def _build_template_from_variant(
    variant: EspeakVariant, parameter_ranges: Dict[str, VoiceParameterRange]
) -> Optional[VoiceTemplate]:
    parameters: "OrderedDict[str, int]" = OrderedDict()
    for name in _VARIANT_PARAMETER_ORDER:
        range_info = parameter_ranges.get(name)
        default = range_info.default if range_info else 0
        parameters[name] = default

    gender_range = parameter_ranges.get("gender")
    if gender_range is not None:
        gender_value = 0
        if variant.gender:
            lowered = variant.gender.lower()
            if "female" in lowered or lowered.startswith("f"):
                gender_value = 1
        parameters["gender"] = gender_range.clamp(int(gender_value))

    rate_range = parameter_ranges.get("rate")
    speed = _variant_scalar(variant, "speed")
    if speed is None:
        words = variant.numbers.get("words")
        if words:
            speed = _variant_mean(words)
    if speed is not None and rate_range is not None:
        parameters["rate"] = _map_speed_to_rate(speed, rate_range)

    pitch_values = variant.numbers.get("pitch")
    pitch_base = pitch_values[0] if pitch_values else None
    pitch_range = pitch_values[1] if pitch_values and len(pitch_values) > 1 else None
    pitch_range_info = parameter_ranges.get("pitch")
    if pitch_base is not None and pitch_range_info is not None:
        parameters["pitch"] = pitch_range_info.clamp(int(round(pitch_base)))

    inflection_target = _map_pitch_range_to_inflection(
        pitch_range,
        _variant_scalar(variant, "intonation"),
    )
    inflection_range = parameter_ranges.get("inflection")
    if inflection_target is not None and inflection_range is not None:
        parameters["inflection"] = inflection_range.clamp(int(round(inflection_target)))

    consonant_values = variant.numbers.get("consonants")
    head_range = parameter_ranges.get("headSize")
    if consonant_values and head_range is not None:
        parameters["headSize"] = head_range.clamp(int(round(_variant_mean(consonant_values))))

    roughness_value = _variant_scalar(variant, "roughness")
    rough_range = parameter_ranges.get("roughness")
    if roughness_value is not None and rough_range is not None:
        parameters["roughness"] = rough_range.clamp(int(round(roughness_value)))

    breath_values = variant.numbers.get("breath") or variant.numbers.get("breathw")
    breathiness_range = parameter_ranges.get("breathiness")
    if breath_values and breathiness_range is not None:
        parameters["breathiness"] = breathiness_range.clamp(
            int(round(_variant_mean(breath_values)))
        )
    else:
        breath_scalar = _variant_scalar(variant, "breath")
        if breath_scalar is not None and breathiness_range is not None:
            parameters["breathiness"] = breathiness_range.clamp(int(round(breath_scalar)))

    volume_range = parameter_ranges.get("volume")
    volume_value = _variant_scalar(variant, "volume")
    if volume_value is None:
        voicing_value = _variant_scalar(variant, "voicing")
        if voicing_value is not None:
            volume_value = 40.0 + 0.5 * voicing_value
    if volume_value is not None and volume_range is not None:
        parameters["volume"] = volume_range.clamp(int(round(volume_value)))

    language = next(iter(variant.languages), None)
    normalized_language = language if language is None else _normalize_language_tag(language)

    tags: List[str] = ["espeak", "variant"]
    for lang in variant.languages:
        tags.append(f"lang:{lang.lower()}")
    if variant.gender:
        tags.append(variant.gender.lower())
    unique_tags = tuple(dict.fromkeys(tags))

    return VoiceTemplate(
        id=f"espeak-variant-{variant.id}",
        name=variant.name or variant.id,
        language=normalized_language,
        description=_variant_description(variant),
        tags=unique_tags,
        base_voice=None,
        variant=None,
        parameters=parameters,
        default_language_profile=_guess_language_profile(variant.languages),
        source_voice=variant.name or variant.id,
        extras={},
    )


def _variant_description(variant: EspeakVariant) -> str:
    label = variant.name or variant.id
    pieces: List[str] = [f"Imported from eSpeak NG variant '{label}'"]
    if variant.languages:
        pieces.append("Languages: " + ", ".join(variant.languages))
    if variant.comments:
        pieces.append("; ".join(comment for comment in variant.comments if comment))
    return " – ".join(piece for piece in pieces if piece)


def _variant_scalar(variant: EspeakVariant, key: str) -> Optional[float]:
    values = variant.numbers.get(key)
    if not values:
        return None
    return values[0]


def _variant_mean(values: Tuple[float, ...]) -> float:
    if not values:
        return 0.0
    return sum(values) / float(len(values))


def _map_speed_to_rate(speed: float, range_info: VoiceParameterRange) -> int:
    default_speed = 170.0
    default_rate = range_info.default or 100
    scale = default_speed / default_rate if default_rate else 1.0
    if scale <= 0:
        scale = 1.0
    return range_info.clamp(int(round(speed / scale)))


def _map_pitch_range_to_inflection(
    pitch_range: Optional[float], intonation: Optional[float]
) -> Optional[float]:
    if pitch_range is not None:
        return pitch_range * 0.6
    if intonation is not None:
        return 40.0 + (intonation * 10.0)
    return None


def _ensure_default_parameter_ranges(
    parameter_ranges: Dict[str, VoiceParameterRange]
) -> None:
    for name, spec in _DEFAULT_PARAMETER_RANGE_SPECS.items():
        if name in parameter_ranges:
            continue
        parameter_ranges[name] = VoiceParameterRange(
            name=name,
            label=str(spec.get("label", name.title())),
            minimum=int(spec.get("min", 0)),
            maximum=int(spec.get("max", 0)),
            default=int(spec.get("default", 0)),
            step=int(spec.get("step", 1)),
            description=str(spec.get("description", "")),
            tags=tuple(spec.get("tags", ())),
        )


def _normalize_language_tag(tag: str) -> str:
    parts = tag.replace("_", "-").split("-")
    normalized: List[str] = []
    for index, part in enumerate(parts):
        if not part:
            continue
        if index == 0:
            normalized.append(part.lower())
        elif len(part) == 2:
            normalized.append(part.upper())
        elif len(part) == 4:
            normalized.append(part.title())
        else:
            normalized.append(part.lower())
    return "-".join(normalized)


def _guess_language_profile(languages: Tuple[str, ...]) -> Optional[str]:
    for language in languages:
        key = language.lower()
        if key in _LANGUAGE_PROFILE_MAP:
            return _LANGUAGE_PROFILE_MAP[key]
        base = key.split("-", 1)[0]
        if base in _LANGUAGE_PROFILE_MAP:
            return _LANGUAGE_PROFILE_MAP[base]
    return None
