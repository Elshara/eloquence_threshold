# Copyright (C) 2009-2019 eloquence fans
# synthDrivers/eci.py
# todo: possibly add to this
import driverHandler
import logging
import threading
import nvwave
import re
import config
import os
import synthDriverHandler
from synthDriverHandler import SynthDriver, VoiceInfo
import unicodedata
from typing import Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import OrderedDict
from .voice_parameters import ADVANCED_VOICE_PARAMETER_SPECS
from .language_profiles import (
    LanguageProfile,
    LanguageProfileCatalog,
    load_default_language_profiles,
)
from .voice_catalog import (
    VoiceCatalog,
    VoiceTemplate,
    VoiceParameterRange,
    load_default_voice_catalog,
)
from .phoneme_customizer import (
    PHONEME_EQ_DEFAULT_FILTER,
    PHONEME_EQ_MAX_Q,
    PHONEME_EQ_MIN_Q,
    PhonemeCustomizer,
    PhonemeEqBand,
    VALID_FILTER_TYPES,
)
from .phoneme_catalog import PhonemeDefinition, PhonemeInventory, PhonemeReplacement, load_default_inventory
from . import _eloquence
from synthDriverHandler import SynthDriver, VoiceInfo, synthIndexReached, synthDoneSpeaking
from ctypes import wintypes
import ctypes.wintypes
from ctypes import *
import speech
import tones
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

_VOICE_PARAMETER_VALUE_BASE_LABEL = VOICE_PARAMETER_VALUE_SETTING.displayName


@dataclass
class VoiceParameterBinding:
    name: str
    engine_param: Optional[int] = None
    getter: Optional[Callable[["EloquenceSynthDriver"], int]] = None
    setter: Optional[Callable[["EloquenceSynthDriver", int], int]] = None

    def get_value(self, driver: "EloquenceSynthDriver") -> int:
        if self.getter:
            return int(self.getter(driver))
        if self.engine_param is not None:
            return int(driver.getVParam(self.engine_param))
        raise UnsupportedConfigParameterError()

    def set_value(self, driver: "EloquenceSynthDriver", value: int) -> int:
        if self.setter:
            return int(self.setter(driver, int(value)))
        if self.engine_param is not None:
            driver.setVParam(self.engine_param, int(value))
            return int(value)
        raise UnsupportedConfigParameterError()

    def targets_engine_param(self, param: int) -> bool:
        return self.engine_param == param


_SAMPLE_RATE_MIN, _SAMPLE_RATE_MAX = _eloquence.getSampleRateBounds()
_SAMPLE_RATE_DEFAULT = _eloquence.getDefaultSampleRate()
SAMPLE_RATE_SETTING = NumericDriverSetting(
    "sampleRate",
    _("Sample &rate (Hz)"),
    availableInSettingsRing=True,
    minVal=_SAMPLE_RATE_MIN,
    maxVal=_SAMPLE_RATE_MAX,
    minStep=50,
    normalStep=500,
    largeStep=2000,
    displayName=_("Sample rate (Hz)"),
)
SAMPLE_RATE_SETTING.defaultVal = _SAMPLE_RATE_DEFAULT


_PHONEME_EQ_LAYER_MIN = 1
_PHONEME_EQ_LAYER_MAX = 32
_PHONEME_EQ_LOW_MIN = 1
_PHONEME_EQ_HIGH_MAX = 384000
_PHONEME_EQ_GAIN_MIN = -24
_PHONEME_EQ_GAIN_MAX = 12
_PHONEME_EQ_Q_SCALE = 100
_PHONEME_EQ_Q_MIN = int(round(PHONEME_EQ_MIN_Q * _PHONEME_EQ_Q_SCALE))
_PHONEME_EQ_Q_MAX = int(round(PHONEME_EQ_MAX_Q * _PHONEME_EQ_Q_SCALE))

_PHONEME_EQ_FILTER_LABELS = {
    "peaking": _("Peaking / bell"),
    "lowShelf": _("Low shelf"),
    "highShelf": _("High shelf"),
    "lowPass": _("Low-pass"),
    "highPass": _("High-pass"),
    "bandPass": _("Band-pass"),
    "notch": _("Notch"),
    "allPass": _("All-pass"),
}


PHONEME_EQ_LAYER_SETTING = NumericDriverSetting(
    "phonemeEqLayer",
    _("Phoneme EQ &layer"),
    availableInSettingsRing=True,
    minVal=_PHONEME_EQ_LAYER_MIN,
    maxVal=_PHONEME_EQ_LAYER_MAX,
    minStep=1,
    normalStep=1,
    largeStep=4,
    displayName=_("Phoneme EQ layer"),
)

PHONEME_EQ_LOW_SETTING = NumericDriverSetting(
    "phonemeEqLow",
    _("Phoneme EQ &low (Hz)"),
    availableInSettingsRing=True,
    minVal=_PHONEME_EQ_LOW_MIN,
    maxVal=_PHONEME_EQ_HIGH_MAX,
    minStep=10,
    normalStep=50,
    largeStep=500,
    displayName=_("Phoneme EQ low (Hz)"),
)

PHONEME_EQ_HIGH_SETTING = NumericDriverSetting(
    "phonemeEqHigh",
    _("Phoneme EQ hi&gh (Hz)"),
    availableInSettingsRing=True,
    minVal=_PHONEME_EQ_LOW_MIN + 1,
    maxVal=_PHONEME_EQ_HIGH_MAX,
    minStep=10,
    normalStep=50,
    largeStep=500,
    displayName=_("Phoneme EQ high (Hz)"),
)

PHONEME_EQ_GAIN_SETTING = NumericDriverSetting(
    "phonemeEqGain",
    _("Phoneme EQ g&ain (dB)"),
    availableInSettingsRing=True,
    minVal=_PHONEME_EQ_GAIN_MIN,
    maxVal=_PHONEME_EQ_GAIN_MAX,
    minStep=1,
    normalStep=2,
    largeStep=4,
    displayName=_("Phoneme EQ gain (dB)"),
)

PHONEME_EQ_FILTER_SETTING = DriverSetting(
    "phonemeEqFilter",
    _("Phoneme EQ &filter"),
    availableInSettingsRing=True,
    displayName=_("Phoneme EQ filter"),
)

PHONEME_EQ_Q_SETTING = NumericDriverSetting(
    "phonemeEqQ",
    _("Phoneme EQ &Q (×100)"),
    availableInSettingsRing=True,
    minVal=_PHONEME_EQ_Q_MIN,
    maxVal=_PHONEME_EQ_Q_MAX,
    minStep=1,
    normalStep=10,
    largeStep=100,
    displayName=_("Phoneme EQ Q (×100)"),
)


punctuation = ",.?:;"
punctuation = [x for x in punctuation]

minRate = 40
maxRate = 150
pause_re = re.compile(r'([a-zA-Z])([.(),:;!?])( |$)')
time_re = re.compile(r"(\d):(\d+):(\d+)")
english_fixes = {
    re.compile(r'(\w+)\.([a-zA-Z]+)'): r'\1 dot \2',
    re.compile(r'([a-zA-Z0-9_]+)@(\w+)'): r'\1 at \2',
    # Does not occur in normal use, however if a dictionary entry contains the Mc prefix, and NVDA splits it up, the synth will crash.
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
    # for emails
    re.compile(r'([a-zA-Z0-9_]+)@(\w+)'): r'\1 arroba \2',
}
german_fixes = {
    # Crash words
    re.compile(r'dane-ben', re.I): r'dane- ben',
    re.compile(r'dage-gen', re.I): r'dage- gen',
}
variants = {1: "Reed",
            2: "Shelley",
            3: "Bobby",
            4: "Rocko",
            5: "Glen",
            6: "Sandy",
            7: "Grandma",
            8: "Grandpa"}

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
    supportedSettings = (
        SynthDriver.VoiceSetting(),
        SynthDriver.VariantSetting(),
        SynthDriver.RateSetting(),
        SynthDriver.PitchSetting(),
        SynthDriver.InflectionSetting(),
        SynthDriver.VolumeSetting(),
        NumericDriverSetting("hsz", "Head Size"),
        NumericDriverSetting("rgh", "Roughness"),
        NumericDriverSetting("bth", "Breathiness"),
        NumericDriverSetting("gender", _("Gender")),
        BooleanDriverSetting("backquoteVoiceTags", "Enable backquote voice &tags", True),
        BooleanDriverSetting("ABRDICT", "Enable &abbreviation dictionary", False),
        BooleanDriverSetting("phrasePrediction", "Enable phrase prediction", False),
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
        SAMPLE_RATE_SETTING,
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
        PHONEME_EQ_LAYER_SETTING,
        PHONEME_EQ_LOW_SETTING,
        PHONEME_EQ_HIGH_SETTING,
        PHONEME_EQ_GAIN_SETTING,
        PHONEME_EQ_FILTER_SETTING,
        PHONEME_EQ_Q_SETTING,
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
    _phonemeCustomizer: PhonemeCustomizer
    _phonemeEqLayerSelection: int
    PROSODY_ATTRS = {
        PitchCommand: _eloquence.pitch,
        VolumeCommand: _eloquence.vlm,
        RateCommand: _eloquence.rate,
    }
    _VOICE_TEMPLATE_DEFAULT = "engine-default"
    _LANGUAGE_PROFILE_AUTO = "auto"
    _LANGUAGE_PROFILE_DISABLED = "disabled"
    _VOICE_PARAMETER_ORDER = (
        "gender",
        "rate",
        "pitch",
        "inflection",
        "headSize",
        "roughness",
        "breathiness",
        "volume",
        "emphasis",
        "stress",
        "timbre",
        "tone",
        "vocalLayers",
        "overtones",
        "subtones",
        "vocalRange",
        "smoothness",
        "whisper",
        "toneSize",
        "scopeDepth",
    )
    _VOICE_PARAM_BINDINGS: Dict[str, VoiceParameterBinding] = {}
    _TEMPLATE_BOOLEAN_SETTINGS = {"backquoteVoiceTags", "ABRDICT", "phrasePrediction"}

    description = 'ETI-Eloquence'
    name = 'eloquence'

    @classmethod
    def check(cls):
        return _eloquence.eciCheck()

    def _load_startup_preferences(self):
        try:
            speech_section = config.conf.get("speech")
        except Exception:
            speech_section = None
        if not isinstance(speech_section, dict):
            return
        synth_section = speech_section.get(self.name)
        if not isinstance(synth_section, dict):
            return
        stored_rate = synth_section.get("sampleRate")
        if stored_rate is None:
            return
        try:
            _eloquence.setSampleRate(int(stored_rate))
        except Exception:
            logging.exception("Unable to restore stored sample rate '%s'", stored_rate)
        else:
            self._persist_sample_rate()

    def __init__(self):
        self._load_startup_preferences()
        _eloquence.initialize(self._onIndexReached)
        self.curvoice = "enu"
        self.rate = 50
        self.variant = "1"
        self._phonemeInventory = load_default_inventory()
        self._phonemeReplacements = {}
        self._phonemeFallbackPreference = _PHONEME_FALLBACK_DEFAULT
        self._load_stored_phoneme_replacements()
        self._lastReplacementSelection = None
        self._phonemeCategorySelection = None
        self._phonemeSelection = None
        self._ensure_phoneme_selection()
        self._phonemeCustomizer = PhonemeCustomizer(
            low_min=_PHONEME_EQ_LOW_MIN,
            high_max=_PHONEME_EQ_HIGH_MAX,
            gain_min=_PHONEME_EQ_GAIN_MIN,
            gain_max=_PHONEME_EQ_GAIN_MAX,
        )
        try:
            active_rate = self._get_sampleRate()
        except Exception:
            active_rate = _SAMPLE_RATE_DEFAULT
        self._phonemeCustomizer.set_sample_rate(active_rate)
        self._phonemeEqLayerSelection = _PHONEME_EQ_LAYER_MIN
        self._load_advanced_voice_parameters()
        self._load_stored_phoneme_eq_profiles()
        self._ensure_phoneme_eq_defaults()
        self._update_phoneme_eq_engine()
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
                    factor = 1.0 * coefficients[ra] + \
                        (coefficients[rb] - coefficients[ra]) * (self.rate - ra) / (rb - ra)
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

    def xspeakText(self, text, should_pause=False):
        # Presumably dashes are handled as symbols by NVDA symbol processing, so strip extra ones to avoid too many dashes.
        text = text.replace("-", " ")
        if _eloquence.params[9] == 65536 or _eloquence.params[9] == 65537:
            text = resub(english_fixes, text)
        if _eloquence.params[9] == 131072 or _eloquence.params[9] == 131073:
            text = resub(spanish_fixes, text)
        if _eloquence.params[9] in (196609, 196608):
            text = resub(french_fixes, text)
        if _eloquence.params[9] in ('deu', 262144):
            text = resub(german_fixes, text)
        # this converts to ansi for anticrash. If this breaks with foreign langs, we can remove it.
        # text = text.encode('mbcs')
        text = normalizeText(text)
        if not self._backquoteVoiceTags:
            text = text.replace('`', ' ')
        text = "`vv%d %s" % (self.getVParam(_eloquence.vlm), text)  # no embedded commands
        text = pause_re.sub(r'\1 `p1\2\3', text)
        text = time_re.sub(r'\1:\2 \3', text)
        if self._ABRDICT:
            text = "`da1 "+text
        else:
            text = "`da0 "+text
        if self._phrasePrediction:
            text = "`pp1 "+text
        else:
            text = "`pp0 "+text
        # if two strings are sent separately, pause between them. This might fix some of the audio issues we're having.
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
    self._ensure_phoneme_eq_defaults()


def _load_stored_phoneme_eq_profiles(self):
    try:
        speech_section = config.conf.get("speech", {})
    except Exception:
        speech_section = {}
    if not isinstance(speech_section, dict):
        speech_section = {}
    synth_section = speech_section.get(self.name, {})
    if not isinstance(synth_section, dict):
        return
    stored = synth_section.get("phonemeEqProfiles")
    if isinstance(stored, dict):
        self._phonemeCustomizer.load_per_phoneme(stored)

    def _load_advanced_voice_parameters(self) -> None:
        try:
            speech_section = config.conf.get("speech", {})
        except Exception:
            speech_section = {}
        if not isinstance(speech_section, dict):
            speech_section = {}
        synth_section = speech_section.get(self.name, {})
        if not isinstance(synth_section, dict):
            return
        stored = synth_section.get("advancedVoiceParameters")
        if isinstance(stored, dict):
            self._phonemeCustomizer.apply_global_parameters(stored)


def _ensure_phoneme_eq_defaults(self):
    if self._phonemeSelection:
        total = self._phonemeCustomizer.layer_count(self._phonemeSelection)
        if total <= 0:
            total = 1
        if self._phonemeEqLayerSelection > total:
            self._phonemeEqLayerSelection = total
    if self._phonemeEqLayerSelection < _PHONEME_EQ_LAYER_MIN:
        self._phonemeEqLayerSelection = _PHONEME_EQ_LAYER_MIN


def _ensure_eq_layers(self, phoneme_id: str, layer: int) -> List[PhonemeEqBand]:
    return self._phonemeCustomizer.ensure_layers(phoneme_id, layer)


def _current_eq_band(self, writable: bool = False) -> Optional[PhonemeEqBand]:
    phoneme_id = self._phonemeSelection
    if not phoneme_id:
        return None
    index = max(0, self._phonemeEqLayerSelection - 1)
    if writable:
        bands = self._ensure_eq_layers(phoneme_id, index + 1)
        return bands[index]
    bands = self._phonemeCustomizer.per_phoneme_bands().get(phoneme_id)
    if bands and index < len(bands):
        return bands[index]
    return PhonemeEqBand.default()


def _collect_eq_payload(self) -> List[Dict[str, object]]:
    return self._phonemeCustomizer.build_engine_payload()


def _update_phoneme_eq_engine(self):
    _eloquence.setPhonemeEqBands(self._collect_eq_payload())


def _persist_phoneme_eq_profiles(self):
    try:
        speech_section = config.conf.setdefault("speech", {})
    except Exception:
        return
    synth_section = speech_section.setdefault(self.name, {})
    serialisable = self._phonemeCustomizer.serialise_per_phoneme()
    if serialisable:
        synth_section["phonemeEqProfiles"] = serialisable
    else:
        synth_section.pop("phonemeEqProfiles", None)


def _persist_advanced_voice_parameters(self) -> None:
    try:
        speech_section = config.conf.setdefault("speech", {})
    except Exception:
        return
    synth_section = speech_section.setdefault(self.name, {})
    values = self._phonemeCustomizer.global_parameter_values()
    defaults = {name: int(spec.get("default", 100)) for name, spec in ADVANCED_VOICE_PARAMETER_SPECS.items()}
    if any(values.get(name, defaults.get(name)) != defaults.get(name) for name in ADVANCED_VOICE_PARAMETER_SPECS):
        synth_section["advancedVoiceParameters"] = values
    else:
        synth_section.pop("advancedVoiceParameters", None)

    def _advanced_parameter_value(self, name: str) -> int:
        return self._phonemeCustomizer.global_parameter_value(name)

    def _apply_advanced_parameter(self, name: str, value: int) -> int:
        applied = self._phonemeCustomizer.set_global_parameter(name, value)
        self._persist_advanced_voice_parameters()
        self._update_phoneme_eq_engine()
        return applied

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
        self._lastVoiceTemplateSelection = _VOICE_TEMPLATE_DEFAULT if _VOICE_TEMPLATE_DEFAULT in options else next(
            iter(options))
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
            if name == "sampleRate":
                try:
                    self._set_sampleRate(int(value))
                except Exception:
                    logging.exception("Unable to apply sample rate '%s' for template '%s'", value, template.id)
                continue
            binding = _VOICE_PARAM_BINDINGS.get(name)
            if binding is None:
                continue
            try:
                numeric = int(value)
            except (TypeError, ValueError):
                continue
            range_info = self._voiceCatalog.parameter_range(name)
            if range_info is not None:
                numeric = range_info.clamp(numeric)
            applied = binding.set_value(self, numeric)
            if binding.targets_engine_param(_eloquence.rate):
                self._rate = applied
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


def _voice_parameter_binding(self) -> Optional[VoiceParameterBinding]:
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
    label = _VOICE_PARAMETER_VALUE_BASE_LABEL
    try:
        options = self._voice_parameter_options()
    except UnsupportedConfigParameterError:
        options = None
    else:
        if options and self._voiceParameterSelection in options:
            selected = options[self._voiceParameterSelection]
            display = getattr(selected, "displayName", None)
            if display:
                label = f"{_VOICE_PARAMETER_VALUE_BASE_LABEL} ({display})"
    setting.displayName = label
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
            label = self._describe_language_profile_option(profile)
            options[profile.id] = StringParameterInfo(profile.id, label)
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

    def _describe_language_profile_option(self, profile: LanguageProfile) -> str:
        metrics = profile.metrics(self._phonemeInventory)
        extras = []
        coverage = metrics.get("ipaCoveragePercent")
        if isinstance(coverage, (int, float)):
            extras.append(f"{coverage:.0f}% IPA")
        stage = metrics.get("stage")
        if stage:
            extras.append(stage.replace("-", " ").title())
        examples = metrics.get("exampleCount", 0)
        if isinstance(examples, int) and examples:
            extras.append(f"{examples} examples")
        matched_defaults = []
        for template_id in metrics.get("defaultVoiceTemplates", []):
            template = self._voiceCatalog.get(template_id)
            if template is not None:
                matched_defaults.append(template_id)
        if matched_defaults:
            count = len(matched_defaults)
            suffix = "s" if count != 1 else ""
            extras.append(f"{count} default template{suffix}")
        if metrics.get("keyboardOptimised"):
            extras.append("Keyboard digraphs")
        if metrics.get("hasGenerativeHints"):
            extras.append("Generative variants")
        if metrics.get("hasContextualHints"):
            extras.append("Contextual pronunciation")
        if extras:
            return f"{profile.display_label()} ({'; '.join(extras)})"
        return profile.display_label()

    def describe_language_progress(self) -> Optional[str]:
        profile = self._active_language_profile()
        if not profile:
            return None
        metrics = profile.metrics(self._phonemeInventory)
        pieces = [profile.display_label()]
        coverage = metrics.get("ipaCoveragePercent")
        if isinstance(coverage, (int, float)):
            pieces.append(f"{coverage:.0f}% IPA coverage")
        stage = metrics.get("stage")
        if stage:
            pieces.append(stage.replace("-", " ").title())
        examples = metrics.get("exampleCount", 0)
        if isinstance(examples, int) and examples:
            pieces.append(f"{examples} documented examples")
        notes_total = (
            int(metrics.get("stressNoteCount", 0))
            + int(metrics.get("sentenceStructureNoteCount", 0))
            + int(metrics.get("grammarNoteCount", 0))
        )
        if notes_total:
            pieces.append(f"{notes_total} structural notes")
        available = metrics.get("availableTemplateCount")
        if isinstance(available, int) and available:
            pieces.append(f"{available} template options")
        return ", ".join(pieces)

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
            current = binding.get_value(self)
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
        applied = binding.set_value(self, numeric)
        if binding.targets_engine_param(_eloquence.rate):
            self._rate = applied

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
    self._phonemeEqLayerSelection = _PHONEME_EQ_LAYER_MIN
    self._ensure_phoneme_eq_defaults()

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

    def _current_sample_rate_limit(self) -> int:
        try:
            active_rate = int(_eloquence.getSampleRate())
        except Exception:
            active_rate = _SAMPLE_RATE_DEFAULT
        upper = active_rate // 2 if active_rate > 0 else _PHONEME_EQ_HIGH_MAX
        return max(_PHONEME_EQ_LOW_MIN + 1, min(upper, _PHONEME_EQ_HIGH_MAX))

    def _get_phonemeEqLayer(self):
        if self._phonemeInventory.is_empty:
            raise UnsupportedConfigParameterError()
        self._ensure_phoneme_selection()
        self._ensure_phoneme_eq_defaults()
        return self._phonemeEqLayerSelection

    def _set_phonemeEqLayer(self, value):
        if self._phonemeInventory.is_empty:
            raise UnsupportedConfigParameterError()
        self._ensure_phoneme_selection()
        if not self._phonemeSelection:
            raise UnsupportedConfigParameterError()
        try:
            layer = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid phoneme EQ layer '{value}'") from None
        if layer < _PHONEME_EQ_LAYER_MIN or layer > _PHONEME_EQ_LAYER_MAX:
            raise ValueError(f"Invalid phoneme EQ layer '{layer}'")
        if layer == self._phonemeEqLayerSelection:
            return
        self._ensure_eq_layers(self._phonemeSelection, layer)
        self._phonemeEqLayerSelection = layer
        self._ensure_phoneme_eq_defaults()
        self._persist_phoneme_eq_profiles()
        self._update_phoneme_eq_engine()

    def _get_phonemeEqLow(self):
        if self._phonemeInventory.is_empty:
            raise UnsupportedConfigParameterError()
        self._ensure_phoneme_selection()
        band = self._current_eq_band()
        if not band:
            raise UnsupportedConfigParameterError()
        return int(band.low_hz)

    def _set_phonemeEqLow(self, value):
        if self._phonemeInventory.is_empty:
            raise UnsupportedConfigParameterError()
        self._ensure_phoneme_selection()
        band = self._current_eq_band(writable=True)
        if not band:
            raise UnsupportedConfigParameterError()
        try:
            numeric = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid phoneme EQ low frequency '{value}'") from None
        upper_limit = self._current_sample_rate_limit() - 1
        numeric = max(_PHONEME_EQ_LOW_MIN, min(numeric, upper_limit))
        changed = False
        if numeric != band.low_hz:
            band.low_hz = numeric
            changed = True
        if band.high_hz <= band.low_hz:
            band.high_hz = min(self._current_sample_rate_limit(), band.low_hz + 1)
            changed = True
        if changed:
            self._phonemeCustomizer.set_band(self._phonemeSelection, self._phonemeEqLayerSelection - 1, band)
            self._persist_phoneme_eq_profiles()
            self._update_phoneme_eq_engine()

    def _get_phonemeEqHigh(self):
        if self._phonemeInventory.is_empty:
            raise UnsupportedConfigParameterError()
        self._ensure_phoneme_selection()
        band = self._current_eq_band()
        if not band:
            raise UnsupportedConfigParameterError()
        return int(band.high_hz)

    def _set_phonemeEqHigh(self, value):
        if self._phonemeInventory.is_empty:
            raise UnsupportedConfigParameterError()
        self._ensure_phoneme_selection()
        band = self._current_eq_band(writable=True)
        if not band:
            raise UnsupportedConfigParameterError()
        try:
            numeric = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid phoneme EQ high frequency '{value}'") from None
        upper = self._current_sample_rate_limit()
        numeric = max(band.low_hz + 1, min(numeric, upper))
        if numeric != band.high_hz:
            band.high_hz = numeric
            self._phonemeCustomizer.set_band(self._phonemeSelection, self._phonemeEqLayerSelection - 1, band)
            self._persist_phoneme_eq_profiles()
            self._update_phoneme_eq_engine()

    def _get_phonemeEqGain(self):
        if self._phonemeInventory.is_empty:
            raise UnsupportedConfigParameterError()
        self._ensure_phoneme_selection()
        band = self._current_eq_band()
        if not band:
            raise UnsupportedConfigParameterError()
        return int(round(band.gain_db))

    def _set_phonemeEqGain(self, value):
        if self._phonemeInventory.is_empty:
            raise UnsupportedConfigParameterError()
        self._ensure_phoneme_selection()
        band = self._current_eq_band(writable=True)
        if not band:
            raise UnsupportedConfigParameterError()
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid phoneme EQ gain '{value}'") from None
        numeric = max(_PHONEME_EQ_GAIN_MIN, min(numeric, _PHONEME_EQ_GAIN_MAX))
        if abs(numeric - band.gain_db) < 1e-6:
            return
        band.gain_db = numeric
        self._phonemeCustomizer.set_band(
            self._phonemeSelection, self._phonemeEqLayerSelection - 1, band
        )
        self._persist_phoneme_eq_profiles()
        self._update_phoneme_eq_engine()

    def _get_availablePhonemeEqFilters(self):
        options: "OrderedDict[str, StringParameterInfo]" = OrderedDict()
        for filter_type in VALID_FILTER_TYPES:
            label = _PHONEME_EQ_FILTER_LABELS.get(filter_type, filter_type)
            options[filter_type] = StringParameterInfo(filter_type, label)
        if not options:
            raise UnsupportedConfigParameterError()
        return options

    def _get_phonemeEqFilter(self):
        if self._phonemeInventory.is_empty:
            raise UnsupportedConfigParameterError()
        self._ensure_phoneme_selection()
        band = self._current_eq_band()
        if not band:
            raise UnsupportedConfigParameterError()
        if band.filter_type in VALID_FILTER_TYPES:
            return band.filter_type
        return PHONEME_EQ_DEFAULT_FILTER

    def _set_phonemeEqFilter(self, value):
        if self._phonemeInventory.is_empty:
            raise UnsupportedConfigParameterError()
        options = self._get_availablePhonemeEqFilters()
        if value not in options:
            raise ValueError(f"Unknown phoneme EQ filter '{value}'")
        band = self._current_eq_band(writable=True)
        if not band:
            raise UnsupportedConfigParameterError()
        if band.filter_type == value:
            return
        band.filter_type = value
        self._phonemeCustomizer.set_band(self._phonemeSelection, self._phonemeEqLayerSelection - 1, band)
        self._persist_phoneme_eq_profiles()
        self._update_phoneme_eq_engine()

    def _get_phonemeEqQ(self):
        if self._phonemeInventory.is_empty:
            raise UnsupportedConfigParameterError()
        self._ensure_phoneme_selection()
        band = self._current_eq_band()
        if not band:
            raise UnsupportedConfigParameterError()
        return int(round(float(band.q) * _PHONEME_EQ_Q_SCALE))

    def _set_phonemeEqQ(self, value):
        if self._phonemeInventory.is_empty:
            raise UnsupportedConfigParameterError()
        self._ensure_phoneme_selection()
        band = self._current_eq_band(writable=True)
        if not band:
            raise UnsupportedConfigParameterError()
        try:
            numeric = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid phoneme EQ Q '{value}'") from None
        numeric = max(_PHONEME_EQ_Q_MIN, min(numeric, _PHONEME_EQ_Q_MAX))
        current = int(round(float(band.q) * _PHONEME_EQ_Q_SCALE))
        if numeric == current:
            return
        q_value = numeric / _PHONEME_EQ_Q_SCALE
        updated = band.apply_q(q_value, _PHONEME_EQ_LOW_MIN, self._current_sample_rate_limit())
        updated.filter_type = band.filter_type
        self._phonemeCustomizer.set_band(self._phonemeSelection, self._phonemeEqLayerSelection - 1, updated)
        self._persist_phoneme_eq_profiles()
        self._update_phoneme_eq_engine()

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

    def _persist_sample_rate(self):
        try:
            speech_section = config.conf.setdefault("speech", {})
        except Exception:
            return
        synth_section = speech_section.setdefault(self.name, {})
        current = _eloquence.getSampleRate()
        if current == _SAMPLE_RATE_DEFAULT:
            synth_section.pop("sampleRate", None)
        else:
            synth_section["sampleRate"] = int(current)

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

    def pause(self, switch):
        _eloquence.pause(switch)
        #  self.dll.eciPause(self.handle,switch)

    def terminate(self):
        _eloquence.terminate()
    _backquoteVoiceTags = False
    _ABRDICT = False
    _phrasePrediction = False

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

    def _get_sampleRate(self):
        return int(_eloquence.getSampleRate())

    def _set_sampleRate(self, value):
        try:
            numeric = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid sample rate '{value}'") from None
        _eloquence.setSampleRate(numeric)
        if hasattr(self, "_phonemeCustomizer"):
            self._phonemeCustomizer.set_sample_rate(numeric)
            self._persist_phoneme_eq_profiles()
            self._update_phoneme_eq_engine()
        self._persist_sample_rate()

    def _get_rate(self):
        return self._paramToPercent(self.getVParam(_eloquence.rate), minRate, maxRate)

    def _set_rate(self, vl):
        self._rate = self._percentToParam(vl, minRate, maxRate)
        self.setVParam(_eloquence.rate, self._percentToParam(vl, minRate, maxRate))

    def _get_pitch(self):
        return self.getVParam(_eloquence.pitch)

    def _set_pitch(self, vl):
        self.setVParam(_eloquence.pitch, vl)

    def _get_volume(self):
        return self.getVParam(_eloquence.vlm)

    def _set_volume(self, vl):
        self.setVParam(_eloquence.vlm, int(vl))

    def _set_inflection(self, vl):
        vl = int(vl)
        self.setVParam(_eloquence.fluctuation, vl)

    def _get_inflection(self):
        return self.getVParam(_eloquence.fluctuation)

    def _set_hsz(self, vl):
        vl = int(vl)
        self.setVParam(_eloquence.hsz, vl)

    def _get_hsz(self):
        return self.getVParam(_eloquence.hsz)

    def _set_rgh(self, vl):
        vl = int(vl)
        self.setVParam(_eloquence.rgh, vl)

    def _get_rgh(self):
        return self.getVParam(_eloquence.rgh)

    def _set_bth(self, vl):
        vl = int(vl)
        self.setVParam(_eloquence.bth, vl)

    def _get_bth(self):
        return self.getVParam(_eloquence.bth)

    def _set_gender(self, vl):
        vl = int(vl)
        self.setVParam(_eloquence.gender, vl)

    def _get_gender(self):
        return self.getVParam(_eloquence.gender)

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

    def _set_voice(self, vl):
        _eloquence.set_voice(vl)
        self.curvoice = vl

    def getVParam(self, pr):
        return _eloquence.getVParam(pr)

    def setVParam(self, pr, vl):
        _eloquence.setVParam(pr, vl)

    def _get_lastIndex(self):
        # fix?
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


def _initialise_voice_parameter_bindings() -> Dict[str, VoiceParameterBinding]:
    bindings: Dict[str, VoiceParameterBinding] = {
        "gender": VoiceParameterBinding("gender", engine_param=_eloquence.gender),
        "pitch": VoiceParameterBinding("pitch", engine_param=_eloquence.pitch),
        "inflection": VoiceParameterBinding("inflection", engine_param=_eloquence.fluctuation),
        "headSize": VoiceParameterBinding("headSize", engine_param=_eloquence.hsz),
        "roughness": VoiceParameterBinding("roughness", engine_param=_eloquence.rgh),
        "breathiness": VoiceParameterBinding("breathiness", engine_param=_eloquence.bth),
        "rate": VoiceParameterBinding("rate", engine_param=_eloquence.rate),
        "volume": VoiceParameterBinding("volume", engine_param=_eloquence.vlm),
    }
    for name in ADVANCED_VOICE_PARAMETER_SPECS:
        bindings[name] = VoiceParameterBinding(
            name=name,
            getter=lambda driver, key=name: driver._advanced_parameter_value(key),
            setter=lambda driver, value, key=name: driver._apply_advanced_parameter(key, value),
        )
    return bindings


_VOICE_PARAM_BINDINGS.update(_initialise_voice_parameter_bindings())
