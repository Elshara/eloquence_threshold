# Assets migration backlog

## Purpose
This backlog tracks every asset family that still needs work after the extension-first restructure. It tells NVDA builders, CodeQL reviewers, and documentation contributors which payloads are already packaged inside `assets/`, which ones remain parked under `speechdata/`, and how to rehearse the Eloquence/eSpeak NG/FonixTalk/NV Speech Player build without downloading anything new. Pair this checklist with the modernization audit so every incremental pull request documents what moved, which cached datasets were touched, and which tests were exercised before cutting a fresh `eloquence.nvda-addon`.

## How to use this backlog
1. Read the current status column for the framework you plan to touch.
2. Follow the recommended tooling commands to regenerate manifests or smoke tests before and after each migration.
3. Update the notes column with concrete deltas (new extensions, renamed fixtures, deleted caches) so the NVDA community can audit the cleanup trail.
4. When you finish a row, move the item into the "Packaged and verified" table and record the NVDA build plus CodeQL profile used for validation.

## In-progress migrations
| Framework / payload | Current staging area | Status | Next verification steps | Notes |
| --- | --- | --- | --- | --- |
| Eloquence runtime (DLLs, `.syn`, config) | `speechdata/eloquence/dll`, `speechdata/eloquence/syn`, `assets/txt/eci_*` | ⚙️ Runtime loaders updated, packaging rehearsal pending | `python -m unittest discover assets/py 'test_*.py'` then `python build.py --insecure --no-download --output dist/eloquence.nvda-addon` on NVDA alpha-52731 | Ensure [`assets/py/resource_paths.py`](../py/resource_paths.py) exposes every architecture probe before cutting new test builds. |
| NV Speech Player voices + phoneme data | `speechdata/nv_speech_player/dll`, `speechdata/speechplayerinespeak` | ⚠️ Extensionless dictionaries still under `speechdata/` | `python assets/py/report_speechdata_extensionless.py --print` to confirm recommended suffixes; update loaders once `.dict` aliases are safe | Document whether NV Speech Player expects legacy names; mirror the findings in [`assets/md/speechdata_extensionless_inventory.md`](speechdata_extensionless_inventory.md). |
| eSpeak NG lexicons & voices | `speechdata/speechplayerinespeak/espeak-ng-data` | ❌ Requires loader decisions before moving | After experimenting with suffixes, rerun `python assets/py/report_speechdata_inventory.py` and refresh [`assets/md/speechdata_manifest.md`](speechdata_manifest.md) | Coordinate with upstream [eSpeak NG](https://github.com/espeak-ng/espeak-ng) docs to keep IPA tables untouched until shims exist. |
| DECtalk / FonixTalk archives | `speechdata/dectalk/dll`, `assets/voice/dectalk_*`, `speechdata/fonixtalk` | ⚙️ Mixed layout; verify runtime search paths | `python -m unittest discover assets/py 'test_*dectalk*.py'` (to be authored) and capture CodeQL findings before moving archives | Check DataJake provenance when promoting new `.syn` templates; record sources in `assets/md/README.md`. |
| IBM TTS + Orpheus payloads | `speechdata/orpheus`, `speechdata/ibmtts` | 🗺️ Requires discovery helpers | Sketch loader hooks in `assets/py/resource_paths.py`, then stage manifests via `python assets/py/report_speechdata_inventory.py` | Align with [NV Speech Player](https://github.com/nvaccess/NVSpeechPlayer) expectations for multi-voice packages before merging. |
| Test fixtures (unit + CLI) | `assets/json`, `assets/ini`, `assets/txt/tests_*` | ⚠️ Need canonical fixture index | Extend this backlog with a `tests` section once fixture taxonomy settles; ensure `python -m unittest discover assets/py 'test_*.py'` covers every path | Keep cached NVDA manifests (`assets/ini/manifest.ini`) immutable; document overrides explicitly. |

## Packaged and verified
| Framework / payload | Verified on | Validation evidence | Follow-up |
| --- | --- | --- | --- |
| Documentation buckets (`assets/md`, `assets/pdf`) | NVDA alpha-52731, CodeQL Python security profile | `python assets/py/report_assets_layout.py --print` and diff review of Markdown snapshots | Refresh language maturity dashboards after every sprint (`python tools/report_language_maturity.py`). |

## Upcoming asset families
- **Generative pronunciation layers**: Stage training corpora and exported JSON controls under `assets/json/pronunciation_*`. Reference the contextual phoneme workflows described in the README so blind users know how WASAPI sample-rate tracking clamps EQ bands.
- **Equalizer APO alignment datasets**: Preserve imports under `assets/txt/eq_apo_*` and keep [`docs/eq_apo_alignment.md`](../../docs/eq_apo_alignment.md) in sync with new presets. Mention Equalizer APO when onboarding new contributors so they understand the Windows audio pipeline integration.
- **Wikipedia/DataJake research snapshots**: Until the remaining tooling is ported, keep cached outputs in `assets/json/research_*` and mirror summaries in `assets/md/*_research.md`. Run `python tools/catalog_wikipedia_languages.py` and `python tools/catalog_datajake_archives.py` from a cached clone; never redownload archives inside review branches.

## Reporting cadence
- Run `python assets/py/report_assets_layout.py --json assets/json/assets_layout_summary.json --markdown assets/md/assets_layout_summary.md --print` after moving any files between extension buckets. This keeps NVDA packaging rehearsals reproducible.
- Regenerate `speechdata` manifests (`python assets/py/report_speechdata_inventory.py` and `python assets/py/report_speechdata_extensionless.py --print`) before sending PRs that rename or delete datasets. Attach the refreshed JSON/Markdown so CodeQL can verify the diff automatically.
- Exercise `python -m unittest discover assets/py 'test_*.py'` whenever loader shims or CLI tools change. Capture the log in the PR description so reviewers can compare with prior runs.
- Finish with `python build.py --insecure --no-download --output dist/eloquence.nvda-addon` on a cached NVDA checkout. Note which snapshot (for example, alpha-52731) you used and record any warnings in the modernization audit.

## Updating this backlog
When you land a migration:
1. Update the appropriate row with the new extension bucket, loader shim, or manifest location.
2. Reference upstream sources (NVDA, eSpeak NG, NV Speech Player, DECtalk/FonixTalk archives, DataJake mirrors) so provenance stays clear.
3. Link to the test and build commands you executed. If CodeQL flagged anything, describe the follow-up tasks required before publishing an add-on update.
4. Announce the change in [`assets/md/file_structure_audit.md`](file_structure_audit.md) and the top-level README so future contributors inherit the context.

By keeping this backlog current we make the extension-first strategy auditable, preserve offline packaging guarantees, and help blind and low-vision users follow the roadmap toward a multilingual, mix-and-match Eloquence experience.
