"""Summarise cached NV Access download snapshots into directory trees.

This helper consumes the JSON output emitted by ``tools/audit_nvaccess_downloads``
and optionally the recommendation file from ``tools/check_nvda_updates``.  It
aggregates entries by directory, highlights the newest files in each folder,
and surfaces the highest severity action that our add-on should consider when
NVDA publishes a fresh build.

The goal is to document the download.nvaccess.org hierarchy without hitting the
network repeatedly.  Generated JSON/Markdown artefacts can be checked into the
repository so future contributors immediately see which folders gained new
installers, documentation bundles, or symbols.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Dict, Iterable, List, Mapping, Optional


SEVERITY_ORDER = {
    "info": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


# High-level descriptions for well-known paths within download.nvaccess.org.
# We default to the closest ancestor description when no direct entry exists.
PATH_DESCRIPTIONS = {
    "": "Root index for download.nvaccess.org.",
    "releases": "Official NVDA releases grouped by channel, including documentation.",
    "releases/stable": "Latest stable NVDA installers, portable builds, and manuals.",
    "releases/beta": "Pre-release betas staged ahead of the next stable version.",
    "releases/candidate": "Release candidates undergoing final validation.",
    "releases/dev": "Historic development snapshots from the legacy development branch.",
    "snapshots": "Nightly and per-commit snapshots primarily for testers.",
    "snapshots/alpha": "The rolling alpha channel that tracks NVDA master commits.",
    "snapshots/beta": "Older beta snapshots preserved for reproducibility.",
    "documentation": "Translated NVDA user guides and change logs.",
    "symbols": "PDB symbol stores for debugging NVDA binaries.",
    "tools": "Assorted utilities shipped alongside NVDA installers.",
}


@dataclass
class SnapshotEntry:
    """Representation of a single snapshot entry."""

    path: str
    name: str
    entry_type: str
    size_bytes: Optional[int]
    size_display: str
    modified: Optional[datetime]
    target: Optional[str]
    depth: int

    recommended_action: Optional[str] = None
    severity_level: Optional[str] = None
    severity_reason: Optional[str] = None

    def to_json(self) -> Dict[str, object]:
        return {
            "path": self.path,
            "name": self.name,
            "entryType": self.entry_type,
            "sizeBytes": self.size_bytes,
            "sizeDisplay": self.size_display,
            "modified": self.modified.isoformat() if self.modified else None,
            "target": self.target,
            "recommendedAction": self.recommended_action,
            "severity": {
                "level": self.severity_level,
                "reason": self.severity_reason,
            }
            if self.severity_level
            else None,
        }


@dataclass
class DirectorySummary:
    """Aggregated statistics for a directory within the snapshot."""

    path: str
    depth: int
    files: List[SnapshotEntry] = dataclasses.field(default_factory=list)
    directories: List[SnapshotEntry] = dataclasses.field(default_factory=list)
    total_size_bytes: int = 0
    latest_modified: Optional[datetime] = None
    latest_entry: Optional[SnapshotEntry] = None
    recommended_actions: Counter = dataclasses.field(default_factory=Counter)
    highest_severity: Optional[SnapshotEntry] = None

    def description(self) -> str:
        if self.path in PATH_DESCRIPTIONS:
            return PATH_DESCRIPTIONS[self.path]
        parts = self.path.split("/") if self.path else []
        for index in range(len(parts), 0, -1):
            prefix = "/".join(parts[:index])
            if prefix in PATH_DESCRIPTIONS:
                return PATH_DESCRIPTIONS[prefix]
        return ""

    def register(self, entry: SnapshotEntry) -> None:
        if entry.entry_type == "dir":
            self.directories.append(entry)
        else:
            self.files.append(entry)
            if entry.size_bytes:
                self.total_size_bytes += entry.size_bytes
        if entry.modified and (self.latest_modified is None or entry.modified > self.latest_modified):
            self.latest_modified = entry.modified
            self.latest_entry = entry
        if entry.recommended_action:
            self.recommended_actions[entry.recommended_action] += 1
        if entry.severity_level:
            if (
                self.highest_severity is None
                or SEVERITY_ORDER.get(entry.severity_level, -1)
                > SEVERITY_ORDER.get(self.highest_severity.severity_level or "", -1)
                or (
                    entry.modified
                    and self.highest_severity.modified
                    and entry.modified > self.highest_severity.modified
                    and SEVERITY_ORDER.get(entry.severity_level, -1)
                    == SEVERITY_ORDER.get(self.highest_severity.severity_level or "", -1)
                )
            ):
                self.highest_severity = entry

    def to_json(self, *, max_items: int) -> Dict[str, object]:
        def pack(entries: Iterable[SnapshotEntry]) -> List[Dict[str, object]]:
            sorted_entries = sorted(
                entries,
                key=lambda e: (
                    SEVERITY_ORDER.get(e.severity_level or "", -1),
                    e.modified or datetime.min,
                ),
                reverse=True,
            )
            limited = list(sorted_entries[:max_items])
            return [entry.to_json() for entry in limited]

        highest = self.highest_severity
        return {
            "path": self.path or "/",
            "depth": self.depth,
            "description": self.description(),
            "fileCount": len(self.files),
            "directoryCount": len(self.directories),
            "totalSizeBytes": self.total_size_bytes,
            "latestModified": self.latest_modified.isoformat() if self.latest_modified else None,
            "latestEntry": highest.to_json() if highest else (self.latest_entry.to_json() if self.latest_entry else None),
            "recommendedActions": dict(self.recommended_actions),
            "highestSeverity": highest.to_json() if highest else None,
            "topFiles": pack(self.files),
            "topDirectories": pack(self.directories),
        }

    def to_markdown(self, *, max_items: int) -> str:
        header = f"### {self.path or '/'} (depth {self.depth})\n"
        description = self.description()
        lines = [header]
        if description:
            lines.append(f"_{description}_\n")
        lines.append(
            f"- Files: **{len(self.files)}**, directories: **{len(self.directories)}**, "
            f"total size (direct files): **{self.total_size_bytes:,} B**"
        )
        if self.latest_modified:
            lines.append(f"- Latest modified: `{self.latest_modified.isoformat()}`")
        if self.recommended_actions:
            action_bits = ", ".join(
                f"{action} × {count}" for action, count in sorted(self.recommended_actions.items())
            )
            lines.append(f"- Recommended actions: {action_bits}")
        if self.highest_severity and self.highest_severity.severity_level:
            lines.append(
                f"- Highest severity: **{self.highest_severity.severity_level}** — "
                f"{self.highest_severity.severity_reason or ''}"
            )
        elif self.latest_entry and self.latest_entry.modified:
            lines.append(f"- Latest entry: `{self.latest_entry.name}`")

        def render_table(entries: Iterable[SnapshotEntry], title: str) -> None:
            sorted_entries = sorted(
                entries,
                key=lambda e: (
                    SEVERITY_ORDER.get(e.severity_level or "", -1),
                    e.modified or datetime.min,
                ),
                reverse=True,
            )
            subset = list(sorted_entries[:max_items])
            if not subset:
                return
            lines.append("")
            lines.append(f"| {title} | Modified | Size | Action | Severity |")
            lines.append("| --- | --- | --- | --- | --- |")
            for entry in subset:
                modified = entry.modified.isoformat() if entry.modified else "";
                size = entry.size_display or ("%d B" % entry.size_bytes if entry.size_bytes else "")
                action = entry.recommended_action or ""
                severity = entry.severity_level or ""
                if entry.severity_reason:
                    severity = f"{severity} — {entry.severity_reason}"
                lines.append(
                    f"| `{entry.name}` | {modified} | {size} | {action} | {severity} |"
                )

        render_table(self.files, "Top files")
        render_table(self.directories, "Top directories")
        lines.append("")
        return "\n".join(lines)


def _load_snapshot(path: str) -> List[SnapshotEntry]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    entries = []
    for item in payload.get("entries", []):
        modified_raw = item.get("modified")
        modified = datetime.fromisoformat(modified_raw) if modified_raw else None
        entry = SnapshotEntry(
            path=item.get("path", ""),
            name=item.get("name", ""),
            entry_type=item.get("entryType", ""),
            size_bytes=item.get("sizeBytes"),
            size_display=item.get("sizeDisplay", ""),
            modified=modified,
            target=item.get("target"),
            depth=int(item.get("depth", 0)),
        )
        entries.append(entry)
    return entries


def _load_recommendations(path: Optional[str]) -> Mapping[str, Dict[str, object]]:
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return {item["path"]: item for item in payload.get("entries", [])}


def _normalise_directory_path(path: str) -> str:
    path = path.strip()
    if not path:
        return ""
    # Remove trailing slash so directories and files align on the same parent.
    if path.endswith("/"):
        path = path[:-1]
    return path


def _parent_path(path: str) -> str:
    if not path:
        return ""
    if "/" not in path:
        return ""
    return path.rsplit("/", 1)[0]


def build_directory_summaries(
    entries: Iterable[SnapshotEntry],
    recommendations: Mapping[str, Dict[str, object]],
) -> Dict[str, DirectorySummary]:
    summaries: Dict[str, DirectorySummary] = {}

    def ensure_summary(path: str) -> DirectorySummary:
        if path not in summaries:
            depth = 0 if not path else len(path.split("/"))
            summaries[path] = DirectorySummary(path=path, depth=depth)
        return summaries[path]

    for entry in entries:
        path = _normalise_directory_path(entry.path)
        if entry.entry_type == "dir" and not path.endswith("/"):
            # Keep directory paths with trailing slash in downstream lookups.
            pass
        recommendation = recommendations.get(entry.path.rstrip("/")) or recommendations.get(entry.path)
        if recommendation:
            entry.recommended_action = recommendation.get("recommendedAction")
            severity = recommendation.get("severity") or {}
            entry.severity_level = severity.get("level")
            entry.severity_reason = severity.get("reason")

        parent = _parent_path(path)
        summary = ensure_summary(parent)
        summary.register(entry)

        # Ensure the directory itself exists in the map so that empty folders
        # still appear in the output (even if they have no listed children).
        if entry.entry_type == "dir":
            ensure_summary(path)

    # Always ensure the root summary exists.
    ensure_summary("")
    return summaries


def render_markdown(summaries: Mapping[str, DirectorySummary], *, max_items: int) -> str:
    ordered_paths = sorted(
    summaries.keys(),
        key=lambda p: (
            summaries[p].latest_modified or datetime.min,
            -summaries[p].depth,
            p,
        ),
        reverse=True,
    )
    lines = ["# NV Access download tree summary", ""]
    for path in ordered_paths:
        lines.append(summaries[path].to_markdown(max_items=max_items))
    return "\n".join(lines)


def render_json(summaries: Mapping[str, DirectorySummary], *, max_items: int) -> Dict[str, object]:
    ordered = sorted(
        summaries.keys(),
        key=lambda p: (
            summaries[p].latest_modified or datetime.min,
            -summaries[p].depth,
            p,
        ),
        reverse=True,
    )
    return {
        "generated": datetime.now(UTC).isoformat(),
        "directories": [summaries[path].to_json(max_items=max_items) for path in ordered],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--snapshot",
        required=True,
        help="Path to docs/download_nvaccess_snapshot.json produced by the audit helper.",
    )
    parser.add_argument(
        "--recommendations",
        help="Optional path to docs/nvda_update_recommendations.json for severity metadata.",
    )
    parser.add_argument("--json", help="Write the aggregated tree to this JSON file.")
    parser.add_argument("--markdown", help="Write a Markdown summary to this file.")
    parser.add_argument(
        "--max-items",
        type=int,
        default=5,
        help="Maximum number of entries to list per directory section.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    entries = _load_snapshot(args.snapshot)
    recommendations = _load_recommendations(args.recommendations)
    summaries = build_directory_summaries(entries, recommendations)

    json_payload = render_json(summaries, max_items=args.max_items)
    markdown = render_markdown(summaries, max_items=args.max_items)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump(json_payload, handle, indent=2)
    if args.markdown:
        with open(args.markdown, "w", encoding="utf-8") as handle:
            handle.write(markdown + "\n")

    top_dirs = sorted(
        summaries.values(),
        key=lambda summary: summary.latest_modified or datetime.min,
        reverse=True,
    )[:5]
    for summary in top_dirs:
        latest = summary.latest_entry
        detail = f" latest entry {latest.name}" if latest else ""
        print(
            f"{summary.path or '/'}: files={len(summary.files)} dirs={len(summary.directories)}"
            f" latest={summary.latest_modified.isoformat() if summary.latest_modified else 'n/a'}{detail}"
        )


if __name__ == "__main__":
    main()

