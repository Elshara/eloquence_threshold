from __future__ import annotations

import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import build


class BuildCliFlagTests(unittest.TestCase):
    def test_parse_args_normalises_subtrees(self) -> None:
        args = build.parse_args(
            [
                "--speechdata-subtree",
                "./eloquence/dll/",
                "--speechdata-subtree",
                "speechdata/eloquence/syn",
                "--speechdata-subtree",
                "eloquence\\syn",
            ]
        )
        self.assertEqual(
            args.speechdata_subtree,
            ["eloquence/dll", "eloquence/syn"],
        )

    def test_parse_args_rejects_invalid_combinations(self) -> None:
        with mock.patch.object(sys, "stderr", io.StringIO()):
            with self.assertRaises(SystemExit):
                build.parse_args(["--no-speechdata", "--speechdata-subtree", "eloquence/dll"])

        with mock.patch.object(sys, "stderr", io.StringIO()):
            with self.assertRaises(SystemExit):
                build.parse_args(["--speechdata-subtree", "/absolute/path"])

    def test_stage_speechdata_tree_subset(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            speechdata_root = Path(tmpdir, "speechdata")
            dll_root = speechdata_root / "eloquence" / "dll"
            syn_root = speechdata_root / "eloquence" / "syn"
            dll_root.mkdir(parents=True)
            syn_root.mkdir(parents=True)
            (dll_root / "eci.dll").write_bytes(b"binary")
            (syn_root / "voice.syn").write_bytes(b"voice")

            staging_dir = Path(tmpdir, "staging")
            staging_dir.mkdir()

            with mock.patch.object(
                build.resource_paths,
                "speechdata_root",
                return_value=speechdata_root,
            ):
                copied, details = build.stage_speechdata_tree(
                    staging_dir,
                    subtrees=["eloquence/dll", "eloquence/syn"],
                )

            self.assertTrue(copied)
            self.assertEqual(details["mode"], "subset")
            self.assertCountEqual(details["included"], ["eloquence/dll", "eloquence/syn"])
            self.assertFalse(details["missing"])
            self.assertTrue((staging_dir / "speechdata" / "eloquence" / "dll" / "eci.dll").exists())
            self.assertTrue((staging_dir / "speechdata" / "eloquence" / "syn" / "voice.syn").exists())

    def test_stage_speechdata_tree_handles_missing_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            staging_dir = Path(tmpdir, "stage")
            staging_dir.mkdir()

            with mock.patch.object(
                build.resource_paths,
                "speechdata_root",
                return_value=Path(tmpdir, "missing"),
            ):
                copied, details = build.stage_speechdata_tree(
                    staging_dir,
                    subtrees=["eloquence/dll", "eloquence/syn"],
                )

        self.assertFalse(copied)
        self.assertEqual(details["mode"], "missing")
        self.assertCountEqual(details["missing"], ["eloquence/dll", "eloquence/syn"])

    def test_stage_speechdata_tree_skip(self) -> None:
        copied, details = build.stage_speechdata_tree(Path("unused"), skip=True, subtrees=["foo"])
        self.assertFalse(copied)
        self.assertEqual(details["mode"], "skipped")
        self.assertEqual(details["missing"], ["foo"])


if __name__ == "__main__":  # pragma: no cover - unittest main hook
    unittest.main()
