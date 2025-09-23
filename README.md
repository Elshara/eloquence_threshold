# Eloquence Threshold for NVDA

Eloquence Threshold keeps the beloved ETI Eloquence 6.1 speech synthesizer alive for blind and low-vision users who rely on the NonVisual Desktop Access (NVDA) screen reader on Windows 10 and Windows 11. By preserving the ultra-low latency performance of this Klatt-based engine—similar to classic voices such as DECtalk—we deliver responsive speech output that remains essential for efficient navigation.

## Why this fork exists
This project builds on the long-standing community work at [pumper42nickel/eloquence_threshold](https://github.com/pumper42nickel/eloquence_threshold). NVDA's evolving add-on policies and frequent Python version shifts have created ongoing incompatibilities for legacy builds, so this fork provides a modern, continuously maintained alternative. Our goal is to keep Eloquence aligned with NVDA's latest expectations while honoring the workflow of both underground and mainstream add-on developers.

## Vision for 2026 and beyond
- Expand Eloquence beyond the historic eight preset voices so users can craft speech that reflects their preferences and cultural context.
- Offer deep phoneme customization directly inside NVDA's voice settings dialog, enabling keyboard-driven tweaks to cadence, articulation, and intonation without external tooling.
- Experiment with phoneme data from projects like [eSpeak NG](https://github.com/espeak-ng/espeak-ng) to broaden language coverage while preserving Eloquence's trademark responsiveness.
- Future-proof the synthesizer against rapid advances in AI and accessibility tech, ensuring that Windows users continue to benefit from dependable, low-latency speech.

## Staying current with NVDA
We actively follow the [NVDA source repository](https://github.com/nvaccess/nvda/) and test against stable, beta, and alpha builds. The driver now runs against NVDA alpha-52705 (`dc226976`), which finalises the jump to 64-bit Python 3.13. Contributions should call out any compatibility insights—particularly where NVDA's speech stack or win32 bindings change—so we can keep the synthesizer usable for the wider community. Regular updates will track NVDA's development cadence so that users can rely on Eloquence throughout major platform transitions.

Because NVDA 2026 builds execute as a 64-bit process, the add-on must load a 64-bit Eloquence runtime. The driver automatically discovers architecture-specific DLLs (for example, `eloquence/x64/eci.dll`) and falls back to the classic 32-bit build when appropriate. If a compatible library is missing the driver logs a clear error instead of silently failing.

## Getting started
1. Download the latest packaged add-on from the [releases page](https://github.com/pumper42nickel/eloquence_threshold/releases/latest/download/eloquence.nvda-addon), or clone this repository to build locally.
2. If you are building your own package, gather the proprietary Eloquence binaries: place the classic 32-bit runtime (for example `ECI.DLL` and the `.syn` voice data) inside an `eloquence/` directory, and optionally add a 64-bit runtime under `eloquence_x64/`. You can also reuse an earlier add-on as a template by dropping it next to the build script as `eloquence_original.nvda-addon` or by passing `--template /path/to/addon.nvda-addon` when building.
3. Run `python build.py` to produce `eloquence.nvda-addon` in the repository root. The builder now stages everything locally so offline or firewalled systems no longer block packaging. Supply `--no-download` if you do not want it to attempt downloading the legacy template, or point at a custom cache with `--template`.
4. Install the add-on in NVDA 2019.3 or newer on Windows 10 or Windows 11. NVDA alpha-52705 has been verified when the 64-bit runtime is available.
5. Visit NVDA's **Preferences → Speech** dialog to select Eloquence and begin exploring customization options—including the growing set of voice and phoneme parameters we surface in the dialog.

### Build script reference
- `python build.py --output dist/eloquence.nvda-addon` writes the package to a custom path.
- `python build.py --template path/to/legacy-addon.nvda-addon` reuses binaries from an existing package instead of copying from `./eloquence/`.
- `python build.py --no-download --insecure` prevents network access entirely; `--insecure` remains available for environments that must bypass TLS validation when downloading a template from a trusted mirror.

## Phoneme and voice customization today
- The add-on now ships with the [eSpeak NG](https://github.com/espeak-ng/espeak-ng) `phsource/phonemes` catalogue under `eloquence_data/espeak_phonemes.txt`. These definitions seed NVDA's phoneme controls without requiring a separate download.
- Use the new **Phoneme category** and **Phoneme symbol** settings in NVDA's voice dialog to focus on a single phoneme at a time. Categories mirror the groupings defined by eSpeak NG, and each symbol entry announces the phoneme name alongside its descriptive comment so you can explore the inventory from the keyboard.
- Once a symbol is selected, the **Phoneme replacement** option lists the available fallbacks—example words, descriptive labels, IPA symbols, or the raw engine token. Choose a combination with arrow keys and NVDA will announce whether it is the **current** or **default** mapping.
- Activating a different replacement immediately updates Eloquence's response when NVDA emits `PhonemeCommand` sequences, so you can tailor pronunciation on the fly without leaving the dialog. Custom choices are stored per phoneme, letting you review or reset mappings at any time.
- NVDA stores those custom mappings inside its `nvda.ini` configuration (`speech/eloquence/phonemeReplacements`), ensuring your language tweaks persist across sessions. Delete that block if you want to revert every phoneme to the bundled defaults in one go.
- If you ever want to refresh the underlying catalogue with a newer upstream snapshot, replace the bundled file before rebuilding the add-on.

### Build bespoke voices with eSpeak templates
- Voice templates derived from eSpeak NG live in `eloquence_data/espeak_voices.json`. Each template maps a language label (for example `en-US` or `es-419`) to Eloquence parameters such as pitch, head size, breathiness, and speaking rate.
- Select **Voice template** inside NVDA's Speech dialog to apply these presets. Eloquence will switch to the appropriate `.syn` voice, set its variant, and adjust sliders instantly. You can still tweak the individual sliders afterward; the template simply provides a faster starting point.
- Contributors can add more templates by editing the JSON file. The metadata documents the expected ranges for each parameter so community voices stay within Eloquence's safe operating window.

### Share language-aware pronunciation profiles
- Character-level pronunciation hints now load from `eloquence_data/languages/*.json`. Each profile records IPA transcriptions, spoken mnemonics, stress patterns, and grammatical notes for a particular locale.
- The new **Language profile** driver setting lets you follow the active voice template automatically, force a specific profile, or turn the hints off entirely. When NVDA sends IPA fallback commands, Eloquence can announce both the unmatched symbol and the language-specific hint so you understand what the command attempted to say.
- To contribute a new language or extend an existing one, drop a JSON file in the `eloquence_data/languages` folder. Profiles may list default templates so NVDA automatically activates them when users pick the matching voice.

### Supplying 64-bit Eloquence binaries
- This project cannot redistribute proprietary Eloquence libraries. Extract the 64-bit runtime from a licensed product (for example, an updated Eloquence synthesizer package) and drop the DLLs into `eloquence_x64` before packaging, or copy them directly into `synthDrivers/eloquence/x64` after installing the add-on.
- Dictionaries (`*.dic`) and voice data (`*.syn`) may stay in the legacy `synthDrivers/eloquence` directory—the driver will automatically reference them from either location.
- When distributing builds to other NVDA users, document how you sourced the binaries so that future maintainers can keep their installations in good standing.

## Roadmap highlights
- Iterative releases that surface new phoneme and voice parameters in NVDA's voice dialog.
- Research into importing phoneme rule sets from eSpeak NG to cover more languages and dialects without sacrificing speed.
- Progressive modernization of the code base to meet accessibility expectations for 2026 and beyond.

## Contributing
We welcome issues, discussions, and pull requests from screen reader users, speech enthusiasts, and developers. Please:
- Describe your NVDA build (including alpha snapshots when relevant) and Windows version when reporting bugs or sharing feedback.
- Help us validate voice and phoneme updates across diverse locales.
- Note that we rely on CodeQL for automated security and quality analysis; contributions should keep CodeQL warnings in mind.

If something feels off or you have an idea to extend Eloquence further, open an issue or start a discussion—we are growing this project together with the community.
