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

    def test_report_language_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp, "language_coverage.json")
            md_path = Path(tmp, "language_coverage.md")
            result = self._run_tool(
                "tools/report_language_coverage.py",
                "--json",
                str(json_path),
                "--markdown",
                str(md_path),
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("entries", payload)
            self.assertGreaterEqual(payload["totalEntries"], 1)
            self.assertTrue(md_path.read_text(encoding="utf-8").strip())

    def test_report_phoneme_fallbacks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp, "phoneme_fallbacks.json")
            md_path = Path(tmp, "phoneme_fallbacks.md")
            result = self._run_tool(
                "tools/report_phoneme_fallbacks.py",
                "--json",
                str(json_path),
                "--markdown",
                str(md_path),
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("profiles", payload)
            self.assertIn("metadata", payload)
            self.assertTrue(md_path.read_text(encoding="utf-8").strip())

    def test_report_language_progress(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp, "language_progress.json")
            md_path = Path(tmp, "language_progress.md")
            result = self._run_tool(
                "tools/report_language_progress.py",
                "--json",
                str(json_path),
                "--markdown",
                str(md_path),
                "--print",
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("entries", payload)
            self.assertIn("stats", payload)
            self.assertGreaterEqual(payload.get("totalProfiles", 0), 0)
            self.assertTrue(md_path.read_text(encoding="utf-8").strip())

    def test_summarize_language_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp, "language_assets.json")
            md_path = Path(tmp, "language_assets.md")
            result = self._run_tool(
                "tools/summarize_language_assets.py",
                "--json",
                str(json_path),
                "--markdown",
                str(md_path),
                "--print",
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("languages", payload)
            self.assertIn("globalStats", payload)
            self.assertIn("globalResearch", payload)
            self.assertGreaterEqual(len(payload["languages"]), 1)
            self.assertTrue(md_path.read_text(encoding="utf-8").strip())

    def test_report_language_maturity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp, "language_maturity.json")
            md_path = Path(tmp, "language_maturity.md")
            result = self._run_tool(
                "tools/report_language_maturity.py",
                "--json",
                str(json_path),
                "--markdown",
                str(md_path),
                "--print",
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("entries", payload)
            self.assertIn("stageCounts", payload)
            self.assertIn("coverageStatusCounts", payload)
            self.assertTrue(md_path.read_text(encoding="utf-8").strip())

    def test_run_nvda_release_checks_from_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            snapshot_source = Path(tmp, "source_snapshot.json")
            snapshot_source.write_text(Path("docs/download_nvaccess_snapshot.json").read_text(encoding="utf-8"), encoding="utf-8")

            snapshot_json = Path(tmp, "snapshot.json")
            snapshot_md = Path(tmp, "snapshot.md")
            recommendations_json = Path(tmp, "recommendations.json")
            recommendations_md = Path(tmp, "recommendations.md")
            delta_json = Path(tmp, "delta.json")
            delta_md = Path(tmp, "delta.md")

            result = self._run_tool(
                "tools/run_nvda_release_checks.py",
                "--snapshot-source",
                str(snapshot_source),
                "--manifest",
                "manifest.ini",
                "--validated",
                "docs/validated_nvda_builds.json",
                "--snapshot-json",
                str(snapshot_json),
                "--snapshot-markdown",
                str(snapshot_md),
                "--recommendations-json",
                str(recommendations_json),
                "--recommendations-markdown",
                str(recommendations_md),
                "--previous-snapshot",
                str(snapshot_source),
                "--delta-json",
                str(delta_json),
                "--delta-markdown",
                str(delta_md),
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)

            snapshot_payload = json.loads(snapshot_json.read_text(encoding="utf-8"))
            self.assertIn("entries", snapshot_payload)
            self.assertTrue(snapshot_payload["entries"])

            recommendations_payload = json.loads(recommendations_json.read_text(encoding="utf-8"))
            self.assertIn("entries", recommendations_payload)
            self.assertTrue(recommendations_payload["entries"])

            delta_payload = json.loads(delta_json.read_text(encoding="utf-8"))
            self.assertIn("differences", delta_payload)


if __name__ == "__main__":
    unittest.main()
