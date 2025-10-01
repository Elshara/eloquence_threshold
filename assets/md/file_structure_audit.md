# File structure modernization audit

## Context and motivation
The current tree reflects the "assets by extension" reshuffle that moved the legacy `eloquence/`, `espeak-ng-data/`, DECtalk/FonixTalk payloads, and supporting documentation into `assets/<extension>/<descriptive_name>.<extension>` directories. The goal is to make the repository easier to reason about while we continue packaging the unified `eloquence.nvda-addon` bundle for modern [NVDA](https://github.com/nvaccess/nvda/) builds. Keeping the structure disciplined also helps CodeQL rulepacks reason about where binary payloads, Python tooling, and Markdown roadmaps live when we run the offline packaging drills captured in [`assets/md/offline_packaging_playbook.md`](offline_packaging_playbook.md).

## Inventory snapshot (2025-10-26)
- `assets/` now contains 22 extension-scoped directories. The heaviest buckets are `py` (75 files), `dll` (44 files), `txt` (44 files), `json` (43 files), and `syn` (36 files). The new [`assets/md/assets_layout_summary.md`](assets_layout_summary.md) snapshot—generated via `python assets/py/report_assets_layout.py --json assets/json/assets_layout_summary.json --markdown assets/md/assets_layout_summary.md --print`—confirms every file matches the bucket extension, keeping the convention predictable for NVDA builds and CodeQL scans.
- `speechdata/` still stages the frameworks that rely on extensionless resources. The tree holds 949 files across 103 subdirectories, with 498 files lacking an extension (primarily eSpeak NG lexicons and phoneme tables). Regenerate [`assets/json/speechdata_inventory.json`](../json/speechdata_inventory.json) and [`assets/md/speechdata_manifest.md`](speechdata_manifest.md) with `python assets/py/report_speechdata_inventory.py` to keep the counts current as you migrate payloads. Pair the manifest with the new [`assets/json/speechdata_extensionless_inventory.json`](../json/speechdata_extensionless_inventory.json) / [`assets/md/speechdata_extensionless_inventory.md`](speechdata_extensionless_inventory.md) snapshot emitted by `python assets/py/report_speechdata_extensionless.py` so NVDA packagers and CodeQL reviewers can see which files still need extensions or loader shims.

_Run `python - <<'PY'` scripts from this audit to regenerate the counts when you move files again so the numbers stay fresh for reviewers._

## Impact on packaging and testing
- Python tooling under `assets/py/` now resolves DLLs, `.syn` voices, JSON catalogues, and Markdown manifests through [`resource_paths.py`](../py/resource_paths.py). Keep extending the shim before touching loaders so partially migrated checkouts and cached NVDA add-on templates continue to work while CodeQL tracks the canonical asset locations.
- The CLI smoke tests and language catalogue unit tests have been retargeted to the extension-first layout. Run `python -m unittest discover assets/py 'test_*.py'` after updating catalogues or loader code so NVDA/CodeQL reviews capture a clean log of the reshuffled fixtures.
- Offline packaging rehearsals must continue to rely on cached datasets. When refreshing NV Access snapshots or DataJake inventories, reuse the commands documented in `AGENTS.md` so we never redownload archives unnecessarily before running `python build.py --insecure --no-download --output dist/eloquence.nvda-addon`.

## Incremental cleanup recommendations
1. **Establish loader shims.** Introduce helper functions (for example `assets/py/resource_paths.py`) that expose canonical lookups for DLLs, voices, lexicons, and Markdown docs. Update the NVDA driver modules to consume the shim instead of embedding `eloquence/` or `espeak-ng-data/` literals. This gives us a single choke point if the asset taxonomy shifts again.
2. **Track unresolved speechdata assets.** Keep [`assets/json/speechdata_inventory.json`](../json/speechdata_inventory.json), [`assets/md/speechdata_manifest.md`](speechdata_manifest.md), and [`assets/md/speechdata_extensionless_inventory.md`](speechdata_extensionless_inventory.md) up to date. The inventories enumerate every high-risk subtree (Festival, NV Speech Player, DECtalk, IBM TTS, etc.), surface how many files remain extensionless, and flag payloads that already look like WAV/OGG/ZIP/JSON so we can prioritise migrations without breaking NVDA loaders.
3. **Normalise testing artefacts.** Decide where test fixtures live (for example `assets/txt/tests_*` or `tests/fixtures/`). Update any pytest/unittest helpers so they read via the new shim. When fixtures cannot be renamed because NVDA expects exact filenames, document the exception directly in the manifest and README.
4. **Refresh documentation.** Keep `assets/md/README.md` aligned with the evolving structure, including notes about architecture-specific DLL lookups, NV Speech Player slider mappings, and CodeQL coverage. Reference upstream projects—eSpeak NG, RetroBunn/dt51, NV Speech Player, and NVDA—when you describe provenance so contributors understand the lineage of each asset folder.
5. **Stage deletion candidates.** Some binaries appear redundant after the move (for example historical `.pyo` caches). Verify whether they are required for backward compatibility. If not, schedule them for removal and record the rationale inside the manifest so reviewers can confirm the decision before we cut a release.

## Open questions and next steps
- **How do we package extensionless lexicons?** Investigate NVDA's expectations for eSpeak NG voice dictionaries. If we must retain the extensionless filenames, consider leaving them in `speechdata/` but surfacing the directory via the resource shim so the loader can locate them without relative path hacks.
- **What is the testing story for the rehomed binaries?** Confirm whether the existing integration scripts exercise each speech engine (Eloquence, DECtalk/FonixTalk, eSpeak NG, IBM TTS). If gaps exist, add targeted smoke tests that run under `python -m unittest discover assets/py 'test_*.py'` to validate DLL discovery, configuration parsing, and speech sample synthesis for every engine we ship.
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

### Progress since the last update

- **Resource path shim landed.** `assets/py/resource_paths.py` now centralises path discovery for DLLs, `.syn` voices, language profiles, phoneme catalogues, and NV Speech Player exports. The Eloquence driver, phoneme and voice catalogues, and the language profile tooling now resolve assets through this helper so the extension-first layout works without recreating the legacy `eloquence/` tree. Follow-up work: teach `build.py` to hydrate `synthDrivers/eloquence_data` from the new buckets before packaging.
- **Migration backlog published.** [`assets/md/assets_migration_backlog.md`](assets_migration_backlog.md) records every framework still straddling `assets/` and `speechdata/`, prescribes the manifest refresh cadence, and calls for the test/build sequence (`python -m unittest discover assets/py 'test_*.py'` then `python build.py --insecure --no-download --output dist/eloquence.nvda-addon`) before we ship updates for NVDA alpha-52731. Update the table after each sprint so CodeQL reviewers can trace which payloads remain in motion.
- **Build helper now hydrates the assets layout.** Running `python build.py --insecure --no-download --output dist/eloquence.nvda-addon` copies the `assets/` hierarchy (DLLs, `.syn` voices, documentation, JSON catalogues) directly into the staging area, falls back to legacy `eloquence_data/` when present, and warns when `eci.dll` is missing from `assets/dll`. This keeps the NVDA packaging drill and downstream CodeQL scanning aligned with the new structure while we continue migrating extensionless datasets out of `speechdata/`.
- **Build helper now uses the resource shim for discovery.** `assets/py/build.py` imports `resource_paths` to resolve the canonical `assets/` and `speechdata/` directories, then reuses the Eloquence runtime search list when warning about missing `eci.dll`. This keeps the packaging workflow in sync with the runtime loader while we test `python build.py --no-download --insecure --output dist/eloquence.nvda-addon` against NVDA alpha builds and CodeQL policies.
- **Speechdata inventory stabilised.** `python assets/py/report_speechdata_inventory.py` now emits deterministically sorted JSON and Markdown so review diffs stay readable. Regenerate the artefacts after every migration batch—the helper now lists `festival`, `mbrulainespeak`, `newfon`, `orpheus`, `sam`, and `speechplayerinespeak` in alphabetical order, matching the Markdown manifest consumers rely on for NVDA and CodeQL cross-checks.
- **Extensionless audit published.** `python assets/py/report_speechdata_extensionless.py` inventories every suffix-less file under `speechdata/`, classifies obvious WAV/OGG/ZIP/MIDI payloads, and recommends extensions when we can add them safely. Refresh [`assets/json/speechdata_extensionless_inventory.json`](../json/speechdata_extensionless_inventory.json) and [`assets/md/speechdata_extensionless_inventory.md`](speechdata_extensionless_inventory.md) before each NVDA or CodeQL rehearsal so reviewers can see which assets still need manual cleanup.
- **Assets layout reporter added.** `python assets/py/report_assets_layout.py` captures the new extension-first structure in machine- and human-readable summaries. Refresh [`assets/json/assets_layout_summary.json`](../json/assets_layout_summary.json) and [`assets/md/assets_layout_summary.md`](assets_layout_summary.md) after moving files so packaging rehearsals and CodeQL rulepacks can validate that DLLs, scripts, and documentation continue to live under matching buckets.
- **CLI smoke tests retargeted.** The unit tests that exercise `python assets/py/report_*` and `python assets/py/run_nvda_release_checks.py` now invoke the tools from the `assets/py` bucket, preload the bucket on `PYTHONPATH`, and consume cached artefacts from `assets/json/` and `assets/ini/manifest.ini`. This keeps the NVDA release-audit workflow passing under the new layout while CodeQL retains visibility into the commands we expect builders to run offline.
- **Root build wrapper now seeds PYTHONPATH.** Calling `python build.py` from the repository root now injects `assets/py/` onto `sys.path` before forwarding execution to the real helper. This guarantees Python 3.13+ environments can resolve `resource_paths` without manual `PYTHONPATH` edits when we package 32-bit and 64-bit builds for NVDA alpha snapshots.
- **Build execution tracing shipped.** `python build.py --trace-json assets/json/build_execution_trace.json --trace-markdown assets/md/build_execution_trace.md --no-download --insecure --output dist/test.nvda-addon` now emits machine- and contributor-friendly reports that track which helpers fired, how many optional directories were copied, and where follow-up NVDA/CodeQL validation remains. The Markdown report feeds directly into reviewer discussions while the JSON log can seed future automation that enforces coverage of the packaging pipeline.

### Packaging execution map (2025-10-26)

Running `python build.py --no-download --insecure --output dist/test.nvda-addon` exercises a specific slice of the packaging pipeline. Track which helpers fired so we can target refactors and Python 3.13 compatibility work:

| Helper | Triggered? | Notes |
| --- | --- | --- |
| `parse_args()` | ✅ | Captured the explicit `--no-download`/`--insecure`/`--output` options for the offline rehearsal. |
| `_validate_template_url()` | ✅ | Checked the default GitHub release URL even though downloads were disabled, confirming the allow-list logic stays Python 3.13-safe. |
| `ensure_template()` | ✅ | Confirmed the `eloquence_original.nvda-addon` template is absent and respected the "no download" flag so the build stayed air-gapped. |
| `stage_template()` | ✅ | Initialised `synthDrivers/` with an empty layout because no template archive was supplied. |
| `stage_root_files()` | ✅ | Copied `assets/ini/manifest.ini` into the staging directory for NVDA alpha compatibility. |
| `stage_synth_driver_modules()` | ✅ | Staged the Eloquence driver modules (Python 3.13-friendly) and generated `synthDrivers/__init__.py` so NVDA treats the folder as a package. |
| `stage_assets_tree()` | ✅ | Mirrored the entire `assets/` hierarchy into the add-on, ensuring DLL, `.syn`, JSON, Markdown, and tooling buckets remain shallow and extension-aligned. |
| `stage_speechdata_tree()` | ✅ | Bundled the temporary `speechdata/` folder so extensionless dictionaries continue working while we refactor them. |
| `copy_optional_directory()` | ⚠️ | Helper executed for `eloquence_data/` and architecture-specific folders but skipped copying because those caches are absent in this checkout. Keep testing on machines that stage x86/x64 payloads. Refer to [`assets/md/build_execution_trace.md`](build_execution_trace.md) for the full event log. |
| `has_runtime_assets()` | ✅ | Detected `eci.dll` inside the `assets/dll` bucket, preventing the fallback warning and confirming the runtime discovery shim works without legacy folders. |
| `write_archive()` | ✅ | Produced `dist/test.nvda-addon` with ZIP_DEFLATED compression ready for NVDA alpha installation. |

Helpers **not** triggered in this offline drill—`ensure_template()`'s download branch, architecture-specific `copy_optional_directory()` copies, and the legacy `eloquence_data` staging—remain queued for validation once we attach cached NVDA runtimes or rehearse with historical add-on templates. Document the next run when those branches execute so we can confirm 32-bit/64-bit parity before NVDA alpha sign-off.

### Current remediation queue (update 2025-10-26)

- [ ] Update the Eloquence driver and helper scripts to read DLL, `.syn`, and configuration assets exclusively through `resource_paths`, then validate on NVDA alpha-52731. *(Packaging helper updated; runtime modules still pending end-to-end verification.)*
- [ ] Port NV Speech Player phoneme and language dictionaries out of `speechdata/` or document loader exceptions when extensions cannot change.
- [ ] Split the remaining multi-purpose Python utilities into single-purpose modules (for example, separate CLI entry points from data transforms) so the `assets/py` folder mirrors the "one function per file" goal.
- [ ] Decide on a permanent home for test fixtures (`tests/fixtures/` vs. `assets/txt/tests_*`) and wire them into `python -m unittest discover assets/py 'test_*.py'` once the loader shims settle.
- [ ] Review `.pyo` and other historical cache files; if they no longer serve NVDA or CodeQL workflows, stage them for deletion and record the rationale here before removing them from the tree.
- [ ] Use [`assets/md/speechdata_extensionless_inventory.md`](speechdata_extensionless_inventory.md) to plan extension or loader updates for the 225 `binary/unknown` files—primarily eSpeak NG dictionaries—so NVDA can keep loading them even if we adopt suffixes or shims.

## Automation helpers

- Run `python assets/py/report_speechdata_inventory.py` after every migration batch. The helper writes both the JSON inventory (consumed by future tooling) and the Markdown summary that the NVDA community reviews when validating cached datasets.
- Extend the helper with additional metadata (`requires_exact_names`, NVDA loader ownership, CodeQL coverage) as you refactor each subtree so downstream packaging scripts can detect risky renames automatically.
- Pair the add-on build with `python build.py --no-download --insecure --trace-json assets/json/build_execution_trace.json --trace-markdown assets/md/build_execution_trace.md --output dist/test.nvda-addon` so reviewers can diff helper coverage across runs and plan NVDA/CodeQL follow-ups when branches of the packaging pipeline stay idle.
