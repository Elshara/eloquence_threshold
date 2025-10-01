# -*- coding: UTF-8 -*-
#synthDrivers/gregor.py by Grzegorz Zlotowicz
#based on synthdrivers/espeak.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2007-2013 NV Access Limited, Peter Vágner
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
from collections import OrderedDict
import Queue
import threading
import languageHandler
from synthDriverHandler import SynthDriver,VoiceInfo,BooleanSynthSetting
import speech
from logHandler import log
import time
import nvwave
from ctypes import *
import config
import globalVars
from pathlib import Path

import resource_paths

BASE_PATH = Path(__file__).resolve().parent
GREGOR_DLL_DIRS = resource_paths.engine_directories("gregor", "dll") + [resource_paths.asset_dir("dll"), BASE_PATH]

def _resolve_gregor_dll() -> str:
    return os.fspath(resource_paths.find_file_casefold("libsyntgregor.dll", GREGOR_DLL_DIRS))


t_gregor_callback=CFUNCTYPE(c_int,POINTER(c_short),c_int)

@t_gregor_callback
def callback(wav,numbytes):
	try:
		global player, isSpeaking
		if not isSpeaking:
			return 1
		if not wav:
			player.idle()
			isSpeaking = False
			return 0
		if numbytes > 0:
			try:
				player.feed(string_at(wav, numbytes))
			except:
				log.debugWarning("Error feeding audio to nvWave",exc_info=True)
		return 0
	except:
		log.error("callback", exc_info=True)

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

def _execWhenDone(func, *args, **kwargs):
	global bgQueue
	# This can't be a kwarg in the function definition because it will consume the first non-keywor dargument which is meant for func.
	mustBeAsync = kwargs.pop("mustBeAsync", False)
	if mustBeAsync or bgQueue.unfinished_tasks != 0:
		# Either this operation must be asynchronous or There is still an operation in progress.
		# Therefore, run this asynchronously in the background thread.
		bgQueue.put((func, args, kwargs))
	else:
		func(*args, **kwargs)

def _speak(text):
	global isSpeaking
	uniqueID=c_int()
	isSpeaking = True
	return gregorDLL.sayunicodestr(text)


class SynthDriver(SynthDriver):
	name = "gregor"
	description = "gregor"

	supportedSettings=(
		#SynthDriver.VoiceSetting(),
		#SynthDriver.VariantSetting(),
		SynthDriver.RateSetting(),
		SynthDriver.PitchSetting(),
		#SynthDriver.InflectionSetting(),
		SynthDriver.VolumeSetting(),
	)
	_rate=10

	@classmethod
	def check(cls):
		return True

	def __init__(self):
		global gregorDLL, libHandle, bgThread, bgQueue, player
		gregorDLL=cdll.LoadLibrary(_resolve_gregor_dll())
		player = nvwave.WavePlayer(channels=1, samplesPerSec=22050, bitsPerSample=16, outputDevice=config.conf["speech"]["outputDevice"])
		gregorDLL.setcallback(callback)
		bgQueue = Queue.Queue()
		bgThread=BgThread()
		bgThread.start()
		#log.info("Using gregor version %s" % _gregor.info())
		self.rate=25
		self.pitch=50
		self.inflection=75

	def speak(self,speechSequence):
		global bgQueue
		textList=[]
		for item in speechSequence:
			if isinstance(item,basestring):
				s=unicode(item)
				# Replace \01 and \02, as this is used for embedded commands.
				s=s.translate({ord(u'\01'):u' ',ord(u'\02'):u' '})
				textList.append(s)
			elif isinstance(item,speech.IndexCommand):
				textList.append(u"\x01%d "%item.index)
			elif isinstance(item,speech.CharacterModeCommand):
				textList.append(u"\x021" if item.state else u"\x020")
			elif isinstance(item,speech.SpeechCommand):
				log.debugWarning("Unsupported speech command: %s"%item)
			else:
				log.error("Unknown speech: %s"%item)
		text=u"".join(textList)
		_execWhenDone(_speak, text, mustBeAsync=True)


	def cancel(self):
		global isSpeaking, bgQueue
		# Kill all speech from now.
		# We still want parameter changes to occur, so requeue them.
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
		isSpeaking = False
		player.stop()


	def pause(self,switch):
		global player
		player.pause(switch)

	def _get_lastIndex(self):
		return gregorDLL.getlastindex()

	def _get_rate(self):
		return gregorDLL.getspeed100()
	def _set_rate(self,rate):
		gregorDLL.setspeed100(rate)

	def _get_pitch(self):
		return gregorDLL.getpitch100()
	def _set_pitch(self,pitch):
		gregorDLL.setpitch100(pitch)

	def _get_volume(self):
		return gregorDLL.getvol100()
	def _set_volume(self,volume):
		gregorDLL.setvol100(volume)

def terminate(self):
		global bgThread, bgQueue, player, gregorDLL 
		bgQueue.put((None, None, None))
		bgThread.join()
		#gregorDLL.espeak_Terminate()
		bgThread=None
		bgQueue=None
		player.close()
		player=None
		del gregorDLL
		gregorDLL=None
