from __future__ import annotations

import unittest
from pathlib import Path

import language_profiles
import resource_paths


class WikipediaLanguageIndexTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.index_path = Path(resource_paths.wikipedia_index_path())

    def test_index_file_exists(self) -> None:
        self.assertTrue(self.index_path.exists(), "Expected cached language index")

    def test_grouped_categories_present(self) -> None:
        grouped = language_profiles.load_wikipedia_language_index(str(self.index_path))
        for key in ("language", "dialect", "accent", "sign-language", "orthography"):
            self.assertIn(key, grouped)
            self.assertIsInstance(grouped[key], list)

    def test_entries_have_required_fields(self) -> None:
        grouped = language_profiles.load_wikipedia_language_index(str(self.index_path))
        total_entries = sum(len(values) for values in grouped.values())
        self.assertGreater(total_entries, 0, "Expected the index to contain language metadata")
        for entries in grouped.values():
            for entry in entries[:10]:
                self.assertIn("title", entry)
                self.assertIn("url", entry)
                self.assertIn("breadcrumbs", entry)
                self.assertIn("tags", entry)

    def test_augmented_tags_present(self) -> None:
        grouped = language_profiles.load_wikipedia_language_index(str(self.index_path))
        for tag in ("family", "constructed", "programming-language", "standard"):
            self.assertIn(tag, grouped)
            self.assertGreater(
                len(grouped[tag]),
                0,
                f"Expected at least one entry tagged '{tag}'",
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
