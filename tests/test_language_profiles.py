from __future__ import annotations

import unittest

import language_profiles


class LanguageProfileParsingTests(unittest.TestCase):
    def test_parse_character_entry_trims_whitespace_tokens(self) -> None:
        entry = {
            "symbol": "ß",
            "ipa": ["  s  ", "\tz  ", "", None],
            "notes": ["  note  ", "   ", "\nextra\n"],
        }
        parsed = language_profiles._parse_character_entry(entry)
        self.assertIsNotNone(parsed, "Expected character entry to be parsed")
        if parsed is None:
            return
        self.assertEqual(parsed.ipa, ("s", "z"))
        self.assertEqual(parsed.notes, ("note", "extra"))

    def test_parse_character_entry_splits_list_string_tokens(self) -> None:
        entry = {
            "symbol": "ç",
            "ipa": ["  t\tʃ", "d\u00a0ʒ  "],
        }
        parsed = language_profiles._parse_character_entry(entry)
        self.assertIsNotNone(parsed)
        if parsed is None:
            return
        self.assertEqual(parsed.ipa, ("t", "ʃ", "d", "ʒ"))

    def test_parse_character_entry_splits_string_whitespace(self) -> None:
        entry = {
            "symbol": "ç",
            "ipa": "  t\tʃ\n d\u00a0ʒ  ",
        }
        parsed = language_profiles._parse_character_entry(entry)
        self.assertIsNotNone(parsed)
        if parsed is None:
            return
        self.assertEqual(parsed.ipa, ("t", "ʃ", "d", "ʒ"))

    def test_parse_character_entry_trims_optional_fields(self) -> None:
        entry = {
            "symbol": "ø",
            "spoken": "  vowel  ",
            "description": "  front vowel   with rounding  ",
            "example": "  Før  ",
            "stress": "  carries stress \n in closed syllables  ",
        }
        parsed = language_profiles._parse_character_entry(entry)
        self.assertIsNotNone(parsed)
        if parsed is None:
            return
        self.assertEqual(parsed.spoken, "vowel")
        self.assertEqual(parsed.description, "front vowel with rounding")
        self.assertEqual(parsed.example, "Før")
        self.assertEqual(parsed.stress, "carries stress in closed syllables")

    def test_tuple_from_field_normalises_strings(self) -> None:
        self.assertEqual(language_profiles._tuple_from_field("  value  "), ("value",))
        self.assertEqual(
            language_profiles._tuple_from_field([" a ", "", "b", "  "]),
            ("a", "b"),
        )
        self.assertEqual(
            language_profiles._tuple_from_field("  spaced\nnotes  with\tmixed\x0cspace  "),
            ("spaced notes with mixed space",),
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
