#-1 auto based on ident, anything else not
unit=-1
ident='DOLORPH' #substring of identifier to use
#copyright blurb goes here
from cStringIO import StringIO
import synthDriverHandler
from synthDriverHandler import SynthDriver, VoiceInfo
from collections import OrderedDict
from logHandler import log
from ctypes import *
from ctypes.wintypes import *
import config
import speech
from winUser import WNDCLASSEXW, WNDPROC
SAM_CONFIG_START=4
SAM_CONFIG_END=5
SAM_SERVER_QUIT=6
SAM_SERVER_RESTART=7

def errcheck(res, func, args):
	if res != 0:
		raise RuntimeError("%s: code %d" % (func.__name__, res))
	return res

class SYNTHPARAMS(Structure):
	_fields_ = [
		('description', WCHAR*128),
		('identifier', c_char*16),
		('params', WORD),
		('caps', DWORD),
		('langs', DWORD),
		('voices', DWORD),
	]

class SAMPARAM(Structure):
	_fields_ = [
		('range', DWORD),
		('first', c_long),
		('type', WORD),
		('id', WORD),
	]

sam = windll.sam32
for i in ('SamInit', 'SamOpenSynth', 'SamQuerySynth', 'SamQueryParam', 'SamIndex', 'SamQueryParamChoice',
'SamGetVoice'):
	getattr(sam, i).errcheck = errcheck

WM_SAM = 0x401


appInstance = windll.kernel32.GetModuleHandleW(None)
nvdaSamWndCls = WNDCLASSEXW()
nvdaSamWndCls.cbSize = sizeof(nvdaSamWndCls)
nvdaSamWndCls.hInstance = appInstance
nvdaSamWndCls.lpszClassName = u"nvdaSamWndCls"

class SynthDriver(synthDriverHandler.SynthDriver):
	name="sam"
	description = _("Sam")
	supportedSettings = (SynthDriver.RateSetting(), SynthDriver.VoiceSetting())

	@classmethod
	def check(cls):
		return True

	def __init__(self):
		super(synthDriverHandler.SynthDriver,self).__init__()
		global unit
		self.setup_wndproc()
		self._messageWindowClassAtom = windll.user32.RegisterClassExW(byref(nvdaSamWndCls))
		self._messageWindow = windll.user32.CreateWindowExW(0, self._messageWindowClassAtom, u"nvdaSamWndCls window", 0, 0, 0, 0, 0, None, None, appInstance, None)
		sam.SamInit(1, self._messageWindow, WM_SAM)
		self.availableVoices = OrderedDict()
		synths = sam.SamControl(2, 0)
		print "synths available: %d" % synths
		if unit == -1:
			for synth in range(1, synths+1):
				sp = SYNTHPARAMS()
				sam.SamQuerySynth(synth, byref(sp), 44)
				if ident in sp.identifier:
					unit = synth
					print "auto-detected %d" % synth
					break

		self.openSynth(unit)
		self.rate=50

	def openSynth(self, u):
		handle = c_int()
		sam.SamOpenSynth(u, byref(handle))
		self.handle = handle.value
		sp = SYNTHPARAMS()
		sam.SamQuerySynth(u, byref(sp), 44)
		print "using synth: %s ident %s with %d params" % (sp.description, sp.identifier, sp.params)
		self.vb = (DWORD*sp.params)()
		sam.SamGetDefaultVoice(unit, 44, byref(self.vb))
		self.curvoice='0'
		#Find which one of these parameters is the speed
		param = SAMPARAM()
		desc = create_unicode_buffer(128)
		for i in range(sp.params):
			sam.SamQueryParamDesc(unit, i, 44, byref(desc), 0)
			sam.SamQueryParam(unit, i, pointer(param))
			print desc.value
			if param.id == 1:
				self.rate_param = SAMPARAM()
				memmove(pointer(self.rate_param), pointer(param), sizeof(SAMPARAM))
				self.rate_param.pid = i
			elif param.id == 13: #voice?
				self.voice_param = SAMPARAM()
				memmove(pointer(self.voice_param), pointer(param), sizeof(SAMPARAM))
				self.voice_param.pid = i
			elif param.id == 7: #lang?
				self.lang_param = SAMPARAM()
				memmove(pointer(self.lang_param), pointer(param), sizeof(SAMPARAM))
				self.lang_param.pid = i
#
		for i in range(sp.voices):
			sam.SamQueryParamChoice(unit, -1, i, 44, desc, 0)
			i = str(i)
			self.availableVoices[i] = VoiceInfo(i, desc.value)

	def speak(self, speechSequence):
		if len(speechSequence) == 1 and speechSequence[0].strip() == '':
			return
		index = 0
		self.vb[self.rate_param.pid] = self.sam_rate
		for item in speechSequence:
			if isinstance(item, basestring):
				sam.SamAppend(self.handle, unicode(item), 0, index, byref(self.vb), 0)
			elif isinstance(item, speech.IndexCommand):
				index = item.index
		sam.SamSpeak(self.handle, index, 0)

	def cancel(self):
		sam.SamMute(self.handle)

	def _set_rate(self, rate):
		val = self._percentToParam(rate, 0, self.rate_param.range-1)
		self.sam_rate = val

	def _get_rate(self):
		return self._paramToPercent(self.sam_rate, 0, self.rate_param.range-1)

	def _get_lastIndex(self):
		index = DWORD(0)
		flags = DWORD(0)
		sam.SamIndex(self.handle, byref(index), byref(flags))
		return index.value

	def terminate(self):
		self.closeSynth()
		sam.SamEnd()
		windll.user32.DestroyWindow(self._messageWindow)

	def closeSynth(self):
		if self.handle:
			sam.SamCloseSynth(self.handle)

	def _get_voice(self):
		return self.curvoice

	def _set_voice(self, voice):
		self.curvoice = voice
		try:
			sam.SamGetVoice(unit, int(voice), byref(self.vb))
		except:
			pass

	def setup_wndproc(self):
		@WNDPROC
		def nvdaSamWndProc(hwnd, msg, wParam, lParam):
			sm = wParam&0xff
			if msg == WM_SAM:
				if sm == 1:
					sam.SamRespond()
				elif sm == SAM_CONFIG_START or sm == SAM_SERVER_QUIT:
					self.closeSynth()
				elif sm == SAM_CONFIG_END or sm == SAM_SERVER_RESTART:
					self.openSynth(unit)
				print "processed %d" % sm
				return 0
			else:
				return windll.user32.DefWindowProcW(hwnd,msg,wParam,lParam)
		nvdaSamWndCls.lpfnWndProc = nvdaSamWndProc
