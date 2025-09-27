import json
import pathlib
import tempfile
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

    def test_bit_depth_and_channel_hints_are_extracted(self) -> None:
        record = archive_catalog.classify(
            "https://mirror/tts/espeak/voice_spanish_16bit_stereo_44khz.zip"
        )
        self.assertEqual(record.metadata.get("bit_depth_bits"), 16)
        self.assertEqual(record.metadata.get("channel_mode"), "Stereo")
        self.assertIn(
            "has_bit_depth_hint", record.metadata.get("priority_tags", [])
        )
        self.assertIn(
            "has_channel_hint", record.metadata.get("priority_tags", [])
        )

    def test_audio_fidelity_signature_is_recorded(self) -> None:
        record = archive_catalog.classify(
            "https://mirror/tts/espeak/voice_elite_24bit_stereo_96khz.zip"
        )
        metadata = record.metadata
        self.assertEqual(metadata.get("audio_signature"), "96 kHz • 24-bit • Stereo")
        self.assertEqual(metadata.get("audio_fidelity_tier"), "High fidelity source")
        self.assertIn("high_fidelity_audio", metadata.get("priority_tags", []))

    def test_platform_and_version_hints_are_extracted(self) -> None:
        record = archive_catalog.classify(
            "https://mirror/tts/espeak/espeak_toolkit_win64_v1_2_x64.zip"
        )
        metadata = record.metadata
        self.assertIsNotNone(metadata)
        self.assertIn("Platform: Windows", metadata.get("platform_hints", []))
        self.assertIn("Architecture: x64", metadata.get("platform_hints", []))
        self.assertEqual(metadata.get("version_hint"), "1.2")
        self.assertIn("has_platform_hint", metadata.get("priority_tags", []))
        self.assertIn("has_version_hint", metadata.get("priority_tags", []))

    def test_json_summary_includes_bit_depth_and_channel_counts(self) -> None:
        urls = [
            "https://mirror/tts/espeak/voice_spanish_16bit_stereo_44khz.zip",
            "https://mirror/tts/dectalk/voice_japanese_8bit_mono_11khz.zip",
        ]
        records = archive_catalog.build_records(urls)
        with tempfile.TemporaryDirectory() as tmp:
            output_path = pathlib.Path(tmp) / "inventory.json"
            archive_catalog.write_json(records, output_path)
            payload = json.loads(output_path.read_text())
        self.assertEqual(payload["summaries"]["bit_depths"].get("16"), 1)
        self.assertEqual(payload["summaries"]["bit_depths"].get("8"), 1)
        self.assertEqual(payload["summaries"]["channel_modes"].get("Stereo"), 1)
        self.assertEqual(payload["summaries"]["channel_modes"].get("Mono"), 1)

    def test_json_summary_includes_audio_fidelity_counts(self) -> None:
        urls = [
            "https://mirror/tts/espeak/voice_elite_24bit_stereo_96khz.zip",
            "https://mirror/tts/dectalk/voice_story_mono_16khz.zip",
        ]
        records = archive_catalog.build_records(urls)
        with tempfile.TemporaryDirectory() as tmp:
            output_path = pathlib.Path(tmp) / "inventory.json"
            archive_catalog.write_json(records, output_path)
            payload = json.loads(output_path.read_text())
        fidelity = payload["summaries"]["audio_fidelity"]
        self.assertEqual(fidelity.get("High fidelity source"), 1)
        self.assertEqual(fidelity.get("Low fidelity reference"), 1)
        self.assertEqual(
            payload["summaries"]["metadata_flags"].get("audio_fidelity_tier"), 2
        )

    def test_language_tags_are_recorded(self) -> None:
        record = archive_catalog.classify(
            "https://mirror/tts/espeak/voice_french_fr_fr_22khz.zip"
        )
        metadata = record.metadata
        self.assertIn("French", metadata.get("language_hints", []))
        self.assertIn("fr", metadata.get("language_tags", []))
        self.assertIn("has_language_tag", metadata.get("priority_tags", []))

    def test_synth_hint_is_detected(self) -> None:
        record = archive_catalog.classify(
            "https://mirror/tts/nvda/BeSTspeech_espeak_toolkit.zip"
        )
        metadata = record.metadata
        self.assertEqual(metadata.get("synth_hint"), "eSpeak NG")
        self.assertIn("has_synth_hint", metadata.get("priority_tags", []))

    def test_voice_gender_and_age_hints_detected(self) -> None:
        record = archive_catalog.classify(
            "https://mirror/tts/espeak/voice_female_child_story_22khz.zip"
        )
        metadata = record.metadata
        self.assertEqual(metadata.get("gender_hint"), "Female")
        self.assertEqual(metadata.get("age_hint"), "Child")
        self.assertIn("has_gender_hint", metadata.get("priority_tags", []))
        self.assertIn("has_age_hint", metadata.get("priority_tags", []))

    def test_json_summary_includes_voice_platform_and_version_counts(self) -> None:
        urls = [
            "https://mirror/tts/espeak/Voice_Eloquence_Toolkit_win64_v1_2.tar.gz",
            "https://mirror/tts/dectalk/voice_spanish_linux_x86_release-2_1.zip",
        ]
        records = archive_catalog.build_records(urls)
        with tempfile.TemporaryDirectory() as tmp:
            output_path = pathlib.Path(tmp) / "inventory.json"
            archive_catalog.write_json(records, output_path)
            payload = json.loads(output_path.read_text())
        summaries = payload["summaries"]
        self.assertGreaterEqual(summaries["voice_hints"].get("Eloquence", 0), 1)
        self.assertGreaterEqual(summaries["platforms"].get("Platform: Windows", 0), 1)
        self.assertGreaterEqual(summaries["platforms"].get("Platform: Linux", 0), 1)
        self.assertGreaterEqual(summaries["platforms"].get("Architecture: x86", 0), 1)
        self.assertGreaterEqual(summaries["platforms"].get("Architecture: x64", 0), 1)
        self.assertGreaterEqual(summaries["versions"].get("1.2", 0), 1)
        self.assertGreaterEqual(summaries["versions"].get("2.1", 0), 1)

    def test_json_summary_tracks_families_and_language_tags(self) -> None:
        urls = [
            "https://mirror/tts/espeak/voice_french_fr_fr_22khz.zip",
            "https://mirror/tts/dectalk/voice_spanish_linux_x86_release-2_1.zip",
        ]
        records = archive_catalog.build_records(urls)
        with tempfile.TemporaryDirectory() as tmp:
            output_path = pathlib.Path(tmp) / "inventory.json"
            archive_catalog.write_json(records, output_path)
            payload = json.loads(output_path.read_text())
        summaries = payload["summaries"]
        self.assertGreaterEqual(summaries["families"].get("espeak", 0), 1)
        self.assertGreaterEqual(summaries["families"].get("dectalk", 0), 1)
        self.assertGreaterEqual(summaries["language_tags"].get("fr", 0), 1)

    def test_metadata_flag_summary_counts_hints(self) -> None:
        urls = [
            "https://mirror/tts/espeak/voice_female_child_story_22khz.zip",
            "https://mirror/tts/dectalk/voice_male_adult_44khz.zip",
        ]
        records = archive_catalog.build_records(urls)
        with tempfile.TemporaryDirectory() as tmp:
            output_path = pathlib.Path(tmp) / "inventory.json"
            archive_catalog.write_json(records, output_path)
            payload = json.loads(output_path.read_text())
        summaries = payload["summaries"]
        metadata_flags = summaries["metadata_flags"]
        self.assertEqual(metadata_flags.get("sample_rate_hz"), 2)
        self.assertEqual(metadata_flags.get("gender_hint"), 2)
        self.assertEqual(metadata_flags.get("age_hint"), 2)
        self.assertEqual(summaries["gender_hints"].get("Female"), 1)
        self.assertEqual(summaries["gender_hints"].get("Male"), 1)
        self.assertEqual(summaries["age_hints"].get("Child"), 1)
        self.assertEqual(summaries["age_hints"].get("Adult"), 1)


if __name__ == "__main__":  # pragma: no cover - unittest CLI entry
    unittest.main()
