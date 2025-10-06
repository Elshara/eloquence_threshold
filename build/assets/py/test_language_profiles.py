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

    def test_parse_character_entry_flattens_nested_tokens(self) -> None:
        entry = {
            "symbol": "  ŋ  ",
            "ipa": [" n ", ["  g"], (None, ("  ɡ  ", [" ʔ "]))],
            "notes": ("  nasal  ", ("  velar ", None)),
        }
        parsed = language_profiles._parse_character_entry(entry)
        self.assertIsNotNone(parsed)
        if parsed is None:
            return
        self.assertEqual(parsed.symbol, "ŋ")
        self.assertEqual(parsed.ipa, ("n", "g", "ɡ", "ʔ"))
        self.assertEqual(parsed.notes, ("nasal", "velar"))

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

    def test_parse_character_entry_requires_non_empty_symbol(self) -> None:
        entry = {"symbol": "   ", "ipa": "a"}
        parsed = language_profiles._parse_character_entry(entry)
        self.assertIsNone(parsed)

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

    def test_tuple_from_field_flattens_nested_sequences(self) -> None:
        self.assertEqual(
            language_profiles._tuple_from_field(["  a  ", [" b ", None], ("c", ("  d  ",))]),
            ("a", "b", "c", "d"),
        )

    def test_parse_language_profile_normalises_metadata(self) -> None:
        payload = {
            "id": "  nb-no  ",
            "language": "  Norwegian  Bokmål  ",
            "displayName": "  Norwegian  Bokmål  profile  ",
            "description": "  Regional  spelling   conventions  ",
            "tags": ["  nordic  ", ["  default "]],
            "characters": [
                {
                    "symbol": "  Å  ",
                    "ipa": [["  o  ː"], "  ɒ  "],
                    "notes": "  long  vowel  ",
                }
            ],
            "stress": [["  Primary  stress  "]],
            "sentenceStructure": ("  SVO  ", None),
            "grammar": [None, "  gendered  nouns  "],
            "defaultVoiceTemplates": ("  nb-eloquence  ", ["  nb-alt  "]),
        }
        profile = language_profiles._parse_language_profile(payload)
        self.assertIsNotNone(profile)
        if profile is None:
            return
        self.assertEqual(profile.id, "nb-no")
        self.assertEqual(profile.language, "Norwegian Bokmål")
        self.assertEqual(profile.display_name, "Norwegian Bokmål profile")
        self.assertEqual(profile.description, "Regional spelling conventions")
        self.assertEqual(profile.tags, ("nordic", "default"))
        self.assertEqual(profile.stress_notes, ("Primary stress",))
        self.assertEqual(profile.sentence_structure, ("SVO",))
        self.assertEqual(profile.grammar_notes, ("gendered nouns",))
        self.assertEqual(profile.default_voice_templates, ("nb-eloquence", "nb-alt"))
        self.assertIn("Å", profile.characters)
        parsed_character = profile.characters["Å"]
        self.assertEqual(parsed_character.symbol, "Å")
        self.assertEqual(parsed_character.ipa, ("o", "ː", "ɒ"))
        self.assertEqual(parsed_character.notes, ("long vowel",))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
