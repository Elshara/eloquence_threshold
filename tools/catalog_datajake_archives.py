"""Classify DataJake TTS archives for Eloquence integration."""
from __future__ import annotations

import argparse
import json
import pathlib
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict

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
ARCHIVE_EXTS = {"zip", "7z", "rar", "tar", "gz", "bz2", "xz", "z"}
ADDON_EXTS = {"nvda-addon"}

CODE_KEYWORDS = [
    "source",
    "src",
    "code",
    "sdk",
    "sample",
    "samples",
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
    "phoneme",
    "voice_data",
    "addon",
    "nvda",
    "mbrola",
    "eloquence",
    "espeak",
    "dectalk",
    "fonix",
    "eloq",
]

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
    extension: str
    family: str | None
    category: str
    viability: str
    notes: str

    def to_markdown_row(self, index: int) -> str:
        return f"| {index} | [{self.filename}]({self.url}) | {self.family or '—'} | {self.category} | {self.viability} | {self.notes} |"


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
    filename_lower = filename.lower()
    extension = filename_lower.split('.')[-1] if '.' in filename_lower else ''
    family = infer_family(url)

    category = "Unknown"
    viability = "Needs triage"
    notes = ""

    if extension in AUDIO_EXTS:
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
        matched_keyword = next((kw for kw in CODE_KEYWORDS if kw in filename_lower), None)
        if matched_keyword:
            category = "Source/tooling archive"
            viability = "High – inspect for portable code"
            notes = f"Keyword '{matched_keyword}' indicates embedded source or tooling."
        else:
            matched_asset = next((kw for kw in ASSET_KEYWORDS if kw in filename_lower), None)
            if matched_asset:
                category = "Voice/data archive"
                viability = "Medium – evaluate data reuse"
                notes = f"Contains voice or language assets (keyword '{matched_asset}')."
            else:
                category = "Generic archive"
                viability = "Low – inspect manually"
                notes = "Archive without clear code/data signal."
    else:
        if any(kw in filename_lower for kw in CODE_KEYWORDS):
            category = "Loose source file"
            viability = "High – integrate as needed"
            notes = "Direct code or config artifact."
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

    return ArchiveRecord(
        url=url,
        filename=filename,
        extension=extension,
        family=family,
        category=category,
        viability=viability,
        notes=notes,
    )


def build_records(urls: list[str]) -> list[ArchiveRecord]:
    return [classify(url) for url in urls]


def write_markdown(records: list[ArchiveRecord], path: pathlib.Path) -> None:
    counts = Counter(record.category for record in records)
    families = defaultdict(int)
    for record in records:
        if record.family:
            families[record.family] += 1
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
    lines.append("## Detailed inventory")
    lines.append("")
    lines.append("| # | Archive | Collection | Category | Viability | Notes |")
    lines.append("| ---: | --- | --- | --- | --- | --- |")
    for idx, record in enumerate(records, 1):
        lines.append(record.to_markdown_row(idx))
    lines.append("")
    path.write_text("\n".join(lines))


def write_json(records: list[ArchiveRecord], path: pathlib.Path) -> None:
    payload = [asdict(record) for record in records]
    path.write_text(json.dumps(payload, indent=2))


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
