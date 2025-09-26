"""Regression tests covering architecture-aware Eloquence runtime loading."""

from __future__ import annotations

import ctypes
import os
import pathlib
import sys
import tempfile
import types
import unittest
from unittest import mock

if "audioop" not in sys.modules:
    audioop_stub = types.ModuleType("audioop")

    def _ratecv(data, width, channels, in_rate, out_rate, state):
        return data, state

    audioop_stub.ratecv = _ratecv  # type: ignore[attr-defined]
    sys.modules["audioop"] = audioop_stub

if "versionInfo" not in sys.modules:
    version_info_stub = types.ModuleType("versionInfo")
    version_info_stub.version_year = 2025
    sys.modules["versionInfo"] = version_info_stub

if "config" not in sys.modules:
    config_stub = types.ModuleType("config")
    config_stub.conf = {
        "audio": {},
        "speech": {"outputDevice": None, "eci": {"voice": ""}},
    }
    sys.modules["config"] = config_stub

if not hasattr(ctypes, "WinDLL"):
    class _StubFunction:
        def __call__(self, *args, **kwargs):  # pragma: no cover - stub
            return 0

    class _StubLibrary:
        def __getattr__(self, _attr):  # pragma: no cover - stub
            return _StubFunction()

    ctypes.WinDLL = lambda *args, **kwargs: _StubLibrary()  # type: ignore[attr-defined]

if not hasattr(ctypes, "GUID"):
    class _StubGUID(ctypes.Structure):
        _fields_ = [
            ("Data1", ctypes.c_ulong),
            ("Data2", ctypes.c_ushort),
            ("Data3", ctypes.c_ushort),
            ("Data4", ctypes.c_ubyte * 8),
        ]

    ctypes.GUID = _StubGUID  # type: ignore[attr-defined]

if not hasattr(ctypes, "WINFUNCTYPE"):
    ctypes.WINFUNCTYPE = ctypes.CFUNCTYPE  # type: ignore[attr-defined]

if not hasattr(ctypes, "wintypes"):
    ctypes.wintypes = types.ModuleType("wintypes")  # type: ignore[attr-defined]

wintypes = ctypes.wintypes
_wintype_defaults = {
    "LRESULT": ctypes.c_long,
    "HWND": ctypes.c_void_p,
    "UINT": ctypes.c_uint,
    "WPARAM": ctypes.c_ulong,
    "LPARAM": ctypes.c_long,
    "DWORD": ctypes.c_ulong,
    "WORD": ctypes.c_ushort,
    "BOOL": ctypes.c_int,
    "HANDLE": ctypes.c_void_p,
    "LPCWSTR": ctypes.c_wchar_p,
    "LPWSTR": ctypes.c_wchar_p,
}
for _name, _ctype in _wintype_defaults.items():
    if not hasattr(wintypes, _name):
        setattr(wintypes, _name, _ctype)

if not hasattr(wintypes, "MSG"):
    class _MSG(ctypes.Structure):  # pragma: no cover - stub
        _fields_ = [
            ("hwnd", ctypes.c_void_p),
            ("message", ctypes.c_uint),
            ("wParam", ctypes.c_ulong),
            ("lParam", ctypes.c_long),
            ("time", ctypes.c_ulong),
            ("pt_x", ctypes.c_long),
            ("pt_y", ctypes.c_long),
        ]

    wintypes.MSG = _MSG  # type: ignore[attr-defined]

if "nvwave" not in sys.modules:
    nvwave_stub = types.ModuleType("nvwave")

    class _StubWavePlayer:
        MIN_BUFFER_MS = 0

        def __init__(self, *args, **kwargs) -> None:
            pass

        def stop(self) -> None:  # pragma: no cover - stub
            pass

        def close(self) -> None:  # pragma: no cover - stub
            pass

        def idle(self) -> None:  # pragma: no cover - stub
            pass

        def feed(self, *_args, **_kwargs) -> None:  # pragma: no cover - stub
            pass

    nvwave_stub.WavePlayer = _StubWavePlayer  # type: ignore[attr-defined]
    sys.modules["nvwave"] = nvwave_stub

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
