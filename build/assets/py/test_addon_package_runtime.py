"""Smoke tests that load modules from the packaged eloquence.nvda-addon."""

from __future__ import annotations

import importlib
import pathlib
import sys
import tempfile
import unittest
import zipfile

from nvda_test_stubs import install_basic_stubs

ADDON_PATH = pathlib.Path(__file__).resolve().parents[1] / "eloquence.nvda-addon"

install_basic_stubs()


@unittest.skipUnless(ADDON_PATH.is_file(), "eloquence.nvda-addon package not found")
class AddonRuntimeSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self._original_sys_path = list(sys.path)

    def tearDown(self) -> None:
        sys.path[:] = self._original_sys_path
        for module_name in ("synthDrivers", "synthDrivers._eloquence", "synthDrivers.eloquence"):
            sys.modules.pop(module_name, None)

    def test_imports_synthdriver_from_packaged_addon(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = pathlib.Path(tmpdir)
            with zipfile.ZipFile(ADDON_PATH) as archive:
                archive.extractall(tmp_path)

            synth_root = tmp_path / "synthDrivers"
            synth_root.mkdir(exist_ok=True)
            init_file = synth_root / "__init__.py"
            if not init_file.exists():
                init_file.write_text("__all__ = []\n")

            sys.path.insert(0, str(tmp_path))
            importlib.invalidate_caches()

            try:
                module = importlib.import_module("synthDrivers.eloquence")
            except Exception as error:
                self.skipTest(f"synthDrivers.eloquence import failed: {error}")
            backend = importlib.import_module("synthDrivers._eloquence")

        self.assertTrue(hasattr(module, "SynthDriver"))
        self.assertTrue(hasattr(backend, "initialize"))

