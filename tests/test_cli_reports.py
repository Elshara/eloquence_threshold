"""Smoke tests for command-line catalogue tooling."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliReportTests(unittest.TestCase):
    maxDiff = None

    def _run_tool(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            (sys.executable, *args),
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )

    def test_report_voice_parameters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp, "voice_parameters.json")
            md_path = Path(tmp, "voice_parameters.md")
            result = self._run_tool(
                "tools/report_voice_parameters.py",
                "--json",
                str(json_path),
                "--markdown",
                str(md_path),
            )
            self.assertEqual(result.returncode, 0)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("parameterRanges", payload)
            self.assertTrue(md_path.read_text(encoding="utf-8").strip())

    def test_report_catalog_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp, "catalog_status.json")
            md_path = Path(tmp, "catalog_status.md")
            result = self._run_tool(
                "tools/report_catalog_status.py",
                "--json",
                str(json_path),
                "--markdown",
                str(md_path),
            )
            self.assertEqual(result.returncode, 0)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("voices", payload)
            self.assertTrue(md_path.read_text(encoding="utf-8").strip())

    def test_validate_language_pronunciations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp, "pronunciation_report.json")
            md_path = Path(tmp, "pronunciation_report.md")
            result = self._run_tool(
                "tools/validate_language_pronunciations.py",
                "--json",
                str(json_path),
                "--markdown",
                str(md_path),
            )
            self.assertIn(result.returncode, {0, 1})
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("profiles", payload)
            self.assertTrue(md_path.read_text(encoding="utf-8").strip())
            self.assertIn("stats", payload)

    def test_check_nvda_updates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp, "nvda_updates.json")
            md_path = Path(tmp, "nvda_updates.md")
            result = self._run_tool(
                "tools/check_nvda_updates.py",
                "--snapshot",
                "docs/download_nvaccess_snapshot.json",
                "--validated",
                "docs/validated_nvda_builds.json",
                "--manifest",
                "manifest.ini",
                "--json",
                str(json_path),
                "--markdown",
                str(md_path),
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("entries", payload)
            self.assertTrue(payload["entries"])
            self.assertTrue(md_path.read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    unittest.main()
