"""Generate integration scope reports for bundled voices, languages, and phonemes.

This helper inspects the bundled catalogues so maintainers can understand how
Eloquence, eSpeak NG, DECtalk, and heritage voice packs intersect.  The output
highlights which languages ship with pronunciation profiles, how many voice
templates map to each locale, and the breadth of phoneme categories available
for NVDA's replacement picker.  Reports are emitted as JSON and/or Markdown so
automation pipelines can diff them alongside other dataset snapshots.
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from language_profiles import (
    LanguageProfile,
    LanguageProfileCatalog,
    load_default_language_profiles,
    normalize_language_tag,
)
from phoneme_catalog import PhonemeInventory, load_default_inventory
from voice_catalog import VoiceCatalog, load_default_voice_catalog


@dataclass
class VoiceLanguageSummary:
    language: str
    normalised: str
    template_ids: Tuple[str, ...]
    default_profile_templates: Tuple[str, ...]


def _collect_voice_language_summary(
    catalog: VoiceCatalog, profiles: LanguageProfileCatalog
) -> Tuple[Dict[str, VoiceLanguageSummary], List[str]]:
    summaries: Dict[str, VoiceLanguageSummary] = {}
    unmatched: List[str] = []
    all_profiles: List[LanguageProfile] = list(profiles)
    profile_by_language: Dict[str, List[LanguageProfile]] = collections.defaultdict(list)
    for profile in all_profiles:
        normalised = normalize_language_tag(profile.language)
        profile_by_language[normalised].append(profile)

    for template in catalog.templates():
        language = template.language or ""
        normalised = normalize_language_tag(language) if language else ""
        key = normalised or language or ""
        summary = summaries.get(key)
        if summary is None:
            summary = VoiceLanguageSummary(
                language=language,
                normalised=normalised,
                template_ids=(),
                default_profile_templates=(),
            )
            summaries[key] = summary
        summary.template_ids = tuple(sorted(set(summary.template_ids + (template.id,))))

        matched_profiles: Sequence[LanguageProfile] = ()
        if normalised:
            matched_profiles = profile_by_language.get(normalised, ())
            if not matched_profiles:
                base = normalised.split("-")[0]
                if base:
                    matched_profiles = tuple(
                        profile
                        for lang, bucket in profile_by_language.items()
                        if lang.split("-")[0] == base
                        for profile in bucket
                    )
        default_hits = set(summary.default_profile_templates)
        for profile in all_profiles:
            if template.id in profile.default_voice_templates:
                default_hits.add(profile.id)
        summary.default_profile_templates = tuple(sorted(default_hits))

        if not matched_profiles and not summary.default_profile_templates:
            unmatched.append(template.id)

    unmatched.sort()
    return summaries, unmatched


def _language_profile_stats(
    profiles: LanguageProfileCatalog, catalog: VoiceCatalog
) -> List[Dict[str, object]]:
    templates_by_id = {template.id: template for template in catalog.templates()}
    stats: List[Dict[str, object]] = []
    for profile in profiles:
        normalised = normalize_language_tag(profile.language)
        char_count = len(profile.characters)
        defaults = list(profile.default_voice_templates)
        linked_templates: List[str] = []
        if normalised:
            for template in catalog.templates():
                candidate = normalize_language_tag(template.language or "")
                if candidate and (candidate == normalised or candidate.split("-")[0] == normalised.split("-")[0]):
                    linked_templates.append(template.id)
        linked_templates.extend(defaults)
        unique_templates = sorted(set(linked_templates))
        template_details = [
            templates_by_id[template_id].display_label()
            for template_id in unique_templates
            if template_id in templates_by_id
        ]
        stats.append(
            {
                "id": profile.id,
                "language": profile.language,
                "normalisedLanguage": normalised,
                "displayName": profile.display_name,
                "characterCount": char_count,
                "defaultVoiceTemplates": defaults,
                "linkedVoiceTemplates": unique_templates,
                "linkedVoiceLabels": template_details,
                "tags": list(profile.tags),
                "stressNotes": list(profile.stress_notes),
                "sentenceStructure": list(profile.sentence_structure),
                "grammarNotes": list(profile.grammar_notes),
            }
        )
    stats.sort(key=lambda item: (item["normalisedLanguage"], item["displayName"]))
    return stats


def _voice_tag_counts(catalog: VoiceCatalog) -> Dict[str, int]:
    counts: Dict[str, int] = collections.Counter()
    for template in catalog.templates():
        for tag in template.tags:
            counts[tag] += 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def _phoneme_category_stats(inventory: PhonemeInventory) -> List[Dict[str, object]]:
    stats: List[Dict[str, object]] = []
    if inventory.is_empty:
        return stats
    for category_id, label in inventory.categories.items():
        phonemes = inventory.phonemes_for_category(category_id)
        ipa_symbols: set[str] = set()
        for definition in phonemes:
            ipa_symbols.update(symbol for symbol in definition.ipa if symbol)
        stats.append(
            {
                "id": category_id,
                "label": label,
                "phonemeCount": len(phonemes),
                "ipaCount": len(ipa_symbols),
                "ipaSymbols": sorted(ipa_symbols),
            }
        )
    stats.sort(key=lambda item: (-item["phonemeCount"], item["label"]))
    return stats


def _aggregate_report() -> Dict[str, object]:
    voice_catalog = load_default_voice_catalog()
    language_profiles = load_default_language_profiles()
    phoneme_inventory = load_default_inventory()

    language_summaries, unmatched_templates = _collect_voice_language_summary(
        voice_catalog, language_profiles
    )
    language_profile_stats = _language_profile_stats(language_profiles, voice_catalog)
    phoneme_categories = _phoneme_category_stats(phoneme_inventory)

    voice_language_entries = [
        {
            "language": summary.language,
            "normalised": summary.normalised,
            "templateIds": list(summary.template_ids),
            "defaultProfileTemplates": list(summary.default_profile_templates),
        }
        for summary in sorted(
            language_summaries.values(),
            key=lambda item: (
                -(len(item.template_ids)),
                item.normalised or item.language,
            ),
        )
    ]

    voice_tags = _voice_tag_counts(voice_catalog)
    total_templates = sum(len(entry["templateIds"]) for entry in voice_language_entries)

    phoneme_total = sum(item["phonemeCount"] for item in phoneme_categories)
    all_ipa_symbols = {
        symbol
        for entry in phoneme_categories
        for symbol in entry.get("ipaSymbols", [])
        if symbol
    }
    distinct_ipa = len(all_ipa_symbols)

    report = {
        "summary": {
            "voices": {
                "totalTemplates": total_templates,
                "languagesWithTemplates": len(voice_language_entries),
                "tagCounts": voice_tags,
                "unmatchedTemplates": unmatched_templates,
                "parameterRanges": {
                    name: {
                        "label": rng.label,
                        "minimum": rng.minimum,
                        "maximum": rng.maximum,
                        "default": rng.default,
                        "step": rng.step,
                        "tags": list(rng.tags),
                    }
                    for name, rng in voice_catalog.parameter_ranges().items()
                },
            },
            "languageProfiles": {
                "total": len(language_profile_stats),
                "withCharacters": sum(1 for item in language_profile_stats if item["characterCount"]),
            },
            "phonemes": {
                "categories": len(phoneme_categories),
                "total": phoneme_total,
                "distinctIPA": distinct_ipa,
                "empty": phoneme_inventory.is_empty,
            },
        },
        "voices": voice_language_entries,
        "languageProfiles": language_profile_stats,
        "phonemeCategories": phoneme_categories,
        "distinctIPASymbols": sorted(all_ipa_symbols),
    }
    return report


def _write_json(path: str, data: Dict[str, object]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def _format_voice_tag_table(tag_counts: Dict[str, int]) -> str:
    if not tag_counts:
        return "No voice tags discovered."
    lines = ["| Tag | Templates |", "| --- | ---: |"]
    for tag, count in tag_counts.items():
        lines.append(f"| `{tag}` | {count} |")
    return "\n".join(lines)


def _format_voice_language_table(entries: Iterable[Dict[str, object]]) -> str:
    lines = [
        "| Language | Normalised | Templates | Default profile references |",
        "| --- | --- | ---: | --- |",
    ]
    for entry in entries:
        language = entry.get("language") or "—"
        normalised = entry.get("normalised") or "—"
        templates = entry.get("templateIds") or []
        defaults = entry.get("defaultProfileTemplates") or []
        template_list = "<br>".join(f"`{template}`" for template in templates) or "—"
        default_list = "<br>".join(f"`{item}`" for item in defaults) or "—"
        lines.append(f"| {language} | {normalised} | {len(templates)} | {default_list} |")
        if templates:
            lines.append(f"| ↳ Templates |  |  | {template_list} |")
    return "\n".join(lines)


def _format_language_profile_table(entries: Iterable[Dict[str, object]]) -> str:
    lines = [
        "| Profile | Language | Characters | Linked templates | Tags |",
        "| --- | --- | ---: | --- | --- |",
    ]
    for entry in entries:
        templates = entry.get("linkedVoiceTemplates") or []
        template_list = "<br>".join(f"`{template}`" for template in templates) or "—"
        tags = entry.get("tags") or []
        tag_list = ", ".join(f"`{tag}`" for tag in tags) or "—"
        lines.append(
            "| {id} ({display}) | {lang} | {chars} | {templates} | {tags} |".format(
                id=entry.get("id"),
                display=entry.get("displayName") or "",
                lang=entry.get("normalisedLanguage") or "—",
                chars=entry.get("characterCount") or 0,
                templates=template_list,
                tags=tag_list,
            )
        )
    return "\n".join(lines)


def _format_phoneme_table(entries: Iterable[Dict[str, object]]) -> str:
    lines = ["| Category | Phonemes | Distinct IPA |", "| --- | ---: | ---: |"]
    for entry in entries:
        lines.append(
            f"| {entry.get('label')} | {entry.get('phonemeCount', 0)} | {entry.get('ipaCount', 0)} |"
        )
    return "\n".join(lines)


def _write_markdown(path: str, data: Dict[str, object]) -> None:
    summary = data.get("summary", {})
    voices = summary.get("voices", {})
    language_profiles = summary.get("languageProfiles", {})
    phonemes = summary.get("phonemes", {})

    lines = [
        "# Integration scope report",
        "",
        "This report captures the current intersection between bundled voices, language",
        "profiles, and phoneme inventories so Eloquence Reloaded contributors can spot",
        "gaps before publishing a new NVDA add-on build.",
        "",
        "## Quick stats",
        "",
        f"- **Voice templates**: {voices.get('totalTemplates', 0)} across {voices.get('languagesWithTemplates', 0)} languages.",
        f"- **Language profiles**: {language_profiles.get('total', 0)} total, {language_profiles.get('withCharacters', 0)} with character coverage.",
        f"- **Phonemes**: {phonemes.get('total', 0)} entries spanning {phonemes.get('categories', 0)} categories and {phonemes.get('distinctIPA', 0)} distinct IPA symbols.",
        "",
        "## Voice templates by language",
        "",
        _format_voice_language_table(data.get("voices", ())),
        "",
        "## Voice tag distribution",
        "",
        _format_voice_tag_table(voices.get("tagCounts", {})),
        "",
        "## Language profiles",
        "",
        _format_language_profile_table(data.get("languageProfiles", ())),
        "",
        "## Phoneme categories",
        "",
        _format_phoneme_table(data.get("phonemeCategories", ())),
    ]

    unmatched = voices.get("unmatchedTemplates", [])
    if unmatched:
        lines.extend(
            [
                "",
                "## Voice templates without a matching language profile",
                "",
                "The following templates do not currently map to a bundled language profile.",
                "Contributors can create new profiles or extend existing ones so NVDA users",
                "receive contextual hints while experimenting with these presets.",
                "",
                "\n".join(f"- `{template_id}`" for template_id in unmatched),
            ]
        )

    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines).strip() + "\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", dest="json_path", help="Write JSON report to the specified path")
    parser.add_argument(
        "--markdown",
        dest="markdown_path",
        help="Write Markdown report to the specified path",
    )
    parser.add_argument(
        "--print",
        dest="print_report",
        action="store_true",
        help="Print the quick stats summary to stdout",
    )
    args = parser.parse_args(argv)

    report = _aggregate_report()

    if args.json_path:
        _write_json(args.json_path, report)
    if args.markdown_path:
        _write_markdown(args.markdown_path, report)

    if args.print_report or (not args.json_path and not args.markdown_path):
        summary = report.get("summary", {})
        voices = summary.get("voices", {})
        profiles = summary.get("languageProfiles", {})
        phonemes = summary.get("phonemes", {})
        print(
            "Voice templates: {templates} across {languages} languages\n"
            "Language profiles: {profiles} total ({profiles_with_chars} with character data)\n"
            "Phoneme entries: {phoneme_total} across {phoneme_categories} categories".format(
                templates=voices.get("totalTemplates", 0),
                languages=voices.get("languagesWithTemplates", 0),
                profiles=profiles.get("total", 0),
                profiles_with_chars=profiles.get("withCharacters", 0),
                phoneme_total=phonemes.get("total", 0),
                phoneme_categories=phonemes.get("categories", 0),
            )
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

