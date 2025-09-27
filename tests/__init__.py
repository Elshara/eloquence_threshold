"""Test suite for the Eloquence Threshold project.

This package now ensures that every invocation of the unit test suite
attempts to build the ``eloquence.nvda-addon`` bundle so regressions in
the packaging pipeline are caught alongside the regular tests.
"""

from __future__ import annotations

import datetime
import pathlib
import subprocess
import sys


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
ADDON_NAME = "eloquence.nvda-addon"


def _run_addon_build() -> None:
    """Invoke the build helper before the rest of the tests import."""

    build_script = PROJECT_ROOT / "build.py"
    if not build_script.exists():
        return

    command = [sys.executable, str(build_script), "--insecure"]
    try:
        subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as error:
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        raise RuntimeError(
            f"Failed to build {ADDON_NAME} at {timestamp}: {error.stderr.decode('utf-8', 'replace')}"
        ) from error


_run_addon_build()

