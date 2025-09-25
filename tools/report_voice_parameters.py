"""Summarise voice parameter coverage across the bundled catalogue."""
from __future__ import annotations

import argparse
import datetime as _dt
import json
from collections import Counter, defaultdict, OrderedDict
from pathlib import Path
import os
import sys
from typing import Dict, Iterable, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from voice_catalog import load_default_voice_catalog


def _build_summary() -> Dict[str, object]:
    catalog = load_default_voice_catalog()
    timestamp = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    parameter_ranges = {
        name: {
            "label": rng.label,
            "minimum": rng.minimum,
            "maximum": rng.maximum,
            "default": rng.default,
            "step": rng.step,
            "description": rng.description,
            "tags": list(rng.tags),
        }
        for name, rng in catalog.parameter_ranges().items()
    }

    templates = [
        {
            "id": template.id,
            "name": template.name,
            "language": template.language,
            "defaultLanguageProfile": template.default_language_profile,
            "tags": list(template.tags),
            "parameters": OrderedDict(template.parameters),
            "extras": template.extras,
        }
        for template in catalog
    ]

    language_index: Dict[str, Dict[str, object]] = defaultdict(lambda: {
        "templates": [],
        "tags": Counter(),
    })
    parameter_usage: Dict[str, List[str]] = defaultdict(list)

    for template in catalog:
        language = template.language or "unspecified"
        entry = language_index[language]
        entry["templates"].append(template.id)
        for tag in template.tags:
            entry["tags"][tag] += 1
        for name in template.parameters:
            parameter_usage[name].append(template.id)

    language_summary = OrderedDict()
    for language in sorted(language_index):
        entry = language_index[language]
        language_summary[language] = {
            "count": len(entry["templates"]),
            "templates": sorted(entry["templates"]),
            "tags": sorted({tag for tag, count in entry["tags"].items() if count}),
        }

    parameter_summary = OrderedDict()
    for name in sorted(parameter_ranges):
        usage = parameter_usage.get(name, [])
        parameter_summary[name] = {
            "templates": sorted(set(usage)),
            "templateCount": len(set(usage)),
        }

    metadata = {
        "generated": timestamp,
        "templateCount": len(templates),
        "languageCount": len(language_summary),
    }
    if catalog.metadata:
        metadata["catalog"] = catalog.metadata

    return {
        "metadata": metadata,
        "parameterRanges": parameter_ranges,
        "parameterUsage": parameter_summary,
        "languages": language_summary,
        "templates": templates,
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
    language_count = metadata.get("languageCount", 0)

    lines.append("# Voice parameter coverage")
    lines.append("")
    lines.append(f"* Generated: {generated}")
    lines.append(f"* Templates analysed: {template_count}")
    lines.append(f"* Languages represented: {language_count}")
    lines.append("")

    lines.append("## Parameter ranges")
    lines.append("")
    lines.append("| Parameter | Range | Default | Step | Tags | Description |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    parameter_ranges: Dict[str, Dict[str, object]] = data.get("parameterRanges", {})  # type: ignore[assignment]
    for name in sorted(parameter_ranges):
        entry = parameter_ranges[name]
        minimum = entry.get("minimum", "?")
        maximum = entry.get("maximum", "?")
        default = entry.get("default", "?")
        step = entry.get("step", "?")
        tags = ", ".join(entry.get("tags", [])) or "–"
        description = entry.get("description", "") or "–"
        lines.append(
            f"| {name} | {minimum} – {maximum} | {default} | {step} | {tags} | {description} |"
        )
    lines.append("")

    lines.append("## Parameter usage")
    lines.append("")
    lines.append("| Parameter | Templates using it | Count |")
    lines.append("| --- | --- | ---: |")
    parameter_usage: Dict[str, Dict[str, object]] = data.get("parameterUsage", {})  # type: ignore[assignment]
    for name in sorted(parameter_usage):
        entry = parameter_usage[name]
        templates = entry.get("templates", [])
        count = entry.get("templateCount", 0)
        template_list = ", ".join(templates) if templates else "–"
        lines.append(f"| {name} | {template_list} | {count} |")
    lines.append("")

    lines.append("## Language coverage")
    lines.append("")
    lines.append("| Language | Templates | Count | Tags |")
    lines.append("| --- | --- | ---: | --- |")
    languages: Dict[str, Dict[str, object]] = data.get("languages", {})  # type: ignore[assignment]
    for language in languages:
        entry = languages[language]
        templates = entry.get("templates", [])
        count = entry.get("count", 0)
        tags = ", ".join(entry.get("tags", [])) or "–"
        template_list = ", ".join(templates) if templates else "–"
        lines.append(f"| {language} | {template_list} | {count} | {tags} |")
    lines.append("")

    lines.append("## Templates")
    lines.append("")
    for template in data.get("templates", []):  # type: ignore[assignment]
        template_id = template.get("id")
        name = template.get("name", template_id)
        language = template.get("language") or "unspecified"
        profile = template.get("defaultLanguageProfile") or "–"
        tags = ", ".join(template.get("tags", [])) or "–"
        lines.append(f"### {template_id} – {name}")
        lines.append("")
        lines.append(f"* Language: {language}")
        lines.append(f"* Default language profile: {profile}")
        lines.append(f"* Tags: {tags}")
        parameters = template.get("parameters", {})
        if parameters:
            lines.append("* Parameters:")
            for param, value in parameters.items():
                lines.append(f"  * {param}: {value}")
        extras = template.get("extras") or {}
        if extras:
            lines.append("* Extras:")
            for key in sorted(extras):
                lines.append(f"  * {key}: {extras[key]}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def _write_markdown(path: Path, data: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = _render_markdown(data)
    path.write_text(content, encoding="utf-8")


def _emit_console(data: Dict[str, object]) -> None:
    parameter_count = len(data.get("parameterRanges", {}))
    template_count = len(data.get("templates", []))
    language_count = len(data.get("languages", {}))
    print(f"Voice parameter coverage: {parameter_count} parameters, {template_count} templates, {language_count} languages")

    print("\nTop parameters by template coverage:")
    usage = data.get("parameterUsage", {})
    ranked = sorted(
        (
            (name, entry.get("templateCount", 0))
            for name, entry in usage.items()
        ),
        key=lambda item: (-item[1], item[0]),
    )
    for name, count in ranked:
        print(f"  {name}: {count}")


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Path to write JSON summary")
    parser.add_argument("--markdown", type=Path, help="Path to write Markdown summary")
    parser.add_argument("--print", dest="print_summary", action="store_true", help="Print a short summary to stdout")
    args = parser.parse_args(argv)

    summary = _build_summary()

    if args.json:
        _write_json(args.json, summary)
    if args.markdown:
        _write_markdown(args.markdown, summary)
    if args.print_summary or (not args.json and not args.markdown):
        _emit_console(summary)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
