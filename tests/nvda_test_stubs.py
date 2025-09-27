"""Helpers for stubbing NVDA-specific modules during unit tests."""

from __future__ import annotations

import builtins
import ctypes
import sys
import types
from typing import Any, List


def _ensure_module(name: str) -> types.ModuleType:
    module = sys.modules.get(name)
    if module is None:
        module = types.ModuleType(name)
        sys.modules[name] = module
    return module


def _install_audio_stubs() -> None:
    if "audioop" in sys.modules:
        return
    audioop_stub = types.ModuleType("audioop")

    def _ratecv(data: bytes, width: int, channels: int, in_rate: int, out_rate: int, state: Any):
        return data, state

    audioop_stub.ratecv = _ratecv  # type: ignore[attr-defined]
    sys.modules["audioop"] = audioop_stub


def _install_version_info_stub() -> None:
    version_stub = sys.modules.get("versionInfo")
    if version_stub is None:
        version_stub = types.ModuleType("versionInfo")
        version_stub.version_year = 2025  # type: ignore[attr-defined]
        sys.modules["versionInfo"] = version_stub


def _install_config_stub() -> None:
    config_stub = sys.modules.get("config")
    if config_stub is None:
        config_stub = types.ModuleType("config")
        config_stub.conf = {  # type: ignore[attr-defined]
            "audio": {},
            "speech": {"outputDevice": None, "eci": {"voice": ""}},
        }
        sys.modules["config"] = config_stub


def _install_speech_stubs() -> None:
    command_names = [
        "IndexCommand",
        "CharacterModeCommand",
        "LangChangeCommand",
        "BreakCommand",
        "PitchCommand",
        "RateCommand",
        "VolumeCommand",
        "PhonemeCommand",
    ]
    speech_module = _ensure_module("speech")
    commands_module = _ensure_module("speech.commands")
    speech_module.commands = commands_module  # type: ignore[attr-defined]

    for name in command_names:
        if hasattr(speech_module, name):
            continue

        class _Command:  # type: ignore[too-many-ancestors]
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                for key, value in kwargs.items():
                    setattr(self, key, value)

        _Command.__name__ = name  # type: ignore[attr-defined]
        setattr(speech_module, name, _Command)
        setattr(commands_module, name, _Command)


def _install_tone_stub() -> None:
    tones_module = sys.modules.get("tones")
    if tones_module is None:
        tones_module = types.ModuleType("tones")
        tones_module.beep = lambda *_args, **_kwargs: None  # type: ignore[attr-defined]
        sys.modules["tones"] = tones_module


def _install_driver_handler_stub() -> None:
    driver_module = sys.modules.get("driverHandler")
    if driver_module is None:
        driver_module = types.ModuleType("driverHandler")

        class DriverSetting:
            def __init__(self, name: str, *args: Any, **kwargs: Any) -> None:
                self.name = name
                display_name = kwargs.pop("displayName", None)
                if args:
                    display_name = args[0] if display_name is None else display_name
                self.displayName = display_name if display_name is not None else name
                self.availableInSettingsRing = kwargs.pop("availableInSettingsRing", False)
                for key, value in kwargs.items():
                    setattr(self, key, value)

        class BooleanDriverSetting(DriverSetting):
            def __init__(self, name: str, *args: Any, defaultValue: bool | None = None, **kwargs: Any) -> None:
                super().__init__(name, *args, **kwargs)
                self.defaultValue = defaultValue

        class NumericDriverSetting(DriverSetting):
            def __init__(self, name: str, *args: Any, **kwargs: Any) -> None:
                self.minVal = kwargs.pop("minVal", 0)
                self.maxVal = kwargs.pop("maxVal", 100)
                self.minStep = kwargs.pop("minStep", 1)
                self.normalStep = kwargs.pop("normalStep", 1)
                self.largeStep = kwargs.pop("largeStep", 1)
                self.defaultVal = kwargs.pop("defaultVal", None)
                super().__init__(name, *args, **kwargs)

        driver_module.DriverSetting = DriverSetting  # type: ignore[attr-defined]
        driver_module.BooleanDriverSetting = BooleanDriverSetting  # type: ignore[attr-defined]
        driver_module.NumericDriverSetting = NumericDriverSetting  # type: ignore[attr-defined]
        sys.modules["driverHandler"] = driver_module

    auto_settings_module = _ensure_module("autoSettingsUtils")
    driver_setting_module = _ensure_module("autoSettingsUtils.driverSetting")
    driver_setting_module.DriverSetting = driver_module.DriverSetting  # type: ignore[attr-defined]
    driver_setting_module.BooleanDriverSetting = driver_module.BooleanDriverSetting  # type: ignore[attr-defined]
    driver_setting_module.NumericDriverSetting = driver_module.NumericDriverSetting  # type: ignore[attr-defined]
    auto_settings_module.driverSetting = driver_setting_module  # type: ignore[attr-defined]

    utils_module = _ensure_module("autoSettingsUtils.utils")

    class UnsupportedConfigParameterError(NotImplementedError):
        pass

    class StringParameterInfo:
        def __init__(self, id: str, displayName: str) -> None:
            self.id = id
            self.displayName = displayName

    utils_module.UnsupportedConfigParameterError = UnsupportedConfigParameterError  # type: ignore[attr-defined]
    utils_module.StringParameterInfo = StringParameterInfo  # type: ignore[attr-defined]


def _install_addon_handler_stub() -> None:
    addon_module = sys.modules.get("addonHandler")
    if addon_module is None:
        addon_module = types.ModuleType("addonHandler")

        def _init_translation() -> None:
            builtins._ = lambda message: message  # type: ignore[attr-defined]

        addon_module.initTranslation = _init_translation  # type: ignore[attr-defined]
        sys.modules["addonHandler"] = addon_module


def _install_synth_driver_handler_stub() -> None:
    synth_module = sys.modules.get("synthDriverHandler")
    if synth_module is None:
        synth_module = types.ModuleType("synthDriverHandler")

        class SynthDriver:
            supportedSettings: List[Any] = []
            supportedCommands: set[Any] = set()
            supportedNotifications: set[Any] = set()

            def __init__(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover - stub
                pass

            def terminate(self) -> None:  # pragma: no cover - stub
                pass

        for _setting_name in (
            "VoiceSetting",
            "VariantSetting",
            "RateSetting",
            "PitchSetting",
            "InflectionSetting",
            "VolumeSetting",
        ):
            setattr(SynthDriver, _setting_name, type(_setting_name, (), {}))

        class VoiceInfo:
            def __init__(self, id: str, displayName: str, language: str | None = None) -> None:
                self.id = id
                self.displayName = displayName
                self.language = language

        def synthIndexReached(index: int) -> None:  # pragma: no cover - stub
            return None

        def synthDoneSpeaking() -> None:  # pragma: no cover - stub
            return None

        synth_module.SynthDriver = SynthDriver  # type: ignore[attr-defined]
        synth_module.VoiceInfo = VoiceInfo  # type: ignore[attr-defined]
        synth_module.synthIndexReached = synthIndexReached  # type: ignore[attr-defined]
        synth_module.synthDoneSpeaking = synthDoneSpeaking  # type: ignore[attr-defined]
        sys.modules["synthDriverHandler"] = synth_module


def _install_nvwave_stub() -> None:
    nvwave_module = sys.modules.get("nvwave")
    if nvwave_module is None:
        nvwave_module = types.ModuleType("nvwave")

        class WavePlayer:  # pragma: no cover - stub
            MIN_BUFFER_MS = 0

            def __init__(self, *args: Any, **kwargs: Any) -> None:
                pass

            def stop(self) -> None:
                pass

            def close(self) -> None:
                pass

            def idle(self) -> None:
                pass

            def feed(self, *args: Any, **kwargs: Any) -> None:
                pass

            def pause(self, *args: Any, **kwargs: Any) -> None:
                pass

        nvwave_module.WavePlayer = WavePlayer  # type: ignore[attr-defined]
        sys.modules["nvwave"] = nvwave_module


def _install_ctypes_stubs() -> None:
    if not hasattr(ctypes, "WinDLL"):
        class _StubFunction:
            def __call__(self, *args: Any, **kwargs: Any) -> int:
                return 0

        class _StubLibrary:
            def __getattr__(self, _attr: str) -> _StubFunction:
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
    defaults = {
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
        "UINT": ctypes.c_uint,
    }
    for name, ctype in defaults.items():
        if not hasattr(wintypes, name):
            setattr(wintypes, name, ctype)

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


def install_basic_stubs() -> None:
    """Install stubs for NVDA-only modules so unit tests can import drivers."""

    _install_audio_stubs()
    _install_version_info_stub()
    _install_config_stub()
    _install_speech_stubs()
    _install_tone_stub()
    _install_driver_handler_stub()
    _install_addon_handler_stub()
    _install_synth_driver_handler_stub()
    _install_nvwave_stub()
    _install_ctypes_stubs()

