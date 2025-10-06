"""Report Eloquence language maturity across progress, coverage, and voice templates."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, Iterable, List, MutableMapping, Optional
import sys

MODULE_DIR = Path(__file__).resolve().parent
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from summarize_language_assets import (  # noqa: E402
    LanguageAggregate,
    build_language_aggregates,
)


def _normalise_stage(stage: Optional[str]) -> Optional[str]:
    if not stage:
        return None
    return str(stage).strip().lower() or None


def _format_stage(stage: Optional[str]) -> str:
    if not stage:
        return "—"
    return stage.replace("-", " ").title()


def _collect_language_entry(tag: str, aggregate: LanguageAggregate) -> Dict[str, object]:
    stage_value: Optional[str] = None
    ipa_percent: Optional[float] = None
    has_progress = aggregate.progress is not None
    if has_progress:
        stage_value = _normalise_stage(aggregate.progress.get("stage"))
        ipa_percent = aggregate.progress.get("ipaCoveragePercent")

    has_coverage = bool(aggregate.coverage_entries)
    coverage_statuses = sorted(
        {str(entry.get("status") or "unknown").lower() for entry in aggregate.coverage_entries}
    )

    voice_templates = aggregate.voice_templates or {}
    template_count = int(voice_templates.get("templateCount", 0))
    profile_count = int(voice_templates.get("profileCount", 0))
    has_voice_templates = template_count > 0 or bool(voice_templates)

    return {
        "languageTag": tag,
        "labels": sorted(aggregate.labels),
        "stage": stage_value,
        "stageDisplay": _format_stage(stage_value),
        "ipaCoveragePercent": ipa_percent,
        "hasProgress": has_progress,
        "hasCoverage": has_coverage,
        "coverageStatuses": coverage_statuses,
        "hasVoiceTemplates": has_voice_templates,
        "voiceTemplateCount": template_count,
        "profileCount": profile_count,
        "sources": sorted(aggregate.sources),
    }


def build_maturity_report() -> Dict[str, object]:
    aggregates, _, _, _ = build_language_aggregates()
    generated_at = datetime.now(UTC).isoformat()

    stage_counts: Counter[str] = Counter()
    coverage_status_counts: Counter[str] = Counter()

    missing_progress: List[str] = []
    missing_coverage: List[str] = []
    missing_voice_templates: List[str] = []
    full_stack: List[str] = []

    entries: List[Dict[str, object]] = []

    for tag in sorted(aggregates.keys()):
        aggregate = aggregates[tag]
        entry = _collect_language_entry(tag, aggregate)
        entries.append(entry)

        stage_value = entry["stage"]
        if stage_value:
            stage_counts[str(stage_value)] += 1
        else:
            missing_progress.append(tag)

        if entry["hasCoverage"]:
            for status in entry["coverageStatuses"]:
                coverage_status_counts[str(status)] += 1
        else:
            missing_coverage.append(tag)

        if entry["hasVoiceTemplates"]:
            pass
        else:
            missing_voice_templates.append(tag)

        if entry["hasProgress"] and entry["hasCoverage"] and entry["hasVoiceTemplates"]:
            full_stack.append(tag)

    full_stack.sort()
    missing_progress.sort()
    missing_coverage.sort()
    missing_voice_templates.sort()

    payload: Dict[str, object] = {
        "generatedAt": generated_at,
        "languageCount": len(entries),
        "stageCounts": dict(stage_counts),
        "coverageStatusCounts": dict(coverage_status_counts),
        "languagesWithFullStack": full_stack,
        "languagesMissingProgress": missing_progress,
        "languagesMissingCoverage": missing_coverage,
        "languagesMissingVoiceTemplates": missing_voice_templates,
        "entries": entries,
    }
    return payload


def render_markdown(payload: Dict[str, object]) -> str:
    lines: List[str] = []
    lines.append("# Language maturity overview")
    lines.append("")
    lines.append(f"- Generated: {payload['generatedAt']}")
    lines.append(f"- Languages analysed: {payload['languageCount']}")
    lines.append(
        "- Languages with full asset stack: "
        f"{len(payload.get('languagesWithFullStack', []))}"
    )
    lines.append("")

    stage_counts: MutableMapping[str, int] = payload.get("stageCounts", {})  # type: ignore[assignment]
    if stage_counts:
        lines.append("## Progress stage distribution")
        lines.append("")
        lines.append("| Stage | Languages |")
        lines.append("| --- | ---: |")
        for stage, count in sorted(stage_counts.items()):
            lines.append(f"| {_format_stage(stage)} | {int(count)} |")
        lines.append("")

    coverage_counts: MutableMapping[str, int] = payload.get("coverageStatusCounts", {})  # type: ignore[assignment]
    if coverage_counts:
        lines.append("## Coverage status distribution")
        lines.append("")
        lines.append("| Status | Languages |")
        lines.append("| --- | ---: |")
        for status, count in sorted(coverage_counts.items()):
            lines.append(f"| {status} | {int(count)} |")
        lines.append("")

    def _render_gap(title: str, values: List[str]) -> None:
        if not values:
            return
        lines.append(f"### {title}")
        lines.append("")
        for tag in values:
            lines.append(f"- `{tag}`")
        lines.append("")

    _render_gap("Languages missing detailed progress entries", payload.get("languagesMissingProgress", []))
    _render_gap("Languages missing coverage snapshots", payload.get("languagesMissingCoverage", []))
    _render_gap(
        "Languages missing voice template pairings",
        payload.get("languagesMissingVoiceTemplates", []),
    )

    lines.append("## Language detail")
    lines.append("")
    lines.append("| Language | Labels | Stage | IPA % | Coverage statuses | Voice templates | Sources |")
    lines.append("| --- | --- | --- | ---: | --- | --- | --- |")

    for entry in payload.get("entries", []):
        ipa_percent = entry.get("ipaCoveragePercent")
        ipa_display = "—"
        if isinstance(ipa_percent, (int, float)):
            ipa_display = f"{float(ipa_percent):.1f}"
        coverage_display = ", ".join(entry.get("coverageStatuses", []) or ["—"])
        template_display = "—"
        if entry.get("hasVoiceTemplates"):
            template_display = (
                f"{entry.get('voiceTemplateCount', 0)} templates / "
                f"{entry.get('profileCount', 0)} profiles"
            )
        lines.append(
            "| {tag} | {labels} | {stage} | {ipa} | {coverage} | {templates} | {sources} |".format(
                tag=entry.get("languageTag", "?"),
                labels=", ".join(entry.get("labels", [])) or "—",
                stage=entry.get("stageDisplay", "—"),
                ipa=ipa_display,
                coverage=coverage_display,
                templates=template_display,
                sources=", ".join(entry.get("sources", [])) or "—",
            )
        )

    lines.append("")
    return "\n".join(lines)


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Write JSON output to this path")
    parser.add_argument("--markdown", type=Path, help="Write Markdown output to this path")
    parser.add_argument(
        "--print",
        action="store_true",
        dest="print_console",
        help="Print a short console summary",
    )
    return parser.parse_args(argv)


def write_json(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    payload = build_maturity_report()
    if args.json:
        write_json(args.json, payload)
    if args.markdown:
        write_markdown(args.markdown, render_markdown(payload))
    if args.print_console:
        stage_counts = payload.get("stageCounts", {})
        summary = (
            f"Analysed {payload.get('languageCount', 0)} languages; "
            f"{len(payload.get('languagesWithFullStack', []))} full-stack locales; "
            f"stage distribution: "
            + ", ".join(
                f"{_format_stage(stage)}={count}" for stage, count in sorted(stage_counts.items())
            )
        )
        print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
