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


def extract_language_hints(filename_lower: str) -> list[str]:
    hints = []
    for regex, label in LANGUAGE_REGEXES:
        if regex.search(filename_lower):
            hints.append(label)
    return sorted(set(hints))


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


def extract_metadata(
    display_name: str, filename_lower: str, category: str, extension: str
) -> dict[str, object]:
    metadata: dict[str, object] = {}
    sample_rate = parse_sample_rate(filename_lower)
    if sample_rate:
        metadata["sample_rate_hz"] = sample_rate
    language_hints = extract_language_hints(filename_lower)
    if language_hints:
        metadata["language_hints"] = language_hints
    voice_hint = extract_voice_hint(display_name)
    if voice_hint:
        metadata["voice_hint"] = voice_hint
    if extension:
        metadata["extension"] = extension
    metadata["category"] = category
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

    if display_name.endswith("..>"):
        category = "Truncated link"
        viability = "Fix manifest entry"
        notes = "Link appears truncated from the HTML index; verify the original filename on the mirror."
    elif extension in AUDIO_EXTS:
        category = "Audio sample"
        viability = "Scrap (non-code asset)"
        notes = "Audio payload useful only for reference recordings."
    elif extension in DOC_EXTS:
        category = "Documentation"
        viability = "Scrap (reference only)"
        notes = "Document scan or text reference."
    elif extension in INDEX_EXTS:
        category = "Archive index"
        viability = "Catalog for manual browsing"
        notes = "HTML index that links to additional payloads."
    elif extension in ADDON_EXTS:
        category = "NVDA add-on package"
        viability = "High – unpack for Python code"
        notes = "NVDA add-on bundle likely contains Python driver code."
    elif extension in BINARY_EXTS:
        category = "Binary installer"
        viability = "Medium – investigate resources"
        notes = "Executable installer – may contain DLLs or lexicon data."
    elif extension in ARCHIVE_EXTS:
        matched_asset = next((kw for kw in ASSET_KEYWORDS if kw in filename_lower), None)
        matched_keyword = next((kw for kw in CODE_KEYWORDS if kw in filename_lower), None)
        if matched_asset and matched_asset in PRIORITY_ASSET_KEYWORDS:
            category = "Voice/data archive"
            viability = "High – prioritise phoneme or lexicon data"
            notes = f"Contains phoneme or language resources (keyword '{matched_asset}')."
        elif matched_keyword:
            category = "Source/tooling archive"
            viability = "High – inspect for portable code"
            notes = f"Keyword '{matched_keyword}' indicates embedded source or tooling."
        elif matched_asset:
            category = "Voice/data archive"
            viability = "Medium – evaluate data reuse"
            notes = f"Contains voice or language assets (keyword '{matched_asset}')."
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
        elif matched_asset:
            category = "Voice/data archive"
            viability = "Medium – evaluate data reuse"
            notes = f"Contains voice or language assets (keyword '{matched_asset}')."
        elif any(kw in filename_lower for kw in CODE_KEYWORDS):
            category = "Loose source file"
            viability = "High – integrate as needed"
            notes = "Direct code or config artifact."
        elif looks_like_document_stub(filename_lower):
            category = "Documentation"
            viability = "Scrap (reference only)"
            notes = "Documentation fragment without explicit extension."
        elif extension:
            category = f"Other ({extension})"
            viability = "Review"
            notes = "Unhandled file type."
        else:
            category = "Directory"
            viability = "Review"
            notes = "Potential directory listing."

    if category.startswith("Generic") and any(kw in filename_lower for kw in SCRAP_KEYWORDS):
        viability = "Low – likely demo/installer"
        notes = "Demo or installer payload; keep only if no alternative."

    metadata = extract_metadata(display_name, filename_lower, category, extension)

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
    language_counts = Counter()
    for record in records:
        if record.family:
            families[record.family] += 1
        extension = record.extension or "(none)"
        extensions[extension] += 1
        sample_rate = record.metadata.get("sample_rate_hz") if record.metadata else None
        if isinstance(sample_rate, int):
            sample_rates[sample_rate] += 1
        for language in record.metadata.get("language_hints", []) if record.metadata else []:
            language_counts[language] += 1
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
    if language_counts:
        lines.append("## Language hints")
        lines.append("")
        lines.append("| Language | Archives |")
        lines.append("| --- | ---: |")
        for language, count in sorted(language_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {language} | {count} |")
        lines.append("")
    if viability_counts:
        lines.append("## Viability summary")
        lines.append("")
        lines.append("| Triage guidance | Archives |")
        lines.append("| --- | ---: |")
        for viability, count in sorted(viability_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {viability} | {count} |")
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
    sample_rates = Counter()
    languages = Counter()
    categories = Counter(record.category for record in records)
    viability = Counter(record.viability for record in records)
    for record in records:
        metadata = record.metadata or {}
        sample_rate = metadata.get("sample_rate_hz")
        if isinstance(sample_rate, int):
            sample_rates[sample_rate] += 1
        for language in metadata.get("language_hints", []):
            languages[language] += 1
    payload = {
        "records": [asdict(record) for record in records],
        "summaries": {
            "extensions": dict(extensions),
            "sample_rates": dict(sample_rates),
            "languages": dict(languages),
            "categories": dict(categories),
            "viability": dict(viability),
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
