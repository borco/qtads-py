# Compatibility with pyside6-qtads

`pyside6_qtads_borco` is meant as a drop-in replacement for PyPI
[`pyside6-qtads`](https://pypi.org/project/pyside6-qtads/) (built from
[mborgerson/pyside6_qtads](https://github.com/mborgerson/pyside6_qtads)): code written for it should keep working
once its import line is changed to `import pyside6_qtads_borco as QtAds`. Our additions are new, opt-in API.

Where their packaging is wrong, we may deviate. Every deviation is listed [below](#deviations), and in the
CHANGELOG under **Breaking**.

## Reference

| | |
| --- | --- |
| `pyside6-qtads` release | 5.1.1.1 (QtAds 5.1.1) |
| Its tests | `extern/pyside6_qtads`, tag `v5.1.1.1` |
| Its API snapshot | `tests/data/pyside6_qtads_api.json` |
| Our QtAds | upstream `master` at `edba03d0`, after 5.1.1 (`extern/qtads`) |

This is only what parity is checked against. Our version numbers don't follow `pyside6-qtads`: they follow QtAds, as
`<QtAds version>.N` with our own `N` (QtAds 5.1.1 → 5.1.1.N).

## How it's checked

- **Their tests run unmodified** against this package. `tests/compat/conftest.py` makes `import PySide6QtAds`
  return `pyside6_qtads_borco` and puts their `tests/` on `sys.path`, and `tests/compat/test_upstream.py` collects
  every `unittest.TestCase` from their `test_*.py` files.
- **`tests/test_api_superset.py`** checks that everything in their API exists here in the same shape: module-level
  names, `ads` classes with their bases, own members and overload signatures, signals, and enum members.

Both have a deviation registry (`DEVIATIONS`). A failing compat test that's listed is a strict `xfail`; a listed
superset difference is allowed. An unlisted difference fails, and so does a listed one that no longer differs.

### Why a snapshot, not a dev dependency

Every `pyside6-qtads` release pins an exact PySide6 (5.1.1 needs 6.11.2, 5.1.1.1 needs 6.12.0), so installing it
next to this package would tie our PySide6 version to theirs and hold back every PySide6 bump until they publish
a matching release. Instead, `tools/dump_api.py` records their API in a throwaway environment, and the test compares
against that file. Only what QtAds itself adds is recorded, so the snapshot's PySide6 version doesn't matter.

Refresh it with `make api-snapshot`, after bumping `PYSIDE6_QTADS_VERSION` in the `Makefile`, when they release
for a QtAds at least as new as ours.

## Deviations

| What differs | Why | Upstream |
| --- | --- | --- |
| `ads.CFloatingDockContainer.waylandMoveOrLeaveInWindowPreview` takes a 4th, required argument, `Floatable: bool` | Not a packaging change: QtAds itself changed this static helper after 5.1.1, and our QtAds is newer than theirs. It's an internal helper of QtAds' Wayland drag handling. | [QtAds #873](https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System/pull/873); `pyside6-qtads` gets the same signature once it moves past QtAds 5.1.1 |

## Not deviations

- **Platform-specific API.** The snapshot is dumped on Windows, and QtAds declares a few things differently on other
  platforms: `CDockAreaWidget.event` and `CFloatingDockContainer.nativeEvent` exist only on Windows, and on Linux
  `CFloatingDockContainer` derives from `QDockWidget` instead of `QWidget`. `pyside6-qtads` differs across platforms
  in the same way. `PLATFORM_SPECIFIC` in `tests/test_api_superset.py` lists them.

- **Enum values at module level** (`QtAds.TopDockWidgetArea`, ...) are taken from their enum
  (`ads.DockWidgetArea.TopDockWidgetArea`) instead of shiboken's old-style `ads.TopDockWidgetArea`. They're the same
  objects; only type checkers see a difference, and they now see the right type.
- **QtAds is a shared library**, where `pyside6-qtads` links it statically. Five classes that `pyside6-qtads` binds
  weren't exported from QtAds' DLL (`CTitleBarButton`, `CSpacerWidget`, `CDockingStateReader`, `CDockOverlayCross`,
  `CFloatingDragPreview`), so our QtAds fork exports them. Their Python API is unchanged.
