from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import speechdata_listing


class SpeechdataListingTests(unittest.TestCase):
    def test_discover_entries_orders_results(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "eloquence" / "dll").mkdir(parents=True)
            (root / "eloquence" / "dll" / "eci.dll").write_bytes(b"dll")
            (root / "eloquence" / "syn").mkdir()
            (root / "eloquence" / "syn" / "voice.syn").write_bytes(b"syn")
            (root / "README").write_text("notes", encoding="utf-8")

            entries = speechdata_listing.discover_entries(root, max_depth=2)

        self.assertEqual(
            entries,
            [
                "README",
                "eloquence",
                "eloquence/dll",
                "eloquence/dll/eci.dll",
                "eloquence/syn",
                "eloquence/syn/voice.syn",
            ],
        )

    def test_discover_entries_clamps_depth(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "eloquence" / "dll").mkdir(parents=True)
            (root / "eloquence" / "dll" / "eci.dll").write_bytes(b"dll")

            entries = speechdata_listing.discover_entries(root, max_depth=0)

        self.assertEqual(entries, ["eloquence"])

    def test_summarise_entries_reports_file_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "eloquence" / "dll").mkdir(parents=True)
            dll_path = root / "eloquence" / "dll" / "eci.dll"
            dll_path.write_bytes(b"dll")
            readme = root / "README"
            readme.write_text("notes", encoding="utf-8")

            entries = ["eloquence", "eloquence/dll", "eloquence/dll/eci.dll", "README"]
            summary = speechdata_listing.summarise_entries(entries, root=root)

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

    def test_build_inventory_summarises_extension_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "eloquence" / "dll").mkdir(parents=True)
            (root / "eloquence" / "dll" / "eci.dll").write_bytes(b"dll")
            (root / "eloquence" / "syn").mkdir()
            (root / "eloquence" / "syn" / "voice.syn").write_bytes(b"syn")

            inventory = speechdata_listing.build_inventory(root, max_depth=2)

        self.assertIn("eloquence/dll", inventory)
        dll_info = inventory["eloquence/dll"]
        self.assertEqual(dll_info["total_files"], 1)
        self.assertEqual(dll_info["extensionless_files"], 0)
        self.assertEqual(dll_info["extensions"], {".dll": 1})

    def test_summarise_inventory_totals(self) -> None:
        inventory = {
            "eloquence/dll": {
                "total_files": 1,
                "extensionless_files": 0,
                "extensions": {".dll": 1},
            },
            "eloquence/syn": {
                "total_files": 2,
                "extensionless_files": 1,
                "extensions": {".syn": 1},
            },
        }

        totals = speechdata_listing.summarise_inventory_totals(inventory)

        self.assertEqual(totals["directories"], 2)
        self.assertEqual(totals["total_files"], 3)
        self.assertEqual(totals["extensionless_files"], 1)
        self.assertEqual(totals["extensions"], {".dll": 1, ".syn": 1})


if __name__ == "__main__":  # pragma: no cover - unittest main hook
    unittest.main()
