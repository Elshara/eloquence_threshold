"""Tests covering the curated voice scene catalogue."""
from __future__ import annotations

import unittest

from voice_scenes import VOICE_SCENES, iter_scene_snapshots


class VoiceScenesTests(unittest.TestCase):
    def test_voice_scenes_have_metadata_and_configuration(self) -> None:
        snapshots = iter_scene_snapshots()
        self.assertEqual(len(VOICE_SCENES), len(snapshots))
        self.assertGreaterEqual(len(snapshots), 3)
        for snapshot in snapshots:
            self.assertIn("configuration", snapshot)
            self.assertIn("metadata", snapshot)
            config = snapshot["configuration"]
            params = config["advancedVoiceParameters"]
            for value in params.values():
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, 200)
            metadata = snapshot["metadata"]
            self.assertTrue(metadata.get("tags"))
            self.assertTrue(metadata.get("archiveSources"))
            self.assertGreater(metadata.get("headroomHz", 0), 0)
            per_phoneme = config["perPhonemeEq"]
            self.assertTrue(per_phoneme)


if __name__ == "__main__":
    unittest.main()
