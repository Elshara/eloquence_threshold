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
created purely from the Python modules and data files in this repository, which
means you must copy ``eci.dll`` and the ``*.syn`` voice data into the
``eloquence`` directory yourself before installing the add-on.
"""

from __future__ import annotations

import argparse
import os
import shutil
import ssl
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional, Tuple

if sys.version_info < (3, 8):
    raise RuntimeError("Python 3.8 or newer is required to build the add-on")


REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = REPO_ROOT / "eloquence.nvda-addon"
DEFAULT_TEMPLATE = REPO_ROOT / "eloquence_original.nvda-addon"
TEMPLATE_URL = (
    "https://github.com/pumper42nickel/eloquence_threshold/releases/download/"
    "v0.20210417.01/eloquence.nvda-addon"
)

FILES_TO_COPY: Tuple[Tuple[str, Path], ...] = (
    ("_eloquence.py", Path("synthDrivers") / "_eloquence.py"),
    ("eloquence.py", Path("synthDrivers") / "eloquence.py"),
    ("phoneme_catalog.py", Path("synthDrivers") / "phoneme_catalog.py"),
    ("voice_catalog.py", Path("synthDrivers") / "voice_catalog.py"),
    ("language_profiles.py", Path("synthDrivers") / "language_profiles.py"),
    ("manifest.ini", Path("manifest.ini")),
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


def ensure_template(
    path: Path, *, url: str, allow_download: bool, insecure: bool
) -> Optional[Path]:
    """Return ``path`` if it exists, otherwise attempt to download it."""

    if path.is_file():
        return path
    if not allow_download:
        return None
    try:
        print(f"Downloading template from {url}…")
        context = ssl._create_unverified_context() if insecure else None
        with urllib.request.urlopen(url, context=context) as response:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("wb") as handle:
                shutil.copyfileobj(response, handle)
        return path
    except (OSError, urllib.error.URLError) as exc:
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
    template_path = ensure_template(
        args.template.expanduser().resolve(),
        url=args.template_url,
        allow_download=not args.no_download,
        insecure=args.insecure,
    )

    with tempfile.TemporaryDirectory(prefix="eloquence_build_") as tmpdir:
        staging_dir = Path(tmpdir)
        template_used = stage_template(staging_dir, template_path)

        for source_name, relative_dest in FILES_TO_COPY:
            copy_file(REPO_ROOT / source_name, staging_dir / relative_dest)

        data_copied = copy_optional_directory(
            REPO_ROOT / "eloquence_data",
            staging_dir / "synthDrivers" / "eloquence_data",
            preserve_existing=False,
        )
        runtime_copied = copy_optional_directory(
            REPO_ROOT / "eloquence",
            staging_dir / "synthDrivers" / "eloquence",
            preserve_existing=True,
        )
        x64_copied = copy_optional_directory(
            REPO_ROOT / "eloquence_x64",
            staging_dir / "synthDrivers" / "eloquence" / "x64",
            preserve_existing=True,
        )

        if data_copied:
            print("Bundled eloquence_data directory")
        if runtime_copied:
            print("Embedded Eloquence runtime from ./eloquence")
        elif not template_used:
            print(
                "Warning: no Eloquence runtime detected. Copy ECI DLLs and .syn files "
                "into ./eloquence before installing the add-on."
            )
        if x64_copied:
            print("Embedded 64-bit Eloquence payload from ./eloquence_x64")

        write_archive(staging_dir, args.output.expanduser().resolve())

    print(f"Created {args.output}")


if __name__ == "__main__":
    main()
