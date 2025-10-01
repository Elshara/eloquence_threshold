# Speechdata migration manifest

This snapshot inventories the extensionless assets that remain under `speechdata/` after the repository-wide extension shuffle. Regenerate it with ``python assets/py/report_speechdata_inventory.py`` whenever files move. The data complements the NVDA-focused roadmap in [`assets/md/README.md`](README.md) and helps us plan the remaining migrations without breaking cached datasets or NVDA loaders.

| Subtree | Files | Extensionless | % Extensionless | Distinct extensions |
| --- | ---: | ---: | ---: | ---: |
| `bestspeech` | 2 | 0 | 0.0% | 1 |
| `bestspeech/dll` | 2 | 0 | 0.0% | 1 |
| `brailab` | 2 | 0 | 0.0% | 2 |
| `brailab/compiled` | 1 | 0 | 0.0% | 1 |
| `brailab/dll` | 1 | 0 | 0.0% | 1 |
| `captain` | 1 | 0 | 0.0% | 1 |
| `captain/dll` | 1 | 0 | 0.0% | 1 |
| `dectalk` | 18 | 0 | 0.0% | 1 |
| `dectalk/dll` | 18 | 0 | 0.0% | 1 |
| `eloquence` | 70 | 0 | 0.0% | 5 |
| `eloquence/dll` | 17 | 0 | 0.0% | 1 |
| `eloquence/exe` | 2 | 0 | 0.0% | 1 |
| `eloquence/ico` | 2 | 0 | 0.0% | 1 |
| `eloquence/syn` | 36 | 0 | 0.0% | 1 |
| `eloquence/uil` | 13 | 0 | 0.0% | 1 |
| `festival` | 128 | 9 | 7.0% | 15 |
| `festival/festival` | 127 | 9 | 7.1% | 14 |
| `gregor` | 3 | 0 | 0.0% | 3 |
| `gregor/compiled` | 2 | 0 | 0.0% | 2 |
| `gregor/dll` | 1 | 0 | 0.0% | 1 |
| `legacy` | 8 | 0 | 0.0% | 1 |
| `legacy/bin` | 8 | 0 | 0.0% | 1 |
| `mbrulainespeak` | 200 | 197 | 98.5% | 2 |
| `mbrulainespeak/espeak-data` | 197 | 197 | 100.0% | 0 |
| `newfon` | 26 | 0 | 0.0% | 6 |
| `newfon/bin` | 5 | 0 | 0.0% | 2 |
| `newfon/languages` | 9 | 0 | 0.0% | 1 |
| `newfon/locale` | 6 | 0 | 0.0% | 3 |
| `nv_speech_player` | 3 | 0 | 0.0% | 1 |
| `nv_speech_player/dll` | 3 | 0 | 0.0% | 1 |
| `orpheus` | 287 | 0 | 0.0% | 17 |
| `orpheus/orpheus` | 285 | 0 | 0.0% | 16 |
| `pico` | 13 | 0 | 0.0% | 2 |
| `pico/dll` | 1 | 0 | 0.0% | 1 |
| `pico/svox-pico-data` | 12 | 0 | 0.0% | 1 |
| `sam` | 1 | 0 | 0.0% | 1 |
| `speechplayerinespeak` | 295 | 292 | 99.0% | 2 |
| `speechplayerinespeak/espeak-ng-data` | 292 | 292 | 100.0% | 0 |

## Migration notes

- Prioritise folders with ≥80% extensionless files when designing loader shims. They are most at risk of breakage if we force renames.
- When migrating DataJake or NV Speech Player corpora, document the new asset paths in [`assets/md/README.md`](README.md) and refresh the cached provenance dashboards before packaging `eloquence.nvda-addon`.
- For each subtree, record whether NVDA expects exact filenames. If so, extend the manifest helper to emit a `requires_exact_names` flag so CodeQL and packaging scripts can warn when extensions change.
