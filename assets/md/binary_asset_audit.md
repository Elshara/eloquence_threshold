# Binary asset audit

## Why binaries now live in `speechdata/`
The 2025-10 restructure moves every proprietary runtime and opaque dataset out of the extension-first `assets/` tree. Staging DLLs, executables, icons, and compiled caches under `speechdata/` makes it clear that these payloads must be regenerated or replaced before publishing an NVDA add-on. Tooling inside [`assets/py/resource_paths.py`](../py/resource_paths.py) now resolves each engine’s binaries from the new locations so NVDA alpha builds, CodeQL scans, and offline packaging rehearsals stay reproducible without keeping vendor blobs in the Python source tree. Refresh the per-file inventory with `python assets/py/report_binary_assets.py --json assets/json/binary_asset_index.json --markdown assets/md/binary_asset_index.md --print` whenever the tree changes so this audit can link to the latest counts.

## Inventory by engine
| Engine / payload | Directory | Binary types | Runtime status | Follow-up work |
| --- | --- | --- | --- | --- |
| Eloquence core runtime | `speechdata/eloquence/dll/` | `ECI*.DLL`, `TI*.DLL`, locale ROM shims (`chsrom.dll`, `jpnrom.dll`, `korrom.dll`), SAPI bridges | Loaded by [`assets/py/Eloquence.py`](../py/Eloquence.py) via `resource_paths`. | Capture per-architecture checksums before bundling redistributable builds in NVDA alpha-52731 rehearsals. |
| Eloquence voices | `speechdata/eloquence/syn/` | `.SYN` voice archives | Staged into packaged add-ons by `build.py`. | Document provenance for each voice before future redistribution. |
| Eloquence UI & tooling | `speechdata/eloquence/uil/`, `speechdata/eloquence/exe/`, `speechdata/eloquence/ico/` | UI resource DLLs, legacy demos (`eloqtalk.exe`), icons | Not exercised by NVDA runtime; retained for archival research. | Determine whether UI resource DLLs are needed for compatibility with legacy installers. |
| NV Speech Player | `speechdata/nv_speech_player/dll/` | `speechPlayer.dll`, `old_speechPlayer.dll`, `SMPRenderer.dll` | Loaded by `speechPlayer.py`, `old_speechPlayer.py`, and `smpsoft.py`. | Align DLL provenance with cached NV Speech Player releases before distributing binaries. |
| SVOX Pico | `speechdata/pico/dll/`, `speechdata/pico/svox-pico-data/` | `svox-pico.dll`, `.bin` voice data | Loaded by `pico.py`. | Validate voice data against current NVDA alpha sample-rate expectations; document licensing for each language pack. |
| DECtalk / FonixTalk | `speechdata/dectalk/dll/`, `speechdata/fonixtalk/dll/` | `dectalk*.dll`, `dtalk_*.dll` | Loaded by `_dectalk.py` and `_fonixtalk.py`. | Record DataJake provenance for each DLL and confirm per-locale voice availability. |
| BestSpeech | `speechdata/bestspeech/dll/` | `B32_TTS.DLL`, `b32_wrapper.dll` | Loaded by `bestspeech.py`. | Audit whether wrapper DLLs require 32-bit compatibility notes for NVDA alpha packaging. |
| Brailab | `speechdata/brailab/dll/`, `speechdata/brailab/compiled/` | `TTS.dll`, legacy `.pyo` cache | Loaded by `brailab.py`; compiled artefacts retained for reverse-engineering. | Replace `.pyo` cache with documented source once compatibility testing completes. |
| Captain | `speechdata/captain/dll/` | `captain.dll` | Loaded by `captain.py`. | Confirm audio format expectations for NVDA 32-bit vs. 64-bit targets. |
| Gregor | `speechdata/gregor/dll/`, `speechdata/gregor/compiled/` | `libsyntgregor.dll`, legacy `.pyc`/`.pyo` cache | Loaded by `gregor.py`. | Rebuild the compiled cache from source to confirm Python 3.13 compatibility. |
| Legacy / unclassified archives | `speechdata/legacy/bin/` | Historical `.bin` voice data (e.g., `BINADATA.BIN`, `adrlong.bin`) | Not used by current loaders. | Identify the originating engine before promoting into an engine-specific bucket or regenerating replacements. |

## Outstanding actions
- Update the modernization audit with per-engine checksum guidance once NVDA alpha-52731 validation runs complete.
- Expand the CodeQL policy so binaries staged in `speechdata/` are automatically flagged when missing provenance notes.
- Continue moving extensionless datasets into typed buckets (for example, Pico dictionaries) so future packaging runs can verify licences before shipping binaries.
