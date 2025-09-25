"""Data integrity checks for bundled catalogues."""
from __future__ import annotations

import unittest

from phoneme_catalog import load_default_inventory
from voice_catalog import load_default_voice_catalog
from language_profiles import load_default_language_profiles


class VoiceCatalogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = load_default_voice_catalog()

    def test_catalog_is_not_empty(self) -> None:
        self.assertFalse(self.catalog.is_empty, "Voice catalog should include bundled templates")

    def test_templates_respect_parameter_ranges(self) -> None:
        for template in self.catalog:
            with self.subTest(template=template.id):
                for name, value in template.parameter_items():
                    range_info = self.catalog.parameter_range(name)
                    self.assertIsNotNone(range_info, f"Missing parameter range for {name}")
                    if range_info is None:
                        continue
                    self.assertGreaterEqual(value, range_info.minimum)
                    self.assertLessEqual(value, range_info.maximum)

    def test_parameter_ranges_have_consistent_steps(self) -> None:
        for name, range_info in self.catalog.parameter_ranges().items():
            with self.subTest(parameter=name):
                self.assertGreaterEqual(range_info.step, 1)
                span = range_info.maximum - range_info.minimum
                self.assertGreaterEqual(span, 0)
                clamped_default = range_info.clamp(range_info.default)
                self.assertGreaterEqual(clamped_default, range_info.minimum)
                self.assertLessEqual(clamped_default, range_info.maximum)


class PhonemeInventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.inventory = load_default_inventory()

    def test_inventory_is_not_empty(self) -> None:
        self.assertFalse(self.inventory.is_empty, "Phoneme inventory should not be empty")

    def test_every_category_has_phonemes(self) -> None:
        for category_id, label in self.inventory.categories.items():
            with self.subTest(category=label):
                phonemes = self.inventory.phonemes_for_category(category_id)
                self.assertTrue(phonemes, f"Category {label} should expose phonemes")

    def test_match_ipa_sequence_handles_known_symbols(self) -> None:
        category_id = self.inventory.default_category_id()
        if not category_id:
            self.skipTest("No default phoneme category available")
        phonemes = self.inventory.phonemes_for_category(category_id)
        sample_tokens = []
        for definition in phonemes:
            ipa_values = [symbol for symbol in definition.ipa if symbol]
            if not ipa_values:
                continue
            sample_tokens.append(ipa_values[0])
            if len(sample_tokens) >= 5:
                break
        if not sample_tokens:
            self.skipTest("Category lacks phonemes with IPA hints")
        sample = " ".join(sample_tokens)
        matches, remainder = self.inventory.match_ipa_sequence(sample)
        self.assertTrue(matches, "Expected at least one IPA match")
        self.assertEqual(remainder, "", "All IPA tokens in the sample should match known phonemes")


class LanguageProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = load_default_language_profiles()

    def test_catalog_is_not_empty(self) -> None:
        self.assertFalse(self.catalog.is_empty, "Language profile catalog should not be empty")

    def test_find_best_match_resolves_regional_variants(self) -> None:
        castilian = self.catalog.find_best_match("es-ES")
        mexican = self.catalog.find_best_match("es-MX")
        self.assertIsNotNone(castilian, "Expected a Castilian Spanish profile")
        self.assertIsNotNone(mexican, "Expected fallback for Mexican Spanish")
        if castilian and mexican:
            self.assertNotEqual(castilian.id, "", "Profiles must expose identifiers")
            self.assertNotEqual(mexican.id, "", "Profiles must expose identifiers")

    def test_profiles_offer_character_descriptions(self) -> None:
        for profile in self.catalog:
            if not profile.characters:
                continue
            sample_symbol = next(iter(profile.characters))
            details = profile.describe_characters(sample_symbol)
            self.assertTrue(details, "Expected describe_characters to return mappings")

    def test_profile_metrics_report_progress(self) -> None:
        inventory = load_default_inventory()
        for profile in self.catalog:
            metrics = profile.metrics(inventory)
            with self.subTest(profile=profile.id):
                self.assertIn("progressScore", metrics)
                self.assertGreaterEqual(metrics["progressScore"], 0.0)
                self.assertLessEqual(metrics["progressScore"], 1.0)
                self.assertIn("stage", metrics)
if __name__ == "__main__":
    unittest.main()
