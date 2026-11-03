"""Everything PyPI ``pyside6-qtads`` exposes must exist here too, in the same shape.

Compares this package's API against the snapshot in
``tests/data/pyside6_qtads_api.json`` (``tools/dump_api.py`` explains how it's
made and what it records): module-level names, ``ads`` classes with their
bases, own members and overload signatures, signals, and enum members.

A deliberate difference goes in ``DEVIATIONS``, keyed by the difference as
``differences()`` reports it, with the reason and the link to the upstream
PR/issue proposing our behaviour (docs/compatibility.md has the details). An
unrecorded difference fails, and so does an entry that's no longer a
difference.
"""

import importlib.util
import json
from pathlib import Path
from typing import Any, Final

REPO_ROOT: Final = Path(__file__).resolve().parent.parent
SNAPSHOT: Final = REPO_ROOT / "tests" / "data" / "pyside6_qtads_api.json"

DEVIATIONS: Final[dict[str, str]] = {
    "ads.CFloatingDockContainer.waylandMoveOrLeaveInWindowPreview: missing (Preview: ads.CFloatingDragPreview, "
    "SourceWindow: PySide6.QtWidgets.QWidget, GlobalPos: PySide6.QtCore.QPoint, /) -> bool": (
        "QtAds itself added a required `Floatable` argument after 5.1.1 "
        "(https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System/pull/873); "
        "pyside6-qtads gets the same signature once it moves past 5.1.1"
    ),
}


def __load_dump_api() -> Any:
    """Import tools/dump_api.py, which isn't part of the package."""
    spec = importlib.util.spec_from_file_location("dump_api", REPO_ROOT / "tools" / "dump_api.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def __missing(where: str, theirs: list[str], ours: list[str]) -> list[str]:
    return [f"{where}: missing {name}" for name in theirs if name not in ours]


def differences(theirs: dict[str, Any], ours: dict[str, Any]) -> list[str]:
    """List what ``theirs`` has that ``ours`` lacks or has in a different shape."""
    found = __missing("module", theirs["module"], ours["module"])
    found += __missing("ads enums", list(theirs["ads"]["enums"]), list(ours["ads"]["enums"]))
    for name, members in theirs["ads"]["enums"].items():
        found += __missing(f"ads.{name}", members, ours["ads"]["enums"].get(name, []))
    for name, cls in theirs["ads"]["classes"].items():
        our_cls = ours["ads"]["classes"].get(name)
        if our_cls is None:
            found.append(f"ads: missing class {name}")
            continue
        where = f"ads.{name}"
        if cls["bases"] != our_cls["bases"]:
            found.append(f"{where}: bases {cls['bases']} != {our_cls['bases']}")
        found += __missing(where, list(cls["members"]), list(our_cls["members"]))
        for member, overloads in cls["members"].items():
            our_overloads = our_cls["members"].get(member)
            if our_overloads is not None:
                found += __missing(f"{where}.{member}", overloads, our_overloads)
        found += __missing(f"{where} signals", cls["signals"], our_cls["signals"])
        found += __missing(f"{where} enums", list(cls["enums"]), list(our_cls["enums"]))
        for enum_name, members in cls["enums"].items():
            found += __missing(f"{where}.{enum_name}", members, our_cls["enums"].get(enum_name, []))
    return found


def test_api_is_a_superset_of_pyside6_qtads() -> None:
    theirs = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    ours = __load_dump_api().api_surface("pyside6_qtads_borco")
    found = differences(theirs, ours)

    unrecorded = [difference for difference in found if difference not in DEVIATIONS]
    stale = [difference for difference in DEVIATIONS if difference not in found]
    assert not unrecorded, "differences from pyside6-qtads not recorded in DEVIATIONS:\n" + "\n".join(unrecorded)
    assert not stale, "DEVIATIONS entries that are no longer differences:\n" + "\n".join(stale)
