# -*- coding: Latin-1 -*-
#synthDrivers\brailab.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2010 Erion (erion@root.hu)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.



from synthDriverHandler import SynthDriver
from ctypes import *
import os

BASE_PATH=os.path.dirname(__file__)
minRate=0
maxRate=9
minPitch=-1
maxPitch=1
minVol=-2
maxVol=2

class SynthDriver(SynthDriver):
	name = "brailab"
	description = "Brailab PC Beszedszintetizator"
	supportedSettings=(SynthDriver.RateSetting(minStep=1),SynthDriver.PitchSetting(minStep=1),SynthDriver.VolumeSetting(minStep=1))



	@classmethod
	def check(cls):
		return os.path.isfile(os.path.join(BASE_PATH,"tts.dll"))

	def __init__(self):
		global dll
		dll=windll.LoadLibrary(os.path.join(BASE_PATH,'tts.dll'))
		dll.TTS_Init(1500,None)

	def terminate(self):
		self.cancel()
		self.dll=None
		del self.dll

	def cancel(self):
		self.isSpeaking=False
		dll.TTS_Stop()

	def speakText(self,text,index=None):
		self.isSpeaking=True
		dll.TTS_StartSay(text)

	def _get_rate(self):
		return self._paramToPercent(dll.TTS_GetTempo(),minRate,maxRate)

	def _set_rate(self,value):
		dll.TTS_SetTempo(self._percentToParam(value,minRate,maxRate))

	def _get_pitch(self):
		return self._paramToPercent(dll.TTS_GetPitch(),minPitch,maxPitch)

	def _set_pitch(self,value):
		dll.TTS_SetPitch(self._percentToParam(value,minPitch,maxPitch))

	def _get_volume(self):
		return self._paramToPercent(dll.TTS_GetVolume(),minVol,maxVol)

	def _set_volume(self,value):
		dll.TTS_SetVolume(self._percentToParam(value,minVol,maxVol))

	def pause(self,switch):
		dll.TTS_Stop()

