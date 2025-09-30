"""Import Equalizer APO configuration files into Eloquence-friendly JSON."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from phoneme_customizer import PhonemeEqBand


@dataclass
class EqApoFilter:
    """Representation of a single Equalizer APO filter line."""

    state: str
    filter_type: str
    params: MutableMapping[str, float] = field(default_factory=dict)

    def to_mapping(self) -> Dict[str, object]:
        mapping: Dict[str, object] = {
            "state": self.state,
            "type": self.filter_type,
        }
        mapping.update(self.params)
        return mapping

    def to_phoneme_band(self, sample_rate: Optional[float] = None) -> Optional[PhonemeEqBand]:
        if self.state.upper() != "ON":
            return None
        if self.filter_type.upper() not in {"PK", "PEAK", "PEAKING"}:
            return None
        center = self.params.get("Fc")
        gain = self.params.get("Gain")
        q = self.params.get("Q")
        if center is None or gain is None or q is None:
            return None
        try:
            center_hz = float(center)
            gain_db = float(gain)
            q_value = float(q)
        except (TypeError, ValueError):
            return None
        return PhonemeEqBand.from_peak_filter(center_hz, gain_db, q_value, sample_rate=sample_rate)


@dataclass
class EqApoBlock:
    """Container for a device/stage combination in an Equalizer APO config."""

    device: str
    stage: List[str]
    channel: str = "ALL"
    copy: str = ""
    delay_ms: float = 0.0
    loudness_correction: Mapping[str, float] = field(default_factory=dict)
    preamp_db: float = 0.0
    filters: List[EqApoFilter] = field(default_factory=list)

    def to_mapping(self) -> Dict[str, object]:
        return {
            "device": self.device,
            "stage": list(self.stage),
            "channel": self.channel,
            "copy": self.copy,
            "delay_ms": self.delay_ms,
            "loudnessCorrection": dict(self.loudness_correction),
            "preamp_db": self.preamp_db,
            "filters": [flt.to_mapping() for flt in self.filters],
        }

    def active_phoneme_bands(self, sample_rate: Optional[float] = None) -> List[PhonemeEqBand]:
        bands: List[PhonemeEqBand] = []
        for flt in self.filters:
            band = flt.to_phoneme_band(sample_rate=sample_rate)
            if band is not None:
                bands.append(band)
        return bands


def _strip_comment(line: str) -> str:
    if "//" in line:
        return line.split("//", 1)[0].strip()
    if "#" in line:
        return line.split("#", 1)[0].strip()
    return line.strip()


def _parse_float(value: str) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _parse_loudness(tokens: Iterable[str]) -> Mapping[str, float]:
    values: Dict[str, float] = {}
    iterator = iter(tokens)
    for token in iterator:
        key = token
        try:
            raw_value = next(iterator)
        except StopIteration:
            break
        numeric = _parse_float(raw_value)
        if numeric is not None:
            values[key] = numeric
    return values


def parse_eq_apo_config(text: str) -> List[EqApoBlock]:
    """Parse an Equalizer APO configuration file into structured blocks."""

    blocks: List[EqApoBlock] = []
    current: Optional[EqApoBlock] = None

    for raw_line in text.splitlines():
        line = _strip_comment(raw_line)
        if not line:
            continue
        if line.lower().startswith("device:"):
            device_name = line.split(":", 1)[1].strip()
            current = EqApoBlock(device=device_name, stage=[])
            blocks.append(current)
            continue
        if current is None:
            continue
        if line.lower().startswith("stage:"):
            stages = [part.strip() for part in line.split(":", 1)[1].split() if part.strip()]
            current.stage = stages or ["pre-mix"]
            continue
        if line.lower().startswith("channel:"):
            current.channel = line.split(":", 1)[1].strip() or "ALL"
            continue
        if line.lower().startswith("copy:"):
            current.copy = line.split(":", 1)[1].strip()
            continue
        if line.lower().startswith("delay:"):
            value = line.split(":", 1)[1].strip().split()[0]
            numeric = _parse_float(value)
            if numeric is not None:
                current.delay_ms = numeric
            continue
        if line.lower().startswith("loudnesscorrection:"):
            remainder = line.split(":", 1)[1].strip()
            tokens = [token for token in remainder.replace("=", " ").split() if token]
            current.loudness_correction = _parse_loudness(tokens)
            continue
        if line.lower().startswith("preamp:"):
            tokens = line.split()
            if len(tokens) >= 2:
                numeric = _parse_float(tokens[1])
                if numeric is not None:
                    current.preamp_db = numeric
            continue
        if line.lower().startswith("filter:"):
            tokens = line.split()
            if len(tokens) < 4:
                continue
            state = tokens[1]
            filter_type = tokens[2]
            params: Dict[str, float] = {}
            idx = 3
            while idx < len(tokens):
                key_token = tokens[idx]
                upper = key_token.upper()
                idx += 1
                canonical = {
                    "FC": "Fc",
                    "FREQ": "Fc",
                    "FREQUENCY": "Fc",
                    "GAIN": "Gain",
                    "Q": "Q",
                    "BW": "Bandwidth",
                    "BANDWIDTH": "Bandwidth",
                    "WIDTH": "Bandwidth",
                    "SLOPE": "Slope",
                }.get(upper)
                if canonical is None:
                    continue
                if idx >= len(tokens):
                    break
                value_token = tokens[idx]
                idx += 1
                while idx < len(tokens) and value_token.upper() in {"HZ", "DB", "MS"}:
                    value_token = tokens[idx]
                    idx += 1
                numeric = _parse_float(value_token)
                if numeric is not None:
                    params[canonical] = numeric
            current.filters.append(EqApoFilter(state=state, filter_type=filter_type, params=params))
            continue
    return blocks


def _blocks_to_json(blocks: Iterable[EqApoBlock]) -> str:
    payload = [block.to_mapping() for block in blocks]
    return json.dumps(payload, indent=2, sort_keys=True)


def _blocks_to_markdown(blocks: Iterable[EqApoBlock], sample_rate: Optional[float]) -> str:
    lines = ["# Equalizer APO import summary", ""]
    for block in blocks:
        lines.append(f"## {block.device}")
        stage_display = ", ".join(block.stage) if block.stage else "pre-mix"
        lines.append(f"- **Stage:** {stage_display}")
        lines.append(f"- **Channel:** {block.channel}")
        if block.copy:
            lines.append(f"- **Copy:** {block.copy}")
        lines.append(f"- **Delay:** {block.delay_ms:.2f} ms")
        if block.loudness_correction:
            summary = ", ".join(f"{k}={v}" for k, v in block.loudness_correction.items())
            lines.append(f"- **Loudness correction:** {summary}")
        lines.append(f"- **Preamp:** {block.preamp_db:.2f} dB")
        bands = block.active_phoneme_bands(sample_rate=sample_rate)
        lines.append(f"- **Active peak filters:** {len(bands)}")
        for index, band in enumerate(bands, start=1):
            lines.append(
                f"  - Band {index}: {band.low_hz:.2f}–{band.high_hz:.2f} Hz @ {band.gain_db:.2f} dB"
            )
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=pathlib.Path, help="Path to an Equalizer APO configuration file")
    parser.add_argument("--output-json", type=pathlib.Path, required=True, help="Destination JSON file")
    parser.add_argument("--output-markdown", type=pathlib.Path, required=True, help="Destination Markdown file")
    parser.add_argument(
        "--sample-rate",
        type=float,
        default=None,
        help="Optional sample rate hint (Hz) used when deriving phoneme EQ bands",
    )
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    blocks = parse_eq_apo_config(text)

    args.output_json.write_text(_blocks_to_json(blocks), encoding="utf-8")
    markdown = _blocks_to_markdown(blocks, sample_rate=args.sample_rate)
    args.output_markdown.write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
