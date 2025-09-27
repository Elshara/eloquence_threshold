# DataJake Archive Recovery Guide

This guide rebuilds the complete DataJake text-to-speech inventory so the Eloquence for NVDA community can focus on portable
source code, scripting utilities, and reusable phoneme data while discarding assets that only duplicate audio demos. The
classification is generated from the historical URL list (restored in `docs/datajake_archive_urls.txt`) using
`python tools/catalog_datajake_archives.py`, which emits a machine-readable manifest (`docs/archive_inventory.json`) and a
full Markdown catalogue (`docs/archive_inventory.md`).

## Workflow summary

1. **Sync the manifest.** Update `docs/datajake_archive_urls.txt` when new mirrors appear, then re-run the cataloguing script.
2. **Prioritise code and tooling.** Filter the manifest for `Source/tooling archive` and `NVDA add-on package` entries—those
   payloads contain build systems, pronunciation dictionaries, and NVDA driver code we can port into this fork.
3. **Scrap non-code payloads.** Files marked as `Audio sample`, `Documentation`, `Binary installer`, or `Generic archive` are
   considered non-actionable for Eloquence integration unless no other source exists. Retain notes in the manifest but avoid
   pulling the binaries into the repository.
4. **Map viable imports.** Track active porting tasks in `docs/archive_code_targets.md`, which summarises how each synthesizer
   family can expand Eloquence voices, phoneme inventories, or NVDA configuration tooling.
5. **Review viability tiers.** Use the manifest's `Viability summary` to prioritise new phoneme/lexicon candidates and flag
   truncated links that require manual repair before mirroring.
6. **Link scenes back to provenance.** Refresh `docs/voice_scene_catalog.{json,md}` with
   `python tools/export_voice_scenes.py --json docs/voice_scene_catalog.json --markdown docs/voice_scene_catalog.md --print` so
   every curated NVDA voice scene documents which DataJake archives (eSpeak NG bundles, DECtalk installers, NV Speech Player
   toolkits) informed the phoneme EQ and slider presets.

## High-value code collections

| Collection | Items flagged as code/tooling | Key opportunities |
| --- | ---: | --- |
| eSpeak releases | 213 | Extract MBROLA/IPA tables to enhance Eloquence's multilingual phoneme coverage and align with NVDA's language picker. |
| NVDA synthesizer add-ons | 55 | Unpack Python drivers (BeSTspeech, Brailab PC, Festival, JTalk) to compare configuration APIs, WASAPI handling, and phoneme mapping strategies. |
| SAPI voice kits | 11 | Review SAPI 4/5 bridge layers (IBM ViaVoice, RealSpeak, RHVoice) for reusable lexicon formats and language switching logic. |
| DECtalk toolchain/source | 7 | Cross-check DECtalk build scripts, ANSI-C phoneme tables, and dictionary tooling against Eloquence presets for retro-compatibility. |
| Legacy Eloquence/Fonix drops | 5 | Locate documentation and runtime DLLs that clarify voice parameter ranges, timbre defaults, and dictionary packaging. |

See `docs/archive_code_targets.md` for synthesizer-specific porting notes and example integration tasks.

## Extension and dataset index

- `docs/archive_inventory.md` now surfaces `File extension index`, `Sample rate hints`, `Language hints`, a `Viability summary`, and a new `Priority tag summary` so we can prioritise IPA dictionaries, lexicons, and other phoneme-friendly payloads before downloading redundant demo audio. Documentation fragments without extensions are now caught automatically, keeping provenance tidy.
- `docs/archive_inventory.json` stores the same catalogue plus machine-readable summaries under the top-level `summaries` key. Each record now includes a `metadata` block with decoded filenames, detected sample rates, language hints, voice names (where present), inferred viability tiers, and priority tags so automated importers understand whether an archive contains tooling, NVDA add-on code, or phoneme-ready dictionaries.
- After updating `docs/datajake_archive_urls.txt`, rerun `python tools/catalog_datajake_archives.py` and scan the extension totals for new `.lex`, `.ipa`, or language-tagged archives that warrant fast-tracked extraction into `phoneme_catalog.py` or `language_profiles.py`.
- When a new archive directly informs a curated scene, capture the impact inside `docs/voice_scene_catalog.md` so NVDA testers
  can trace how phoneme EQ macros, slider tweaks, and language targets map back to DataJake.


## Scrap categories

The manifest flags 868 audio-only files and 218 binary installers. These are preserved for provenance but are not part of the
active Eloquence roadmap. Contributors should rely on the JSON/Markdown manifest for historical reference while concentrating
engineering effort on archives labelled as source, tooling, or NVDA add-ons.

## Updating this guide

- Regenerate the manifest after auditing new mirrors or when additional NVDA add-ons are published. The JSON output makes it easy to diff viability changes inside pull requests.
- Cross-reference the extension, sample-rate, and language summaries before downloading large payloads so phoneme/lexicon bundles reach the pipeline ahead of demo audio.
- When new code paths are imported into the repository, update `docs/archive_code_targets.md` with the implemented outcome and link the corresponding manifest rows. Use the manifest priority tags (`tooling_candidate`, `phoneme_or_lexicon`, `voice_or_language_pack`) to describe which payloads powered each import so future contributors can retrace decisions quickly.
- Surface major catalogue updates in `README.md` so NVDA community testers understand which external synthesizers now inform Eloquence's phoneme engine and configuration workflows.
