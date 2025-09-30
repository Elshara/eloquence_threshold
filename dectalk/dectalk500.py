# Future Modules:
from __future__ import annotations

# Add-on Modules:
from synthDrivers import _dectalk


class SynthDriver(_dectalk.SynthDriver):
	name = "dectalk500"
	description = _("DECTalk5.00")  # NOQA: F821
