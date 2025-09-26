"""Helper package exposing Eloquence tooling modules to the test suite."""

# The directory previously hosted only standalone scripts. Creating a package
# keeps backwards compatibility (scripts remain executable) while letting the
# unit tests import helpers such as :mod:`tools.catalog_datajake_archives`.
