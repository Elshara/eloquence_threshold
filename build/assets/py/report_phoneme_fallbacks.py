"""Summarise phoneme fallback options across language profiles."""
from __future__ import annotations

import argparse
import datetime as _dt
import json
from collections import OrderedDict
from pathlib import Path
import sys
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from language_profiles import CharacterPronunciation, LanguageProfileCatalog, load_default_language_profiles
from phoneme_catalog import PhonemeInventory, load_default_inventory


def _timestamp() -> str:
    return (
        _dt.datetime.now(_dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _build_profile_entries(
    catalog: LanguageProfileCatalog, inventory: PhonemeInventory
) -> List[Dict[str, object]]:
    entries: List[Dict[str, object]] = []
    for profile in catalog:
        coverage: List[Dict[str, object]] = []
        coverage_counts = {"complete": 0, "partial": 0, "missing": 0}
        for symbol, entry in profile.characters.items():
            status, phonemes, remainder = _analyse_pronunciation(entry, inventory)
            coverage_counts[status] += 1
            coverage.append(
                {
                    "symbol": symbol,
                    "ipa": list(entry.ipa),
                    "spoken": entry.spoken,
                    "status": status,
                    "matchedPhonemes": phonemes,
                    "unmatched": remainder,
                }
            )
        entries.append(
            OrderedDict(
                [
                    ("id", profile.id),
                    ("display", profile.display_label()),
                    ("language", profile.language),
                    ("characterCount", len(profile.characters)),
                    ("coverage", coverage_counts),
                    ("entries", coverage),
                    ("stress", list(profile.stress_notes)),
                    ("sentenceStructure", list(profile.sentence_structure)),
                    ("grammar", list(profile.grammar_notes)),
                ]
            )
        )
    return entries


def _analyse_pronunciation(
    entry: CharacterPronunciation, inventory: PhonemeInventory
) -> Tuple[str, List[str], str]:
    if inventory.is_empty:
        return "missing", [], ""
    ipa_text = " ".join(entry.ipa)
    if not ipa_text:
        return "missing", [], ""
    matches, remainder = inventory.match_ipa_sequence(ipa_text)
    matched_names = [definition.name for definition in matches]
    status = "complete"
    if remainder and matched_names:
        status = "partial"
    elif not matched_names:
        status = "missing"
    return status, matched_names, remainder


def _summarise_phonemes(inventory: PhonemeInventory) -> List[Dict[str, object]]:
    summary: List[Dict[str, object]] = []
    for category_id, label in inventory.categories.items():
        for definition in inventory.phonemes_for_category(category_id):
            replacements = definition.replacement_options()
            summary.append(
                {
                    "name": definition.name,
                    "category": label,
                    "ipa": list(definition.ipa),
                    "replacementKinds": sorted({opt.kind for opt in replacements.values()}),
                    "replacementCount": len(replacements),
                }
            )
    return summary


def _build_summary() -> Dict[str, object]:
    inventory = load_default_inventory()
    profiles = load_default_language_profiles()
    profile_entries = _build_profile_entries(profiles, inventory)
    phoneme_summary: List[Dict[str, object]] = []
    if not inventory.is_empty:
        phoneme_summary = _summarise_phonemes(inventory)
    data: Dict[str, object] = {
        "metadata": {
            "generated": _timestamp(),
            "profileCount": len(profile_entries),
            "phonemeCount": len(phoneme_summary),
        },
        "profiles": profile_entries,
    }
    if phoneme_summary:
        data["phonemes"] = phoneme_summary
    return data


def _write_json(path: Path, data: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _render_markdown(data: Dict[str, object]) -> str:
    lines: List[str] = []
    metadata = data.get("metadata", {})
    generated = metadata.get("generated", "")
    profile_count = metadata.get("profileCount", 0)
    phoneme_count = metadata.get("phonemeCount", 0)

    lines.append("# Phoneme fallback coverage")
    lines.append("")
    lines.append(f"* Generated: {generated}")
    lines.append(f"* Language profiles analysed: {profile_count}")
    lines.append(f"* Phonemes catalogued: {phoneme_count}")
    lines.append("")

    profiles: Sequence[Dict[str, object]] = data.get("profiles", [])  # type: ignore[assignment]
    if profiles:
        lines.append("## Profile coverage summary")
        lines.append("")
        lines.append("| Profile | Language | Characters | Complete | Partial | Missing |")
        lines.append("| --- | --- | ---: | ---: | ---: | ---: |")
        for profile in profiles:
            coverage = profile.get("coverage", {})
            lines.append(
                "| {display} | {language} | {total} | {complete} | {partial} | {missing} |".format(
                    display=profile.get("display", profile.get("id", "?")),
                    language=profile.get("language", "–") or "–",
                    total=profile.get("characterCount", 0),
                    complete=coverage.get("complete", 0),
                    partial=coverage.get("partial", 0),
                    missing=coverage.get("missing", 0),
                )
            )
        lines.append("")

    for profile in profiles:
        lines.append(f"### {profile.get('display', profile.get('id', 'Profile'))}")
        lines.append("")
        coverage = profile.get("coverage", {})
        lines.append(
            "* Characters analysed: {count} (complete {complete}, partial {partial}, missing {missing})".format(
                count=profile.get("characterCount", 0),
                complete=coverage.get("complete", 0),
                partial=coverage.get("partial", 0),
                missing=coverage.get("missing", 0),
            )
        )
        lines.append("")
        lines.append("| Symbol | IPA | Status | Matched phonemes | Unmatched |")
        lines.append("| --- | --- | --- | --- | --- |")
        for entry in profile.get("entries", []):
            ipa = " ".join(entry.get("ipa", [])) or "–"
            phonemes = ", ".join(entry.get("matchedPhonemes", [])) or "–"
            remainder = entry.get("unmatched", "") or "–"
            lines.append(
                f"| {entry.get('symbol')} | {ipa} | {entry.get('status')} | {phonemes} | {remainder} |"
            )
        lines.append("")

    phonemes: Iterable[Dict[str, object]] = data.get("phonemes", [])  # type: ignore[assignment]
    if phonemes:
        lines.append("## Phoneme replacement overview")
        lines.append("")
        lines.append("| Category | Phoneme | IPA | Replacement kinds | Replacement count |")
        lines.append("| --- | --- | --- | --- | ---: |")
        for entry in phonemes:
            ipa = " ".join(entry.get("ipa", [])) or "–"
            kinds = ", ".join(entry.get("replacementKinds", [])) or "–"
            lines.append(
                "| {category} | {name} | {ipa} | {kinds} | {count} |".format(
                    category=entry.get("category", "–"),
                    name=entry.get("name", "–"),
                    ipa=ipa,
                    kinds=kinds,
                    count=entry.get("replacementCount", 0),
                )
            )
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def _write_markdown(path: Path, data: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_render_markdown(data), encoding="utf-8")


def _emit_console(data: Dict[str, object]) -> None:
    metadata = data.get("metadata", {})
    print(
        "Profiles: {profiles}, phonemes: {phonemes}".format(
            profiles=metadata.get("profileCount", 0),
            phonemes=metadata.get("phonemeCount", 0),
        )
    )
    for profile in data.get("profiles", []):
        coverage = profile.get("coverage", {})
        print(
            "- {display}: complete {complete}, partial {partial}, missing {missing}".format(
                display=profile.get("display", profile.get("id", "profile")),
                complete=coverage.get("complete", 0),
                partial=coverage.get("partial", 0),
                missing=coverage.get("missing", 0),
            )
        )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Write JSON output to this path")
    parser.add_argument("--markdown", type=Path, help="Write Markdown output to this path")
    parser.add_argument("--print", action="store_true", help="Print a console summary")
    args = parser.parse_args(argv)

    data = _build_summary()
    if args.json:
        _write_json(args.json, data)
    if args.markdown:
        _write_markdown(args.markdown, data)
    if args.print:
        _emit_console(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
