# CLAUDE.md

This file grounds Claude sessions working on this repository.

## What this is

`qtads-py` is a PySide6 binding for [Qt Advanced Docking System](https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System)
(QtAds), built with shiboken6 + CMake + scikit-build-core.

| | |
| --- | --- |
| PyPI | [`pyside6-qtads-borco`](https://pypi.org/project/pyside6-qtads-borco/) (only a 0.0.0 name reservation so far) |
| Import | `pyside6_qtads_borco`. Users switch with `import pyside6_qtads_borco as QtAds` |
| License | LGPL-2.1-or-later, to match QtAds and pyside6_qtads. QtAds is built as a **shared** library bundled in the wheel |
| Versioning | follows QtAds: QtAds 5.1.1 → this package 5.1.1.N |

**Why it exists.** PyPI [`pyside6-qtads`](https://pypi.org/project/pyside6-qtads/) (built from
[mborgerson/pyside6_qtads](https://github.com/mborgerson/pyside6_qtads)) pins exact PySide6 versions, so it lags behind
every PySide6 release, and upstream QtAds fixes only reach its users when someone rebuilds it. Its main consumer here is
[borco/rehuco](https://github.com/borco/rehuco), which also carries about 2.5k lines of Python workarounds for QtAds
(`packages/borco-pyside/src/borco_pyside/qtads/`). **The goal is for all of those workarounds to move into this binding.**

**Status.** The repo is being scaffolded (#1). Until a feature is built and tested here, don't describe it in the
README, the PyPI description or the GitHub description as something that works now. Write about intended features under
a heading that says they're planned.

## Design rules (decided, don't relitigate)

### 1. Drop-in for `pyside6-qtads` by default, not as a fixed rule

Code written for vanilla `pyside6-qtads` must keep working once its import line is changed: the same class, enum,
method and signal names and shapes. Our additions are **new, opt-in** API, and vanilla classes keep their vanilla
behaviour.

Where we think their packaging is wrong (a mis-bound signature, bad typing, a wrongly exposed enum or ownership), we
**may deviate**. Each deviation must:

- come with a PR or issue against `mborgerson/pyside6_qtads` proposing the fix;
- be recorded as a **breaking change** in `docs/compatibility.md` (what differs, why, a link to the upstream PR) and in
  `CHANGELOG.md` under `Breaking`;
- be listed in the tests' deviation registry: compat tests are `xfail(strict=True)` with reason and link, and
  `test_api_superset.py` gets an allowlist entry. An unrecorded difference fails CI.

How this is checked (#2):

- **Their tests run unmodified.** `extern/pyside6_qtads` is a submodule. `tests/compat/conftest.py` sets
  `sys.modules["PySide6QtAds"] = pyside6_qtads_borco` and puts their `tests/` on `sys.path`. Never edit their files.
- **`tests/test_api_superset.py`**: with PyPI `pyside6-qtads` installed as a dev-only dependency, every public name and
  member of theirs must exist in ours.

### 2. Our fixes are permanent and applied all together

We never wait for upstream to accept a fix. Each fix goes in the **cheapest layer that can carry it**:

1. **Python layer** (`src/pyside6_qtads_borco/`): pure Python, costs nothing when upstream changes. Most of rehuco's
   workarounds land here first, moved along with their tests.
2. **C++ extensions outside upstream source** (`src/pyside6_qtads_borco/bindings/*_ext.{h,cpp}`, like scintilla-py's
   `*_fixed.cpp`): new subclasses and helpers built on QtAds' public and protected API, for what Python can't do.
3. **Patch stack** in [borco/Qt-Advanced-Docking-System](https://github.com/borco/Qt-Advanced-Docking-System): root-cause
   fixes that need QtAds internals.

Move a fix down a layer only when that removes a workaround's root cause, and then delete the workaround above it.

### 3. The patch stack

- The fork has **one branch per upstream base**, `qtads-py/<upstream-tag-or-short-sha>`: the base plus **one commit
  per fix**, each commit message giving the reason, what it fixes, and an upstream PR link if one was sent.
- The `extern/qtads` submodule points at that branch's tip. There is no patch-apply step.
- **Following upstream**: create a new `qtads-py/<new-base>` branch from the new upstream tag or commit and
  `git rebase --onto` the stack onto it (fixes that upstream merged drop out on their own), then bump the submodule and
  let CI run.
- **Never force-push a published `qtads-py/*` branch.** Every old commit of this repo must keep a reachable submodule
  commit.
- Sending a fix upstream is optional: a cherry-pick of one commit onto upstream `master`, and nothing waits on it.
- `docs/patches.md` (#4) is where this procedure and the table of the stack live.

## Work tracking

- **Issues here**: #1 scaffold, #2 vanilla parity, #3 wheels/publish/PySide6 auto-bump, #4 the patch-stack procedure,
  #5 nested dock managers, #6 dock tabs, #7 dock restoration, #8 maximize (deferred). They're linked with *blocked by*:
  #1 comes first, then #2 and #4, and everything else needs #2.
- **What to work on next**: the lowest-numbered open issue that isn't blocked and isn't `deferred`. If unsure, say
  which one you'd pick and why, and ask.
- **Two repos, two issues.** Anything that changes rehuco is a **borco/rehuco** issue, never one here. A change that
  needs both repos gets an issue here that implements it and a rehuco issue that adopts it, linked *blocked by*. The
  rehuco side so far: rehuco#524 (switch to this package), and rehuco#614 / #615 / #616 / #617, which adopt #5 / #6 /
  #7 / #8. They're all in rehuco's `Migrations` milestone.
- **Labels**, one of each kind per issue:
  - **Size**: `XS` (≤30 min agent time), `S` (30–60 min), `M` (1–2 h), `L` (2–4 h), `XL` (>4 h, split before starting).
  - **Model**: `sonnet`, `opusplan`, `opus`, `fable`. The issue body ends with a `## Model` section saying which and why.
  - **Category**: `binding`, `packaging`, `maintenance`, `fixes`. `deferred` *replaces* the category on work that is
    deliberately unplanned.
- When a fix moves a rehuco workaround in, the rehuco side describes the problem in
  [`docs/specs/appendices/qt-ads.md`](https://github.com/borco/rehuco/blob/master/docs/specs/appendices/qt-ads.md)
  (cited by §). Read the relevant section before designing the fix.

## Stack

- **Languages**: C++ (binding glue, extensions) and Python (package, Python-layer fixes, tests)
- **Binding generator**: shiboken6. The starting typesystem is mborgerson/pyside6_qtads' `src/bindings.xml`, used as a
  reference for names, not something we keep in step with
- **Build**: CMake + scikit-build-core, built without isolation so CMake finds the PySide6/shiboken6 of the `.venv` it
  will run in
- **Package manager**: uv
- **CI**: GitHub Actions + cibuildwheel, with one cp311-abi3 wheel per platform
- **PySide6 pin**: one PySide6 minor per release, as in scintilla-py, with a daily workflow that opens a PR bumping it (#3)

## Template

The layout and build setup copy **pre-monorepo pyside6-scintilla**: `borco/scintilla-py` at commit `9a55be0e`
(`gh api "repos/borco/scintilla-py/git/trees/9a55be0e?recursive=1"`). Read its `pyproject.toml`, `CMakeLists.txt`,
`src/pyside6_scintilla/bindings/CMakeLists.txt`, `tools/generate_pyi.py` and `.github/workflows/` before writing ours.
Differences from it:

- the C++ source is a **submodule** (`extern/qtads`), not a vendored copy;
- the license is LGPL-2.1-or-later, not MIT;
- QtAds needs `Qt6::GuiPrivate`, plus xcb on Linux;
- the Linux wheel repair must also exclude `libxkbcommon*` and `libxcb*`. `pyside6-qtads` vendors its own
  `libxkbcommon`, which crashes Qt on mouse motion (rehuco's qt-ads.md §7).

## Where things go (once #1 lands)

- `extern/qtads/`: submodule, our fork's `qtads-py/<base>` branch
- `extern/pyside6_qtads/`: submodule, mborgerson/pyside6_qtads (their tests)
- `src/pyside6_qtads_borco/__init__.py`: the public Python API surface
- `src/pyside6_qtads_borco/bindings/`: typesystem XML, `bindings.h`, `*_ext.{h,cpp}`
- `tests/`, with `tests/compat/` for their tests run against us
- `tools/generate_pyi.py`: generated stubs
- `docs/`: `compatibility.md`, `patches.md`, and the mkdocs site

## Dev machines and platforms

- Dev machines: Windows 11 (primary) and a macOS M1 Mac Mini.
- Wheels: Windows x86_64, Linux x86_64/aarch64, macOS arm64/x86_64.

## Python style

For hand-written Python, as in scintilla-py and rehuco:

- Prefer a bare `Final` over `Final[T]` when the type can be inferred.
- Names are either public (`name`) or private (`__name`). There's no single-underscore "protected" convention.
- Write brief docstrings, private members included, saying *why* and *what*, without restating what a good name says.
  Stub and hover docs aimed at users of the binding can say more.
- ruff for formatting and linting, pyright in standard mode.

## Git

- **Never commit or push without explicit approval.** Stage the changes and present them for review first.
- For a tracked issue, branch off the current branch as `issue/NN/short-slug`. Prefix commit subjects with
  `refs #NN: <type>:` (types: `repo:`, `config:`, `docs:`, `feat:`, `fix:`, `refactor:`, `test:`), where `NN` is this
  repo's issue number. Commits directly on `main` carry no `refs` prefix.
- Merge back with `--no-ff`. Before merging, check whether the parent branch has moved and say so. Ask before rebasing.
- Commits in the fork (`extern/qtads`) follow the patch-stack rules above: one fix per commit, on a `qtads-py/*`
  branch, never force-pushed.
