"""Regression test for `_pyside6_qtads_borco.pyi` typing bugs, not a `tools/generate_pyi.py` unit test.

genpyi references the stub's own classes in ways pyright can't resolve -- a
bare `import _pyside6_qtads_borco` self-import, and base classes qualified as
`pyside6_qtads_borco._pyside6_qtads_borco.ads.<Name>`. Either silently turns
the reference into `Unknown`, which then also poisons every member inherited
through those bases (e.g. `CDockManager.dockAreaCount()`, from
`CDockContainerWidget`). `fix_self_references()` in `tools/generate_pyi.py`
fixes this; this test pins the actual pyright-observed behaviour, through the
package's module-level names, so a future regeneration can't silently
reintroduce it.
"""

import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

# Matches pyright's `--outputjson` reveal_type message, e.g.
# 'Type of "dock_manager.dockAreaCount()" is "int"'.
REVEAL_TYPE_RE = re.compile(r'^Type of ".*" is "(?P<type>[^"]*)"$')

REPO_ROOT = Path(__file__).resolve().parent.parent

CHECK_SCRIPT = textwrap.dedent("""\
    import pyside6_qtads_borco as QtAds

    dock_manager = QtAds.CDockManager()
    dock_widget = QtAds.CDockWidget(dock_manager, "title")
    reveal_type(dock_manager.addDockWidget(QtAds.TopDockWidgetArea, dock_widget))
    reveal_type(dock_manager.dockAreaCount())
    reveal_type(dock_widget.dockManager())
    reveal_type(QtAds.TopDockWidgetArea)
    """)


def test_module_names_and_inherited_members_resolve_real_types(tmp_path: Path) -> None:
    """Pyright must report real types for these, never `Unknown`."""
    script = tmp_path / "check_types.py"
    script.write_text(CHECK_SCRIPT)

    result = subprocess.run(
        [sys.executable, "-m", "pyright", "--outputjson", str(script)],
        check=False,  # the JSON report is what's checked, not pyright's exit status
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    report = json.loads(result.stdout)

    resolved_types = [
        match.group("type") for d in report["generalDiagnostics"] if (match := REVEAL_TYPE_RE.match(d["message"]))
    ]

    assert resolved_types == ["CDockAreaWidget", "int", "CDockManager", "DockWidgetArea"]
