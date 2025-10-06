"""Inventory extensionless speechdata assets after the extension-first reshuffle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

import speechdata_listing

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEECHDATA_ROOT = REPO_ROOT / "speechdata"
DEFAULT_JSON = REPO_ROOT / "assets" / "json" / "speechdata_inventory.json"
DEFAULT_MARKDOWN = REPO_ROOT / "assets" / "md" / "speechdata_manifest.md"
def build_manifest(data: Dict[str, Dict[str, object]]) -> str:
    lines = ["# Speechdata migration manifest", ""]
    lines.append(
        "This snapshot inventories the extensionless assets that remain under `speechdata/` "
        "after the repository-wide extension shuffle. Regenerate it with ``python "
        "assets/py/report_speechdata_inventory.py`` whenever files move. The data "
        "complements the NVDA-focused roadmap in [`assets/md/README.md`](README.md) "
        "and helps us plan the remaining migrations without breaking cached datasets "
        "or NVDA loaders."
    )
    lines.append("")
    lines.append("| Subtree | Files | Extensionless | % Extensionless | Distinct extensions |")
    lines.append("| --- | ---: | ---: | ---: | ---: |")
    for key in sorted(data):
        info = data[key]
        total = info["total_files"] or 0
        extless = info["extensionless_files"] or 0
        percent = 0 if total == 0 else round((extless / total) * 100, 1)
        distinct = len(info["extensions"])
        lines.append(
            f"| `{key}` | {total} | {extless} | {percent:.1f}% | {distinct} |"
        )
    lines.append("")
    lines.append("## Migration notes")
    lines.append("")
    lines.append(
        "- Prioritise folders with ≥80% extensionless files when designing loader shims. "
        "They are most at risk of breakage if we force renames."
    )
    lines.append(
        "- When migrating DataJake or NV Speech Player corpora, document the new asset paths "
        "in [`assets/md/README.md`](README.md) and refresh the cached provenance dashboards "
        "before packaging `eloquence.nvda-addon`."
    )
    lines.append(
        "- For each subtree, record whether NVDA expects exact filenames. If so, extend the "
        "manifest helper to emit a `requires_exact_names` flag so CodeQL and packaging scripts "
        "can warn when extensions change."
    )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        type=Path,
        default=DEFAULT_JSON,
        help="Path to write the JSON inventory (default: %(default)s)",
    )
    parser.add_argument(
        "--markdown",
        type=Path,
        default=DEFAULT_MARKDOWN,
        help="Path to write the Markdown manifest (default: %(default)s)",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=2,
        help="Maximum directory depth to summarise beneath speechdata/ (default: %(default)s)",
    )
    args = parser.parse_args()

    if not SPEECHDATA_ROOT.exists():
        raise SystemExit(
            f"speechdata directory not found at {SPEECHDATA_ROOT}. Run the script from the repository root."
        )

    snapshot = speechdata_listing.build_inventory(SPEECHDATA_ROOT, max_depth=args.max_depth)

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.write_text(build_manifest(snapshot), encoding="utf-8")


if __name__ == "__main__":
    main()
