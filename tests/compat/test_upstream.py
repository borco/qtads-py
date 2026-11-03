"""Collect the ``unittest.TestCase`` classes of every ``test_*.py`` in mborgerson/pyside6_qtads' tests.

pytest only collects files under ``testpaths``, and a conftest only applies
below its own directory, so their files are imported here and their test
cases exposed as this module's. Only ``TestCase`` subclasses: their helper
classes are also named ``Test*`` (e.g. ``TestDockWidget``), which pytest
would otherwise try to collect.
"""

import importlib
import unittest

from conftest import THEIR_TESTS_DIR


def __collect() -> None:
    """Expose each of their test cases under its own name; two with the same name would hide one."""
    for path in sorted(THEIR_TESTS_DIR.glob("test_*.py")):
        module = importlib.import_module(path.stem)
        for name, value in vars(module).items():
            if isinstance(value, type) and issubclass(value, unittest.TestCase) and value.__module__ == path.stem:
                assert name not in globals(), f"{name} is defined by two of their test files"
                globals()[name] = value


__collect()
