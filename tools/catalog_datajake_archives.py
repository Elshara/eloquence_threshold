"""Classify DataJake TTS archives for Eloquence integration."""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import urllib.parse
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field

RAW_URL_PATH = pathlib.Path("docs/datajake_archive_urls.txt")
DEFAULT_MARKDOWN = pathlib.Path("docs/archive_inventory.md")
DEFAULT_JSON = pathlib.Path("docs/archive_inventory.json")

AUDIO_EXTS = {
    "wav",
    "aiff",
    "aif",
    "au",
    "mp3",
    "flac",
    "nist",
    "sph",
    "ogg",
    "wma",
}

DOC_EXTS = {"pdf", "txt", "doc", "docx", "rtf"}
INDEX_EXTS = {"html", "htm"}
BINARY_EXTS = {"exe", "msi", "dll", "iso", "img", "bin", "sit", "cab"}
ARCHIVE_EXTS = {"zip", "7z", "rar", "tar", "gz", "bz2", "xz", "z", "tar.gz", "tar.bz2", "tar.xz"}
ADDON_EXTS = {"nvda-addon"}

VOICE_GENDER_TOKENS = {
    "female": "Female",
    "woman": "Female",
    "women": "Female",
    "girl": "Female",
    "male": "Male",
    "man": "Male",
    "men": "Male",
    "boy": "Male",
}

VOICE_AGE_TOKENS = {
    "child": "Child",
    "children": "Child",
    "kid": "Child",
    "boy": "Child",
    "girl": "Child",
    "teen": "Teen",
    "teenager": "Teen",
    "youth": "Teen",
    "young": "Teen",
    "adult": "Adult",
    "adults": "Adult",
    "mature": "Adult",
    "senior": "Senior",
    "seniors": "Senior",
    "elder": "Senior",
    "elderly": "Senior",
    "older": "Senior",
    "old": "Senior",
}


@dataclass(frozen=True)
class DatasetRule:
    category: str
    viability: str
    notes: str
    tags: frozenset[str]


DATASET_EXTENSION_RULES: dict[str, DatasetRule] = {
    "dic": DatasetRule(
        category="Voice/data archive",
        viability="High – prioritise phoneme or lexicon data",
        notes="Pronunciation dictionary payload (DIC).",
        tags=frozenset({"phoneme_or_lexicon", "voice_or_language_pack"}),
    ),
    "dict": DatasetRule(
        category="Voice/data archive",
        viability="High – prioritise phoneme or lexicon data",
        notes="Dictionary payload (DICT).",
        tags=frozenset({"phoneme_or_lexicon", "voice_or_language_pack"}),
    ),
    "ipa": DatasetRule(
        category="Voice/data archive",
        viability="High – prioritise phoneme or lexicon data",
        notes="IPA phoneme inventory.",
        tags=frozenset({"phoneme_or_lexicon"}),
    ),
    "lex": DatasetRule(
        category="Voice/data archive",
        viability="High – prioritise phoneme or lexicon data",
        notes="Lexicon payload (LEX).",
        tags=frozenset({"phoneme_or_lexicon", "voice_or_language_pack"}),
    ),
    "pho": DatasetRule(
        category="Voice/data archive",
        viability="High – prioritise phoneme or lexicon data",
        notes="Phoneme definition payload (PHO).",
        tags=frozenset({"phoneme_or_lexicon"}),
    ),
    "phd": DatasetRule(
        category="Voice/data archive",
        viability="High – prioritise phoneme or lexicon data",
        notes="Pronunciation dictionary payload (PHD).",
        tags=frozenset({"phoneme_or_lexicon"}),
    ),
    "prn": DatasetRule(
        category="Voice/data archive",
        viability="Medium – evaluate data reuse",
        notes="Pronunciation rules payload (PRN).",
        tags=frozenset({"voice_or_language_pack"}),
    ),
    "cfg": DatasetRule(
        category="Voice/data archive",
        viability="Medium – evaluate data reuse",
        notes="Configuration or language mapping (CFG).",
        tags=frozenset({"voice_or_language_pack"}),
    ),
    "lst": DatasetRule(
        category="Voice/data archive",
        viability="Medium – evaluate data reuse",
        notes="List or index of phoneme assets (LST).",
        tags=frozenset({"voice_or_language_pack"}),
    ),
}

CODE_KEYWORDS = [
    "source",
    "src",
    "code",
    "sdk",
    "demo",
    "examples",
    "program",
    "app",
    "python",
    "java",
    "c99",
    "c-",
    "cpp",
    "lib",
    "library",
    "tool",
    "tools",
    "builder",
    "compiler",
    "module",
    "driver",
    "addon",
    "plugin",
    "voicebuilder",
    "mbrola",
    "gnuspeech",
    "espeak",
    "eloquence",
    "dectalk",
    "fonix",
    "meridian",
    "ibm",
    "ibmtts",
    "ttsapp",
    "nuance",
    "realvoice",
    "realspeak",
    "speechplayer",
    "phoneme",
    "phon",
    "dic",
    "dictionary",
    "lex",
    "language",
    "profile",
    "voice",
    "sapi",
    "sdk",
    "sapi5",
    "sapi4",
    "win32",
    "sourceforge",
    "git",
    "repo",
    "project",
]

ASSET_KEYWORDS = [
    "voice",
    "voices",
    "voicepack",
    "language",
    "lang",
    "dictionary",
    "lex",
    "lexicon",
    "phoneme",
    "voice_data",
    "dataset",
    "ipa",
    "addon",
    "nvda",
    "mbrola",
    "eloquence",
    "espeak",
    "dectalk",
    "fonix",
    "eloq",
]

DOC_KEYWORDS = {
    "readme",
    "changelog",
    "license",
    "licence",
    "manual",
    "guide",
    "notes",
    "overview",
    "spec",
    "specification",
}


def looks_like_document_stub(filename_lower: str) -> bool:
    tokens = [token for token in re.split(r"[^a-z0-9]+", filename_lower) if token]
    return any(token in DOC_KEYWORDS for token in tokens)

SCRAP_KEYWORDS = [
    "demo",
    "sample",
    "trial",
    "evaluation",
    "setup",
    "installer",
    "upgrade",
    "update",
]

PRIORITY_ASSET_KEYWORDS = {"phoneme", "phon", "lex", "lexicon", "dictionary", "ipa"}

KEYWORD_PRIORITY_TAGS = {
    "phoneme": "phoneme_or_lexicon",
    "phon": "phoneme_or_lexicon",
    "lex": "phoneme_or_lexicon",
    "lexicon": "phoneme_or_lexicon",
    "dictionary": "phoneme_or_lexicon",
    "ipa": "phoneme_or_lexicon",
    "addon": "tooling_candidate",
    "tool": "tooling_candidate",
    "tools": "tooling_candidate",
    "compiler": "tooling_candidate",
    "driver": "tooling_candidate",
    "module": "tooling_candidate",
    "plugin": "tooling_candidate",
    "source": "tooling_candidate",
    "src": "tooling_candidate",
    "code": "tooling_candidate",
    "language": "voice_or_language_pack",
    "voice": "voice_or_language_pack",
    "voices": "voice_or_language_pack",
    "voicepack": "voice_or_language_pack",
    "mbrola": "voice_or_language_pack",
    "espeak": "voice_or_language_pack",
    "eloquence": "voice_or_language_pack",
    "dectalk": "voice_or_language_pack",
    "fonix": "voice_or_language_pack",
    "ibmtts": "voice_or_language_pack",
}

LANGUAGE_PATTERNS: dict[str, str] = {
    r"arabic": "Arabic",
    r"brazilian": "Brazilian Portuguese",
    r"cantonese": "Cantonese",
    r"catalan": "Catalan",
    r"chinese": "Chinese",
    r"czech": "Czech",
    r"danish": "Danish",
    r"dutch": "Dutch",
    r"english": "English",
    r"finnish": "Finnish",
    r"french": "French",
    r"german": "German",
    r"greek": "Greek",
    r"hindi": "Hindi",
    r"icelandic": "Icelandic",
    r"indian": "Indian English",
    r"irish": "Irish",
    r"italian": "Italian",
    r"japanese|japan": "Japanese",
    r"korean": "Korean",
    r"mandarin": "Mandarin",
    r"mexican": "Mexican Spanish",
    r"norwegian": "Norwegian",
    r"polish": "Polish",
    r"portuguese": "Portuguese",
    r"romanian": "Romanian",
    r"russian": "Russian",
    r"spanish": "Spanish",
    r"swedish": "Swedish",
    r"taiwanese": "Taiwanese Mandarin",
    r"thai": "Thai",
    r"turkish": "Turkish",
    r"ukrainian": "Ukrainian",
    r"vietnamese": "Vietnamese",
}

LANGUAGE_REGEXES = [(re.compile(pattern), label) for pattern, label in LANGUAGE_PATTERNS.items()]

LANGUAGE_LABEL_TO_BCP47 = {
    "Arabic": "ar",
    "Brazilian Portuguese": "pt-BR",
    "Cantonese": "yue",
    "Catalan": "ca",
    "Chinese": "zh",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "English (US)": "en-US",
    "English (UK)": "en-GB",
    "Finnish": "fi",
    "French": "fr",
    "German": "de",
    "Greek": "el",
    "Hindi": "hi",
    "Icelandic": "is",
    "Indian English": "en-IN",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Mandarin": "zh-CN",
    "Mexican Spanish": "es-MX",
    "Norwegian": "nb",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Spanish": "es",
    "Swedish": "sv",
    "Taiwanese Mandarin": "zh-TW",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Vietnamese": "vi",
}

LANGUAGE_CODE_PATTERN = re.compile(r"(?<![a-z0-9])([a-z]{2,3}(?:[-_][a-z]{2})?)(?![a-z0-9])")

LANGUAGE_CODE_MAP: dict[str, tuple[str, str]] = {
    "ar": ("Arabic", "ar"),
    "ara": ("Arabic", "ar"),
    "ca": ("Catalan", "ca"),
    "cat": ("Catalan", "ca"),
    "cs": ("Czech", "cs"),
    "cze": ("Czech", "cs"),
    "da": ("Danish", "da"),
    "dan": ("Danish", "da"),
    "de": ("German", "de"),
    "deu": ("German", "de"),
    "el": ("Greek", "el"),
    "ell": ("Greek", "el"),
    "en": ("English", "en"),
    "eng": ("English", "en"),
    "enus": ("English (US)", "en-US"),
    "enuk": ("English (UK)", "en-GB"),
    "enin": ("Indian English", "en-IN"),
    "es": ("Spanish", "es"),
    "esp": ("Spanish", "es"),
    "esmx": ("Mexican Spanish", "es-MX"),
    "fr": ("French", "fr"),
    "fra": ("French", "fr"),
    "fi": ("Finnish", "fi"),
    "fin": ("Finnish", "fi"),
    "ga": ("Irish", "ga"),
    "gle": ("Irish", "ga"),
    "hi": ("Hindi", "hi"),
    "hin": ("Hindi", "hi"),
    "is": ("Icelandic", "is"),
    "isl": ("Icelandic", "is"),
    "it": ("Italian", "it"),
    "ita": ("Italian", "it"),
    "ja": ("Japanese", "ja"),
    "jpn": ("Japanese", "ja"),
    "ko": ("Korean", "ko"),
    "kor": ("Korean", "ko"),
    "nb": ("Norwegian", "nb"),
    "no": ("Norwegian", "nb"),
    "nob": ("Norwegian", "nb"),
    "nl": ("Dutch", "nl"),
    "nld": ("Dutch", "nl"),
    "pl": ("Polish", "pl"),
    "pol": ("Polish", "pl"),
    "pt": ("Portuguese", "pt"),
    "por": ("Portuguese", "pt"),
    "ptbr": ("Brazilian Portuguese", "pt-BR"),
    "ptpt": ("Portuguese", "pt-PT"),
    "ro": ("Romanian", "ro"),
    "ron": ("Romanian", "ro"),
    "ru": ("Russian", "ru"),
    "rus": ("Russian", "ru"),
    "sv": ("Swedish", "sv"),
    "swe": ("Swedish", "sv"),
    "th": ("Thai", "th"),
    "tha": ("Thai", "th"),
    "tr": ("Turkish", "tr"),
    "tur": ("Turkish", "tr"),
    "uk": ("Ukrainian", "uk"),
    "ukr": ("Ukrainian", "uk"),
    "vi": ("Vietnamese", "vi"),
    "vie": ("Vietnamese", "vi"),
    "yue": ("Cantonese", "yue"),
    "zh": ("Chinese", "zh"),
    "zhcn": ("Mandarin", "zh-CN"),
    "zhtw": ("Taiwanese Mandarin", "zh-TW"),
    "zhhk": ("Cantonese", "yue"),
}


def parse_sample_rate(filename_lower: str) -> int | None:
    khz_match = re.search(r"(\d{2,3}(?:[._]\d)?)\s*[-_]?k(?:hz)?", filename_lower)
    if khz_match:
        raw = khz_match.group(1).replace("_", ".")
        if "." in raw:
            value = int(round(float(raw) * 1000))
        else:
            value = int(raw) * 1000
        if 4000 <= value <= 384000:
            return value
    hz_match = re.search(r"(\d{4,6})\s*hz", filename_lower)
    if hz_match:
        value = int(hz_match.group(1))
        if 4000 <= value <= 384000:
            return value
    return None


BIT_DEPTH_PATTERN = re.compile(r"(?<!\d)(\d{1,2})(?:\s*|[-_])?(?:bit|bits)(?![a-z])", re.IGNORECASE)


def parse_bit_depth(filename_lower: str) -> int | None:
    match = BIT_DEPTH_PATTERN.search(filename_lower)
    if not match:
        return None
    value = int(match.group(1))
    if 4 <= value <= 64:
        return value
    return None


CHANNEL_KEYWORDS = {
    "mono": "Mono",
    "stereo": "Stereo",
    "binaural": "Binaural",
}

CHANNEL_PATTERN = re.compile(r"(?<!\d)([124])\s*(?:ch|channel|channels)(?![a-z])")


def parse_channel_mode(filename_lower: str) -> str | None:
    for token, label in CHANNEL_KEYWORDS.items():
        if token in filename_lower:
            return label
    match = CHANNEL_PATTERN.search(filename_lower)
    if not match:
        return None
    value = match.group(1)
    if value == "1":
        return "Mono"
    if value == "2":
        return "Stereo"
    if value == "4":
        return "Quad"
    return f"{value}-channel"


def extract_language_metadata(filename_lower: str) -> tuple[list[str], list[str]]:
    hints: set[str] = set()
    tags: set[str] = set()
    for regex, label in LANGUAGE_REGEXES:
        if regex.search(filename_lower):
            hints.add(label)
    for match in LANGUAGE_CODE_PATTERN.finditer(filename_lower):
        token = match.group(1).lower().replace("-", "").replace("_", "")
        mapped = LANGUAGE_CODE_MAP.get(token)
        if mapped:
            label, tag = mapped
            hints.add(label)
            tags.add(tag)
    for label in hints:
        tag = LANGUAGE_LABEL_TO_BCP47.get(label)
        if tag:
            tags.add(tag)
    return sorted(hints), sorted(tags)


def extract_voice_hint(display_name: str) -> str | None:
    base = display_name.rsplit('.', 1)[0]
    tokens = re.split(r"[\s_\-]+", base)
    if not tokens:
        return None
    if tokens[0].lower() != "voice":
        return None
    skip_tokens = {
        "voice",
        "us",
        "uk",
        "gb",
        "au",
        "male",
        "female",
        "english",
        "spanish",
        "french",
        "german",
        "italian",
        "portuguese",
        "dutch",
        "danish",
        "norwegian",
        "swedish",
        "finnish",
        "polish",
        "russian",
        "czech",
        "mandarin",
        "cantonese",
        "chinese",
        "korean",
        "thai",
        "brazilian",
        "mexican",
        "castilian",
        "irish",
        "icelandic",
        "catalan",
        "22khz",
        "11khz",
        "16khz",
        "8khz",
        "22",
        "11",
        "16",
        "8",
        "khz",
        "hz",
        "msi",
        "exe",
    }
    for token in tokens[1:]:
        lower = token.lower()
        if not token:
            continue
        if lower in skip_tokens or lower.endswith("khz") or lower.endswith("hz"):
            continue
        if lower.isdigit():
            continue
        return token
    return None


SYNTH_HINT_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"eloq", re.IGNORECASE), "Eloquence"),
    (re.compile(r"dectalk", re.IGNORECASE), "DECtalk"),
    (re.compile(r"fonix", re.IGNORECASE), "FonixTalk"),
    (re.compile(r"espeak", re.IGNORECASE), "eSpeak NG"),
    (re.compile(r"mbrola", re.IGNORECASE), "MBROLA"),
    (re.compile(r"ibmtts|viavoice", re.IGNORECASE), "IBM TTS"),
    (re.compile(r"nv[_-]?speech[_-]?player", re.IGNORECASE), "NV Speech Player"),
    (re.compile(r"realspeak", re.IGNORECASE), "RealSpeak"),
    (re.compile(r"sapi5", re.IGNORECASE), "Microsoft SAPI 5"),
    (re.compile(r"sapi4", re.IGNORECASE), "Microsoft SAPI 4"),
]


def extract_synth_hint(filename_lower: str) -> str | None:
    for pattern, label in SYNTH_HINT_PATTERNS:
        if pattern.search(filename_lower):
            return label
    return None


def extract_voice_characteristics(filename_lower: str) -> tuple[str | None, str | None]:
    tokens = [token for token in re.split(r"[^a-z0-9]+", filename_lower) if token]
    gender_hint: str | None = None
    age_hint: str | None = None
    for raw_token in tokens:
        token = raw_token.lower()
        singular = token[:-1] if token.endswith("s") and len(token) > 3 else token
        if not gender_hint:
            gender_hint = VOICE_GENDER_TOKENS.get(token) or VOICE_GENDER_TOKENS.get(singular)
        if not age_hint:
            age_hint = VOICE_AGE_TOKENS.get(token) or VOICE_AGE_TOKENS.get(singular)
        if gender_hint and age_hint:
            break
    return gender_hint, age_hint


ARCHITECTURE_PATTERNS: dict[re.Pattern[str], str] = {
    re.compile(r"(?<![a-z0-9])x86(?![a-z0-9])"): "Architecture: x86",
    re.compile(r"(?<![a-z0-9])i[3-6]86(?![a-z0-9])"): "Architecture: x86",
    re.compile(r"(?<![a-z0-9])x64(?![a-z0-9])"): "Architecture: x64",
    re.compile(r"(?<![a-z0-9])amd64(?![a-z0-9])"): "Architecture: x64",
    re.compile(r"(?<![a-z0-9])win32(?![a-z0-9])"): "Architecture: x86",
    re.compile(r"(?<![a-z0-9])win64(?![a-z0-9])"): "Architecture: x64",
    re.compile(r"(?<![a-z0-9])winx64(?![a-z0-9])"): "Architecture: x64",
    re.compile(r"(?<![a-z0-9])64bit(?![a-z0-9])"): "Architecture: x64",
    re.compile(r"(?<![a-z0-9])arm64(?![a-z0-9])"): "Architecture: ARM64",
    re.compile(r"(?<![a-z0-9])aarch64(?![a-z0-9])"): "Architecture: ARM64",
    re.compile(r"(?<![a-z0-9])armv7(?![a-z0-9])"): "Architecture: ARMv7",
    re.compile(r"(?<![a-z0-9])arm32(?![a-z0-9])"): "Architecture: ARMv7",
    re.compile(r"(?<![a-z0-9])armv6(?![a-z0-9])"): "Architecture: ARMv6",
}

PLATFORM_PATTERNS: dict[re.Pattern[str], str] = {
    re.compile(r"(?<![a-z0-9])win(?:32|xp|7|8|10|11)?(?![a-z0-9])"): "Platform: Windows",
    re.compile(r"(?<![a-z0-9])win64(?![a-z0-9])"): "Platform: Windows",
    re.compile(r"(?<![a-z0-9])winx64(?![a-z0-9])"): "Platform: Windows",
    re.compile(r"(?<![a-z0-9])windows(?![a-z0-9])"): "Platform: Windows",
    re.compile(r"(?<![a-z0-9])linux(?![a-z0-9])"): "Platform: Linux",
    re.compile(r"(?<![a-z0-9])ubuntu(?![a-z0-9])"): "Platform: Linux",
    re.compile(r"(?<![a-z0-9])debian(?![a-z0-9])"): "Platform: Linux",
    re.compile(r"(?<![a-z0-9])mac(?:os|osx)?(?![a-z0-9])"): "Platform: macOS",
    re.compile(r"(?<![a-z0-9])darwin(?![a-z0-9])"): "Platform: macOS",
    re.compile(r"(?<![a-z0-9])android(?![a-z0-9])"): "Platform: Android",
    re.compile(r"(?<![a-z0-9])ios(?![a-z0-9])"): "Platform: iOS",
    re.compile(r"(?<![a-z0-9])ipad(?![a-z0-9])"): "Platform: iOS",
    re.compile(r"(?<![a-z0-9])iphone(?![a-z0-9])"): "Platform: iOS",
}


VERSION_PATTERN = re.compile(
    r"(?:(?:^|[^a-z0-9])(v(?:er(?:sion)?)?)[-_ ]*(\d{1,4}(?:[._]\d{1,4}){1,3})(?=$|[^a-z0-9]))",
    re.IGNORECASE,
)
VERSION_FALLBACK_PATTERN = re.compile(
    r"(?:(?:^|[^a-z0-9])(release|rev|build)[-_ ]*(\d{1,4}(?:[._]\d{1,4}){1,3})(?=$|[^a-z0-9]))",
    re.IGNORECASE,
)


def extract_platform_hints(filename_lower: str) -> list[str]:
    hints: set[str] = set()
    for pattern, label in ARCHITECTURE_PATTERNS.items():
        if pattern.search(filename_lower):
            hints.add(label)
    for pattern, label in PLATFORM_PATTERNS.items():
        if pattern.search(filename_lower):
            hints.add(label)
    return sorted(hints)


def extract_version_hint(filename_lower: str) -> str | None:
    match = VERSION_PATTERN.search(filename_lower)
    if not match:
        match = VERSION_FALLBACK_PATTERN.search(filename_lower)
        if not match:
            return None
    value = match.group(2).replace("_", ".")
    return value


def extract_metadata(
    display_name: str,
    filename_lower: str,
    category: str,
    extension: str,
    priority_tags: set[str],
) -> dict[str, object]:
    metadata: dict[str, object] = {}
    sample_rate = parse_sample_rate(filename_lower)
    if sample_rate:
        metadata["sample_rate_hz"] = sample_rate
        priority_tags.add("has_sample_rate_hint")
    bit_depth = parse_bit_depth(filename_lower)
    if bit_depth:
        metadata["bit_depth_bits"] = bit_depth
        priority_tags.add("has_bit_depth_hint")
    channel_mode = parse_channel_mode(filename_lower)
    if channel_mode:
        metadata["channel_mode"] = channel_mode
        priority_tags.add("has_channel_hint")
    language_hints, language_tags = extract_language_metadata(filename_lower)
    if language_hints:
        metadata["language_hints"] = language_hints
        priority_tags.add("has_language_hint")
    if language_tags:
        metadata["language_tags"] = language_tags
        priority_tags.add("has_language_tag")
    voice_hint = extract_voice_hint(display_name)
    if voice_hint:
        metadata["voice_hint"] = voice_hint
    platform_hints = extract_platform_hints(filename_lower)
    if platform_hints:
        metadata["platform_hints"] = platform_hints
        priority_tags.add("has_platform_hint")
    version_hint = extract_version_hint(filename_lower)
    if version_hint:
        metadata["version_hint"] = version_hint
        priority_tags.add("has_version_hint")
    synth_hint = extract_synth_hint(filename_lower)
    if synth_hint:
        metadata["synth_hint"] = synth_hint
        priority_tags.add("has_synth_hint")
    gender_hint, age_hint = extract_voice_characteristics(filename_lower)
    if gender_hint:
        metadata["gender_hint"] = gender_hint
        priority_tags.add("has_gender_hint")
    if age_hint:
        metadata["age_hint"] = age_hint
        priority_tags.add("has_age_hint")
    if extension:
        metadata["extension"] = extension
    metadata["category"] = category
    if priority_tags:
        metadata["priority_tags"] = sorted(priority_tags)
    return metadata


def detect_extension(display_name: str) -> str:
    name_lower = display_name.lower().strip()
    # ``PurePosixPath`` keeps multi-part suffixes so installers like ``.tar.gz``
    # round-trip cleanly even when the manifest stores uppercase names.
    path = pathlib.PurePosixPath(name_lower)
    suffixes = [suffix.lstrip(".") for suffix in path.suffixes if suffix]
    if not suffixes:
        return ""
    if suffixes[-1] in {"gz", "bz2", "xz", "z"} and len(suffixes) >= 2:
        if suffixes[-2] == "tar":
            return f"tar.{suffixes[-1]}"
    if suffixes[-1] == "tgz":
        return "tar.gz"
    if suffixes[-1] == "tbz2":
        return "tar.bz2"
    if suffixes[-1] == "txz":
        return "tar.xz"
    # ``.nvda-addon`` keeps a hyphenated suffix. ``PurePosixPath`` preserves it.
    return suffixes[-1]

SYNTH_ALIAS = {
    "CircumReality": "CircumReality",
    "DECtalk": "DECtalk",
    "Fonix": "FonixTalk",
    "FonixTalk": "FonixTalk",
    "IBMTTS": "IBM TTS",
    "Meridian": "Meridian",
    "MeridianOne": "Meridian",
    "SAPI4": "Microsoft SAPI 4",
    "SAPI5": "Microsoft SAPI 5",
    "TTSApp": "TTSApp",
    "Worlds": "Worlds of Speech",
}

@dataclass
class ArchiveRecord:
    url: str
    filename: str
    display_name: str
    extension: str
    family: str | None
    category: str
    viability: str
    notes: str
    metadata: dict[str, object] = field(default_factory=dict)

    def to_markdown_row(self, index: int) -> str:
        return (
            f"| {index} | [{self.display_name}]({self.url}) | {self.family or '—'} | "
            f"{self.category} | {self.viability} | {self.notes} |"
        )


def infer_family(url: str) -> str | None:
    parts = url.split('/')
    try:
        idx = parts.index('tts')
    except ValueError:
        return None
    for part in parts[idx + 1:-1]:
        if part:
            alias = SYNTH_ALIAS.get(part, part)
            return alias
    return None


def classify(url: str) -> ArchiveRecord:
    filename = url.rsplit('/', 1)[-1]
    display_name = urllib.parse.unquote(filename)
    filename_lower = display_name.lower()
    extension = detect_extension(display_name)
    family = infer_family(url)

    category = "Unknown"
    viability = "Needs triage"
    notes = ""
    priority_tags: set[str] = set()

    if display_name.endswith("..>"):
        category = "Truncated link"
        viability = "Fix manifest entry"
        notes = "Link appears truncated from the HTML index; verify the original filename on the mirror."
        priority_tags.add("index_listing")
    elif extension in AUDIO_EXTS:
        category = "Audio sample"
        viability = "Scrap (non-code asset)"
        notes = "Audio payload useful only for reference recordings."
        priority_tags.add("audio_demo")
    elif extension in DOC_EXTS:
        category = "Documentation"
        viability = "Scrap (reference only)"
        notes = "Document scan or text reference."
        priority_tags.add("documentation")
    elif extension in INDEX_EXTS:
        category = "Archive index"
        viability = "Catalog for manual browsing"
        notes = "HTML index that links to additional payloads."
        priority_tags.add("index_listing")
    elif extension in ADDON_EXTS:
        category = "NVDA add-on package"
        viability = "High – unpack for Python code"
        notes = "NVDA add-on bundle likely contains Python driver code."
        priority_tags.update({"nvda_addon_bundle", "tooling_candidate"})
    elif extension in BINARY_EXTS:
        category = "Binary installer"
        viability = "Medium – investigate resources"
        notes = "Executable installer – may contain DLLs or lexicon data."
        priority_tags.add("installer_payload")
    elif extension in DATASET_EXTENSION_RULES:
        rule = DATASET_EXTENSION_RULES[extension]
        category = rule.category
        viability = rule.viability
        notes = rule.notes
        priority_tags.update(rule.tags)
    elif extension in ARCHIVE_EXTS:
        matched_asset = next((kw for kw in ASSET_KEYWORDS if kw in filename_lower), None)
        matched_keyword = next((kw for kw in CODE_KEYWORDS if kw in filename_lower), None)
        if matched_asset and matched_asset in PRIORITY_ASSET_KEYWORDS:
            category = "Voice/data archive"
            viability = "High – prioritise phoneme or lexicon data"
            notes = f"Contains phoneme or language resources (keyword '{matched_asset}')."
            priority_tags.add("phoneme_or_lexicon")
            priority_tags.add("voice_or_language_pack")
        elif matched_keyword:
            category = "Source/tooling archive"
            viability = "High – inspect for portable code"
            notes = f"Keyword '{matched_keyword}' indicates embedded source or tooling."
            priority_tags.add("tooling_candidate")
            keyword_tag = KEYWORD_PRIORITY_TAGS.get(matched_keyword)
            if keyword_tag:
                priority_tags.add(keyword_tag)
        elif matched_asset:
            category = "Voice/data archive"
            viability = "Medium – evaluate data reuse"
            notes = f"Contains voice or language assets (keyword '{matched_asset}')."
            priority_tags.add("voice_or_language_pack")
        else:
            category = "Generic archive"
            viability = "Low – inspect manually"
            notes = "Archive without clear code/data signal."
    else:
        matched_asset = next((kw for kw in ASSET_KEYWORDS if kw in filename_lower), None)
        if matched_asset and matched_asset in PRIORITY_ASSET_KEYWORDS:
            category = "Voice/data archive"
            viability = "High – prioritise phoneme or lexicon data"
            notes = f"Contains phoneme or language resources (keyword '{matched_asset}')."
            priority_tags.add("phoneme_or_lexicon")
            priority_tags.add("voice_or_language_pack")
        elif matched_asset:
            category = "Voice/data archive"
            viability = "Medium – evaluate data reuse"
            notes = f"Contains voice or language assets (keyword '{matched_asset}')."
            priority_tags.add("voice_or_language_pack")
        elif any(kw in filename_lower for kw in CODE_KEYWORDS):
            matched_keyword = next((kw for kw in CODE_KEYWORDS if kw in filename_lower), None)
            category = "Loose source file"
            viability = "High – integrate as needed"
            notes = "Direct code or config artifact."
            priority_tags.add("tooling_candidate")
            if matched_keyword:
                keyword_tag = KEYWORD_PRIORITY_TAGS.get(matched_keyword)
                if keyword_tag:
                    priority_tags.add(keyword_tag)
        elif looks_like_document_stub(filename_lower):
            category = "Documentation"
            viability = "Scrap (reference only)"
            notes = "Documentation fragment without explicit extension."
            priority_tags.add("documentation")
        elif extension:
            category = f"Other ({extension})"
            viability = "Review"
            notes = "Unhandled file type."
        else:
            category = "Directory"
            viability = "Review"
            notes = "Potential directory listing."
            priority_tags.add("index_listing")

    if category.startswith("Generic") and any(kw in filename_lower for kw in SCRAP_KEYWORDS):
        viability = "Low – likely demo/installer"
        notes = "Demo or installer payload; keep only if no alternative."

    metadata = extract_metadata(
        display_name,
        filename_lower,
        category,
        extension,
        priority_tags,
    )

    return ArchiveRecord(
        url=url,
        filename=filename,
        display_name=display_name,
        extension=extension,
        family=family,
        category=category,
        viability=viability,
        notes=notes,
        metadata=metadata,
    )


def build_records(urls: list[str]) -> list[ArchiveRecord]:
    return [classify(url) for url in urls]


def write_markdown(records: list[ArchiveRecord], path: pathlib.Path) -> None:
    counts = Counter(record.category for record in records)
    families = defaultdict(int)
    extensions = Counter()
    sample_rates = Counter()
    bit_depths = Counter()
    channel_modes = Counter()
    language_counts = Counter()
    language_tag_counts = Counter()
    priority_counts = Counter()
    voice_hints = Counter()
    synth_counts = Counter()
    platform_counts = Counter()
    version_counts = Counter()
    gender_counts = Counter()
    age_counts = Counter()
    metadata_flags = Counter()
    for record in records:
        if record.family:
            families[record.family] += 1
        extension = record.extension or "(none)"
        extensions[extension] += 1
        sample_rate = record.metadata.get("sample_rate_hz") if record.metadata else None
        if isinstance(sample_rate, int):
            sample_rates[sample_rate] += 1
            metadata_flags["sample_rate_hz"] += 1
        bit_depth = record.metadata.get("bit_depth_bits") if record.metadata else None
        if isinstance(bit_depth, int):
            bit_depths[bit_depth] += 1
            metadata_flags["bit_depth_bits"] += 1
        channel_mode = record.metadata.get("channel_mode") if record.metadata else None
        if isinstance(channel_mode, str):
            channel_modes[channel_mode] += 1
            metadata_flags["channel_mode"] += 1
        language_hints = record.metadata.get("language_hints") if record.metadata else []
        if language_hints:
            metadata_flags["language_hints"] += 1
            for language in language_hints:
                language_counts[language] += 1
        language_tags = record.metadata.get("language_tags") if record.metadata else []
        if language_tags:
            metadata_flags["language_tags"] += 1
            for language_tag in language_tags:
                language_tag_counts[language_tag] += 1
        for tag in record.metadata.get("priority_tags", []) if record.metadata else []:
            priority_counts[tag] += 1
        voice_hint = record.metadata.get("voice_hint") if record.metadata else None
        if isinstance(voice_hint, str):
            voice_hints[voice_hint] += 1
            metadata_flags["voice_hint"] += 1
        synth_hint = record.metadata.get("synth_hint") if record.metadata else None
        if isinstance(synth_hint, str):
            synth_counts[synth_hint] += 1
            metadata_flags["synth_hint"] += 1
        platform_hints = record.metadata.get("platform_hints") if record.metadata else []
        if platform_hints:
            metadata_flags["platform_hints"] += 1
            for platform in platform_hints:
                platform_counts[platform] += 1
        version_hint = record.metadata.get("version_hint") if record.metadata else None
        if isinstance(version_hint, str):
            version_counts[version_hint] += 1
            metadata_flags["version_hint"] += 1
        gender_hint = record.metadata.get("gender_hint") if record.metadata else None
        if isinstance(gender_hint, str):
            gender_counts[gender_hint] += 1
            metadata_flags["gender_hint"] += 1
        age_hint = record.metadata.get("age_hint") if record.metadata else None
        if isinstance(age_hint, str):
            age_counts[age_hint] += 1
            metadata_flags["age_hint"] += 1
    viability_counts = Counter(record.viability for record in records)
    lines = []
    lines.append("# DataJake Archive Classification")
    lines.append("")
    lines.append("This inventory classifies each DataJake TTS archive so Eloquence contributors can quickly locate reusable "
                 "source code, tooling, and supplementary voice assets. The list is generated from `docs/datajake_archive_urls.txt` "
                 "via `python tools/catalog_datajake_archives.py`.")
    lines.append("")
    lines.append("## Category summary")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("| --- | ---: |")
    for category, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {category} | {count} |")
    lines.append("")
    lines.append("## Synthesizer/collection coverage")
    lines.append("")
    lines.append("| Collection | Items |")
    lines.append("| --- | ---: |")
    for family, count in sorted(families.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {family} | {count} |")
    lines.append("")
    lines.append("## File extension index")
    lines.append("")
    lines.append("| Extension | Count |")
    lines.append("| --- | ---: |")
    for ext, count in sorted(extensions.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {ext} | {count} |")
    lines.append("")
    if sample_rates:
        lines.append("## Sample rate hints")
        lines.append("")
        lines.append("| Sample rate (Hz) | Archives |")
        lines.append("| ---: | ---: |")
        for rate, count in sorted(sample_rates.items(), key=lambda item: (-item[1], -item[0])):
            lines.append(f"| {rate} | {count} |")
        lines.append("")
    if bit_depths:
        lines.append("## Bit depth hints")
        lines.append("")
        lines.append("| Bit depth (bits) | Archives |")
        lines.append("| ---: | ---: |")
        for depth, count in sorted(bit_depths.items(), key=lambda item: (-item[1], -item[0])):
            lines.append(f"| {depth} | {count} |")
        lines.append("")
    if channel_modes:
        lines.append("## Channel layout hints")
        lines.append("")
        lines.append("| Channel layout | Archives |")
        lines.append("| --- | ---: |")
        for layout, count in sorted(channel_modes.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {layout} | {count} |")
        lines.append("")
    if language_counts:
        lines.append("## Language hints")
        lines.append("")
        lines.append("| Language | Archives |")
        lines.append("| --- | ---: |")
        for language, count in sorted(language_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {language} | {count} |")
        lines.append("")
    if language_tag_counts:
        lines.append("## Language tags")
        lines.append("")
        lines.append("| BCP-47 tag | Archives |")
        lines.append("| --- | ---: |")
        for language_tag, count in sorted(
            language_tag_counts.items(), key=lambda item: (-item[1], item[0])
        ):
            lines.append(f"| {language_tag} | {count} |")
        lines.append("")
    if viability_counts:
        lines.append("## Viability summary")
        lines.append("")
        lines.append("| Triage guidance | Archives |")
        lines.append("| --- | ---: |")
        for viability, count in sorted(viability_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {viability} | {count} |")
        lines.append("")
    if metadata_flags:
        flag_labels = {
            "sample_rate_hz": "Sample rate hints",
            "bit_depth_bits": "Bit depth hints",
            "channel_mode": "Channel layout hints",
            "language_hints": "Language hints",
            "language_tags": "BCP-47 language tags",
            "voice_hint": "Voice name hints",
            "synth_hint": "Synthesizer hints",
            "platform_hints": "Platform/architecture hints",
            "version_hint": "Version strings",
            "gender_hint": "Voice gender hints",
            "age_hint": "Voice age hints",
        }
        lines.append("## Metadata coverage summary")
        lines.append("")
        lines.append("| Metadata hint | Archives |")
        lines.append("| --- | ---: |")
        for key, count in sorted(metadata_flags.items(), key=lambda item: (-item[1], item[0])):
            label = flag_labels.get(key, key)
            lines.append(f"| {label} | {count} |")
        lines.append("")
    if priority_counts:
        lines.append("## Priority tag summary")
        lines.append("")
        lines.append("| Priority signal | Archives |")
        lines.append("| --- | ---: |")
        for tag, count in sorted(priority_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {tag} | {count} |")
        lines.append("")
    if voice_hints:
        lines.append("## Voice hint index")
        lines.append("")
        lines.append("| Voice token | Archives |")
        lines.append("| --- | ---: |")
        for hint, count in sorted(voice_hints.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {hint} | {count} |")
        lines.append("")
    if synth_counts:
        lines.append("## Synthesizer hint index")
        lines.append("")
        lines.append("| Synthesizer | Archives |")
        lines.append("| --- | ---: |")
        for hint, count in sorted(synth_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {hint} | {count} |")
        lines.append("")
    if platform_counts:
        lines.append("## Platform and architecture hints")
        lines.append("")
        lines.append("| Platform hint | Archives |")
        lines.append("| --- | ---: |")
        for platform, count in sorted(platform_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {platform} | {count} |")
        lines.append("")
    if version_counts:
        lines.append("## Version hints")
        lines.append("")
        lines.append("| Version | Archives |")
        lines.append("| --- | ---: |")
        for version, count in sorted(version_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {version} | {count} |")
        lines.append("")
    if gender_counts:
        lines.append("## Voice gender hints")
        lines.append("")
        lines.append("| Gender | Archives |")
        lines.append("| --- | ---: |")
        for gender, count in sorted(gender_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {gender} | {count} |")
        lines.append("")
    if age_counts:
        lines.append("## Voice age hints")
        lines.append("")
        lines.append("| Age | Archives |")
        lines.append("| --- | ---: |")
        for age, count in sorted(age_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {age} | {count} |")
        lines.append("")
    lines.append("## Detailed inventory")
    lines.append("")
    lines.append("| # | Archive | Collection | Category | Viability | Notes |")
    lines.append("| ---: | --- | --- | --- | --- | --- |")
    for idx, record in enumerate(records, 1):
        lines.append(record.to_markdown_row(idx))
    lines.append("")
    path.write_text("\n".join(lines))


def write_json(records: list[ArchiveRecord], path: pathlib.Path) -> None:
    extensions = Counter(record.extension or "(none)" for record in records)
    families = Counter(record.family for record in records if record.family)
    sample_rates = Counter()
    bit_depths = Counter()
    channel_modes = Counter()
    languages = Counter()
    language_tags = Counter()
    categories = Counter(record.category for record in records)
    viability = Counter(record.viability for record in records)
    priority = Counter()
    voice_hints = Counter()
    synth_counts = Counter()
    platform_counts = Counter()
    version_counts = Counter()
    gender_counts = Counter()
    age_counts = Counter()
    metadata_flags = Counter()
    for record in records:
        metadata = record.metadata or {}
        sample_rate = metadata.get("sample_rate_hz")
        if isinstance(sample_rate, int):
            sample_rates[sample_rate] += 1
            metadata_flags["sample_rate_hz"] += 1
        bit_depth = metadata.get("bit_depth_bits")
        if isinstance(bit_depth, int):
            bit_depths[bit_depth] += 1
            metadata_flags["bit_depth_bits"] += 1
        channel_mode = metadata.get("channel_mode")
        if isinstance(channel_mode, str):
            channel_modes[channel_mode] += 1
            metadata_flags["channel_mode"] += 1
        language_hints = metadata.get("language_hints", [])
        if language_hints:
            metadata_flags["language_hints"] += 1
            for language in language_hints:
                languages[language] += 1
        language_tags_list = metadata.get("language_tags", [])
        if language_tags_list:
            metadata_flags["language_tags"] += 1
            for language_tag in language_tags_list:
                language_tags[language_tag] += 1
        for tag in metadata.get("priority_tags", []):
            priority[tag] += 1
        voice_hint = metadata.get("voice_hint")
        if isinstance(voice_hint, str):
            voice_hints[voice_hint] += 1
            metadata_flags["voice_hint"] += 1
        synth_hint = metadata.get("synth_hint")
        if isinstance(synth_hint, str):
            synth_counts[synth_hint] += 1
            metadata_flags["synth_hint"] += 1
        platform_hints = metadata.get("platform_hints", [])
        if platform_hints:
            metadata_flags["platform_hints"] += 1
            for platform in platform_hints:
                platform_counts[platform] += 1
        version_hint = metadata.get("version_hint")
        if isinstance(version_hint, str):
            version_counts[version_hint] += 1
            metadata_flags["version_hint"] += 1
        gender_hint = metadata.get("gender_hint")
        if isinstance(gender_hint, str):
            gender_counts[gender_hint] += 1
            metadata_flags["gender_hint"] += 1
        age_hint = metadata.get("age_hint")
        if isinstance(age_hint, str):
            age_counts[age_hint] += 1
            metadata_flags["age_hint"] += 1
    payload = {
        "records": [asdict(record) for record in records],
        "summaries": {
            "extensions": dict(extensions),
            "sample_rates": dict(sample_rates),
            "bit_depths": dict(bit_depths),
            "channel_modes": dict(channel_modes),
            "languages": dict(languages),
            "language_tags": dict(language_tags),
            "categories": dict(categories),
            "viability": dict(viability),
            "priority_tags": dict(priority),
            "voice_hints": dict(voice_hints),
            "synth_hints": dict(synth_counts),
            "families": dict(families),
            "platforms": dict(platform_counts),
            "versions": dict(version_counts),
            "gender_hints": dict(gender_counts),
            "age_hints": dict(age_counts),
            "metadata_flags": dict(metadata_flags),
        },
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def load_urls(path: pathlib.Path) -> list[str]:
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url-list", type=pathlib.Path, default=RAW_URL_PATH, help="Path to the URL manifest")
    parser.add_argument("--markdown", type=pathlib.Path, default=DEFAULT_MARKDOWN, help="Markdown output path")
    parser.add_argument("--json", type=pathlib.Path, default=DEFAULT_JSON, help="JSON output path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    urls = load_urls(args.url_list)
    records = build_records(urls)
    write_markdown(records, args.markdown)
    write_json(records, args.json)


if __name__ == "__main__":
    main()
