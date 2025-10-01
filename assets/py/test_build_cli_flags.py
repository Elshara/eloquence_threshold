from __future__ import annotations

import io
import json
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

        with mock.patch.object(sys, "stderr", io.StringIO()):
            with self.assertRaises(SystemExit):
                build.parse_args(["--list-speechdata-output", "report.json"])

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

    def test_summarise_speechdata_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            speechdata_root = Path(tmpdir)
            (speechdata_root / "eloquence" / "dll").mkdir(parents=True)
            dll = speechdata_root / "eloquence" / "dll" / "eci.dll"
            dll.write_bytes(b"dll")
            doc = speechdata_root / "README"
            doc.write_text("notes", encoding="utf-8")

            entries = ["eloquence", "eloquence/dll", "eloquence/dll/eci.dll", "README"]
            summary = build.summarise_speechdata_entries(entries, root=speechdata_root)

        summary_by_path = {item["path"]: item for item in summary}
        self.assertEqual(summary_by_path["eloquence"]["kind"], "directory")
        self.assertIn("children", summary_by_path["eloquence"])
        dll_entry = summary_by_path["eloquence/dll/eci.dll"]
        self.assertEqual(dll_entry["kind"], "file")
        self.assertEqual(dll_entry["extension"], "dll")
        self.assertFalse(dll_entry["extensionless"])
        readme_entry = summary_by_path["README"]
        self.assertEqual(readme_entry["kind"], "file")
        self.assertTrue(readme_entry["extensionless"])

    def test_list_speechdata_output_creates_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            speechdata_root = Path(tmpdir, "speechdata")
            (speechdata_root / "eloquence" / "dll").mkdir(parents=True)
            (speechdata_root / "eloquence" / "dll" / "eci.dll").write_bytes(b"dll")
            output_path = Path(tmpdir, "report.json")

            argv = [
                "build.py",
                "--list-speechdata",
                "--list-speechdata-depth",
                "2",
                "--list-speechdata-output",
                str(output_path),
            ]
            with mock.patch.object(sys, "argv", argv):
                with mock.patch.object(build.resource_paths, "speechdata_root", return_value=speechdata_root):
                    with mock.patch.object(sys, "stdout", new=io.StringIO()):
                        build.main()

            data = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertTrue(data["root_exists"])
        self.assertEqual(data["max_depth"], 2)
        discovered_paths = [entry["path"] for entry in data["entries"]]
        self.assertIn("eloquence", discovered_paths)
        self.assertIn("eloquence/dll/eci.dll", discovered_paths)


if __name__ == "__main__":  # pragma: no cover - unittest main hook
    unittest.main()
