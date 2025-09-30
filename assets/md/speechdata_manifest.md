# Speechdata migration manifest

This snapshot inventories the extensionless assets that remain under `speechdata/` after the repository-wide extension shuffle. Regenerate it with ``python assets/py/report_speechdata_inventory.py`` whenever files move. The data complements the NVDA-focused roadmap in [`assets/md/README.md`](README.md) and helps us plan the remaining migrations without breaking cached datasets or NVDA loaders.

| Subtree | Files | Extensionless | % Extensionless | Distinct extensions |
| --- | ---: | ---: | ---: | ---: |
| `festival` | 128 | 9 | 7.0% | 15 |
| `festival/festival` | 127 | 9 | 7.1% | 14 |
| `mbrulainespeak` | 200 | 197 | 98.5% | 2 |
| `mbrulainespeak/espeak-data` | 197 | 197 | 100.0% | 0 |
| `newfon` | 38 | 0 | 0.0% | 11 |
| `newfon/bin` | 5 | 0 | 0.0% | 2 |
| `newfon/doc` | 5 | 0 | 0.0% | 3 |
| `newfon/languages` | 9 | 0 | 0.0% | 1 |
| `newfon/licenses` | 5 | 0 | 0.0% | 1 |
| `newfon/locale` | 6 | 0 | 0.0% | 3 |
| `orpheus` | 287 | 0 | 0.0% | 17 |
| `orpheus/orpheus` | 285 | 0 | 0.0% | 16 |
| `sam` | 1 | 0 | 0.0% | 1 |
| `speechplayerinespeak` | 295 | 292 | 99.0% | 2 |
| `speechplayerinespeak/espeak-ng-data` | 292 | 292 | 100.0% | 0 |

## Migration notes

- Prioritise folders with ≥80% extensionless files when designing loader shims. They are most at risk of breakage if we force renames.
- When migrating DataJake or NV Speech Player corpora, document the new asset paths in [`assets/md/README.md`](README.md) and refresh the cached provenance dashboards before packaging `eloquence.nvda-addon`.
- For each subtree, record whether NVDA expects exact filenames. If so, extend the manifest helper to emit a `requires_exact_names` flag so CodeQL and packaging scripts can warn when extensions change.
