"""Generate NVDA compatibility reports from cached download snapshots.

This helper consumes the JSON output produced by
``tools/audit_nvaccess_downloads.py`` and enriches each entry with the
severity grading logic used during the original crawl.  The goal is to
provide a sortable view of recent NVDA releases, alphas, and other
channel drops so Eloquence maintainers can confirm which builds still
fall inside the add-on's validated support window.

Typical usage::

    python tools/report_nvda_compatibility.py \
        --snapshot docs/download_nvaccess_snapshot.json \
        --validated docs/validated_nvda_builds.json \
        --markdown docs/nvda_compatibility_matrix.md \
        --json docs/nvda_compatibility_matrix.json

The script prints a concise roll-up to stdout, writes optional Markdown
and JSON artefacts, and sorts entries by their ``modified`` timestamp in
descending order so the newest builds appear first.  It exists alongside
``tools/compare_nvaccess_snapshots.py`` to make incremental monitoring of
download.nvaccess.org easier for anyone packaging or testing this
Eloquence fork.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import asdict
from datetime import datetime
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from audit_nvaccess_downloads import (  # type: ignore[import-not-found]
    ListingEntry,
    ManifestInfo,
    Severity,
    classify_entry,
    load_manifest_info,
    load_validated_snapshots,
    parse_release_version,
)


def _load_snapshot_entries(path: str) -> List[ListingEntry]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    entries: List[ListingEntry] = []
    for raw in payload.get("entries", []):
        modified_raw = raw.get("modified")
        modified = None
        if modified_raw:
            try:
                modified = datetime.fromisoformat(str(modified_raw))
            except ValueError:
                modified = None

        entry = ListingEntry(
            path=str(raw.get("path", "")),
            url=str(raw.get("url", "")),
            name=str(raw.get("name", "")),
            entry_type=str(raw.get("entryType", "file")),
            size_bytes=raw.get("sizeBytes"),
            size_display=str(raw.get("sizeDisplay", "")),
            modified=modified,
            target=raw.get("target"),
            depth=int(raw.get("depth", 0)),
        )
        entries.append(entry)

    return entries


def _channel_for_entry(entry: ListingEntry) -> str:
    if entry.path.startswith("snapshots/"):
        parts = entry.path.split("/", 2)
        if len(parts) > 1 and parts[1]:
            return f"snapshot:{parts[1]}"
        return "snapshot"
    if entry.path.startswith("releases/"):
        return "release"
    return "other"


def _serialize_entry(entry: ListingEntry) -> Dict[str, object]:
    result = asdict(entry)
    if entry.modified:
        result["modified"] = entry.modified.isoformat()
    return result


def _serialize_severity(severity: Optional[Severity]) -> Optional[Dict[str, str]]:
    if severity is None:
        return None
    return severity.to_json()


def _build_rows(
    entries: Iterable[ListingEntry],
    manifest: ManifestInfo,
    validated: Dict[str, str],
    current_nvda: Optional[str],
) -> List[Tuple[ListingEntry, Optional[str], Optional[Severity]]]:
    rows: List[Tuple[ListingEntry, Optional[str], Optional[Severity]]] = []
    for entry in entries:
        version = parse_release_version(entry)
        severity = classify_entry(entry, manifest, validated, current_nvda)
        rows.append((entry, version, severity))
    rows.sort(key=lambda item: (item[0].modified or datetime.min), reverse=True)
    return rows


def render_markdown(
    rows: Sequence[Tuple[ListingEntry, Optional[str], Optional[Severity]]]
) -> str:
    lines = [
        "# NVDA compatibility matrix",
        "",
        "| Modified | Channel | Path | Version | Severity | Notes | Size |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry, version, severity in rows:
        channel = _channel_for_entry(entry)
        severity_level = severity.level if severity else ""
        notes = severity.reason if severity else ""
        lines.append(
            "| {modified} | {channel} | `{path}` | {version} | {severity} | {notes} | {size} |".format(
                modified=entry.modified.isoformat(sep=" ") if entry.modified else "",
                channel=channel,
                path=entry.path or "/",
                version=version or "",
                severity=severity_level,
                notes=notes.replace("|", "\\|") if notes else "",
                size=entry.size_display or ("-" if entry.entry_type == "dir" else ""),
            )
        )
    return "\n".join(lines) + "\n"


def summarize(rows: Sequence[Tuple[ListingEntry, Optional[str], Optional[Severity]]]) -> str:
    channel_counts: Dict[str, Counter[str]] = defaultdict(Counter)
    total = 0
    for entry, _version, severity in rows:
        channel = _channel_for_entry(entry)
        if severity:
            channel_counts[channel][severity.level] += 1
            total += 1

    lines = ["Compatibility summary (newest first)"]
    for channel in sorted(channel_counts.keys()):
        counts = channel_counts[channel]
        fragments = [f"{level}:{counts[level]}" for level in sorted(counts.keys())]
        lines.append(f"- {channel}: {', '.join(fragments)}")
    lines.append(f"- total graded entries: {total}")
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--snapshot",
        default="docs/download_nvaccess_snapshot.json",
        help="Path to cached snapshot JSON generated by audit_nvaccess_downloads",
    )
    parser.add_argument(
        "--validated",
        default="docs/validated_nvda_builds.json",
        help="JSON file describing last validated builds per channel",
    )
    parser.add_argument(
        "--manifest",
        default="manifest.ini",
        help="Path to the add-on manifest used for minimum/last-tested metadata",
    )
    parser.add_argument(
        "--current-nvda",
        help="Optional NVDA version string to compare against releases",
    )
    parser.add_argument(
        "--markdown",
        help="Write a Markdown table to this path",
    )
    parser.add_argument(
        "--json",
        help="Write a machine-readable summary JSON to this path",
    )

    args = parser.parse_args(argv)

    entries = _load_snapshot_entries(args.snapshot)
    validated = load_validated_snapshots(args.validated)
    manifest = load_manifest_info(args.manifest)
    rows = _build_rows(entries, manifest, validated, args.current_nvda)

    print(summarize(rows))

    if args.markdown:
        markdown_payload = render_markdown(rows)
        with open(args.markdown, "w", encoding="utf-8") as handle:
            handle.write(markdown_payload)

    if args.json:
        serialized = []
        for entry, version, severity in rows:
            serialized.append(
                {
                    "entry": _serialize_entry(entry),
                    "version": version,
                    "channel": _channel_for_entry(entry),
                    "severity": _serialize_severity(severity),
                }
            )
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump(serialized, handle, indent=2, ensure_ascii=False)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
