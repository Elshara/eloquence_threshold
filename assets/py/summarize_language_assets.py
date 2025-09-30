"""Aggregate language assets across progress, coverage, and voice catalogues."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, Iterable, List, MutableMapping, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
import sys

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from language_profiles import normalize_language_tag  # noqa: E402


@dataclass
class LanguageAggregate:
    """In-memory aggregator for a single language tag."""

    language_tag: str
    labels: set[str] = field(default_factory=set)
    sources: set[str] = field(default_factory=set)
    progress: Optional[MutableMapping[str, object]] = None
    coverage_entries: List[MutableMapping[str, object]] = field(default_factory=list)
    voice_templates: Optional[MutableMapping[str, object]] = None

    def to_json(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "languageTag": self.language_tag,
            "labels": sorted(self.labels),
            "sources": sorted(self.sources),
        }
        if self.progress is not None:
            payload["progress"] = self.progress
        if self.coverage_entries:
            payload["coverage"] = sorted(
                self.coverage_entries,
                key=lambda item: (
                    item.get("status", "zzzz"),
                    item.get("profileName", ""),
                ),
            )
        if self.voice_templates is not None:
            payload["voiceTemplates"] = self.voice_templates
        return payload


def _normalise_tag(tag: Optional[str]) -> Optional[str]:
    if not tag:
        return None
    try:
        return normalize_language_tag(tag)
    except Exception:  # pragma: no cover - defensive path for malformed tags
        return tag.lower().replace("_", "-")


def load_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_language_aggregates() -> Dict[str, LanguageAggregate]:
    aggregates: Dict[str, LanguageAggregate] = {}

    def ensure(tag: Optional[str]) -> Optional[LanguageAggregate]:
        normalised = _normalise_tag(tag)
        if not normalised:
            return None
        aggregate = aggregates.get(normalised)
        if aggregate is None:
            aggregate = LanguageAggregate(language_tag=normalised)
            aggregates[normalised] = aggregate
        return aggregate

    progress_path = REPO_ROOT / "docs" / "language_progress.json"
    if progress_path.exists():
        progress_payload = load_json(progress_path)
        for entry in progress_payload.get("entries", []):
            tag = entry.get("language") or entry.get("id")
            aggregate = ensure(tag)
            if aggregate is None:
                continue
            aggregate.sources.add("language_progress")
            display_name = entry.get("displayName") or entry.get("id")
            if display_name:
                aggregate.labels.add(str(display_name))
            aggregate.progress = {
                "stage": entry.get("stage"),
                "ipaCoveragePercent": float(entry.get("ipaCoveragePercent", 0.0)),
                "progressScore": float(entry.get("progressScore", 0.0)),
                "defaultVoiceTemplates": sorted(entry.get("defaultVoiceTemplates", [])),
                "availableTemplateCount": int(entry.get("availableTemplateCount", 0)),
                "hasGenerativeHints": bool(entry.get("hasGenerativeHints")),
                "hasContextualHints": bool(entry.get("hasContextualHints")),
            }

    coverage_path = REPO_ROOT / "docs" / "language_coverage.json"
    coverage_status_counts: Counter[str] = Counter()
    if coverage_path.exists():
        coverage_payload = load_json(coverage_path)
        for entry in coverage_payload.get("entries", []):
            tag = entry.get("normalisedTag") or entry.get("languageTag")
            aggregate = ensure(tag)
            if aggregate is None:
                continue
            aggregate.sources.add("language_coverage")
            for label in (entry.get("profileName"), entry.get("languageTag")):
                if label:
                    aggregate.labels.add(str(label))
            status = str(entry.get("status") or "unknown").lower()
            coverage_status_counts[status] += 1
            aggregate.coverage_entries.append(
                {
                    "profileId": entry.get("profileId"),
                    "profileName": entry.get("profileName"),
                    "status": status,
                    "ipaCoverage": float(entry.get("ipaCoverage", 0.0)),
                    "templateCount": int(entry.get("templateCount", 0)),
                    "defaultTemplateIds": sorted(entry.get("defaultTemplateIds", [])),
                }
            )

    matrix_path = REPO_ROOT / "docs" / "voice_language_matrix.json"
    template_totals = {
        "languages": 0,
        "pairings": 0,
        "templates": 0,
    }
    if matrix_path.exists():
        matrix_payload = load_json(matrix_path)
        for language_entry in matrix_payload.get("languages", []):
            tag = language_entry.get("languageTag") or language_entry.get("key")
            aggregate = ensure(tag)
            if aggregate is None:
                continue
            aggregate.sources.add("voice_language_matrix")
            for label in language_entry.get("languageNames", []):
                aggregate.labels.add(str(label))
            aggregate.voice_templates = {
                "profileCount": int(language_entry.get("profileCount", 0)),
                "profileIds": sorted(language_entry.get("profileIds", [])),
                "templateCount": int(language_entry.get("templateCount", 0)),
                "templateIds": sorted(language_entry.get("templateIds", [])),
                "profileDefaultTemplates": sorted(
                    language_entry.get("profileDefaultTemplates", [])
                ),
                "templateDefaultProfiles": sorted(
                    language_entry.get("templateDefaultProfiles", [])
                ),
            }
            template_totals["languages"] += 1
            template_totals["pairings"] += len(language_entry.get("pairings", []))
            template_totals["templates"] += int(language_entry.get("templateCount", 0))

    research_path = REPO_ROOT / "docs" / "language_research_index.json"
    research_classifications: Counter[str] = Counter()
    research_source_total = 0
    research_updated: Optional[str] = None
    if research_path.exists():
        research_payload = load_json(research_path)
        research_updated = str(research_payload.get("updated") or "") or None
        for source in research_payload.get("sources", []):
            research_source_total += 1
            for cls in source.get("classification", []) or []:
                research_classifications[str(cls).lower()] += 1

    generated_at = datetime.now(UTC).isoformat()

    global_stats: Dict[str, object] = {
        "generatedAt": generated_at,
        "languageCount": len(aggregates),
        "languagesWithProgress": sum(1 for agg in aggregates.values() if agg.progress),
        "languagesWithCoverage": sum(
            1 for agg in aggregates.values() if agg.coverage_entries
        ),
        "languagesWithVoiceTemplates": sum(
            1 for agg in aggregates.values() if agg.voice_templates
        ),
        "coverageStatusCounts": dict(coverage_status_counts),
        "voiceTemplateTotals": template_totals,
    }

    global_research: Dict[str, object] = {
        "sourceCount": research_source_total,
        "classificationCounts": dict(research_classifications),
    }
    if research_updated:
        global_research["updated"] = research_updated

    return aggregates, global_stats, global_research, generated_at


def render_markdown(
    aggregates: Dict[str, LanguageAggregate],
    global_stats: Dict[str, object],
    global_research: Dict[str, object],
    generated_at: str,
) -> str:
    lines: List[str] = []
    lines.append("# Language asset summary")
    lines.append("")
    lines.append(f"- Generated: {generated_at}")
    lines.append(f"- Languages analysed: {global_stats.get('languageCount', 0)}")
    lines.append(
        "- Languages with voice templates: "
        f"{global_stats.get('languagesWithVoiceTemplates', 0)}"
    )
    lines.append(
        "- Languages with coverage data: "
        f"{global_stats.get('languagesWithCoverage', 0)}"
    )
    lines.append(
        "- Languages with detailed progress: "
        f"{global_stats.get('languagesWithProgress', 0)}"
    )
    lines.append(
        "- Research sources indexed: "
        f"{global_research.get('sourceCount', 0)}"
    )
    lines.append("")

    coverage_counts = global_stats.get("coverageStatusCounts", {})
    if coverage_counts:
        lines.append("## Coverage status overview")
        lines.append("")
        lines.append("| Status | Entries |")
        lines.append("| --- | ---: |")
        for status, count in sorted(coverage_counts.items()):
            lines.append(f"| {status} | {int(count)} |")
        lines.append("")

    lines.append("## Language breakdown")
    lines.append("")
    lines.append(
        "| Language | Labels | Stage | IPA % | Coverage statuses | Voice templates |"
    )
    lines.append("| --- | --- | --- | ---: | --- | --- |")

    for tag in sorted(aggregates.keys()):
        aggregate = aggregates[tag]
        stage = "—"
        ipa_percent = "—"
        if aggregate.progress:
            stage = str(aggregate.progress.get("stage") or "—").replace("-", " ").title()
            ipa_percent = f"{aggregate.progress.get('ipaCoveragePercent', 0.0):.1f}"
        coverage_statuses = ", ".join(
            sorted({entry.get("status", "unknown") for entry in aggregate.coverage_entries})
        ) or "—"
        template_summary = "—"
        if aggregate.voice_templates:
            template_summary = (
                f"{aggregate.voice_templates.get('templateCount', 0)} templates / "
                f"{aggregate.voice_templates.get('profileCount', 0)} profiles"
            )
        lines.append(
            "| {lang} | {labels} | {stage} | {ipa} | {coverage} | {templates} |".format(
                lang=tag,
                labels=", ".join(aggregate.to_json()["labels"]) or "—",
                stage=stage,
                ipa=ipa_percent,
                coverage=coverage_statuses,
                templates=template_summary,
            )
        )

    if global_research:
        lines.append("")
        lines.append("## Research classifications")
        lines.append("")
        if global_research.get("updated"):
            lines.append(f"- Last updated: {global_research['updated']}")
        classification_counts = global_research.get("classificationCounts", {})
        if classification_counts:
            lines.append("- Classification counts:")
            for name, count in sorted(classification_counts.items()):
                lines.append(f"  - {name}: {int(count)}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def write_json(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


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
        help="Print a short console summary",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    aggregates, global_stats, global_research, generated_at = build_language_aggregates()

    payload = {
        "generatedAt": generated_at,
        "globalStats": global_stats,
        "globalResearch": global_research,
        "languages": [agg.to_json() for agg in aggregates.values()],
    }

    if args.json:
        write_json(args.json, payload)
    if args.markdown:
        write_markdown(args.markdown, render_markdown(aggregates, global_stats, global_research, generated_at))
    if args.print_console:
        summary = (
            f"Analysed {global_stats.get('languageCount', 0)} languages; "
            f"{global_stats.get('languagesWithVoiceTemplates', 0)} have voice templates; "
            f"{global_stats.get('languagesWithCoverage', 0)} include coverage snapshots."
        )
        print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
