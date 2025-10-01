Newfon NVDA add-on metadata staged under ``assets/newfon/`` centralises every
editable text resource that previously lived inside ``speechdata/newfon``.
These files describe the synthesizer, capture its upstream licensing, and keep
the translated documentation accessible for review without disturbing the
binary DLL payloads that still ship from ``speechdata/newfon``.

Contents:
- ``newfon.json`` mirrors the NVDA add-on manifest (ID, version, download URL,
  and compatibility metadata) so tooling can validate cached releases.
- ``newfon_license.txt`` and the ``licenses/`` folder record the GPL and
  derivative license notices required by upstream developers.
- ``doc/`` hosts the English and Russian README copies (both HTML and Markdown)
  along with the shared stylesheet to preserve formatting when packaging the
  add-on alongside our CodeQL-validated documentation.

When updating these resources, refresh the binary inventory with
``python assets/py/report_binary_assets.py --print`` and regenerate the
speechdata manifests so the NVDA packaging workflow tracks which assets remain
binary-only.  Keep the speech dictionaries and DLLs under ``speechdata/newfon``
until the runtime loader is updated to resolve them from the resource shim.
