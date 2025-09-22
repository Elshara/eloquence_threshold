import time
import logging
import ctypes
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
buffer = create_string_buffer(samples*2)
bgQueue = queue.Queue()
synth_queue = queue.Queue()
stopped = threading.Event()
started = threading.Event()
param_event = threading.Event()
Callback = WINFUNCTYPE(c_int, wintypes.HANDLE, wintypes.UINT, wintypes.WPARAM, c_void_p)
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
vparams = {}

audio_queue = queue.Queue()
#We can only have one of each in NVDA. Make this global
dll = None
handle = None

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
    for i in (rate, pitch, vlm, fluctuation, hsz, rgh, bth):
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
 for i in (rate, pitch, vlm, fluctuation):
  vparams[i] = eci.eciGetVoiceParam(handle, 0, i)
 return eci,handle

@WINFUNCTYPE(c_int,c_int,c_int,c_long,c_void_p)
def _bgExec(func, *args, **kwargs):
 global bgQueue
 bgQueue.put((func, args, kwargs))
def setLast(lp):
 global lastindex
 lastindex = lp
 #we can use this to set player idle
 #player.idle()
def bgPlay(stri, onDone=None):
 if len(stri) == 0: return
 # Sometimes player.feed() tries to open the device when it's already open,
 # causing a WindowsError. This code catches and works around this.
 # [DGL, 2012-12-18 with help from Tyler]
 tries = 0
 while tries < 10:
  try:
   player.feed(stri, onDone=onDone)
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
 if version_year >= 2025:
  device = config.conf["audio"]["outputDevice"]
  ducking = True if config.conf["audio"]["audioDuckingMode"] else False
  player = nvwave.WavePlayer(1, 11025, 16, outputDevice=device, wantDucking=ducking)
 else:
  device = config.conf["speech"]["outputDevice"]
  nvwave.WavePlayer.MIN_BUFFER_MS = 1500
  player = nvwave.WavePlayer(1, 11025, 16, outputDevice=device, buffered=True)
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
