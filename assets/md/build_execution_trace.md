# Build helper execution trace

The table below captures which packaging helpers executed during the most recent
`python build.py` invocation. Use it alongside the file-structure audit to plan
follow-up refactors and CodeQL-reviewed NVDA packaging drills.

## Invocation context
- **Assets Copied**: True
- **Copied Architectures**: []
- **Legacy Data Copied**: False
- **Legacy Runtime Copied**: False
- **Output**: dist/test.nvda-addon
- **Speechdata Copied**: True
- **Template**: None
- **Template Used**: False

## Helper coverage

| Helper | Triggered? | Calls | Notes |
| --- | --- | --- | --- |
| `parse_args` | ✅ | 1 | output=dist/test.nvda-addon, template=eloquence_original.nvda-addon, no_download=True, insecure=True, template_url=https://github.com/pumper42nickel/eloquence_threshold/releases/download/v0.20210417.01/eloquence.nvda-addon |
| `_validate_template_url` | ✅ | 1 | template_url=https://github.com/pumper42nickel/eloquence_threshold/releases/download/v0.20210417.01/eloquence.nvda-addon |
| `ensure_template` | ✅ | 1 | path=eloquence_original.nvda-addon, result=missing, allow_download=False |
| `stage_template` | ✅ | 1 | template=None, result=initialised |
| `stage_root_files` | ✅ | 1 | files_copied=1 |
| `stage_synth_driver_modules` | ✅ | 1 | modules_copied=8 |
| `stage_assets_tree` | ✅ | 1 | copied=True, entries=13 |
| `stage_speechdata_tree` | ✅ | 1 | copied=True |
| `copy_optional_directory` | ✅ | 21 | source=assets/cjk, destination=<temp>/eloquence_build/<run>/assets/cjk, copied=True, preserve_existing=False<br>source=assets/cmd, destination=<temp>/eloquence_build/<run>/assets/cmd, copied=True, preserve_existing=False<br>source=assets/cnt, destination=<temp>/eloquence_build/<run>/assets/cnt, copied=True, preserve_existing=False<br>source=assets/csv, destination=<temp>/eloquence_build/<run>/assets/csv, copied=True, preserve_existing=False<br>source=assets/dic, destination=<temp>/eloquence_build/<run>/assets/dic, copied=True, preserve_existing=False<br>source=assets/hlp, destination=<temp>/eloquence_build/<run>/assets/hlp, copied=True, preserve_existing=False<br>source=assets/html, destination=<temp>/eloquence_build/<run>/assets/html, copied=True, preserve_existing=False<br>source=assets/ini, destination=<temp>/eloquence_build/<run>/assets/ini, copied=True, preserve_existing=False<br>source=assets/json, destination=<temp>/eloquence_build/<run>/assets/json, copied=True, preserve_existing=False<br>source=assets/md, destination=<temp>/eloquence_build/<run>/assets/md, copied=True, preserve_existing=False<br>source=assets/pdf, destination=<temp>/eloquence_build/<run>/assets/pdf, copied=True, preserve_existing=False<br>source=assets/txt, destination=<temp>/eloquence_build/<run>/assets/txt, copied=True, preserve_existing=False<br>source=assets/voice, destination=<temp>/eloquence_build/<run>/assets/voice, copied=True, preserve_existing=False<br>source=speechdata, destination=<temp>/eloquence_build/<run>/speechdata, copied=True, preserve_existing=False<br>source=eloquence_data, destination=<temp>/eloquence_build/<run>/synthDrivers/eloquence_data, copied=False, reason=missing_source<br>source=eloquence, destination=<temp>/eloquence_build/<run>/synthDrivers/eloquence, copied=False, reason=missing_source<br>source=eloquence_x86, destination=<temp>/eloquence_build/<run>/synthDrivers/eloquence/x86, copied=False, reason=missing_source<br>source=eloquence_x64, destination=<temp>/eloquence_build/<run>/synthDrivers/eloquence/x64, copied=False, reason=missing_source<br>source=eloquence_arm32, destination=<temp>/eloquence_build/<run>/synthDrivers/eloquence/arm32, copied=False, reason=missing_source<br>source=eloquence_arm64, destination=<temp>/eloquence_build/<run>/synthDrivers/eloquence/arm64, copied=False, reason=missing_source<br>source=eloquence_arm, destination=<temp>/eloquence_build/<run>/synthDrivers/eloquence/arm, copied=False, reason=missing_source |
| `has_runtime_assets` | ✅ | 1 | found=True |
| `write_archive` | ✅ | 1 | output=dist/test.nvda-addon, files_packaged=1277 |
