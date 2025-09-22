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
2. If you are building your own package, place the 64-bit Eloquence runtime files (for example `ECI.DLL` plus accompanying `.SYN` voice data) in an `eloquence_x64` folder before running `python build.py`. The build script copies that payload into `synthDrivers/eloquence/x64` inside the generated `.nvda-addon` so NVDA alpha builds can load it.
3. Install the add-on in NVDA 2019.3 or newer on Windows 10 or Windows 11. NVDA alpha-52705 has been verified when the 64-bit runtime is available.
4. Visit NVDA's **Preferences → Speech** dialog to select Eloquence and begin exploring customization options—including the growing set of voice and phoneme parameters we surface in the dialog.

## Phoneme customization today
- The add-on now ships with the [eSpeak NG](https://github.com/espeak-ng/espeak-ng) `phsource/phonemes` catalogue under `eloquence_data/espeak_phonemes.txt`. These definitions seed NVDA's phoneme controls without requiring a separate download.
- A new **Phoneme replacement** option appears in NVDA's voice settings dialog. Each entry lists an Eloquence phoneme (grouped by category) and several keyboard-selectable fallbacks—example words, descriptive labels, IPA symbols, or the raw engine token.
- Choose a combination with arrow keys and NVDA will announce whether it is the **current** or **default** mapping. Activating a different option immediately updates Eloquence's response when NVDA emits `PhonemeCommand` sequences, so you can tailor pronunciation on the fly without leaving the dialog.
- Custom choices are stored per phoneme, letting you review or reset mappings at any time. If you ever want to refresh the underlying catalogue with a newer upstream snapshot, replace the bundled file before rebuilding the add-on.

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
