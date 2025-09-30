#!/usr/bin/env python3
"""Preview language profile pronunciation hints from the command line.

This helper loads the bundled language profile catalogue and lets
contributors inspect how a profile would describe arbitrary text when
NVDA emits phoneme fallbacks. It is a lightweight way to review
community submissions, prototype new characters, and share feedback on
pronunciation coverage without installing the add-on.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional, Sequence, Tuple

import resource_paths

from language_profiles import (
    LanguageProfile,
    LanguageProfileCatalog,
    load_default_language_profiles,
    normalize_language_tag,
)


def list_profiles(catalog: LanguageProfileCatalog) -> None:
    profiles = catalog.profiles()
    if not profiles:
        print("No language profiles are bundled with this checkout.", file=sys.stderr)
        return
    width = max(len(profile.id) for profile in profiles)
    for profile in profiles:
        label = profile.display_label()
        print(f"{profile.id.ljust(width)}  {label}")


def _format_symbol(symbol: str) -> str:
    parts: List[str] = []
    for char in symbol:
        if char == " ":
            parts.append("␠")
        elif char == "\n":
            parts.append("\\n")
        elif char == "\r":
            parts.append("\\r")
        elif char == "\t":
            parts.append("\\t")
        else:
            parts.append(char)
    return "".join(parts) or "⌀"


def show_character_table(profile: LanguageProfile) -> None:
    entries: List[Tuple[str, str]] = []
    for symbol, pronunciation in profile.characters.items():
        label = pronunciation.fallback_hint()
        entries.append((_format_symbol(symbol), label))
    if not entries:
        print("This profile does not define any character pronunciations yet.")
        return
    width = max(len(symbol) for symbol, _ in entries)
    print("Symbol".ljust(width), "Description", sep="  ")
    print("-" * width, "-" * 40, sep="  ")
    for symbol, label in entries:
        print(symbol.ljust(width), label, sep="  ")


def describe_text(profile: LanguageProfile, text: str, per_character: bool) -> None:
    matches = profile.describe_characters(text)
    if per_character:
        if not matches:
            print("No characters were provided.")
        else:
            width = max(len(_format_symbol(symbol)) for symbol, _entry in matches)
            print("Input".ljust(width), "Hint", sep="  ")
            print("-" * width, "-" * 40, sep="  ")
            for symbol, entry in matches:
                formatted = _format_symbol(symbol)
                if entry is None:
                    hint = "(no mapping)"
                else:
                    hint = entry.fallback_hint()
                print(formatted.ljust(width), hint, sep="  ")
            print()
    summary = profile.describe_text(text)
    if summary:
        print("Fallback summary:")
        print(summary)
    else:
        print("No pronunciation hints were generated for the supplied text.")


def select_profile(
    catalog: LanguageProfileCatalog, profile_id: Optional[str], language: Optional[str]
) -> Optional[LanguageProfile]:
    if profile_id:
        candidate = catalog.get(profile_id)
        if candidate:
            return candidate
        raise SystemExit(
            f"Unknown language profile '{profile_id}'. Use --list-profiles to explore options."
        )
    if language:
        normalized = normalize_language_tag(language)
        candidate = catalog.find_best_match(normalized)
        if candidate:
            return candidate
        raise SystemExit(
            f"No bundled profile matches the language tag '{language}'. Try --list-profiles."
        )
    profiles = catalog.profiles()
    if len(profiles) == 1:
        return profiles[0]
    if not profiles:
        return None
    raise SystemExit(
        "Multiple profiles are available. Specify one with --profile or provide a language tag with --language."
    )


def parse_arguments(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect the bundled language profiles and preview the fallback hints "
            "Eloquence will announce when NVDA emits phoneme commands."
        )
    )
    parser.add_argument(
        "text",
        nargs="*",
        help=(
            "Text to analyse. If omitted, the tool reads from standard input so you "
            "can pipe longer passages directly."
        ),
    )
    parser.add_argument(
        "-p",
        "--profile",
        help="Language profile identifier (see --list-profiles for the available options).",
    )
    parser.add_argument(
        "-l",
        "--language",
        help=(
            "BCP-47 language tag used to pick the closest profile automatically. "
            "Examples include en-US, es-ES, and pt-BR."
        ),
    )
    parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="List all bundled language profiles and exit.",
    )
    parser.add_argument(
        "--show-characters",
        action="store_true",
        help="Print the pronunciation table for the selected profile before analysing text.",
    )
    parser.add_argument(
        "--per-character",
        action="store_true",
        help="Display hints for each character in addition to the combined summary.",
    )
    return parser.parse_args(argv)


def read_text(arguments: argparse.Namespace) -> str:
    if arguments.text:
        return " ".join(arguments.text)
    if sys.stdin.isatty():
        return ""
    return sys.stdin.read()


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = parse_arguments(argv)
    catalog = load_default_language_profiles()
    if catalog.is_empty:
        targets = [str(path) for path in resource_paths.language_profile_directories()]
        if not targets:
            targets = [str(resource_paths.asset_dir("json"))]
        hint = ", ".join(targets)
        raise SystemExit(
            f"No language profiles were found. Ensure the JSON bundles in {hint} include language entries."
        )
    if arguments.list_profiles:
        list_profiles(catalog)
        return 0
    profile = select_profile(catalog, arguments.profile, arguments.language)
    if profile is None:
        targets = [str(path) for path in resource_paths.language_profile_directories()]
        if not targets:
            targets = [str(resource_paths.asset_dir("json"))]
        hint = ", ".join(targets)
        raise SystemExit(
            f"No language profiles are available. Populate {hint} with language JSON files first."
        )
    print(f"Using profile: {profile.display_label()} ({profile.id})")
    if arguments.show_characters:
        show_character_table(profile)
        print()
    text = read_text(arguments)
    if not text:
        if not arguments.show_characters:
            print(
                "No text was supplied. Provide a sample as arguments or pipe it through stdin to preview hints.",
                file=sys.stderr,
            )
            return 1
        return 0
    describe_text(profile, text, arguments.per_character)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
