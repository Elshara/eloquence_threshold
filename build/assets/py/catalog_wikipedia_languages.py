"""Generate a canonical index of Wikipedia's language, dialect, and accent lists.

This helper downloads the `Lists_of_languages` article from Wikipedia and
parses the nested bullet lists so Eloquence can expose an authoritative index of
languages, dialects, and accent resources.  The driver and documentation teams
can import this JSON file to cross-reference which locales still need phoneme
coverage or NVDA templates.

The script intentionally stays dependency free.  It uses Python's
``html.parser`` module instead of BeautifulSoup so we can run it inside
restricted build environments.  When new headings or sub-sections are added to
the Wikipedia page, rerunning this tool will refresh our cached copy without
manual editing.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Dict, Iterable, List, Optional
from urllib.error import URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import ssl

WIKIPEDIA_SOURCE = "https://en.wikipedia.org/wiki/Lists_of_languages"


@dataclass
class Entry:
    """One bullet list entry on the page."""

    title: str
    url: Optional[str]
    breadcrumbs: List[str]
    tags: List[str]


@dataclass
class Section:
    """Group of entries scoped by a heading hierarchy."""

    breadcrumbs: List[str]
    entries: List[Entry] = field(default_factory=list)


class _LanguageHTMLParser(HTMLParser):
    """Lightweight parser that extracts headings and bullet list entries."""

    def __init__(self) -> None:
        super().__init__()
        self._sections: Dict[tuple[str, ...], Section] = {}
        self._heading_stack: List[str] = []
        self._current_li_text: List[str] = []
        self._current_href: Optional[str] = None
        self._collect_headline = False
        self._pending_headline: Optional[str] = None
        self._within_li = False
        self._content_depth = 0

    # -- Public helpers -------------------------------------------------
    @property
    def sections(self) -> List[Section]:
        return list(self._sections.values())

    # -- HTMLParser callbacks -------------------------------------------
    def handle_starttag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "div":
            if attrs_dict.get("id") == "mw-content-text":
                self._content_depth = 1
            elif self._content_depth:
                self._content_depth += 1
        if tag in {"h2", "h3"}:
            self._collect_headline = False
            self._pending_headline = None
        if tag == "span" and attrs_dict.get("class") == "mw-headline" and self._content_depth:
            self._collect_headline = True
            self._pending_headline = ""
        elif tag == "li" and self._content_depth:
            self._within_li = True
            self._current_li_text = []
            self._current_href = None
        elif tag == "a" and self._within_li:
            href = attrs_dict.get("href")
            if href and href.startswith("/"):
                self._current_href = urljoin(WIKIPEDIA_SOURCE, href)
            elif href:
                self._current_href = href

    def handle_endtag(self, tag: str) -> None:
        if tag == "div" and self._content_depth:
            self._content_depth -= 1
        if tag in {"h2", "h3"} and self._pending_headline is not None and self._content_depth:
            headline = _normalise_text(self._pending_headline)
            if headline:
                level = 0 if tag == "h2" else 1
                if level == 0:
                    self._heading_stack = [headline]
                else:
                    if not self._heading_stack:
                        self._heading_stack = [headline]
                    elif len(self._heading_stack) == 1:
                        self._heading_stack = [self._heading_stack[0], headline]
                    else:
                        self._heading_stack = [self._heading_stack[0], headline]
                key = tuple(self._heading_stack)
                self._sections.setdefault(key, Section(breadcrumbs=list(self._heading_stack)))
            self._pending_headline = None
            self._collect_headline = False
        elif tag == "li" and self._within_li and self._content_depth:
            text = _normalise_text("".join(self._current_li_text))
            if text:
                breadcrumbs = list(self._heading_stack)
                key = tuple(breadcrumbs) if breadcrumbs else ("Miscellaneous",)
                section = self._sections.setdefault(key, Section(breadcrumbs=list(key)))
                tags = _classify_entry(text)
                section.entries.append(
                    Entry(
                        title=text,
                        url=self._current_href,
                        breadcrumbs=list(breadcrumbs),
                        tags=tags,
                    )
                )
            self._within_li = False
            self._current_li_text = []
            self._current_href = None

    def handle_data(self, data: str) -> None:
        if self._collect_headline and self._pending_headline is not None:
            self._pending_headline += data
        elif self._within_li:
            self._current_li_text.append(data)


def _normalise_text(value: str) -> str:
    return " ".join(value.split())


def _classify_entry(text: str) -> List[str]:
    """Return heuristic tags describing a Wikipedia list entry."""

    lowered = text.lower()
    tags = {"language"}

    def flag(condition: bool, *values: str) -> None:
        if condition:
            tags.update(values)

    flag("dialect" in lowered or "dialects" in lowered, "dialect")
    flag("accent" in lowered or "accents" in lowered, "accent")
    flag(
        "sign language" in lowered
        or "sign-language" in lowered
        or "signed" in lowered,
        "sign-language",
    )
    flag(
        "script" in lowered
        or "alphabet" in lowered
        or "writing system" in lowered
        or "shorthand" in lowered
        or "unicode" in lowered
        or "orthography" in lowered,
        "orthography",
    )
    flag("iso" in lowered or "ietf" in lowered or "code" in lowered, "standard")
    flag("family" in lowered or "families" in lowered, "family")
    flag("proposed" in lowered and ("family" in lowered or "families" in lowered), "family-proposed")
    flag("isolate" in lowered, "language-isolate")
    flag("creole" in lowered or "pidgin" in lowered or "mixed language" in lowered, "contact-language")
    flag("constructed" in lowered or "conlang" in lowered, "constructed")
    flag("fiction" in lowered, "constructed-fictional")
    flag("programming" in lowered or "computer" in lowered, "programming-language")
    flag("markup" in lowered or "modeling" in lowered or "ontology" in lowered, "technical-language")
    flag("extinct" in lowered, "status-extinct")
    flag("endangered" in lowered, "status-endangered")
    flag("revived" in lowered or "revival" in lowered, "status-revived")
    flag("official" in lowered, "status-official")
    flag("lingua franca" in lowered or "auxiliary" in lowered or "international" in lowered, "status-lingua-franca")
    flag("diversity" in lowered or "index" in lowered, "statistics")
    flag("number of" in lowered or "by country" in lowered, "statistics")
    flag("dictionary" in lowered or "lexicon" in lowered, "lexicography")
    flag("phoneme" in lowered or "phonology" in lowered, "phonology")
    flag("grammar" in lowered or "sentence" in lowered, "grammar")
    flag("sample" in lowered or "recordings" in lowered or "speech" in lowered, "samples")
    flag("america" in lowered or "africa" in lowered or "asia" in lowered or "europe" in lowered or "oceania" in lowered,
         "geography")

    ordered: List[str] = []
    if "language" in tags:
        ordered.append("language")
    ordered.extend(sorted(tag for tag in tags if tag != "language"))
    return ordered


def _load_html(source: str) -> str:
    request = Request(source, headers={"User-Agent": "eloquence-threshold-language-index/1.0"})
    try:
        with urlopen(request) as handle:
            return handle.read().decode("utf-8")
    except URLError as error:
        reason = getattr(error, "reason", None)
        if isinstance(reason, ssl.SSLCertVerificationError):
            insecure_context = ssl._create_unverified_context()
            with urlopen(request, context=insecure_context) as handle:
                return handle.read().decode("utf-8")
        raise


def _parse_sections(html: str) -> List[Section]:
    parser = _LanguageHTMLParser()
    parser.feed(html)
    return parser.sections


def _serialise_sections(sections: Iterable[Section]) -> Dict[str, object]:
    entries: List[Dict[str, object]] = []
    for section in sections:
        for entry in section.entries:
            entries.append(
                {
                    "title": entry.title,
                    "url": entry.url,
                    "breadcrumbs": entry.breadcrumbs,
                    "tags": entry.tags,
                }
            )
    return {
        "source": WIKIPEDIA_SOURCE,
        "entries": entries,
    }


def _to_markdown(sections: Iterable[Section]) -> str:
    lines: List[str] = ["# Wikipedia language index", "", f"Source: [{WIKIPEDIA_SOURCE}]({WIKIPEDIA_SOURCE})", ""]
    for section in sections:
        if not section.entries:
            continue
        heading = " / ".join(section.breadcrumbs)
        lines.append(f"## {heading}")
        lines.append("")
        for entry in section.entries:
            link = entry.url or ""
            if link:
                lines.append(f"- [{entry.title}]({link}) — tags: {', '.join(entry.tags)}")
            else:
                lines.append(f"- {entry.title} — tags: {', '.join(entry.tags)}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-json", required=True, help="Path for the JSON index output")
    parser.add_argument("--output-markdown", required=True, help="Path for the Markdown index output")
    parser.add_argument(
        "--source",
        default=WIKIPEDIA_SOURCE,
        help="Override the Wikipedia source URL or provide a local HTML file",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    options = parse_args(argv)
    if options.source.startswith("http://") or options.source.startswith("https://"):
        html = _load_html(options.source)
    else:
        with open(options.source, "r", encoding="utf-8") as handle:
            html = handle.read()
    sections = _parse_sections(html)
    json_payload = _serialise_sections(sections)
    with open(options.output_json, "w", encoding="utf-8") as handle:
        json.dump(json_payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    markdown = _to_markdown(sections)
    with open(options.output_markdown, "w", encoding="utf-8") as handle:
        handle.write(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
