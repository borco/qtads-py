"""Run mborgerson/pyside6_qtads' tests, unmodified, against this package.

Their tests (``extern/pyside6_qtads/tests``) do ``import PySide6QtAds as
QtAds`` and ``from base_qt_test import BaseQtTest``: alias the first to
``pyside6_qtads_borco`` and put their directory on ``sys.path`` for the
second. ``test_upstream.py`` collects their test cases.

A test that fails because of a deliberate deviation goes in ``DEVIATIONS``,
which marks it ``xfail(strict=True)``: an unrecorded difference fails, and so
does an entry whose test starts passing or no longer exists.
"""

import sys
from pathlib import Path
from typing import Final

import pytest

import pyside6_qtads_borco

THEIR_TESTS_DIR: Final = Path(__file__).resolve().parents[2] / "extern" / "pyside6_qtads" / "tests"

# "<TestCase class>::<test method>" -> why it differs, and the link to the
# upstream PR/issue proposing our behaviour (docs/compatibility.md has the details).
DEVIATIONS: Final[dict[str, str]] = {}

sys.modules["PySide6QtAds"] = pyside6_qtads_borco
sys.path.insert(0, str(THEIR_TESTS_DIR))


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Mark recorded deviations as strict xfails, and fail on entries that match no test."""
    compat_items = {item.nodeid.split("::", 1)[1]: item for item in items if "/compat/" in item.nodeid}
    if not compat_items:
        return  # compat tests deselected
    for test_id, reason in DEVIATIONS.items():
        if test_id not in compat_items:
            raise pytest.UsageError(f"tests/compat/conftest.py DEVIATIONS: no such test {test_id!r}")
        compat_items[test_id].add_marker(pytest.mark.xfail(reason=reason, strict=True))
