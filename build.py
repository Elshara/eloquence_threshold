"""Convenience wrapper for the add-on packaging helper.

The primary build logic lives in ``assets/py/build.py`` so the module ships
alongside other developer tooling.  Documentation and automation workflows,
however, still invoke ``python build.py`` from the repository root.  This
wrapper loads the real script and forwards command-line arguments unchanged.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    builder = repo_root / "assets" / "py" / "build.py"
    if not builder.is_file():
        raise FileNotFoundError(
            "Expected build script at assets/py/build.py; the repository layout may be corrupt."
        )
    sys.argv[0] = str(builder)
    sys.path.insert(0, str(builder.parent))
    runpy.run_path(str(builder), run_name="__main__")


if __name__ == "__main__":
    main()
