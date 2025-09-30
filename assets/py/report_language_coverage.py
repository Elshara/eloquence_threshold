"""Summarise language coverage across voice templates, profiles, and phonemes.

This helper inspects the bundled language profiles, voice templates, and
phoneme inventory to produce a consolidated report that highlights how mature
each locale is.  The JSON output is designed for automation (CodeQL, CI), while
the Markdown snapshot gives contributors a human-friendly digest they can scan
before adding new datasets or packaging releases.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, OrderedDict, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
import sys
from typing import Dict, Iterable, List, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from language_profiles import (
    LanguageProfile,
    LanguageProfileCatalog,
    load_default_language_profiles,
    normalize_language_tag,
)
from phoneme_catalog import PhonemeInventory, load_default_inventory
from voice_catalog import VoiceCatalog, VoiceTemplate, load_default_voice_catalog


@dataclass
class CoverageEntry:
    """Structured representation of one locale within the coverage report."""

    language_tag: str
    normalised_tag: str
    profile: Optional[LanguageProfile]
    templates: Sequence[VoiceTemplate]
    default_template_ids: Sequence[str]
    matched_phonemes: Sequence[str]
    ipa_sample_total: int
    ipa_samples_with_match: int
    ipa_samples_full_match: int
    unmatched_samples: Sequence[Dict[str, str]]

    @property
    def status(self) -> str:
        has_profile = self.profile is not None
        has_templates = bool(self.templates)
        if has_profile and has_templates:
            return "profile+templates"
        if has_profile:
            return "profile-only"
        if has_templates:
            return "template-only"
        return "uncovered"

    @property
    def status_label(self) -> str:
        return {
            "profile+templates": "Profile + templates",
            "profile-only": "Profile only",
            "template-only": "Templates only",
            "uncovered": "Uncovered",
        }[self.status]

    @property
    def template_count(self) -> int:
        return len(self.templates)

    @property
    def character_count(self) -> int:
        if not self.profile:
            return 0
        return len(self.profile.characters)

    @property
    def multi_character_count(self) -> int:
        if not self.profile:
            return 0
        return sum(1 for symbol in self.profile.characters if len(symbol) > 1)

    @property
    def ipa_coverage_ratio(self) -> Optional[float]:
        if not self.ipa_sample_total:
            return None
        return self.ipa_samples_full_match / self.ipa_sample_total

    @property
    def ipa_any_match_ratio(self) -> Optional[float]:
        if not self.ipa_sample_total:
            return None
        return self.ipa_samples_with_match / self.ipa_sample_total


def _collect_templates_by_language(voice_catalog: VoiceCatalog) -> Dict[str, List[VoiceTemplate]]:
    mapping: Dict[str, List[VoiceTemplate]] = defaultdict(list)
    for template in voice_catalog.templates():
        tag = normalize_language_tag(template.language or "")
        mapping[tag].append(template)
    return mapping


def _collect_templates_by_profile(voice_catalog: VoiceCatalog) -> Dict[str, List[VoiceTemplate]]:
    mapping: Dict[str, List[VoiceTemplate]] = defaultdict(list)
    for template in voice_catalog.templates():
        profile_id = template.default_language_profile
        if profile_id:
            mapping[profile_id].append(template)
    return mapping


def _resolve_templates(
    template_ids: Iterable[str],
    template_lookup: Dict[str, VoiceTemplate],
) -> List[VoiceTemplate]:
    resolved: List[VoiceTemplate] = []
    seen: set[str] = set()
    for template_id in template_ids:
        if template_id in seen:
            continue
        seen.add(template_id)
        template = template_lookup.get(template_id)
        if template is not None:
            resolved.append(template)
    return resolved


def _profile_templates(
    profile: LanguageProfile,
    templates_by_language: Dict[str, List[VoiceTemplate]],
    templates_by_profile: Dict[str, List[VoiceTemplate]],
    template_lookup: Dict[str, VoiceTemplate],
) -> List[VoiceTemplate]:
    linked: List[VoiceTemplate] = []
    normalised = normalize_language_tag(profile.language)
    linked.extend(templates_by_language.get(normalised, ()))
    linked.extend(templates_by_profile.get(profile.id, ()))
    linked.extend(_resolve_templates(profile.default_voice_templates, template_lookup))
    ordered: OrderedDict[str, VoiceTemplate] = OrderedDict()
    for template in linked:
        if template.id not in ordered:
            ordered[template.id] = template
    return list(ordered.values())


def _analyse_profile_phonemes(
    profile: LanguageProfile,
    inventory: PhonemeInventory,
) -> tuple[Sequence[str], int, int, int, Sequence[Dict[str, str]]]:
    matched_names: OrderedDict[str, None] = OrderedDict()
    unmatched: List[Dict[str, str]] = []
    total_samples = 0
    samples_with_match = 0
    samples_full_match = 0
    for character in profile.characters.values():
        for ipa_value in character.ipa:
            ipa_value = ipa_value.strip()
            if not ipa_value:
                continue
            total_samples += 1
            definitions, remainder = inventory.match_ipa_sequence(ipa_value)
            if definitions:
                samples_with_match += 1
                for definition in definitions:
                    matched_names.setdefault(definition.name, None)
            if definitions and not remainder:
                samples_full_match += 1
            if remainder:
                unmatched.append(
                    {
                        "symbol": character.symbol,
                        "ipa": ipa_value,
                        "unmatched": remainder,
                    }
                )
    return list(matched_names.keys()), total_samples, samples_with_match, samples_full_match, unmatched


def build_coverage_entries(
    profile_catalog: LanguageProfileCatalog,
    voice_catalog: VoiceCatalog,
    inventory: PhonemeInventory,
) -> List[CoverageEntry]:
    template_lookup = {template.id: template for template in voice_catalog.templates()}
    templates_by_language = _collect_templates_by_language(voice_catalog)
    templates_by_profile = _collect_templates_by_profile(voice_catalog)

    entries: List[CoverageEntry] = []
    seen_keys: set[str] = set()

    for profile in profile_catalog:
        normalised = normalize_language_tag(profile.language)
        key = normalised or f"profile:{profile.id}"
        seen_keys.add(key)
        templates = _profile_templates(profile, templates_by_language, templates_by_profile, template_lookup)
        matched_phonemes, sample_total, sample_with_match, sample_full_match, unmatched = _analyse_profile_phonemes(
            profile, inventory
        )
        entries.append(
            CoverageEntry(
                language_tag=profile.language,
                normalised_tag=normalised,
                profile=profile,
                templates=templates,
                default_template_ids=profile.default_voice_templates,
                matched_phonemes=matched_phonemes,
                ipa_sample_total=sample_total,
                ipa_samples_with_match=sample_with_match,
                ipa_samples_full_match=sample_full_match,
                unmatched_samples=unmatched[:10],
            )
        )

    for normalised_tag, templates in templates_by_language.items():
        key = normalised_tag or ""
        if key and key in seen_keys:
            continue
        if not key and not templates:
            continue
        entries.append(
            CoverageEntry(
                language_tag=normalised_tag,
                normalised_tag=normalised_tag,
                profile=None,
                templates=templates,
                default_template_ids=(),
                matched_phonemes=(),
                ipa_sample_total=0,
                ipa_samples_with_match=0,
                ipa_samples_full_match=0,
                unmatched_samples=(),
            )
        )

    entries.sort(key=lambda entry: (entry.normalised_tag or "", entry.profile.id if entry.profile else ""))
    return entries


def _format_percentage(value: Optional[float]) -> str:
    if value is None:
        return "—"
    return f"{value * 100:.0f}%"


def _summarise_templates(templates: Sequence[VoiceTemplate]) -> str:
    if not templates:
        return "None"
    names = [template.id for template in templates]
    if len(names) <= 3:
        return ", ".join(names)
    preview = ", ".join(names[:3])
    return f"{preview}, … ({len(names)} total)"


def _render_markdown(report: Dict[str, object], entries: Sequence[CoverageEntry]) -> str:
    lines: List[str] = []
    lines.append("# Language coverage report")
    lines.append("")
    lines.append(f"Generated at: {report['generatedAt']}")
    lines.append(f"Phoneme inventory size: {report['phonemeInventorySize']}")
    lines.append(f"Total locales tracked: {report['totalEntries']}")
    lines.append("")
    lines.append("## Status overview")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("| --- | --- |")
    for status, count in report["statusCounts"].items():
        lines.append(f"| {status} | {count} |")
    lines.append("")
    lines.append("## Locale summary")
    lines.append("")
    lines.append("| Locale | Profile | Characters | Templates | IPA coverage | Status |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for entry in entries:
        locale = entry.language_tag or entry.normalised_tag or "(unspecified)"
        if entry.profile:
            profile_label = f"{entry.profile.display_label()} (`{entry.profile.id}`)"
        else:
            profile_label = "—"
        characters = str(entry.character_count)
        templates = _summarise_templates(entry.templates)
        ipa = _format_percentage(entry.ipa_coverage_ratio)
        lines.append(
            f"| {locale} | {profile_label} | {characters} | {templates} | {ipa} | {entry.status_label} |"
        )
    lines.append("")
    lines.append("## Locale details")
    for entry in entries:
        locale = entry.language_tag or entry.normalised_tag or "(unspecified)"
        lines.append("")
        header = locale
        if entry.profile:
            header = f"{entry.profile.display_label()} ({locale or 'unspecified'})"
        lines.append(f"### {header}")
        lines.append("")
        lines.append(f"- Status: **{entry.status_label}**")
        if entry.profile:
            lines.append(f"- Characters documented: {entry.character_count} (multi-character: {entry.multi_character_count})")
            if entry.profile.tags:
                lines.append(f"- Profile tags: {', '.join(entry.profile.tags)}")
        if entry.templates:
            template_list = ", ".join(template.id for template in entry.templates)
            lines.append(f"- Templates: {template_list}")
        else:
            lines.append("- Templates: none bundled yet")
        if entry.default_template_ids:
            lines.append(f"- Default templates: {', '.join(entry.default_template_ids)}")
        ipa_ratio = _format_percentage(entry.ipa_coverage_ratio)
        any_ratio = _format_percentage(entry.ipa_any_match_ratio)
        lines.append(
            f"- IPA samples with matches: {entry.ipa_samples_with_match}/{entry.ipa_sample_total} ({any_ratio}); "
            f"complete matches: {entry.ipa_samples_full_match}/{entry.ipa_sample_total} ({ipa_ratio})"
        )
        if entry.matched_phonemes:
            preview = ", ".join(entry.matched_phonemes[:10])
            if len(entry.matched_phonemes) > 10:
                preview += ", …"
            lines.append(f"- Matched phonemes: {preview}")
        if entry.unmatched_samples:
            lines.append("- Unmatched IPA samples:")
            for sample in entry.unmatched_samples:
                lines.append(
                    f"  - `{sample['symbol']}` with IPA `{sample['ipa']}` left remainder `{sample['unmatched']}`"
                )
        else:
            lines.append("- Unmatched IPA samples: none")
    lines.append("")
    return "\n".join(lines)


def _inventory_size(inventory: PhonemeInventory) -> int:
    seen: set[str] = set()
    try:
        categories = inventory.categories  # type: ignore[attr-defined]
    except AttributeError:
        return 0
    for category_id in categories.keys():
        try:
            phonemes = inventory.phonemes_for_category(category_id)
        except AttributeError:
            continue
        for definition in phonemes:
            seen.add(getattr(definition, "name", ""))
    return len(seen)


def _build_report(entries: Sequence[CoverageEntry], inventory: PhonemeInventory) -> Dict[str, object]:
    status_counter = Counter(entry.status_label for entry in entries)
    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "generatedAt": timestamp,
        "phonemeInventorySize": _inventory_size(inventory),
        "totalEntries": len(entries),
        "statusCounts": OrderedDict((status, status_counter.get(status, 0)) for status in [
            "Profile + templates",
            "Profile only",
            "Templates only",
            "Uncovered",
        ]),
        "entries": [
            {
                "languageTag": entry.language_tag,
                "normalisedTag": entry.normalised_tag,
                "status": entry.status_label,
                "characterCount": entry.character_count,
                "multiCharacterCount": entry.multi_character_count,
                "templateCount": entry.template_count,
                "templateIds": [template.id for template in entry.templates],
                "defaultTemplateIds": list(entry.default_template_ids),
                "profileId": entry.profile.id if entry.profile else None,
                "profileName": entry.profile.display_label() if entry.profile else None,
                "profileTags": list(entry.profile.tags) if entry.profile else [],
                "ipaSampleTotal": entry.ipa_sample_total,
                "ipaSamplesWithMatch": entry.ipa_samples_with_match,
                "ipaSamplesFullMatch": entry.ipa_samples_full_match,
                "ipaCoverage": entry.ipa_coverage_ratio,
                "ipaAnyMatchRatio": entry.ipa_any_match_ratio,
                "matchedPhonemes": list(entry.matched_phonemes),
                "unmatchedSamples": list(entry.unmatched_samples),
            }
            for entry in entries
        ],
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", dest="json_path", help="Write the JSON report to this path")
    parser.add_argument("--markdown", dest="markdown_path", help="Write the Markdown report to this path")
    parser.add_argument("--print", dest="print_summary", action="store_true", help="Print a short summary to stdout")
    args = parser.parse_args(argv)

    profile_catalog = load_default_language_profiles()
    voice_catalog = load_default_voice_catalog()
    inventory = load_default_inventory()

    entries = build_coverage_entries(profile_catalog, voice_catalog, inventory)
    report = _build_report(entries, inventory)

    if args.json_path:
        with open(args.json_path, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2, sort_keys=True)
            handle.write("\n")

    if args.markdown_path:
        markdown = _render_markdown(report, entries)
        with open(args.markdown_path, "w", encoding="utf-8") as handle:
            handle.write(markdown)

    if args.print_summary:
        print(f"Locales tracked: {report['totalEntries']}")
        for status, count in report["statusCounts"].items():
            print(f"  {status}: {count}")

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
