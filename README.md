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
We actively follow the [NVDA source repository](https://github.com/nvaccess/nvda/) and test against stable, beta, and alpha builds. Contributions should note any compatibility insights, especially when NVDA introduces new speech requirements. Regular updates will track NVDA's development cadence so that users can rely on Eloquence throughout major platform transitions.

## Getting started
1. Download the latest packaged add-on from the [releases page](https://github.com/pumper42nickel/eloquence_threshold/releases/latest/download/eloquence.nvda-addon).
2. Install the add-on in NVDA 2019.3 or newer, including Windows 10 and Windows 11 builds.
3. Visit NVDA's **Preferences → Speech** dialog to select Eloquence and begin exploring customization options as they become available.

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
