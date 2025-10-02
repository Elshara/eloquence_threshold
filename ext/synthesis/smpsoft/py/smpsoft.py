from ctypes import *
import os
from pathlib import Path
import synthDriverHandler
from synthDriverHandler import SynthDriver
import nvwave
import config
import threading
from logHandler import log
import Queue
import re

import resource_paths

BASE_PATH = Path(__file__).resolve().parent
SMP_DLL_DIRS = resource_paths.engine_directories("nv_speech_player", "dll") + [resource_paths.asset_dir("dll"), BASE_PATH]
SMP_DATA_DIRS = resource_paths.engine_directories("nv_speech_player", "data") + [BASE_PATH / 'smp' / 'data']


def _resolve_smp_dll() -> str:
    return os.fspath(resource_paths.find_file_casefold('SMPRenderer.dll', SMP_DLL_DIRS))


def _resolve_smp_data() -> str:
    for directory in SMP_DATA_DIRS:
        if directory.exists():
            return os.fspath(directory)
    return os.fspath(BASE_PATH / 'smp' / 'data')

last = None
bgQueue = Queue.Queue()
#I don't know how many drivers I've put this in by now. Like 10.
#One day I'll turn it into a package.
class BgThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.setDaemon(True)

	def run(self):
		global isSpeaking
		while True:
			func, args, kwargs = bgQueue.get()
			if not func:
				break
			try:
				func(*args, **kwargs)
			except:
				log.error("Error running function from queue", exc_info=True)
			bgQueue.task_done()

def _bgExec(func, *args, **kwargs):
 global bgQueue
 bgQueue.put((func, args, kwargs))

file_path = os.path.abspath(os.path.dirname(__file__))
smp_path = os.path.join(file_path, 'smp')
data_path = _resolve_smp_data()
dll_file = _resolve_smp_dll()
punctuation_re = re.compile(r"([,:.?!;])|(\d+)")
punctuation = ",:?.;!"
#really ugly hack, passing self, but it should work.
def _speak(cls, text):
	text = replace(text.encode('windows-1250', 'replace'))
	cls.dll.speak(text, cls.smprate, cls.smppitch, 100)
	#I think this is size, in samples, minus the wave header.
	size = cls.dll.GetWielkoscSygn()
	#And the data. Who came up with these retarded function names?
	ptr = cls.dll.GetSygnalWyj()
	data = string_at(ptr+44, size*2)
	player.feed(data)

def _setLast(index):
	global last
	last = index

class SynthDriver(synthDriverHandler.SynthDriver):
	name = 'smpsoft'
	description = 'smp software'
	supportedSettings = (SynthDriver.RateSetting(), SynthDriver.PitchSetting())
	@classmethod
	def check(cls):
		return True

	def __init__(self):
		super(SynthDriver, self).__init__()
		global player
		player = nvwave.WavePlayer(1, 14000, 16, outputDevice=config.conf["speech"]["outputDevice"])
		self.dll = cdll[dll_file]
		self.dll.initialize(data_path, 'x')
		self.bgt = BgThread()
		self.bgt.start()
		self.smprate = 1
		self.smppitch = 0

	def speakText(self, text, index=None):
		#This is aweful
		l = punctuation_re.split(text)
		nl = ['']
		for item in l:
			if item is None: continue
			item = item.strip()
			if item in punctuation:
				nl[-1] += item
			else:
				nl.append(item)

		for newtext in nl:
			if newtext == '' or newtext is None: continue
			_bgExec(_speak, self, newtext)
		if index is not None:
			_bgExec(_setLast, index)

	def _get_lastIndex(self):
		return last

	def cancel(self):
		#And this code... so many times
		params = []
		try:
			while True:
				item = bgQueue.get_nowait()
				if item[0] != _speak:
					params.append(item)
				bgQueue.task_done()
		except Queue.Empty:
			# Let the exception break us out of this loop, as queue.empty() is not reliable anyway.
			pass
		for item in params:
			bgQueue.put(item)
		player.stop()

	def terminate(self):
		player.stop()
		bgQueue.put((None, None, None))
		player.close()

	def _get_rate(self):
		return (self.smprate*5) + 50

	def _set_rate(self, rate):
		self.smprate = (rate - 50) / 5
	def _get_pitch(self):
		return (self.smppitch*5) + 50

	def _set_pitch(self, rate):
		self.smppitch = (rate - 50) / 5

	def pause(self, switch):
		player.pause(switch)

	#When smp encounters some characters, it stops. Replace them
replacements = {
"Q": "Ku",
"V": "W",
"X": "Ks",
"q": "ku",
"v": "w",
"x": "ks",
}
def replace(text):
	for o, r in replacements.iteritems():
		text = text.replace(o, r)
	return text
