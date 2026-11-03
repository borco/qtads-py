"""Dump the public API of a QtAds binding module as JSON, for tests/test_api_superset.py.

The snapshot of PyPI ``pyside6-qtads`` (``tests/data/pyside6_qtads_api.json``)
is made in a throwaway environment, since every ``pyside6-qtads`` release pins
an exact PySide6 that needn't be ours::

    uv run --isolated --no-project --with pyside6-qtads==5.1.1.1 \\
        python tools/dump_api.py PySide6QtAds pyside6-qtads tests/data/pyside6_qtads_api.json

``tests/test_api_superset.py`` calls ``api_surface()`` on this package and
checks that it contains everything in the snapshot. Only what QtAds itself
adds is recorded -- module-level names, each ``ads`` class's own members
(not those inherited from Qt) with their overloads' signatures, its signals
from its own meta-object, and enum members -- so a different PySide6
version on either side doesn't show up as a difference.
"""

from __future__ import annotations

import enum
import importlib
import importlib.metadata
import json
import re
import sys
import types
from pathlib import Path
from typing import Any

# The qualified names each binding's extension module uses in signatures.
MODULE_PREFIX_RE = re.compile(
    r"\b(?:PySide6QtAds\.PySide6QtAds|pyside6_qtads_borco\._pyside6_qtads_borco|PySide6QtAds)\."
)

# Python 3.13 writes `typing.Any` inside a `X | Y` union where 3.14 writes `Any`.
TYPING_PREFIX_RE = re.compile(r"\btyping\.")


def __normalise(text: str) -> str:
    """Drop the binding's own module path and `typing.` from type names, so both bindings' signatures compare
    equal, whichever Python each was dumped with."""
    return TYPING_PREFIX_RE.sub("", MODULE_PREFIX_RE.sub("", text))


def __signatures(member: Any) -> list[str]:
    """Return the signature of each overload of a bound method, or [] if shiboken gives none.

    shiboken's own registry, as its stub generator uses it: on Python 3.14
    methods no longer carry ``__signature__``, and ``inspect.signature()``
    finds nothing.
    """
    from shibokensupport.signature import get_signature  # importable once shiboken6 is

    signature = get_signature(member)
    if signature is None:
        return []
    overloads = signature if isinstance(signature, list) else [signature]
    return sorted(__normalise(str(overload)) for overload in overloads)


def __signals(cls: type) -> list[str]:
    """Return the C++ signatures of the signals a QObject class declares itself, e.g. "closed()"."""
    meta = getattr(cls, "staticMetaObject", None)
    if meta is None:
        return []
    from PySide6.QtCore import QMetaMethod

    return sorted(
        bytes(meta.method(i).methodSignature().data()).decode()
        for i in range(meta.methodOffset(), meta.methodCount())
        if meta.method(i).methodType() == QMetaMethod.MethodType.Signal
    )


def __class_surface(cls: type) -> dict[str, Any]:
    """Return a class's own public members (with overload signatures), signals, and nested enums."""
    members: dict[str, list[str]] = {}
    enums: dict[str, list[str]] = {}
    for name, member in vars(cls).items():
        if name.startswith("_"):
            continue
        if isinstance(member, enum.EnumMeta):
            enums[name] = sorted(member.__members__)
        elif callable(member) or isinstance(member, (staticmethod, classmethod)):
            members[name] = __signatures(member)
        else:
            members[name] = []
    return {
        "bases": [__normalise(f"{base.__module__}.{base.__qualname__}") for base in cls.__bases__],
        "members": dict(sorted(members.items())),
        "signals": __signals(cls),
        "enums": dict(sorted(enums.items())),
    }


def api_surface(module_name: str) -> dict[str, Any]:
    """Return the public API of a binding's top-level module and of its ``ads`` namespace."""
    module = importlib.import_module(module_name)
    ads = module.ads
    module_names = sorted(
        name
        for name, value in vars(module).items()
        if not name.startswith("_") and not isinstance(value, types.ModuleType)
    )
    classes = {}
    enums = {}
    for name, value in sorted(vars(ads).items()):
        if name.startswith("_"):
            continue
        if isinstance(value, enum.EnumMeta):
            enums[name] = sorted(value.__members__)
        elif isinstance(value, type):
            classes[name] = __class_surface(value)
    return {"module": module_names, "ads": {"classes": classes, "enums": enums}}


def main() -> None:
    """Write ``api_surface(<module>)`` to ``<output.json>``, noting which release of ``<distribution>`` it came from."""
    if len(sys.argv) != 4:
        sys.exit(f"usage: {Path(sys.argv[0]).name} <module> <distribution> <output.json>")
    module_name, distribution, output = sys.argv[1:]
    surface = api_surface(module_name)
    surface["source"] = {
        "distribution": distribution,
        "version": importlib.metadata.version(distribution),
        "pyside6": importlib.metadata.version("PySide6-Essentials"),
    }
    Path(output).write_text(json.dumps(surface, indent=2, sort_keys=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
