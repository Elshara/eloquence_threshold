import globalPluginHandler
import addonHandler
import gui
import wx
import speech
import globalVars

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super().__init__()
		if globalVars.appArgs.secure:
			return
		tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.config = tools_menu.Append(wx.ID_ANY, _("Configure &Orpheus..."))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.on_config, self.config)

	def on_config(self, evt):
		speech.speech.getSynth().lib.TTS_Config()

	def terminate(self):
		if globalVars.appArgs.secure:
			return
		tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
		tools_menu.RemoveItem(self.config.Id)
