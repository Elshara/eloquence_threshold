#!/usr/bin/env python3
"""Build an ``eloquence.nvda-addon`` package from the working tree.

The original build helper downloaded an upstream ``eloquence.nvda-addon``
release and patched a handful of files in-place.  That approach is brittle in
modern environments where outbound TLS may be blocked or certificate trust
stores are incomplete, so this script now stages the repository contents into a
fresh NVDA add-on archive instead.

Usage highlights::

    python build.py                      # create eloquence.nvda-addon
    python build.py --output dist/addon.nvda-addon
    python build.py --template path/to/existing-addon.nvda-addon

If a base add-on template is supplied (or already cached as
``eloquence_original.nvda-addon``) the script will extract its payload first so
that legacy 32-bit Eloquence binaries remain intact.  Otherwise the archive is
created purely from the Python modules and data files in this repository.  Make
sure any proprietary runtime you are entitled to redistribute is staged inside
``speechdata/eloquence/dll`` and the accompanying ``*.syn`` voices live in
``speechdata/eloquence/syn`` before packaging the add-on.
"""

from __future__ import annotations

import argparse
import json
import shutil
import ssl
import sys
import tempfile
import urllib.error
import urllib.request
import urllib.parse
import socket
import ipaddress
import zipfile
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple, List, Sequence

import resource_paths
import speechdata_listing

if sys.version_info < (3, 8):
    raise RuntimeError("Python 3.8 or newer is required to build the add-on")


SCRIPT_DIR = Path(__file__).resolve().parent
ASSETS_ROOT = resource_paths.assets_root()
REPO_ROOT = resource_paths.repo_root()

DEFAULT_OUTPUT = REPO_ROOT / "eloquence.nvda-addon"
DEFAULT_TEMPLATE = REPO_ROOT / "eloquence_original.nvda-addon"
TEMPLATE_URL = (
    "https://github.com/pumper42nickel/eloquence_threshold/releases/download/"
    "v0.20210417.01/eloquence.nvda-addon"
)

SYNTH_DRIVER_MODULES: Dict[Path, Path] = {
    SCRIPT_DIR / "all_phonemes.py": Path("synthDrivers") / "eloquence.py",
    SCRIPT_DIR / "Eloquence.py": Path("synthDrivers") / "_eloquence.py",
    SCRIPT_DIR / "language_profiles.py": Path("synthDrivers") / "language_profiles.py",
    SCRIPT_DIR / "phoneme_catalog.py": Path("synthDrivers") / "phoneme_catalog.py",
    SCRIPT_DIR / "phoneme_customizer.py": Path("synthDrivers") / "phoneme_customizer.py",
    SCRIPT_DIR / "voice_catalog.py": Path("synthDrivers") / "voice_catalog.py",
    SCRIPT_DIR / "voice_parameters.py": Path("synthDrivers") / "voice_parameters.py",
    SCRIPT_DIR / "resource_paths.py": Path("synthDrivers") / "resource_paths.py",
}

ROOT_FILES: Tuple[Tuple[Path, Path], ...] = (
    (ASSETS_ROOT / "ini" / "manifest.ini", Path("manifest.ini")),
)

ASSET_EXCLUDES = {"py", "pyc", "pyo"}


TRACE_REGISTRY = {
    "parse_args": "Parse CLI arguments and apply defaults for offline packaging runs.",
    "_validate_template_url": "Confirm the template URL targets an approved GitHub host before optional downloads.",
    "ensure_template": "Locate or download the baseline template archive that seeds legacy binaries.",
    "stage_template": "Extract an optional template archive into the temporary staging directory.",
    "stage_root_files": "Copy root-level metadata such as manifest.ini into the staging directory.",
    "stage_synth_driver_modules": "Copy the Eloquence synth driver modules into synthDrivers/ for NVDA.",
    "stage_assets_tree": "Mirror the extension-scoped assets/ hierarchy into the packaged add-on.",
    "stage_speechdata_tree": "Bundle temporary speechdata/ payloads that still need extension triage.",
    "discover_speechdata_subtrees": "Enumerate candidate speechdata/ entries for targeted packaging drills.",
    "build_speechdata_inventory": "Collect extension statistics for discovered speechdata/ directories.",
    "aggregate_speechdata_inventory": "Aggregate speechdata directory stats into a global inventory summary.",
    "write_speechdata_list_output": "Serialise speechdata listings when --list-speechdata-output is supplied.",
    "copy_optional_directory": "Copy opt-in legacy/runtime directories like eloquence_data or architecture caches.",
    "has_runtime_assets": "Scan known locations for eci.dll so packaging can warn about missing runtimes.",
    "write_archive": "Zip the staged tree into an .nvda-addon payload ready for NVDA installation.",
}

TRACE_DATA = {
    name: {"description": description, "calls": 0, "events": []}
    for name, description in TRACE_REGISTRY.items()
}

TRACE_ENABLED = False
TEMP_DIRECTORY_ROOT = Path(tempfile.gettempdir()).resolve()


def _normalise_path_for_trace(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        pass
    try:
        relative_temp = path.resolve().relative_to(TEMP_DIRECTORY_ROOT)
    except ValueError:
        return path.as_posix()
    parts = list(relative_temp.parts)
    if parts:
        first = parts[0]
        if first.startswith("eloquence_build_"):
            parts[0] = "eloquence_build/<run>"
        else:
            parts[0] = f"<temp_root>/{first}"
    return "<temp>/" + "/".join(parts)


def _serialise_details(details: Dict[str, object]) -> Dict[str, object]:
    serialised: Dict[str, object] = {}
    for key, value in details.items():
        if isinstance(value, Path):
            serialised[key] = _normalise_path_for_trace(value)
        else:
            serialised[key] = value
    return serialised


def configure_trace(json_path: Optional[Path], markdown_path: Optional[Path]) -> None:
    """Enable tracing when either report path is supplied."""

    global TRACE_ENABLED
    TRACE_ENABLED = bool(json_path or markdown_path)
    if not TRACE_ENABLED:
        return
    for entry in TRACE_DATA.values():
        entry["calls"] = 0
        entry["events"] = []


def record_trace(name: str, *, details: Optional[Dict[str, object]] = None) -> None:
    if not TRACE_ENABLED:
        return
    if name not in TRACE_DATA:
        return
    entry = TRACE_DATA[name]
    entry["calls"] += 1
    if details:
        entry["events"].append(_serialise_details(details))


def build_trace_summary() -> Dict[str, Dict[str, object]]:
    summary: Dict[str, Dict[str, object]] = {}
    for name, payload in TRACE_DATA.items():
        summary[name] = {
            "description": payload["description"],
            "calls": payload["calls"],
            "triggered": bool(payload["calls"]),
            "events": payload["events"],
        }
    return summary


def _format_event(details: Dict[str, object]) -> str:
    components = []
    for key, value in details.items():
        components.append(f"{key}={value}")
    return ", ".join(components)


def emit_trace_reports(
    *,
    json_path: Optional[Path],
    markdown_path: Optional[Path],
    context: Dict[str, object],
) -> None:
    if not TRACE_ENABLED:
        return

    summary = build_trace_summary()
    serialised_context = _serialise_details(context)

    if json_path is not None:
        json_path = json_path.expanduser()
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with json_path.open("w", encoding="utf-8") as handle:
            json.dump(
                {
                    "context": serialised_context,
                    "helpers": summary,
                },
                handle,
                indent=2,
                sort_keys=True,
            )

    if markdown_path is not None:
        markdown_path = markdown_path.expanduser()
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Build helper execution trace",
            "",
            "The table below captures which packaging helpers executed during the most recent",
            "`python build.py` invocation. Use it alongside the file-structure audit to plan",
            "follow-up refactors and CodeQL-reviewed NVDA packaging drills.",
            "",
            "## Invocation context",
        ]
        for key, value in sorted(serialised_context.items()):
            lines.append(f"- **{key.replace('_', ' ').title()}**: {value}")
        lines.append("")
        lines.extend(
            [
                "## Helper coverage",
                "",
                "| Helper | Triggered? | Calls | Notes |",
                "| --- | --- | --- | --- |",
            ]
        )
        for name, payload in summary.items():
            triggered = "✅" if payload["triggered"] else "⚠️"
            calls = payload["calls"]
            if payload["events"]:
                notes = "<br>".join(_format_event(event) for event in payload["events"])
            else:
                notes = "—"
            lines.append(
                f"| `{name}` | {triggered} | {calls} | {notes} |"
            )

        markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _contains_eci_dll(path: Path) -> bool:
    if not path.is_dir():
        return False
    for entry in path.iterdir():
        if entry.name.lower() == "eci.dll":
            return True
    return False


def has_runtime_assets() -> bool:
    """Return ``True`` if any staged directory exposes ``eci.dll``."""

    found = False
    for candidate in resource_paths.eloquence_library_roots():
        if _contains_eci_dll(candidate):
            found = True
            break
    record_trace("has_runtime_assets", details={"found": found})
    return found

ARCH_DIRECTORIES: Tuple[Tuple[str, Path, str], ...] = (
    ("eloquence_x86", Path("synthDrivers") / "eloquence" / "x86", "Embedded 32-bit runtime from ./eloquence_x86"),
    ("eloquence_x64", Path("synthDrivers") / "eloquence" / "x64", "Embedded 64-bit runtime from ./eloquence_x64"),
    ("eloquence_arm32", Path("synthDrivers") / "eloquence" / "arm32", "Embedded 32-bit ARM runtime from ./eloquence_arm32"),
    ("eloquence_arm64", Path("synthDrivers") / "eloquence" / "arm64", "Embedded 64-bit ARM runtime from ./eloquence_arm64"),
    ("eloquence_arm", Path("synthDrivers") / "eloquence" / "arm", "Embedded ARM runtime from ./eloquence_arm"),
)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Eloquence NVDA add-on")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Destination path for the generated .nvda-addon archive",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=DEFAULT_TEMPLATE,
        help="Existing add-on to use as a packaging template",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Do not attempt to download a template when it is missing",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Skip TLS certificate verification when downloading the template",
    )
    parser.add_argument(
        "--template-url",
        default=TEMPLATE_URL,
        help="Override the URL used to fetch the base template",
    )
    parser.add_argument(
        "--no-speechdata",
        action="store_true",
        help="Skip bundling the speechdata/ directory when packaging the add-on",
    )
    parser.add_argument(
        "--speechdata-subtree",
        action="append",
        default=[],
        metavar="RELATIVE_PATH",
        help=(
            "Relative path under speechdata/ to include in the package. "
            "Provide multiple times to bundle several subtrees."
        ),
    )
    parser.add_argument(
        "--list-speechdata",
        action="store_true",
        help=(
            "List available speechdata/ entries (up to the configured depth) and exit "
            "without packaging."
        ),
    )
    parser.add_argument(
        "--list-speechdata-summary",
        action="store_true",
        help=(
            "When listing speechdata/, print per-directory extension statistics "
            "and include them in generated JSON reports."
        ),
    )
    parser.add_argument(
        "--list-speechdata-bytes",
        action="store_true",
        help=(
            "When listing speechdata/ summaries, include byte-level totals for each "
            "directory and aggregated extension sizes."
        ),
    )
    parser.add_argument(
        "--list-speechdata-depth",
        type=int,
        default=2,
        metavar="DEPTH",
        help=(
            "Directory depth to scan when listing speechdata/ entries (default: %(default)s)."
        ),
    )
    parser.add_argument(
        "--list-speechdata-output",
        type=Path,
        metavar="JSON_PATH",
        help=(
            "Write a JSON report describing discovered speechdata entries when listing."
        ),
    )
    parser.add_argument(
        "--trace-json",
        type=Path,
        help="Write a JSON report summarising which helpers executed during the build",
    )
    parser.add_argument(
        "--trace-markdown",
        type=Path,
        help="Write a Markdown report summarising which helpers executed during the build",
    )
    args = parser.parse_args(argv)

    if args.no_speechdata and args.speechdata_subtree:
        parser.error("--no-speechdata cannot be combined with --speechdata-subtree")

    if args.list_speechdata_depth < 1:
        parser.error("--list-speechdata-depth must be at least 1")

    if args.list_speechdata_output and not args.list_speechdata:
        parser.error("--list-speechdata-output requires --list-speechdata")

    if args.list_speechdata_summary and not args.list_speechdata:
        parser.error("--list-speechdata-summary requires --list-speechdata")

    if args.list_speechdata_bytes and not args.list_speechdata:
        parser.error("--list-speechdata-bytes requires --list-speechdata")

    normalised: list[str] = []
    root_requested = False
    for entry in args.speechdata_subtree:
        normalised_entry = entry.replace("\\", "/")
        candidate = Path(normalised_entry)
        if candidate.is_absolute() or any(part == ".." for part in candidate.parts):
            parser.error(
                "--speechdata-subtree values must be relative paths beneath speechdata/."
            )
        filtered_parts = [part for part in candidate.parts if part not in ("", ".")]
        if filtered_parts and filtered_parts[0].lower() == "speechdata":
            filtered_parts = filtered_parts[1:]
        if not filtered_parts:
            root_requested = True
            continue
        normalised.append(Path(*filtered_parts).as_posix())

    if root_requested:
        normalised = []

    seen: set[str] = set()
    ordered: list[str] = []
    for entry in normalised:
        if entry in seen:
            continue
        seen.add(entry)
        ordered.append(entry)

    args.speechdata_subtree = ordered
    return args


ALLOWED_TEMPLATE_HOSTS = {"github.com", "raw.githubusercontent.com"}
ALLOWED_REPO_PREFIXES = ("nvaccess/", "pumper42nickel/", "Elshara/")


def _is_trusted_template_url(url: str) -> bool:
    """Return ``True`` when *url* points at an approved template source."""

    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return False

    if parsed.scheme.lower() != "https":
        return False

    hostname = (parsed.hostname or "").lower()
    if hostname not in ALLOWED_TEMPLATE_HOSTS:
        return False

    normalized_path = parsed.path.lstrip("/")
    if hostname == "github.com":
        return normalized_path.startswith(ALLOWED_REPO_PREFIXES)

    if hostname == "raw.githubusercontent.com":
        return bool(normalized_path)

    return False


def _validate_template_url(url: str) -> None:
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception as error:
        raise ValueError(f"Invalid template URL: {error}") from error

    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for template downloads.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Invalid URL: missing hostname.")

    if not _is_trusted_template_url(url):
        raise ValueError(
            "Only GitHub or raw.githubusercontent.com URLs within approved "
            "repositories are allowed for --template-url"
        )

    try:
        resolved_ip = socket.gethostbyname(hostname)
    except Exception as dns_exc:
        raise ValueError(f"Could not resolve hostname '{hostname}': {dns_exc}") from dns_exc

    ip_obj = ipaddress.ip_address(resolved_ip)
    if any(
        (
            ip_obj.is_loopback,
            ip_obj.is_private,
            ip_obj.is_link_local,
            ip_obj.is_reserved,
            ip_obj.is_multicast,
        )
    ):
        raise ValueError(
            f"Refusing to download template from restricted network address: {resolved_ip}"
        )


def ensure_template(
    path: Path, *, url: str, allow_download: bool, insecure: bool
) -> Optional[Path]:
    """Return ``path`` if it exists, otherwise attempt to download it."""

    if path.is_file():
        record_trace(
            "ensure_template",
            details={"path": path, "result": "existing"},
        )
        return path
    if not allow_download:
        record_trace(
            "ensure_template",
            details={"path": path, "result": "missing", "allow_download": False},
        )
        return None
    try:
        _validate_template_url(url)
    except ValueError as error:
        print(f"Warning: {error}")
        record_trace(
            "ensure_template",
            details={"path": path, "result": "skipped_invalid_url", "error": str(error)},
        )
        return None
    try:
        print(f"Downloading template from {url}…")
        context = ssl._create_unverified_context() if insecure else None
        with urllib.request.urlopen(url, context=context) as response:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("wb") as handle:
                shutil.copyfileobj(response, handle)
        record_trace(
            "ensure_template",
            details={
                "path": path,
                "result": "downloaded",
                "insecure": insecure,
            },
        )
        return path
    except (OSError, urllib.error.URLError, ValueError) as exc:
        print(f"Warning: unable to download template: {exc}")
        record_trace(
            "ensure_template",
            details={
                "path": path,
                "result": "download_failed",
                "error": str(exc),
            },
        )
    return None


def stage_template(staging_dir: Path, template: Optional[Path]) -> bool:
    """Extract ``template`` into ``staging_dir`` if provided."""

    if template is None:
        (staging_dir / "synthDrivers").mkdir(parents=True, exist_ok=True)
        record_trace(
            "stage_template",
            details={"template": None, "result": "initialised"},
        )
        return False
    with zipfile.ZipFile(template, "r") as archive:
        archive.extractall(staging_dir)
    record_trace(
        "stage_template",
        details={"template": template, "result": "extracted"},
    )
    return True


def copy_file(src: Path, dest: Path) -> None:
    if not src.is_file():
        raise FileNotFoundError(f"Missing source file: {src}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def copy_optional_directory(
    src: Path, dest: Path, *, preserve_existing: bool = False
) -> bool:
    if not src.is_dir():
        record_trace(
            "copy_optional_directory",
            details={
                "source": src,
                "destination": dest,
                "copied": False,
                "reason": "missing_source",
            },
        )
        return False
    if dest.exists() and not preserve_existing:
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest, dirs_exist_ok=preserve_existing)
    record_trace(
        "copy_optional_directory",
        details={
            "source": src,
            "destination": dest,
            "copied": True,
            "preserve_existing": preserve_existing,
        },
    )
    return True


def stage_synth_driver_modules(staging_dir: Path) -> None:
    """Copy synthesizer modules into the ``synthDrivers`` package."""

    for src, relative_dest in SYNTH_DRIVER_MODULES.items():
        copy_file(src, staging_dir / relative_dest)

    synth_root = staging_dir / "synthDrivers"
    synth_root.mkdir(parents=True, exist_ok=True)
    init_file = synth_root / "__init__.py"
    if not init_file.exists():
        init_file.write_text(
            "# Auto-generated by build.py so NVDA treats this folder as a package.\n"
            "__all__ = ['eloquence']\n"
        )
    record_trace(
        "stage_synth_driver_modules",
        details={"modules_copied": len(SYNTH_DRIVER_MODULES)},
    )


def stage_root_files(staging_dir: Path) -> None:
    for src, relative_dest in ROOT_FILES:
        copy_file(src, staging_dir / relative_dest)
    record_trace(
        "stage_root_files",
        details={"files_copied": len(ROOT_FILES)},
    )


def iter_asset_directories() -> Iterable[Path]:
    assets_root = resource_paths.assets_root()
    if not assets_root.exists():
        return
    for path in sorted(assets_root.iterdir()):
        if path.name in ASSET_EXCLUDES:
            continue
        yield path


def stage_assets_tree(staging_dir: Path) -> bool:
    """Copy the ``assets`` hierarchy into the packaged add-on."""

    dest_root = staging_dir / "assets"
    dest_root.mkdir(parents=True, exist_ok=True)
    copied_any = False
    copied_entries = 0
    for asset_path in iter_asset_directories():
        destination = dest_root / asset_path.name
        if asset_path.is_dir():
            copy_optional_directory(asset_path, destination, preserve_existing=False)
            copied_any = True
            copied_entries += 1
        elif asset_path.is_file():
            copy_file(asset_path, destination)
            copied_any = True
            copied_entries += 1
    record_trace(
        "stage_assets_tree",
        details={"copied": copied_any, "entries": copied_entries},
    )
    return copied_any


def discover_speechdata_subtrees(*, max_depth: int = 2) -> List[str]:
    """Return candidate ``speechdata/`` entries up to ``max_depth`` directories deep."""

    root = resource_paths.speechdata_root()
    effective_depth = max(1, max_depth)
    exists = root.is_dir()
    entries = (
        speechdata_listing.discover_entries(root, max_depth=effective_depth)
        if exists
        else []
    )

    record_trace(
        "discover_speechdata_subtrees",
        details={
            "exists": exists,
            "max_depth": effective_depth,
            "entries": len(entries),
        },
    )
    return entries


def build_speechdata_inventory(*, max_depth: int = 2) -> Dict[str, Dict[str, object]]:
    """Return extension statistics for directories beneath ``speechdata/``."""

    root = resource_paths.speechdata_root()
    effective_depth = max(1, max_depth)
    exists = root.is_dir()
    inventory = (
        speechdata_listing.build_inventory(root, max_depth=effective_depth)
        if exists
        else {}
    )

    record_trace(
        "build_speechdata_inventory",
        details={
            "exists": exists,
            "max_depth": effective_depth,
            "entries": len(inventory),
        },
    )
    return inventory


def aggregate_speechdata_inventory(
    inventory: Dict[str, Dict[str, object]]
) -> Dict[str, object]:
    """Aggregate *inventory* statistics so listings can report global totals."""

    summary = speechdata_listing.summarise_inventory_totals(inventory)

    record_trace(
        "aggregate_speechdata_inventory",
        details={
            "directories": summary.get("directories", 0),
            "total_files": summary.get("total_files", 0),
            "extensionless_files": summary.get("extensionless_files", 0),
            "total_bytes": summary.get("total_bytes", 0),
            "unique_extensions": len(summary.get("extensions", {})),
        },
    )

    return summary


def summarise_speechdata_entries(
    entries: Sequence[str],
    *,
    root: Path,
) -> List[Dict[str, object]]:
    """Describe discovered speechdata entries with lightweight metadata."""

    return speechdata_listing.summarise_entries(entries, root=root)


def write_speechdata_list_output(
    output_path: Path,
    *,
    speechdata_root: Path,
    depth: int,
    entries: Sequence[str],
    inventory: Optional[Dict[str, Dict[str, object]]],
    inventory_totals: Optional[Dict[str, object]],
) -> Dict[str, object]:
    """Write a JSON payload describing the speechdata listing to *output_path*."""

    output_path = output_path.expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    root_exists = speechdata_root.is_dir()
    payload: Dict[str, object] = {
        "speechdata_root": speechdata_root.as_posix(),
        "root_exists": root_exists,
        "max_depth": depth,
        "entries": [] if not root_exists else summarise_speechdata_entries(entries, root=speechdata_root),
        "inventory": inventory if inventory is not None else None,
        "inventory_totals": inventory_totals if inventory_totals is not None else None,
    }

    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)

    record_trace(
        "write_speechdata_list_output",
        details={
            "output": output_path,
            "entries": len(entries),
            "root_exists": root_exists,
            "inventory_entries": 0 if inventory is None else len(inventory),
            "has_inventory_totals": inventory_totals is not None,
            "total_bytes": 0
            if not inventory_totals
            else inventory_totals.get("total_bytes", 0),
        },
    )

    return payload


def stage_speechdata_tree(
    staging_dir: Path,
    *,
    subtrees: Optional[Iterable[str]] = None,
    skip: bool = False,
) -> Tuple[bool, Dict[str, object]]:
    """Copy ``speechdata/`` (or selected subtrees) into ``staging_dir``.

    When *subtrees* is empty the entire ``speechdata`` directory is copied.
    Otherwise each relative path is mirrored beneath ``speechdata/`` inside the
    staging directory.  The return value pairs a boolean that signals whether
    any data was copied with a dictionary describing the mode and which entries
    were included or missing.
    """

    requested = list(subtrees or [])
    if skip:
        record_trace(
            "stage_speechdata_tree",
            details={
                "copied": False,
                "reason": "skip_requested",
                "mode": "skipped",
                "requested": len(requested),
                "missing": list(requested),
            },
        )
        return False, {
            "mode": "skipped",
            "requested": len(requested),
            "copied_entries": 0,
            "missing": list(requested),
            "included": [],
        }

    speechdata_root = resource_paths.speechdata_root()
    if not speechdata_root.is_dir():
        record_trace(
            "stage_speechdata_tree",
            details={
                "copied": False,
                "reason": "missing_directory",
                "mode": "missing",
                "requested": len(requested),
                "missing": list(requested),
            },
        )
        return False, {
            "mode": "missing",
            "requested": len(requested),
            "copied_entries": 0,
            "missing": list(requested),
            "included": [],
        }

    if not requested:
        copied = copy_optional_directory(
            speechdata_root,
            staging_dir / "speechdata",
            preserve_existing=False,
        )
        record_trace(
            "stage_speechdata_tree",
            details={
                "copied": copied,
                "mode": "full",
                "requested": 0,
                "missing": [],
            },
        )
        return copied, {
            "mode": "full",
            "requested": 0,
            "copied_entries": 1 if copied else 0,
            "missing": [],
            "included": ["."] if copied else [],
        }

    dest_root = staging_dir / "speechdata"
    dest_root.mkdir(parents=True, exist_ok=True)

    copied_any = False
    copied_entries = 0
    missing: List[str] = []
    included: List[str] = []
    for relative in requested:
        source = speechdata_root / relative
        if not source.exists():
            missing.append(relative)
            continue
        destination = dest_root / relative
        if source.is_dir():
            copy_optional_directory(source, destination, preserve_existing=False)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        copied_any = True
        copied_entries += 1
        included.append(relative)

    record_trace(
        "stage_speechdata_tree",
        details={
            "copied": copied_any,
            "mode": "subset",
            "requested": len(requested),
            "copied_entries": copied_entries,
            "missing": missing,
            "included": included,
        },
    )
    return copied_any, {
        "mode": "subset",
        "requested": len(requested),
        "copied_entries": copied_entries,
        "missing": missing,
        "included": included,
    }


def write_archive(staging_dir: Path, output: Path) -> None:
    if output.exists():
        output.unlink()
    output.parent.mkdir(parents=True, exist_ok=True)
    file_count = 0
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(staging_dir.rglob("*")):
            if not path.is_file():
                continue
            arcname = path.relative_to(staging_dir).as_posix()
            archive.write(path, arcname)
            file_count += 1
    record_trace(
        "write_archive",
        details={"output": output, "files_packaged": file_count},
    )


def main() -> None:
    args = parse_args()
    configure_trace(args.trace_json, args.trace_markdown)
    record_trace(
        "parse_args",
        details={
            "output": args.output,
            "template": args.template,
            "no_download": args.no_download,
            "insecure": args.insecure,
            "template_url": args.template_url,
            "no_speechdata": args.no_speechdata,
            "speechdata_subtrees": args.speechdata_subtree,
        "list_speechdata": args.list_speechdata,
        "list_speechdata_summary": args.list_speechdata_summary,
        "list_speechdata_bytes": args.list_speechdata_bytes,
        "list_speechdata_depth": args.list_speechdata_depth,
        "list_speechdata_output": args.list_speechdata_output,
    },
)

    if args.list_speechdata:
        subtrees = discover_speechdata_subtrees(max_depth=args.list_speechdata_depth)
        speechdata_root = resource_paths.speechdata_root()
        payload: Optional[Dict[str, object]] = None
        inventory: Optional[Dict[str, Dict[str, object]]] = None
        inventory_totals: Optional[Dict[str, object]] = None
        if (
            args.list_speechdata_summary
            or args.list_speechdata_bytes
            or args.list_speechdata_output is not None
        ):
            inventory = build_speechdata_inventory(max_depth=args.list_speechdata_depth)
            inventory_totals = aggregate_speechdata_inventory(inventory)
        if subtrees:
            print(
                "Discovered speechdata entries (depth ≤ "
                f"{args.list_speechdata_depth}):"
            )
            for entry in subtrees:
                print(f" - {entry}")
        elif speechdata_root.is_dir():
            print(
                "speechdata directory exists but no entries were found within the "
                f"requested depth ({args.list_speechdata_depth})."
            )
        else:
            print(
                "speechdata directory not found – stage cached datasets before "
                "packaging or adjust the repository checkout."
            )

        if args.list_speechdata_summary:
            if inventory:
                print(
                    "Speechdata inventory summary (depth ≤ "
                    f"{args.list_speechdata_depth}):"
                )
                if inventory_totals:
                    total_parts = [
                        f"directories={inventory_totals.get('directories', 0)}",
                        f"total_files={inventory_totals.get('total_files', 0)}",
                    ]
                    total_extensionless = inventory_totals.get("extensionless_files", 0)
                    if total_extensionless:
                        total_parts.append(
                            f"extensionless={total_extensionless}"
                        )
                    if args.list_speechdata_bytes:
                        total_parts.append(
                            f"bytes={inventory_totals.get('total_bytes', 0)}"
                        )
                        extensionless_bytes = inventory_totals.get(
                            "extensionless_bytes", 0
                        )
                        if extensionless_bytes:
                            total_parts.append(
                                f"extensionless_bytes={extensionless_bytes}"
                            )
                    print(f" Overall totals: {'; '.join(total_parts)}")
                    total_extensions = inventory_totals.get("extensions", {})
                    if total_extensions:
                        overall_extensions = ", ".join(
                            f"{ext}×{count}" for ext, count in total_extensions.items()
                        )
                        print(f"   Extensions: {overall_extensions}")
                    if args.list_speechdata_bytes:
                        total_extension_bytes = inventory_totals.get(
                            "extension_bytes", {}
                        )
                        if total_extension_bytes:
                            bytes_fragments = ", ".join(
                                f"{ext}={size}" for ext, size in total_extension_bytes.items()
                            )
                            print(f"   Extension sizes: {bytes_fragments}")
                for relative, stats in inventory.items():
                    extensions = stats.get("extensions", {})
                    extension_fragments = [
                        f"{ext}×{count}" for ext, count in extensions.items()
                    ]
                    summary_parts = [f"total={stats.get('total_files', 0)}"]
                    extensionless = stats.get("extensionless_files", 0)
                    if extensionless:
                        summary_parts.append(f"extensionless={extensionless}")
                    if args.list_speechdata_bytes:
                        summary_parts.append(
                            f"bytes={stats.get('total_bytes', 0)}"
                        )
                        extensionless_bytes = stats.get("extensionless_bytes", 0)
                        if extensionless_bytes:
                            summary_parts.append(
                                f"extensionless_bytes={extensionless_bytes}"
                            )
                    if extension_fragments:
                        summary_parts.append(
                            "extensions=" + ", ".join(extension_fragments)
                        )
                    if args.list_speechdata_bytes:
                        extension_bytes = stats.get("extension_bytes", {})
                        if extension_bytes:
                            summary_parts.append(
                                "extension_bytes="
                                + ", ".join(
                                    f"{ext}={size}" for ext, size in extension_bytes.items()
                                )
                            )
                    print(f" - {relative}: {'; '.join(summary_parts)}")
            elif speechdata_root.is_dir():
                print(
                    "No directory-level statistics were collected within the "
                    "requested depth. Increase --list-speechdata-depth to see "
                    "nested directories."
                )

        if args.list_speechdata_output is not None:
            payload = write_speechdata_list_output(
                args.list_speechdata_output,
                speechdata_root=speechdata_root,
                depth=args.list_speechdata_depth,
                entries=subtrees,
                inventory=inventory,
                inventory_totals=inventory_totals,
            )
            print(f"Wrote speechdata listing to {args.list_speechdata_output}")

        emit_trace_reports(
            json_path=args.trace_json,
            markdown_path=args.trace_markdown,
            context={
                "mode": "list_speechdata",
                "speechdata_entries": subtrees,
                "speechdata_root": speechdata_root,
                "speechdata_depth": args.list_speechdata_depth,
                "speechdata_bytes_requested": args.list_speechdata_bytes,
                "speechdata_listing": payload,
                "speechdata_inventory": inventory,
                "speechdata_inventory_totals": inventory_totals,
            },
        )
        return

    _validate_template_url(str(args.template_url))
    record_trace(
        "_validate_template_url",
        details={"template_url": args.template_url},
    )
    template_path = ensure_template(
        args.template.expanduser().resolve(),
        url=args.template_url,
        allow_download=not args.no_download,
        insecure=args.insecure,
    )

    with tempfile.TemporaryDirectory(prefix="eloquence_build_") as tmpdir:
        staging_dir = Path(tmpdir)
        template_used = stage_template(staging_dir, template_path)

        stage_root_files(staging_dir)
        stage_synth_driver_modules(staging_dir)
        assets_copied = stage_assets_tree(staging_dir)
        speechdata_copied, speechdata_details = stage_speechdata_tree(
            staging_dir,
            subtrees=args.speechdata_subtree,
            skip=args.no_speechdata,
        )

        legacy_data_copied = copy_optional_directory(
            REPO_ROOT / "eloquence_data",
            staging_dir / "synthDrivers" / "eloquence_data",
            preserve_existing=False,
        )
        legacy_runtime_copied = copy_optional_directory(
            REPO_ROOT / "eloquence",
            staging_dir / "synthDrivers" / "eloquence",
            preserve_existing=True,
        )

        copied_architectures = []
        for directory, destination, message in ARCH_DIRECTORIES:
            if copy_optional_directory(
                REPO_ROOT / directory,
                staging_dir / destination,
                preserve_existing=True,
            ):
                copied_architectures.append(message)

        if assets_copied:
            print("Copied assets/ directory into the package")
        else:
            print("Warning: assets directory was not copied – packaged add-on may be incomplete")

        mode = speechdata_details["mode"]
        if mode == "full" and speechdata_copied:
            print("Bundled speechdata directory for extensionless resources")
        elif mode == "skipped":
            print("Skipped speechdata bundling (requested via --no-speechdata)")
        elif mode == "missing":
            print(
                "Warning: speechdata directory not found – no extensionless assets were bundled"
            )
        elif mode == "subset":
            included = speechdata_details.get("included", [])
            missing = speechdata_details.get("missing", [])
            if included:
                print(
                    "Bundled speechdata subtrees: "
                    + ", ".join(sorted(included))
                )
            if missing:
                print(
                    "Warning: missing speechdata subtrees were skipped: "
                    + ", ".join(sorted(missing))
                )
        else:
            print(
                "Warning: speechdata directory was not copied – check repository permissions"
            )

        if legacy_data_copied:
            print("Bundled legacy eloquence_data directory")

        if legacy_runtime_copied:
            print("Embedded legacy Eloquence runtime from ./eloquence")
        elif not template_used and not has_runtime_assets():
            print(
                "Warning: no Eloquence runtime detected. Stage ECI.DLL inside "
                "speechdata/eloquence/dll and copy .syn voices into "
                "speechdata/eloquence/syn before installing the add-on."
            )
        for notice in copied_architectures:
            print(notice)

        write_archive(staging_dir, args.output.expanduser().resolve())

    print(f"Created {args.output}")

    emit_trace_reports(
        json_path=args.trace_json,
        markdown_path=args.trace_markdown,
        context={
            "output": args.output,
            "template": template_path,
            "template_used": template_used,
            "assets_copied": assets_copied,
            "speechdata_copied": speechdata_copied,
            "speechdata_details": speechdata_details,
            "legacy_data_copied": legacy_data_copied,
            "legacy_runtime_copied": legacy_runtime_copied,
            "copied_architectures": copied_architectures,
        },
    )


if __name__ == "__main__":
    main()
