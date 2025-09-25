"""Language profile loader for character-level pronunciation hints."""
from __future__ import annotations

import json
import logging
import os
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

LOG = logging.getLogger(__name__)

_DATA_DIR = os.path.join(os.path.dirname(__file__), "eloquence_data", "languages")


@dataclass(frozen=True)
class CharacterPronunciation:
    symbol: str
    spoken: Optional[str]
    ipa: Tuple[str, ...]
    description: str
    example: Optional[str]
    stress: Optional[str]
    notes: Tuple[str, ...]

    def fallback_hint(self) -> str:
        pieces: List[str] = []
        label = self.spoken or " ".join(self.ipa) or self.symbol
        pieces.append(f"{self.symbol} – {label}")
        ipa_text = " ".join(self.ipa)
        if ipa_text and ipa_text != label:
            pieces.append(f"IPA {ipa_text}")
        if self.example:
            pieces.append(f"as in {self.example}")
        if self.stress:
            pieces.append(self.stress)
        pieces.extend(self.notes)
        return ", ".join(piece for piece in pieces if piece)


@dataclass
class LanguageProfile:
    id: str
    language: str
    display_name: str
    description: str
    tags: Tuple[str, ...]
    characters: "OrderedDict[str, CharacterPronunciation]"
    stress_notes: Tuple[str, ...]
    sentence_structure: Tuple[str, ...]
    grammar_notes: Tuple[str, ...]
    default_voice_templates: Tuple[str, ...]
    _lowercase_index: Dict[str, CharacterPronunciation] = field(init=False, repr=False)
    _max_symbol_length: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._lowercase_index = {}
        max_len = 1
        for symbol, entry in self.characters.items():
            lower = symbol.lower()
            if lower not in self._lowercase_index:
                self._lowercase_index[lower] = entry
            if len(symbol) > max_len:
                max_len = len(symbol)
        self._max_symbol_length = max_len

    def display_label(self) -> str:
        pieces: List[str] = [self.display_name]
        if self.language:
            pieces.append(self.language)
        if self.description:
            pieces.append(self.description)
        return " – ".join(piece for piece in pieces if piece)

    def describe_characters(
        self, text: str
    ) -> List[Tuple[str, Optional[CharacterPronunciation]]]:
        """Return the pronunciation entries that best match *text*.

        The result preserves the order of the supplied characters and includes
        unmatched symbols so callers can highlight gaps in the profile. Space
        characters are returned with a ``None`` entry to keep positional context
        intact while signalling that no pronunciation hint is required.
        """

        matches: List[Tuple[str, Optional[CharacterPronunciation]]] = []
        position = 0
        length = len(text)
        while position < length:
            char = text[position]
            if char.isspace():
                matches.append((char, None))
                position += 1
                continue
            matched_symbol: Optional[str] = None
            matched_entry: Optional[CharacterPronunciation] = None
            for size in range(self._max_symbol_length, 0, -1):
                if position + size > length:
                    continue
                fragment = text[position : position + size]
                entry = self.characters.get(fragment)
                if entry is None:
                    entry = self._lowercase_index.get(fragment.lower())
                if entry is not None:
                    matched_symbol = fragment
                    matched_entry = entry
                    position += size
                    break
            if matched_symbol is None:
                matched_symbol = text[position]
                position += 1
            matches.append((matched_symbol, matched_entry))
        return matches

    def describe_text(self, text: str) -> str:
        hints: List[str] = []
        for _symbol, entry in self.describe_characters(text):
            if entry is None:
                continue
            hints.append(entry.fallback_hint())
        return "; ".join(hints)


class LanguageProfileCatalog:
    def __init__(self, profiles: Iterable[LanguageProfile]) -> None:
        self._profiles: "OrderedDict[str, LanguageProfile]" = OrderedDict()
        for profile in profiles:
            if not profile.id:
                continue
            if profile.id in self._profiles:
                LOG.debug("Duplicate language profile '%s' ignored", profile.id)
                continue
            self._profiles[profile.id] = profile

    @property
    def is_empty(self) -> bool:
        return not self._profiles

    def get(self, profile_id: Optional[str]) -> Optional[LanguageProfile]:
        if not profile_id:
            return None
        return self._profiles.get(profile_id)

    def __iter__(self) -> Iterator[LanguageProfile]:
        return iter(self._profiles.values())

    def profiles(self) -> List[LanguageProfile]:
        return list(self._profiles.values())

    def find_best_match(self, language_tag: Optional[str]) -> Optional[LanguageProfile]:
        """Return the profile that best matches *language_tag*.

        Matching first checks the explicit ``language`` field on each profile using
        BCP-47 case folding rules. If no exact match exists, profiles sharing the
        same base language (for example ``es`` matching ``es-ES``) are considered.
        As a final fallback we inspect profile identifiers and tags, including any
        ``lang:*`` tags contributors might provide, so custom locales can still be
        discovered.
        """

        if not language_tag:
            return None
        normalized = normalize_language_tag(language_tag)
        if not normalized:
            return None
        normalized_lower = normalized.lower()
        base = normalized_lower.split("-", 1)[0]

        specific_match: Optional[LanguageProfile] = None
        generic_match: Optional[LanguageProfile] = None
        for profile in self._profiles.values():
            candidate = normalize_language_tag(profile.language or "")
            if not candidate:
                continue
            candidate_lower = candidate.lower()
            if candidate_lower == normalized_lower:
                return profile
            if base:
                if candidate_lower.startswith(f"{base}-") and specific_match is None:
                    specific_match = profile
                elif candidate_lower == base and generic_match is None:
                    generic_match = profile
        if specific_match:
            return specific_match
        if generic_match:
            return generic_match

        targets = {normalized_lower}
        if base:
            targets.add(base)
        for profile in self._profiles.values():
            tokens = {profile.id.lower()}
            if profile.language:
                tokens.add(normalize_language_tag(profile.language).lower())
            for tag in profile.tags:
                token = str(tag).strip().lower()
                tokens.add(token)
                if token.startswith("lang:"):
                    tokens.add(token.split(":", 1)[1])
            if targets & tokens:
                return profile
        return None


def load_default_language_profiles() -> LanguageProfileCatalog:
    if not os.path.isdir(_DATA_DIR):
        LOG.info("No language profiles found under %s", _DATA_DIR)
        return LanguageProfileCatalog([])
    profiles: List[LanguageProfile] = []
    for name in sorted(os.listdir(_DATA_DIR)):
        if not name.lower().endswith(".json"):
            continue
        path = os.path.join(_DATA_DIR, name)
        try:
            with open(path, "r", encoding="utf-8") as source:
                data = json.load(source)
        except (OSError, json.JSONDecodeError):
            LOG.exception("Unable to parse language profile %s", path)
            continue
        profile = _parse_language_profile(data)
        if profile is not None:
            profiles.append(profile)
    return LanguageProfileCatalog(profiles)


def _parse_language_profile(data: Dict[str, object]) -> Optional[LanguageProfile]:
    profile_id = data.get("id")
    if not profile_id:
        LOG.warning("Ignoring language profile without id. Keys: %r", list(data.keys()))
        return None
    characters = OrderedDict()
    raw_characters = data.get("characters", [])
    if isinstance(raw_characters, list):
        for entry in raw_characters:
            parsed = _parse_character_entry(entry)
            if parsed is not None and parsed.symbol not in characters:
                characters[parsed.symbol] = parsed
    tags: Tuple[str, ...]
    raw_tags = data.get("tags", ())
    if isinstance(raw_tags, (list, tuple)):
        tags = tuple(str(tag) for tag in raw_tags)
    elif isinstance(raw_tags, str):
        tags = (raw_tags,)
    else:
        tags = ()
    stress_notes = _tuple_from_field(data.get("stress", ()))
    sentence_structure = _tuple_from_field(data.get("sentenceStructure", ()))
    grammar_notes = _tuple_from_field(data.get("grammar", ()))
    defaults = _tuple_from_field(data.get("defaultVoiceTemplates", ()))
    return LanguageProfile(
        id=str(profile_id),
        language=str(data.get("language", "")),
        display_name=str(data.get("displayName", profile_id)),
        description=str(data.get("description", "")),
        tags=tags,
        characters=characters,
        stress_notes=stress_notes,
        sentence_structure=sentence_structure,
        grammar_notes=grammar_notes,
        default_voice_templates=defaults,
    )


def _parse_character_entry(entry: object) -> Optional[CharacterPronunciation]:
    if not isinstance(entry, dict):
        return None
    symbol = entry.get("symbol")
    if not symbol:
        return None
    raw_ipa = entry.get("ipa", ())
    if isinstance(raw_ipa, str):
        ipa = tuple(part.strip() for part in raw_ipa.split(" ") if part.strip())
    elif isinstance(raw_ipa, (list, tuple)):
        ipa = tuple(str(part) for part in raw_ipa if str(part))
    else:
        ipa = ()
    notes = _tuple_from_field(entry.get("notes", ()))
    return CharacterPronunciation(
        symbol=str(symbol),
        spoken=str(entry["spoken"]) if "spoken" in entry and entry["spoken"] is not None else None,
        ipa=ipa,
        description=str(entry.get("description", "")),
        example=str(entry["example"]) if "example" in entry and entry["example"] is not None else None,
        stress=str(entry["stress"]) if "stress" in entry and entry["stress"] is not None else None,
        notes=notes,
    )


def _tuple_from_field(field: object) -> Tuple[str, ...]:
    if isinstance(field, str):
        return (field,) if field else ()
    if isinstance(field, (list, tuple)):
        return tuple(str(item) for item in field if str(item))
    return ()


def normalize_language_tag(language_tag: str) -> str:
    """Normalise a BCP-47 language tag for comparisons."""

    if not language_tag:
        return ""
    parts = language_tag.replace("_", "-").split("-")
    normalised: List[str] = []
    for index, part in enumerate(parts):
        if not part:
            continue
        if index == 0:
            normalised.append(part.lower())
        elif len(part) == 2:
            normalised.append(part.upper())
        elif len(part) == 4:
            normalised.append(part.title())
        else:
            normalised.append(part.lower())
    return "-".join(normalised)
