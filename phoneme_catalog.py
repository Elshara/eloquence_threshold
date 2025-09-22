"""Utilities for loading and cataloguing phoneme metadata.

This module parses the eSpeak NG ``phsource/phonemes`` definition file so we can
surface phoneme information inside NVDA's Eloquence driver.  The loader focuses
on data that helps blind users explore and customise phoneme mappings from the
keyboard:

* Category labels (for grouping phonemes in the voice settings dialog).
* IPA symbols declared for each phoneme, to match NVDA ``PhonemeCommand``
  entries.
* Human readable descriptions and example words, which become replacement
  options when Eloquence can't articulate a requested phoneme directly.
"""
from __future__ import annotations

import logging
import os
import re
from collections import OrderedDict, defaultdict
from dataclasses import dataclass, field
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

LOG = logging.getLogger(__name__)

_CATEGORY_BORDER_CHARS = "*/=\\-#~"
_IPA_CODE_RE = re.compile(r"U\+([0-9A-Fa-f]{4,6})")
_MARKED_SAMPLE_RE = re.compile(r"\*\*([^*]+)\*\*")
_NON_ID_CHAR_RE = re.compile(r"[^0-9a-z]+")


@dataclass(frozen=True)
class PhonemeReplacement:
    """Concrete replacement option for a phoneme."""

    id: str
    kind: str
    source: str
    output: str


@dataclass
class PhonemeDefinition:
    """Structured view of one phoneme entry from eSpeak's master file."""

    name: str
    comment: str
    category: Optional[str]
    ipa: Tuple[str, ...]
    attributes: Tuple[Tuple[str, Tuple[str, ...]], ...]
    _replacement_cache: Optional[OrderedDict[str, PhonemeReplacement]] = field(
        default=None, init=False, repr=False
    )

    @property
    def display_label(self) -> str:
        """Concise label combining the phoneme's name and description."""
        description = self.description
        if description:
            return f"{self.name} – {description}"
        return self.name

    @property
    def description(self) -> str:
        text = self.comment.replace("**", "").strip()
        return " ".join(text.split())

    def sample_words(self) -> List[str]:
        words: List[str] = []
        for match in _MARKED_SAMPLE_RE.finditer(self.comment):
            start, end = match.span()
            left = _find_word_start(self.comment, start)
            right = _find_word_end(self.comment, end)
            candidate = self.comment[left:right].replace("**", "").strip(" ,;:()[]{}")
            if candidate and candidate not in words:
                words.append(candidate)
        return words

    def replacement_options(self) -> OrderedDict[str, PhonemeReplacement]:
        if self._replacement_cache is None:
            options: "OrderedDict[str, PhonemeReplacement]" = OrderedDict()
            for idx, word in enumerate(self.sample_words()):
                option_id = "example" if idx == 0 else f"example{idx + 1}"
                options[option_id] = PhonemeReplacement(
                    id=option_id,
                    kind="example",
                    source=word,
                    output=word,
                )
            description = self.description
            if description:
                options.setdefault(
                    "description",
                    PhonemeReplacement(
                        id="description",
                        kind="description",
                        source=description,
                        output=description,
                    ),
                )
            for index, ipa_value in enumerate(self.ipa):
                if not ipa_value:
                    continue
                option_id = "ipa" if index == 0 else f"ipa{index + 1}"
                options[option_id] = PhonemeReplacement(
                    id=option_id,
                    kind="ipa",
                    source=ipa_value,
                    output=ipa_value,
                )
            options.setdefault(
                "name",
                PhonemeReplacement(
                    id="name",
                    kind="name",
                    source=self.name,
                    output=self.name,
                ),
            )
            self._replacement_cache = options
        return self._replacement_cache

    def get_replacement(self, replacement_id: Optional[str]) -> Optional[PhonemeReplacement]:
        options = self.replacement_options()
        if replacement_id and replacement_id in options:
            return options[replacement_id]
        return next(iter(options.values()), None)


class PhonemeInventory:
    """Catalogue of phoneme definitions with helper lookups."""

    def __init__(self, phonemes: Iterable[PhonemeDefinition]):
        self._by_name: "OrderedDict[str, PhonemeDefinition]" = OrderedDict()
        self._category_labels: "OrderedDict[str, str]" = OrderedDict()
        self._by_category: Dict[str, List[PhonemeDefinition]] = defaultdict(list)
        self._ipa_index: Dict[str, PhonemeDefinition] = {}
        for definition in phonemes:
            if definition.name in self._by_name:
                continue
            self._by_name[definition.name] = definition
            category_label = definition.category or "General"
            category_id = _register_category(self._category_labels, category_label)
            self._by_category[category_id].append(definition)
        for ipa_value in definition.ipa:
            if ipa_value and ipa_value not in self._ipa_index:
                self._ipa_index[ipa_value] = definition
        self._ipa_keys_desc = sorted(self._ipa_index.keys(), key=len, reverse=True)

    @property
    def is_empty(self) -> bool:
        return not self._by_name

    @property
    def categories(self) -> "OrderedDict[str, str]":
        return self._category_labels

    def phonemes_for_category(self, category_id: str) -> List[PhonemeDefinition]:
        return list(self._by_category.get(category_id, ()))

    def get(self, name: str) -> Optional[PhonemeDefinition]:
        return self._by_name.get(name)

    def match_ipa_sequence(self, ipa_text: str) -> Tuple[List[PhonemeDefinition], str]:
        if not ipa_text:
            return [], ""
        position = 0
        matches: List[PhonemeDefinition] = []
        remainder: List[str] = []
        while position < len(ipa_text):
            char = ipa_text[position]
            if char.isspace():
                remainder.append(char)
                position += 1
                continue
            definition, ipa_value = self._match_at(ipa_text, position)
            if definition and ipa_value:
                matches.append(definition)
                position += len(ipa_value)
            else:
                remainder.append(char)
                position += 1
        return matches, "".join(remainder).strip()

    def _match_at(self, text: str, start: int) -> Tuple[Optional[PhonemeDefinition], Optional[str]]:
        for key in self._ipa_keys_desc:
            if text.startswith(key, start):
                definition = self._ipa_index.get(key)
                if definition:
                    return definition, key
        return None, None

    def default_category_id(self) -> Optional[str]:
        return next(iter(self._category_labels), None)

    def default_phoneme_for(self, category_id: str) -> Optional[PhonemeDefinition]:
        phonemes = self.phonemes_for_category(category_id)
        return phonemes[0] if phonemes else None


def load_default_inventory() -> PhonemeInventory:
    """Load the bundled eSpeak NG phoneme catalogue if present."""
    data_path = os.path.join(os.path.dirname(__file__), "eloquence_data", "espeak_phonemes.txt")
    if not os.path.exists(data_path):
        LOG.debug("Bundled eSpeak phoneme file is missing: %s", data_path)
        return PhonemeInventory([])
    try:
        with open(data_path, "r", encoding="utf-8") as source:
            phonemes = list(parse_espeak_phonemes(source))
    except OSError:
        LOG.exception("Unable to read eSpeak phoneme data from %s", data_path)
        return PhonemeInventory([])
    return PhonemeInventory(phonemes)


def parse_espeak_phonemes(lines: Iterable[str]) -> Iterator[PhonemeDefinition]:
    current_category: Optional[str] = None
    inside_block = False
    comment: str = ""
    name: str = ""
    ipa_values: List[str] = []
    attributes: List[Tuple[str, Tuple[str, ...]]] = []
    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()
        if not inside_block:
            if stripped.startswith("//"):
                label = _category_label(stripped[2:])
                if label:
                    current_category = label
                continue
            if stripped.startswith("phoneme"):
                inside_block = True
                before_comment, _, inline_comment = line.partition("//")
                tokens = before_comment.strip().split()
                if len(tokens) < 2:
                    inside_block = False
                    continue
                name = tokens[1]
                comment = inline_comment.strip()
                ipa_values = []
                attributes = []
                continue
            continue
        if stripped.startswith("endphoneme"):
            yield PhonemeDefinition(
                name=name,
                comment=comment,
                category=current_category,
                ipa=tuple(ipa_values),
                attributes=tuple(attributes),
            )
            inside_block = False
            continue
        before_comment, _, _ = line.partition("//")
        tokens = before_comment.strip().split()
        if not tokens:
            continue
        key = tokens[0]
        values = tokens[1:]
        if key == "ipa":
            ipa_value = _decode_ipa(values)
            if ipa_value:
                ipa_values.append(ipa_value)
        else:
            attributes.append((key, tuple(values)))


def _decode_ipa(tokens: Sequence[str]) -> str:
    parts: List[str] = []
    for token in tokens:
        decoded = _decode_ipa_token(token)
        if decoded:
            parts.append(decoded)
    return "".join(parts)


def _decode_ipa_token(token: str) -> str:
    if token == "NULL":
        return ""
    result: List[str] = []
    position = 0
    while position < len(token):
        match = _IPA_CODE_RE.search(token, position)
        if not match:
            result.append(token[position:])
            break
        start, end = match.span()
        if start > position:
            result.append(token[position:start])
        codepoint = int(match.group(1), 16)
        result.append(chr(codepoint))
        position = end
    return "".join(result)


def _category_label(comment_text: str) -> Optional[str]:
    stripped = comment_text.strip()
    stripped = stripped.strip(_CATEGORY_BORDER_CHARS)
    stripped = stripped.strip()
    return stripped or None


def _register_category(labels: "OrderedDict[str, str]", label: str) -> str:
    base = _slugify(label)
    candidate = base
    suffix = 2
    while candidate in labels and labels[candidate] != label:
        candidate = f"{base}-{suffix}"
        suffix += 1
    labels.setdefault(candidate, label)
    return candidate


def _slugify(label: str) -> str:
    slug = _NON_ID_CHAR_RE.sub("-", label.lower()).strip("-")
    return slug or "category"


def _find_word_start(text: str, position: int) -> int:
    while position > 0 and text[position - 1] not in " ,;:()[]{}\n\t/\\":
        position -= 1
    return position


def _find_word_end(text: str, position: int) -> int:
    while position < len(text) and text[position] not in " ,;:()[]{}\n\t/\\":
        position += 1
    return position


