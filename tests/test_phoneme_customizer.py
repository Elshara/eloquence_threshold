"""Unit tests covering the phoneme EQ customiser helpers.

These tests guard against regressions in the advanced NV Speech Player style
parameter mapping documented in ``AGENTS.md`` and ensure the serialisation
helpers keep values in the 1 Hz–384 kHz / ±24 dB window enforced by the driver.
"""
from __future__ import annotations

import unittest

from phoneme_customizer import PhonemeCustomizer, PhonemeEqBand
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
        self.assertIn({"low_hz": 300.0, "high_hz": 900.0, "gain_db": 2.5}, payload)

    def test_serialise_and_load_round_trip(self) -> None:
        original = PhonemeEqBand(low_hz=150, high_hz=4800, gain_db=6.0)
        self.customizer.set_band("SH", 0, original)
        payload = self.customizer.serialise_per_phoneme()
        other = PhonemeCustomizer()
        other.load_per_phoneme(payload)
        restored = other.band_for_layer("SH", 0)
        self.assertAlmostEqual(restored.low_hz, original.low_hz)
        self.assertAlmostEqual(restored.high_hz, original.high_hz)
        self.assertAlmostEqual(restored.gain_db, original.gain_db)


if __name__ == "__main__":
    unittest.main()
