import unittest

from tools import catalog_datajake_archives as archive_catalog


class ArchiveCatalogDetectionTests(unittest.TestCase):
    def test_detect_extension_handles_compressed_tarballs(self) -> None:
        self.assertEqual(archive_catalog.detect_extension("voices.tar.gz"), "tar.gz")
        self.assertEqual(archive_catalog.detect_extension("dataset.TGZ"), "tar.gz")

    def test_parse_sample_rate_handles_decimals_and_underscores(self) -> None:
        self.assertEqual(archive_catalog.parse_sample_rate("voice_44.1khz"), 44100)
        self.assertEqual(archive_catalog.parse_sample_rate("voice_48_khz"), 48000)

    def test_classify_document_stub_without_extension(self) -> None:
        record = archive_catalog.classify("https://example.com/tts/test/readme")
        self.assertEqual(record.category, "Documentation")
        self.assertEqual(record.viability, "Scrap (reference only)")

    def test_classify_phoneme_archive_marks_high_priority(self) -> None:
        record = archive_catalog.classify(
            "https://mirror/tts/espeak/espeak_english_phoneme_pack_16khz.zip"
        )
        self.assertEqual(record.category, "Voice/data archive")
        self.assertEqual(record.viability, "High – prioritise phoneme or lexicon data")
        self.assertEqual(record.metadata.get("sample_rate_hz"), 16000)
        self.assertIn("English", record.metadata.get("language_hints", []) or [])
        self.assertIn(
            "phoneme_or_lexicon",
            record.metadata.get("priority_tags", []),
        )

    def test_extract_voice_hint_prefers_named_variants(self) -> None:
        hint = archive_catalog.extract_voice_hint("Voice Eloquence Dectalk 22kHz.exe")
        self.assertEqual(hint, "Eloquence")

    def test_dictionary_extension_receives_dataset_priority(self) -> None:
        record = archive_catalog.classify(
            "https://mirror/tts/dectalk/pronunciations/custom.dic"
        )
        self.assertEqual(record.category, "Voice/data archive")
        self.assertEqual(
            record.viability, "High – prioritise phoneme or lexicon data"
        )
        self.assertIn(
            "phoneme_or_lexicon", record.metadata.get("priority_tags", [])
        )

    def test_nvda_addon_marked_as_tooling_candidate(self) -> None:
        record = archive_catalog.classify(
            "https://mirror/tts/nvda/NVDA-IBMTTS-Driver.nvda-addon"
        )
        self.assertEqual(record.category, "NVDA add-on package")
        self.assertIn(
            "nvda_addon_bundle", record.metadata.get("priority_tags", [])
        )
        self.assertIn(
            "tooling_candidate", record.metadata.get("priority_tags", [])
        )


if __name__ == "__main__":  # pragma: no cover - unittest CLI entry
    unittest.main()
