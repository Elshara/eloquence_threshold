# Equalizer APO alignment notes

Equalizer APO is a system-level audio processing suite for Windows that injects
Audio Processing Objects (APOs) into the Core Audio pipeline. Its source code
and documentation outline several implementation details that inform how we
extend Eloquence Threshold's phoneme EQ and sample-rate controls:

## APO registration and device binding
- Equalizer APO registers custom system effects (s-APOs) under the `HKLM\\SYSTEM`
  registry hive and associates them with device interface GUIDs. This approach
  ensures every playback endpoint can maintain its own configuration.
- Eloquence Threshold already queries the active device GUID when sampling
  WASAPI rates. Mirroring Equalizer APO's binding strategy will let us persist
  phoneme EQ curves, macro volume envelopes, or capture/post-mix tweaks per
  endpoint inside NVDA's configuration without guessing which device is active.

## Filter topology inspiration
- Equalizer APO's configuration grammar exposes shelving, peaking, and custom
  convolution filters that can be stacked per channel.
- Our `voice_parameters.py` metadata now mirrors that flexibility by declaring
  multi-band profiles (dual, triple, and shelf-wide) so NV Speech Player-style
  sliders can sculpt both low and high regions simultaneously.
- Studying Equalizer APO's filter blocks helps us keep the phoneme manager's
  1 Hz–384 kHz / ±24 dB limits aligned with what Windows' APO runtime expects,
  giving us confidence that future pre- or post-mix hooks will remain stable.

## Sample-rate awareness
- Equalizer APO inspects each device's mix format before applying filters so it
  can design coefficients that match the current sample rate.
- `_eloquence.py` now follows the same pattern, retrieving the active endpoint's
  rate via WASAPI and clamping it to Eloquence's supported 8 kHz–384 kHz window
  before feeding the resampler. The new `macroVolume` and `inflectionContour`
  sliders piggyback on that query so large EQ boosts never overrun the mixer's
  headroom.

## Future integration ideas
- Equalizer APO offers separate pre-mix, post-mix, and capture pipelines. If
  NVDA exposes those hooks in the future we can translate phoneme EQ presets
  into APO configuration fragments, letting users share one set of controls
  between Eloquence and system-wide processing.
- The project also demonstrates how to expose configuration via text files and
  live reload them. Pairing this model with NVDA's voice dialog could unlock
  advanced workflows where phoneme EQ edits are synchronised with Equalizer
  APO's engine for critical listening sessions.

## Import tooling
- `tools/import_eq_apo_config.py` parses Equalizer APO preset files and emits
  JSON/Markdown summaries that document device metadata, loudness correction
  states, and every peaking filter we can map onto Eloquence's phoneme EQ bands.
- The helper approximates each peaking filter's bandwidth using its centre
  frequency and Q factor, keeping the derived low/high bounds inside the
  synthesizer's 1 Hz–384 kHz envelope (or the supplied sample-rate hint's
  Nyquist limit). The resulting data can seed NVDA's per-phoneme editor so
  advanced APO workflows remain accessible without editing the Windows registry.
