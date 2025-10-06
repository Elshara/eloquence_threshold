"""Smoke tests for command-line catalogue tooling."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = REPO_ROOT / "assets" / "py"
ASSET_JSON_DIR = REPO_ROOT / "assets" / "json"
MANIFEST_PATH = REPO_ROOT / "assets" / "ini" / "manifest.ini"
VALIDATED_NVDA_PATH = ASSET_JSON_DIR / "validated_nvda_builds.json"
SNAPSHOT_PATH = ASSET_JSON_DIR / "download_nvaccess_snapshot.json"


class CliReportTests(unittest.TestCase):
    maxDiff = None

    def _run_tool(self, script_name: str, *args: str) -> subprocess.CompletedProcess:
        script_path = TOOLS_DIR / script_name
        python_path = [str(TOOLS_DIR)]
        existing = os.environ.get("PYTHONPATH")
        if existing:
            python_path.append(existing)
        return subprocess.run(
            (sys.executable, str(script_path), *args),
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            cwd=str(REPO_ROOT),
            env={**os.environ, "PYTHONPATH": os.pathsep.join(python_path)},
        )

    def test_report_voice_parameters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp, "voice_parameters.json")
            md_path = Path(tmp, "voice_parameters.md")
            result = self._run_tool(
                "report_voice_parameters.py",
                "--json",
                str(json_path),
                "--markdown",
                str(md_path),
            )
            self.assertEqual(result.returncode, 0)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("parameterRanges", payload)
            self.assertTrue(md_path.read_text(encoding="utf-8").strip())

    def test_report_voice_frequency_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp, "voice_frequency.json")
            md_path = Path(tmp, "voice_frequency.md")
            result = self._run_tool(
                "report_voice_frequency_matrix.py",
                "--json",
                str(json_path),
                "--markdown",
                str(md_path),
                "--print",
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("parameters", payload)
            self.assertGreater(payload.get("parameterCount", 0), 0)
            self.assertTrue(md_path.read_text(encoding="utf-8").strip())

    def test_report_catalog_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp, "catalog_status.json")
            md_path = Path(tmp, "catalog_status.md")
            result = self._run_tool(
                "report_catalog_status.py",
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
                "validate_language_pronunciations.py",
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
                "check_nvda_updates.py",
                "--snapshot",
                str(SNAPSHOT_PATH),
                "--validated",
                str(VALIDATED_NVDA_PATH),
                "--manifest",
                str(MANIFEST_PATH),
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
                "report_language_coverage.py",
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
                "report_phoneme_fallbacks.py",
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
                "report_language_progress.py",
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
                "summarize_language_assets.py",
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
                "report_language_maturity.py",
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
            snapshot_source.write_text(SNAPSHOT_PATH.read_text(encoding="utf-8"), encoding="utf-8")

            snapshot_json = Path(tmp, "snapshot.json")
            snapshot_md = Path(tmp, "snapshot.md")
            recommendations_json = Path(tmp, "recommendations.json")
            recommendations_md = Path(tmp, "recommendations.md")
            delta_json = Path(tmp, "delta.json")
            delta_md = Path(tmp, "delta.md")

            result = self._run_tool(
                "run_nvda_release_checks.py",
                "--snapshot-source",
                str(snapshot_source),
                "--manifest",
                str(MANIFEST_PATH),
                "--validated",
                str(VALIDATED_NVDA_PATH),
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
