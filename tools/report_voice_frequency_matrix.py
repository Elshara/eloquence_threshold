"""Summarise advanced voice parameter frequency coverage."""
from __future__ import annotations

import argparse
import datetime as _dt
import json
from dataclasses import dataclass
from pathlib import Path
import statistics
import sys
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from voice_parameters import ADVANCED_VOICE_PARAMETER_SPECS


@dataclass
class FrequencyBand:
    """Representation of a single EQ band in Hz."""

    low_hz: float
    high_hz: float
    gain_multiplier: Optional[float] = None

    def to_mapping(self) -> Dict[str, float]:
        payload: Dict[str, float] = {
            "lowHz": round(self.low_hz, 6),
            "highHz": round(self.high_hz, 6),
            "widthHz": round(self.high_hz - self.low_hz, 6),
            "centreHz": round((self.low_hz + self.high_hz) / 2.0, 6),
        }
        if self.gain_multiplier is not None:
            payload["gainMultiplier"] = round(self.gain_multiplier, 6)
        return payload


def _timestamp() -> str:
    return (
        _dt.datetime.now(_dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _iter_bands(profile: Mapping[str, object]) -> Iterable[FrequencyBand]:
    range_value = profile.get("range")
    if isinstance(range_value, (tuple, list)) and len(range_value) == 2:
        low, high = float(range_value[0]), float(range_value[1])
        yield FrequencyBand(low, high, None)
    bands = profile.get("bands")
    if isinstance(bands, Sequence):
        for item in bands:
            if not isinstance(item, Mapping):
                continue
            band_range = item.get("range")
            if (
                isinstance(band_range, (tuple, list))
                and len(band_range) == 2
            ):
                low, high = float(band_range[0]), float(band_range[1])
                gain_multiplier = item.get("gainMultiplier")
                try:
                    gain_multiplier_value = None
                    if gain_multiplier is not None:
                        gain_multiplier_value = float(gain_multiplier)
                except (TypeError, ValueError):
                    gain_multiplier_value = None
                yield FrequencyBand(low, high, gain_multiplier_value)


def _summarise_parameter(param_id: str, spec: Mapping[str, object]) -> Dict[str, object]:
    label = str(spec.get("label", param_id))
    tags = sorted({str(tag) for tag in spec.get("tags", ()) if tag})
    description = str(spec.get("description", "")).strip()
    min_value = spec.get("min")
    max_value = spec.get("max")
    default_value = spec.get("default")
    profile = spec.get("profile")

    bands: List[FrequencyBand] = []
    gain_hint: Optional[float] = None
    kind: Optional[str] = None

    if isinstance(profile, Mapping):
        kind_value = profile.get("kind")
        if isinstance(kind_value, str):
            kind = kind_value
        gain_value = profile.get("gain")
        if isinstance(gain_value, (int, float)):
            gain_hint = float(gain_value)
        bands.extend(_iter_bands(profile))

    band_mappings = [band.to_mapping() for band in bands]
    lows = [band.low_hz for band in bands]
    highs = [band.high_hz for band in bands]
    centres = [band.to_mapping()["centreHz"] for band in bands]

    parameter_summary: Dict[str, object] = {
        "id": param_id,
        "label": label,
        "description": description,
        "min": min_value,
        "max": max_value,
        "default": default_value,
        "tags": tags,
        "profileKind": kind,
        "profileGain": gain_hint,
        "bandCount": len(bands),
        "bands": band_mappings,
    }

    if lows and highs:
        parameter_summary["minFrequencyHz"] = round(min(lows), 6)
        parameter_summary["maxFrequencyHz"] = round(max(highs), 6)
        parameter_summary["coverageWidthHz"] = round(max(highs) - min(lows), 6)
    if centres:
        parameter_summary["medianCentreHz"] = round(statistics.median(centres), 6)
        parameter_summary["meanCentreHz"] = round(statistics.fmean(centres), 6)

    return parameter_summary


def _build_summary() -> Dict[str, object]:
    parameters: List[Dict[str, object]] = []
    missing_profiles: List[str] = []
    for param_id in sorted(ADVANCED_VOICE_PARAMETER_SPECS):
        spec = ADVANCED_VOICE_PARAMETER_SPECS[param_id]
        summary = _summarise_parameter(param_id, spec)
        if summary["bandCount"] == 0:
            missing_profiles.append(param_id)
        parameters.append(summary)

    min_hz_values = [param["minFrequencyHz"] for param in parameters if "minFrequencyHz" in param]
    max_hz_values = [param["maxFrequencyHz"] for param in parameters if "maxFrequencyHz" in param]
    centre_values = [param["medianCentreHz"] for param in parameters if "medianCentreHz" in param]

    tag_summary: Dict[str, MutableMapping[str, object]] = {}
    for param in parameters:
        for tag in param.get("tags", []):
            entry = tag_summary.setdefault(
                tag,
                {
                    "tag": tag,
                    "parameterIds": [],
                    "minFrequencyHz": None,
                    "maxFrequencyHz": None,
                },
            )
            entry["parameterIds"].append(param["id"])
            if "minFrequencyHz" in param and isinstance(param["minFrequencyHz"], (int, float)):
                if entry["minFrequencyHz"] is None or param["minFrequencyHz"] < entry["minFrequencyHz"]:
                    entry["minFrequencyHz"] = param["minFrequencyHz"]
            if "maxFrequencyHz" in param and isinstance(param["maxFrequencyHz"], (int, float)):
                if entry["maxFrequencyHz"] is None or param["maxFrequencyHz"] > entry["maxFrequencyHz"]:
                    entry["maxFrequencyHz"] = param["maxFrequencyHz"]

    ordered_tag_summary = [
        {
            "tag": tag,
            "parameterIds": sorted(values["parameterIds"]),
            "minFrequencyHz": values["minFrequencyHz"],
            "maxFrequencyHz": values["maxFrequencyHz"],
            "coverageWidthHz": (
                round(values["maxFrequencyHz"] - values["minFrequencyHz"], 6)
                if values["minFrequencyHz"] is not None and values["maxFrequencyHz"] is not None
                else None
            ),
        }
        for tag, values in sorted(tag_summary.items())
    ]

    return {
        "generated": _timestamp(),
        "parameterCount": len(parameters),
        "parameters": parameters,
        "missingProfiles": sorted(missing_profiles),
        "globalFrequency": {
            "minHz": min(min_hz_values) if min_hz_values else None,
            "maxHz": max(max_hz_values) if max_hz_values else None,
            "medianCentreHz": statistics.median(centre_values) if centre_values else None,
            "meanCentreHz": statistics.fmean(centre_values) if centre_values else None,
        },
        "tagSummary": ordered_tag_summary,
    }


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def _format_frequency_range(item: Mapping[str, object]) -> str:
    min_hz = item.get("minFrequencyHz")
    max_hz = item.get("maxFrequencyHz")
    if min_hz is None or max_hz is None:
        return "–"
    return f"{float(min_hz):.2f}–{float(max_hz):.2f} Hz"


def _write_markdown(path: Path, payload: Mapping[str, object]) -> None:
    lines: List[str] = []
    lines.append("# Voice frequency matrix")
    lines.append("")
    lines.append(
        "This matrix outlines the frequency coverage of Eloquence's advanced voice "
        "parameters. Each slider shapes the phoneme EQ bands documented in "
        "`voice_parameters.py`, giving NVDA users and tooling a reproducible way to "
        "align NV Speech Player metadata with Eloquence's parametric filters."
    )
    lines.append("")
    generated = payload.get("generated")
    if generated:
        lines.append(f"*Generated:* `{generated}`")
        lines.append("")

    lines.append("## Parameter coverage")
    lines.append("")
    lines.append("| Parameter | Range (0–200) | Frequency focus | Bands | Tags | Gain hint |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for param in payload.get("parameters", []):
        label = param.get("label", param.get("id"))
        range_text = f"{param.get('min', '–')}–{param.get('max', '–')}"
        frequency_text = _format_frequency_range(param)
        band_count = param.get("bandCount", 0)
        tags = ", ".join(param.get("tags", [])) or "–"
        gain_hint = param.get("profileGain")
        gain_text = f"{gain_hint:.2f} dB" if isinstance(gain_hint, (int, float)) else "–"
        lines.append(
            f"| {label} | {range_text} | {frequency_text} | {band_count} | {tags} | {gain_text} |"
        )

    lines.append("")
    tag_summary = payload.get("tagSummary", [])
    if tag_summary:
        lines.append("## Tag frequency envelopes")
        lines.append("")
        lines.append("| Tag | Parameters | Frequency span |")
        lines.append("| --- | --- | --- |")
        for entry in tag_summary:
            tag = entry.get("tag", "–")
            parameters = ", ".join(entry.get("parameterIds", [])) or "–"
            frequency_text = _format_frequency_range(entry)
            lines.append(f"| {tag} | {parameters} | {frequency_text} |")
        lines.append("")

    missing = payload.get("missingProfiles", [])
    if missing:
        lines.append("## Parameters without frequency metadata")
        lines.append("")
        lines.append(
            "The following sliders do not yet expose band hints in `voice_parameters.py`. "
            "Update their `profile` entries with frequency ranges so documentation and "
            "analysis tooling can highlight their impact across NVDA's Speech dialog."
        )
        lines.append("")
        for param_id in missing:
            lines.append(f"- `{param_id}`")
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Path to write the JSON payload.")
    parser.add_argument(
        "--markdown",
        type=Path,
        help="Path to write the Markdown summary.",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print a condensed summary to stdout.",
    )
    args = parser.parse_args(argv)

    payload = _build_summary()

    if args.json:
        _write_json(args.json, payload)
    if args.markdown:
        _write_markdown(args.markdown, payload)

    if args.print:
        global_freq = payload.get("globalFrequency", {})
        min_hz = global_freq.get("minHz")
        max_hz = global_freq.get("maxHz")
        mean_centre = global_freq.get("meanCentreHz")
        span_text = (
            f"{min_hz:.2f}–{max_hz:.2f} Hz"
            if isinstance(min_hz, (int, float)) and isinstance(max_hz, (int, float))
            else "–"
        )
        mean_text = (
            f"{mean_centre:.2f} Hz" if isinstance(mean_centre, (int, float)) else "–"
        )
        print(
            "Voice frequency coverage:\n"
            f"  Parameters analysed: {payload.get('parameterCount', 0)}\n"
            f"  Frequency span: {span_text}\n"
            f"  Mean centre: {mean_text}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
