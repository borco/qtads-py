# Build instructions

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- A C++17 compiler: MSVC 2022 on Windows, GCC or Clang on Linux, Xcode's Clang on macOS
- A Qt SDK of the same minor as the pinned PySide6 (6.11), e.g. from the Qt online installer or
  [aqtinstall](https://github.com/miurahr/aqtinstall). The PySide6 wheels ship Qt's libraries but not its headers,
  CMake packages or private headers, which QtAds needs on Linux (`Qt6::GuiPrivate`)
- On Linux, the xcb and xkbcommon development headers (`libxcb1-dev`, `libxkbcommon-dev` on Debian/Ubuntu), and clang
  for shiboken6's libclang (see `.github/workflows/ci.yml`)

QtAds' source is a submodule, so clone with `--recurse-submodules`, or run `git submodule update --init` afterwards.

## Local development build

`uv sync` builds everything (scikit-build-core + CMake + `shiboken_generator_create_binding()`): QtAds from
`extern/qtads` as a shared library, then the `_pyside6_qtads_borco` extension. CMake needs `CMAKE_PREFIX_PATH`
pointing at the Qt SDK:

```powershell
# Windows (PowerShell)
$env:CMAKE_PREFIX_PATH = "C:\Qt\6.11.1\msvc2022_64"
uv sync
```

```bash
# Linux / macOS
export CMAKE_PREFIX_PATH=/path/to/Qt/6.11.1/gcc_64   # or macos, etc.
uv sync
```

The project is built without build isolation, so that CMake finds the PySide6 and shiboken6 of the `.venv` the
extension will be imported from. uv installs the build tools from the `dev` group first and builds this package
last, which only works because `[project].version` in `pyproject.toml` is static (see the comment there).

### Forcing a rebuild

`uv sync` doesn't always notice changes to `CMakeLists.txt`, the typesystem, or the QtAds submodule. Force a
rebuild with:

```bash
uv sync --reinstall-package pyside6-qtads-borco
```

### Faster C++/binding-only iteration

`make configure`, `make build` and `make install` reuse an incremental CMake build tree (`build/venv/`) and install
the extension and the QtAds library straight into `src/pyside6_qtads_borco/`.

**Windows**: the `venv` preset uses Ninja, which needs `cl.exe` on `PATH`. Run these from an **x64 Native Tools
Command Prompt for VS 2022**, or call `vcvarsall.bat x64` first. `uv sync` doesn't need this: scikit-build-core
uses the Visual Studio generator, which finds MSVC itself.

## Verifying the build

```bash
uv run pytest
uv run ruff check .
uv run python examples/simple.py
```
