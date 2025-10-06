"""Utility to refresh the bundled eSpeak NG phoneme catalogue.

This helper copies the upstream ``phsource/phonemes`` file from an eSpeak NG
checkout (or unpacked data directory) into ``assets/txt/espeak_phonemes.txt``.
Keeping the catalogue in sync with eSpeak ensures Eloquence exposes the latest
phoneme categories and sample comments when users explore NVDA's voice dialog.

Usage examples::

    # Point the script at a cloned repository
    python tools/refresh_espeak_phonemes.py /path/to/espeak-ng

    # Or reuse a standalone data bundle
    python tools/refresh_espeak_phonemes.py /path/to/espeak-ng-data \
        --output custom_phonemes.txt --commit HEAD

The script accepts both repositories and direct file paths. When given a
 directory it searches a handful of known layouts before failing with a clear
 error message so contributors understand how to supply the correct source.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Optional

import resource_paths


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Copy eSpeak NG's phoneme catalogue into this repository."
    )
    parser.add_argument(
        "source",
        help=(
            "Path to an eSpeak NG checkout, an extracted espeak-ng-data package, "
            "or the phonemes file itself."
        ),
    )
    parser.add_argument(
        "--output",
        help="Destination path for the copied phoneme catalogue.",
        default=_default_output_path(),
    )
    parser.add_argument(
        "--commit",
        help=(
            "Optional commit or version identifier to add as a comment at the "
            "top of the generated file."
        ),
    )
    args = parser.parse_args()

    source_path = Path(args.source)
    phoneme_file = _resolve_phoneme_source(source_path)
    if phoneme_file is None:
        parser.error(
            "Unable to locate an eSpeak NG phoneme file under %s" % source_path
        )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = phoneme_file.read_text(encoding="utf-8")
    normalized = _normalize_newlines(content)

    if args.commit:
        header = [
            "// eSpeak NG phoneme catalogue refreshed from %s" % phoneme_file,
            "// Source commit: %s" % args.commit,
            "",
        ]
        normalized = "\n".join(header) + normalized.lstrip("\n")

    output_path.write_text(normalized, encoding="utf-8")
    print("Wrote %s (%d bytes)" % (output_path, output_path.stat().st_size))


def _resolve_phoneme_source(base_path: Path) -> Optional[Path]:
    if base_path.is_file():
        return base_path

    search_roots: Iterable[Path] = (
        base_path,
        base_path / "espeak-ng-data",
        base_path / "data",
        base_path / "source",
    )
    candidate_relpaths = (
        Path("phsource/phonemes"),
        Path("phonemes"),
    )
    for root in search_roots:
        for relpath in candidate_relpaths:
            candidate = root / relpath
            if candidate.is_file():
                return candidate
    return None


def _normalize_newlines(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.endswith("\n"):
        text += "\n"
    return text


def _default_output_path() -> str:
    return str(resource_paths.phoneme_inventory_path())


if __name__ == "__main__":
    main()
