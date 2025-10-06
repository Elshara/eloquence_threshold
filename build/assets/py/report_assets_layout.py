"""Generate a summary of the extension-scoped asset layout.

The repository restructures documentation, binaries, and tooling so they live
under ``assets/<extension>/<descriptive_name>.<extension>``.  This helper
produces JSON and Markdown snapshots that confirm each bucket stays aligned
with the convention while surfacing any files whose suffix does not match the
parent directory.  Keeping the summary refreshed helps CodeQL reviewers and
NVDA packaging drills reason about the migration without trawling the entire
working tree."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Sequence

MAX_MARKDOWN_MISMATCHES = 12


@dataclass
class AssetBucket:
    extension: str
    path: str
    file_count: int
    directory_count: int
    mismatched_files: Sequence[str]

    @property
    def mismatch_count(self) -> int:
        return len(self.mismatched_files)


@dataclass
class AssetLayoutReport:
    assets_root: str
    total_buckets: int
    total_files: int
    total_directories: int
    buckets: Sequence[AssetBucket]
    top_level_files: Sequence[str]


def _iter_buckets(assets_root: Path) -> Iterable[AssetBucket]:
    for entry in sorted(assets_root.iterdir(), key=lambda item: item.name.lower()):
        if not entry.is_dir():
            continue
        extension = entry.name
        files = 0
        directories = 0
        mismatched: List[str] = []
        for path in sorted(entry.rglob("*")):
            if path.is_dir():
                directories += 1
                continue
            files += 1
            suffix = path.suffix.lower().lstrip(".")
            expected = extension.lower()
            if expected and suffix != expected:
                mismatched.append(str(path.relative_to(entry)))
            if not expected and suffix:
                mismatched.append(str(path.relative_to(entry)))
        yield AssetBucket(
            extension=extension,
            path=str(entry.relative_to(assets_root)),
            file_count=files,
            directory_count=directories,
            mismatched_files=mismatched,
        )


def _collect_report(assets_root: Path) -> AssetLayoutReport:
    buckets = list(_iter_buckets(assets_root))
    total_files = sum(bucket.file_count for bucket in buckets)
    total_directories = sum(bucket.directory_count for bucket in buckets)
    top_level_files = [
        str(path.name)
        for path in sorted(assets_root.iterdir(), key=lambda item: item.name.lower())
        if path.is_file()
    ]
    return AssetLayoutReport(
        assets_root=str(assets_root),
        total_buckets=len(buckets),
        total_files=total_files,
        total_directories=total_directories,
        buckets=buckets,
        top_level_files=top_level_files,
    )


def _write_json(report: AssetLayoutReport, destination: Path) -> None:
    serialisable = {
        "assets_root": report.assets_root,
        "total_buckets": report.total_buckets,
        "total_files": report.total_files,
        "total_directories": report.total_directories,
        "top_level_files": list(report.top_level_files),
        "buckets": [
            {
                **asdict(bucket),
                "mismatch_count": bucket.mismatch_count,
                "mismatched_files": list(bucket.mismatched_files),
            }
            for bucket in report.buckets
        ],
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(serialisable, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_markdown(report: AssetLayoutReport, destination: Path) -> None:
    lines: List[str] = []
    lines.append("# Assets layout summary")
    lines.append("")
    lines.append(
        "This report inventories the extension-scoped directories under ``assets/`` "
        "so NVDA packaging rehearsals and CodeQL reviews can confirm the "
        "reshuffle remains consistent. Refresh it after moving files so reviewers "
        "know which buckets still contain mismatched extensions."
    )
    lines.append("")
    lines.append(f"* Assets root: `{report.assets_root}`")
    lines.append(f"* Extension buckets: {report.total_buckets}")
    lines.append(f"* Total files scanned: {report.total_files}")
    lines.append(f"* Nested directories scanned: {report.total_directories}")
    if report.top_level_files:
        lines.append(
            "* Top-level files staged directly under ``assets/``: "
            + ", ".join(f"`{name}`" for name in report.top_level_files)
        )
    lines.append("")
    lines.append("| Extension | Files | Subdirectories | Mismatches | Notes |")
    lines.append("| --- | ---: | ---: | ---: | --- |")
    for bucket in report.buckets:
        if bucket.mismatch_count:
            displayed = ", ".join(f"`{path}`" for path in bucket.mismatched_files[:MAX_MARKDOWN_MISMATCHES])
            if bucket.mismatch_count > MAX_MARKDOWN_MISMATCHES:
                displayed += ", …"
            note = (
                f"{bucket.mismatch_count} file(s) with unexpected suffixes: {displayed}"
            )
        else:
            note = "All files match the directory extension."
        lines.append(
            f"| `{bucket.extension}` | {bucket.file_count} | {bucket.directory_count} | "
            f"{bucket.mismatch_count} | {note} |"
        )
    lines.append("")
    lines.append(
        "Run `python assets/py/report_assets_layout.py --json assets/json/assets_layout_summary.json "
        "--markdown assets/md/assets_layout_summary.md` after reorganising the tree to "
        "keep this snapshot current."
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarise the assets/ extension layout")
    parser.add_argument(
        "--assets-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Path to the assets directory to inspect",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "json" / "assets_layout_summary.json",
        help="Destination for the JSON summary",
    )
    parser.add_argument(
        "--markdown",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "md" / "assets_layout_summary.md",
        help="Destination for the Markdown summary",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Echo a brief human-readable summary to stdout",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    assets_root = args.assets_root.resolve()
    if not assets_root.is_dir():
        raise SystemExit(f"Assets directory not found: {assets_root}")

    report = _collect_report(assets_root)
    _write_json(report, args.json.resolve())
    _write_markdown(report, args.markdown.resolve())

    if args.print:
        print(
            f"Scanned {report.total_buckets} buckets with {report.total_files} files and "
            f"{report.total_directories} nested directories inside {assets_root}"
        )
        mismatched_total = sum(bucket.mismatch_count for bucket in report.buckets)
        if mismatched_total:
            print(f"Found {mismatched_total} file(s) with unexpected suffixes; check the Markdown report for details")
        else:
            print("All files matched their bucket extensions.")


if __name__ == "__main__":
    main()
