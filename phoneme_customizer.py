"""Helpers for managing phoneme-focused EQ and extended voice controls."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional

from voice_parameters import ADVANCED_VOICE_PARAMETER_SPECS, advanced_parameter_defaults


_DEFAULT_LOW_HZ = 200
_DEFAULT_HIGH_HZ = 3400
_DEFAULT_GAIN_DB = 0.0


@dataclass
class PhonemeEqBand:
    """Container representing a single parametric EQ band."""

    low_hz: float = _DEFAULT_LOW_HZ
    high_hz: float = _DEFAULT_HIGH_HZ
    gain_db: float = _DEFAULT_GAIN_DB

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
        return PhonemeEqBand(low, high, gain)

    def to_storage_mapping(self) -> Dict[str, float]:
        return {
            "lowHz": float(self.low_hz),
            "highHz": float(self.high_hz),
            "gainDb": float(self.gain_db),
        }

    def to_engine_mapping(self) -> Dict[str, float]:
        return {
            "low_hz": float(self.low_hz),
            "high_hz": float(self.high_hz),
            "gain_db": float(self.gain_db),
        }

    @classmethod
    def default(cls) -> "PhonemeEqBand":
        return cls()

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, object]) -> Optional["PhonemeEqBand"]:
        if not isinstance(mapping, Mapping):
            return None
        low = mapping.get("lowHz", mapping.get("low_hz", _DEFAULT_LOW_HZ))
        high = mapping.get("highHz", mapping.get("high_hz", _DEFAULT_HIGH_HZ))
        gain = mapping.get("gainDb", mapping.get("gain_db", _DEFAULT_GAIN_DB))
        try:
            low_val = float(low)
            high_val = float(high)
            gain_val = float(gain)
        except (TypeError, ValueError):
            return None
        return cls(low_val, high_val, gain_val)


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

    def _rebuild_global_bands(self) -> None:
        bands: List[PhonemeEqBand] = []

        def add_band(low: float, high: float, gain: float) -> None:
            if not math.isfinite(gain) or abs(gain) < 0.05:
                return
            candidate = PhonemeEqBand(low, high, gain).clamp(
                self._low_min, self._high_max, self._gain_min, self._gain_max
            )
            bands.append(candidate)

        for name, value in self._global_parameters.items():
            scale = _scale(value)
            if not scale:
                continue
            spec = ADVANCED_VOICE_PARAMETER_SPECS.get(name)
            if not spec:
                continue
            profile = spec.get("profile", {})
            base_gain = float(profile.get("gain", 6.0)) * scale

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
                    add_band(low, high, base_gain * multiplier)
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
                add_band(low, high, base_gain)
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

