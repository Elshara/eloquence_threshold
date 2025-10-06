"""Generate a maturity report for bundled language profiles.

This helper inspects the language profiles, the phoneme inventory, and the
voice catalogue to score each locale.  The resulting JSON/Markdown artefacts
are designed for automation and documentation so we can track how quickly new
locales gain IPA coverage, structural notes, and keyboard-friendly digraph
support.
"""
from __future__ import annotations

import argparse
import json
from collections import OrderedDict
from datetime import UTC, datetime
from pathlib import Path
import sys
from typing import Dict, Iterable, List

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from language_profiles import (  # noqa: E402
    LanguageProfileCatalog,
    load_default_language_profiles,
    normalize_language_tag,
)
from phoneme_catalog import load_default_inventory  # noqa: E402
from voice_catalog import load_default_voice_catalog  # noqa: E402


def build_summary(sort_key: str) -> Dict[str, object]:
    catalog = load_default_language_profiles()
    inventory = load_default_inventory()
    voice_catalog = load_default_voice_catalog()

    summary = catalog.metrics(inventory, voice_catalog)
    entries = list(summary.get("entries", []))

    if sort_key == "name":
        entries.sort(key=lambda item: item.get("displayName", "").lower())
    elif sort_key == "language":
        entries.sort(
            key=lambda item: (
                normalize_language_tag(str(item.get("language", ""))).lower(),
                item.get("displayName", "").lower(),
            )
        )
    else:
        entries.sort(
            key=lambda item: (
                -float(item.get("progressScore", 0.0)),
                item.get("displayName", "").lower(),
            )
        )

    summary.update(
        {
            "generatedAt": datetime.now(UTC).isoformat(),
            "entries": entries,
            "sortKey": sort_key,
        }
    )
    return summary


def render_markdown(summary: Dict[str, object]) -> str:
    lines: List[str] = []
    generated = summary.get("generatedAt")
    stats = summary.get("stats", {})
    stage_counts: Dict[str, int] = dict(stats.get("stageCounts", {}))

    lines.append("# Language profile progress")
    lines.append("")
    lines.append(f"- Generated: {generated}")
    lines.append(f"- Sort key: {summary.get('sortKey')}")
    lines.append(
        f"- Profiles analysed: {stats.get('totalProfiles', len(summary.get('entries', [])))}"
    )
    lines.append(
        f"- Average IPA coverage: {round(stats.get('averageIpaCoverage', 0.0) * 100, 1)}%"
    )
    lines.append(
        f"- Median IPA coverage: {round(stats.get('medianIpaCoverage', 0.0) * 100, 1)}%"
    )
    if stage_counts:
        ordered = OrderedDict(sorted(stage_counts.items()))
        parts = [f"{key}: {value}" for key, value in ordered.items()]
        lines.append(f"- Stage distribution: {', '.join(parts)}")
    lines.append("")

    lines.append("## Coverage overview")
    lines.append("")
    lines.append(
        "| Profile | Language | Stage | IPA % | Characters | Examples | Templates | Missing defaults | Structural notes |"
    )
    lines.append("| --- | --- | --- | ---: | ---: | ---: | --- | --- | ---: |")

    for entry in summary.get("entries", []):
        missing_defaults = entry.get("missingDefaultTemplates") or []
        matched_defaults = entry.get("matchedDefaultTemplates") or []
        stage = str(entry.get("stage", "")).title()
        structural_notes = (
            int(entry.get("stressNoteCount", 0))
            + int(entry.get("sentenceStructureNoteCount", 0))
            + int(entry.get("grammarNoteCount", 0))
        )
        lines.append(
            "| {name} | {language} | {stage} | {ipa:.1f}% | {chars} | {examples} | {templates} | {missing} | {notes} |".format(
                name=entry.get("displayName", entry.get("id", "?")),
                language=entry.get("language") or "—",
                stage=stage or "—",
                ipa=float(entry.get("ipaCoveragePercent", 0.0)),
                chars=int(entry.get("characterCount", 0)),
                examples=int(entry.get("exampleCount", 0)),
                templates=", ".join(matched_defaults) or "—",
                missing=", ".join(missing_defaults) or "—",
                notes=structural_notes,
            )
        )

    lines.append("")
    lines.append("## Profile details")

    for entry in summary.get("entries", []):
        heading = entry.get("displayName") or entry.get("id") or "Unknown profile"
        language = entry.get("language") or "—"
        lines.append("")
        lines.append(f"### {heading} ({language})")
        lines.append("")
        lines.append(
            f"- Stage: {str(entry.get('stage', 'unknown')).replace('-', ' ').title()}"
        )
        lines.append(
            f"- IPA coverage: {float(entry.get('ipaCoveragePercent', 0.0)):.1f}% ({int(entry.get('ipaCoveredCount', 0))}/{int(entry.get('charactersWithIPA', 0))} characters with IPA)"
        )
        lines.append(
            f"- Examples documented: {int(entry.get('exampleCount', 0))}"
        )
        lines.append(
            f"- Notes recorded: {int(entry.get('notesTotal', 0))} (stress {int(entry.get('stressNoteCount', 0))}, sentence {int(entry.get('sentenceStructureNoteCount', 0))}, grammar {int(entry.get('grammarNoteCount', 0))})"
        )
        lines.append(
            f"- Generative hints: {'yes' if entry.get('hasGenerativeHints') else 'no'}, contextual hints: {'yes' if entry.get('hasContextualHints') else 'no'}"
        )
        lines.append(
            f"- Keyboard digraph coverage: {'yes' if entry.get('keyboardOptimised') else 'no'}"
        )
        lines.append(
            f"- Available templates: {int(entry.get('availableTemplateCount', 0))}"
        )
        lines.append(
            f"- Default templates bundled: {', '.join(entry.get('defaultVoiceTemplates', [])) or '—'}"
        )
        missing_ipa = entry.get("charactersWithoutIPA") or []
        unmatched = entry.get("charactersWithUnmatchedIPA") or []
        if missing_ipa:
            lines.append(
                f"- Characters without IPA coverage: {', '.join(missing_ipa)}"
            )
        if unmatched:
            lines.append(
                f"- Characters with partial IPA matches: {', '.join(unmatched)}"
            )

    return "\n".join(lines).strip() + "\n"


def write_json(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Write JSON output to this path")
    parser.add_argument(
        "--markdown",
        type=Path,
        help="Write Markdown output to this path",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        dest="print_console",
        help="Print a short summary to stdout",
    )
    parser.add_argument(
        "--sort",
        choices=["coverage", "name", "language"],
        default="coverage",
        help="Sort order for the output entries",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    options = parse_args(argv)
    summary = build_summary(options.sort)

    if options.json:
        write_json(options.json, summary)
    if options.markdown:
        write_markdown(options.markdown, render_markdown(summary))
    if options.print_console:
        stats = summary.get("stats", {})
        print(
            "{profiles} profiles, avg {avg:.1f}% IPA, median {med:.1f}%".format(
                profiles=stats.get("totalProfiles", len(summary.get("entries", []))),
                avg=float(stats.get("averageIpaCoverage", 0.0)) * 100,
                med=float(stats.get("medianIpaCoverage", 0.0)) * 100,
            )
        )
        top = summary.get("entries", [])[:5]
        for entry in top:
            print(
                " - {name}: {stage} at {ipa:.1f}%".format(
                    name=entry.get("displayName", entry.get("id", "unknown")),
                    stage=str(entry.get("stage", "")).replace("-", " ").title(),
                    ipa=float(entry.get("ipaCoveragePercent", 0.0)),
                )
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
