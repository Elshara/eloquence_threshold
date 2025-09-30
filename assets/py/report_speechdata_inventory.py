"""Inventory extensionless speechdata assets after the extension-first reshuffle."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, Iterable, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEECHDATA_ROOT = REPO_ROOT / "speechdata"
DEFAULT_JSON = REPO_ROOT / "assets" / "json" / "speechdata_inventory.json"
DEFAULT_MARKDOWN = REPO_ROOT / "assets" / "md" / "speechdata_manifest.md"


def iter_subtrees(max_depth: int = 2) -> Iterable[Tuple[str, Path]]:
    """Yield subtrees (relative path, absolute path) up to ``max_depth`` directories deep."""
    root_depth = len(SPEECHDATA_ROOT.parts)
    for path, dirnames, _ in os.walk(SPEECHDATA_ROOT):
        rel = Path(path).relative_to(SPEECHDATA_ROOT)
        depth = len(Path(path).parts) - root_depth
        if depth == 0:
            # skip the root marker
            continue
        if depth > max_depth:
            dirnames[:] = []  # prune deeper walks
            continue
        yield rel.as_posix(), Path(path)


def summarise_tree(path: Path) -> Dict[str, object]:
    total = 0
    extensionless = 0
    extensions: Dict[str, int] = {}
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            total += 1
            ext = Path(filename).suffix
            if not ext:
                extensionless += 1
            else:
                ext_key = ext.lower()
                extensions[ext_key] = extensions.get(ext_key, 0) + 1
    return {
        "total_files": total,
        "extensionless_files": extensionless,
        "extensions": dict(sorted(extensions.items())),
    }


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

    snapshot: Dict[str, Dict[str, object]] = {}
    for rel, path in iter_subtrees(args.max_depth):
        snapshot[rel] = summarise_tree(path)

    # Keep outputs deterministic so diffs stay readable for CodeQL and review.
    ordered_snapshot = {key: snapshot[key] for key in sorted(snapshot)}

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(ordered_snapshot, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.write_text(build_manifest(ordered_snapshot), encoding="utf-8")


if __name__ == "__main__":
    main()
