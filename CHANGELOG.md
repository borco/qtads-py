# Changelog

All notable changes to this project are documented in this file, one entry
per release. Format loosely follows [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/); entries are kept high-level
(what shipped, breaking changes) rather than a full commit-by-commit log --
see git history for that.

Differences from PyPI `pyside6-qtads` are listed under **Breaking**, with the
details in `docs/compatibility.md`.

## [Unreleased]

### Added

- Repository scaffold (#1): QtAds built from
  [borco/Qt-Advanced-Docking-System](https://github.com/borco/Qt-Advanced-Docking-System)
  (`extern/qtads`, branch `qtads-py/edba03d0`, upstream `master` after 5.1.1)
  as a shared library, and a minimal shiboken6 binding (`CDockManager`,
  `CDockContainerWidget`, `CDockWidget`, `CDockAreaWidget` and the `ads`
  enums) against PySide6 6.11.
