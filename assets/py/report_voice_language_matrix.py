"""Correlate voice templates with language profiles for coverage analysis."""
from __future__ import annotations

import argparse
import datetime as _dt
import json
from collections import OrderedDict, defaultdict
from pathlib import Path
import sys
from typing import Dict, Iterable, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from voice_catalog import VoiceTemplate, load_default_voice_catalog
from language_profiles import (
    LanguageProfile,
    load_default_language_profiles,
    normalize_language_tag,
)


def _language_key(language: Optional[str]) -> Tuple[str, Optional[str]]:
    """Return a stable key and normalised tag for *language*."""

    normalised = normalize_language_tag(language or "")
    if normalised:
        return normalised, normalised
    return "unspecified", None


def _timestamp() -> str:
    return (
        _dt.datetime.now(_dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _collect_templates(templates: Iterable[VoiceTemplate]) -> Tuple[
    Dict[str, VoiceTemplate],
    Dict[str, Dict[str, object]],
    Dict[str, List[str]],
    List[Dict[str, str]],
]:
    template_index: Dict[str, VoiceTemplate] = {}
    language_map: Dict[str, Dict[str, object]] = {}
    missing_default_profiles: List[Dict[str, str]] = []
    template_defaults: Dict[str, List[str]] = defaultdict(list)

    for template in templates:
        template_index[template.id] = template
        key, tag = _language_key(template.language)
        entry = language_map.setdefault(
            key,
            {
                "key": key,
                "languageTag": tag,
                "languageNames": set(),
                "templateIds": [],
                "profileIds": [],
                "templateTags": set(),
                "profileTags": set(),
                "pairings": [],
                "templateDefaultProfiles": set(),
                "profileDefaultTemplates": set(),
            },
        )
        if template.language:
            entry["languageNames"].add(template.language)
        entry["templateIds"].append(template.id)
        for tag_name in template.tags:
            entry["templateTags"].add(tag_name)
        if template.default_language_profile:
            entry["templateDefaultProfiles"].add(template.default_language_profile)
            template_defaults[template.default_language_profile].append(template.id)

    return template_index, language_map, template_defaults, missing_default_profiles


def _collect_profiles(
    profiles: Iterable[LanguageProfile],
    language_map: Dict[str, Dict[str, object]],
    template_index: Dict[str, VoiceTemplate],
) -> Tuple[Dict[str, LanguageProfile], List[Dict[str, str]], List[Dict[str, str]]]:
    profile_index: Dict[str, LanguageProfile] = {}
    missing_default_templates: List[Dict[str, str]] = []
    profiles_without_language: List[Dict[str, str]] = []

    for profile in profiles:
        profile_index[profile.id] = profile
        key, tag = _language_key(profile.language)
        entry = language_map.setdefault(
            key,
            {
                "key": key,
                "languageTag": tag,
                "languageNames": set(),
                "templateIds": [],
                "profileIds": [],
                "templateTags": set(),
                "profileTags": set(),
                "pairings": [],
                "templateDefaultProfiles": set(),
                "profileDefaultTemplates": set(),
            },
        )
        if profile.language:
            entry["languageNames"].add(profile.language)
        else:
            profiles_without_language.append({"profileId": profile.id})
        entry["profileIds"].append(profile.id)
        for tag_name in profile.tags:
            entry["profileTags"].add(tag_name)
        for template_id in profile.default_voice_templates:
            entry["profileDefaultTemplates"].add(template_id)
            if template_id not in template_index:
                missing_default_templates.append(
                    {"profileId": profile.id, "templateId": template_id}
                )
    return profile_index, missing_default_templates, profiles_without_language


def _build_summary() -> Dict[str, object]:
    voice_catalog = load_default_voice_catalog()
    language_catalog = load_default_language_profiles()

    template_index, language_map, template_defaults, _ = _collect_templates(voice_catalog)
    profile_index, missing_default_templates, profiles_without_language = _collect_profiles(
        language_catalog,
        language_map,
        template_index,
    )

    missing_default_profiles: List[Dict[str, str]] = []
    for profile_id, template_ids in template_defaults.items():
        if profile_id not in profile_index:
            for template_id in template_ids:
                missing_default_profiles.append(
                    {"templateId": template_id, "profileId": profile_id}
                )
        else:
            entry_key, _tag = _language_key(profile_index[profile_id].language)
            language_entry = language_map.setdefault(
                entry_key,
                {
                    "key": entry_key,
                    "languageTag": _tag,
                    "languageNames": set(),
                    "templateIds": [],
                    "profileIds": [],
                    "templateTags": set(),
                    "profileTags": set(),
                    "pairings": [],
                    "templateDefaultProfiles": set(),
                    "profileDefaultTemplates": set(),
                },
            )
            for template_id in template_ids:
                if template_id in template_index:
                    language_entry["pairings"].append(
                        {"templateId": template_id, "profileId": profile_id}
                    )

    languages: List[Dict[str, object]] = []
    for key, entry in language_map.items():
        language_names = sorted(entry["languageNames"]) if entry["languageNames"] else []
        templates = sorted(entry["templateIds"])
        profiles = sorted(entry["profileIds"])
        template_tags = sorted(entry["templateTags"])
        profile_tags = sorted(entry["profileTags"])
        pairings = sorted(
            entry["pairings"],
            key=lambda item: (item["templateId"], item["profileId"]),
        )
        languages.append(
            {
                "key": key,
                "languageTag": entry["languageTag"],
                "languageNames": language_names,
                "templateIds": templates,
                "profileIds": profiles,
                "templateCount": len(templates),
                "profileCount": len(profiles),
                "templateTags": template_tags,
                "profileTags": profile_tags,
                "templateDefaultProfiles": sorted(entry["templateDefaultProfiles"]),
                "profileDefaultTemplates": sorted(entry["profileDefaultTemplates"]),
                "pairings": pairings,
            }
        )

    languages.sort(key=lambda item: (-item["templateCount"], -item["profileCount"], item["key"]))

    templates_payload = [
        {
            "id": template.id,
            "name": template.name,
            "language": template.language,
            "defaultLanguageProfile": template.default_language_profile,
            "tags": list(template.tags),
        }
        for template in voice_catalog
    ]
    profiles_payload = [
        {
            "id": profile.id,
            "language": profile.language,
            "displayName": profile.display_name,
            "defaultVoiceTemplates": list(profile.default_voice_templates),
            "tags": list(profile.tags),
        }
        for profile in language_catalog
    ]

    metadata: Dict[str, object] = {
        "generated": _timestamp(),
        "templateCount": len(templates_payload),
        "profileCount": len(profiles_payload),
        "languageCount": len(languages),
    }
    if voice_catalog.metadata:
        metadata["voiceCatalog"] = voice_catalog.metadata

    return {
        "metadata": metadata,
        "languages": languages,
        "templates": templates_payload,
        "profiles": profiles_payload,
        "issues": {
            "missingDefaultProfiles": missing_default_profiles,
            "missingDefaultTemplates": missing_default_templates,
            "profilesWithoutLanguage": profiles_without_language,
        },
    }


def _write_json(path: Path, data: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _render_markdown(data: Dict[str, object]) -> str:
    lines: List[str] = []
    metadata = data.get("metadata", {})
    generated = metadata.get("generated", "")
    template_count = metadata.get("templateCount", 0)
    profile_count = metadata.get("profileCount", 0)
    language_count = metadata.get("languageCount", 0)

    lines.append("# Voice and language linkage")
    lines.append("")
    lines.append(f"* Generated: {generated}")
    lines.append(f"* Templates analysed: {template_count}")
    lines.append(f"* Language profiles analysed: {profile_count}")
    lines.append(f"* Languages observed: {language_count}")
    lines.append("")

    lines.append("## Language matrix")
    lines.append("")
    lines.append(
        "| Language tag | Names | Templates | Profiles | Template tags | Profile tags | Default pairings |"
    )
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for entry in data.get("languages", []):  # type: ignore[assignment]
        language_tag = entry.get("languageTag") or "–"
        names = ", ".join(entry.get("languageNames", [])) or "–"
        template_ids = ", ".join(entry.get("templateIds", [])) or "–"
        profile_ids = ", ".join(entry.get("profileIds", [])) or "–"
        template_tags = ", ".join(entry.get("templateTags", [])) or "–"
        profile_tags = ", ".join(entry.get("profileTags", [])) or "–"
        pairings = entry.get("pairings", [])
        if pairings:
            pairing_text = ", ".join(
                f"{item['templateId']} → {item['profileId']}" for item in pairings
            )
        else:
            pairing_text = "–"
        lines.append(
            f"| {language_tag} | {names} | {template_ids} | {profile_ids} | {template_tags} | {profile_tags} | {pairing_text} |"
        )
    lines.append("")

    issues = data.get("issues", {})
    missing_profiles = issues.get("missingDefaultProfiles", [])
    missing_templates = issues.get("missingDefaultTemplates", [])
    profiles_without_language = issues.get("profilesWithoutLanguage", [])

    if missing_profiles:
        lines.append("## Templates referencing missing language profiles")
        lines.append("")
        lines.append("| Template | Requested profile |")
        lines.append("| --- | --- |")
        for item in missing_profiles:
            lines.append(f"| {item['templateId']} | {item['profileId']} |")
        lines.append("")

    if missing_templates:
        lines.append("## Language profiles referencing missing templates")
        lines.append("")
        lines.append("| Profile | Requested template |")
        lines.append("| --- | --- |")
        for item in missing_templates:
            lines.append(f"| {item['profileId']} | {item['templateId']} |")
        lines.append("")

    if profiles_without_language:
        lines.append("## Profiles without language tags")
        lines.append("")
        lines.append("| Profile |")
        lines.append("| --- |")
        for item in profiles_without_language:
            lines.append(f"| {item['profileId']} |")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def _write_markdown(path: Path, data: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_render_markdown(data), encoding="utf-8")


def _emit_console(data: Dict[str, object]) -> None:
    metadata = data.get("metadata", {})
    template_count = metadata.get("templateCount", 0)
    profile_count = metadata.get("profileCount", 0)
    language_count = metadata.get("languageCount", 0)
    print(
        f"Templates: {template_count} | Language profiles: {profile_count} | Languages: {language_count}"
    )
    languages = data.get("languages", [])
    for entry in languages[:10]:
        tag = entry.get("languageTag") or entry.get("key")
        template_total = entry.get("templateCount", 0)
        profile_total = entry.get("profileCount", 0)
        print(f"- {tag}: {template_total} templates, {profile_total} profiles")
    issues = data.get("issues", {})
    missing_profiles = issues.get("missingDefaultProfiles", [])
    missing_templates = issues.get("missingDefaultTemplates", [])
    if missing_profiles:
        print(f"! {len(missing_profiles)} templates reference missing language profiles")
    if missing_templates:
        print(f"! {len(missing_templates)} profiles reference missing templates")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Write JSON summary to this path")
    parser.add_argument(
        "--markdown", type=Path, help="Write Markdown summary to this path"
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print a brief summary to standard output",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    data = _build_summary()
    if args.json:
        _write_json(args.json, data)
    if args.markdown:
        _write_markdown(args.markdown, data)
    if args.print:
        _emit_console(data)
    if args.json or args.markdown or args.print:
        return 0
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
