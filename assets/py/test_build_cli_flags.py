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

        with mock.patch.object(sys, "stderr", io.StringIO()):
            with self.assertRaises(SystemExit):
                build.parse_args(["--list-speechdata-depth", "0"])

    def test_parse_args_accepts_list_flags(self) -> None:
        args = build.parse_args(["--list-speechdata", "--list-speechdata-depth", "3"])
        self.assertTrue(args.list_speechdata)
        self.assertEqual(args.list_speechdata_depth, 3)

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

    def test_discover_speechdata_subtrees_orders_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            speechdata_root = Path(tmpdir, "speechdata")
            (speechdata_root / "eloquence" / "dll").mkdir(parents=True)
            (speechdata_root / "eloquence" / "dll" / "eci.dll").write_bytes(b"dll")
            (speechdata_root / "eloquence" / "syn").mkdir(parents=True)
            (speechdata_root / "eloquence" / "syn" / "voice.syn").write_bytes(b"syn")
            (speechdata_root / "nv_speech_player").mkdir()
            (speechdata_root / "nv_speech_player" / "nvSpeechPlayer.dll").write_bytes(b"np")
            (speechdata_root / "README").write_text("notes", encoding="utf-8")

            with mock.patch.object(
                build.resource_paths,
                "speechdata_root",
                return_value=speechdata_root,
            ):
                entries = build.discover_speechdata_subtrees(max_depth=2)

        self.assertEqual(
            entries,
            [
                "README",
                "eloquence",
                "eloquence/dll",
                "eloquence/dll/eci.dll",
                "eloquence/syn",
                "eloquence/syn/voice.syn",
                "nv_speech_player",
                "nv_speech_player/nvSpeechPlayer.dll",
            ],
        )

    def test_discover_speechdata_subtrees_respects_depth(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            speechdata_root = Path(tmpdir, "speechdata")
            (speechdata_root / "eloquence" / "dll").mkdir(parents=True)
            (speechdata_root / "eloquence" / "dll" / "eci.dll").write_bytes(b"dll")

            with mock.patch.object(
                build.resource_paths,
                "speechdata_root",
                return_value=speechdata_root,
            ):
                entries = build.discover_speechdata_subtrees(max_depth=1)

        self.assertEqual(entries, ["eloquence"])

    def test_discover_speechdata_subtrees_handles_missing_root(self) -> None:
        with mock.patch.object(
            build.resource_paths,
            "speechdata_root",
            return_value=Path("/missing"),
        ):
            entries = build.discover_speechdata_subtrees(max_depth=2)

        self.assertEqual(entries, [])


if __name__ == "__main__":  # pragma: no cover - unittest main hook
    unittest.main()
