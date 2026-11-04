"""`tools/bump_pyside6.py` moves the Qt SDK version always, and the pins and sonames only with a new minor."""

import importlib.util
from pathlib import Path
from typing import Any, Final

REPO_ROOT: Final = Path(__file__).resolve().parent.parent

TEXT: Final = """\
"PySide6-Essentials>=6.12,<6.13",
CMAKE_PREFIX_PATH = "/opt/qt/6.12.0/gcc_64"
--exclude libpyside6.abi3.so.6.12
"""


def __load_bump_pyside6() -> Any:
    """Import tools/bump_pyside6.py, which isn't part of the package."""
    spec = importlib.util.spec_from_file_location("bump_pyside6", REPO_ROOT / "tools" / "bump_pyside6.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_patch_release_moves_only_the_qt_sdk() -> None:
    assert __load_bump_pyside6().bump(TEXT, "6.12.0", "6.12.1") == TEXT.replace("6.12.0", "6.12.1")


def test_minor_release_moves_the_pins_and_sonames_too() -> None:
    assert __load_bump_pyside6().bump(TEXT, "6.12.0", "6.13.0") == (
        '"PySide6-Essentials>=6.13,<6.14",\nCMAKE_PREFIX_PATH = "/opt/qt/6.13.0/gcc_64"\n'
        "--exclude libpyside6.abi3.so.6.13\n"
    )


def test_current_version_is_uv_locks_pyside6() -> None:
    assert __load_bump_pyside6().current_version().startswith("6.")
