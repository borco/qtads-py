# qtads-py

PySide6 bindings for [Qt Advanced Docking System](https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System)
(QtAds), published on PyPI as [`pyside6-qtads-borco`](https://pypi.org/project/pyside6-qtads-borco/) and imported as
`pyside6_qtads_borco`.

!!! note "Early development"
    The repository binds the whole API of `pyside6-qtads` and passes its tests, but nothing has been released
    yet. See [Compatibility with pyside6-qtads](compatibility.md).

## Planned

- **A drop-in replacement for [`pyside6-qtads`](https://pypi.org/project/pyside6-qtads/)**: the same class, enum,
  method and signal names, so that switching is an import-line change: `import pyside6_qtads_borco as QtAds`.
- **Released for each PySide6 minor**, soon after PySide6 itself.
- **QtAds fixes applied in the binding**, from a patched fork of QtAds and from a Python layer, without waiting for
  upstream releases.
