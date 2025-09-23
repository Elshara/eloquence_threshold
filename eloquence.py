#Copyright (C) 2009-2019 eloquence fans
#synthDrivers/eci.py
#todo: possibly add to this
import speech, tones
try:
    from speech import (
        IndexCommand,
        CharacterModeCommand,
        LangChangeCommand,
        BreakCommand,
        PitchCommand,
        RateCommand,
        VolumeCommand,
        PhonemeCommand,
    )
except ImportError:
    from speech.commands import (
        IndexCommand,
        CharacterModeCommand,
        LangChangeCommand,
        BreakCommand,
        PitchCommand,
        RateCommand,
        VolumeCommand,
        PhonemeCommand,
    )

try:
    from driverHandler import NumericDriverSetting, BooleanDriverSetting, DriverSetting
except ImportError:
    from autoSettingsUtils.driverSetting import BooleanDriverSetting, DriverSetting, NumericDriverSetting

try:
    from autoSettingsUtils.utils import StringParameterInfo, UnsupportedConfigParameterError
except ImportError:
    class UnsupportedConfigParameterError(NotImplementedError):
        pass

    class StringParameterInfo(object):
        def __init__(self, id: str, displayName: str):
            self.id = id
            self.displayName = displayName

try:
    import addonHandler
except ImportError:
    def _(s):
        return s
else:
    addonHandler.initTranslation()


VOICE_PARAMETER_SETTING = DriverSetting(
 "voiceParameter",
 _("Voice para&meter"),
 availableInSettingsRing=True,
 displayName=_("Voice parameter"),
)

VOICE_PARAMETER_VALUE_SETTING = NumericDriverSetting(
 "voiceParameterValue",
 _("Voice parameter &value"),
 availableInSettingsRing=True,
 minVal=0,
 maxVal=200,
 minStep=1,
 normalStep=5,
 largeStep=10,
 displayName=_("Voice parameter value"),
)


punctuation = ",.?:;"
punctuation = [x for x in punctuation]
from ctypes import *
import ctypes.wintypes
from ctypes import wintypes
import synthDriverHandler, os, config, re, nvwave, threading, logging,driverHandler
from synthDriverHandler import SynthDriver, VoiceInfo, synthIndexReached, synthDoneSpeaking
from synthDriverHandler import SynthDriver,VoiceInfo
from . import _eloquence
from .phoneme_catalog import PhonemeDefinition, PhonemeInventory, PhonemeReplacement, load_default_inventory
from .voice_catalog import (
 VoiceCatalog,
 VoiceTemplate,
 VoiceParameterRange,
 load_default_voice_catalog,
)
from .language_profiles import (
 LanguageProfile,
 LanguageProfileCatalog,
 load_default_language_profiles,
)
from collections import OrderedDict
from typing import Dict, List, Optional, Tuple
import unicodedata

minRate=40
maxRate=150
pause_re = re.compile(r'([a-zA-Z])([.(),:;!?])( |$)')
time_re = re.compile(r"(\d):(\d+):(\d+)")
english_fixes = {
re.compile(r'(\w+)\.([a-zA-Z]+)'): r'\1 dot \2',
re.compile(r'([a-zA-Z0-9_]+)@(\w+)'): r'\1 at \2',
#Does not occur in normal use, however if a dictionary entry contains the Mc prefix, and NVDA splits it up, the synth will crash.
re.compile(r"\b(Mc)\s+([A-Z][a-z]+)"): r"\1\2",
re.compile(r'\b(.*?)c(ae|\xe6)sur(e)?', re.I): r'\1seizur',
re.compile(r"\b(|\d+|\W+)h'(r|v)[e]", re.I): r"\1h \2e",
re.compile(r"\b(\w+[bdfhjlmnqrvz])(h[he]s)([abcdefghjklmnopqrstvwy]\w+)\b", re.I): r"\1 \2\3",
re.compile(r"\b(\w+[bdfhjlmnqrvz])(h[he]s)(iron+[degins]?)", re.I): r"\1 \2\3",
re.compile(r"(\d):(\d\d[snrt][tdh])", re.I): r"\1 \2",
re.compile(r"\b([bcdfghjklmnpqrstvwxz]+)'([bcdefghjklmnprstvwxz']+)'([drtv][aeiou]?)", re.I): r"\1 \2 \3",
re.compile(r"\b(you+)'(re)+'([drv]e?)", re.I): r"\1 \2 \3",
re.compile(r"(re|un|non|anti)cosp", re.I): r"\1kosp",
re.compile(r"(EUR[A-Z]+)(\d+)", re.I): r"\1 \2",
re.compile(r"\b(\d+|\W+|[bcdfghjklmnpqrstvwxz])?t+z[s]che", re.I): r"\1tz sche",
re.compile(r"\b(juar[aeou]s)([aeiou]{6,})", re.I): r"\1 \2"
}
french_fixes = {
re.compile(r'([a-zA-Z0-9_]+)@(\w+)'): r'\1 arobase \2',
}
spanish_fixes = {
#for emails
re.compile(r'([a-zA-Z0-9_]+)@(\w+)'): r'\1 arroba \2',
}
german_fixes = {
#Crash words
re.compile(r'dane-ben', re.I): r'dane- ben',
	re.compile(r'dage-gen', re.I): r'dage- gen',
}
variants = {1:"Reed",
2:"Shelley",
3:"Bobby",
4:"Rocko",
5:"Glen",
6:"Sandy",
7:"Grandma",
8:"Grandpa"}

_PHONEME_FALLBACK_POLICIES: "OrderedDict[str, Tuple[str, ...]]" = OrderedDict([
 ("examplesFirst", ("example", "description", "ipa", "name")),
 ("descriptionsFirst", ("description", "example", "ipa", "name")),
 ("ipaFirst", ("ipa", "example", "description", "name")),
 ("engineSymbolsFirst", ("name", "ipa", "example", "description")),
])
_PHONEME_FALLBACK_DEFAULT = "examplesFirst"

def strip_accents(s):
  return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')  
                  
def normalizeText(s):
  """
  Normalizes  text by removing unicode characters.
  Tries to preserve accented characters if they fall into MBCS encoding page.
  Tries to find closest ASCII characters if accented characters cannot be represented in MBCS.
  """
  result = []
  for c in s:
   try:
    cc = c.encode('mbcs').decode('mbcs')
   except UnicodeEncodeError:
    cc = strip_accents(c)
    try:
     cc.encode('mbcs')
    except UnicodeEncodeError:
     cc = "?"
   result.append(cc)
  return "".join(result)

class SynthDriver(synthDriverHandler.SynthDriver):
 supportedSettings=(
  SynthDriver.VoiceSetting(),
  SynthDriver.VariantSetting(),
  SynthDriver.RateSetting(),
  SynthDriver.PitchSetting(),
  SynthDriver.InflectionSetting(),
  SynthDriver.VolumeSetting(),
  NumericDriverSetting("hsz", "Head Size"),
  NumericDriverSetting("rgh", "Roughness"),
  NumericDriverSetting("bth", "Breathiness"),
  BooleanDriverSetting("backquoteVoiceTags","Enable backquote voice &tags", True),
  BooleanDriverSetting("ABRDICT","Enable &abbreviation dictionary", False),
  BooleanDriverSetting("phrasePrediction","Enable phrase prediction", False),
  DriverSetting(
   "voiceTemplate",
   _("eSpeak voice &template"),
   availableInSettingsRing=True,
   displayName=_("Voice template"),
  ),
  DriverSetting(
   "languageProfile",
   _("Language &profile"),
   availableInSettingsRing=True,
   displayName=_("Language profile"),
  ),
  VOICE_PARAMETER_SETTING,
  VOICE_PARAMETER_VALUE_SETTING,
  DriverSetting(
   "phonemeCategory",
   _("Phoneme &category"),
   availableInSettingsRing=True,
   displayName=_("Phoneme category"),
  ),
  DriverSetting(
   "phonemeSymbol",
   _("Phoneme s&ymbol"),
   availableInSettingsRing=True,
   displayName=_("Phoneme symbol"),
  ),
  DriverSetting(
   "phonemeReplacement",
   _("Phoneme &replacement"),
   availableInSettingsRing=True,
   displayName=_("Phoneme replacement"),
  ),
  DriverSetting(
   "phonemeFallback",
   _("Default phoneme &fallback"),
   availableInSettingsRing=True,
   displayName=_("Default phoneme fallback"),
  ),
 )
 supportedCommands = {
     IndexCommand,
     CharacterModeCommand,
     LangChangeCommand,
     BreakCommand,
     PitchCommand,
     RateCommand,
     VolumeCommand,
     PhonemeCommand,
 }
 supportedNotifications = {synthIndexReached, synthDoneSpeaking}
 _phonemeInventory: PhonemeInventory
 _phonemeReplacements: Dict[str, str]
 _phonemeFallbackPreference: str
 _lastReplacementSelection: Optional[str]
 _voiceCatalog: VoiceCatalog
 _voiceTemplateId: Optional[str]
 _languageProfiles: LanguageProfileCatalog
 _languageProfileSelection: str
 _activeLanguageProfileId: Optional[str]
 _languageProfileOverrideId: Optional[str]
 _lastVoiceTemplateSelection: Optional[str]
 _voiceParameterSelection: Optional[str]
 _lastVoiceParameterSelection: Optional[str]
 _phonemeCategorySelection: Optional[str]
 _phonemeSelection: Optional[str]
 PROSODY_ATTRS = {
  PitchCommand: _eloquence.pitch,
  VolumeCommand: _eloquence.vlm,
  RateCommand: _eloquence.rate,
 }
 _VOICE_TEMPLATE_DEFAULT = "engine-default"
 _LANGUAGE_PROFILE_AUTO = "auto"
 _LANGUAGE_PROFILE_DISABLED = "disabled"
 _VOICE_PARAMETER_ORDER = (
  "rate",
  "pitch",
  "inflection",
  "headSize",
  "roughness",
  "breathiness",
  "volume",
 )
 _VOICE_PARAM_BINDINGS = {
  "pitch": _eloquence.pitch,
  "inflection": _eloquence.fluctuation,
  "headSize": _eloquence.hsz,
  "roughness": _eloquence.rgh,
  "breathiness": _eloquence.bth,
  "rate": _eloquence.rate,
  "volume": _eloquence.vlm,
 }
 _TEMPLATE_BOOLEAN_SETTINGS = {"backquoteVoiceTags", "ABRDICT", "phrasePrediction"}

 description='ETI-Eloquence'
 name='eloquence'
 @classmethod
 def check(cls):
  return _eloquence.eciCheck()
 def __init__(self):
  _eloquence.initialize(self._onIndexReached)
 self.curvoice="enu"
 self.rate=50
 self.variant = "1"
 self._phonemeInventory = load_default_inventory()
 self._phonemeReplacements = {}
 self._phonemeFallbackPreference = _PHONEME_FALLBACK_DEFAULT
 self._load_stored_phoneme_replacements()
 self._lastReplacementSelection = None
 self._phonemeCategorySelection = None
 self._phonemeSelection = None
 self._ensure_phoneme_selection()
 self._voiceCatalog = load_default_voice_catalog()
 self._voiceTemplateId = None
 self._lastVoiceTemplateSelection = None
 self._voiceParameterSelection = None
 self._lastVoiceParameterSelection = None
 self._ensure_voice_parameter_selection()
 self._languageProfiles = load_default_language_profiles()
 self._languageProfileSelection = _LANGUAGE_PROFILE_AUTO
 self._activeLanguageProfileId = None
 self._languageProfileOverrideId = None
 self._refresh_language_profile()

 def speak(self, speechSequence):
  last = None
  outlist = []
  for item in speechSequence:
   if isinstance(item, str):
    s = str(item)
    s = self.xspeakText(s)
    outlist.append((_eloquence.speak, (s,)))
    last = s
   elif isinstance(item, IndexCommand):
    outlist.append((_eloquence.index, (item.index,)))
   elif isinstance(item, LangChangeCommand):
    self._handle_lang_change(getattr(item, "lang", None))
    continue
   elif isinstance(item, BreakCommand):
    # Eloquence doesn't respect delay time in milliseconds.
    # Therefor we need to adjust waiting time depending on current speech rate.
    coefficients = {
        10: 1,
        43: 2,
        60: 3,
        75: 4,
        85: 5,
    }
    ck = sorted(coefficients.keys())
    if self.rate <= ck[0]:
     factor = coefficients[ck[0]]
    elif self.rate >= ck[-1]:
     factor = coefficients[ck[-1]]
    elif self.rate in ck:
     factor = coefficients[self.rate]
    else:
     li = [index for index, r in enumerate(ck) if r < self.rate][-1]
     ri = li + 1
     ra = ck[li]
     rb = ck[ri]
     factor = 1.0 * coefficients[ra] + (coefficients[rb] - coefficients[ra]) * (self.rate - ra) / (rb - ra)
    pFactor = factor * item.time
    pFactor = int(pFactor)
    outlist.append((_eloquence.speak, (f"`p{pFactor}.",)))
   elif isinstance(item, PhonemeCommand):
    rendered = self._renderPhonemeCommand(item)
    if rendered:
     spoken = self.xspeakText(rendered)
     outlist.append((_eloquence.speak, (spoken,)))
     last = rendered
   elif type(item) in self.PROSODY_ATTRS:
    pr = self.PROSODY_ATTRS[type(item)]
    if item.multiplier == 1:
     # Revert back to defaults
     outlist.append((_eloquence.cmdProsody, (pr, None,)))
    else:
     outlist.append((_eloquence.cmdProsody, (pr, item.multiplier,)))
  if last is not None and last.rstrip() and last.rstrip()[-1] not in punctuation:
   outlist.append((_eloquence.speak, ("`p1.",)))
  outlist.append((_eloquence.index, (0xffff,)))
  outlist.append((_eloquence.synth, ()))
  _eloquence.synth_queue.put(outlist)
  _eloquence.process()

 def xspeakText(self,text, should_pause=False):
  # Presumably dashes are handled as symbols by NVDA symbol processing, so strip extra ones to avoid too many dashes.
  text = text.replace("-", " ")
  if _eloquence.params[9] == 65536 or _eloquence.params[9] == 65537: text = resub(english_fixes, text)
  if _eloquence.params[9] == 131072 or _eloquence.params[9] == 131073: text = resub(spanish_fixes, text)
  if _eloquence.params[9] in (196609, 196608): text = resub(french_fixes, text)
  if _eloquence.params[9] in ('deu', 262144): text = resub(german_fixes, text)
  #this converts to ansi for anticrash. If this breaks with foreign langs, we can remove it.
  #text = text.encode('mbcs')
  text = normalizeText(text)
  if not self._backquoteVoiceTags:
   text=text.replace('`', ' ')
  text = "`vv%d %s" % (self.getVParam(_eloquence.vlm), text) #no embedded commands
  text = pause_re.sub(r'\1 `p1\2\3', text)
  text = time_re.sub(r'\1:\2 \3', text)
  if self._ABRDICT:
   text="`da1 "+text
  else:
   text="`da0 "+text
  if self._phrasePrediction:
   text="`pp1 "+text
  else:
   text="`pp0 "+text
  #if two strings are sent separately, pause between them. This might fix some of the audio issues we're having.
  if should_pause:
   text = text + ' `p1.'
  return text
  #  _eloquence.speak(text, index)

  # def cancel(self):
  #  self.dll.eciStop(self.handle)

 def _renderPhonemeCommand(self, command: PhonemeCommand) -> Optional[str]:
  inventory = self._phonemeInventory
  ipa_text = getattr(command, "ipa", "") or ""
  fallback = command.text or ipa_text
  if inventory.is_empty:
   return fallback
  matches, remainder = inventory.match_ipa_sequence(ipa_text)
  outputs: List[str] = []
  for definition in matches:
   replacement = definition.get_replacement(
    self._phonemeReplacements.get(definition.name),
    self._current_fallback_order(),
   )
   if replacement and replacement.output:
    outputs.append(replacement.output)
  if remainder:
   logging.debug("Unmatched IPA sequence for Eloquence fallback: %s", remainder)
   fallback_text = remainder
   profile = self._active_language_profile()
   if profile:
    hint = profile.describe_text(remainder)
    if hint:
     fallback_text = f"{remainder} ({hint})"
   outputs.append(fallback_text)
  spoken = " ".join(part.strip() for part in outputs if isinstance(part, str) and part.strip())
  return spoken or fallback

 def _ensure_phoneme_selection(self):
  if self._phonemeInventory.is_empty:
   self._phonemeCategorySelection = None
   self._phonemeSelection = None
   return
  categories = list(self._phonemeInventory.categories.keys())
  if not categories:
   self._phonemeCategorySelection = None
   self._phonemeSelection = None
   return
  if self._phonemeCategorySelection not in categories:
   self._phonemeCategorySelection = categories[0]
  phonemes = self._phonemeInventory.phonemes_for_category(self._phonemeCategorySelection)
  if not phonemes:
   for category_id in categories:
    phonemes = self._phonemeInventory.phonemes_for_category(category_id)
    if phonemes:
     self._phonemeCategorySelection = category_id
     break
   else:
    self._phonemeSelection = None
    return
  valid_names = [definition.name for definition in phonemes]
  if self._phonemeSelection not in valid_names:
   self._phonemeSelection = valid_names[0] if valid_names else None

 def _current_phoneme_definition(self) -> Optional[PhonemeDefinition]:
  if not self._phonemeSelection:
   return None
  return self._phonemeInventory.get(self._phonemeSelection)

 def _reset_replacement_cursor(self):
  self._lastReplacementSelection = None

 def _current_fallback_order(self) -> Tuple[str, ...]:
  order = _PHONEME_FALLBACK_POLICIES.get(self._phonemeFallbackPreference)
  if order is None:
   order = _PHONEME_FALLBACK_POLICIES.get(_PHONEME_FALLBACK_DEFAULT, ("example", "description", "ipa", "name"))
  return order

 def _get_availableVoiceTemplates(self):
  if self._voiceCatalog.is_empty:
   raise UnsupportedConfigParameterError()
  options: "OrderedDict[str, StringParameterInfo]" = OrderedDict()
  options[_VOICE_TEMPLATE_DEFAULT] = StringParameterInfo(
   _VOICE_TEMPLATE_DEFAULT,
   _("Keep Eloquence defaults"),
  )
  for template in self._voiceCatalog:
   label = template.display_label()
   options[template.id] = StringParameterInfo(template.id, label)
  return options

 def _get_voiceTemplate(self):
  if self._voiceCatalog.is_empty:
   raise UnsupportedConfigParameterError()
  options = self._get_availableVoiceTemplates()
  if self._voiceTemplateId and self._voiceTemplateId in options:
   self._lastVoiceTemplateSelection = self._voiceTemplateId
   return self._voiceTemplateId
  if self._lastVoiceTemplateSelection and self._lastVoiceTemplateSelection in options:
   return self._lastVoiceTemplateSelection
  self._lastVoiceTemplateSelection = _VOICE_TEMPLATE_DEFAULT if _VOICE_TEMPLATE_DEFAULT in options else next(iter(options))
  return self._lastVoiceTemplateSelection

 def _set_voiceTemplate(self, value):
  if self._voiceCatalog.is_empty:
   raise UnsupportedConfigParameterError()
  options = self._get_availableVoiceTemplates()
  if value not in options:
   raise ValueError(f"Unknown voice template '{value}'")
  self._lastVoiceTemplateSelection = value
  if value == _VOICE_TEMPLATE_DEFAULT:
   self._voiceTemplateId = None
   self._refresh_language_profile()
   return
  template = self._voiceCatalog.get(value)
  if not template:
   raise ValueError(f"Unknown voice template '{value}'")
  self._voiceTemplateId = template.id
  self._apply_voice_template(template)

 def _apply_voice_template(self, template: VoiceTemplate):
  voice_code = template.base_voice
  if voice_code and voice_code in _eloquence.langs:
   desired_voice = str(_eloquence.langs[voice_code][0])
   if desired_voice != self._get_voice():
    self._set_voice(desired_voice)
  if template.variant:
   self._set_variant(template.variant)
  for name, value in template.parameter_items():
   binding = _VOICE_PARAM_BINDINGS.get(name)
   if binding is None:
    continue
   try:
    numeric = int(value)
   except (TypeError, ValueError):
    continue
   self.setVParam(binding, numeric)
   if name == "rate":
    self._rate = numeric
  self._apply_template_extras(template)
  self._refresh_language_profile(template)

 def _apply_template_extras(self, template: VoiceTemplate) -> None:
  extras = template.extras if isinstance(template.extras, dict) else {}
  if not extras:
   return
  self._apply_template_boolean_settings(template, extras.get("settings"))
  self._apply_template_fallback(template, extras.get("phonemeFallback"))
  overrides = extras.get("phonemeReplacements")
  if isinstance(overrides, dict):
   self._apply_template_phoneme_overrides(template, overrides)

 def _apply_template_boolean_settings(self, template: VoiceTemplate, settings):
  if not isinstance(settings, dict):
   return
  for key, raw_value in settings.items():
   if key not in _TEMPLATE_BOOLEAN_SETTINGS:
    logging.debug(
     "Voice template '%s' requested unsupported toggle '%s'",
     template.id,
     key,
    )
    continue
   setter = getattr(self, f"_set_{key}", None)
   if not callable(setter):
    logging.debug(
     "Voice template '%s' cannot set toggle '%s' because setter is missing",
     template.id,
     key,
    )
    continue
   try:
    setter(bool(raw_value))
   except Exception:
    logging.exception("Unable to apply template toggle '%s' for '%s'", key, template.id)

 def _apply_template_fallback(self, template: VoiceTemplate, preference):
  if not isinstance(preference, str):
   return
  if preference not in _PHONEME_FALLBACK_POLICIES:
   logging.debug(
    "Voice template '%s' supplied unknown phoneme fallback '%s'",
    template.id,
    preference,
   )
   return
  try:
   self._set_phonemeFallback(preference)
  except UnsupportedConfigParameterError:
   logging.debug(
    "Phoneme fallback not available while applying template '%s'",
    template.id,
   )
  except ValueError:
   logging.debug(
    "Template '%s' failed to update phoneme fallback '%s'",
    template.id,
    preference,
   )

 def _apply_template_phoneme_overrides(self, template: VoiceTemplate, overrides: Dict[str, object]):
  if self._phonemeInventory.is_empty:
   return
  changed = False
  for phoneme_id, target in overrides.items():
   if not isinstance(phoneme_id, str):
    continue
   if phoneme_id in self._phonemeReplacements:
    logging.debug(
     "Skipping template override for phoneme '%s' because a user override is present",
     phoneme_id,
    )
    continue
   definition = self._phonemeInventory.get(phoneme_id)
   if definition is None:
    logging.debug(
     "Voice template '%s' references unknown phoneme '%s'",
     template.id,
     phoneme_id,
    )
    continue
   replacement_id: Optional[str] = None
   if isinstance(target, str):
    candidate = target.strip()
    if candidate in definition.replacement_options():
     replacement_id = candidate
    else:
     found = definition.get_replacement(None, (candidate,))
     if found is not None:
      replacement_id = found.id
     else:
      for option in definition.replacement_options().values():
       if option.output == candidate or option.source == candidate:
        replacement_id = option.id
        break
   elif isinstance(target, (list, tuple)):
    for entry in target:
     if not isinstance(entry, str):
      continue
     found = definition.get_replacement(None, (entry,))
     if found is not None:
      replacement_id = found.id
      break
   if not replacement_id:
    logging.debug(
     "Template '%s' could not resolve replacement '%r' for phoneme '%s'",
     template.id,
     target,
     phoneme_id,
    )
    continue
   self._phonemeReplacements[phoneme_id] = replacement_id
   changed = True
 if changed:
  self._persist_phoneme_replacements()
  self._reset_replacement_cursor()

 def _voice_parameter_options(self) -> "OrderedDict[str, StringParameterInfo]":
  options: "OrderedDict[str, StringParameterInfo]" = OrderedDict()
  ranges = self._voiceCatalog.parameter_ranges() if self._voiceCatalog else {}

  def register_option(name: str, range_info: Optional[VoiceParameterRange]):
   if not range_info:
    return
   if name not in _VOICE_PARAM_BINDINGS:
    return
   if name in options:
    return
   label = range_info.label or name
   description = range_info.description.strip()
   if description:
    label = f"{label} – {description}"
   options[name] = StringParameterInfo(name, label)

  for parameter_name in _VOICE_PARAMETER_ORDER:
   register_option(parameter_name, ranges.get(parameter_name))
  for parameter_name, range_info in sorted(ranges.items()):
   register_option(parameter_name, range_info)
  return options

 def _voice_parameter_binding(self) -> Optional[int]:
  if not self._voiceParameterSelection:
   return None
  return _VOICE_PARAM_BINDINGS.get(self._voiceParameterSelection)

 def _current_voice_parameter_range(self) -> Optional[VoiceParameterRange]:
  if not self._voiceParameterSelection or self._voiceCatalog.is_empty:
   return None
  return self._voiceCatalog.parameter_range(self._voiceParameterSelection)

 def _update_voice_parameter_slider(self) -> None:
  setting = VOICE_PARAMETER_VALUE_SETTING
  range_info = self._current_voice_parameter_range()
  if range_info is None:
   setting.minVal = 0
   setting.maxVal = 200
   setting.minStep = 1
   setting.normalStep = max(setting.minStep, 5)
   setting.largeStep = max(setting.normalStep, 10)
   setting.defaultVal = 0
   return
  step = max(1, range_info.step)
  setting.minVal = range_info.minimum
  setting.maxVal = range_info.maximum
  setting.minStep = step
  span = max(range_info.maximum - range_info.minimum, step)
  normal = span // 10 if span // 10 >= step else step
  setting.normalStep = max(step, normal)
  large = span // 4 if span // 4 >= setting.normalStep else setting.normalStep
  setting.largeStep = max(setting.normalStep, large)
  setting.defaultVal = range_info.clamp(range_info.default)

 def _ensure_voice_parameter_selection(self) -> None:
  options = self._voice_parameter_options()
  if not options:
   self._voiceParameterSelection = None
   self._lastVoiceParameterSelection = None
   self._update_voice_parameter_slider()
   return
  if self._voiceParameterSelection in options:
   self._lastVoiceParameterSelection = self._voiceParameterSelection
   self._update_voice_parameter_slider()
   return
  if self._lastVoiceParameterSelection in options:
   self._voiceParameterSelection = self._lastVoiceParameterSelection
   self._update_voice_parameter_slider()
   return
  first = next(iter(options))
  self._voiceParameterSelection = first
  self._lastVoiceParameterSelection = first
  self._update_voice_parameter_slider()

def _default_profile_for_template(self, template: Optional[VoiceTemplate]) -> Optional[str]:
 if template is None:
  return None
 candidate = template.default_language_profile
 if candidate and self._languageProfiles.get(candidate):
  return candidate
 for profile in self._languageProfiles:
  if template.id in profile.default_voice_templates:
   return profile.id
 return None

def _handle_lang_change(self, language_code: Optional[str]) -> None:
 if self._languageProfiles.is_empty:
  return
 new_override: Optional[str] = None
 if language_code:
  profile = self._languageProfiles.find_best_match(language_code)
  if profile:
   new_override = profile.id
 if new_override == self._languageProfileOverrideId:
  return
 self._languageProfileOverrideId = new_override
 self._refresh_language_profile()

def _refresh_language_profile(self, template: Optional[VoiceTemplate] = None):
 if self._languageProfiles.is_empty:
  self._activeLanguageProfileId = None
  return
 if template is None and self._voiceTemplateId:
  template = self._voiceCatalog.get(self._voiceTemplateId)
 if self._languageProfileSelection == _LANGUAGE_PROFILE_DISABLED:
  self._activeLanguageProfileId = None
  return
 if self._languageProfileOverrideId and self._languageProfileSelection in (
  _LANGUAGE_PROFILE_AUTO,
  self._languageProfileOverrideId,
 ):
  override_profile = self._languageProfiles.get(self._languageProfileOverrideId)
  if override_profile:
   self._activeLanguageProfileId = override_profile.id
   return
  if self._languageProfileSelection == _LANGUAGE_PROFILE_AUTO:
   self._languageProfileOverrideId = None
 if self._languageProfileSelection == _LANGUAGE_PROFILE_AUTO:
  profile_id = self._default_profile_for_template(template)
  if profile_id is None and template is None:
   # fall back to the catalogue default if nothing is selected
   default_template = self._voiceCatalog.default_template()
   profile_id = self._default_profile_for_template(default_template)
  if profile_id and self._languageProfiles.get(profile_id):
   self._activeLanguageProfileId = profile_id
  else:
   self._activeLanguageProfileId = None
  return
 if self._languageProfiles.get(self._languageProfileSelection):
  self._activeLanguageProfileId = self._languageProfileSelection
 else:
  self._activeLanguageProfileId = None

 def _active_language_profile(self) -> Optional[LanguageProfile]:
  return self._languageProfiles.get(self._activeLanguageProfileId)

 def _get_availableLanguageProfiles(self):
  if self._languageProfiles.is_empty:
   raise UnsupportedConfigParameterError()
  options: "OrderedDict[str, StringParameterInfo]" = OrderedDict()
  options[_LANGUAGE_PROFILE_AUTO] = StringParameterInfo(
   _LANGUAGE_PROFILE_AUTO,
   _("Follow voice template"),
  )
  options[_LANGUAGE_PROFILE_DISABLED] = StringParameterInfo(
   _LANGUAGE_PROFILE_DISABLED,
   _("Disable language hints"),
  )
  for profile in self._languageProfiles:
   options[profile.id] = StringParameterInfo(profile.id, profile.display_label())
  return options

 def _get_languageProfile(self):
  if self._languageProfiles.is_empty:
   raise UnsupportedConfigParameterError()
  options = self._get_availableLanguageProfiles()
  if self._languageProfileSelection in options:
   return self._languageProfileSelection
  self._languageProfileSelection = _LANGUAGE_PROFILE_AUTO
  self._refresh_language_profile()
  return self._languageProfileSelection

 def _set_languageProfile(self, value):
  if self._languageProfiles.is_empty:
   raise UnsupportedConfigParameterError()
  options = self._get_availableLanguageProfiles()
  if value not in options:
   raise ValueError(f"Unknown language profile '{value}'")
  self._languageProfileSelection = value
  if value == _LANGUAGE_PROFILE_DISABLED:
   self._activeLanguageProfileId = None
   return
  if value == _LANGUAGE_PROFILE_AUTO:
   self._refresh_language_profile()
   return
 if self._languageProfiles.get(value):
  self._activeLanguageProfileId = value
 else:
  self._activeLanguageProfileId = None

 def _get_availableVoiceParameters(self):
  options = self._voice_parameter_options()
  if not options:
   raise UnsupportedConfigParameterError()
  return options

 def _get_voiceParameter(self):
  options = self._get_availableVoiceParameters()
  if self._voiceParameterSelection in options:
   self._lastVoiceParameterSelection = self._voiceParameterSelection
   return self._voiceParameterSelection
  if self._lastVoiceParameterSelection in options:
   self._voiceParameterSelection = self._lastVoiceParameterSelection
   self._update_voice_parameter_slider()
   return self._voiceParameterSelection
  first = next(iter(options))
  self._voiceParameterSelection = first
  self._lastVoiceParameterSelection = first
  self._update_voice_parameter_slider()
  return first

 def _set_voiceParameter(self, value):
  options = self._get_availableVoiceParameters()
  if value not in options:
   raise ValueError(f"Unknown voice parameter '{value}'")
  self._voiceParameterSelection = value
  self._lastVoiceParameterSelection = value
  self._update_voice_parameter_slider()

 def _get_voiceParameterValue(self):
  binding = self._voice_parameter_binding()
  if binding is None:
   raise UnsupportedConfigParameterError()
  try:
   current = int(self.getVParam(binding))
  except Exception:
   range_info = self._current_voice_parameter_range()
   if range_info is None:
    raise
   current = range_info.default
  range_info = self._current_voice_parameter_range()
  if range_info is not None:
   current = range_info.clamp(current)
  return current

 def _set_voiceParameterValue(self, value):
  binding = self._voice_parameter_binding()
  if binding is None:
   raise UnsupportedConfigParameterError()
  try:
   numeric = int(value)
  except (TypeError, ValueError):
   raise ValueError(f"Invalid voice parameter value '{value}'") from None
  range_info = self._current_voice_parameter_range()
  if range_info is not None:
   numeric = range_info.clamp(numeric)
  self.setVParam(binding, numeric)
  if binding == _eloquence.rate:
   self._rate = numeric

 def _get_availablePhonemeCategories(self):
  if self._phonemeInventory.is_empty:
   raise UnsupportedConfigParameterError()
  self._ensure_phoneme_selection()
  options: "OrderedDict[str, StringParameterInfo]" = OrderedDict()
  for category_id, label in self._phonemeInventory.categories.items():
   options[category_id] = StringParameterInfo(category_id, label)
  if not options:
   raise UnsupportedConfigParameterError()
  return options

 def _get_phonemeCategory(self):
  if self._phonemeInventory.is_empty:
   raise UnsupportedConfigParameterError()
  self._ensure_phoneme_selection()
  if not self._phonemeCategorySelection:
   raise UnsupportedConfigParameterError()
  return self._phonemeCategorySelection

 def _set_phonemeCategory(self, value):
  if self._phonemeInventory.is_empty:
   raise UnsupportedConfigParameterError()
  options = self._get_availablePhonemeCategories()
  if value not in options:
   raise ValueError(f"Unknown phoneme category '{value}'")
  if value == self._phonemeCategorySelection:
   return
  self._phonemeCategorySelection = value
  self._phonemeSelection = None
  self._ensure_phoneme_selection()
  self._reset_replacement_cursor()

 def _get_availablePhonemeSymbols(self):
  if self._phonemeInventory.is_empty:
   raise UnsupportedConfigParameterError()
  self._ensure_phoneme_selection()
  if not self._phonemeCategorySelection:
   raise UnsupportedConfigParameterError()
  options: "OrderedDict[str, StringParameterInfo]" = OrderedDict()
  for definition in self._phonemeInventory.phonemes_for_category(self._phonemeCategorySelection):
   options[definition.name] = StringParameterInfo(
    definition.name,
    definition.display_label,
   )
  if not options:
   raise UnsupportedConfigParameterError()
  return options

 def _get_phonemeSymbol(self):
  if self._phonemeInventory.is_empty:
   raise UnsupportedConfigParameterError()
  self._ensure_phoneme_selection()
  if not self._phonemeSelection:
   raise UnsupportedConfigParameterError()
  return self._phonemeSelection

 def _set_phonemeSymbol(self, value):
  if self._phonemeInventory.is_empty:
   raise UnsupportedConfigParameterError()
  options = self._get_availablePhonemeSymbols()
  if value not in options:
   raise ValueError(f"Unknown phoneme symbol '{value}'")
  if value == self._phonemeSelection:
   return
  self._phonemeSelection = value
  self._reset_replacement_cursor()

 def _get_availablePhonemeReplacements(self):
  if self._phonemeInventory.is_empty:
   raise UnsupportedConfigParameterError()
  self._ensure_phoneme_selection()
  definition = self._current_phoneme_definition()
  if not definition:
   raise UnsupportedConfigParameterError()
  replacements = definition.replacement_options()
  if not replacements:
   raise UnsupportedConfigParameterError()
  default_choice = definition.get_replacement(None, self._current_fallback_order())
  active_choice = self._phonemeReplacements.get(definition.name)
  if active_choice is None and default_choice is not None:
   active_choice = default_choice.id
  options: "OrderedDict[str, StringParameterInfo]" = OrderedDict()
  for replacement_id, replacement in replacements.items():
   entry_id = f"{definition.name}::{replacement_id}"
   label = self._format_replacement_label(
    definition,
    replacement,
    active_choice == replacement_id,
    default_choice is not None and replacement_id == default_choice.id,
   )
   options[entry_id] = StringParameterInfo(entry_id, label)
  return options

 def _get_phonemeReplacement(self):
  if self._phonemeInventory.is_empty:
   raise UnsupportedConfigParameterError()
  options = self._get_availablePhonemeReplacements()
  if self._lastReplacementSelection in options:
   return self._lastReplacementSelection
  for entry_id in options:
   try:
    phoneme_id, replacement_id = entry_id.split("::", 1)
   except ValueError:
    continue
   definition = self._phonemeInventory.get(phoneme_id)
   if not definition:
    continue
   default_choice = definition.get_replacement(None, self._current_fallback_order())
   active_choice = self._phonemeReplacements.get(phoneme_id)
   if active_choice is None and default_choice is not None:
    active_choice = default_choice.id
   if active_choice == replacement_id:
    self._lastReplacementSelection = entry_id
    return entry_id
  first = next(iter(options), None)
  if first is None:
   raise UnsupportedConfigParameterError()
  self._lastReplacementSelection = first
  return first

 def _set_phonemeReplacement(self, value):
  if self._phonemeInventory.is_empty:
   raise UnsupportedConfigParameterError()
  try:
   phoneme_id, replacement_id = value.split("::", 1)
  except ValueError as error:
   raise ValueError("Invalid phoneme replacement identifier") from error
  definition = self._phonemeInventory.get(phoneme_id)
  if not definition:
   raise ValueError(f"Unknown phoneme '{phoneme_id}'")
  category_id = self._phonemeInventory.category_for(phoneme_id)
  if category_id:
   self._phonemeCategorySelection = category_id
  self._phonemeSelection = phoneme_id
  options = definition.replacement_options()
  if replacement_id not in options:
   raise ValueError(f"Unknown replacement '{replacement_id}' for phoneme '{phoneme_id}'")
  default_choice = definition.get_replacement(None, self._current_fallback_order())
  if default_choice is not None and replacement_id == default_choice.id:
   self._phonemeReplacements.pop(phoneme_id, None)
  else:
   self._phonemeReplacements[phoneme_id] = replacement_id
  self._persist_phoneme_replacements()
  self._lastReplacementSelection = value

 def _get_availablePhonemeFallbacks(self):
  if self._phonemeInventory.is_empty:
   raise UnsupportedConfigParameterError()
  options: "OrderedDict[str, StringParameterInfo]" = OrderedDict()
  for policy_id in _PHONEME_FALLBACK_POLICIES:
   if policy_id == "examplesFirst":
    # Translators: choice describing the default fallback order for phoneme replacements.
    label = _("Prefer sample words")
   elif policy_id == "descriptionsFirst":
    # Translators: choice describing the default fallback order for phoneme replacements.
    label = _("Prefer descriptions")
   elif policy_id == "ipaFirst":
    # Translators: choice describing the default fallback order for phoneme replacements.
    label = _("Prefer IPA symbols")
   else:
    # Translators: choice describing the default fallback order for phoneme replacements.
    label = _("Prefer engine symbols")
   options[policy_id] = StringParameterInfo(policy_id, label)
  return options

 def _get_phonemeFallback(self):
  if self._phonemeInventory.is_empty:
   raise UnsupportedConfigParameterError()
  if self._phonemeFallbackPreference not in _PHONEME_FALLBACK_POLICIES:
   self._phonemeFallbackPreference = _PHONEME_FALLBACK_DEFAULT
  return self._phonemeFallbackPreference

 def _set_phonemeFallback(self, value):
  if self._phonemeInventory.is_empty:
   raise UnsupportedConfigParameterError()
  if value not in _PHONEME_FALLBACK_POLICIES:
   raise ValueError(f"Unknown phoneme fallback policy '{value}'")
  if value == self._phonemeFallbackPreference:
   return
  self._phonemeFallbackPreference = value
  self._reset_replacement_cursor()
  self._persist_phoneme_replacements()

 def _load_stored_phoneme_replacements(self):
  if self._phonemeInventory.is_empty:
   return
  try:
   speech_section = config.conf.get("speech")
  except Exception:
   speech_section = None
  if not isinstance(speech_section, dict):
   return
  synth_section = speech_section.get(self.name)
  if not isinstance(synth_section, dict):
   return
  stored = synth_section.get("phonemeReplacements", {})
  if not isinstance(stored, dict):
   return
  cleaned: Dict[str, str] = {}
  changed = False
  for phoneme_id, replacement_id in stored.items():
   if not isinstance(phoneme_id, str) or not isinstance(replacement_id, str):
    changed = True
    continue
   definition = self._phonemeInventory.get(phoneme_id)
   if not definition:
    changed = True
    continue
   options = definition.replacement_options()
   if replacement_id not in options:
    changed = True
    continue
   cleaned[phoneme_id] = replacement_id
  fallback_policy = synth_section.get("phonemeFallback")
  if isinstance(fallback_policy, str) and fallback_policy in _PHONEME_FALLBACK_POLICIES:
   self._phonemeFallbackPreference = fallback_policy
  elif fallback_policy is not None:
   changed = True
  self._phonemeReplacements = cleaned
  if changed or len(cleaned) != len(stored) or fallback_policy not in (None, self._phonemeFallbackPreference):
   self._persist_phoneme_replacements()

 def _persist_phoneme_replacements(self):
  try:
   speech_section = config.conf.setdefault("speech", {})
  except Exception:
   return
  synth_section = speech_section.setdefault(self.name, {})
  if self._phonemeReplacements:
   synth_section["phonemeReplacements"] = dict(self._phonemeReplacements)
  else:
   synth_section.pop("phonemeReplacements", None)
  if self._phonemeFallbackPreference != _PHONEME_FALLBACK_DEFAULT:
   synth_section["phonemeFallback"] = self._phonemeFallbackPreference
  else:
   synth_section.pop("phonemeFallback", None)

 def _format_replacement_label(
  self,
  definition: PhonemeDefinition,
  replacement: PhonemeReplacement,
  is_active: bool,
  is_default: bool,
 ) -> str:
  if replacement.kind == "example":
   # Translators: label for a phoneme replacement option derived from an example word.
   base = _("Example: {word}").format(word=replacement.source)
  elif replacement.kind == "description":
   # Translators: label for a phoneme replacement option derived from a description.
   base = _("Description: {description}").format(description=replacement.source)
  elif replacement.kind == "ipa":
   # Translators: label for a phoneme replacement option derived from an IPA symbol.
   base = _("IPA: {ipa}").format(ipa=replacement.source)
  elif replacement.kind == "name":
   # Translators: label for a phoneme replacement option derived from the internal engine symbol.
   base = _("Engine symbol: {symbol}").format(symbol=replacement.source)
  else:
   base = replacement.source
  status_parts: List[str] = []
  if is_active:
   # Translators: short status tag shown for the currently selected phoneme replacement mapping.
   status_parts.append(_("current"))
  elif is_default:
   # Translators: short status tag shown for the default phoneme replacement mapping.
   status_parts.append(_("default"))
  status = f" [{', '.join(status_parts)}]" if status_parts else ""
  return f"{definition.display_label} → {base}{status}"

 def pause(self,switch):
  _eloquence.pause(switch)
  #  self.dll.eciPause(self.handle,switch)

 def terminate(self):
  _eloquence.terminate()
 _backquoteVoiceTags=False
 _ABRDICT=False
 _phrasePrediction=False
 def _get_backquoteVoiceTags(self):
  return self._backquoteVoiceTags

 def _set_backquoteVoiceTags(self, enable):
  if enable == self._backquoteVoiceTags:
   return
  self._backquoteVoiceTags = enable
 def _get_ABRDICT(self):
  return self._ABRDICT
 def _set_ABRDICT(self, enable):
  if enable == self._ABRDICT:
   return
  self._ABRDICT = enable 
 def _get_phrasePrediction(self):
  return self._phrasePrediction
 def _set_phrasePrediction(self, enable):
  if enable == self._phrasePrediction:
   return
  self._phrasePrediction = enable
 def _get_rate(self):
  return self._paramToPercent(self.getVParam(_eloquence.rate),minRate,maxRate)

 def _set_rate(self,vl):
  self._rate = self._percentToParam(vl,minRate,maxRate)
  self.setVParam(_eloquence.rate,self._percentToParam(vl,minRate,maxRate))

 def _get_pitch(self):
  return self.getVParam(_eloquence.pitch)

 def _set_pitch(self,vl):
  self.setVParam(_eloquence.pitch,vl)

 def _get_volume(self):
  return self.getVParam(_eloquence.vlm)

 def _set_volume(self,vl):
  self.setVParam(_eloquence.vlm,int(vl))

 def _set_inflection(self,vl):
  vl = int(vl)
  self.setVParam(_eloquence.fluctuation,vl)

 def _get_inflection(self):
  return self.getVParam(_eloquence.fluctuation)
 def _set_hsz(self,vl):
  vl = int(vl)
  self.setVParam(_eloquence.hsz,vl)

 def _get_hsz(self):
  return self.getVParam(_eloquence.hsz)

 def _set_rgh(self,vl):
  vl = int(vl)
  self.setVParam(_eloquence.rgh,vl)

 def _get_rgh(self):
  return self.getVParam(_eloquence.rgh)

 def _set_bth(self,vl):
  vl = int(vl)
  self.setVParam(_eloquence.bth,vl)

 def _get_bth(self):
  return self.getVParam(_eloquence.bth)

 def _getAvailableVoices(self):
  o = OrderedDict()
  voice_dir = getattr(_eloquence, "voiceDirectory", os.path.join(os.path.dirname(__file__), "eloquence"))
  try:
   entries = os.listdir(voice_dir)
  except FileNotFoundError:
   logging.error("Eloquence voice directory not found: %s", voice_dir)
   return o
  for name in sorted(entries):
   if not name.lower().endswith('.syn'):
    continue
   key = os.path.splitext(name)[0].lower()
   info = _eloquence.langs.get(key)
   if not info:
    continue
   o[str(info[0])] = synthDriverHandler.VoiceInfo(str(info[0]), info[1], None)
  return o

 def _get_voice(self):
  return str(_eloquence.params[9])
 def _set_voice(self,vl):
  _eloquence.set_voice(vl)
  self.curvoice = vl
 def getVParam(self,pr):
  return _eloquence.getVParam(pr)

 def setVParam(self, pr,vl):
  _eloquence.setVParam(pr, vl)

 def _get_lastIndex(self):
  #fix?
  return _eloquence.lastindex

 def cancel(self):
  _eloquence.stop()

 def _getAvailableVariants(self):
  
  global variants
  return OrderedDict((str(id), synthDriverHandler.VoiceInfo(str(id), name)) for id, name in variants.items())

 def _set_variant(self, v):
  global variants
  self._variant = v if int(v) in variants else "1"
  _eloquence.setVariant(int(v))
  self.setVParam(_eloquence.rate, self._rate)
  #  if 'eloquence' in config.conf['speech']:
  #   config.conf['speech']['eloquence']['pitch'] = self.pitch

 def _get_variant(self): return self._variant
 
 def _onIndexReached(self, index):
  if index is not None:
   synthIndexReached.notify(synth=self, index=index)
  else:
   synthDoneSpeaking.notify(synth=self)
 

def resub(dct, s):
 for r in dct.keys():
  s = r.sub(dct[r], s)
 return s
