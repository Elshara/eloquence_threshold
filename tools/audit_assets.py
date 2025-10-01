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
DUPLICATE_DISPLAY_LIMIT = 50

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
    actual_root: str
    usefulness: str
    priority: str
    action: str
    notes: str

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


def choose_usefulness(
    synthesizer: str, editable: bool, category: str, actual_root: str
) -> str:
    if editable and synthesizer != "unspecified":
        return "core-editable"
    if editable:
        return "reference"
    if category == "audio":
        return "audio-archive"
    if actual_root == "speechdata":
        return "runtime-binary"
    return "archive"


def determine_action(actual_root: str, recommended: str, editable: bool) -> str:
    if actual_root == recommended:
        if recommended == "assets":
            return "retain-in-assets"
        return "retain-in-speechdata"
    if recommended == "assets":
        return "relocate-to-assets"
    if editable:
        return "split-reference"
    return "relocate-to-speechdata"


def priority_rank(priority: str) -> int:
    order = {"high": 0, "medium": 1, "low": 2, "info": 3}
    return order.get(priority, 99)


def determine_priority(action: str, size_bytes: int, editable: bool) -> str:
    if action in {"relocate-to-assets", "relocate-to-speechdata"}:
        return "high"
    if action == "split-reference":
        return "medium"
    if editable or size_bytes < 32 * 1024:
        return "medium"
    if size_bytes > 50 * 1024 * 1024:
        return "high"
    return "low"


def build_notes(
    record_path: str,
    actual_root: str,
    recommended: str,
    action: str,
    editable: bool,
    category: str,
    size_bytes: int,
    synthesizer: str,
) -> str:
    notes: List[str] = []
    if action.startswith("relocate"):
        notes.append(
            f"Currently in {actual_root}; recommend staging under {recommended} to match audit policy."
        )
    if action == "split-reference":
        notes.append(
            "Mixed payload: keep binaries in speechdata and extract editable portions into assets."
        )
    if editable and actual_root == "speechdata":
        notes.append(
            "Editable resource is hidden in speechdata; move so version control can track diffs."
        )
    if not editable and actual_root == "assets":
        notes.append("Binary payload inflates assets; archive it in speechdata instead.")
    if category == "audio":
        notes.append("Audio sample useful for phoneme or timbre reference.")
    if size_bytes > 50 * 1024 * 1024:
        notes.append(
            f"Large file (~{size_bytes / (1024 * 1024):.1f} MiB); plan dedicated extraction or compression."
        )
    if synthesizer == "unspecified":
        notes.append(
            "Synthesizer family undetected—tag the path or relocate next to known assets for clarity."
        )
    return " " + " ".join(notes) if notes else ""


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
        rel_path_obj = path.relative_to(ROOT)
        rel_path = str(rel_path_obj).replace(os.sep, "/")
        parts = rel_path_obj.parts
        actual_root = parts[0] if parts else ""
        usefulness = choose_usefulness(synthesizer, editable, category, actual_root)
        action = determine_action(actual_root, recommended, editable)
        priority = determine_priority(action, size_bytes, editable)
        notes = build_notes(
            rel_path,
            actual_root,
            recommended,
            action,
            editable,
            category,
            size_bytes,
            synthesizer,
        )
        records.append(
            AssetRecord(
                path=rel_path,
                synthesizer=synthesizer,
                category=category,
                editable=editable,
                recommended_location=recommended,
                size_bytes=size_bytes,
                sha256=digest,
                actual_root=actual_root,
                usefulness=usefulness,
                priority=priority,
                action=action,
                notes=notes,
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


def prioritised_candidates(records: Iterable[AssetRecord]) -> List[AssetRecord]:
    return sorted(
        records,
        key=lambda record: (
            priority_rank(record.priority),
            0 if record.action.startswith("relocate") else 1,
            -1 if record.editable else 0,
            -record.size_bytes,
            record.path,
        ),
    )


def summarise_relocations(relocations: Iterable[AssetRecord]) -> Dict[str, Dict[str, int]]:
    summary: Dict[str, Dict[str, int]] = {}
    for record in relocations:
        bucket = summary.setdefault(record.recommended_location, {"count": 0, "bytes": 0})
        bucket["count"] += 1
        bucket["bytes"] += record.size_bytes
    return summary


def summarise_by(records: Iterable[AssetRecord], attribute: str) -> Dict[str, Dict[str, int]]:
    summary: Dict[str, Dict[str, int]] = {}
    for record in records:
        key = getattr(record, attribute)
        bucket = summary.setdefault(key, {"count": 0, "bytes": 0})
        bucket["count"] += 1
        bucket["bytes"] += record.size_bytes
    return summary


def summarise_extensions(records: Iterable[AssetRecord]) -> Dict[str, Dict[str, int]]:
    summary: Dict[str, Dict[str, int]] = {}
    for record in records:
        suffix = Path(record.path).suffix.lower() or "<no extension>"
        bucket = summary.setdefault(suffix, {"count": 0, "bytes": 0})
        bucket["count"] += 1
        bucket["bytes"] += record.size_bytes
    return summary


def find_duplicate_groups(records: Iterable[AssetRecord]) -> List[Dict[str, object]]:
    buckets: Dict[str, List[AssetRecord]] = {}
    for record in records:
        buckets.setdefault(record.sha256, []).append(record)

    groups: List[Dict[str, object]] = []
    for digest, items in buckets.items():
        if len(items) < 2:
            continue
        total_bytes = sum(item.size_bytes for item in items)
        synths = sorted({item.synthesizer for item in items})
        groups.append(
            {
                "sha256": digest,
                "count": len(items),
                "total_bytes": total_bytes,
                "synthesizers": synths,
                "paths": [item.path for item in items],
            }
        )

    groups.sort(key=lambda group: (-group["count"], -group["total_bytes"], group["sha256"]))
    return groups


def consolidation_targets(records: Iterable[AssetRecord]) -> Dict[str, Dict[str, Dict[str, int]]]:
    summary: Dict[str, Dict[str, Dict[str, int]]] = {}
    for record in records:
        if record.action != "relocate-to-assets":
            continue
        synth_bucket = summary.setdefault(record.synthesizer, {})
        category_bucket = synth_bucket.setdefault(
            record.category,
            {"count": 0, "bytes": 0},
        )
        category_bucket["count"] += 1
        category_bucket["bytes"] += record.size_bytes
    return summary


def render_markdown(
    records: List[AssetRecord],
    duplicates: List[Dict[str, object]],
    consolidation: Dict[str, Dict[str, Dict[str, int]]],
    extension_summary: Dict[str, Dict[str, int]],
    duplicate_limit: int,
) -> str:
    summary = summarise(records)
    priority_summary = summarise_by(records, "priority")
    usefulness_summary = summarise_by(records, "usefulness")
    action_summary = summarise_by(records, "action")
    relocations = relocation_candidates(records)
    relocation_limit = RELOCATION_DISPLAY_LIMIT
    displayed = relocations[:relocation_limit]
    plan_candidates = prioritised_candidates(records)
    plan_display = plan_candidates[:relocation_limit]
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
            "## Priority mix",
            "",
            "| Priority | Files | Size (MiB) |",
            "|----------|-------|------------|",
        ]
    )
    for priority in sorted(priority_summary.keys(), key=priority_rank):
        payload = priority_summary[priority]
        size_mib = payload["bytes"] / (1024 * 1024)
        lines.append(f"| {priority} | {payload['count']} | {size_mib:.2f} |")
    lines.extend(
        [
            "",
            "## Usefulness overview",
            "",
            "| Usefulness | Files | Size (MiB) |",
            "|------------|-------|------------|",
        ]
    )
    for usefulness, payload in sorted(usefulness_summary.items()):
        size_mib = payload["bytes"] / (1024 * 1024)
        lines.append(f"| {usefulness} | {payload['count']} | {size_mib:.2f} |")
    lines.extend(
        [
            "",
            "## Action outcomes",
            "",
            "| Action | Files | Size (MiB) |",
            "|--------|-------|------------|",
        ]
    )
    for action, payload in sorted(action_summary.items()):
        size_mib = payload["bytes"] / (1024 * 1024)
        lines.append(f"| {action} | {payload['count']} | {size_mib:.2f} |")
    lines.extend(
        [
            "",
            "## Extension footprint",
            "",
            "The following breakdown highlights which file extensions dominate the inventory so we can",
            "target consolidation work for editable materials before merging synthesizer code paths.",
            "",
            "| Extension | Files | Size (MiB) |",
            "|-----------|-------|------------|",
        ]
    )
    for extension, payload in sorted(
        extension_summary.items(), key=lambda item: (-item[1]["count"], item[0])
    ):
        size_mib = payload["bytes"] / (1024 * 1024)
        lines.append(f"| {extension} | {payload['count']} | {size_mib:.2f} |")
    lines.extend(
        [
            "",
            "## Consolidation targets",
            "",
            "Editable resources currently parked under ``speechdata`` need to move into ``assets`` before",
            "we can merge Eloquence, eSpeak NG, and NV Speech Player logic into unified modules.  Focus on",
            "the synthesizer/category pairs below to unblock that consolidation work.",
            "",
            "| Synthesizer | Category | Files | Size (MiB) |",
            "|-------------|----------|-------|------------|",
        ]
    )
    if consolidation:
        for synth in sorted(consolidation):
            for category, payload in sorted(consolidation[synth].items(), key=lambda item: (-item[1]["count"], item[0])):
                size_mib = payload["bytes"] / (1024 * 1024)
                lines.append(f"| {synth} | {category} | {payload['count']} | {size_mib:.2f} |")
    else:
        lines.append("| _No outstanding relocations into assets._ | | | |")
    lines.extend(
        [
            "",
            "## Duplicate payloads",
            "",
            "Use the digest-matched entries below to deduplicate archives before packaging the NVDA add-on.",
            "This keeps the repo lean while still capturing references for contextual voice design.",
            "",
            "| SHA-256 | Files | Size (MiB) | Synthesizers | Example path |",
            "|---------|-------|------------|--------------|--------------|",
        ]
    )
    shown_duplicates = duplicates[:duplicate_limit]
    if shown_duplicates:
        for group in shown_duplicates:
            size_mib = group["total_bytes"] / (1024 * 1024)
            synths = ", ".join(group["synthesizers"])
            example = group["paths"][0]
            lines.append(
                "| `{digest}` | {count} | {size:.2f} | {synths} | `{example}` |".format(
                    digest=group["sha256"],
                    count=group["count"],
                    size=size_mib,
                    synths=synths or "unspecified",
                    example=example,
                )
            )
        if len(duplicates) > duplicate_limit:
            lines.extend(
                [
                    "",
                    f"_Showing {duplicate_limit} of {len(duplicates)} duplicate groups.  Export the full JSON manifest for the complete list._",
                ]
            )
    else:
        lines.append("| _No duplicate payloads detected._ | | | | |")
    lines.extend(
        [
            "",
            "## Prioritised action list",
            "",
            "Use this table to drive incremental clean-ups.  It combines relocation guidance",
            "with usefulness scoring so we can focus on high-impact edits first.",
            "",
            "| Path | Priority | Action | Synth | Editable | Notes |",
            "|------|----------|--------|-------|----------|-------|",
        ]
    )
    for record in plan_display:
        lines.append(
            "| `{path}` | {priority} | {action} | {synth} | {editable} | {notes} |".format(
                path=record.path,
                priority=record.priority,
                action=record.action,
                synth=record.synthesizer,
                editable="yes" if record.editable else "no",
                notes=record.notes.strip() if record.notes else "",
            )
        )
    if len(plan_candidates) > relocation_limit:
        lines.extend(
            [
                "",
                f"_Showing {relocation_limit} of {len(plan_candidates)} prioritised actions.  Use ``python tools/audit_assets.py --full-json assets/md/asset_audit_full.json`` for the entire list._",
            ]
        )
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
    priority_summary = summarise_by(records, "priority")
    action_summary = summarise_by(records, "action")
    usefulness_summary = summarise_by(records, "usefulness")
    extension_summary = summarise_extensions(records)
    duplicate_groups = find_duplicate_groups(records)
    consolidation_summary = consolidation_targets(records)
    plan_candidates = prioritised_candidates(records)
    relocation_limit = RELOCATION_DISPLAY_LIMIT
    audit_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_files": len(records),
        "total_bytes": sum(record.size_bytes for record in records),
        "summary": summary,
        "relocation_summary": relocation_summary,
        "priority_summary": priority_summary,
        "action_summary": action_summary,
        "usefulness_summary": usefulness_summary,
        "extension_summary": extension_summary,
        "consolidation_summary": consolidation_summary,
        "duplicate_group_count": len(duplicate_groups),
        "duplicate_group_limit": DUPLICATE_DISPLAY_LIMIT,
        "duplicate_groups": duplicate_groups[:DUPLICATE_DISPLAY_LIMIT],
        "relocation_count": len(relocations),
        "relocation_limit": relocation_limit,
        "relocations": [
            {**record.to_dict(), "actual_root": location_bucket(record)} for record in relocations[:relocation_limit]
        ],
        "action_plan_count": len(plan_candidates),
        "action_plan_limit": relocation_limit,
        "action_plan": [record.to_dict() for record in plan_candidates[:relocation_limit]],
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    with args.output_json.open("w", encoding="utf-8") as fh:
        json.dump(audit_payload, fh, indent=2)
        fh.write("\n")

    args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
    with args.output_markdown.open("w", encoding="utf-8") as fh:
        fh.write(
            render_markdown(
                records,
                duplicate_groups,
                consolidation_summary,
                extension_summary,
                DUPLICATE_DISPLAY_LIMIT,
            )
        )

    if args.full_json:
        args.full_json.parent.mkdir(parents=True, exist_ok=True)
        with args.full_json.open("w", encoding="utf-8") as fh:
            json.dump([record.to_dict() for record in records], fh, indent=2)
            fh.write("\n")


if __name__ == "__main__":
    main()
