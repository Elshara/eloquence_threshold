"""Orchestrate NVDA download audits and recommendation reports."""
from __future__ import annotations

import argparse
import dataclasses
import json
import os
from datetime import UTC, datetime
from typing import Dict, Iterable, List, Optional, Sequence

from audit_nvaccess_downloads import (  # type: ignore[import-not-found]
    DEFAULT_BASE_URL,
    ListingEntry,
    Severity,
    build_listing_entries,
    classify_entry,
    load_manifest_info,
    load_validated_snapshots,
    render_markdown as render_snapshot_markdown,
)
from check_nvda_updates import (  # type: ignore[import-not-found]
    _evaluate_entries,
    _load_snapshot_entries,
    _serialize_entry,
    render_markdown as render_recommendation_markdown,
    summarize as summarize_recommendations,
)
from compare_nvaccess_snapshots import (  # type: ignore[import-not-found]
    calculate_diffs,
    diff_to_json,
    load_snapshot as load_snapshot_map,
    render_markdown as render_diff_markdown,
)


def _write_json(path: Optional[str], payload: Dict[str, object]) -> None:
    if not path:
        return
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def _write_text(path: Optional[str], content: str) -> None:
    if not path:
        return
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def _load_entries_from_snapshot(path: str) -> List[ListingEntry]:
    # Reuse the loader from check_nvda_updates so depth/size handling stays in sync.
    return _load_snapshot_entries(path)


def _entries_to_map(entries: Iterable[ListingEntry]) -> Dict[str, ListingEntry]:
    return {entry.path: entry for entry in entries}


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Base URL for NV Access downloads",
    )
    parser.add_argument(
        "--roots",
        nargs="*",
        default=["releases/stable", "releases/2024.3", "snapshots/alpha"],
        help="Root directories (relative to base URL) to audit",
    )
    parser.add_argument("--max-depth", type=int, default=2, help="Traversal depth for audits")
    parser.add_argument(
        "--limit-per-dir",
        type=int,
        default=12,
        help="Limit the number of entries fetched per directory",
    )
    parser.add_argument(
        "--manifest",
        default="manifest.ini",
        help="Path to the add-on manifest",
    )
    parser.add_argument(
        "--validated",
        default="docs/validated_nvda_builds.json",
        help="JSON file recording validated NVDA builds",
    )
    parser.add_argument(
        "--current-nvda",
        help="Optional NVDA version string representing the running environment",
    )
    parser.add_argument(
        "--snapshot-json",
        default="docs/download_nvaccess_snapshot.json",
        help="Output path for the consolidated snapshot JSON",
    )
    parser.add_argument(
        "--snapshot-markdown",
        default="docs/download_nvaccess_snapshot.md",
        help="Output path for the consolidated snapshot Markdown",
    )
    parser.add_argument(
        "--recommendations-json",
        default="docs/nvda_update_recommendations.json",
        help="Output path for the update recommendation JSON",
    )
    parser.add_argument(
        "--recommendations-markdown",
        default="docs/nvda_update_recommendations.md",
        help="Output path for the update recommendation Markdown",
    )
    parser.add_argument(
        "--previous-snapshot",
        help="Optional older snapshot JSON for delta comparisons",
    )
    parser.add_argument(
        "--delta-json",
        default="docs/download_nvaccess_delta.json",
        help="Output path for the snapshot delta JSON",
    )
    parser.add_argument(
        "--delta-markdown",
        default="docs/download_nvaccess_delta.md",
        help="Output path for the snapshot delta Markdown",
    )
    parser.add_argument(
        "--snapshot-source",
        help="Reuse an existing snapshot JSON instead of crawling the NV Access site",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS verification when crawling download.nvaccess.org",
    )

    args = parser.parse_args(argv)

    manifest = load_manifest_info(args.manifest)
    validated_snapshots = load_validated_snapshots(args.validated)

    entries: List[ListingEntry]
    base_url = args.base_url
    if args.snapshot_source:
        if not os.path.exists(args.snapshot_source):
            raise FileNotFoundError(f"Snapshot source {args.snapshot_source!r} does not exist")
        with open(args.snapshot_source, "r", encoding="utf-8") as handle:
            cached_payload = json.load(handle)
            base_url = cached_payload.get("baseUrl", base_url)
        entries = _load_entries_from_snapshot(args.snapshot_source)
    else:
        entries = build_listing_entries(
            base_url=args.base_url,
            roots=args.roots,
            max_depth=args.max_depth,
            limit_per_dir=args.limit_per_dir,
            insecure=args.insecure,
        )

    severities: Dict[str, Severity] = {}
    for entry in entries:
        severity = classify_entry(entry, manifest, validated_snapshots, args.current_nvda)
        if severity:
            severities[entry.path] = severity

    entries.sort(key=lambda item: (item.modified or datetime.min), reverse=True)

    print("NVDA download snapshot summary (newest first):")
    for entry in entries[:20]:
        severity = severities.get(entry.path)
        severity_label = severity.level if severity else "-"
        modified = entry.modified.isoformat(sep=" ") if entry.modified else "-"
        print(
            f"[{severity_label:>6}] {modified} | {entry.path} | {entry.entry_type} | {entry.size_display or '-'}"
        )
        if severity:
            print(f"         -> {severity.reason}")
    if len(entries) > 20:
        print(f"... {len(entries) - 20} additional entries omitted from console output")

    generated = datetime.now(UTC).isoformat()
    snapshot_payload = {
        "baseUrl": base_url,
        "generated": generated,
        "entries": [entry.to_json() for entry in entries],
        "severities": {path: severity.to_json() for path, severity in severities.items()},
        "manifest": dataclasses.asdict(manifest),
        "validatedSnapshots": validated_snapshots,
        "roots": args.roots,
        "maxDepth": args.max_depth,
        "limitPerDir": args.limit_per_dir,
    }
    _write_json(args.snapshot_json, snapshot_payload)
    _write_text(args.snapshot_markdown, render_snapshot_markdown(entries, severities))

    recommendation_rows = _evaluate_entries(entries, manifest, validated_snapshots, args.current_nvda)
    print()
    print(summarize_recommendations(recommendation_rows))

    recommendation_payload = {
        "generated": generated.replace("+00:00", "Z"),
        "entries": [
            _serialize_entry(entry, version, severity, action)
            for entry, version, severity, action in recommendation_rows
        ],
    }
    _write_json(args.recommendations_json, recommendation_payload)
    _write_text(args.recommendations_markdown, render_recommendation_markdown(recommendation_rows))

    if args.previous_snapshot:
        if not os.path.exists(args.previous_snapshot):
            raise FileNotFoundError(
                f"Previous snapshot {args.previous_snapshot!r} does not exist"
            )
        old_entries = load_snapshot_map(args.previous_snapshot)
        new_entries = _entries_to_map(entries)
        diffs = calculate_diffs(
            old_entries,
            new_entries,
            manifest,
            validated_snapshots,
            args.current_nvda,
        )
        if diffs:
            print()
            print("Snapshot differences detected:")
            for diff in diffs[:20]:
                severity_label = diff.severity.level if diff.severity else "-"
                detail = "; ".join(diff.details)
                print(f"[{severity_label:>6}] {diff.change:>8} | {diff.path} | {detail}")
                if diff.severity:
                    print(f"         -> {diff.severity.reason}")
            if len(diffs) > 20:
                print(f"... {len(diffs) - 20} additional differences omitted")
        else:
            print()
            print("No differences detected between the provided snapshots.")

        _write_json(args.delta_json, diff_to_json(diffs))
        _write_text(args.delta_markdown, render_diff_markdown(diffs))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
