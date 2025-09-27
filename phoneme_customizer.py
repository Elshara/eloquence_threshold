"""Helpers for managing phoneme-focused EQ, voice scenes, and configuration exports."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from voice_parameters import ADVANCED_VOICE_PARAMETER_SPECS, advanced_parameter_defaults


_DEFAULT_LOW_HZ = 200
_DEFAULT_HIGH_HZ = 3400
_DEFAULT_GAIN_DB = 0.0
_DEFAULT_FILTER_TYPE = "peaking"
_DEFAULT_Q = 1.0
_MIN_Q = 0.05
_MAX_Q = 50.0

PHONEME_EQ_DEFAULT_FILTER = _DEFAULT_FILTER_TYPE
PHONEME_EQ_MIN_Q = _MIN_Q
PHONEME_EQ_MAX_Q = _MAX_Q


# The synthesizer currently implements bell-style parametric filters but we
# record the broader taxonomy so future APO integrations can map the stored
# metadata directly onto Windows' pre-mix/post-mix stages.
VALID_FILTER_TYPES: Tuple[str, ...] = (
    "peaking",
    "lowShelf",
    "highShelf",
    "lowPass",
    "highPass",
    "bandPass",
    "notch",
    "allPass",
)


def _normalise_filter_type(value: object) -> str:
    if isinstance(value, str):
        lowered = value.strip()
        if lowered:
            canonical = lowered[0].lower() + lowered[1:]
            if canonical in VALID_FILTER_TYPES:
                return canonical
    return _DEFAULT_FILTER_TYPE


def _coerce_q(value: object) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return _DEFAULT_Q
    if not math.isfinite(numeric):
        return _DEFAULT_Q
    if numeric < _MIN_Q:
        return _MIN_Q
    if numeric > _MAX_Q:
        return _MAX_Q
    return numeric


def _derive_q(low_hz: float, high_hz: float, fallback: float) -> float:
    try:
        low = float(low_hz)
        high = float(high_hz)
    except (TypeError, ValueError):
        return _coerce_q(fallback)
    if low <= 0 or high <= 0 or not math.isfinite(low) or not math.isfinite(high):
        return _coerce_q(fallback)
    if high <= low:
        return _coerce_q(fallback)
    ratio = high / low
    if ratio <= 1.0:
        return _coerce_q(fallback)
    try:
        q_value = 1.0 / (2.0 * math.log(ratio, 2.0))
    except (ValueError, ZeroDivisionError):
        return _coerce_q(fallback)
    return _coerce_q(q_value)


@dataclass
class PhonemeEqBand:
    """Container representing a single parametric EQ band."""

    low_hz: float = _DEFAULT_LOW_HZ
    high_hz: float = _DEFAULT_HIGH_HZ
    gain_db: float = _DEFAULT_GAIN_DB
    filter_type: str = _DEFAULT_FILTER_TYPE
    q: float = _DEFAULT_Q

    def clamp(
        self,
        low_min: float,
        high_max: float,
        gain_min: float,
        gain_max: float,
    ) -> "PhonemeEqBand":
        low = max(low_min, min(float(self.low_hz), high_max - 1.0))
        high = max(low + 1.0, min(float(self.high_hz), high_max))
        gain = max(gain_min, min(float(self.gain_db), gain_max))
        filter_type = _normalise_filter_type(self.filter_type)
        q_value = _coerce_q(self.q)
        band = PhonemeEqBand(low, high, gain, filter_type, q_value)
        if filter_type == "peaking":
            band = band.with_derived_q()
        return band

    def to_storage_mapping(self) -> Dict[str, float]:
        return {
            "lowHz": float(self.low_hz),
            "highHz": float(self.high_hz),
            "gainDb": float(self.gain_db),
            "filterType": self.filter_type,
            "q": float(self.q),
        }

    def to_engine_mapping(self) -> Dict[str, float]:
        return {
            "low_hz": float(self.low_hz),
            "high_hz": float(self.high_hz),
            "gain_db": float(self.gain_db),
            "filter_type": self.filter_type,
            "q": float(self.q),
        }

    @classmethod
    def default(cls) -> "PhonemeEqBand":
        return cls()

    @classmethod
    def from_peak_filter(
        cls,
        center_hz: float,
        gain_db: float,
        q: float,
        *,
        sample_rate: Optional[float] = None,
    ) -> Optional["PhonemeEqBand"]:
        """Approximate a constant-Q peak filter with symmetric low/high bounds."""

        try:
            center = float(center_hz)
            gain = float(gain_db)
            q_value = float(q)
        except (TypeError, ValueError):
            return None
        if not (math.isfinite(center) and math.isfinite(gain) and math.isfinite(q_value)):
            return None
        if center <= 0.0 or q_value <= 0.0:
            return None

        q_value = max(q_value, 1e-6)
        ratio = math.pow(2.0, 1.0 / (2.0 * q_value))
        low = max(1.0, center / ratio)
        high = center * ratio

        if sample_rate and sample_rate > 0:
            nyquist = float(sample_rate) / 2.0
            if nyquist > 1.0:
                low = min(low, nyquist - 1.0)
            high = min(high, nyquist)
        if high <= low:
            high = low + 1.0

        return cls(low, high, gain, _DEFAULT_FILTER_TYPE, max(_MIN_Q, min(q_value, _MAX_Q))).with_derived_q()

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, object]) -> Optional["PhonemeEqBand"]:
        if not isinstance(mapping, Mapping):
            return None
        low = mapping.get("lowHz", mapping.get("low_hz", _DEFAULT_LOW_HZ))
        high = mapping.get("highHz", mapping.get("high_hz", _DEFAULT_HIGH_HZ))
        gain = mapping.get("gainDb", mapping.get("gain_db", _DEFAULT_GAIN_DB))
        filter_type = mapping.get("filterType", mapping.get("filter_type", _DEFAULT_FILTER_TYPE))
        q_value = mapping.get("q", mapping.get("quality", _DEFAULT_Q))
        try:
            low_val = float(low)
            high_val = float(high)
            gain_val = float(gain)
        except (TypeError, ValueError):
            return None
        filter_kind = _normalise_filter_type(filter_type)
        try:
            q_val = float(q_value)
        except (TypeError, ValueError):
            q_val = _DEFAULT_Q
        band = cls(low_val, high_val, gain_val, filter_kind, _coerce_q(q_val))
        if filter_kind == "peaking":
            return band.with_derived_q()
        return band

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------
    def with_derived_q(self) -> "PhonemeEqBand":
        return PhonemeEqBand(
            self.low_hz,
            self.high_hz,
            self.gain_db,
            self.filter_type,
            _derive_q(self.low_hz, self.high_hz, self.q),
        )

    def apply_q(self, q_value: float, low_min: float, high_max: float) -> "PhonemeEqBand":
        q_clamped = _coerce_q(q_value)
        center = self.center_frequency()
        if center <= 0.0:
            center = max(low_min, min(self.high_hz, self.low_hz + 1.0))
        ratio = math.pow(2.0, 1.0 / (2.0 * max(q_clamped, 1e-6)))
        low = max(low_min, min(center / ratio, high_max - 1.0))
        high = min(high_max, max(low + 1.0, center * ratio))
        return PhonemeEqBand(low, high, self.gain_db, self.filter_type, q_clamped)

    def center_frequency(self) -> float:
        return math.sqrt(max(1.0, self.low_hz) * max(1.0, self.high_hz))


@dataclass(frozen=True)
class VoiceScene:
    """Declarative description of a reusable phoneme/parameter scene."""

    name: str
    description: str
    sample_rate_hz: Optional[float] = None
    global_parameters: Mapping[str, object] = field(default_factory=dict)
    phoneme_overrides: Mapping[str, Iterable[Mapping[str, object]]] = field(default_factory=dict)
    tags: Sequence[str] = field(default_factory=tuple)
    archive_sources: Sequence[str] = field(default_factory=tuple)
    language_focus: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        sample_rate: Optional[float]
        try:
            sample_rate = float(self.sample_rate_hz) if self.sample_rate_hz is not None else None
        except (TypeError, ValueError):
            sample_rate = None
        if sample_rate is not None and (not math.isfinite(sample_rate) or sample_rate <= 0.0):
            sample_rate = None
        object.__setattr__(self, "sample_rate_hz", sample_rate)

        object.__setattr__(self, "tags", _normalise_string_iterable(self.tags))
        object.__setattr__(self, "archive_sources", _normalise_string_iterable(self.archive_sources))
        object.__setattr__(self, "language_focus", _normalise_string_iterable(self.language_focus))

        global_parameters = {}
        for key, value in (self.global_parameters or {}).items():
            if not isinstance(key, str):
                continue
            global_parameters[key] = value
        object.__setattr__(self, "global_parameters", global_parameters)

        overrides: Dict[str, List[Dict[str, Any]]] = {}
        for phoneme_id, entries in (self.phoneme_overrides or {}).items():
            if not isinstance(phoneme_id, str):
                continue
            parsed_entries: List[Dict[str, Any]] = []
            iterable: Iterable[Mapping[str, object]]
            if isinstance(entries, Mapping):
                iterable = [entries]  # type: ignore[list-item]
            elif isinstance(entries, Iterable):
                iterable = entries  # type: ignore[assignment]
            else:
                continue
            for entry in iterable:
                if not isinstance(entry, Mapping):
                    continue
                parsed_entries.append(dict(entry))
            if parsed_entries:
                overrides[phoneme_id] = parsed_entries
        object.__setattr__(self, "phoneme_overrides", overrides)

    # ------------------------------------------------------------------
    # Metadata helpers
    # ------------------------------------------------------------------
    def metadata(self) -> Dict[str, object]:
        """Return metadata describing provenance and focus."""

        return {
            "tags": list(self.tags),
            "archiveSources": list(self.archive_sources),
            "languageFocus": list(self.language_focus),
            "sampleRateHz": self.sample_rate_hz,
        }


class PhonemeCustomizer:
    """Maintains global and per-phoneme EQ definitions."""

    def __init__(
        self,
        low_min: float = 1.0,
        high_max: float = 384000.0,
        gain_min: float = -24.0,
        gain_max: float = 12.0,
    ) -> None:
        self._low_min = float(low_min)
        self._absolute_high_max = float(high_max)
        self._high_max = float(high_max)
        self._gain_min = gain_min
        self._gain_max = gain_max
        self._phoneme_bands: Dict[str, List[PhonemeEqBand]] = {}
        self._global_parameters: Dict[str, int] = advanced_parameter_defaults()
        self._global_bands: List[PhonemeEqBand] = []
        self._rebuild_global_bands()

    # ------------------------------------------------------------------
    # Global parameter handling
    # ------------------------------------------------------------------
    def global_parameter_names(self) -> Iterable[str]:
        return self._global_parameters.keys()

    def global_parameter_value(self, name: str) -> int:
        return int(self._global_parameters.get(name, ADVANCED_VOICE_PARAMETER_SPECS.get(name, {}).get("default", 100)))

    def apply_global_parameters(self, values: Mapping[str, object]) -> None:
        if not isinstance(values, Mapping):
            return
        updated = False
        for name, raw in values.items():
            if name not in ADVANCED_VOICE_PARAMETER_SPECS:
                continue
            spec = ADVANCED_VOICE_PARAMETER_SPECS[name]
            try:
                numeric = int(raw)
            except (TypeError, ValueError):
                continue
            clamped = _clamp(numeric, spec.get("min", 0), spec.get("max", 200))
            if self._global_parameters.get(name) != clamped:
                self._global_parameters[name] = clamped
                updated = True
        if updated:
            self._rebuild_global_bands()

    def set_global_parameter(self, name: str, value: int) -> int:
        if name not in ADVANCED_VOICE_PARAMETER_SPECS:
            raise KeyError(name)
        spec = ADVANCED_VOICE_PARAMETER_SPECS[name]
        clamped = _clamp(value, spec.get("min", 0), spec.get("max", 200))
        if self._global_parameters.get(name) != clamped:
            self._global_parameters[name] = clamped
            self._rebuild_global_bands()
        return clamped

    def global_parameter_values(self) -> Dict[str, int]:
        return dict(self._global_parameters)

    def clone(self) -> "PhonemeCustomizer":
        """Return a deep copy preserving limits and state."""

        clone = PhonemeCustomizer(self._low_min, self._absolute_high_max, self._gain_min, self._gain_max)
        clone._high_max = self._high_max
        clone._global_parameters = dict(self._global_parameters)
        clone._rebuild_global_bands()
        clone._phoneme_bands = {
            phoneme_id: [
                PhonemeEqBand(band.low_hz, band.high_hz, band.gain_db, band.filter_type, band.q)
                for band in bands
            ]
            for phoneme_id, bands in self._phoneme_bands.items()
        }
        return clone

    def reset_to_defaults(self) -> None:
        """Clear per-phoneme EQ and restore default slider positions."""

        self._global_parameters = advanced_parameter_defaults()
        self._phoneme_bands = {}
        self._rebuild_global_bands()

    def _rebuild_global_bands(self) -> None:
        bands: List[PhonemeEqBand] = []

        for name, value in self._global_parameters.items():
            scale = _scale(value)
            if not scale:
                continue
            spec = ADVANCED_VOICE_PARAMETER_SPECS.get(name)
            if not spec:
                continue
            profile = spec.get("profile", {})
            base_gain = float(profile.get("gain", 6.0)) * scale
            default_filter_type = _normalise_filter_type(profile.get("filterType", _DEFAULT_FILTER_TYPE))
            default_q = _coerce_q(profile.get("q", _DEFAULT_Q))

            band_entries = profile.get("bands")
            if band_entries:
                for entry in band_entries:
                    if not isinstance(entry, Mapping):
                        continue
                    range_value = entry.get("range")
                    if not isinstance(range_value, (tuple, list)) or len(range_value) != 2:
                        continue
                    try:
                        low, high = float(range_value[0]), float(range_value[1])
                    except (TypeError, ValueError):
                        continue
                    gain_multiplier = entry.get("gainMultiplier", 1.0)
                    try:
                        multiplier = float(gain_multiplier)
                    except (TypeError, ValueError):
                        multiplier = 1.0
                    gain_value = base_gain * multiplier
                    if not math.isfinite(gain_value) or abs(gain_value) < 0.05:
                        continue
                    candidate = PhonemeEqBand(
                        low,
                        high,
                        gain_value,
                        _normalise_filter_type(entry.get("filterType", default_filter_type)),
                        _coerce_q(entry.get("q", default_q)),
                    ).clamp(self._low_min, self._high_max, self._gain_min, self._gain_max)
                    if "q" in entry:
                        candidate = candidate.apply_q(
                            _coerce_q(entry.get("q", default_q)), self._low_min, self._high_max
                        )
                    bands.append(candidate)
                continue

            ranges = profile.get("ranges")
            if not ranges and "range" in profile:
                ranges = (profile.get("range"),)
            if not ranges:
                continue
            for range_value in ranges:
                if not isinstance(range_value, (tuple, list)) or len(range_value) != 2:
                    continue
                try:
                    low, high = float(range_value[0]), float(range_value[1])
                except (TypeError, ValueError):
                    continue
                if not math.isfinite(base_gain) or abs(base_gain) < 0.05:
                    continue
                candidate = PhonemeEqBand(
                    low,
                    high,
                    base_gain,
                    default_filter_type,
                    default_q,
                ).clamp(self._low_min, self._high_max, self._gain_min, self._gain_max)
                if "q" in profile:
                    candidate = candidate.apply_q(default_q, self._low_min, self._high_max)
                bands.append(candidate)
        self._global_bands = bands

    # ------------------------------------------------------------------
    # Per-phoneme EQ handling
    # ------------------------------------------------------------------
    def ensure_layers(self, phoneme_id: str, layer: int) -> List[PhonemeEqBand]:
        if layer < 1:
            layer = 1
        bands = self._phoneme_bands.setdefault(phoneme_id, [PhonemeEqBand.default()])
        while len(bands) < layer:
            bands.append(PhonemeEqBand.default())
        return bands

    def layer_count(self, phoneme_id: Optional[str]) -> int:
        if not phoneme_id:
            return 0
        return len(self._phoneme_bands.get(phoneme_id, []))

    def set_sample_rate(self, sample_rate_hz: float) -> float:
        """Clamp EQ bands so they remain valid for the active sample rate."""

        try:
            numeric = float(sample_rate_hz)
        except (TypeError, ValueError):
            numeric = 0.0
        if numeric <= 0:
            limit = self._absolute_high_max
        else:
            limit = min(self._absolute_high_max, numeric / 2.0)
        limit = max(self._low_min + 1.0, limit)
        if math.isclose(limit, self._high_max, rel_tol=1e-6, abs_tol=1e-6):
            return self._high_max
        self._high_max = limit
        # Rebuild global bands so they honour the tighter headroom.
        self._rebuild_global_bands()
        # Clamp per-phoneme bands in place so persisted values remain valid.
        for phoneme_id, bands in list(self._phoneme_bands.items()):
            clamped = [
                band.clamp(self._low_min, self._high_max, self._gain_min, self._gain_max)
                for band in bands
            ]
            self._phoneme_bands[phoneme_id] = clamped
        return self._high_max

    def band_for_layer(self, phoneme_id: str, index: int) -> PhonemeEqBand:
        bands = self.ensure_layers(phoneme_id, index + 1)
        return bands[index]

    def set_band(self, phoneme_id: str, index: int, band: PhonemeEqBand) -> None:
        bands = self.ensure_layers(phoneme_id, index + 1)
        bands[index] = band.clamp(self._low_min, self._high_max, self._gain_min, self._gain_max)

    def per_phoneme_bands(self) -> Dict[str, List[PhonemeEqBand]]:
        return self._phoneme_bands

    def headroom_hz(self) -> float:
        """Return the maximum usable frequency after sample-rate clamping."""

        return self._high_max

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------
    def serialise_per_phoneme(self) -> Dict[str, List[Dict[str, float]]]:
        payload: Dict[str, List[Dict[str, float]]] = {}
        for phoneme_id, bands in self._phoneme_bands.items():
            serialised = [band.clamp(self._low_min, self._high_max, self._gain_min, self._gain_max).to_storage_mapping() for band in bands]
            if serialised:
                payload[phoneme_id] = serialised
        return payload

    def load_per_phoneme(self, payload: Mapping[str, object]) -> None:
        if not isinstance(payload, Mapping):
            return
        parsed: Dict[str, List[PhonemeEqBand]] = {}
        for phoneme_id, entries in payload.items():
            if not isinstance(phoneme_id, str):
                continue
            if isinstance(entries, Mapping):
                # Accept legacy single-band mapping
                entries_iterable = [entries]
            elif isinstance(entries, Iterable):
                entries_iterable = list(entries)
            else:
                continue
            bands: List[PhonemeEqBand] = []
            for entry in entries_iterable:
                band = PhonemeEqBand.from_mapping(entry)
                if band is None:
                    continue
                bands.append(band.clamp(self._low_min, self._high_max, self._gain_min, self._gain_max))
            if bands:
                parsed[phoneme_id] = bands
        if parsed:
            self._phoneme_bands = parsed

    # ------------------------------------------------------------------
    # Engine payload
    # ------------------------------------------------------------------
    def build_engine_payload(self) -> List[Dict[str, float]]:
        payload: List[Dict[str, float]] = [band.to_engine_mapping() for band in self._global_bands]
        for bands in self._phoneme_bands.values():
            payload.extend(band.to_engine_mapping() for band in bands)
        return payload

    def build_configuration_snapshot(self) -> Dict[str, object]:
        """Summarise the current configuration for NVDA storage."""

        snapshot: Dict[str, object] = {
            "advancedVoiceParameters": self.global_parameter_values(),
            "perPhonemeEq": self.serialise_per_phoneme(),
            "limits": {
                "lowHzMinimum": self._low_min,
                "highHzMaximum": self._high_max,
                "gainDbMinimum": self._gain_min,
                "gainDbMaximum": self._gain_max,
            },
            "enginePayload": self.build_engine_payload(),
        }
        snapshot["headroomHz"] = self.headroom_hz()
        return snapshot

    # ------------------------------------------------------------------
    # Scene helpers
    # ------------------------------------------------------------------
    def apply_scene(self, scene: VoiceScene) -> None:
        """Apply a :class:`VoiceScene` definition to the customiser."""

        if scene.sample_rate_hz:
            self.set_sample_rate(scene.sample_rate_hz)
        if scene.global_parameters:
            self.apply_global_parameters(scene.global_parameters)
        if scene.phoneme_overrides:
            self.load_per_phoneme(scene.phoneme_overrides)


def _scale(value: int, neutral: int = 100, span: int = 100) -> float:
    try:
        scaled = (int(value) - neutral) / float(span)
    except Exception:
        return 0.0
    return max(-1.0, min(1.0, scaled))


def _clamp(value: int, minimum: object, maximum: object) -> int:
    try:
        numeric = int(value)
    except (TypeError, ValueError):
        numeric = int(minimum) if isinstance(minimum, int) else 0
    min_val = int(minimum) if isinstance(minimum, int) else 0
    max_val = int(maximum) if isinstance(maximum, int) else 200
    if numeric < min_val:
        return min_val
    if numeric > max_val:
        return max_val
    return numeric


def _normalise_string_iterable(values: Sequence[str]) -> Tuple[str, ...]:
    unique: Dict[str, None] = {}
    for value in values or ():
        if not isinstance(value, str):
            continue
        trimmed = value.strip()
        if not trimmed:
            continue
        canonical = trimmed[0].lower() + trimmed[1:]
        unique[canonical] = None
    return tuple(sorted(unique.keys()))


def build_scene_snapshot(
    scene: VoiceScene,
    *,
    base_customizer: Optional[PhonemeCustomizer] = None,
) -> Dict[str, object]:
    """Render a :class:`VoiceScene` into a configuration snapshot."""

    working = base_customizer.clone() if base_customizer else PhonemeCustomizer()
    working.reset_to_defaults()
    working.apply_scene(scene)
    configuration = working.build_configuration_snapshot()
    metadata = scene.metadata()
    headroom = working.headroom_hz()
    metadata["headroomHz"] = headroom
    if metadata.get("sampleRateHz") is None and headroom > 0:
        metadata["sampleRateHz"] = headroom * 2.0
    return {
        "name": scene.name,
        "description": scene.description,
        "metadata": metadata,
        "configuration": configuration,
    }


__all__ = [
    "PhonemeCustomizer",
    "PhonemeEqBand",
    "VoiceScene",
    "build_scene_snapshot",
]

