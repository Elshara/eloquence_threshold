#!/usr/bin/env python3
"""Inventory synthesizer assets and recommend staging locations.

This helper inspects both ``assets`` and ``speechdata`` so we can keep
editable source material under version control without bloating the add-on
package with large binary payloads.  Each file is categorised by
extension, synthesizer family (inferred from the path), and an estimated
"editability" flag that suggests whether the file belongs in ``assets``
(source-friendly) or ``speechdata`` (archival payloads such as DLLs or
large acoustic corpora).

The JSON manifest includes an entry for every file along with hashes and
size metadata so follow-up automation can detect drift.  A Markdown report
summarises the inventory for quick human review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"
SPEECHDATA_DIR = ROOT / "speechdata"
DEFAULT_TARGETS = (ASSETS_DIR, SPEECHDATA_DIR)
RELOCATION_DISPLAY_LIMIT = 200

# File extensions that typically indicate editable text content.
TEXT_EXTENSIONS = {
    ".md",
    ".rst",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".ini",
    ".cfg",
    ".py",
    ".csv",
    ".tsv",
    ".xml",
    ".html",
    ".css",
    ".js",
    ".phd",
    ".pho",
    ".ipa",
    ".lex",
}

# Binary-heavy extensions that we normally keep under speechdata.
BINARY_EXTENSIONS = {
    ".dll",
    ".exe",
    ".so",
    ".dylib",
    ".lib",
    ".a",
    ".bin",
    ".dat",
    ".mp3",
    ".wav",
    ".ogg",
    ".zip",
    ".7z",
    ".rar",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    ".lzma",
    ".cab",
    ".img",
    ".iso",
    ".apk",
    ".msi",
    ".ttf",
    ".fon",
    ".fonx",
    ".fonix",
    ".voc",
}

SYNTH_HINTS: List[Tuple[str, str]] = [
    ("eloquence", "eloquence"),
    ("espeak", "espeak-ng"),
    ("speechplayer", "nv speech player"),
    ("nvda", "nvda"),
    ("pico", "svox pico"),
    ("sam", "sam"),
    ("ibm", "ibm tts"),
    ("fonix", "fonix"),
    ("dectalk", "dectalk"),
    ("klatt", "klatt"),
]


@dataclass
class AssetRecord:
    path: str
    synthesizer: str
    category: str
    editable: bool
    recommended_location: str
    size_bytes: int
    sha256: str

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


def guess_synth_family(path: Path) -> str:
    lower = str(path).lower()
    for token, label in SYNTH_HINTS:
        if token in lower:
            return label
    return "unspecified"


def guess_category(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in TEXT_EXTENSIONS:
        return "text"
    if suffix in BINARY_EXTENSIONS:
        return "binary"
    mimetype, _ = mimetypes.guess_type(str(path))
    if mimetype:
        if mimetype.startswith("text/"):
            return "text"
        if mimetype.startswith("audio/"):
            return "audio"
    if suffix:
        return suffix.lstrip(".")
    return "unknown"


def is_editable(path: Path, category: str) -> bool:
    if category == "text":
        return True
    suffix = path.suffix.lower()
    if suffix in TEXT_EXTENSIONS:
        return True
    if path.stat().st_size < 64 * 1024 and category not in {"binary", "audio"}:
        return True
    return False


def recommend_location(path: Path, editable: bool) -> str:
    return "assets" if editable else "speechdata"


def sha256sum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_files(targets: Iterable[Path]) -> Iterable[Path]:
    for base in targets:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                yield path


def build_records(paths: Iterable[Path]) -> List[AssetRecord]:
    records: List[AssetRecord] = []
    for path in sorted(paths):
        category = guess_category(path)
        editable = is_editable(path, category)
        synthesizer = guess_synth_family(path.relative_to(ROOT))
        recommended = recommend_location(path, editable)
        size_bytes = path.stat().st_size
        digest = sha256sum(path)
        rel_path = str(path.relative_to(ROOT)).replace(os.sep, "/")
        records.append(
            AssetRecord(
                path=rel_path,
                synthesizer=synthesizer,
                category=category,
                editable=editable,
                recommended_location=recommended,
                size_bytes=size_bytes,
                sha256=digest,
            )
        )
    return records


def summarise(records: Iterable[AssetRecord]) -> Dict[str, Dict[str, int]]:
    summary: Dict[str, Dict[str, int]] = {}
    for record in records:
        synth_bucket = summary.setdefault(record.synthesizer, {"count": 0, "bytes": 0})
        synth_bucket["count"] += 1
        synth_bucket["bytes"] += record.size_bytes
    return summary


def location_bucket(record: AssetRecord) -> str:
    return record.path.split("/", 1)[0]


def relocation_candidates(records: Iterable[AssetRecord]) -> List[AssetRecord]:
    candidates: List[AssetRecord] = []
    for record in records:
        actual_root = location_bucket(record)
        if actual_root != record.recommended_location:
            candidates.append(record)
    return sorted(candidates, key=lambda record: (record.recommended_location, record.path))


def summarise_relocations(relocations: Iterable[AssetRecord]) -> Dict[str, Dict[str, int]]:
    summary: Dict[str, Dict[str, int]] = {}
    for record in relocations:
        bucket = summary.setdefault(record.recommended_location, {"count": 0, "bytes": 0})
        bucket["count"] += 1
        bucket["bytes"] += record.size_bytes
    return summary


def render_markdown(records: List[AssetRecord]) -> str:
    summary = summarise(records)
    relocations = relocation_candidates(records)
    relocation_limit = RELOCATION_DISPLAY_LIMIT
    displayed = relocations[:relocation_limit]
    lines = [
        "# Synthesizer asset audit",
        "",
        "This audit reflects the NVDA community fork of ETI Eloquence 6.1 and our push to keep",
        "classic Klatt-era synthesizers such as DECtalk and FonixTalk alive alongside eSpeak NG",
        "and NV Speech Player voices.  By aligning editable resources with ``assets`` and pushing",
        "bulk runtime binaries into ``speechdata`` we make it easier to ship `eloquence.nvda-addon`",
        "while following CodeQL-friendly packaging expectations.",
        "",
        "## Context and follow-up",
        "",
        "- Keep README and offline packaging guides in sync with NVDA upstream (https://github.com/nvaccess/nvda/).",
        "  Refresh cached downloads with ``python tools/audit_nvaccess_downloads.py --roots releases/stable releases/2024.3 snapshots/alpha --max-depth 2 --limit-per-dir 12 --insecure --json docs/download_nvaccess_snapshot.json --markdown docs/download_nvaccess_snapshot.md`` before running ``python build.py --insecure --no-download --output dist/eloquence.nvda-addon``.",
        "- When updating locale templates or phoneme data, pair this inventory with ``python tools/report_language_progress.py --json docs/language_progress.json --markdown docs/language_progress.md --print`` so contributors see",
        "  how far the 42 seeded locales (Arabic through Finnish) have progressed.",
        "- Use ``python tools/report_voice_parameters.py --json docs/voice_parameter_report.json --markdown docs/voice_parameter_report.md --print``",
        "  to keep slider metadata aligned with the phoneme customiser and NV Speech Player mappings.",
        "",
        "## Synthesizer breakdown",
        "",
        "| Synthesizer | Files | Size (MiB) |",
        "|-------------|-------|------------|",
    ]
    for synth, payload in sorted(summary.items()):
        size_mib = payload["bytes"] / (1024 * 1024)
        lines.append(f"| {synth} | {payload['count']} | {size_mib:.2f} |")
    lines.extend(
        [
            "",
            "## Relocation priorities",
            "",
            "The table below only lists files whose current root directory (``assets`` or ``speechdata``)",
            "does not match the recommended location.  Use these entries to plan incremental clean-ups",
            "without committing the entire 50k-line manifest.",
            "",
            "| Path | Synthesizer | Category | Editable | Suggested home |",
            "|------|-------------|----------|----------|----------------|",
        ]
    )
    for record in displayed:
        lines.append(
            "| `{path}` | {synth} | {category} | {editable} | {home} |".format(
                path=record.path,
                synth=record.synthesizer,
                category=record.category,
                editable="yes" if record.editable else "no",
                home=record.recommended_location,
            )
        )
    if not relocations:
        lines.append("| _No relocation candidates discovered._ | | | | |")
    elif len(relocations) > relocation_limit:
        lines.extend(
            [
                "",
                f"_Showing {relocation_limit} of {len(relocations)} candidates.  Run ``python tools/audit_assets.py --full-json assets/md/asset_audit_full.json`` to export the complete manifest._",
            ]
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-json",
        type=Path,
        default=ROOT / "assets" / "md" / "asset_audit_report.json",
        help="Path to write the JSON manifest.",
    )
    parser.add_argument(
        "--output-markdown",
        type=Path,
        default=ROOT / "assets" / "md" / "asset_audit_report.md",
        help="Path to write the Markdown report.",
    )
    parser.add_argument(
        "--roots",
        nargs="*",
        type=Path,
        default=list(DEFAULT_TARGETS),
        help="Directories to audit.  Defaults to assets and speechdata.",
    )
    parser.add_argument(
        "--full-json",
        type=Path,
        help="Optional path for a complete per-file manifest (omitted by default to keep commits small).",
    )
    args = parser.parse_args()

    records = build_records(iter_files(args.roots))

    relocations = relocation_candidates(records)
    summary = summarise(records)
    relocation_summary = summarise_relocations(relocations)
    relocation_limit = RELOCATION_DISPLAY_LIMIT
    audit_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_files": len(records),
        "total_bytes": sum(record.size_bytes for record in records),
        "summary": summary,
        "relocation_summary": relocation_summary,
        "relocation_count": len(relocations),
        "relocation_limit": relocation_limit,
        "relocations": [
            {**record.to_dict(), "actual_root": location_bucket(record)} for record in relocations[:relocation_limit]
        ],
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    with args.output_json.open("w", encoding="utf-8") as fh:
        json.dump(audit_payload, fh, indent=2)
        fh.write("\n")

    args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
    with args.output_markdown.open("w", encoding="utf-8") as fh:
        fh.write(render_markdown(records))

    if args.full_json:
        args.full_json.parent.mkdir(parents=True, exist_ok=True)
        with args.full_json.open("w", encoding="utf-8") as fh:
            json.dump([record.to_dict() for record in records], fh, indent=2)
            fh.write("\n")


if __name__ == "__main__":
    main()
