# Build instructions

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- A C++17 compiler: MSVC 2022 on Windows, GCC or Clang on Linux, Xcode's Clang on macOS
- A Qt SDK of the same minor as the pinned PySide6 (6.12), e.g. from the Qt online installer or
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
$env:CMAKE_PREFIX_PATH = "C:\Qt\6.12.0\msvc2022_64"
uv sync
```

```bash
# Linux / macOS
export CMAKE_PREFIX_PATH=/path/to/Qt/6.12.0/gcc_64   # or macos, etc.
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

After switching to another Qt SDK, also delete `build/`: its CMake cache keeps the old SDK's paths, and the build
then mixes the old SDK's headers with the new PySide6's.

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

## Wheels and releases

- **Wheels**: `.github/workflows/wheels.yml` runs cibuildwheel (`[tool.cibuildwheel]` in `pyproject.toml`), one
  cp311-abi3 wheel each for Windows x86_64, Linux x86_64/aarch64 and macOS arm64/x86_64, tested in place. Qt and
  PySide6's libraries aren't bundled: they come from the installed PySide6. On Linux, neither are libxcb and
  libxkbcommon, which come from the system, and the workflow fails if any of these end up in a wheel.
- **Releasing**: bump `[project].version`, add its `## [<version>] - <date>` section to `CHANGELOG.md`, and push a
  `v<version>` tag. `.github/workflows/publish.yml` builds the sdist and wheels, publishes to TestPyPI and then PyPI,
  and creates the GitHub Release from the changelog section. Run it by hand for a dry run that stops at TestPyPI.
- **Following PySide6**: `.github/workflows/bump-pyside6.yml` checks PyPI daily. When there's a newer PySide6, it
  opens an issue for it, pushes an `issue/<NN>/pyside6-<version>` branch made by `tools/bump_pyside6.py` and
  `uv lock`, and runs CI on it. Adopting it is a `--no-ff` merge of that branch and closing the issue. The Qt SDK version (in `ci.yml`, `wheels.yml` and `[tool.cibuildwheel]`) moves with it, since it must equal
  `uv.lock`'s PySide6. A new minor also moves the `>=6.X,<6.Y` pins, and starts a new release line.
