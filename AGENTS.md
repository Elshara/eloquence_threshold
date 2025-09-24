# Repository Guidelines for `eloquence_threshold`

## Project identity
- This fork maintains and modernizes the ETI Eloquence 6.1 synthesizer for the NVDA screen reader on Windows 10 and Windows 11.
- Always acknowledge that the project originates from the NVDA community and aims to deliver low-latency speech comparable to classic Klatt-based synthesizers such as DECtalk and FonixTalk.
- Document the motivation for the fork when relevant: NVDA's evolving Python requirements and add-on policies necessitate an actively maintained alternative that follows alpha builds.
- Recognise that we are building a unified add-on that can surface Eloquence, eSpeak NG, DECtalk/FonixTalk, and IBM TTS heritage assets so blind users have a modern way to mix and match classic Klatt voices.

## Documentation expectations
- Use clear, welcoming language that addresses blind and low-vision users as well as contributors.
- When updating documentation, include forward-looking plans for expanding beyond the historic eight default voices and for providing customizable phoneme controls through NVDA's voice dialog.
- Reference the NVDA upstream project (https://github.com/nvaccess/nvda/) when discussing compatibility or testing expectations.
- Mention CodeQL usage whenever documenting security or quality assurance processes.
- Call out upstream resources when relevant (for example, https://github.com/espeak-ng/espeak-ng, https://github.com/RetroBunn/dt51, https://github.com/davidacm/NVDA-IBMTTS-Driver, https://github.com/nvaccess/NVSpeechPlayer, and any community-provided FonixTalk/Dectalk packages) so maintainers understand data provenance.
- When documenting the NV Access download archive, run `python tools/audit_nvaccess_downloads.py --roots releases/stable releases/2024.3 snapshots/alpha --max-depth 2 --limit-per-dir 12 --insecure --json docs/download_nvaccess_snapshot.json --markdown docs/download_nvaccess_snapshot.md` (adjust the roots as needed). Update `docs/validated_nvda_builds.json` first if a newer snapshot has been validated so severity notes stay accurate.
- Track multilingual ambitions explicitly: whenever you touch README or supporting docs, include a snapshot of current language coverage, what stages (phoneme data, language profiles, voice templates, keyboard-driven customization, and braille or dictionary exports) each locale has reached, and clearly state expansion priorities.
- Reinforce that the long-term goal is universal script coverage—explain how phoneme, sound, and symbol customization helps the synthesizer speak any code point, and outline how contributors can import new text corpora or pronunciation data to fill gaps.
- Document how generative and contextual pronunciation layers interact: note when a language profile includes automatic (AI-driven or algorithmic) phoneme generation, contextual variants for grammar or prosody, and how these map onto NVDA's phoneme picker so keyboard users understand the available levers.
- Capture build and packaging requirements for every platform you mention. When laying out supported languages, describe expected speech fluency, braille translation/export status, and any dictionary or corpus dependencies that have to ship inside release bundles.

## Contribution notes
- Encourage community participation via issues and discussions, and invite contributors to help test against current and alpha NVDA builds.
- Keep instructions actionable for both users and developers, including any planned integration with resources such as eSpeak NG or Dectalk for additional language phonemes.
- Prefer extensible data formats (JSON, structured text) that let people contribute additional voices, phonemes, or runtime assets without editing core Python unless necessary.
- Ensure new features keep keyboard-centric workflows in mind so users can customise every phoneme combination directly from NVDA's dialogs.
- Remember to resolve merge conflicts with awareness of any cached datasets or external archives that collaborators might rely on.
- When adding language data or phoneme assets, describe the provenance, enumerate dialects/variants included, and document how users can further customise pronunciations beyond legacy dictionary files.
- Whenever you introduce cross-platform guidance (for example, NVDA, Orca, Narrator, VoiceOver, TalkBack, ChromeVox), specify the packaging format, build prerequisites, and how the shared Eloquence data should flow between platforms so future maintainers can publish coordinated releases.

These guidelines apply to the entire repository.
