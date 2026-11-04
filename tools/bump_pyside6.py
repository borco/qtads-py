"""Move the build to another PySide6 release, and the Qt SDK with it.

Usage: `python tools/bump_pyside6.py <version>`, then `uv lock` (the bump
workflow does both). The current version is the PySide6-Essentials one in
uv.lock. The Qt SDK version named in CI, the wheel builds and their install
paths always moves with it, since it must equal uv.lock's PySide6 (ci.yml
explains why). A new minor also moves the `>=6.X,<6.Y` pins and the
`libpyside6.abi3.so.6.X` sonames: that starts a new release line of this
package, since each PySide6 minor needs its own.
"""

import re
import sys
from pathlib import Path
from typing import Final

REPO_ROOT: Final = Path(__file__).resolve().parent.parent
UV_LOCK: Final = REPO_ROOT / "uv.lock"
# Every file that names the Qt SDK version or the PySide6 pins.
FILES: Final = [
    REPO_ROOT / "pyproject.toml",
    REPO_ROOT / ".github" / "workflows" / "ci.yml",
    REPO_ROOT / ".github" / "workflows" / "wheels.yml",
]
VERSION_RE: Final = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def current_version() -> str:
    """PySide6-Essentials' version in uv.lock."""
    match = re.search(r'^name = "pyside6-essentials"\nversion = "([^"]+)"', UV_LOCK.read_text("utf-8"), re.MULTILINE)
    if match is None:
        sys.exit(f"no pyside6-essentials in {UV_LOCK}")
    return match.group(1)


def bump(text: str, old: str, new: str) -> str:
    """`text` with `old`'s Qt SDK version, pins and sonames moved to `new`'s."""
    old_major, old_minor, _ = (int(part) for part in old.split("."))
    new_major, new_minor, _ = (int(part) for part in new.split("."))
    text = text.replace(old, new)
    if (old_major, old_minor) != (new_major, new_minor):
        text = text.replace(
            f">={old_major}.{old_minor},<{old_major}.{old_minor + 1}",
            f">={new_major}.{new_minor},<{new_major}.{new_minor + 1}",
        )
        text = text.replace(f".abi3.so.{old_major}.{old_minor}", f".abi3.so.{new_major}.{new_minor}")
    return text


def main() -> int:
    new = sys.argv[1]
    if VERSION_RE.match(new) is None:
        sys.exit(f"not a X.Y.Z version: {new}")
    old = current_version()
    if old == new:
        print(f"already at {new}")
        return 0
    for path in FILES:
        # newline="": keep each file's own line endings.
        with path.open(encoding="utf-8", newline="") as file:
            text = file.read()
        if old not in text:
            sys.exit(f"{path} doesn't name {old}: has the Qt SDK version drifted from uv.lock?")
        with path.open("w", encoding="utf-8", newline="") as file:
            file.write(bump(text, old, new))
    print(f"{old} -> {new}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
