"""Unit tests covering the phoneme EQ customiser helpers.

These tests guard against regressions in the advanced NV Speech Player style
parameter mapping documented in ``AGENTS.md`` and ensure the serialisation
helpers keep values in the 1 Hz–384 kHz / ±24 dB window enforced by the driver.
"""
from __future__ import annotations

import unittest

from phoneme_customizer import (
    PhonemeCustomizer,
    PhonemeEqBand,
    VoiceScene,
    build_scene_snapshot,
)
from voice_parameters import ADVANCED_VOICE_PARAMETER_SPECS


class PhonemeCustomizerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.customizer = PhonemeCustomizer()

    def test_apply_global_parameters_clamps_to_spec(self) -> None:
        spec = ADVANCED_VOICE_PARAMETER_SPECS["emphasis"]
        self.customizer.apply_global_parameters({"emphasis": spec["max"] + 20, "unknown": 42})
        self.assertEqual(self.customizer.global_parameter_value("emphasis"), spec["max"])

    def test_build_engine_payload_includes_global_and_per_phoneme_bands(self) -> None:
        self.customizer.set_global_parameter("emphasis", 140)
        self.customizer.set_band("AH", 0, PhonemeEqBand(low_hz=300, high_hz=900, gain_db=2.5))
        payload = self.customizer.build_engine_payload()
        self.assertTrue(any(entry["high_hz"] == 5200.0 for entry in payload))
        band = next(entry for entry in payload if entry["low_hz"] == 300.0 and entry["high_hz"] == 900.0)
        self.assertAlmostEqual(band["gain_db"], 2.5)
        self.assertEqual(band.get("filter_type"), "peaking")
        self.assertGreater(band.get("q", 0.0), 0.0)

    def test_profile_band_metadata_shapes_gain(self) -> None:
        self.customizer.set_global_parameter("vocalLayers", 140)
        payload = self.customizer.build_engine_payload()
        low_band = next(entry for entry in payload if entry["high_hz"] == 380.0)
        high_band = next(entry for entry in payload if entry["low_hz"] == 2400.0)
        self.assertAlmostEqual(high_band["gain_db"], 2.2, places=1)
        self.assertAlmostEqual(low_band["gain_db"], 1.5, places=1)

    def test_smoothness_positive_reduces_high_band(self) -> None:
        self.customizer.set_global_parameter("smoothness", 140)
        payload = self.customizer.build_engine_payload()
        band = next(entry for entry in payload if entry["low_hz"] == 4200.0)
        self.assertLess(band["gain_db"], 0.0)

    def test_whisper_scales_dual_band_profile(self) -> None:
        self.customizer.set_global_parameter("whisper", 130)
        payload = self.customizer.build_engine_payload()
        high_band = next(entry for entry in payload if entry["low_hz"] == 3600.0)
        low_band = next(entry for entry in payload if entry["high_hz"] == 900.0)
        self.assertGreater(high_band["gain_db"], 0.0)
        self.assertLess(low_band["gain_db"], 0.0)

    def test_pitch_height_boosts_fundamental_band(self) -> None:
        self.customizer.set_global_parameter("pitchHeight", 150)
        payload = self.customizer.build_engine_payload()
        fundamental = next(entry for entry in payload if entry["low_hz"] == 70.0)
        self.assertGreater(fundamental["gain_db"], 0.0)

    def test_plosive_impact_targets_transient_region(self) -> None:
        self.customizer.set_global_parameter("plosiveImpact", 150)
        payload = self.customizer.build_engine_payload()
        burst_band = next(entry for entry in payload if entry["low_hz"] == 900.0)
        self.assertGreater(burst_band["gain_db"], 0.0)

    def test_sibilant_clarity_shapes_high_noise_band(self) -> None:
        self.customizer.set_global_parameter("sibilantClarity", 160)
        payload = self.customizer.build_engine_payload()
        sibilant_band = next(entry for entry in payload if entry["low_hz"] == 5200.0)
        self.assertGreater(sibilant_band["gain_db"], 0.0)

    def test_nasal_balance_biases_upper_formant_slot(self) -> None:
        self.customizer.set_global_parameter("nasalBalance", 140)
        payload = self.customizer.build_engine_payload()
        nasal_band = next(entry for entry in payload if entry["low_hz"] == 980.0)
        self.assertGreater(nasal_band["gain_db"], 0.0)

    def test_inflection_contour_shapes_low_and_high_regions(self) -> None:
        self.customizer.set_global_parameter("inflectionContour", 160)
        payload = self.customizer.build_engine_payload()
        low_band = next(entry for entry in payload if entry["high_hz"] == 320.0)
        glide_band = next(entry for entry in payload if entry["low_hz"] == 2200.0)
        self.assertGreater(glide_band["gain_db"], low_band["gain_db"])
        self.assertGreater(low_band["gain_db"], 0.0)

    def test_head_size_contour_pushes_first_formants(self) -> None:
        self.customizer.set_global_parameter("headSizeContour", 140)
        payload = self.customizer.build_engine_payload()
        low_band = next(entry for entry in payload if entry["low_hz"] == 260.0)
        mid_band = next(entry for entry in payload if entry["low_hz"] == 820.0)
        high_band = next(entry for entry in payload if entry["high_hz"] == 3200.0)
        self.assertGreater(low_band["gain_db"], 0.0)
        self.assertGreater(mid_band["gain_db"], 0.0)
        self.assertLess(high_band["gain_db"], 0.0)

    def test_macro_volume_behaves_as_broadband_shelf(self) -> None:
        self.customizer.set_global_parameter("macroVolume", 160)
        payload = self.customizer.build_engine_payload()
        shelf_band = next(entry for entry in payload if entry["low_hz"] == 90.0)
        self.assertGreater(shelf_band["gain_db"], 0.0)

    def test_roughness_control_boosts_upper_band(self) -> None:
        self.customizer.set_global_parameter("roughnessControl", 160)
        payload = self.customizer.build_engine_payload()
        band = next(entry for entry in payload if entry["low_hz"] == 2600.0)
        self.assertGreater(band["gain_db"], 0.0)

    def test_sample_rate_clamp_limits_global_and_per_phoneme_bands(self) -> None:
        self.customizer.set_global_parameter("sibilantClarity", 170)
        # Store a per-phoneme band with an intentionally high frequency to ensure
        # the clamping logic tightens it once the sample rate drops.
        self.customizer.set_band(
            "S",
            0,
            PhonemeEqBand(low_hz=1800, high_hz=20000, gain_db=6.0),
        )
        nyquist = self.customizer.set_sample_rate(16000)
        self.assertLessEqual(nyquist, 8000.0)
        payload = self.customizer.build_engine_payload()
        self.assertTrue(all(entry["high_hz"] <= 8000.0 for entry in payload))
        band = self.customizer.band_for_layer("S", 0)
        self.assertLessEqual(band.high_hz, 8000.0)

    def test_serialise_and_load_round_trip(self) -> None:
        original = PhonemeEqBand(low_hz=150, high_hz=4800, gain_db=6.0, filter_type="bandPass", q=2.4)
        original = original.apply_q(original.q, 1.0, 384000.0)
        self.customizer.set_band("SH", 0, original)
        payload = self.customizer.serialise_per_phoneme()
        other = PhonemeCustomizer()
        other.load_per_phoneme(payload)
        restored = other.band_for_layer("SH", 0)
        self.assertAlmostEqual(restored.low_hz, original.low_hz)
        self.assertAlmostEqual(restored.high_hz, original.high_hz)
        self.assertAlmostEqual(restored.gain_db, original.gain_db)
        self.assertEqual(restored.filter_type, "bandPass")
        self.assertAlmostEqual(restored.q, original.q, places=3)

    def test_serialised_payload_includes_filter_and_q(self) -> None:
        band = PhonemeEqBand(low_hz=500, high_hz=1500, gain_db=3.0, filter_type="notch", q=1.5)
        self.customizer.set_band("S", 0, band)
        payload = self.customizer.serialise_per_phoneme()
        stored = payload["S"][0]
        self.assertEqual(stored["filterType"], "notch")
        self.assertAlmostEqual(stored["q"], band.q, places=3)

    def test_clone_and_reset_restore_independent_state(self) -> None:
        self.customizer.set_global_parameter("emphasis", 150)
        clone = self.customizer.clone()
        clone.set_global_parameter("emphasis", 80)
        self.assertNotEqual(
            clone.global_parameter_value("emphasis"), self.customizer.global_parameter_value("emphasis")
        )
        clone.reset_to_defaults()
        self.assertEqual(clone.global_parameter_value("emphasis"), ADVANCED_VOICE_PARAMETER_SPECS["emphasis"]["default"])

    def test_build_configuration_snapshot_reports_limits(self) -> None:
        self.customizer.set_band("S", 0, PhonemeEqBand(low_hz=600, high_hz=2600, gain_db=3.2))
        snapshot = self.customizer.build_configuration_snapshot()
        self.assertIn("advancedVoiceParameters", snapshot)
        self.assertIn("perPhonemeEq", snapshot)
        self.assertIn("enginePayload", snapshot)
        limits = snapshot["limits"]
        self.assertGreater(limits["highHzMaximum"], limits["lowHzMinimum"])

    def test_build_scene_snapshot_applies_voice_scene(self) -> None:
        scene = VoiceScene(
            name="Unit test clarity",
            description="Exercise the scene renderer",
            sample_rate_hz=44100.0,
            global_parameters={"emphasis": 140, "plosiveImpact": 128},
            phoneme_overrides={
                "S": [
                    {"lowHz": 4200.0, "highHz": 8600.0, "gainDb": 3.1, "filterType": "peaking", "q": 1.1},
                ]
            },
            tags=("espeak-ng", "nvda"),
            archive_sources=("docs/archive_inventory.json#example",),
            language_focus=("en", "multi"),
        )
        snapshot = build_scene_snapshot(scene)
        config = snapshot["configuration"]
        self.assertGreater(config["advancedVoiceParameters"]["emphasis"], 100)
        self.assertIn("S", config["perPhonemeEq"])
        metadata = snapshot["metadata"]
        self.assertIn("espeak-ng", metadata["tags"])
        self.assertEqual(metadata["sampleRateHz"], 44100.0)


if __name__ == "__main__":
    unittest.main()
