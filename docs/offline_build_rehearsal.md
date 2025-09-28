# Offline build rehearsal checklist (October 2025)

This checklist captures the full workflow for rebuilding `eloquence.nvda-addon`
without a published release.  It ties every step to cached Wikipedia, DataJake,
GitHub, and NV Access artefacts so contributors can reproduce the same
provenance trail during follow-up ISO expansion sprints.

## 1. Clone the repository and restore caches

1. Install Python 3.11+ with `venv`, Git, 7-Zip, and `cabextract` on Windows (or
   the GNU equivalents on Linux/macOS).
2. Clone the repository and initialise submodules:
   ```bash
   git clone https://github.com/<your-org>/eloquence_threshold.git
   cd eloquence_threshold
   git submodule update --init --recursive
   ```
3. Restore cached datasets into `eloquence_data/`:
   - Extract DataJake pronunciation archives listed in
     [`docs/datajake_archive_urls.txt`](docs/datajake_archive_urls.txt) and place
     their `.dic`, `.lex`, and audio captures inside the matching language
     folders.
   - Mirror GitHub pronunciation projects (for example eSpeak NG or NV Speech
     Player exports) referenced in
     [`docs/language_research_index.md`](docs/language_research_index.md) so the
     loader can hydrate contextual phoneme presets.
   - Stage NV Access installers documented by the latest
     [`docs/nvda_update_recommendations.md`](docs/nvda_update_recommendations.md)
     under `archives/nvaccess/` to keep regression tests aligned with validated
     alpha and stable builds.

## 2. Refresh reporting artefacts

The README and ISO roadmap expect cached JSON/Markdown snapshots before you
package new locales.

1. Language coverage and maturity:
   ```bash
   python tools/report_language_progress.py --json docs/language_progress.json \
       --markdown docs/language_progress.md --print
   python tools/report_language_coverage.py --json docs/language_coverage.json \
       --markdown docs/language_coverage.md --print
   python tools/report_language_maturity.py --json docs/language_maturity.json \
       --markdown docs/language_maturity.md --print
   ```
2. Voice/language linkage and parameter metadata:
   ```bash
   python tools/report_voice_language_matrix.py \
       --json docs/voice_language_matrix.json \
       --markdown docs/voice_language_matrix.md --print
   python tools/report_voice_parameters.py --json docs/voice_parameter_report.json \
       --markdown docs/voice_parameter_report.md --print
   ```
3. Asset summary dashboards for provenance tracking:
   ```bash
   python tools/summarize_language_assets.py \
       --json docs/language_asset_summary.json \
       --markdown docs/language_asset_summary.md --print
   ```

## 3. Audit NV Access snapshots

Follow the repository guidelines to keep NVDA provenance aligned with CodeQL and
release engineering expectations.

```bash
python tools/audit_nvaccess_downloads.py \
    --roots releases/stable releases/2024.3 snapshots/alpha \
    --max-depth 2 --limit-per-dir 12 --insecure \
    --json docs/download_nvaccess_snapshot.json \
    --markdown docs/download_nvaccess_snapshot.md
python tools/check_nvda_updates.py \
    --snapshot docs/download_nvaccess_snapshot.json \
    --validated docs/validated_nvda_builds.json \
    --manifest manifest.ini \
    --markdown docs/nvda_update_recommendations.md \
    --json docs/nvda_update_recommendations.json
python tools/report_nvaccess_tree.py \
    --snapshot docs/download_nvaccess_snapshot.json \
    --recommendations docs/nvda_update_recommendations.json \
    --json docs/nvaccess_tree.json \
    --markdown docs/nvaccess_tree.md
```

## 4. Run automated tests and the offline build

1. Execute the unit tests.  The suite validates voice slider ranges, phoneme
   inventories, and reporting helpers:
   ```bash
   python -m unittest discover tests
   ```
2. Build the add-on without pulling new archives so the workflow stays
   reproducible:
   ```bash
   python build.py --insecure --no-download --output dist/eloquence.nvda-addon
   ```
3. (Optional) Run your CodeQL query suite against the repository to confirm new
   dictionary ingestion helpers and NV Access tooling pass security and
   reliability checks.

## 5. Validate deliverables

1. Inspect `dist/eloquence.nvda-addon` to confirm the metadata reflects the
   current sprint (language additions, voice parameters, provenance notes).
2. Review the regenerated Markdown dashboards in `docs/` and update the README
   summary tables if new ISO scripts moved stages.
3. Update `AGENTS.md` and `docs/iso_language_expansion.md` with the sprint
   highlights so future contributors can trace the provenance chain.

## 6. Share findings

* Raise a pull request describing the ISO/script additions, datasets consumed,
  and NVDA builds exercised.  Link to the refreshed dashboards for reviewers.
* Attach unit test and build transcripts so blind/low-vision contributors can
  replay the commands without leaving the terminal.
* File issues for any missing archives, unresolved pronunciation conflicts, or
  scripts that still need braille dictionary exports so the roadmap remains
  actionable.
