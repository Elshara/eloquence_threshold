"""Audit helper for download.nvaccess.org.

This tool walks the NV Access download index, captures metadata for each
directory entry, and evaluates how new NVDA builds relate to the
eloquence_threshold manifest.  It is intentionally incremental: callers can
limit the traversal depth or restrict the set of directories to avoid flooding
the output while still surfacing the newest releases, betas, and alphas.

Example usage::

    python tools/audit_nvaccess_downloads.py \
        --roots releases/stable snapshots/alpha \
        --max-depth 3 \
        --limit-per-dir 20 \
        --markdown docs/download_nvaccess_snapshot.md

The script always prints a concise summary to stdout.  Optional JSON and
Markdown outputs make it easy to cache a snapshot inside the repository for
documentation or regression tracking.
"""

from __future__ import annotations

import argparse
import configparser
import dataclasses
import json
import os
import posixpath
import re
import ssl
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from typing import Dict, List, Optional, Sequence, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "https://download.nvaccess.org/"


@dataclass
class ListingEntry:
    """Represents a row from the NV Access download index."""

    path: str
    url: str
    name: str
    entry_type: str
    size_bytes: Optional[int]
    size_display: str
    modified: Optional[datetime]
    target: Optional[str]
    depth: int

    def to_json(self) -> Dict[str, object]:
        return {
            "path": self.path,
            "url": self.url,
            "name": self.name,
            "entryType": self.entry_type,
            "sizeBytes": self.size_bytes,
            "sizeDisplay": self.size_display,
            "modified": self.modified.isoformat() if self.modified else None,
            "target": self.target,
            "depth": self.depth,
        }


@dataclass
class Severity:
    level: str
    reason: str

    def to_json(self) -> Dict[str, str]:
        return {"level": self.level, "reason": self.reason}


class IndexParser(HTMLParser):
    """Parses the NV Access directory listing HTML into dictionaries."""

    def __init__(self) -> None:
        super().__init__()
        self.entries: List[Dict[str, str]] = []
        self._current: Optional[Dict[str, str]] = None
        self._current_field: Optional[str] = None
        self._current_type: Optional[str] = None

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        attr_map = {k: v for k, v in attrs}
        if tag == "li":
            self._current = {"name": "", "target": "", "size": "", "date": "", "href": ""}
            self._current_field = None
            self._current_type = None
        elif self._current is not None and tag == "span":
            class_name = attr_map.get("class", "")
            if class_name:
                field = class_name.split()[0]
                if field in ("name", "target", "size", "date"):
                    self._current_field = field
                    # ensure key exists for accumulation
                    self._current.setdefault(field, "")
        elif self._current is not None and tag == "a":
            href = attr_map.get("href", "")
            if href:
                self._current["href"] = href
            class_name = attr_map.get("class", "")
            if class_name:
                # the first token encodes dir/file/symlink
                self._current_type = class_name.split()[0]

    def handle_data(self, data: str) -> None:
        if self._current is None or self._current_field is None:
            return
        fragment = data.strip()
        if fragment:
            existing = self._current.get(self._current_field, "")
            if existing:
                fragment = existing + fragment
            self._current[self._current_field] = fragment

    def handle_endtag(self, tag: str) -> None:
        if tag == "span":
            self._current_field = None
        elif tag == "li" and self._current is not None:
            record = dict(self._current)
            if self._current_type:
                record["type"] = self._current_type
            self.entries.append(record)
            self._current = None
            self._current_field = None
            self._current_type = None


SIZE_PATTERN = re.compile(r"^(?P<value>[0-9]+(?:\.[0-9]+)?)\s*(?P<unit>[KMGTP]?B)$", re.IGNORECASE)


def parse_size(size_str: str) -> Tuple[Optional[int], str]:
    text = size_str.strip()
    if not text or text in {"-", ""}:
        return None, ""
    match = SIZE_PATTERN.match(text)
    if not match:
        return None, text
    value = float(match.group("value"))
    unit = match.group("unit").upper()
    exponent = {
        "B": 0,
        "KB": 1,
        "MB": 2,
        "GB": 3,
        "TB": 4,
        "PB": 5,
    }[unit]
    size_bytes = int(value * (1024 ** exponent))
    return size_bytes, f"{value:g} {unit}"


def parse_date(date_str: str) -> Optional[datetime]:
    text = date_str.strip()
    if not text:
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def fetch_listing(url: str, insecure: bool = False) -> List[Dict[str, str]]:
    context = None
    if insecure:
        context = ssl._create_unverified_context()  # noqa: SLF001 - intentional override for CLI flag
    request = Request(url, headers={"User-Agent": "eloquence-threshold-audit/1.0"})
    with urlopen(request, context=context) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        payload = response.read().decode(charset, errors="replace")
    parser = IndexParser()
    parser.feed(payload)
    return parser.entries


def normalize_path(base: str, child: str) -> str:
    # ensure trailing slash on directories stays intact for recursion decisions
    combined = posixpath.normpath(posixpath.join(base, child))
    if child.endswith("/") and not combined.endswith("/"):
        combined += "/"
    return combined.lstrip("./")


def build_listing_entries(
    base_url: str,
    roots: Sequence[str],
    max_depth: int,
    limit_per_dir: Optional[int],
    insecure: bool,
) -> List[ListingEntry]:
    queue: List[Tuple[str, int]] = []
    visited: set[str] = set()
    results: List[ListingEntry] = []

    for root in roots:
        root_path = root.strip("/") + "/" if root.strip("/") else ""
        queue.append((root_path, 0))

    while queue:
        current_path, depth = queue.pop(0)
        url = urljoin(base_url, current_path)
        try:
            raw_entries = fetch_listing(url, insecure=insecure)
        except HTTPError as exc:
            print(f"Failed to fetch {url}: HTTP {exc.code}")
            continue
        except URLError as exc:
            print(f"Failed to fetch {url}: {exc.reason}")
            continue

        if limit_per_dir is not None:
            raw_entries = raw_entries[:limit_per_dir]

        for record in raw_entries:
            href = record.get("href", "")
            if not href or href == "../":
                continue
            entry_path = normalize_path(current_path, href)
            if entry_path in visited:
                continue
            visited.add(entry_path)

            entry_type = record.get("type", "") or "file"
            size_bytes, size_display = parse_size(record.get("size", ""))
            modified = parse_date(record.get("date", ""))
            target = record.get("target", "") or None
            entry = ListingEntry(
                path=entry_path,
                url=urljoin(base_url, entry_path),
                name=record.get("name", href).strip(),
                entry_type=entry_type,
                size_bytes=size_bytes,
                size_display=size_display,
                modified=modified,
                target=target,
                depth=depth,
            )
            results.append(entry)

            if entry_type == "dir" and depth + 1 <= max_depth:
                queue.append((entry_path, depth + 1))

    return results


@dataclass
class ManifestInfo:
    minimum_nvda: str
    last_tested_nvda: str


def load_manifest_info(manifest_path: str) -> ManifestInfo:
    parser = configparser.ConfigParser()
    with open(manifest_path, "r", encoding="utf-8") as handle:
        payload = handle.read()
    parser.read_string("[manifest]\n" + payload)
    section = parser["manifest"]
    minimum_nvda = section.get("minimumNVDAVersion", fallback="0")
    last_tested = section.get("lastTestedNVDAVersion", fallback="0")
    return ManifestInfo(minimum_nvda, last_tested)


VERSION_PATTERN = re.compile(r"(\d{4}\.\d(?:\.\d)?)")
ALPHA_PATTERN = re.compile(r"alpha-(\d+)", re.IGNORECASE)


def parse_release_version(entry: ListingEntry) -> Optional[str]:
    if entry.path.startswith("releases/"):
        match = VERSION_PATTERN.search(entry.path)
        if match:
            return match.group(1)
    if entry.path.startswith("snapshots/"):
        match = ALPHA_PATTERN.search(entry.path)
        if match:
            return f"alpha-{match.group(1)}"
    return None


def compare_version_strings(version_a: str, version_b: str) -> int:
    """Compares NVDA version strings, returning -1, 0, or 1."""

    def normalize(version: str) -> Tuple[int, ...]:
        if version.startswith("alpha-"):
            return (9, int(version.split("-", 1)[1]))
        parts = version.split(".")
        numbers = [int(part) for part in parts if part.isdigit()]
        return tuple(numbers + [0] * (3 - len(numbers)))

    return (normalize(version_a) > normalize(version_b)) - (normalize(version_a) < normalize(version_b))


def load_validated_snapshots(path: Optional[str]) -> Dict[str, str]:
    if not path or not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    result: Dict[str, str] = {}
    for channel, payload in data.items():
        if isinstance(payload, dict) and "lastValidated" in payload:
            result[channel] = str(payload["lastValidated"])
    return result


def classify_entry(
    entry: ListingEntry,
    manifest: ManifestInfo,
    validated_snapshots: Dict[str, str],
    current_nvda: Optional[str],
) -> Optional[Severity]:
    version = parse_release_version(entry)
    if not version:
        return None

    channel = "stable"
    if entry.path.startswith("snapshots/"):
        channel = entry.path.split("/", 2)[1]

    if version.startswith("alpha-"):
        validated = validated_snapshots.get(channel)
        if validated is None:
            return Severity("high", f"No validated {channel} snapshot recorded; review {entry.name}")
        if compare_version_strings(version, validated) > 0:
            return Severity("high", f"Snapshot {version} is newer than validated {validated}")
        if compare_version_strings(version, validated) == 0:
            return Severity("medium", f"Snapshot {version} matches the validated build")
        return Severity("low", f"Snapshot {version} is older than validated {validated}")

    # Stable / release builds
    last_tested = manifest.last_tested_nvda
    minimum = manifest.minimum_nvda
    if compare_version_strings(version, last_tested) > 0:
        return Severity("high", f"Release {version} is newer than last tested {last_tested}")
    if compare_version_strings(version, minimum) < 0:
        return Severity("medium", f"Release {version} predates minimum supported {minimum}")

    if current_nvda and not current_nvda.lower().startswith("alpha-"):
        cmp_current = compare_version_strings(version, current_nvda)
        if cmp_current == 0:
            return Severity("medium", f"Release {version} matches the currently running NVDA build")
        if cmp_current > 0:
            return Severity("high", f"Release {version} is ahead of the current NVDA build {current_nvda}")

    return Severity("info", f"Release {version} is within the tested support window")


def render_markdown(entries: List[ListingEntry], severities: Dict[str, Severity]) -> str:
    lines = ["# NV Access download snapshot", "", "| Depth | Path | Type | Size | Modified | Severity | Notes |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for entry in entries:
        severity = severities.get(entry.path)
        severity_text = severity.level if severity else ""
        notes = severity.reason if severity else ""
        lines.append(
            "| {depth} | `{path}` | {etype} | {size} | {modified} | {severity} | {notes} |".format(
                depth=entry.depth,
                path=entry.path or "/",
                etype=entry.entry_type,
                size=entry.size_display or ("-" if entry.entry_type == "dir" else ""),
                modified=entry.modified.isoformat(sep=" ") if entry.modified else "",
                severity=severity_text,
                notes=notes.replace("|", "\\|") if notes else "",
            )
        )
    return "\n".join(lines) + "\n"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Base URL for NV Access downloads")
    parser.add_argument("--roots", nargs="*", default=[""], help="Root paths to traverse (relative to the base URL)")
    parser.add_argument("--max-depth", type=int, default=2, help="Maximum traversal depth")
    parser.add_argument("--limit-per-dir", type=int, default=25, help="Limit entries per directory to avoid huge outputs")
    parser.add_argument("--manifest", default="manifest.ini", help="Path to the add-on manifest")
    parser.add_argument("--validated-snapshots", default="docs/validated_nvda_builds.json", help="JSON file with last validated snapshots")
    parser.add_argument("--current-nvda", help="Version string for the NVDA build currently in use")
    parser.add_argument("--json", dest="json_path", help="Optional path to write JSON output")
    parser.add_argument("--markdown", dest="markdown_path", help="Optional path to write Markdown output")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS verification (useful on restricted networks)")

    args = parser.parse_args(argv)

    manifest = load_manifest_info(args.manifest)
    validated_snapshots = load_validated_snapshots(args.validated_snapshots)

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

    for entry in entries:
        severity = severities.get(entry.path)
        severity_label = severity.level if severity else "-"
        modified = entry.modified.isoformat(sep=" ") if entry.modified else "-"
        print(f"[{severity_label:>6}] {modified} | {entry.path} | {entry.entry_type} | {entry.size_display or '-'}")
        if severity:
            print(f"         -> {severity.reason}")

    if args.json_path:
        payload = {
            "baseUrl": args.base_url,
            "generated": datetime.now(UTC).isoformat(),
            "entries": [entry.to_json() for entry in entries],
            "severities": {path: severity.to_json() for path, severity in severities.items()},
            "manifest": dataclasses.asdict(manifest),
            "validatedSnapshots": validated_snapshots,
        }
        os.makedirs(os.path.dirname(args.json_path), exist_ok=True)
        with open(args.json_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)

    if args.markdown_path:
        markdown = render_markdown(entries, severities)
        os.makedirs(os.path.dirname(args.markdown_path), exist_ok=True)
        with open(args.markdown_path, "w", encoding="utf-8") as handle:
            handle.write(markdown)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
