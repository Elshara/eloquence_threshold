import os
from synthDriverHandler import synthDoneSpeaking, SynthDriver, synthIndexReached, VoiceInfo
from speech.commands import PitchCommand
import addonHandler
addonHandler.initTranslation()
import ctypes
from ctypes import *
from ctypes.wintypes import DWORD
import struct
from io import StringIO
from speech.commands import IndexCommand
import threading
import time
import queueHandler
import config
import nvwave

LANGUAGES = {
	1: 'en',
	44: 'en-gb',
	30: 'el',
	31: 'nl',
	33: 'fr',
	34: 'es',
	36: 'hu',
	38: 'hr',
	39: 'it',
	40: 'ro',
	42: 'cs',
	45: 'da',
	46: 'sv',
	47: 'nb_NO',
	48: 'pl',
	49: 'de',
	52: 'es-mx',
	55: 'pt-br',
	60: 'ms',
	86: 'zh',
	351: 'pt-pt',
	358: 'fi',
	370: 'lt',
	10044: 'cy',
	10086: 'zh',
}

class SynthDriver(SynthDriver):
	supportedSettings = (
		SynthDriver.RateSetting(),
		SynthDriver.PitchSetting(),
		SynthDriver.VoiceSetting(),
		SynthDriver.VariantSetting(),
#		SynthDriver.InflectionSetting(),
#		SynthDriver.VolumeSetting(),
		)
	supportedCommands = {
		IndexCommand,
#		CharacterModeCommand,
#		LangChangeCommand,
#		BreakCommand,
		PitchCommand,
#		RateCommand,
#		VolumeCommand,
	}

	supportedNotifications = {synthIndexReached, synthDoneSpeaking}

	name='orpheus'
	description='Orpheus'
	lib = None
	hook = None

	@classmethod
	def check(cls):
		return True

	def __init__(self):
		dll_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'orpheus', 'a3s.dll')
		if not self.lib:
			self.lib = ctypes.windll[dll_path]
			self.write_sys()
		self.lib.TTS_Open.errcheck = errcheck
		self.lib.TTS_Close.errcheck = errcheck
		self.lib.TTS_Append.argtypes = (c_int, c_char_p, c_int, c_char_p)
		self.lib.TTS_Append.errcheck = errcheck
		self.lib.TTS_ReadStatus.errcheck = errcheck
		self.lib.TTS_Speak.argtypes = (c_int, c_char_p, c_int, c_wchar_p)
		self.lib.TTS_Speak.errcheck = errcheck
		self.lib.TTS_GetParams.errcheck = errcheck
		self.lib.TTS_DescParams.argtypes = (POINTER(c_ulong), POINTER(POINTER(ParamDesc)))
		self.lib.TTS_DescParams.errcheck = errcheck
		self.lib.TTS_GetLangs.argtypes = (POINTER(DWORD), POINTER(POINTER(Lang)))
		self.lib.TTS_GetLangs.errcheck = errcheck
		self.closed = False
		hook_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'orpheus', 'hook.dll')
		exe_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'orpheus', 'nvda.exe')
		if not self.hook:
			self.hook = windll[hook_path]
			self.hook.SetData(exe_path.encode('mbcs'))
		self.hook.Hook()
		try:
			self.lib.TTS_Open()
		finally:
			self.hook.Unhook()
		self.event = threading.Event()
		try:
			output = config.conf["audio"]["outputDevice"]
		except:
			output = config.conf["speech"]["outputDevice"]
		self.player = nvwave.WavePlayer(1, 22050, 16, outputDevice=output)
		self.is_speaking = False
		self.callback = self.setup_callback()
		self.lib.TTS_SetAudioMethod(1, self.callback)
		params = self.get_params()
		self.pitch = self._paramToPercent(params[1].current, params[1].min, params[1].max)
		self.rate = 50
		self.voice = 0
		self.variant = 0
		self.index = 0
		self.last_reached = 0
		self.lock = threading.Lock()
		self.queue = []

	def write_sys(self):
		sys_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'orpheus', 'orpheus.sys')
		newpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'orpheus')
		newpath = (newpath+'\0').encode('utf-16le')
		with open(sys_path, 'rb') as fp:
			s = fp.read()
		ln = len(newpath)
		s = s[:268] + newpath + s[268+ln:]
		if len(s) != 804:
			print("Unexpected length")
			return
		with open(sys_path, 'wb') as fp:
			fp.write(s)

	def speak(self, seq):
		# start_char, unknown, param_id, value
		parameters = [(0, 0, 0, self._rate), (0, 0, 12, self._voice), (0, 0, 7, self._variant),
		(0, 0, 1, self._pitch),
		]
		text = StringIO()
		text.write(' ')
		lastindex = 0
		for item in seq:
			if isinstance(item, str):
				text.write(item + ' ')
			elif isinstance(item, IndexCommand):
				parameters += [(text.tell() - 1, 0, 14, item.index)]
				text.write(' ')
				lastindex = item.index
			elif isinstance(item, PitchCommand):
				parameters += [(text.tell() - 1, 0, 1, self._pitch + item.offset)]
				text.write(' ')

		# Orpheus doesn't return all indexes on each word, only the last one.
		# Let's try to keep track of it while marking the end of the string.
		parameters.append((text.tell() - 1, 0, 14, lastindex | 0x80000000))
		self.queue.append((parameters, text.getvalue()))
		queueHandler.queueFunction(queueHandler.eventQueue, self.process_queue)

	def process_queue(self):
		with self.lock:
			if self.is_speaking:
				return # Callback will process the queue
			if self.queue:
				parameters, text = self.queue.pop(0)
				self.is_speaking = True
				self.append(parameters, text)
				self.speak_append()

	# Orpheus doesn't handle u+2019.
	table = {
	ord("’"): ord("'"),
	ord("“"): ord('"'),
	ord("”"): ord('"'),
	}

	def append(self, parameters, text):
		text = text.translate(self.table)
		param_str = b"".join(struct.pack('4I', *x) for x in parameters)
		text = text.encode('utf-16le')
		self.lib.TTS_Append(len(parameters), param_str, len(text) // 2, text)

	def lib_speak(self, parameters, text):
		text = text.translate(self.table)
		param_str = b"".join(struct.pack('4i', *x) for x in parameters)
		self.lib.TTS_Speak(len(parameters), param_str, len(text), text)

	def speak_append(self):
		self.lib.TTS_SpeakAppend()

	def _set_rate(self, rate):
		val = self._percentToParam(rate, 10, 700)
		self._rate = val

	def _get_rate(self):
		val = self._paramToPercent(self._rate, 10, 700)
		return val

	def _set_pitch(self, pitch):
		params = self.get_params()
		self._pitch = self._percentToParam(pitch, params[1].min, params[1].max)

	def _get_pitch(self):
		params= self.get_params()
		return self._paramToPercent(params[1].current, params[1].min, params[1].max)

	def cancel(self):
		with self.lock:
			self.queue = []
			self.player.stop()
			self.lib.TTS_Mute(3)
			self.is_speaking = False

	def _get_availableVoices(self):
		count = DWORD()
		ptr = POINTER(Lang)()
		self.lib.TTS_GetLangs(byref(count), byref(ptr))
		infos = {}
		for i in range(count.value):
			infos[str(i)] = VoiceInfo(str(i), ptr[i].lang, LANGUAGES.get(ptr[i].country))
		return infos

	def _get_voice(self):
		return str(self._voice)

	def _set_voice(self, voice):
		self._voice = int(voice)

	def _get_availableVariants(self):
		count = DWORD()
		ptr = POINTER(Lang)()
		self.lib.TTS_GetLangs(byref(count), byref(ptr))
		country = ptr[self._voice].country
		ptr = POINTER(Voice)()
		self.lib.TTS_GetVoices(country, byref(count), byref(ptr))
		infos = {}
		for i in range(count.value):
			infos[str(i)] = VoiceInfo(str(i), ptr[i].name)
		return infos

	def _get_variant(self):
		return str(self._variant)

	def _set_variant(self, variant):
		if variant is None:
			self._variant = 0
		else:
			self._variant = int(variant)
		params = ((0, 0, 7, self._variant),)
		self.lib_speak(params, ' ')
		self.event.wait()
		self.event.clear()
		self._pitch = self.get_params()[1].current

	def terminate(self):
		self.cancel()
		self.player.close()
		self.player = None
		self.lib.TTS_Close()
		self.closed = True
		#self.lib = None

	def status_reader(self):
		if self.closed:
			return
		self.is_speaking, self.index = self.status()
		if self.last_reached != self.index:
			self.last_reached = self.index
			synthIndexReached.notify(synth=self, index=self.index)
		if not self.is_speaking:
			synthDoneSpeaking.notify(synth=self)
			return
		queueHandler.queueFunction(queueHandler.eventQueue, self.status_reader)

	def status(self):
		st = create_string_buffer(8)
		self.lib.TTS_ReadStatus(pointer(st))
		x, y = struct.unpack('ii', st)
		return bool(x), y

	def get_params(self):
		count = DWORD()
		params = POINTER(ParamDesc)()
		self.lib.TTS_DescParams(byref(count), byref(params))
		params_lst = []
		for i in range(count.value):
			params_lst.append(ParamDesc(min=params[i].min, max=params[i].max, name=params[i].name))
		# This function copies more than count
		current = (c_ulong*(count.value+2))()
		self.lib.TTS_GetParams(byref(current))
		for i in range(count.value):
			params_lst[i].current = current[i]
		return params_lst

	def setup_callback(self):
		@WINFUNCTYPE(DWORD, c_void_p, DWORD, c_void_p, DWORD)
		def callback(buf, written, ctrlbuf, ctrls):
			c = string_at(ctrlbuf, ctrls*12)
			if not self.is_speaking:
#				self.lib.TTS_Mute(3)
				self.event.set()
#				return 0
			audio_data = string_at(buf, written*2)
			if ctrls == 0:
				controls = []
			else:
				controls = list(struct.iter_unpack('III', c))
			# We only want index marks
			controls = [c for c in controls if c[1] == 2]
#			if not self.is_speaking:
#				return 0
			self.player.feed(audio_data)
			for pos, type, value in controls:
				if value & 0x80000000:
					index = value & 0x7FFFFFFF
					if index:
						synthIndexReached.notify(synth=self, index=index)
					self.player.idle()
					synthDoneSpeaking.notify(synth=self)
					self.is_speaking = False
					queueHandler.queueFunction(queueHandler.eventQueue, self.process_queue)
				else: # Not at end of string
					synthIndexReached.notify(synth=self, index=value)
			return 0
		return callback

	def pause(self, switch):
		self.player.pause(switch)

def params(v):
	p = 'i' * len(v)
	packed = struct.pack(p, *v)
	return packed

class Lang(ctypes.Structure):
	_fields_ = (
		# Needed for GetVoice
		('country', DWORD),
		('lang', c_wchar*65),
		('unknown', DWORD),
	)

class Voice(ctypes.Structure):
	_fields_ = (
		('name', c_wchar*65),
		# I have no idea what these are
		('u1', DWORD),
		('u2', DWORD),
		('u3', DWORD),
		)

class ParamDesc(Structure):
	_fields_ = (
		('unknown', DWORD),
		('min', c_long),
		('max', c_long),
		('name', c_wchar_p),
	)

def errcheck(res, func, args):
	if res != 0:
		raise RuntimeError(res)
