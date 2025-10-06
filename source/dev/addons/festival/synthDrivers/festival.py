#Copyright 2008 Olga Yakovleva <Yakovleva.O.V@gmail.com>

#This program is free software:
#you can redistribute it and/or modify it under the terms of
#the GNU General Public License as published by the Free Software Foundation,
#either version 2 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#See the GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.

import ctypes
from synthDriverHandler import SynthDriver,VoiceInfo
import config
import nvwave
import os.path
import globalVars
from collections import OrderedDict
BASE_PATH = os.path.dirname(__file__)
class SynthDriver(SynthDriver):
	supportedSettings=(SynthDriver.VoiceSetting(),SynthDriver.RateSetting(),SynthDriver.VolumeSetting())

	name="festival"
	description="Festival Speech Synthesis System"

	@classmethod
	def check(cls):
		return os.path.isfile(os.path.join(BASE_PATH, "festlib.dll"))

	def __init__(self):
		self.tts_lib=ctypes.cdll.LoadLibrary(os.path.join(BASE_PATH, "festlib.dll"))
		res=self.tts_lib.festlib_initialize(unicode(BASE_PATH))
		if res!=0:
			raise RuntimeError("cannot initialize Festival synthesizer")

	def terminate(self):
		self.tts_lib.festlib_stop()

	def _get_rate(self):
		return self.tts_lib.festlib_get_rate()

	def _set_rate(self,value):
		self.tts_lib.festlib_set_rate(value)

	def _get_volume(self):
		return self.tts_lib.festlib_get_volume()

	def _set_volume(self,value):
		self.tts_lib.festlib_set_volume(value)

	def _getAvailableVoices(self):
		voices=OrderedDict()
		voiceList=map(lambda x:ctypes.string_at(self.tts_lib.festlib_get_voice_name(x)),range(self.tts_lib.festlib_get_voice_count()))
		for v in voiceList:
			voices[v]=VoiceInfo(v,v,None)
		return voices

	def _get_voice(self):
		addr=self.tts_lib.festlib_get_current_voice_name()
		if addr==0:
			return None
		return ctypes.string_at(addr)

	def _set_voice(self,name):
		self.tts_lib.festlib_set_voice(name.encode("utf-8"))
		device=nvwave.outputDeviceNameToID(config.conf["speech"]["outputDevice"], True)
		if device>=0:
			self.tts_lib.festlib_set_audio_device(device)

	def speakText(self,text,index=None):
		bookmark=index if index is not None else -1
		self.tts_lib.festlib_say_text(unicode(text),bookmark)

	def cancel(self):
		self.tts_lib.festlib_stop()

	def pause(self,switch):
		if switch:
			self.cancel()

	def _get_lastIndex(self):
		return self.tts_lib.festlib_get_bookmark()
