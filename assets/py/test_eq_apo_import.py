"""Tests for Equalizer APO configuration import tooling."""
from __future__ import annotations

from import_eq_apo_config import parse_eq_apo_config


_SAMPLE_CONFIG = """Device: Test Device
Stage: pre-mix post-mix capture
Channel: ALL
Copy: L=L R=R
Delay: 0.5 ms
LoudnessCorrection: State 1 ReferenceLevel 0 Attenuation 1.5
Preamp: -3 dB
Filter: ON PK Fc 1000 Hz Gain 6 dB Q 2
Filter: ON PK Fc 8000 Hz Gain -4 dB Q 1
"""


def test_parse_eq_apo_blocks() -> None:
    blocks = parse_eq_apo_config(_SAMPLE_CONFIG)
    assert len(blocks) == 1
    block = blocks[0]
    assert block.device == "Test Device"
    assert block.stage == ["pre-mix", "post-mix", "capture"]
    assert block.channel == "ALL"
    assert block.copy == "L=L R=R"
    assert block.delay_ms == 0.5
    assert block.loudness_correction["State"] == 1.0
    assert block.preamp_db == -3.0
    assert len(block.filters) == 2


def test_filter_to_phoneme_band_respects_sample_rate() -> None:
    blocks = parse_eq_apo_config(_SAMPLE_CONFIG)
    block = blocks[0]
    first_band = block.filters[0].to_phoneme_band(sample_rate=48000.0)
    assert first_band is not None
    assert 600.0 < first_band.low_hz < 1000.0
    assert first_band.high_hz <= 24000.0
    assert first_band.gain_db == 6.0
    assert first_band.filter_type == "peaking"
    assert first_band.q > 0.0

    second_band = block.filters[1].to_phoneme_band(sample_rate=16000.0)
    assert second_band is not None
    # Nyquist limit should cap the high frequency to <= 8000 Hz.
    assert second_band.high_hz <= 8000.0
    assert second_band.low_hz < second_band.high_hz
    assert second_band.gain_db == -4.0
