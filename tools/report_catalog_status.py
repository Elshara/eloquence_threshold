"""Summarise bundled voice, phoneme, and language assets.

This helper inspects the catalogues that ship with Eloquence Threshold and
emits a machine-readable summary.  The report helps contributors verify that
voice templates, language profiles, and phoneme inventories reference one
another correctly so NVDA's voice dialog exposes coherent data.
"""
from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

import pathlib
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import language_profiles
import phoneme_catalog
import voice_catalog


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        dest="json_path",
        help="Write the summary to PATH as JSON",
    )
    parser.add_argument(
        "--markdown",
        dest="markdown_path",
        help="Write a Markdown digest to PATH",
    )
    parser.add_argument(
        "--cwd",
        dest="working_directory",
        default=None,
        help="Change to this directory before loading catalogues",
    )
    args = parser.parse_args(argv)

    if args.working_directory:
        os.chdir(args.working_directory)

    summary = build_summary()

    if args.json_path:
        write_json(args.json_path, summary)
    if args.markdown_path:
        write_markdown(args.markdown_path, summary)

    if not args.json_path and not args.markdown_path:
        print(format_markdown(summary))

    issues = summary.get("issues", [])
    return 0 if not issues else 1


def build_summary() -> Dict[str, Any]:
    phonemes = phoneme_catalog.load_default_inventory()
    voices = voice_catalog.load_default_voice_catalog()
    languages = language_profiles.load_default_language_profiles()

    language_index = {profile.id: profile for profile in languages.profiles()}

    templates_by_profile: Dict[str, Set[str]] = {}
    voice_entries: List[Dict[str, Any]] = []
    voice_issues: List[str] = []

    for template in voices.templates():
        issues: List[str] = []
        default_profile = template.default_language_profile or None
        if default_profile and default_profile not in language_index:
            issues.append(
                f"Default language profile '{default_profile}' is missing"
            )
        locale = template.language or ""
        matched_profile_id: Optional[str] = None
        if locale:
            matched = languages.find_best_match(locale)
            if matched is None:
                issues.append(f"Locale '{locale}' has no matching language profile")
            else:
                matched_profile_id = matched.id
        if default_profile:
            templates_by_profile.setdefault(default_profile, set()).add(template.id)
        if matched_profile_id:
            templates_by_profile.setdefault(matched_profile_id, set()).add(template.id)
        entry = {
            "id": template.id,
            "name": template.name,
            "language": locale,
            "defaultLanguageProfile": default_profile,
            "issues": issues,
        }
        voice_entries.append(entry)
        voice_issues.extend(issues)

    language_entries: List[Dict[str, Any]] = []
    language_issues: List[str] = []
    for profile in languages.profiles():
        defaults = list(profile.default_voice_templates)
        missing = [template_id for template_id in defaults if voices.get(template_id) is None]
        referenced = sorted(templates_by_profile.get(profile.id, set()))
        entry = {
            "id": profile.id,
            "language": profile.language,
            "display": profile.display_label(),
            "characterCount": len(profile.characters),
            "defaultVoiceTemplates": defaults,
            "referencedBy": referenced,
            "missingDefaults": missing,
        }
        language_entries.append(entry)
        for missing_template in missing:
            language_issues.append(
                f"Language profile '{profile.id}' references missing voice template '{missing_template}'"
            )

    category_entries: List[Dict[str, Any]] = []
    total_phonemes = 0
    for category_id, label in phonemes.categories.items():
        members = phonemes.phonemes_for_category(category_id)
        count = len(members)
        total_phonemes += count
        category_entries.append(
            {
                "id": category_id,
                "label": label,
                "count": count,
            }
        )

    summary = {
        "phonemes": {
            "total": total_phonemes,
            "categories": category_entries,
        },
        "voices": {
            "total": len(voice_entries),
            "templates": sorted(voice_entries, key=lambda item: item["id"]),
        },
        "languages": {
            "total": len(language_entries),
            "profiles": sorted(language_entries, key=lambda item: item["id"]),
        },
    }

    issues = voice_issues + language_issues
    if issues:
        summary["issues"] = issues
    return summary


def write_json(path: str, summary: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_markdown(path: str, summary: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(format_markdown(summary))
        handle.write("\n")


def format_markdown(summary: Dict[str, Any]) -> str:
    lines: List[str] = []
    phoneme_summary = summary.get("phonemes", {})
    voice_summary = summary.get("voices", {})
    language_summary = summary.get("languages", {})

    lines.append("# Catalog status report")
    lines.append("")
    lines.append(
        f"* Phoneme entries: {phoneme_summary.get('total', 0)}"
    )
    lines.append(
        f"* Voice templates: {voice_summary.get('total', 0)}"
    )
    lines.append(
        f"* Language profiles: {language_summary.get('total', 0)}"
    )
    lines.append("")

    category_rows = phoneme_summary.get("categories", [])
    if category_rows:
        lines.append("## Phoneme categories")
        lines.append("")
        lines.append("| Category | Entries |")
        lines.append("| --- | ---: |")
        for category in category_rows:
            lines.append(
                f"| {category.get('label', category.get('id'))} | {category.get('count', 0)} |"
            )
        lines.append("")

    language_rows = language_summary.get("profiles", [])
    if language_rows:
        lines.append("## Language profiles")
        lines.append("")
        lines.append("| Profile | Locale | Characters | Default templates | Referenced by | Notes |")
        lines.append("| --- | --- | ---: | --- | --- | --- |")
        for entry in language_rows:
            defaults = ", ".join(entry.get("defaultVoiceTemplates", [])) or "–"
            referenced = ", ".join(entry.get("referencedBy", [])) or "–"
            missing = entry.get("missingDefaults", [])
            notes = ", ".join(
                f"Missing template {template_id}" for template_id in missing
            ) or ""
            lines.append(
                "| {display} | {language} | {count} | {defaults} | {referenced} | {notes} |".format(
                    display=entry.get("display", entry.get("id")),
                    language=entry.get("language", ""),
                    count=entry.get("characterCount", 0),
                    defaults=defaults,
                    referenced=referenced,
                    notes=notes or "–",
                )
            )
        lines.append("")

    voice_rows = voice_summary.get("templates", [])
    if voice_rows:
        lines.append("## Voice templates")
        lines.append("")
        lines.append("| Template | Locale | Default profile | Issues |")
        lines.append("| --- | --- | --- | --- |")
        for entry in voice_rows:
            issues = ", ".join(entry.get("issues", [])) or "–"
            lines.append(
                "| {id} ({name}) | {language} | {profile} | {issues} |".format(
                    id=entry.get("id"),
                    name=entry.get("name"),
                    language=entry.get("language", ""),
                    profile=entry.get("defaultLanguageProfile") or "–",
                    issues=issues,
                )
            )
        lines.append("")

    issues = summary.get("issues", [])
    if issues:
        lines.append("## Issues")
        lines.append("")
        for item in issues:
            lines.append(f"- {item}")
        lines.append("")

    return "\n".join(lines).rstrip()


if __name__ == "__main__":
    raise SystemExit(main())
