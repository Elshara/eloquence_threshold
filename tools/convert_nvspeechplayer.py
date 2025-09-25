#!/usr/bin/env python3
"""Convert NV Speech Player phoneme data into Eloquence Threshold JSON.

The script reads the ``data.py`` table from the NV Speech Player project and
emits a JSON payload compatible with :mod:`phoneme_catalog`. Use this helper to
refresh ``eloquence_data/phonemes/nvspeechplayer_core.json`` whenever you pull a
new upstream revision.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
from datetime import datetime, timezone
from typing import Dict, List, Mapping, MutableMapping, Optional, Sequence, Tuple

CATEGORY_MAP = {
    "_isVowel": "NVSpeechPlayer vowels",
    "_isNasal": "NVSpeechPlayer nasals",
    "_isAfricate": "NVSpeechPlayer affricates",
    "_isLiquid": "NVSpeechPlayer liquids",
    "_isSemivowel": "NVSpeechPlayer semivowels",
    "_isStop": "NVSpeechPlayer stops",
    "_isVoiced": "NVSpeechPlayer voiced consonants",
}

FLAG_LABELS = {
    "_isVowel": "vowel",
    "_isNasal": "nasal",
    "_isLiquid": "liquid",
    "_isSemivowel": "semivowel",
    "_isStop": "stop",
    "_isAfricate": "affricate",
    "_isVoiced": "voiced",
    "_copyAdjacent": "copies-adjacent-formants",
}

AMPLITUDE_KEYS = ("voiceAmplitude", "aspirationAmplitude", "fricationAmplitude", "parallelBypass")
SPECIAL_KEYS = ("cfNP", "cfN0", "cbNP", "cbN0", "caNP")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert NV Speech Player data.py phoneme frames into Eloquence Threshold "
            "JSON so NVDA users can browse them from the Speech dialog."
        )
    )
    parser.add_argument(
        "source",
        nargs="?",
        default=os.path.join("..", "NVSpeechPlayer"),
        help="Path to a checkout of the NV Speech Player repository (default: ../NVSpeechPlayer)",
    )
    parser.add_argument(
        "--data",
        dest="data_path",
        help="Explicit path to the NV Speech Player data.py file",
    )
    parser.add_argument(
        "--output",
        dest="output_path",
        default=os.path.join("eloquence_data", "phonemes", "nvspeechplayer_core.json"),
        help="Where to write the generated JSON payload",
    )
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Skip embedding git revision metadata in the output",
    )
    return parser.parse_args()


def load_phoneme_data(path: str, source_root: str) -> Mapping[str, Mapping[str, object]]:
    abspath = os.path.abspath(path)
    source_root = os.path.abspath(source_root)
    # Ensure abspath is under source_root
    if not abspath.startswith(source_root + os.sep):
        raise SystemExit(f"Refusing to open data file outside of source root: {abspath}")
    with open(abspath, "r", encoding="utf-8-sig") as handle:
        payload = handle.read()
    try:
        data = ast.literal_eval(payload)
    except (SyntaxError, ValueError) as error:
        raise SystemExit(f"Unable to parse NV Speech Player data at {path}: {error}")
    if not isinstance(data, MutableMapping):
        raise SystemExit(f"Unexpected data structure in {path}; expected a dict")
    return data


def resolve_category(entry: Mapping[str, object]) -> str:
    for flag, category in (
        ("_isVowel", CATEGORY_MAP["_isVowel"]),
        ("_isNasal", CATEGORY_MAP["_isNasal"]),
        ("_isAfricate", CATEGORY_MAP["_isAfricate"]),
        ("_isLiquid", CATEGORY_MAP["_isLiquid"]),
        ("_isSemivowel", CATEGORY_MAP["_isSemivowel"]),
        ("_isStop", CATEGORY_MAP["_isStop"]),
    ):
        if entry.get(flag):
            if flag == "_isStop" and not entry.get("_isVoiced"):
                return "NVSpeechPlayer voiceless stops"
            if flag == "_isStop":
                return "NVSpeechPlayer voiced stops"
            return category
    if entry.get("_isVoiced"):
        return CATEGORY_MAP["_isVoiced"]
    return "NVSpeechPlayer voiceless consonants"


def describe_entry(name: str, entry: Mapping[str, object]) -> str:
    labels = [label for key, label in FLAG_LABELS.items() if entry.get(key)]
    if labels:
        return f"NV Speech Player {'/'.join(labels)} phoneme"
    return "NV Speech Player phoneme frame"


def format_series(entry: Mapping[str, object], prefix: str, count: int) -> Tuple[str, ...]:
    items: List[str] = []
    for index in range(1, count + 1):
        key = f"{prefix}{index}"
        if key in entry:
            items.append(f"{key}={entry[key]}")
    return tuple(items)


def collect_strings(entry: Mapping[str, object], keys: Sequence[str]) -> Tuple[str, ...]:
    values: List[str] = []
    for key in keys:
        if key in entry:
            values.append(f"{key}={entry[key]}")
    return tuple(values)


def build_payload(data: Mapping[str, Mapping[str, object]], revision: Optional[str]) -> Dict[str, object]:
    phonemes: List[Dict[str, object]] = []
    for name, entry in sorted(data.items(), key=lambda item: item[0]):
        category = resolve_category(entry)
        attributes: Dict[str, Tuple[str, ...]] = {}
        classification = tuple(label for key, label in FLAG_LABELS.items() if entry.get(key))
        if classification:
            attributes["classification"] = classification
        cascade_formants = format_series(entry, "cf", 6)
        if cascade_formants:
            attributes["cascadeFormants"] = cascade_formants
        cascade_bandwidths = format_series(entry, "cb", 6)
        if cascade_bandwidths:
            attributes["cascadeBandwidths"] = cascade_bandwidths
        parallel_formants = format_series(entry, "pf", 6)
        if parallel_formants:
            attributes["parallelFormants"] = parallel_formants
        parallel_bandwidths = format_series(entry, "pb", 6)
        if parallel_bandwidths:
            attributes["parallelBandwidths"] = parallel_bandwidths
        amplitudes = collect_strings(entry, AMPLITUDE_KEYS)
        if amplitudes:
            attributes["amplitudes"] = amplitudes
        specials = collect_strings(entry, SPECIAL_KEYS)
        if specials:
            attributes["special"] = specials
        notes: List[str] = []
        if entry.get("_copyAdjacent"):
            notes.append(
                "Copies formant targets from the surrounding phoneme when used as aspiration or inserted silence."
            )
        phonemes.append(
            {
                "name": name,
                "category": category,
                "description": describe_entry(name, entry),
                "ipa": [name] if name else [],
                "notes": notes,
                "attributes": attributes,
            }
        )
    metadata: Dict[str, object] = {
        "source": "NV Speech Player data.py",
        "generated": datetime.now(timezone.utc).date().isoformat(),
        "license": "GPL-2.0-or-later (NV Speech Player)",
    }
    if revision:
        metadata["revision"] = revision
    return {
        "category": "NV Speech Player phoneme frames",
        "metadata": metadata,
        "phonemes": phonemes,
    }


def detect_revision(source_root: str) -> Optional[str]:
    result = subprocess.run(
        ["git", "-C", source_root, "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def main() -> None:
    args = parse_arguments()
    source_root = os.path.abspath(args.source)
    data_path = args.data_path or os.path.join(source_root, "data.py")
    data = load_phoneme_data(data_path, source_root)
    revision = None if args.no_metadata else detect_revision(source_root)
    payload = build_payload(data, revision)
    output_path = os.path.abspath(args.output_path)
    # Constrain the output path to a safe output directory root
    default_output_dir = os.path.abspath(os.path.join("eloquence_data", "phonemes"))
    output_dir = os.path.dirname(output_path)
    # Ensure that output_dir is within the default_output_dir
    if not output_dir.startswith(default_output_dir + os.sep) and output_dir != default_output_dir:
        raise SystemExit(f"Refusing to write output file outside of allowed directory: {output_path}")
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    print(f"Wrote {output_path} with {len(payload['phonemes'])} entries")


if __name__ == "__main__":
    main()
