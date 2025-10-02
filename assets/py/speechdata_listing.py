from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Iterator, List, Sequence, Tuple


def _normalise_depth(max_depth: int) -> int:
    """Clamp *max_depth* so walkers always traverse at least one level."""

    return max(1, max_depth)


def iter_subtrees(root: Path, *, max_depth: int = 2) -> Iterator[Tuple[str, Path]]:
    """Yield (relative, absolute) directory pairs beneath *root* up to *max_depth*."""

    if not root.is_dir():
        return iter(())

    root = root.resolve()
    max_depth = _normalise_depth(max_depth)
    root_depth = len(root.parts)

    def _walker() -> Iterator[Tuple[str, Path]]:
        for dirpath, dirnames, _ in os.walk(root):
            current = Path(dirpath)
            relative = current.relative_to(root)
            depth = len(current.parts) - root_depth

            dirnames.sort()

            if depth >= max_depth:
                dirnames[:] = []

            if depth == 0:
                continue

            yield relative.as_posix(), current

    return _walker()


def discover_entries(root: Path, *, max_depth: int = 2) -> List[str]:
    """Return entries beneath *root* up to *max_depth* directories deep."""

    if not root.is_dir():
        return []

    entries: List[str] = []
    max_depth = _normalise_depth(max_depth)

    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        relative = current.relative_to(root)
        depth = len(relative.parts)

        dirnames.sort()
        filenames.sort()

        if depth > max_depth:
            dirnames[:] = []
            continue

        if depth >= max_depth:
            dirnames[:] = []

        if depth > 0:
            entries.append(relative.as_posix())

        for filename in filenames:
            if depth == 0:
                entries.append(filename)
            else:
                entries.append((relative / filename).as_posix())

    return entries


def summarise_entries(entries: Sequence[str], *, root: Path) -> List[Dict[str, object]]:
    """Describe each entry within *entries* relative to *root*."""

    summary: List[Dict[str, object]] = []

    for entry in entries:
        resolved = root / entry
        details: Dict[str, object] = {"path": entry}

        try:
            stat_result = resolved.stat()
        except FileNotFoundError:
            details["kind"] = "missing"
            summary.append(details)
            continue
        except OSError as error:
            details["kind"] = "error"
            details["error"] = type(error).__name__
            summary.append(details)
            continue

        if resolved.is_dir():
            files = 0
            directories = 0
            try:
                for child in resolved.iterdir():
                    if child.is_dir():
                        directories += 1
                    elif child.is_file():
                        files += 1
            except OSError as error:
                details["kind"] = "directory"
                details["child_scan_error"] = type(error).__name__
            else:
                details["kind"] = "directory"
                details["children"] = {"directories": directories, "files": files}
        else:
            suffix = resolved.suffix
            details["kind"] = "file"
            details["size_bytes"] = stat_result.st_size
            details["extension"] = suffix[1:] if suffix else ""
            details["extensionless"] = not bool(suffix)

        summary.append(details)

    return summary


def summarise_subtree(path: Path) -> Dict[str, object]:
    """Return extension statistics for the subtree rooted at *path*."""

    total = 0
    extensionless = 0
    extensions: Dict[str, int] = {}

    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            total += 1
            suffix = Path(filename).suffix
            if not suffix:
                extensionless += 1
                continue
            key = suffix.lower()
            extensions[key] = extensions.get(key, 0) + 1

    return {
        "total_files": total,
        "extensionless_files": extensionless,
        "extensions": dict(sorted(extensions.items())),
    }


def build_inventory(root: Path, *, max_depth: int = 2) -> Dict[str, Dict[str, object]]:
    """Return a mapping of relative subtree paths to extension statistics."""

    if not root.is_dir():
        return {}

    inventory: Dict[str, Dict[str, object]] = {}
    for relative, absolute in iter_subtrees(root, max_depth=max_depth):
        inventory[relative] = summarise_subtree(absolute)

    return {key: inventory[key] for key in sorted(inventory)}
