"""Export curated voice scenes into Markdown and JSON catalogues."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from voice_parameters import ADVANCED_VOICE_PARAMETER_SPECS
from voice_scenes import iter_scene_snapshots


def _format_delta(value: int, default: int) -> str:
    delta = value - default
    if delta == 0:
        return "±0"
    prefix = "+" if delta > 0 else ""
    return f"{prefix}{delta}"


def _markdown_for_scene(snapshot: dict) -> str:
    metadata = snapshot["metadata"]
    configuration = snapshot["configuration"]
    params = configuration["advancedVoiceParameters"]
    lines: List[str] = []
    lines.append(f"## {snapshot['name']}")
    lines.append("")
    lines.append(snapshot["description"])
    lines.append("")
    tags = ", ".join(metadata.get("tags", [])) or "(none)"
    languages = ", ".join(metadata.get("languageFocus", [])) or "(unspecified)"
    archives = metadata.get("archiveSources", [])
    lines.append(f"- **Tags:** {tags}")
    lines.append(f"- **Language focus:** {languages}")
    if metadata.get("sampleRateHz"):
        sample_rate = int(metadata["sampleRateHz"])
        lines.append(f"- **Sample rate target:** {sample_rate:,} Hz")
    lines.append(
        f"- **Headroom:** {int(metadata.get('headroomHz', configuration.get('headroomHz', 0))):,} Hz (post WASAPI clamp)"
    )
    if archives:
        lines.append("- **DataJake archive references:**")
        for archive in archives:
            lines.append(f"  - {archive}")
    lines.append("")
    lines.append("### Global NV Speech Player sliders")
    lines.append("")
    lines.append("| Parameter | Value | Default | Delta |")
    lines.append("| --- | ---: | ---: | ---: |")
    for name, value in sorted(params.items()):
        spec = ADVANCED_VOICE_PARAMETER_SPECS.get(name, {})
        default = int(spec.get("default", 100))
        lines.append(f"| {name} | {value} | {default} | {_format_delta(value, default)} |")
    lines.append("")
    lines.append("### Per-phoneme EQ guidance")
    lines.append("")
    lines.append("| Phoneme | Band | Range (Hz) | Gain (dB) | Filter | Q |")
    lines.append("| --- | ---: | --- | ---: | --- | ---: |")
    per_phoneme = configuration.get("perPhonemeEq", {})
    for phoneme, bands in sorted(per_phoneme.items()):
        for index, band in enumerate(bands, start=1):
            low = int(band["lowHz"])
            high = int(band["highHz"])
            gain = band["gainDb"]
            filt = band.get("filterType", "peaking")
            q_value = band.get("q", 1.0)
            lines.append(
                f"| {phoneme} | {index} | {low:,}–{high:,} | {gain:.2f} | {filt} | {q_value:.2f} |"
            )
    lines.append("")
    lines.append(
        "These settings layer on top of Eloquence's existing NVDA configuration. They reference DataJake's mirrors so "
        "contributors can port phoneme rules, IPA tables, and tooling back into the synthesiser without hunting across "
        "1,500+ archives."
    )
    lines.append("")
    return "\n".join(lines)


def build_markdown(snapshots: Iterable[dict]) -> str:
    lines: List[str] = []
    lines.append("# Voice scene catalog")
    lines.append("")
    lines.append(
        "This catalog integrates DataJake's archive inventory with Eloquence's phoneme customiser so NVDA contributors can "
        "stage reusable presets. Each scene references eSpeak NG, DECtalk/Fonix, NV Speech Player, or similar tooling from the "
        "cache and maps them to the extended sliders documented in `AGENTS.md`."
    )
    lines.append("")
    lines.append(
        "Run `python tools/export_voice_scenes.py --json docs/voice_scene_catalog.json --markdown docs/voice_scene_catalog.md` "
        "to refresh this file after adjusting the curated scenes."
    )
    lines.append("")
    for snapshot in snapshots:
        lines.append(_markdown_for_scene(snapshot))
    return "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export Eloquence voice scenes")
    parser.add_argument("--json", type=Path, default=Path("docs/voice_scene_catalog.json"))
    parser.add_argument("--markdown", type=Path, default=Path("docs/voice_scene_catalog.md"))
    parser.add_argument("--print", action="store_true", help="Dump Markdown to stdout")
    args = parser.parse_args(list(argv) if argv is not None else None)

    snapshots = iter_scene_snapshots()

    markdown = build_markdown(snapshots)
    json_payload = snapshots

    args.markdown.write_text(markdown, encoding="utf-8")
    args.json.write_text(json.dumps(json_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.print:
        print(markdown)

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    raise SystemExit(main())
