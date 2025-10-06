"""Inventory binary speechdata payloads for NVDA/CodeQL audits.

This helper walks the :mod:`speechdata` tree, classifies files as binary or
text, and records which NVDA loaders consume the payloads.  The generated
JSON/Markdown artefacts help reviewers confirm that non-editable DLLs, EXEs,
voice archives, and compiled caches live outside the extension-first
``assets/`` hierarchy while documenting which tooling still depends on each
engine.  Keeping the index up to date is a prerequisite for packaging the
``eloquence.nvda-addon`` on current NVDA alpha builds and for running CodeQL
scans against the editable Python sources without shipping opaque binaries.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Dict, Iterable, List, Optional

MODULE_DIR = Path(__file__).resolve().parent
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import resource_paths


# Extensions that typically contain human-readable text even when staged inside
# ``speechdata``.  Everything else is treated as binary by default so DLLs,
# EXEs, compiled caches, and opaque voice archives are highlighted for
# remediation.
TEXTUAL_EXTENSIONS = {
    ".cfg",
    ".csv",
    ".dic",
    ".ini",
    ".json",
    ".lex",
    ".lic",
    ".lst",
    ".md",
    ".txt",
}


# Engines mapped to the NVDA loader modules that currently consume their
# binaries.  This keeps the resulting reports actionable for CodeQL reviewers
# and NVDA packagers.
ENGINE_LOADERS: Dict[str, List[str]] = {
    "eloquence": ["assets/py/Eloquence.py"],
    "nv_speech_player": [
        "assets/py/speechPlayer.py",
        "assets/py/old_speechPlayer.py",
        "assets/py/smpsoft.py",
    ],
    "pico": ["assets/py/pico.py"],
    "dectalk": ["assets/py/_dectalk.py"],
    "fonixtalk": ["assets/py/_fonixtalk.py"],
    "bestspeech": ["assets/py/bestspeech.py"],
    "brailab": ["assets/py/brailab.py"],
    "captain": ["assets/py/captain.py"],
    "gregor": ["assets/py/gregor.py"],
    "orpheus": ["assets/py/gregor.py"],
    "sam": ["assets/py/old_speechPlayer.py"],
}


# Short descriptions capture why each engine remains in the repository.  These
# surface in the Markdown report alongside loader references so the audit stays
# understandable to contributors reviewing the speechdata tree for the first
# time.
ENGINE_PURPOSE: Dict[str, str] = {
    "eloquence": (
        "Primary Eloquence runtime shipped to NVDA users; DLLs and .SYN voices"
        " are required for 32-bit compatibility during alpha packaging drills."
    ),
    "nv_speech_player": (
        "Modern NV Speech Player bridge that backs NVDA's bundled voices;"
        " binaries must match upstream NV Access releases."
    ),
    "pico": (
        "SVOX Pico offline engine used for lightweight language coverage"
        " during NVDA smoketests."
    ),
    "dectalk": (
        "Classic DECtalk runtime retained for heritage voice research and"
        " interoperability testing."
    ),
    "fonixtalk": (
        "FonixTalk successor to DECtalk maintained for archival driver"
        " validation against NVDA alpha builds."
    ),
    "bestspeech": "Legacy Taiwanese driver kept for provenance research.",
    "brailab": "Hungarian BraiLab+ runtime pending Python 3.13 rebuild.",
    "captain": "Captain synthesizer bridge awaiting modern audio validation.",
    "gregor": "Orpheus/Gregor hybrid runtime archived for compatibility tests.",
    "orpheus": (
        "Alias of Gregor runtime assets staged for potential future driver"
        " restoration."
    ),
    "sam": "SAM (Software Automatic Mouth) samples preserved for testing.",
    "legacy": (
        "Unclassified speech archives awaiting provenance research before"
        " promotion into engine-specific buckets."
    ),
}


@dataclass
class FileRecord:
    relative_path: str
    extension: str
    size_bytes: int
    classification: str
    loaders: List[str]
    notes: Optional[str] = None


def iter_engine_files(engine_root: Path) -> Iterable[Path]:
    for path in sorted(engine_root.rglob("*")):
        if path.is_file():
            yield path


def classify_path(path: Path) -> str:
    """Return ``"binary"`` or ``"text"`` for *path*."""

    suffix = path.suffix.lower()
    if suffix in TEXTUAL_EXTENSIONS:
        return "text"
    # Fallback heuristic: consider files with NUL bytes within the first 1024
    # bytes binary.  This keeps icons, DLLs, and compiled caches marked even if
    # they have uncommon suffixes.
    try:
        chunk = path.read_bytes()[:1024]
    except OSError:
        return "binary"
    if b"\x00" in chunk:
        return "binary"
    return "text"


def build_engine_records(engine: str, root: Path) -> Dict[str, object]:
    loaders = ENGINE_LOADERS.get(engine, [])
    files: List[FileRecord] = []
    for path in iter_engine_files(root):
        classification = classify_path(path)
        entry_loaders = loaders if classification == "binary" else []
        notes: Optional[str] = None
        if not loaders and classification == "binary":
            notes = "No active loader references."
        files.append(
            FileRecord(
                relative_path=str(path.relative_to(root).as_posix()),
                extension=path.suffix.lower() or "(none)",
                size_bytes=path.stat().st_size,
                classification=classification,
                loaders=entry_loaders,
                notes=notes,
            )
        )

    binaries = sum(1 for record in files if record.classification == "binary")
    text = len(files) - binaries

    return {
        "engine": engine,
        "path": str(root.relative_to(resource_paths.repo_root()).as_posix()),
        "purpose": ENGINE_PURPOSE.get(engine, ""),
        "loader_modules": loaders,
        "file_count": len(files),
        "binary_count": binaries,
        "text_count": text,
        "files": [asdict(record) for record in files],
    }


def collect_binary_assets() -> Dict[str, object]:
    root = resource_paths.speechdata_root()
    engines: List[Dict[str, object]] = []
    if not root.exists():
        return {
            "generated": datetime.now(timezone.utc).isoformat(),
            "engines": engines,
        }

    for engine_dir in sorted(root.iterdir()):
        if not engine_dir.is_dir():
            continue
        engines.append(build_engine_records(engine_dir.name, engine_dir))

    return {
        "generated": datetime.now(timezone.utc).isoformat(),
        "engines": engines,
    }


def render_markdown(report: Dict[str, object]) -> str:
    lines: List[str] = []
    lines.append("# Speechdata binary index")
    lines.append("")
    lines.append(
        "Generated on {} to document which binaries live under `speechdata/` and"
        " which NVDA loaders still consume them.".format(report["generated"])
    )
    lines.append("")

    engines: List[Dict[str, object]] = report["engines"]
    if not engines:
        lines.append("No speechdata directories were discovered.")
        return "\n".join(lines)

    for engine in engines:
        lines.append(f"## {engine['engine']}")
        purpose = engine.get("purpose")
        if purpose:
            lines.append(purpose)
            lines.append("")

        loader_modules = engine.get("loader_modules") or []
        if loader_modules:
            lines.append("**Loader modules:** " + ", ".join(loader_modules))
        else:
            lines.append("**Loader modules:** _None_ (pending migration)")
        lines.append("")

        counts = (
            f"{engine['file_count']} files | {engine['binary_count']} binary |"
            f" {engine['text_count']} text"
        )
        lines.append(counts)
        lines.append("")
        lines.append("| File | Extension | Size (bytes) | Classification | Notes |")
        lines.append("| --- | --- | ---: | --- | --- |")

        for record in engine["files"]:
            notes = record.get("notes") or ""
            rel_path = record["relative_path"]
            if record["loaders"]:
                rel_path = f"**{rel_path}**"
            lines.append(
                "| {file} | {ext} | {size} | {cls} | {notes} |".format(
                    file=rel_path,
                    ext=record["extension"],
                    size=record["size_bytes"],
                    cls=record["classification"],
                    notes=notes,
                )
            )
        lines.append("")

    return "\n".join(lines)


def write_json(path: Path, report: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown(path: Path, markdown: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown + "\n", encoding="utf-8")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        type=Path,
        help="Path to the JSON report to write (defaults to assets/json/binary_asset_index.json)",
    )
    parser.add_argument(
        "--markdown",
        type=Path,
        help="Path to the Markdown report to write (defaults to assets/md/binary_asset_index.md)",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print a short summary to stdout",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    report = collect_binary_assets()
    markdown = render_markdown(report)

    json_path = args.json or (resource_paths.assets_root() / "json" / "binary_asset_index.json")
    markdown_path = args.markdown or (resource_paths.assets_root() / "md" / "binary_asset_index.md")

    write_json(json_path, report)
    write_markdown(markdown_path, markdown)

    if args.print:
        engines = report.get("engines", [])
        print(f"Indexed {len(engines)} speechdata engines")
        for engine in engines:
            print(
                f"- {engine['engine']}: {engine['binary_count']} binary /"
                f" {engine['text_count']} text files"
            )
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
