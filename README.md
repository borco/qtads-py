# qtads-py

PySide6 bindings for [Qt Advanced Docking System](https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System)
(QtAds), built with shiboken6, CMake and scikit-build-core. The PyPI package is
[`pyside6-qtads-borco`](https://pypi.org/project/pyside6-qtads-borco/), imported as `pyside6_qtads_borco`.

> [!NOTE]
> Early development. The repository binds the whole API of `pyside6-qtads` and passes its tests, but nothing has
> been released yet: the only version on PyPI is a 0.0.0 name reservation.

## Planned

- **A drop-in replacement for [`pyside6-qtads`](https://pypi.org/project/pyside6-qtads/)**: the same class, enum,
  method and signal names, so that switching is an import-line change:
  `import pyside6_qtads_borco as QtAds`.
- **Released for each PySide6 minor**, soon after PySide6 itself.
- **QtAds fixes applied in the binding**, from a patched fork of QtAds and from a Python layer, without waiting for
  upstream releases.

## Building

Needs [uv](https://docs.astral.sh/uv/), a C++17 compiler (MSVC 2022 on Windows) and a Qt SDK of the same minor as the
PySide6 that's pinned (6.12), found through `CMAKE_PREFIX_PATH`:

```sh
git clone --recurse-submodules https://github.com/borco/qtads-py.git
cd qtads-py
CMAKE_PREFIX_PATH=/path/to/Qt/6.12.0/<arch> uv sync
uv run pytest
```

## License

LGPL-2.1-or-later, the same as QtAds. QtAds is built as a shared library and bundled in the wheel.
