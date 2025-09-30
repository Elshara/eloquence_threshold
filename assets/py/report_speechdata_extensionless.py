"""Audit extensionless files under ``speechdata/`` and suggest follow-up actions.

The extension-first reshuffle parked legacy datasets that still rely on
extensionless filenames inside ``speechdata/``.  This helper inventories those
files, attempts lightweight file-type classification, and writes JSON and
Markdown reports so we can plan migrations without breaking NVDA loaders or the
cached datasets referenced by our CodeQL checks.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEECHDATA_ROOT = REPO_ROOT / "speechdata"
DEFAULT_JSON = REPO_ROOT / "assets" / "json" / "speechdata_extensionless_inventory.json"
DEFAULT_MARKDOWN = REPO_ROOT / "assets" / "md" / "speechdata_extensionless_inventory.md"
MAX_BYTES_TO_SAMPLE = 4096


@dataclass
class ExtensionlessEntry:
    relative_path: str
    size_bytes: int
    top_level: str
    classification: str
    recommended_extension: Optional[str]
    notes: str


SIGNATURES: Tuple[Tuple[bytes, str, str, Optional[str]], ...] = (
    (b"RIFF", "audio/wav", "RIFF container (likely WAV)", "wav"),
    (b"OggS", "audio/ogg", "Ogg bitstream", "ogg"),
    (b"fLaC", "audio/flac", "FLAC stream", "flac"),
    (b"ID3", "audio/mp3", "MP3 with ID3 tag", "mp3"),
    (b"\xff\xfb", "audio/mp3", "MP3 frame (0xFFFB)", "mp3"),
    (b"\xff\xf3", "audio/mp3", "MP3 frame (0xFFF3)", "mp3"),
    (b"MThd", "audio/midi", "Standard MIDI header", "mid"),
    (b"PK\x03\x04", "archive/zip", "ZIP archive", "zip"),
    (b"7z\xbc\xaf'\x1c", "archive/7z", "7-Zip archive", "7z"),
    (b"%PDF", "document/pdf", "PDF document", "pdf"),
    (b"{\n", "text/json", "Likely JSON (starts with '{')", "json"),
    (b"[\n", "text/json", "Likely JSON array (starts with '[')", "json"),
    (b"<?xm", "text/xml", "XML declaration", "xml"),
)


def iter_extensionless_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix:
            continue
        yield path


def sample_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    return data[:MAX_BYTES_TO_SAMPLE]


def classify_sample(data: bytes) -> Tuple[str, Optional[str], str]:
    if not data:
        return "empty", None, "File has no content"

    for signature, classification, note, recommendation in SIGNATURES:
        if data.startswith(signature):
            return classification, recommendation, note

    if data.startswith(b"\xef\xbb\xbf"):
        return "text/utf-8-bom", "txt", "UTF-8 text with BOM"

    # Treat printable ASCII (plus whitespace) as text.
    printable = sum(1 for byte in data if 32 <= byte <= 126 or byte in (9, 10, 13))
    ratio = printable / len(data)
    if ratio > 0.85:
        try:
            data.decode("utf-8")
            return "text/utf-8", "txt", "UTF-8 text"
        except UnicodeDecodeError:
            return "text/unknown", "txt", "Text-like but not UTF-8"

    return "binary/unknown", None, "Binary payload (no known signature)"


def build_entries() -> List[ExtensionlessEntry]:
    entries: List[ExtensionlessEntry] = []
    for path in iter_extensionless_files(SPEECHDATA_ROOT):
        sample = sample_bytes(path)
        classification, recommendation, note = classify_sample(sample)
        relative = path.relative_to(SPEECHDATA_ROOT).as_posix()
        top_level = relative.split("/", 1)[0] if "/" in relative else relative
        entries.append(
            ExtensionlessEntry(
                relative_path=relative,
                size_bytes=path.stat().st_size,
                top_level=top_level,
                classification=classification,
                recommended_extension=recommendation,
                notes=note,
            )
        )
    return entries


def summarise_by(entries: Iterable[ExtensionlessEntry], attribute: str) -> Dict[str, Dict[str, object]]:
    summary: Dict[str, Dict[str, object]] = {}
    for entry in entries:
        key = getattr(entry, attribute)
        bucket = summary.setdefault(key, {"files": 0, "bytes": 0})
        bucket["files"] += 1
        bucket["bytes"] += entry.size_bytes
    return dict(sorted(summary.items()))


def write_json(entries: List[ExtensionlessEntry], destination: Path) -> None:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "speechdata_root": str(SPEECHDATA_ROOT),
        "total_extensionless_files": len(entries),
        "summary_by_top_level": summarise_by(entries, "top_level"),
        "summary_by_classification": summarise_by(entries, "classification"),
        "entries": [asdict(entry) for entry in entries],
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def format_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB"):
        if value < 1024 or unit == "GiB":
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} GiB"


def write_markdown(entries: List[ExtensionlessEntry], destination: Path) -> None:
    summary_by_top_level = summarise_by(entries, "top_level")
    summary_by_classification = summarise_by(entries, "classification")

    lines: List[str] = []
    lines.append("# Speechdata extensionless audit")
    lines.append("")
    lines.append(
        "This report lists every file under ``speechdata/`` without an extension. "
        "Use it alongside [`assets/md/speechdata_manifest.md`](speechdata_manifest.md) "
        "when planning migrations so NVDA packaging drills and CodeQL scans retain "
        "access to cached datasets."
    )
    lines.append("")
    lines.append("## Summary by top-level subtree")
    lines.append("")
    lines.append("| Subtree | Files | Size |")
    lines.append("| --- | ---: | ---: |")
    for key, info in summary_by_top_level.items():
        lines.append(f"| `{key}` | {info['files']} | {format_size(info['bytes'])} |")
    lines.append("")
    lines.append("## Summary by classification")
    lines.append("")
    lines.append("| Classification | Files | Size | Suggested extension |")
    lines.append("| --- | ---: | ---: | --- |")
    classification_extensions: Dict[str, Optional[str]] = {}
    for entry in entries:
        classification_extensions.setdefault(entry.classification, entry.recommended_extension)
    for key, info in summary_by_classification.items():
        recommendation = classification_extensions.get(key)
        suggestion = f"`{recommendation}`" if recommendation else "—"
        lines.append(f"| `{key}` | {info['files']} | {format_size(info['bytes'])} | {suggestion} |")
    lines.append("")
    lines.append("## File-level detail")
    lines.append("")
    lines.append("| Path | Size | Classification | Suggested extension | Notes |")
    lines.append("| --- | ---: | --- | --- | --- |")
    for entry in entries:
        suggestion = f"`{entry.recommended_extension}`" if entry.recommended_extension else "—"
        lines.append(
            f"| `{entry.relative_path}` | {format_size(entry.size_bytes)} | "
            f"`{entry.classification}` | {suggestion} | {entry.notes} |"
        )
    lines.append("")
    lines.append(
        "Regenerate this snapshot with ``python assets/py/report_speechdata_extensionless.py`` "
        "after migrating files. Pair it with ``python build.py --insecure --no-download --output "
        "dist/eloquence.nvda-addon`` to confirm the NVDA add-on still stages every dataset."
    )

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON, help="Where to write the JSON snapshot")
    parser.add_argument(
        "--markdown",
        type=Path,
        default=DEFAULT_MARKDOWN,
        help="Where to write the Markdown snapshot",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not SPEECHDATA_ROOT.is_dir():
        raise SystemExit(
            f"speechdata directory not found at {SPEECHDATA_ROOT}. Run the script from the repository root."
        )

    entries = build_entries()
    write_json(entries, args.json)
    write_markdown(entries, args.markdown)


if __name__ == "__main__":
    main()
