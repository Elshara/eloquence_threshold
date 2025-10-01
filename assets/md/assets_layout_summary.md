# Assets layout summary

This report inventories the extension-scoped directories under ``assets/`` so NVDA packaging rehearsals and CodeQL reviews can confirm the reshuffle remains consistent. Refresh it after moving files so reviewers know which buckets still contain mismatched extensions.

* Assets root: `/workspace/eloquence_threshold/assets`
* Extension buckets: 15
* Total files scanned: 288
* Nested directories scanned: 4

| Extension | Files | Subdirectories | Mismatches | Notes |
| --- | ---: | ---: | ---: | --- |
| `cjk` | 1 | 0 | 0 | All files match the directory extension. |
| `cmd` | 1 | 0 | 0 | All files match the directory extension. |
| `cnt` | 16 | 0 | 0 | All files match the directory extension. |
| `csv` | 1 | 0 | 0 | All files match the directory extension. |
| `dic` | 13 | 0 | 0 | All files match the directory extension. |
| `hlp` | 32 | 0 | 0 | All files match the directory extension. |
| `html` | 1 | 0 | 0 | All files match the directory extension. |
| `ini` | 4 | 0 | 0 | All files match the directory extension. |
| `json` | 46 | 0 | 0 | All files match the directory extension. |
| `md` | 36 | 0 | 0 | All files match the directory extension. |
| `newfon` | 13 | 4 | 13 | 13 file(s) with unexpected suffixes: `README.txt`, `doc/en/readme.html`, `doc/en/readme.md`, `doc/ru/readme.html`, `doc/ru/readme.md`, `doc/style.css`, `licenses/GNU GENERAL PUBLIC LICENSE.txt`, `licenses/NewfonScriptsLicense.txt`, `licenses/libsamplerate_license.txt`, `licenses/newfon_license_en.txt`, `licenses/newfon_license_ru.txt`, `newfon.json`, … |
| `pdf` | 1 | 0 | 0 | All files match the directory extension. |
| `py` | 77 | 0 | 0 | All files match the directory extension. |
| `txt` | 44 | 0 | 0 | All files match the directory extension. |
| `voice` | 2 | 0 | 0 | All files match the directory extension. |

Run `python assets/py/report_assets_layout.py --json assets/json/assets_layout_summary.json --markdown assets/md/assets_layout_summary.md` after reorganising the tree to keep this snapshot current.
