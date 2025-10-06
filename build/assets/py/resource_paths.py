"""Centralised helpers for locating repository assets after the restructure.

The add-on historically bundled dictionaries, phoneme catalogues, and voice
templates under ``eloquence/`` and ``eloquence_data/`` next to the Python
modules.  The extension-first layout introduced by the repository cleanup now
groups files by extension under ``assets/<ext>/``.  Runtime modules, tooling,
and packaging helpers call into this module so they can resolve the new
locations without hard-coding relative paths in dozens of places.

These utilities prefer the new ``assets/`` directories but keep the legacy
paths as fallbacks so partially migrated trees (or cached packaging templates)
continue to function while we finish the cleanup.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Iterator, List


def _discover_repo_root() -> Path:
    """Return the directory that hosts the ``assets`` tree.

    The helper walks up from the current module until it finds a parent that
    exposes an ``assets`` directory.  This keeps the logic resilient to both
    repository checkouts (where this file lives under ``assets/py``) and
    packaged add-ons (where the module ships inside ``synthDrivers`` alongside
    a sibling ``assets`` directory).
    """

    current = Path(__file__).resolve().parent
    for candidate in [current, *current.parents]:
        assets_dir = candidate / "assets"
        if assets_dir.is_dir():
            return candidate
    # Fall back to the immediate parent so unit tests still run even if the
    # asset tree has not been staged yet.
    return current


_REPO_ROOT = _discover_repo_root()
_ASSETS_ROOT = _REPO_ROOT / "assets"


def repo_root() -> Path:
    """Return the repository root."""

    return _REPO_ROOT


def assets_root() -> Path:
    """Return the ``assets`` directory introduced by the restructuring."""

    return _ASSETS_ROOT


def speechdata_root() -> Path:
    """Return the repository's ``speechdata`` directory.

    The folder continues to host extensionless datasets (for example eSpeak NG
    lexicons) until we can either add safe suffixes or teach the NVDA loaders to
    resolve them dynamically.  Callers should still check ``Path.exists``
    because lean deployments or future cleanups may omit the tree entirely.
    """

    return _REPO_ROOT / "speechdata"


def asset_dir(name: str) -> Path:
    """Return the directory for a given *name* under ``assets/``.

    The directory may not exist if the migration has not staged files of that
    extension yet, so callers should check ``Path.exists`` when appropriate.
    """

    return _ASSETS_ROOT / name


def _existing(paths: Iterable[Path]) -> List[Path]:
    return [path for path in paths if path.exists()]


def _iter_existing(paths: Iterable[Path]) -> Iterator[Path]:
    for path in paths:
        if path.exists():
            yield path


def find_file_casefold(name: str, directories: Iterable[Path]) -> Path:
    """Locate *name* within *directories* using case-folded comparison.

    The helper searches each directory that exists and returns the first entry
    whose name matches ``name`` when both strings are lowered via
    :py:meth:`str.casefold`.  A :class:`FileNotFoundError` is raised when no
    candidate is discovered.  Callers should prefer this over direct
    ``Path(name)`` joins so Windows-centric payloads with inconsistent casing
    (for example ``ECI.DLL`` versus ``eci.dll``) resolve correctly on
    case-sensitive filesystems.
    """

    target = name.casefold()
    for directory in _iter_existing(directories):
        for entry in directory.iterdir():
            if entry.name.casefold() == target:
                return entry
    raise FileNotFoundError(name)


def engine_root(engine: str) -> Path:
    """Return the ``speechdata`` subdirectory assigned to *engine*."""

    return speechdata_root() / engine


def engine_directories(engine: str, *subdirs: str) -> List[Path]:
    """Return existing directories for *engine* under ``speechdata``.

    When *subdirs* is provided, each entry is appended to the engine root and
    candidates that exist on disk are returned.  Without *subdirs* the engine
    root itself is validated.  The helper keeps callers concise when
    translating between engine names (``"eloquence"``, ``"pico"``,
    ``"dectalk"``…) and their staged binary buckets.
    """

    root = engine_root(engine)
    if not subdirs:
        return _existing([root])
    return _existing([root / subdir for subdir in subdirs])


def eloquence_dictionary_dirs() -> List[Path]:
    """Return directories that may contain Eloquence dictionary assets."""

    candidates: List[Path] = []
    # Primary extension buckets.
    for bucket in ("syn", "dic", "txt", "cnt", "uil", "voice"):
        candidates.extend(_existing([asset_dir(bucket)]))

    for subdir in ("syn", "dic", "txt", "cnt", "uil", "voice"):
        candidates.extend(engine_directories("eloquence", subdir))
    candidates.extend(engine_directories("eloquence"))

    # Legacy and partially migrated locations.
    legacy_dirs = [
        _REPO_ROOT / "eloquence",
        _REPO_ROOT / "eloquence_data",
        _REPO_ROOT / "eloquence_data" / "languages",
        _REPO_ROOT / "eloquence_data" / "voices",
    ]
    for legacy in legacy_dirs:
        if legacy.exists():
            candidates.append(legacy)

    # Some extensionless payloads remain in speechdata/ during migration.
    speechdata_root = _REPO_ROOT / "speechdata"
    if speechdata_root.exists():
        candidates.append(speechdata_root)

    # Deduplicate while preserving order.
    seen: set[Path] = set()
    ordered: List[Path] = []
    for path in candidates:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        ordered.append(path)
    return ordered


def eloquence_default_voice_directory() -> Path:
    """Return the preferred directory for Eloquence voice data."""

    directories = eloquence_dictionary_dirs()
    if directories:
        return directories[0]
    return asset_dir("syn")


def eloquence_library_roots() -> List[Path]:
    """Return directories that may contain Eloquence runtime DLLs."""

    roots: List[Path] = _existing([asset_dir("dll"), asset_dir("bin")])
    roots.extend(engine_directories("eloquence", "dll"))
    roots.extend(engine_directories("eloquence", "runtime"))
    roots.extend(engine_directories("eloquence", "sapi"))
    for name in ("eloquence_x64", "eloquence_x86", "eloquence_arm64", "eloquence_arm32", "eloquence_arm"):
        candidate = _REPO_ROOT / name
        if candidate.exists():
            roots.append(candidate)
    legacy = _REPO_ROOT / "eloquence"
    if legacy.exists():
        roots.append(legacy)

    seen: set[Path] = set()
    ordered: List[Path] = []
    for path in roots:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        ordered.append(path)
    return ordered


def voice_data_directories() -> List[Path]:
    """Return directories that store voice catalogue JSON files."""

    roots = [asset_dir("json")]
    voices_subdir = roots[0] / "voices"
    if voices_subdir.exists():
        roots.append(voices_subdir)

    legacy_root = _REPO_ROOT / "eloquence_data"
    if legacy_root.exists():
        roots.append(legacy_root)
        voices_dir = legacy_root / "voices"
        if voices_dir.exists():
            roots.append(voices_dir)

    seen: set[Path] = set()
    ordered: List[Path] = []
    for path in roots:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        ordered.append(path)
    return ordered


def phoneme_inventory_path() -> Path:
    """Return the canonical ``espeak_phonemes.txt`` path."""

    for candidate in (
        asset_dir("txt") / "espeak_phonemes.txt",
        _REPO_ROOT / "eloquence_data" / "espeak_phonemes.txt",
    ):
        if candidate.exists():
            return candidate
    return asset_dir("txt") / "espeak_phonemes.txt"


def phoneme_json_directories() -> List[Path]:
    """Return directories that may contain contributed phoneme JSON data."""

    roots: List[Path] = []
    json_dir = asset_dir("json")
    roots.append(json_dir)
    phoneme_dir = json_dir / "phonemes"
    if phoneme_dir.exists():
        roots.append(phoneme_dir)

    legacy_dir = _REPO_ROOT / "eloquence_data" / "phonemes"
    if legacy_dir.exists():
        roots.append(legacy_dir)

    seen: set[Path] = set()
    ordered: List[Path] = []
    for path in roots:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        ordered.append(path)
    return ordered


def language_profile_directories() -> List[Path]:
    """Return directories containing language profile JSON files."""

    roots = [asset_dir("json")]
    languages_subdir = roots[0] / "languages"
    if languages_subdir.exists():
        roots.append(languages_subdir)

    legacy_dir = _REPO_ROOT / "eloquence_data" / "languages"
    if legacy_dir.exists():
        roots.append(legacy_dir)

    seen: set[Path] = set()
    ordered: List[Path] = []
    for path in roots:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        ordered.append(path)
    return ordered


def wikipedia_index_path() -> Path:
    """Return the cached Wikipedia language index JSON path."""

    for candidate in (
        asset_dir("json") / "wikipedia_language_index.json",
        _REPO_ROOT / "docs" / "wikipedia_language_index.json",
    ):
        if candidate.exists():
            return candidate
    return asset_dir("json") / "wikipedia_language_index.json"


def nvspeechplayer_core_path() -> Path:
    """Return the canonical NV Speech Player phoneme export location."""

    for candidate in (
        asset_dir("json") / "nvspeechplayer_core.json",
        _REPO_ROOT / "eloquence_data" / "phonemes" / "nvspeechplayer_core.json",
    ):
        if candidate.exists():
            return candidate
    return asset_dir("json") / "nvspeechplayer_core.json"


def language_seed_output_path() -> Path:
    """Return the canonical seed bundle location for language profiles."""

    for candidate in (
        asset_dir("json") / "world_language_seeds.json",
        _REPO_ROOT / "eloquence_data" / "languages" / "world_language_seeds.json",
    ):
        if candidate.exists():
            return candidate
    return asset_dir("json") / "world_language_seeds.json"


def voice_seed_output_path() -> Path:
    """Return the canonical seed bundle location for voice templates."""

    for candidate in (
        asset_dir("json") / "eloquence_global_seeds.json",
        _REPO_ROOT / "eloquence_data" / "voices" / "eloquence_global_seeds.json",
    ):
        if candidate.exists():
            return candidate
    return asset_dir("json") / "eloquence_global_seeds.json"


def iter_language_profile_files() -> Iterator[Path]:
    """Yield JSON files that look like language profiles."""

    for directory in language_profile_directories():
        if not directory.exists():
            continue
        for entry in sorted(directory.glob("*.json")):
            yield entry


def iter_voice_catalog_files() -> Iterator[Path]:
    """Yield JSON files that may contain voice catalogue data."""

    for directory in voice_data_directories():
        if not directory.exists():
            continue
        for entry in sorted(directory.glob("*.json")):
            yield entry


def iter_phoneme_json_files() -> Iterator[Path]:
    """Yield JSON files that may contain contributed phoneme definitions."""

    for directory in phoneme_json_directories():
        if not directory.exists():
            continue
        for entry in sorted(directory.glob("*.json")):
            yield entry
