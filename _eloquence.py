import time
import logging
import ctypes
import audioop
import logging
import math
from array import array
from io import StringIO, BytesIO
from versionInfo import version_year

gb = BytesIO()
empty_gb = BytesIO()
empty_gb.write(b'\0\0')
onIndexReached = None
speaking = False
lang = 'enu'
from ctypes import *
import config
from ctypes import wintypes
import threading, os, queue, re
import nvwave

OLE32 = ctypes.WinDLL("ole32", use_last_error=True)

HRESULT = ctypes.c_long
LPVOID = ctypes.c_void_p

CLSCTX_INPROC_SERVER = 0x1

OLE32.CoInitialize.argtypes = [LPVOID]
OLE32.CoInitialize.restype = HRESULT
OLE32.CoUninitialize.argtypes = []
OLE32.CoUninitialize.restype = None
OLE32.CoCreateInstance.argtypes = [ctypes.POINTER(GUID), LPVOID, ctypes.c_ulong, ctypes.POINTER(GUID), ctypes.POINTER(LPVOID)]
OLE32.CoCreateInstance.restype = HRESULT
OLE32.CoTaskMemFree.argtypes = [LPVOID]
OLE32.CoTaskMemFree.restype = None

class GUID(ctypes.Structure):
 _fields_ = [
  ("Data1", wintypes.DWORD),
  ("Data2", wintypes.WORD),
  ("Data3", wintypes.WORD),
  ("Data4", ctypes.c_ubyte * 8),
 ]


def _guid(data1, data2, data3, data4):
 return GUID(data1, data2, data3, (ctypes.c_ubyte * 8)(*data4))


CLSID_MMDeviceEnumerator = _guid(
 0xBCDE0395,
 0xE52F,
 0x467C,
 (0x8E, 0x3D, 0xC4, 0x57, 0x92, 0x91, 0x69, 0x2E),
)
IID_IMMDeviceEnumerator = _guid(
 0xA95664D2,
 0x9614,
 0x4F35,
 (0xA7, 0x46, 0xDE, 0x8D, 0xB6, 0x36, 0x17, 0xE6),
)
IID_IAudioClient = _guid(
 0x1CB9AD4C,
 0xDBFA,
 0x4C32,
 (0xB1, 0x78, 0xC2, 0xF5, 0x68, 0xA7, 0x03, 0xB2),
)


class IMMDeviceEnumerator(ctypes.Structure):
 pass


class IMMDevice(ctypes.Structure):
 pass


class IAudioClient(ctypes.Structure):
 pass


LPIMMDeviceEnumerator = ctypes.POINTER(IMMDeviceEnumerator)
LPIMMDevice = ctypes.POINTER(IMMDevice)
LPIAudioClient = ctypes.POINTER(IAudioClient)


class IMMDeviceEnumeratorVtbl(ctypes.Structure):
 _fields_ = [
  ("QueryInterface", ctypes.WINFUNCTYPE(HRESULT, LPIMMDeviceEnumerator, ctypes.POINTER(GUID), ctypes.POINTER(LPVOID))),
  ("AddRef", ctypes.WINFUNCTYPE(ctypes.c_ulong, LPIMMDeviceEnumerator)),
  ("Release", ctypes.WINFUNCTYPE(ctypes.c_ulong, LPIMMDeviceEnumerator)),
  ("EnumAudioEndpoints", LPVOID),
  ("GetDefaultAudioEndpoint", ctypes.WINFUNCTYPE(HRESULT, LPIMMDeviceEnumerator, ctypes.c_int, ctypes.c_int, ctypes.POINTER(LPIMMDevice))),
  ("GetDevice", ctypes.WINFUNCTYPE(HRESULT, LPIMMDeviceEnumerator, wintypes.LPCWSTR, ctypes.POINTER(LPIMMDevice))),
  ("RegisterEndpointNotificationCallback", LPVOID),
  ("UnregisterEndpointNotificationCallback", LPVOID),
 ]


class IMMDeviceVtbl(ctypes.Structure):
 _fields_ = [
  ("QueryInterface", ctypes.WINFUNCTYPE(HRESULT, LPIMMDevice, ctypes.POINTER(GUID), ctypes.POINTER(LPVOID))),
  ("AddRef", ctypes.WINFUNCTYPE(ctypes.c_ulong, LPIMMDevice)),
  ("Release", ctypes.WINFUNCTYPE(ctypes.c_ulong, LPIMMDevice)),
  ("Activate", ctypes.WINFUNCTYPE(HRESULT, LPIMMDevice, ctypes.POINTER(GUID), ctypes.c_ulong, LPVOID, ctypes.POINTER(LPVOID))),
  ("OpenPropertyStore", LPVOID),
  ("GetId", ctypes.WINFUNCTYPE(HRESULT, LPIMMDevice, ctypes.POINTER(wintypes.LPWSTR))),
  ("GetState", LPVOID),
 ]


class WAVEFORMATEX(ctypes.Structure):
 _fields_ = [
  ("wFormatTag", wintypes.WORD),
  ("nChannels", wintypes.WORD),
  ("nSamplesPerSec", wintypes.DWORD),
  ("nAvgBytesPerSec", wintypes.DWORD),
  ("nBlockAlign", wintypes.WORD),
  ("wBitsPerSample", wintypes.WORD),
  ("cbSize", wintypes.WORD),
 ]


class IAudioClientVtbl(ctypes.Structure):
 _fields_ = [
  ("QueryInterface", ctypes.WINFUNCTYPE(HRESULT, LPIAudioClient, ctypes.POINTER(GUID), ctypes.POINTER(LPVOID))),
  ("AddRef", ctypes.WINFUNCTYPE(ctypes.c_ulong, LPIAudioClient)),
  ("Release", ctypes.WINFUNCTYPE(ctypes.c_ulong, LPIAudioClient)),
  ("Initialize", LPVOID),
  ("GetBufferSize", LPVOID),
  ("GetStreamLatency", LPVOID),
  ("GetCurrentPadding", LPVOID),
  ("IsFormatSupported", LPVOID),
  ("GetMixFormat", ctypes.WINFUNCTYPE(HRESULT, LPIAudioClient, ctypes.POINTER(ctypes.POINTER(WAVEFORMATEX)))),
  ("GetDevicePeriod", LPVOID),
  ("Start", LPVOID),
  ("Stop", LPVOID),
  ("Reset", LPVOID),
  ("SetEventHandle", LPVOID),
  ("GetService", LPVOID),
 ]


IMMDeviceEnumerator._fields_ = [("lpVtbl", ctypes.POINTER(IMMDeviceEnumeratorVtbl))]
IMMDevice._fields_ = [("lpVtbl", ctypes.POINTER(IMMDeviceVtbl))]
IAudioClient._fields_ = [("lpVtbl", ctypes.POINTER(IAudioClientVtbl))]


EDataFlow_eRender = 0
ERole_eConsole = 0

IS_64BIT = ctypes.sizeof(ctypes.c_void_p) == 8
VOICE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "eloquence"))
voiceDirectory = VOICE_DIR
_dictionaryDirs = [VOICE_DIR]

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
LPMSG = ctypes.POINTER(wintypes.MSG)
user32.PeekMessageW.argtypes = (LPMSG, wintypes.HWND, wintypes.UINT, wintypes.UINT, wintypes.UINT)
user32.PeekMessageW.restype = wintypes.BOOL
user32.GetMessageW.argtypes = (LPMSG, wintypes.HWND, wintypes.UINT, wintypes.UINT)
user32.GetMessageW.restype = wintypes.BOOL
user32.TranslateMessage.argtypes = (LPMSG,)
user32.TranslateMessage.restype = wintypes.BOOL
user32.DispatchMessageW.argtypes = (LPMSG,)
user32.DispatchMessageW.restype = wintypes.LRESULT
user32.PostThreadMessageW.argtypes = (wintypes.DWORD, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
user32.PostThreadMessageW.restype = wintypes.BOOL
kernel32.GetCurrentThreadId.restype = wintypes.DWORD
kernel32.GlobalAlloc.argtypes = (wintypes.UINT, ctypes.c_size_t)
kernel32.GlobalAlloc.restype = ctypes.c_void_p

eci = None
tid = None
bgt = None
samples = 3300
buffer = create_string_buffer(samples * 2)
bgQueue = queue.Queue()
synth_queue = queue.Queue()
stopped = threading.Event()
started = threading.Event()
param_event = threading.Event()
Callback = WINFUNCTYPE(c_int, wintypes.HANDLE, wintypes.UINT, wintypes.WPARAM, c_void_p)
gender=0
hsz=1
pitch=2
fluctuation=3
rgh=4
bth=5
rate=6
vlm=7
lastindex=0
langs={'esm': (131073, 'Latin American Spanish'),
'esp': (131072, 'Castilian Spanish'),
'ptb': (458752, 'Brazilian Portuguese'),
'frc': (196609, 'French Canadian'),
'fra': (196608, 'French'),
'fin': (589824, 'Finnish'),
'deu': (262144, 'German'),
'ita': (327680, 'Italian'),
'enu': (65536, 'American English'),
'eng': (65537, 'British English')}
avLangs = 0
eciPath = ""
WM_PROCESS=1025
WM_SILENCE = 1026
WM_PARAM = 1027
WM_VPARAM=1028
WM_COPYVOICE=1029
WM_KILL=1030
WM_SYNTH=1031
WM_INDEX=1032
params = {}
_SAMPLE_RATE_PARAM = 31
_SAMPLE_RATE_CODE_TO_HZ = {0: 8000, 1: 11025, 2: 22050}
_MIN_REQUESTED_SAMPLE_RATE = 8000
_MAX_REQUESTED_SAMPLE_RATE = 384000
_DEFAULT_REQUESTED_SAMPLE_RATE = 22050
_requested_sample_rate_hz = _DEFAULT_REQUESTED_SAMPLE_RATE
_device_sample_rate_hz = None
_current_engine_sample_code = min(
    _SAMPLE_RATE_CODE_TO_HZ,
    key=lambda code: abs(_SAMPLE_RATE_CODE_TO_HZ[code] - _requested_sample_rate_hz),
)
_current_engine_sample_rate_hz = _SAMPLE_RATE_CODE_TO_HZ[_current_engine_sample_code]
_resample_state = None
params[_SAMPLE_RATE_PARAM] = _current_engine_sample_code
vparams = {}

audio_queue = queue.Queue()
#We can only have one of each in NVDA. Make this global
dll = None
handle = None


def _clamp_sample_rate(hz):
 try:
  numeric = int(hz)
 except (TypeError, ValueError):
  return _requested_sample_rate_hz
 if numeric < _MIN_REQUESTED_SAMPLE_RATE:
  return _MIN_REQUESTED_SAMPLE_RATE
 if numeric > _MAX_REQUESTED_SAMPLE_RATE:
  return _MAX_REQUESTED_SAMPLE_RATE
 return numeric


class ParametricEQBand:
 def __init__(self, sample_rate, low_hz, high_hz, gain_db):
  self._sample_rate = max(sample_rate, _MIN_REQUESTED_SAMPLE_RATE)
  self._low_hz = max(1.0, float(low_hz))
 self._high_hz = max(self._low_hz + 1.0, float(high_hz))
 nyquist = self._sample_rate / 2.0
 if self._high_hz > nyquist:
  self._high_hz = nyquist
 if self._low_hz >= self._high_hz:
  self._low_hz = max(1.0, self._high_hz - 1.0)
 self._gain_db = float(gain_db)
 self.gain_db = self._gain_db
 self._z1 = 0.0
 self._z2 = 0.0
 self._configure()

 def _configure(self):
  fc = math.sqrt(self._low_hz * self._high_hz)
  bandwidth = max(self._high_hz - self._low_hz, fc * 0.05, 1.0)
  q = max(0.1, min(50.0, fc / bandwidth))
  omega = 2.0 * math.pi * fc / self._sample_rate
  sin_omega = math.sin(omega)
  cos_omega = math.cos(omega)
  alpha = sin_omega / (2.0 * q)
  a = math.pow(10.0, self._gain_db / 40.0)
  b0 = 1.0 + alpha * a
  b1 = -2.0 * cos_omega
  b2 = 1.0 - alpha * a
  a0 = 1.0 + alpha / a
  a1 = -2.0 * cos_omega
  a2 = 1.0 - alpha / a
  self._b0 = b0 / a0
  self._b1 = b1 / a0
  self._b2 = b2 / a0
  self._a1 = a1 / a0
  self._a2 = a2 / a0

 def process(self, samples):
  if not samples:
   return
  z1 = self._z1
  z2 = self._z2
  b0 = self._b0
  b1 = self._b1
  b2 = self._b2
  a1 = self._a1
  a2 = self._a2
  for idx, x in enumerate(samples):
   y = b0 * x + z1
   z1 = b1 * x - a1 * y + z2
   z2 = b2 * x - a2 * y
   samples[idx] = y
  self._z1 = z1
  self._z2 = z2


class ParametricEQEngine:
 def __init__(self):
  self._lock = threading.RLock()
  self._sample_rate = _requested_sample_rate_hz
  self._band_configs = []
  self._bands = []

 def set_sample_rate(self, hz):
  hz = _clamp_sample_rate(hz)
  with self._lock:
   if hz == self._sample_rate:
    return
   self._sample_rate = hz
   self._rebuild()

 def set_band_configs(self, configs):
  if configs is None:
   configs = []
  filtered = []
  for entry in configs:
   if not isinstance(entry, dict):
    continue
   low = entry.get("low_hz")
   high = entry.get("high_hz")
   gain = entry.get("gain_db", 0.0)
   try:
    low_val = float(low)
    high_val = float(high)
    gain_val = float(gain)
   except (TypeError, ValueError):
    continue
   if high_val <= 0 or low_val <= 0:
    continue
   filtered.append({"low_hz": low_val, "high_hz": high_val, "gain_db": gain_val})
  with self._lock:
   self._band_configs = filtered
   self._rebuild()

 def _rebuild(self):
  sample_rate = self._sample_rate
  self._bands = [ParametricEQBand(sample_rate, cfg["low_hz"], cfg["high_hz"], cfg["gain_db"]) for cfg in self._band_configs]

 def process(self, pcm_bytes):
  if not pcm_bytes:
   return pcm_bytes
  with self._lock:
   bands = list(self._bands)
  if not bands:
   return pcm_bytes
  samples = array("h")
  samples.frombytes(pcm_bytes)
  float_samples = [float(value) for value in samples]
  for band in bands:
   band.process(float_samples)
  max_abs = max(abs(value) for value in float_samples) or 1.0
  # Automatic gain control to avoid clipping when stacking boosts.
  boosting = sum(1 for band in bands if getattr(band, "gain_db", 0.0) > 0.0)
  headroom = max(1.0, math.sqrt(boosting) if boosting else 1.0)
  scale = min(1.0 / headroom, 32760.0 / max_abs)
  for idx, value in enumerate(float_samples):
   scaled = int(round(value * scale))
   if scaled > 32767:
    scaled = 32767
   elif scaled < -32768:
    scaled = -32768
   samples[idx] = scaled
  return samples.tobytes()


_eq_engine = ParametricEQEngine()


def setPhonemeEqBands(bands):
 if bands is None:
  _eq_engine.set_band_configs([])
  return
 normalised = []
 for entry in bands:
  if not isinstance(entry, dict):
   continue
  payload = {}
  for key, mapped in (("low_hz", "low_hz"), ("high_hz", "high_hz"), ("gain_db", "gain_db")):
   if mapped in entry:
    payload[mapped] = entry[mapped]
  if len(payload) < 2:
   continue
  normalised.append(payload)
 _eq_engine.set_band_configs(normalised)


def getPhonemeEqBands():
 return list(_eq_engine._band_configs)


def _release(interface):
 if not interface:
  return
 try:
  vtbl = interface.contents.lpVtbl.contents
 except Exception:
  return
 release = vtbl.Release
 release(interface)


def _configured_output_device_id():
 try:
  audio_section = config.conf.get("audio", {})
 except Exception:
  return None
 device = None
 if isinstance(audio_section, dict):
  device = audio_section.get("outputDevice")
 if not device:
  return None
 candidate = str(device).strip()
 if not candidate or candidate.lower() in {"default", "auto", "none", "null"}:
  return None
 return candidate


def _query_device_sample_rate():
 enumerator = None
 device = None
 audio_client = None
 fmt_ptr = LPVOID()
 initialized = False
 coinit_hr = OLE32.CoInitialize(None)
 if coinit_hr in (0, 1):
  initialized = True
 elif coinit_hr == 0x80010106:
  initialized = False
 else:
  logging.debug("CoInitialize failed with HRESULT 0x%08X", coinit_hr & 0xFFFFFFFF)
  return None
 try:
  enumerator_ptr = LPVOID()
  hr = OLE32.CoCreateInstance(
   ctypes.byref(CLSID_MMDeviceEnumerator),
   None,
   CLSCTX_INPROC_SERVER,
   ctypes.byref(IID_IMMDeviceEnumerator),
   ctypes.byref(enumerator_ptr),
  )
  if hr != 0 or not enumerator_ptr:
   logging.debug("CoCreateInstance(IMMDeviceEnumerator) failed: 0x%08X", hr & 0xFFFFFFFF)
   return None
  enumerator = ctypes.cast(enumerator_ptr, LPIMMDeviceEnumerator)
  device_id = _configured_output_device_id()
  enum_vtbl = enumerator.contents.lpVtbl.contents
  device_ptr = LPIMMDevice()
  if device_id:
   hr = enum_vtbl.GetDevice(enumerator, ctypes.c_wchar_p(device_id), ctypes.byref(device_ptr))
   if hr != 0 or not device_ptr:
    logging.debug("GetDevice('%s') failed: 0x%08X", device_id, hr & 0xFFFFFFFF)
    device_id = None
  if not device_id:
   hr = enum_vtbl.GetDefaultAudioEndpoint(
    enumerator,
    EDataFlow_eRender,
    ERole_eConsole,
    ctypes.byref(device_ptr),
   )
   if hr != 0 or not device_ptr:
    logging.debug("GetDefaultAudioEndpoint failed: 0x%08X", hr & 0xFFFFFFFF)
    return None
  device = device_ptr
  device_vtbl = device.contents.lpVtbl.contents
  audio_ptr = LPVOID()
  hr = device_vtbl.Activate(
   device,
   ctypes.byref(IID_IAudioClient),
   CLSCTX_INPROC_SERVER,
   None,
   ctypes.byref(audio_ptr),
  )
  if hr != 0 or not audio_ptr:
   logging.debug("Activate(IAudioClient) failed: 0x%08X", hr & 0xFFFFFFFF)
   return None
  audio_client = ctypes.cast(audio_ptr, LPIAudioClient)
  audio_vtbl = audio_client.contents.lpVtbl.contents
  wf_ptr = ctypes.POINTER(WAVEFORMATEX)()
  hr = audio_vtbl.GetMixFormat(audio_client, ctypes.byref(wf_ptr))
  if hr != 0 or not wf_ptr:
   logging.debug("GetMixFormat failed: 0x%08X", hr & 0xFFFFFFFF)
   return None
  fmt_ptr = wf_ptr
  sample_rate = int(wf_ptr.contents.nSamplesPerSec)
  return sample_rate if sample_rate > 0 else None
 except Exception:
  logging.exception("Unable to determine output device sample rate")
  return None
 finally:
  if fmt_ptr:
   OLE32.CoTaskMemFree(fmt_ptr)
  if audio_client:
   _release(audio_client)
  if device:
   _release(device)
  if enumerator:
   _release(enumerator)
  if initialized:
   OLE32.CoUninitialize()


def _apply_sample_rate(sample_rate_hz, rebuild_player=True):
 global _requested_sample_rate_hz, _resample_state, _device_sample_rate_hz
 if sample_rate_hz is None:
  return _requested_sample_rate_hz
 clamped = _clamp_sample_rate(sample_rate_hz)
 _device_sample_rate_hz = clamped
 _eq_engine.set_sample_rate(clamped)
 if clamped == _requested_sample_rate_hz:
  return clamped
 _requested_sample_rate_hz = clamped
 _resample_state = None
 desired_code = _choose_engine_sample_code(clamped)
 _set_engine_sample_code(desired_code)
 if rebuild_player and player is not None:
  _rebuild_player(_requested_sample_rate_hz)
 return _requested_sample_rate_hz


def refresh_sample_rate_from_device(rebuild_player=True):
 device_rate = _query_device_sample_rate()
 if device_rate is None:
  return _apply_sample_rate(_requested_sample_rate_hz, rebuild_player=rebuild_player)
 return _apply_sample_rate(device_rate, rebuild_player=rebuild_player)

_SUPPORTED_64BIT_MACHINES = {0x8664, 0xAA64}
_SUPPORTED_32BIT_MACHINES = {0x14C}


def _machine_type_for(path):
 try:
  with open(path, "rb") as f:
   f.seek(0x3C)
   offset_bytes = f.read(4)
   if len(offset_bytes) != 4:
    return None
   pe_offset = int.from_bytes(offset_bytes, "little")
   if pe_offset < 0:
    return None
   f.seek(pe_offset)
   if f.read(4) != b"PE\0\0":
    return None
   machine_bytes = f.read(2)
   if len(machine_bytes) != 2:
    return None
   return int.from_bytes(machine_bytes, "little")
 except OSError:
  return None


def _library_matches_current_arch(path):
 machine = _machine_type_for(path)
 if machine is None:
  return True
 if IS_64BIT:
  return machine in _SUPPORTED_64BIT_MACHINES
 return machine in _SUPPORTED_32BIT_MACHINES


def _candidate_library_paths():
 base_dir = VOICE_DIR
 candidates = []
 if IS_64BIT:
  arch_dirs = ("x64", "amd64", "arm64", "arm64ec")
  file_names = ("eci.dll", "ECI.DLL", "eci64.dll", "ECI64.DLL", "eci_x64.dll", "ECI_X64.DLL")
  for arch_dir in arch_dirs:
   arch_root = os.path.join(base_dir, arch_dir)
   for name in file_names:
    candidates.append(os.path.join(arch_root, name))
  for name in file_names:
   candidates.append(os.path.join(base_dir, name))
 else:
  for name in ("eci.dll", "ECI.DLL"):
   candidates.append(os.path.join(base_dir, name))
 return candidates


def _resolve_eci_path():
 for candidate in _candidate_library_paths():
  if not os.path.exists(candidate):
   continue
  if _library_matches_current_arch(candidate):
   return os.path.abspath(candidate)
  logging.debug("Skipping Eloquence library at %s due to architecture mismatch", candidate)
 raise FileNotFoundError(
  "Missing {arch} Eloquence engine. Expected to find a compatible ECI library in {base}.".format(
   arch="64-bit" if IS_64BIT else "32-bit",
   base=VOICE_DIR,
  )
 )


def _refresh_dictionary_dirs():
 global _dictionaryDirs, voiceDirectory
 dirs = []
 eci_dir = os.path.dirname(eciPath)
 for entry in (eci_dir, VOICE_DIR):
  if entry and os.path.isdir(entry) and entry not in dirs:
   dirs.append(entry)
 if not dirs:
  dirs.append(eci_dir)
 _dictionaryDirs = dirs
 voiceDirectory = dirs[0]
 for entry in dirs:
  try:
   if any(name.lower().endswith(".syn") for name in os.listdir(entry)):
    voiceDirectory = entry
    break
  except OSError:
   continue


def _find_resource(*names):
 for directory in _dictionaryDirs:
  for name in names:
   candidate = os.path.join(directory, name)
   if os.path.exists(candidate):
    return candidate
 return None


def _post_message(message, wparam=0, lparam=0):
 if tid is None:
  return
 user32.PostThreadMessageW(
  tid,
  message,
  wintypes.WPARAM(wparam),
  wintypes.LPARAM(lparam),
 )


def _choose_engine_sample_code(target_hz):
 global _current_engine_sample_code
 try:
  desired = int(target_hz)
 except (TypeError, ValueError):
  desired = _requested_sample_rate_hz
 code = min(
  _SAMPLE_RATE_CODE_TO_HZ,
  key=lambda candidate: abs(_SAMPLE_RATE_CODE_TO_HZ[candidate] - desired),
 )
 return code


def _set_engine_sample_code(code):
 global _current_engine_sample_code, _current_engine_sample_rate_hz, _resample_state
 if code not in _SAMPLE_RATE_CODE_TO_HZ:
  raise ValueError(f"Unsupported Eloquence sample rate code: {code}")
 if code == _current_engine_sample_code:
  return
 _current_engine_sample_code = code
 _current_engine_sample_rate_hz = _SAMPLE_RATE_CODE_TO_HZ[code]
 _resample_state = None
 if dll and handle:
  _post_message(WM_PARAM, code, _SAMPLE_RATE_PARAM)
  param_event.wait()
  param_event.clear()
 else:
  params[_SAMPLE_RATE_PARAM] = code


def _create_wave_player(sample_rate_hz):
 if version_year >= 2025:
  device = config.conf["audio"]["outputDevice"]
  ducking = True if config.conf["audio"]["audioDuckingMode"] else False
  return nvwave.WavePlayer(1, sample_rate_hz, 16, outputDevice=device, wantDucking=ducking)
 device = config.conf["speech"]["outputDevice"]
 nvwave.WavePlayer.MIN_BUFFER_MS = 1500
 return nvwave.WavePlayer(1, sample_rate_hz, 16, outputDevice=device, buffered=True)


def _rebuild_player(sample_rate_hz):
 global player
 if player is not None:
  try:
   player.stop()
  except Exception:
   logging.exception("Unable to stop audio player while changing sample rate")
  try:
   player.close()
  except Exception:
   logging.exception("Unable to close audio player while changing sample rate")
 player = _create_wave_player(sample_rate_hz)


def _resample_audio(data):
 global _resample_state
 if not data:
  return data
 if _current_engine_sample_rate_hz == _requested_sample_rate_hz:
  processed = _eq_engine.process(data)
  return processed
 converted, _resample_state = audioop.ratecv(
  data,
  2,
  1,
  _current_engine_sample_rate_hz,
  _requested_sample_rate_hz,
  _resample_state,
 )
 return _eq_engine.process(converted)


def setSampleRate(hz):
 device_rate = _query_device_sample_rate()
 if device_rate is not None:
  return _apply_sample_rate(device_rate)
 if hz is None:
  return _apply_sample_rate(_requested_sample_rate_hz)
 try:
  fallback = int(hz)
 except (TypeError, ValueError):
  raise ValueError(f"Invalid sample rate '{hz}'") from None
 return _apply_sample_rate(fallback)


def getSampleRate():
 return _requested_sample_rate_hz


def getSampleRateBounds():
 return _MIN_REQUESTED_SAMPLE_RATE, _MAX_REQUESTED_SAMPLE_RATE


def getDefaultSampleRate():
 return _DEFAULT_REQUESTED_SAMPLE_RATE

class eciThread(threading.Thread):
 def run(self):
  global vparams, params, speaking
  global tid, dll, handle
  tid = kernel32.GetCurrentThreadId()
  msg = wintypes.MSG()
  user32.PeekMessageW(byref(msg), None, 0x400, 0x400, 0)
  (dll, handle) = eciNew()
  dll.eciRegisterCallback(handle, callback, None)
  dll.eciSetOutputBuffer(handle, samples, pointer(buffer))
  dll.eciSetParam(handle,1, 1)
  dll.eciSetParam(handle, _SAMPLE_RATE_PARAM, _current_engine_sample_code)
  params[_SAMPLE_RATE_PARAM] = _current_engine_sample_code
  self.dictionaryHandle = dll.eciNewDict(handle)
  dll.eciSetDict(handle, self.dictionaryHandle)
  #0 = main dictionary
  main_dict = _find_resource("enumain.dic", "main.dic")
  if main_dict:
   dll.eciLoadDict(handle, self.dictionaryHandle, 0, main_dict.encode('mbcs'))
  root_dict = _find_resource("enuroot.dic", "root.dic")
  if root_dict:
   dll.eciLoadDict(handle, self.dictionaryHandle, 1, root_dict.encode('mbcs'))
  abbr_dict = _find_resource("enuabbr.dic", "abbr.dic")
  if abbr_dict:
   dll.eciLoadDict(handle, self.dictionaryHandle, 2, abbr_dict.encode('mbcs'))
  params[9] = dll.eciGetParam(handle, 9)
  started.set()
  while True:
   user32.GetMessageW(byref(msg), None, 0, 0)
   user32.TranslateMessage(byref(msg))
   if msg.message == WM_PROCESS:
    internal_process_queue()
   elif msg.message == WM_SILENCE:
    speaking=False
    gb.seek(0)
    gb.truncate(0)
    dll.eciStop(handle)
    try:
     while True:
      bgQueue.get_nowait()
    except:
      pass
    player.stop()
   elif msg.message == WM_PARAM:
    dll.eciSetParam(handle, msg.lParam, msg.wParam)
    params[msg.lParam] = msg.wParam
    param_event.set()
   elif msg.message == WM_VPARAM:
    setVParamImpl(param=msg.wParam, val=msg.lParam)
    param_event.set()
   elif msg.message == WM_COPYVOICE:
    dll.eciCopyVoice(handle, msg.wParam, 0)
    for i in (gender, hsz, pitch, fluctuation, rgh, bth, rate, vlm):
     vparams[i] = dll.eciGetVoiceParam(handle, 0, i)
    param_event.set()
   elif msg.message == WM_KILL:
    dll.eciDelete(handle)
    stopped.set()
    break
   else:
    user32.DispatchMessageW(byref(msg))

def eciCheck():
 global eciPath
 try:
  eciPath = _resolve_eci_path()
 except FileNotFoundError as exc:
  logging.error("%s", exc)
  return False
 _refresh_dictionary_dirs()
 iniCheck()
 return os.path.exists(eciPath)

def iniCheck():
 base_name = os.path.splitext(os.path.basename(eciPath))[0]
 ini_path = _find_resource(f"{base_name}.ini", "eci.ini", "ECI.INI")
 if not ini_path:
  return
 try:
  ini = open(ini_path, "r+")
 except OSError:
  return
 with ini:
  ini.seek(12)
  tml = ini.readline()
  if not tml:
   return
  expected = os.path.dirname(eciPath)
  if not expected.endswith(os.sep):
   expected = expected + os.sep
  current = tml[:-9]
  if current != expected:
   ini.seek(12)
   tmp = ini.read()
   ini.seek(12)
   ini.write(tmp.replace(current, expected))
   ini.truncate()

def eciNew():
 global avLangs
 if not eciCheck():
  raise RuntimeError("Eloquence engine is not available for this architecture")
 eci = ctypes.WinDLL(eciPath)
 b=c_int()
 eci.eciGetAvailableLanguages(0,byref(b))
 avLangs=(c_int*b.value)()
 eci.eciGetAvailableLanguages(byref(avLangs),byref(b))
 if 'eci' in config.conf['speech'] and config.conf['speech']['eci']['voice'] != '': handle=eci.eciNewEx(langs[config.conf['speech']['eci']['voice']][0])
 else: handle=eci.eciNewEx(langs[lang][0])
 for i in (gender, hsz, pitch, fluctuation, rgh, bth, rate, vlm):
  vparams[i] = eci.eciGetVoiceParam(handle, 0, i)
 return eci,handle

def setLast(lp):
 global lastindex
 lastindex = lp
 #we can use this to set player idle
 #player.idle()
def bgPlay(stri, onDone=None):
 if len(stri) == 0: return
 data = _resample_audio(stri)
 # Sometimes player.feed() tries to open the device when it's already open,
 # causing a WindowsError. This code catches and works around this.
 # [DGL, 2012-12-18 with help from Tyler]
 tries = 0
 while tries < 10:
  try:
   player.feed(data, onDone=onDone)
   if tries > 0:
    logging.warn("Eloq speech retries: %d" % (tries))
   return
  except:
   player.idle()
   time.sleep(0.02)
   tries += 1
 logging.error("Eloq speech failed to feed one buffer.")

def flush(updateIndex=False, index=None):
 onDone = None
 if updateIndex:
  onDone = lambda i=index: onIndexReached(i)
 this_gb = gb if gb.tell() > 0 else empty_gb
 _bgExec(bgPlay,
  this_gb.getvalue(),
  onDone=onDone,
 )
 gb.seek(0)
 gb.truncate(0)
 if updateIndex and index is not None:
  _bgExec(setLast, index)



curindex=None
@Callback
def callback (h, ms, lp, dt):
 global gb, curindex, speaking
 if not speaking:
  return 2
 #We need to buffer x amount of audio, and send the indexes after it.
 #Accuracy is lost with this method, but it should stop the say all breakage.
 if speaking and ms == 0: #audio data
  if gb.tell() >= samples*2:
   flush()
  gb.write(string_at(buffer, lp*2))
 elif ms==2: #index
  if lp != 0xffff: #end of string
   curindex = lp
   flush(updateIndex=True, index=curindex)
  else: #We reached the end of string
   flush(updateIndex=True, index=None)
   _bgExec(player.idle)
 return 1

class BgThread(threading.Thread):
 def __init__(self):
  threading.Thread.__init__(self)
  self.setDaemon(True)

 def run(self):
  global isSpeaking
  try:
   while True:
    func, args, kwargs = bgQueue.get()
    if not func:
     break
    func(*args, **kwargs)
    bgQueue.task_done()
  except:
   logging.error("bgThread.run", exc_info=True)

def _bgExec(func, *args, **kwargs):
 global bgQueue
 bgQueue.put((func, args, kwargs))
def str2mem(value):
 if isinstance(value, str):
  value = value.encode("mbcs")
 buf = create_string_buffer(value)
 blen = sizeof(buf)
 ptr = kernel32.GlobalAlloc(0x40, blen)
 cdll.msvcrt.memcpy(ptr, ctypes.addressof(buf), blen)
 return ptr

def initialize(indexCallback=None):
 global eci, player, bgt, dll, handle, onIndexReached

 onIndexReached = indexCallback
 refresh_sample_rate_from_device(rebuild_player=False)
 _rebuild_player(_requested_sample_rate_hz)
 eci = eciThread()
 eci.start()
 started.wait()
 started.clear()
 bgt = BgThread()
 bgt.start()

def speak(text):
 #Sometimes the synth slows down for one string of text. Why?
 #Trying to fix it here.
 if rate in vparams: text = "`vs%d" % (vparams[rate],)+text
 text = text.encode("mbcs")

 dll.eciAddText(handle, text)

def index(x):
 dll.eciInsertIndex(handle, x)
 
def cmdProsody(pr, multiplier):
 value = getVParam(pr)
 if multiplier:
  value = int(value * multiplier)
 setVParam(pr, value, temporary=True)

def synth():
 global speaking
 speaking = True
 dll.eciSynthesize(handle)

def stop():
 _post_message(WM_SILENCE)

def pause(switch):
 player.pause(switch)

def terminate():
 global bgt, player
 _post_message(WM_KILL)
 stopped.wait()
 stopped.clear()
 bgQueue.put((None, None, None))
 eci.join()
 bgt.join()
 player.close()
 player = None
 bgt = None

def set_voice(vl):
  _post_message(WM_PARAM, int(vl), 9)

def getVParam(pr):
 return vparams[pr]
 
def isInEciThread():
 return tid == kernel32.GetCurrentThreadId()

def setVParam(pr, vl, temporary=False):
 if isInEciThread():
  # We are running inside eciThread, so do it synchronously
  setVParamImpl(pr, vl, temporary)
 else:
   # Send a message to eciThread
   assert not temporary, "Can only set vParams permanently from another thread."
   _post_message(WM_VPARAM, pr, vl)
   param_event.wait()
   param_event.clear()
  
def setVParamImpl(param, val, temporary=False):
    global handle
    dll.eciSetVoiceParam(handle, 0, param, val)
    if not temporary:
     vparams[param] = val
     
def setVariant(v):
 _post_message(WM_COPYVOICE, v, 0)
 param_event.wait()
 param_event.clear()

def process():
  _post_message(WM_PROCESS)

def internal_process_queue():
 lst = synth_queue.get()
 for (func, args) in lst:
  func(*args)
