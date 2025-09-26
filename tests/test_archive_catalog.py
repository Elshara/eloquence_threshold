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

    def test_extract_voice_hint_prefers_named_variants(self) -> None:
        hint = archive_catalog.extract_voice_hint("Voice Eloquence Dectalk 22kHz.exe")
        self.assertEqual(hint, "Eloquence")


if __name__ == "__main__":  # pragma: no cover - unittest CLI entry
    unittest.main()
