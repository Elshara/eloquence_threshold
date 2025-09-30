# File structure modernization audit

## Context and motivation
The current tree reflects the "assets by extension" reshuffle that moved the legacy `eloquence/`, `espeak-ng-data/`, DECtalk/FonixTalk payloads, and supporting documentation into `assets/<extension>/<descriptive_name>.<extension>` directories. The goal is to make the repository easier to reason about while we continue packaging the unified `eloquence.nvda-addon` bundle for modern [NVDA](https://github.com/nvaccess/nvda/) builds. Keeping the structure disciplined also helps CodeQL rulepacks reason about where binary payloads, Python tooling, and Markdown roadmaps live when we run the offline packaging drills captured in [`assets/md/offline_packaging_playbook.md`](offline_packaging_playbook.md).

## Inventory snapshot (2025-10-26)
- `assets/` now contains 22 extension-scoped directories. The heaviest buckets are `py` (72 files), `dll` (44 files), `txt` (44 files), `json` (41 files), and `syn` (36 files). No mismatched extensions were detected inside the asset folders, so the renaming pass stayed internally consistent.
- `speechdata/` still stages the frameworks that rely on extensionless resources. The tree holds 949 files across 103 subdirectories, with 498 files lacking an extension (primarily eSpeak NG lexicons and phoneme tables). Regenerate [`assets/json/speechdata_inventory.json`](../json/speechdata_inventory.json) and [`assets/md/speechdata_manifest.md`](speechdata_manifest.md) with `python assets/py/report_speechdata_inventory.py` to keep the counts current as you migrate payloads. Those datasets need bespoke handling when we promote them into the extension-first layout or wire them into the add-on without renaming.

_Run `python - <<'PY'` scripts from this audit to regenerate the counts when you move files again so the numbers stay fresh for reviewers._

## Impact on packaging and testing
- The Python tooling under `assets/py/` still expects historical relative paths (for example `eloquence/eci.dll`, `espeak-ng-data/voices/`). Before we can ship another build we must update import paths, resource loaders, and packaging manifests (`python build.py --insecure --no-download --output dist/eloquence.nvda-addon`) so they resolve the new asset layout.
- The unit test suite (`python -m unittest discover tests`) will currently fail because resource discovery hooks and fixture paths still point at the pre-shuffle directories. We need to triage each failure, then update fixtures to reference the `assets/` layout. Capture the failure logs so CodeQL and NVDA compatibility docs can track the delta.
- Offline packaging rehearsals must continue to rely on cached datasets. When refreshing NV Access snapshots or DataJake inventories, reuse the commands documented in `AGENTS.md` so we never redownload archives unnecessarily.

## Incremental cleanup recommendations
1. **Establish loader shims.** Introduce helper functions (for example `assets/py/resource_paths.py`) that expose canonical lookups for DLLs, voices, lexicons, and Markdown docs. Update the NVDA driver modules to consume the shim instead of embedding `eloquence/` or `espeak-ng-data/` literals. This gives us a single choke point if the asset taxonomy shifts again.
2. **Track unresolved speechdata assets.** Keep [`assets/json/speechdata_inventory.json`](../json/speechdata_inventory.json) and [`assets/md/speechdata_manifest.md`](speechdata_manifest.md) up to date. The inventory enumerates every high-risk subtree (Festival, NV Speech Player, DECtalk, IBM TTS, etc.) and surfaces how many files remain extensionless. Use it to prioritise which datasets move into `assets/` next versus which should stay in place with documentation updates.
3. **Normalise testing artefacts.** Decide where test fixtures live (for example `assets/txt/tests_*` or `tests/fixtures/`). Update any pytest/unittest helpers so they read via the new shim. When fixtures cannot be renamed because NVDA expects exact filenames, document the exception directly in the manifest and README.
4. **Refresh documentation.** Keep `assets/md/README.md` aligned with the evolving structure, including notes about architecture-specific DLL lookups, NV Speech Player slider mappings, and CodeQL coverage. Reference upstream projects—eSpeak NG, RetroBunn/dt51, NV Speech Player, and NVDA—when you describe provenance so contributors understand the lineage of each asset folder.
5. **Stage deletion candidates.** Some binaries appear redundant after the move (for example historical `.pyo` caches). Verify whether they are required for backward compatibility. If not, schedule them for removal and record the rationale inside the manifest so reviewers can confirm the decision before we cut a release.

## Open questions and next steps
- **How do we package extensionless lexicons?** Investigate NVDA's expectations for eSpeak NG voice dictionaries. If we must retain the extensionless filenames, consider leaving them in `speechdata/` but surfacing the directory via the resource shim so the loader can locate them without relative path hacks.
- **What is the testing story for the rehomed binaries?** Confirm whether the existing integration scripts exercise each speech engine (Eloquence, DECtalk/FonixTalk, eSpeak NG, IBM TTS). If gaps exist, add targeted smoke tests that run under `python -m unittest discover tests` to validate DLL discovery, configuration parsing, and speech sample synthesis for every engine we ship.
- **How will we document partial migrations?** Until all payloads follow the extension-first convention, keep this audit file updated with a checklist of which frameworks have been fully normalised. Link to the manifest recommended above so contributors know where to focus.

## Suggested status tracking template
Use the table below to mark progress. Update it whenever you move assets or finish a remediation task so reviewers can scan the delta quickly.

| Framework / payload | Current location | Ready for packaging? | Notes |
| --- | --- | --- | --- |
| Eloquence runtime DLLs | `assets/dll/eloquence_*` | ⚠️ Needs loader updates | Update `eci.ini` lookups to use the resource shim before testing on NVDA alpha-52731. |
| NV Speech Player binaries | `assets/dll/nv_speech_player_*` + `speechdata/speechplayerinespeak` | ⚠️ Partially migrated | Extensionless phoneme dictionaries remain under `speechdata/`. Document loader expectations before moving. |
| eSpeak NG lexicons | `speechdata/speechplayerinespeak/espeak-ng-data` | ❌ Not migrated | Extensionless `*_dict` files must either retain their names or gain `.dict` aliases; investigate NVDA import behaviour. |
| DECtalk / FonixTalk assets | `assets/dll/_dectalk*`, `assets/py/_dectalk.py` | ⚠️ Needs verification | Confirm that DECtalk helper modules still load voice data after the move and update tests accordingly. |
| Documentation bundles | `assets/md/*.md` | ✅ Aligned | Continue refreshing snapshot reports with the documented tooling cadence so CodeQL, NVDA, and DataJake coverage stays current. |

Document future updates here as you work through the backlog so the history of the cleanup stays transparent to both maintainers and the NVDA community.

## Automation helpers

- Run `python assets/py/report_speechdata_inventory.py` after every migration batch. The helper writes both the JSON inventory (consumed by future tooling) and the Markdown summary that the NVDA community reviews when validating cached datasets.
- Extend the helper with additional metadata (`requires_exact_names`, NVDA loader ownership, CodeQL coverage) as you refactor each subtree so downstream packaging scripts can detect risky renames automatically.
