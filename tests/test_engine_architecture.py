"""Regression tests covering architecture-aware Eloquence runtime loading."""

from __future__ import annotations

import os
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

from tests.nvda_test_stubs import install_basic_stubs

install_basic_stubs()

import _eloquence


def _write_fake_dll(path: pathlib.Path, machine: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Minimal PE header with the requested machine value.
    data = bytearray(512)
    data[0:2] = b"MZ"
    pe_offset = 0x80
    data[0x3C:0x40] = pe_offset.to_bytes(4, "little")
    data[pe_offset : pe_offset + 4] = b"PE\0\0"
    data[pe_offset + 4 : pe_offset + 6] = machine.to_bytes(2, "little")
    path.write_bytes(data)


class EngineArchitectureResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self._original_voice_dir = _eloquence.VOICE_DIR
        self._original_voice_directory = _eloquence.voiceDirectory
        self._original_dictionary_dirs = list(_eloquence._dictionaryDirs)

        voice_dir = pathlib.Path(self.tmpdir.name) / "eloquence"
        voice_dir.mkdir(parents=True, exist_ok=True)
        _eloquence.VOICE_DIR = str(voice_dir)
        _eloquence.voiceDirectory = _eloquence.VOICE_DIR
        _eloquence._dictionaryDirs = [
            _eloquence.VOICE_DIR,
        ]
        self.addCleanup(self._restore_globals)

    def _restore_globals(self) -> None:
        _eloquence.VOICE_DIR = self._original_voice_dir
        _eloquence.voiceDirectory = self._original_voice_directory
        _eloquence._dictionaryDirs = list(self._original_dictionary_dirs)

    def test_resolve_prefers_matching_x64_library(self) -> None:
        repo_root = pathlib.Path(_eloquence.VOICE_DIR).parent
        x64_path = repo_root / "eloquence_x64" / "eci64.dll"
        base_path = pathlib.Path(_eloquence.VOICE_DIR) / "eci.dll"
        _write_fake_dll(x64_path, 0x8664)
        _write_fake_dll(base_path, 0x14C)

        with mock.patch("_eloquence._current_architecture_family", return_value="x64"):
            resolved = _eloquence._resolve_eci_path()

        self.assertEqual(os.path.normcase(resolved), os.path.normcase(str(x64_path)))

    def test_resolve_prefers_matching_arm64_library(self) -> None:
        repo_root = pathlib.Path(_eloquence.VOICE_DIR).parent
        arm64_path = repo_root / "eloquence_arm64" / "eci_arm64.dll"
        base_path = pathlib.Path(_eloquence.VOICE_DIR) / "eci.dll"
        _write_fake_dll(arm64_path, 0xAA64)
        _write_fake_dll(base_path, 0x14C)

        with mock.patch("_eloquence._current_architecture_family", return_value="arm64"):
            resolved = _eloquence._resolve_eci_path()

        self.assertEqual(os.path.normcase(resolved), os.path.normcase(str(arm64_path)))

    def test_resolve_prefers_matching_x86_library(self) -> None:
        repo_root = pathlib.Path(_eloquence.VOICE_DIR).parent
        x86_path = repo_root / "eloquence_x86" / "eci.dll"
        legacy_path = pathlib.Path(_eloquence.VOICE_DIR) / "eci.dll"
        _write_fake_dll(x86_path, 0x14C)
        _write_fake_dll(legacy_path, 0x8664)

        with mock.patch("_eloquence._current_architecture_family", return_value="x86"):
            resolved = _eloquence._resolve_eci_path()

        self.assertEqual(os.path.normcase(resolved), os.path.normcase(str(x86_path)))

    def test_library_mismatch_is_rejected(self) -> None:
        repo_root = pathlib.Path(_eloquence.VOICE_DIR).parent
        mismatched = repo_root / "eloquence_x64" / "eci64.dll"
        _write_fake_dll(mismatched, 0x8664)

        with mock.patch("_eloquence._current_architecture_family", return_value="arm64"):
            self.assertFalse(_eloquence._library_matches_current_arch(str(mismatched)))


if __name__ == "__main__":
    unittest.main()
