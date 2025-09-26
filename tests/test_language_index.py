from __future__ import annotations

import os
import unittest

import language_profiles


class WikipediaLanguageIndexTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.index_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "docs",
            "wikipedia_language_index.json",
        )

    def test_index_file_exists(self) -> None:
        self.assertTrue(os.path.exists(self.index_path), "Expected cached language index")

    def test_grouped_categories_present(self) -> None:
        grouped = language_profiles.load_wikipedia_language_index(self.index_path)
        for key in ("language", "dialect", "accent", "sign-language", "orthography"):
            self.assertIn(key, grouped)
            self.assertIsInstance(grouped[key], list)

    def test_entries_have_required_fields(self) -> None:
        grouped = language_profiles.load_wikipedia_language_index(self.index_path)
        total_entries = sum(len(values) for values in grouped.values())
        self.assertGreater(total_entries, 0, "Expected the index to contain language metadata")
        for entries in grouped.values():
            for entry in entries[:10]:
                self.assertIn("title", entry)
                self.assertIn("url", entry)
                self.assertIn("breadcrumbs", entry)
                self.assertIn("tags", entry)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
