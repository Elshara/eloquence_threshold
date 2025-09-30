# Assets layout summary

This report inventories the extension-scoped directories under ``assets/`` so NVDA packaging rehearsals and CodeQL reviews can confirm the reshuffle remains consistent. Refresh it after moving files so reviewers know which buckets still contain mismatched extensions.

* Assets root: `/workspace/eloquence_threshold/assets`
* Extension buckets: 22
* Total files scanned: 385
* Nested directories scanned: 0

| Extension | Files | Subdirectories | Mismatches | Notes |
| --- | ---: | ---: | ---: | --- |
| `bin` | 20 | 0 | 0 | All files match the directory extension. |
| `cjk` | 1 | 0 | 0 | All files match the directory extension. |
| `cmd` | 1 | 0 | 0 | All files match the directory extension. |
| `cnt` | 16 | 0 | 0 | All files match the directory extension. |
| `csv` | 1 | 0 | 0 | All files match the directory extension. |
| `dic` | 13 | 0 | 0 | All files match the directory extension. |
| `dll` | 44 | 0 | 0 | All files match the directory extension. |
| `exe` | 2 | 0 | 0 | All files match the directory extension. |
| `hlp` | 32 | 0 | 0 | All files match the directory extension. |
| `html` | 1 | 0 | 0 | All files match the directory extension. |
| `ico` | 2 | 0 | 0 | All files match the directory extension. |
| `ini` | 4 | 0 | 0 | All files match the directory extension. |
| `json` | 43 | 0 | 0 | All files match the directory extension. |
| `md` | 31 | 0 | 0 | All files match the directory extension. |
| `pdf` | 1 | 0 | 0 | All files match the directory extension. |
| `py` | 75 | 0 | 0 | All files match the directory extension. |
| `pyc` | 1 | 0 | 0 | All files match the directory extension. |
| `pyo` | 2 | 0 | 0 | All files match the directory extension. |
| `syn` | 36 | 0 | 0 | All files match the directory extension. |
| `txt` | 44 | 0 | 0 | All files match the directory extension. |
| `uil` | 13 | 0 | 0 | All files match the directory extension. |
| `voice` | 2 | 0 | 0 | All files match the directory extension. |

Run `python assets/py/report_assets_layout.py --json assets/json/assets_layout_summary.json --markdown assets/md/assets_layout_summary.md` after reorganising the tree to keep this snapshot current.
