"""Language profile loader for character-level pronunciation hints."""
from __future__ import annotations

import json
import logging
import os
import re
from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from statistics import median
from typing import TYPE_CHECKING, Dict, Iterable, Iterator, List, Optional, Tuple

if TYPE_CHECKING:
    from phoneme_catalog import PhonemeInventory
    from voice_catalog import VoiceCatalog, VoiceTemplate

LOG = logging.getLogger(__name__)

_REPO_ROOT = os.path.dirname(__file__)
_DATA_DIR = os.path.join(_REPO_ROOT, "eloquence_data", "languages")
_DOCS_DIR = os.path.join(_REPO_ROOT, "docs")
_WIKIPEDIA_INDEX_PATH = os.path.join(_DOCS_DIR, "wikipedia_language_index.json")


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
    _progress_cache: Optional[Dict[str, object]] = field(default=None, init=False, repr=False)

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

    def metrics(self, inventory: Optional["PhonemeInventory"] = None) -> Dict[str, object]:
        """Return cached progress metadata for this profile."""

        if self._progress_cache is not None and (
            inventory is None or self._progress_cache.get("_inventory_id") is inventory
        ):
            cached = dict(self._progress_cache)
            cached.pop("_inventory_id", None)
            return cached

        total_characters = len(self.characters)
        multi_character = 0
        uppercase_count = 0
        with_ipa = 0
        ipa_covered = 0
        ipa_tokens: set[str] = set()
        fallback_total = 0
        description_total = 0
        notes_total = 0
        spoken_total = 0
        example_total = 0
        contextual_total = 0
        stress_total = len(self.stress_notes)
        sentence_total = len(self.sentence_structure)
        grammar_total = len(self.grammar_notes)
        no_ipa_symbols: List[str] = []
        unmatched_symbols: List[str] = []

        inventory_ref: Optional["PhonemeInventory"] = inventory

        for symbol, entry in self.characters.items():
            if len(symbol) > 1:
                multi_character += 1
            if symbol != symbol.lower():
                uppercase_count += 1
            if entry.description:
                description_total += 1
            if entry.notes:
                notes_total += len(entry.notes)
            if entry.spoken:
                spoken_total += 1
            if entry.example:
                example_total += 1
            if entry.stress:
                contextual_total += 1
            if entry.fallback_hint():
                fallback_total += 1
            ipa_values = tuple(token for token in entry.ipa if token)
            if not ipa_values:
                no_ipa_symbols.append(symbol)
                continue
            with_ipa += 1
            ipa_tokens.update(ipa_values)
            if not inventory_ref:
                continue
            sequence = " ".join(ipa_values)
            matches, remainder = inventory_ref.match_ipa_sequence(sequence)
            if matches and not remainder:
                ipa_covered += 1
            else:
                unmatched_symbols.append(symbol)

        coverage_ratio = ipa_covered / with_ipa if with_ipa else 0.0
        example_ratio = example_total / total_characters if total_characters else 0.0
        structure_bonus = 0.0
        if stress_total:
            structure_bonus += 0.05
        if sentence_total:
            structure_bonus += 0.05
        if grammar_total:
            structure_bonus += 0.05
        progress_score = min(
            1.0,
            coverage_ratio
            + example_ratio * 0.2
            + structure_bonus
            + (0.05 if multi_character else 0.0)
            + (0.05 if fallback_total >= total_characters else 0.0),
        )

        if total_characters == 0:
            stage = "empty"
        elif progress_score >= 0.9:
            stage = "comprehensive"
        elif progress_score >= 0.65:
            stage = "established"
        elif progress_score >= 0.4:
            stage = "developing"
        else:
            stage = "seed"

        metrics: Dict[str, object] = {
            "id": self.id,
            "language": self.language,
            "displayName": self.display_name,
            "description": self.description,
            "tags": list(self.tags),
            "characterCount": total_characters,
            "multiCharacterCount": multi_character,
            "uppercaseCharacterCount": uppercase_count,
            "charactersWithIPA": with_ipa,
            "charactersWithoutIPA": no_ipa_symbols[:25],
            "charactersWithUnmatchedIPA": unmatched_symbols[:25],
            "ipaCoveredCount": ipa_covered,
            "ipaCoverageRatio": round(coverage_ratio, 4),
            "ipaCoveragePercent": round(coverage_ratio * 100, 2),
            "uniqueIpaCount": len(ipa_tokens),
            "fallbackHintCount": fallback_total,
            "descriptionCount": description_total,
            "notesTotal": notes_total,
            "spokenCount": spoken_total,
            "exampleCount": example_total,
            "contextualCount": contextual_total,
            "stressNoteCount": stress_total,
            "sentenceStructureNoteCount": sentence_total,
            "grammarNoteCount": grammar_total,
            "defaultVoiceTemplates": list(self.default_voice_templates),
            "keyboardOptimised": multi_character > 0,
            "hasGenerativeHints": any(
                str(tag).lower().startswith("generative") for tag in self.tags
            ),
            "hasContextualHints": any(
                str(tag).lower().startswith("context") for tag in self.tags
            ),
            "progressScore": round(progress_score, 4),
            "stage": stage,
        }

        metrics["_inventory_id"] = inventory_ref
        self._progress_cache = dict(metrics)
        result = dict(metrics)
        result.pop("_inventory_id", None)
        return result

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

    def metrics(
        self,
        inventory: Optional["PhonemeInventory"] = None,
        voice_catalog: Optional["VoiceCatalog"] = None,
    ) -> Dict[str, object]:
        """Return a repository-wide summary of language profile progress."""

        entries = []
        for profile in self._profiles.values():
            entry = profile.metrics(inventory)
            if voice_catalog is not None:
                entry.update(
                    _voice_links_for_profile(
                        profile,
                        entry,
                        voice_catalog,
                    )
                )
            entries.append(entry)

        if not entries:
            return {
                "generatedAt": datetime.now(timezone.utc).isoformat(),
                "totalProfiles": 0,
                "stats": {},
                "entries": [],
            }

        coverage_values = [entry.get("ipaCoverageRatio", 0.0) for entry in entries]
        stage_counter = Counter(entry.get("stage", "unknown") for entry in entries)
        total_characters = sum(entry.get("characterCount", 0) for entry in entries)
        stats = {
            "totalProfiles": len(entries),
            "stageCounts": dict(stage_counter),
            "averageIpaCoverage": round(
                sum(coverage_values) / len(coverage_values), 4
            ),
            "medianIpaCoverage": round(median(coverage_values), 4),
            "totalCharacters": int(total_characters),
            "profilesWithExamples": sum(
                1 for entry in entries if entry.get("exampleCount", 0) > 0
            ),
            "profilesWithTemplates": sum(
                1 for entry in entries if entry.get("matchedDefaultTemplates")
            ),
        }

        entries.sort(
            key=lambda item: (
                -float(item.get("progressScore", 0.0)),
                item.get("displayName", ""),
            )
        )

        return {
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "totalProfiles": len(entries),
            "stats": stats,
            "entries": entries,
        }

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
        if isinstance(data, dict) and "profiles" in data and isinstance(data["profiles"], list):
            payloads = [entry for entry in data["profiles"] if isinstance(entry, dict)]
        else:
            payloads = [data]
        for payload in payloads:
            profile = _parse_language_profile(payload)
            if profile is not None:
                profiles.append(profile)
    return LanguageProfileCatalog(profiles)


def _sanitize_for_log(obj: object) -> object:
    """Recursively strip control characters from log payloads."""

    if isinstance(obj, str):
        return obj.replace("\n", "").replace("\r", "")
    if isinstance(obj, dict):
        return {str(_sanitize_for_log(key)): _sanitize_for_log(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_for_log(item) for item in obj]
    if isinstance(obj, tuple):
        return tuple(_sanitize_for_log(item) for item in obj)
    return obj


def _parse_language_profile(data: Dict[str, object]) -> Optional[LanguageProfile]:
    profile_id = data.get("id")
    if not profile_id:
        sanitized_data = _sanitize_for_log(data)
        LOG.warning(
            "Ignoring language profile without id. Keys: %r Payload: %r",
            sorted(data.keys()),
            sanitized_data,
        )
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


def _normalize_text(value: str) -> str:
    """Collapse internal whitespace and trim surrounding space."""

    collapsed = re.sub(r"\s+", " ", value.strip())
    return collapsed


def _optional_text(entry: Dict[str, object], key: str) -> Optional[str]:
    if key not in entry or entry[key] is None:
        return None
    text = _normalize_text(str(entry[key]))
    return text or None


def _iter_ipa_tokens(raw_ipa: object) -> Iterator[str]:
    if isinstance(raw_ipa, str):
        for token in raw_ipa.split():
            cleaned = _normalize_text(token)
            if cleaned:
                yield cleaned
        return
    if isinstance(raw_ipa, (list, tuple)):
        for part in raw_ipa:
            if part is None:
                continue
            if isinstance(part, str):
                for token in part.split():
                    cleaned = _normalize_text(token)
                    if cleaned:
                        yield cleaned
            else:
                cleaned = _normalize_text(str(part))
                if cleaned:
                    yield cleaned
        return
    if raw_ipa is not None:
        cleaned = _normalize_text(str(raw_ipa))
        if cleaned:
            yield cleaned


def _parse_character_entry(entry: object) -> Optional[CharacterPronunciation]:
    if not isinstance(entry, dict):
        return None
    symbol = entry.get("symbol")
    if not symbol:
        return None
    raw_ipa = entry.get("ipa", ())
    ipa = tuple(_iter_ipa_tokens(raw_ipa))
    notes = _tuple_from_field(entry.get("notes", ()))
    return CharacterPronunciation(
        symbol=str(symbol),
        spoken=_optional_text(entry, "spoken"),
        ipa=ipa,
        description=_normalize_text(str(entry.get("description", ""))),
        example=_optional_text(entry, "example"),
        stress=_optional_text(entry, "stress"),
        notes=notes,
    )


def _tuple_from_field(field: object) -> Tuple[str, ...]:
    if isinstance(field, str):
        value = _normalize_text(field)
        return (value,) if value else ()
    if isinstance(field, (list, tuple)):
        values: List[str] = []
        for item in field:
            if item is None:
                continue
            value = _normalize_text(str(item))
            if value:
                values.append(value)
        return tuple(values)
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


def _voice_links_for_profile(
    profile: LanguageProfile,
    metrics: Dict[str, object],
    catalog: "VoiceCatalog",
) -> Dict[str, object]:
    matched_templates: List[str] = []
    missing_templates: List[str] = []
    requested = [str(item) for item in metrics.get("defaultVoiceTemplates", [])]
    for template_id in requested:
        template = catalog.get(template_id)
        if template is None:
            missing_templates.append(template_id)
        else:
            matched_templates.append(template.id)

    language_key = normalize_language_tag(profile.language or "")
    available_templates: List[str] = []
    for template in catalog.templates():
        template_id = getattr(template, "id", None)
        template_language = normalize_language_tag(getattr(template, "language", "") or "")
        default_profile = getattr(template, "default_language_profile", None)
        if default_profile and default_profile == profile.id:
            available_templates.append(template_id)
        elif language_key and template_language == language_key:
            available_templates.append(template_id)

    available_templates = sorted({item for item in available_templates if item})

    return {
        "matchedDefaultTemplates": matched_templates,
        "missingDefaultTemplates": missing_templates,
        "availableTemplateCount": len(available_templates),
        "availableTemplates": available_templates,
    }


def load_wikipedia_language_index(path: Optional[str] = None) -> Dict[str, List[Dict[str, object]]]:
    """Load the cached Wikipedia language index and group entries by tag."""

    file_path = path or _WIKIPEDIA_INDEX_PATH
    if not os.path.exists(file_path):
        LOG.warning("Wikipedia language index not found at %s", file_path)
        return {tag: [] for tag in ("language", "dialect", "accent", "sign-language", "orthography")}

    with open(file_path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    entries = payload.get("entries", [])
    base_tags = ("language", "dialect", "accent", "sign-language", "orthography")
    grouped: "OrderedDict[str, List[Dict[str, object]]]" = OrderedDict(
        (tag, []) for tag in base_tags
    )
    extras: "OrderedDict[str, List[Dict[str, object]]]" = OrderedDict()

    for entry in entries:
        record = {
            "title": entry.get("title", ""),
            "url": entry.get("url"),
            "breadcrumbs": entry.get("breadcrumbs", []),
            "tags": entry.get("tags", []),
        }
        tags = record["tags"] or ["language"]
        assigned = False
        for tag in tags:
            bucket = grouped.get(tag)
            if bucket is not None:
                bucket.append(record)
                assigned = True
                continue
            extras.setdefault(tag, []).append(record)
            assigned = True
        if not assigned:
            grouped["language"].append(record)

    for tag, records in extras.items():
        grouped.setdefault(tag, []).extend(records)

    return grouped
