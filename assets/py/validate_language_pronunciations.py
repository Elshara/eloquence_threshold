"""Validate language profile IPA coverage against the phoneme catalogue.

This helper inspects every bundled language profile and checks whether the IPA
sequences provided for each character map cleanly onto known phoneme
definitions. It surfaces gaps that appear when new datasets are merged so
contributors can keep pronunciation metadata in sync with the phoneme
inventory.
"""
from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, Iterable, List, Optional, Sequence

import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import language_profiles
import phoneme_catalog


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        dest="json_path",
        help="Write validation results to PATH as JSON",
    )
    parser.add_argument(
        "--markdown",
        dest="markdown_path",
        help="Write validation results to PATH as Markdown",
    )
    parser.add_argument(
        "--cwd",
        dest="working_directory",
        help="Change to this directory before loading catalogues",
    )
    args = parser.parse_args(argv)

    if args.working_directory:
        os.chdir(args.working_directory)

    inventory = phoneme_catalog.load_default_inventory()
    profiles = language_profiles.load_default_language_profiles()

    report = validate_profiles(inventory, profiles)

    if args.json_path:
        write_json(args.json_path, report)
    if args.markdown_path:
        write_markdown(args.markdown_path, report)

    if not args.json_path and not args.markdown_path:
        print(format_markdown(report))

    return 0 if not report.get("issues") else 1


def validate_profiles(
    inventory: phoneme_catalog.PhonemeInventory,
    profiles: language_profiles.LanguageProfileCatalog,
) -> Dict[str, Any]:
    profile_rows: List[Dict[str, Any]] = []
    global_issues: List[str] = []
    total_ipa = 0
    matched_ipa = 0

    for profile in profiles.profiles():
        summary, issues = _inspect_profile(profile, inventory)
        profile_rows.append(summary)
        global_issues.extend(issues)
        total_ipa += summary.get("ipaCount", 0)
        matched_ipa += summary.get("matchedCount", 0)

    report = {
        "profiles": profile_rows,
        "stats": {
            "profileCount": len(profile_rows),
            "ipaCount": total_ipa,
            "matchedCount": matched_ipa,
            "unmatchedCount": total_ipa - matched_ipa,
        },
    }
    if global_issues:
        report["issues"] = global_issues
    return report


def _inspect_profile(
    profile: language_profiles.LanguageProfile,
    inventory: phoneme_catalog.PhonemeInventory,
) -> Any:
    issues: List[str] = []
    entries: List[Dict[str, Any]] = []
    ipa_checked = 0
    ipa_matched = 0
    characters_with_ipa = 0

    for symbol, character in profile.characters.items():
        ipa_values = list(character.ipa)
        if ipa_values:
            characters_with_ipa += 1
        else:
            message = (
                f"Profile '{profile.id}' has no IPA data for symbol '{symbol}'"
            )
            issues.append(message)
            entries.append(
                {
                    "symbol": symbol,
                    "ipa": None,
                    "matches": [],
                    "issue": message,
                }
            )
            continue
        for ipa_value in ipa_values:
            ipa_checked += 1
            matches, remainder = inventory.match_ipa_sequence(ipa_value)
            match_names = [definition.name for definition in matches]
            entry: Dict[str, Any] = {
                "symbol": symbol,
                "ipa": ipa_value,
                "matches": match_names,
            }
            if matches and not remainder:
                ipa_matched += 1
            else:
                if not matches:
                    reason = (
                        f"IPA '{ipa_value}' for symbol '{symbol}' in profile '{profile.id}'"
                        " does not map to any known phoneme"
                    )
                else:
                    reason = (
                        f"IPA '{ipa_value}' for symbol '{symbol}' in profile '{profile.id}'"
                        f" leaves unmatched fragment '{remainder}'"
                    )
                entry["issue"] = reason
                issues.append(reason)
            entries.append(entry)

    summary = {
        "id": profile.id,
        "language": profile.language,
        "display": profile.display_label(),
        "characterCount": len(profile.characters),
        "charactersWithIpa": characters_with_ipa,
        "ipaCount": ipa_checked,
        "matchedCount": ipa_matched,
        "issues": issues,
        "entries": entries,
    }
    return summary, issues


def write_json(path: str, report: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_markdown(path: str, report: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(format_markdown(report))
        handle.write("\n")


def format_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    stats = report.get("stats", {})

    lines.append("# Language pronunciation validation")
    lines.append("")
    lines.append(f"* Profiles checked: {stats.get('profileCount', 0)}")
    lines.append(f"* IPA entries analysed: {stats.get('ipaCount', 0)}")
    lines.append(
        f"* Fully matched IPA entries: {stats.get('matchedCount', 0)}"
    )
    lines.append(
        f"* Unmatched or partial entries: {stats.get('unmatchedCount', 0)}"
    )
    lines.append("")

    for profile in report.get("profiles", []):
        lines.extend(_format_profile_markdown(profile))

    issues = report.get("issues", [])
    if issues:
        lines.append("## Aggregate issues")
        lines.append("")
        for issue in issues:
            lines.append(f"- {issue}")
        lines.append("")

    return "\n".join(lines).rstrip()


def _format_profile_markdown(profile: Dict[str, Any]) -> Iterable[str]:
    lines: List[str] = []
    lines.append(f"## {profile.get('display')}")
    lines.append("")
    lines.append(
        f"* Characters with IPA data: {profile.get('charactersWithIpa', 0)}"
        f" / {profile.get('characterCount', 0)}"
    )
    lines.append(f"* IPA entries: {profile.get('ipaCount', 0)}")
    lines.append(f"* Fully matched: {profile.get('matchedCount', 0)}")
    lines.append("")

    issue_entries = [
        entry
        for entry in profile.get("entries", [])
        if entry.get("issue")
    ]
    if not issue_entries:
        lines.append("No issues detected.")
        lines.append("")
        return lines

    lines.append("### Problematic entries")
    lines.append("")
    lines.append("| Symbol | IPA | Matched phonemes | Notes |")
    lines.append("| --- | --- | --- | --- |")
    for entry in issue_entries:
        symbol = entry.get("symbol")
        ipa_value = entry.get("ipa") or "—"
        matches = ", ".join(entry.get("matches", [])) or "—"
        note = entry.get("issue", "")
        lines.append(
            f"| `{symbol}` | `{ipa_value}` | {matches} | {note} |"
        )
    lines.append("")
    return lines


if __name__ == "__main__":
    raise SystemExit(main())
