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
from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

LOG = logging.getLogger(__name__)

_DATA_FILES = (
    ("espeak", os.path.join(os.path.dirname(__file__), "eloquence_data", "espeak_voices.json")),
    ("dectalk", os.path.join(os.path.dirname(__file__), "eloquence_data", "dectalk_voices.json")),
)


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
    for source_id, path in _DATA_FILES:
        payload = _load_voice_payload(path)
        if payload is None:
            continue
        payloads.append((source_id, path, payload))
    if not payloads:
        LOG.info("No voice catalogue data found in %s", [path for _, path in _DATA_FILES])
        return VoiceCatalog({}, [])

    parameter_ranges: Dict[str, VoiceParameterRange] = {}
    templates: List[VoiceTemplate] = []
    metadata: Dict[str, object] = {}
    source_metadata: List[Dict[str, object]] = []
    default_template_id: Optional[str] = None

    for source_id, path, payload in payloads:
        ranges = _parse_parameter_ranges(payload.get("parameters", {}))
        for name, range_info in ranges.items():
            parameter_ranges.setdefault(name, range_info)
        combined_ranges = dict(parameter_ranges)
        combined_ranges.update(ranges)
        templates.extend(_parse_templates(payload.get("templates", []), combined_ranges))

        meta_entry: Dict[str, object] = {}
        raw_metadata = payload.get("metadata")
        if isinstance(raw_metadata, dict):
            meta_entry.update(raw_metadata)
        meta_entry.setdefault("id", source_id)
        meta_entry.setdefault("file", os.path.basename(path))
        source_metadata.append(meta_entry)

        defaults = payload.get("defaults", {}) or {}
        if default_template_id is None and isinstance(defaults, dict):
            candidate = defaults.get("template")
            if candidate:
                default_template_id = candidate

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
        LOG.warning("Voice catalogue payload in %s is not an object", path)
        return None
    return payload


def _parse_parameter_ranges(raw: Dict[str, object]) -> Dict[str, VoiceParameterRange]:
    ranges: Dict[str, VoiceParameterRange] = {}
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
