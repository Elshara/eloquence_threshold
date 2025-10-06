#Copyright (C) 2009-2011 Aleksey Sadovoy <lex@progger.ru>

from collections import OrderedDict
import os
from synthDriverHandler import SynthDriver,VoiceInfo
from ctypes import *
import config
import nvwave
from nvwave import outputDeviceNameToID

isSpeaking = False
player = None
ProcessAudioCallback = CFUNCTYPE(c_bool, POINTER(c_char),c_int)

@ProcessAudioCallback
def processAudio(buffer,length):
	global isSpeaking,player
	if not isSpeaking: return False
	s=string_at(buffer, length)
	player.feed(s)
	player.idle()
	return True

class SynthDriver(SynthDriver):
	name="captain"
	description = _("Captain synthesizer by Gennady Nefedov (Russian)")
	supportedSettings=(
		SynthDriver.RateSetting(),
		SynthDriver.VoiceSetting(),
	)
	dll = None
	availableVoices = OrderedDict((("default", VoiceInfo("default", _("default")),),))

	@classmethod
	def check(cls):
		return os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'captain.dll'))

	def __init__(self):
		global player
		player = nvwave.WavePlayer(channels=1, samplesPerSec=22050, bitsPerSample=8, outputDevice=config.conf["speech"]["outputDevice"])
		self.dll = CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'captain.dll'))
		self.dll.SpeakText.argtypes = [c_wchar_p, c_int]
		if not self.dll.InitSynth(processAudio): raise Exception

	def terminate(self):
		self.cancel()
		global player
		player.close()
		player=None
		self.dll.TerminateSynth()
		del self.dll

	def speakText(self, text, index=None):
		global isSpeaking
		isSpeaking = True
		if index is not None: 
			self.dll.SpeakText(text,index)
		else:
			self.dll.SpeakText(text,-1)

	def cancel(self):
		self.dll.cancel()
		global isSpeaking,player
		isSpeaking = False
		player.stop()

	def pause(self,switch):
		global player
		player.pause(switch)

	def _get_lastIndex(self):
		return self.dll._get_lastIndex()

	def _get_voice(self):
		return "default"

	def _set_voice(self,value):
		pass

	def _get_rate(self):
		return self.dll._get_rate()

	def _set_rate(self, value):
		self.dll._set_rate(value)
