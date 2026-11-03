"""Regenerate `src/pyside6_qtads_borco/_pyside6_qtads_borco.pyi`.

`shiboken6-genpyi` generates a `.pyi` stub for `_pyside6_qtads_borco`, giving
pyright/Pylance full signatures and autocomplete for the `ads` namespace.
Running it directly on the built extension fails for two reasons that don't
affect PySide6's own `pyside6-genpyi`:

1. genpyi re-imports the extension from a bare path, bypassing
   `pyside6_qtads_borco/__init__.py`'s `import PySide6.QtWidgets` DLL-path
   setup -- without that import happening first, the bare re-import fails
   with "DLL load failed".
2. genpyi's `find_imports()` references a `PySide6` global that only
   `PySide6.support.generate_pyi` sets up (via `global PySide6; import
   PySide6`) before calling it. The generic `shiboken6-genpyi` entry point
   never sets it, so it raises `NameError: name 'PySide6' is not defined`.

After generation, `fix_self_references()` drops genpyi's
`pyside6_qtads_borco._pyside6_qtads_borco.` qualifier from the stub's
references to its own classes (e.g. base classes), which pyright can't
resolve through the stub's bare self-import.

Run after rebuilding the extension (`make install` or `uv sync
--reinstall-package pyside6-qtads-borco`), whenever `bindings.xml`/
`bindings.h` change the public API surface.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Final

REPO_ROOT: Final = Path(__file__).resolve().parent.parent
PACKAGE_DIR: Final = REPO_ROOT / "src" / "pyside6_qtads_borco"
PYI_PATH: Final = PACKAGE_DIR / "_pyside6_qtads_borco.pyi"

# The extension's own dotted module path, which genpyi uses to qualify
# references to its classes (e.g. base classes) -- see fix_self_references().
SELF_MODULE_QUALIFIER: Final = "pyside6_qtads_borco._pyside6_qtads_borco."


def fix_self_references(text: str) -> str:
    """Make the stub's references to its own classes resolvable for pyright.

    genpyi qualifies them with the extension's dotted module path (e.g.
    `class CDockManager(pyside6_qtads_borco._pyside6_qtads_borco.ads.CDockContainerWidget)`),
    while its self-import is a bare `import _pyside6_qtads_borco` -- neither
    of which pyright can resolve. An unresolved name silently becomes
    `Unknown`, and an unresolved base class makes every inherited member
    `Unknown` too. The classes are defined in this same stub, so the
    qualifier and the self-import are simply dropped.
    """
    text = text.replace("import _pyside6_qtads_borco\n", "", 1)
    return text.replace(SELF_MODULE_QUALIFIER, "")


def run_genpyi() -> None:
    """Run shiboken6-genpyi against the built extension, with the PySide6 workarounds applied."""
    import PySide6
    import shiboken6  # noqa: F401 -- side effect: makes `shibokensupport` importable
    from shibokensupport.signature.lib import pyi_generator

    import pyside6_qtads_borco._pyside6_qtads_borco as extension  # workaround 1, see module docstring

    pyi_generator.PySide6 = PySide6  # workaround 2, see module docstring
    sys.argv = ["shiboken6-genpyi", extension.__file__, "--outpath", str(PACKAGE_DIR)]
    pyi_generator.main()


def main() -> None:
    """Generate `_pyside6_qtads_borco.pyi`, then post-process it in place."""
    run_genpyi()
    text = PYI_PATH.read_text(encoding="utf-8")
    text = fix_self_references(text)
    PYI_PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
