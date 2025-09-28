# Offline packaging playbook (October 2025 refresh)

This guide walks contributors through a complete offline rebuild of
`eloquence.nvda-addon` using only the assets shipped in this repository and
the cached datasets documented under `docs/`.  It assumes no public releases
are available and mirrors the workflow we follow during quarterly ISO/script
expansion sprints.

## 1. Prepare the workspace

1. **Clone the repository**
   ```bash
   git clone https://github.com/pumper42nickel/eloquence_threshold.git
   cd eloquence_threshold
   ```
2. **Restore cached reports** – Copy (or regenerate) the Markdown/JSON pairs
   under `docs/` so every command references the same Wikipedia, DataJake,
   GitHub, and NV Access snapshots documented in the README scorecards.
   - Wikipedia taxonomy → `docs/wikipedia_language_index.md`
   - DataJake archive manifest → `docs/archive_inventory.md`
   - NVDA snapshot + severity report → `docs/download_nvaccess_snapshot.md`,
     `docs/nvda_update_recommendations.md`
   - Voice/language coverage dashboards → `docs/language_progress.md`,
     `docs/language_coverage.md`, `docs/voice_language_matrix.md`
3. **Optional virtual environment** – Create an isolated interpreter if you
   are cross-testing Windows and WSL builds:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # PowerShell: .venv\Scripts\Activate.ps1
   ```
4. **Install helper tooling** – Our build and reporting scripts rely on the
   Python standard library, but reproducible packaging benefits from the
   optional utilities captured in `tools/requirements-build.txt`:
   ```bash
   pip install -r tools/requirements-build.txt
   ```

## 2. Stage Eloquence runtime assets

The add-on loader inspects sibling directories to find architecture-specific
DLLs and accompanying `.syn` voice data while verifying PE headers:

```
eloquence_threshold/
├─ eloquence/         # classic 32-bit payload (required)
├─ eloquence_x86/     # optional override for 32-bit NVDA builds
├─ eloquence_x64/     # 64-bit binaries for modern NVDA
├─ eloquence_arm32/   # ARM32 binaries for Surface Pro X legacy builds
└─ eloquence_arm64/   # ARM64 payload for Windows on ARM nightlies
```

Place the appropriate `eci.dll`, `eci20.dll`, `.syn`, `.ph`, `.phs`, and
dictionary bundles in these folders.  The builder aborts with a descriptive
error if a DLL's architecture does not match NVDA's current process (for
example, shipping an ARM library into a 64-bit x86 package).

## 3. Sync language, phoneme, and dictionary datasets

1. **Wikipedia research dossiers** – Review
   `docs/language_research_index.md` (and the JSON companion) so any newly
   targeted ISO codes inherit the correct pronunciation sources and licensing
   notes.  Entries flagged as *Pending structured ingestion* usually require a
   follow-up conversion script before packaging.
2. **DataJake archive inventory** – Use
   `python tools/catalog_datajake_archives.py --json docs/archive_inventory.json --markdown docs/archive_inventory.md`
   to refresh metadata when adding `.dic`, `.lex`, MBROLA voices, or NV Speech
   Player captures.  The manifest records sample rate, bit depth, channel
   layout, synthesizer hints, provenance URLs, and CodeQL viability tags.
3. **GitHub mirrors** – The curated list inside
   `docs/language_research_index.json` calls out repositories with phoneme
   tables, finite-state morphology tools, and NV Speech Player exports.  Clone
   or vendor them under `eloquence_data/` as needed, then document the commit
   hash in the research index.
4. **NV Access snapshots** – When NV Access publishes a new nightly, audit the
   cached tree before updating binaries:
   ```bash
   python tools/audit_nvaccess_downloads.py --roots releases/stable releases/2024.3 snapshots/alpha \
       --max-depth 2 --limit-per-dir 12 --insecure \
       --json docs/download_nvaccess_snapshot.json \
       --markdown docs/download_nvaccess_snapshot.md
   python tools/check_nvda_updates.py --snapshot docs/download_nvaccess_snapshot.json \
       --validated docs/validated_nvda_builds.json --manifest manifest.ini \
       --markdown docs/nvda_update_recommendations.md \
       --json docs/nvda_update_recommendations.json
   python tools/report_nvaccess_tree.py --snapshot docs/download_nvaccess_snapshot.json \
       --recommendations docs/nvda_update_recommendations.json \
       --json docs/nvaccess_tree.json --markdown docs/nvaccess_tree.md
   ```
   Compare deltas with `tools/compare_nvaccess_snapshots.py` when you capture
   a newer build so the README and `AGENTS.md` can cite concrete changes.

## 4. Refresh coverage dashboards

Before packaging, regenerate the cached coverage artefacts so CodeQL and manual
reviewers can detect regressions caused by dictionary updates or new ISO
targets:

```bash
python tools/report_language_progress.py --json docs/language_progress.json --markdown docs/language_progress.md --print
python tools/report_language_coverage.py --json docs/language_coverage.json --markdown docs/language_coverage.md --print
python tools/report_voice_language_matrix.py --json docs/voice_language_matrix.json --markdown docs/voice_language_matrix.md --print
python tools/report_voice_parameters.py --json docs/voice_parameter_report.json --markdown docs/voice_parameter_report.md --print
```

The generated Markdown/JSON files power the README scorecards and provide a
baseline for CodeQL checks that validate phoneme metadata, slider coverage, and
EQ ranges across every locale.

## 5. Run quality gates

1. **Unit tests** – Execute the full suite to verify voice catalog integrity,
   phoneme inventory completeness, and documentation parsers:
   ```bash
   python -m unittest discover tests
   ```
2. **Static analysis (optional but encouraged)** – Pair the tests with CodeQL or
   `python -m compileall` before merging large dictionary imports.  CodeQL
   catches unsafe archive handling, while `compileall` surfaces syntax errors in
   seeding scripts.

## 6. Build the add-on

Produce the NVDA package directly from the repository snapshot:

```bash
python build.py --insecure --output dist/eloquence.nvda-addon
```

Additional flags:

- `--template path/to/existing-addon.nvda-addon` – reuse binaries from a
  previously published package.
- `--include-docs` – embed refreshed Markdown/JSON dashboards inside the add-on
  for offline browsing.

Inspect `dist/eloquence.nvda-addon` (a ZIP archive) to ensure it contains the
`manifest.ini`, `globalPlugins/` module, `eloquence*/` runtime folders, and any
documentation or dataset payloads you staged.

## 7. Validate in NVDA

1. Install the add-on via **Tools → Add-ons → Install** inside NVDA (alpha-52731
   or newer is our validation baseline).
2. Select **Eloquence Threshold** in **Preferences → Speech** and confirm that
   the expanded slider catalogue (Emphasis, Stress, Timbre, Tone, Pitch height,
   Vocal layers, Plosive impact, Overtones, Sibilant clarity, Subtones, Nasal
   balance, Vocal range, Inflection contour, Roughness, Smoothness, Whisper,
   Head size contour, Macro volume, Tone size, Scope depth, Sample rate, and
   per-phoneme EQ bands) loads without errors.
3. Switch between newly seeded ISO profiles and note IPA coverage percentages,
   contextual pronunciation hints, and dictionary provenance messages announced
   by the Speech dialog.

## 8. Document the run

- Update `README.md` and `AGENTS.md` with the commands you executed, the cached
  datasets you refreshed, and any new ISO/script coverage validated during the
  build.
- Record newly imported archives in `docs/archive_inventory.json` and
  `docs/archive_code_targets.md` with their provenance, priority tags, and
  sample-rate metadata so future packaging runs remain reproducible.
- Open a pull request summarising dictionary imports, slider adjustments, and
  NVDA compatibility results.  Include the test/build commands above and call
  out any CodeQL or static-analysis findings you addressed.

Following this playbook ensures every offline build leverages the cached
Wikipedia, DataJake, GitHub, and NVDA artefacts without re-downloading public
mirrors, while keeping the Eloquence Threshold roadmap aligned with CodeQL and
NVDA policy expectations.
