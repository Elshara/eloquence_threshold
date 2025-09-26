"""Inventory archive and directory contents for speech asset provenance.

This helper inspects local directories or files (including supported archives)
and emits structured JSON/Markdown summaries that document payload counts,
sizes, timestamps, and relevant extraction notes.  The output is designed to
support the repository's archival tracking plans so contributors can compare
updates from sources such as DataJake, Blind Help Project mirrors, or upstream
Eloquence distributions.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import stat
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterable, List, Optional, Sequence


ARCHIVE_EXTENSIONS = {
    ".zip": "zip",
    ".tar": "tar",
    ".tar.gz": "tar",
    ".tgz": "tar",
    ".tar.bz2": "tar",
    ".tbz2": "tar",
    ".tar.xz": "tar",
    ".txz": "tar",
    ".7z": "7z",
}


def _is_archive(path: Path) -> Optional[str]:
    lower = path.name.lower()
    for ext, kind in ARCHIVE_EXTENSIONS.items():
        if lower.endswith(ext):
            return kind
    return None


def _iter_suffixes(path: Path) -> Iterable[str]:
    name = path.name
    while True:
        base, dot, suffix = name.partition(".")
        if not dot:
            break
        yield "." + suffix
        name = suffix


def _format_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    units = ["KB", "MB", "GB", "TB"]
    value = float(size)
    for unit in units:
        value /= 1024.0
        if value < 1024.0:
            return f"{value:.1f} {unit}"
    return f"{value:.1f} PB"


def _utc_iso(timestamp: float) -> str:
    return _dt.datetime.fromtimestamp(timestamp, tz=_dt.timezone.utc).isoformat()


def _describe_permissions(mode: int) -> str:
    return stat.filemode(mode)


@dataclass
class ArchiveEntry:
    """Metadata about a discovered file or directory."""

    path: str
    type: str
    size: int
    modified: str
    depth: int
    mode: str
    notes: List[str] = field(default_factory=list)
    archive_type: Optional[str] = None
    archive_preview: Optional[List[str]] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        # Skip empty notes for cleaner JSON.
        if not data["notes"]:
            data.pop("notes")
        if not data.get("archive_preview"):
            data.pop("archive_preview", None)
        if not data.get("archive_type"):
            data.pop("archive_type", None)
        return data


def _scan_directory(root: Path, max_depth: int, include_hidden: bool) -> List[ArchiveEntry]:
    entries: List[ArchiveEntry] = []
    root = root.resolve()
    root_depth = len(root.parts)

    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        depth = len(path.parts) - root_depth
        if max_depth >= 0 and depth > max_depth:
            continue
        if not include_hidden and any(part.startswith(".") for part in rel.parts):
            continue
        try:
            stat_result = path.stat()
        except OSError as exc:  # pragma: no cover - filesystem race.
            entry = ArchiveEntry(
                path=str(rel),
                type="unknown",
                size=0,
                modified=_utc_iso(_dt.datetime.now().timestamp()),
                depth=depth,
                mode="?",
                notes=[f"stat failed: {exc}"],
            )
            entries.append(entry)
            continue

        if path.is_dir():
            entry_type = "directory"
        elif path.is_file():
            entry_type = "file"
        else:
            entry_type = "special"

        notes: List[str] = []
        archive_preview: Optional[List[str]] = None
        archive_type = None
        if entry_type == "file":
            archive_type = _is_archive(path)
            if archive_type == "zip":
                import zipfile

                try:
                    with zipfile.ZipFile(path) as zf:
                        archive_preview = sorted(zf.namelist()[:25])
                        if len(zf.namelist()) > 25:
                            notes.append(f"zip preview truncated to 25 entries (of {len(zf.namelist())})")
                except Exception as exc:  # pragma: no cover - unexpected archive failure.
                    notes.append(f"zip read failed: {exc}")
            elif archive_type == "tar":
                import tarfile

                try:
                    with tarfile.open(path) as tf:
                        members = tf.getmembers()
                        preview_names = [m.name for m in members[:25]]
                        archive_preview = sorted(preview_names)
                        if len(members) > 25:
                            notes.append(f"tar preview truncated to 25 entries (of {len(members)})")
                except Exception as exc:
                    notes.append(f"tar read failed: {exc}")
            elif archive_type == "7z":
                notes.append("7z archive detected; install `py7zr` or 7-Zip CLI for deep inspection")

        entry = ArchiveEntry(
            path=str(rel) if rel.parts else ".",
            type=entry_type,
            size=stat_result.st_size,
            modified=_utc_iso(stat_result.st_mtime),
            depth=depth,
            mode=_describe_permissions(stat_result.st_mode),
            notes=notes,
            archive_type=archive_type,
            archive_preview=archive_preview,
        )
        entries.append(entry)

    return entries


def _scan_path(path: Path, max_depth: int, include_hidden: bool) -> List[ArchiveEntry]:
    if path.is_dir():
        entries = [
            ArchiveEntry(
                path=".",
                type="directory",
                size=path.stat().st_size,
                modified=_utc_iso(path.stat().st_mtime),
                depth=0,
                mode=_describe_permissions(path.stat().st_mode),
            )
        ]
        entries.extend(_scan_directory(path, max_depth=max_depth, include_hidden=include_hidden))
        return entries

    if path.is_file():
        stat_result = path.stat()
        archive_type = _is_archive(path)
        notes: List[str] = []
        archive_preview: Optional[List[str]] = None
        if archive_type == "zip":
            import zipfile

            try:
                with zipfile.ZipFile(path) as zf:
                    archive_preview = sorted(zf.namelist()[:25])
                    if len(zf.namelist()) > 25:
                        notes.append(f"zip preview truncated to 25 entries (of {len(zf.namelist())})")
            except Exception as exc:
                notes.append(f"zip read failed: {exc}")
        elif archive_type == "tar":
            import tarfile

            try:
                with tarfile.open(path) as tf:
                    members = tf.getmembers()
                    archive_preview = sorted([m.name for m in members[:25]])
                    if len(members) > 25:
                        notes.append(f"tar preview truncated to 25 entries (of {len(members)})")
            except Exception as exc:
                notes.append(f"tar read failed: {exc}")
        elif archive_type == "7z":
            notes.append("7z archive detected; install `py7zr` or 7-Zip CLI for deep inspection")

        return [
            ArchiveEntry(
                path=path.name,
                type="file",
                size=stat_result.st_size,
                modified=_utc_iso(stat_result.st_mtime),
                depth=0,
                mode=_describe_permissions(stat_result.st_mode),
                archive_type=archive_type,
                notes=notes,
                archive_preview=archive_preview,
            )
        ]

    stat_result = path.stat()
    return [
        ArchiveEntry(
            path=path.name,
            type="special",
            size=stat_result.st_size,
            modified=_utc_iso(stat_result.st_mtime),
            depth=0,
            mode=_describe_permissions(stat_result.st_mode),
            notes=["Non-file, non-directory entry"],
        )
    ]


def _summarize(entries: Sequence[ArchiveEntry]) -> dict:
    total_size = sum(entry.size for entry in entries)
    file_count = sum(1 for entry in entries if entry.type == "file")
    dir_count = sum(1 for entry in entries if entry.type == "directory")
    archive_count = sum(1 for entry in entries if entry.archive_type)
    notes = sorted({note for entry in entries for note in entry.notes})
    return {
        "totalEntries": len(entries),
        "totalSize": total_size,
        "fileCount": file_count,
        "directoryCount": dir_count,
        "archiveCount": archive_count,
        "notes": notes,
    }


def _render_markdown(root: Path, entries: Sequence[ArchiveEntry], summary: dict) -> str:
    lines = [f"# Archive inventory: `{root}`", ""]
    lines.append(f"Scanned at: {_utc_iso(_dt.datetime.now().timestamp())}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("| --- | --- |")
    lines.append(f"| Total entries | {summary['totalEntries']} |")
    lines.append(f"| Total size | {_format_size(summary['totalSize'])} |")
    lines.append(f"| Files | {summary['fileCount']} |")
    lines.append(f"| Directories | {summary['directoryCount']} |")
    lines.append(f"| Archives | {summary['archiveCount']} |")
    if summary["notes"]:
        lines.append(f"| Notes | {'; '.join(summary['notes'])} |")
    lines.append("")
    lines.append("## Entries")
    lines.append("")
    lines.append("| Depth | Type | Path | Size | Modified (UTC) | Extras |")
    lines.append("| --- | --- | --- | --- | --- | --- |")

    for entry in entries:
        extras: List[str] = []
        if entry.archive_type:
            extras.append(f"archive={entry.archive_type}")
        if entry.notes:
            extras.extend(entry.notes)
        if entry.archive_preview:
            preview = ", ".join(entry.archive_preview[:5])
            extras.append(f"preview: {preview}{'…' if len(entry.archive_preview) > 5 else ''}")
        lines.append(
            "| {depth} | {type} | `{path}` | {size} | {modified} | {extras} |".format(
                depth=entry.depth,
                type=entry.type,
                path=entry.path,
                size=_format_size(entry.size),
                modified=entry.modified,
                extras="; ".join(extras) if extras else "",
            )
        )

    return "\n".join(lines) + "\n"


def inventory_paths(paths: Sequence[Path], max_depth: int, include_hidden: bool) -> dict:
    payload = {
        "scannedAt": _utc_iso(_dt.datetime.now().timestamp()),
        "roots": [],
    }
    for path in paths:
        entries = _scan_path(path, max_depth=max_depth, include_hidden=include_hidden)
        summary = _summarize(entries)
        payload["roots"].append(
            {
                "root": str(path),
                "summary": summary,
                "entries": [entry.to_dict() for entry in entries],
            }
        )
    return payload


def write_outputs(data: dict, json_path: Optional[Path], markdown_path: Optional[Path]) -> None:
    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if markdown_path:
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        sections: List[str] = []
        for root in data["roots"]:
            md = _render_markdown(Path(root["root"]), [ArchiveEntry(**entry) for entry in root["entries"]], root["summary"])
            sections.append(md)
        markdown_path.write_text("\n\n".join(sections), encoding="utf-8")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory archives and directories for NVDA speech asset tracking.")
    parser.add_argument("roots", nargs="+", help="Directories or files to inspect")
    parser.add_argument("--json", dest="json_path", type=Path, help="Optional path for JSON output")
    parser.add_argument("--markdown", dest="markdown_path", type=Path, help="Optional path for Markdown output")
    parser.add_argument(
        "--max-depth",
        dest="max_depth",
        type=int,
        default=5,
        help="Maximum recursion depth for directory scans (default: 5; use -1 for unlimited)",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include entries whose names begin with a dot",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    safe_root = Path.cwd().resolve()

    def is_within_safe_root(path: Path, base: Path) -> bool:
        try:
            path.relative_to(base)
            return True
        except ValueError:
            return False

    paths = []
    for root in args.roots:
        candidate = (safe_root / root).expanduser().resolve()
        if is_within_safe_root(candidate, safe_root):
            paths.append(candidate)
        else:
            print(
                f"error: {root!r} resolves to {candidate}, which is outside the allowed scan root ({safe_root})",
                file=sys.stderr,
            )
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        for item in missing:
            print(f"warning: {item} does not exist", file=sys.stderr)
        paths = [path for path in paths if path.exists()]
        if not paths:
            print("error: no valid roots to scan", file=sys.stderr)
            return 1

    data = inventory_paths(paths, max_depth=args.max_depth, include_hidden=args.include_hidden)
    write_outputs(data, args.json_path, args.markdown_path)

    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
