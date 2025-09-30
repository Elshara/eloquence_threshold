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
``assets/dll`` and the accompanying ``*.syn`` voices live in ``assets/syn``
before packaging the add-on.
"""

from __future__ import annotations

import argparse
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
from typing import Dict, Iterable, Optional, Tuple

import resource_paths

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


def _contains_eci_dll(path: Path) -> bool:
    if not path.is_dir():
        return False
    for entry in path.iterdir():
        if entry.name.lower() == "eci.dll":
            return True
    return False


def has_runtime_assets() -> bool:
    """Return ``True`` if any staged directory exposes ``eci.dll``."""

    for candidate in resource_paths.eloquence_library_roots():
        if _contains_eci_dll(candidate):
            return True
    return False

ARCH_DIRECTORIES: Tuple[Tuple[str, Path, str], ...] = (
    ("eloquence_x86", Path("synthDrivers") / "eloquence" / "x86", "Embedded 32-bit runtime from ./eloquence_x86"),
    ("eloquence_x64", Path("synthDrivers") / "eloquence" / "x64", "Embedded 64-bit runtime from ./eloquence_x64"),
    ("eloquence_arm32", Path("synthDrivers") / "eloquence" / "arm32", "Embedded 32-bit ARM runtime from ./eloquence_arm32"),
    ("eloquence_arm64", Path("synthDrivers") / "eloquence" / "arm64", "Embedded 64-bit ARM runtime from ./eloquence_arm64"),
    ("eloquence_arm", Path("synthDrivers") / "eloquence" / "arm", "Embedded ARM runtime from ./eloquence_arm"),
)


def parse_args() -> argparse.Namespace:
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
    return parser.parse_args()


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
        return path
    if not allow_download:
        return None
    try:
        _validate_template_url(url)
    except ValueError as error:
        print(f"Warning: {error}")
        return None
    try:
        print(f"Downloading template from {url}…")
        context = ssl._create_unverified_context() if insecure else None
        with urllib.request.urlopen(url, context=context) as response:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("wb") as handle:
                shutil.copyfileobj(response, handle)
        return path
    except (OSError, urllib.error.URLError, ValueError) as exc:
        print(f"Warning: unable to download template: {exc}")
    return None


def stage_template(staging_dir: Path, template: Optional[Path]) -> bool:
    """Extract ``template`` into ``staging_dir`` if provided."""

    if template is None:
        (staging_dir / "synthDrivers").mkdir(parents=True, exist_ok=True)
        return False
    with zipfile.ZipFile(template, "r") as archive:
        archive.extractall(staging_dir)
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
        return False
    if dest.exists() and not preserve_existing:
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest, dirs_exist_ok=preserve_existing)
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


def stage_root_files(staging_dir: Path) -> None:
    for src, relative_dest in ROOT_FILES:
        copy_file(src, staging_dir / relative_dest)


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
    for asset_path in iter_asset_directories():
        destination = dest_root / asset_path.name
        if asset_path.is_dir():
            copy_optional_directory(asset_path, destination, preserve_existing=False)
            copied_any = True
        elif asset_path.is_file():
            copy_file(asset_path, destination)
            copied_any = True
    return copied_any


def stage_speechdata_tree(staging_dir: Path) -> bool:
    speechdata_root = resource_paths.speechdata_root()
    if not speechdata_root.is_dir():
        return False
    return copy_optional_directory(
        speechdata_root,
        staging_dir / "speechdata",
        preserve_existing=False,
    )


def write_archive(staging_dir: Path, output: Path) -> None:
    if output.exists():
        output.unlink()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(staging_dir.rglob("*")):
            if not path.is_file():
                continue
            arcname = path.relative_to(staging_dir).as_posix()
            archive.write(path, arcname)


def main() -> None:
    args = parse_args()
    _validate_template_url(str(args.template_url))
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
        speechdata_copied = stage_speechdata_tree(staging_dir)

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

        if speechdata_copied:
            print("Bundled speechdata directory for extensionless resources")

        if legacy_data_copied:
            print("Bundled legacy eloquence_data directory")

        if legacy_runtime_copied:
            print("Embedded legacy Eloquence runtime from ./eloquence")
        elif not template_used and not has_runtime_assets():
            print(
                "Warning: no Eloquence runtime detected. Stage eci.dll inside assets/dll "
                "and copy .syn voices into assets/syn before installing the add-on."
            )
        for notice in copied_architectures:
            print(notice)

        write_archive(staging_dir, args.output.expanduser().resolve())

    print(f"Created {args.output}")


if __name__ == "__main__":
    main()
