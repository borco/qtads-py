.PHONY: setup lint format test clean clean-setup configure build install docs-serve qa stubs api-snapshot

setup:
	uv sync

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run pyright

# Serve the docs site locally with live-reload (http://127.0.0.1:8000/).
docs-serve:
	uv run --group docs mkdocs serve

format:
	uv run ruff format .

test:
	uv run pytest

clean:
	rm -rf build dist

clean-setup:
	rm -rf .venv

# Fast local iteration on the C++/binding side: reconfigure/rebuild the
# extension in-place against the existing .venv, without a full `uv sync`.
# `install` copies the built module and the QtAds library into
# src/pyside6_qtads_borco/ so `import pyside6_qtads_borco` picks up the
# change. Only the `python` component: QtAds' own install rules would also
# drop its headers and CMake package files into src/.
# On Windows, run these from an x64 Native Tools Command Prompt for VS 2022
# (the `venv` preset uses Ninja, which needs cl.exe on PATH).
configure:
	cmake --preset venv

build: configure
	cmake --build --preset venv

install: build
	cmake --install build/venv --component python

# Regenerate src/pyside6_qtads_borco/_pyside6_qtads_borco.pyi (see
# tools/generate_pyi.py). Run after `make install` / `uv sync
# --reinstall-package pyside6-qtads-borco` whenever bindings.xml/bindings.h
# change the public API.
stubs:
	uv run python tools/generate_pyi.py

# Re-snapshot PyPI pyside6-qtads' API for tests/test_api_superset.py, in a
# throwaway env (its exact PySide6 pin needn't match ours). Bump the version
# when pyside6-qtads releases one for a newer QtAds than ours.
PYSIDE6_QTADS_VERSION := 5.1.1.1
api-snapshot:
	uv run --isolated --no-project --with pyside6-qtads==$(PYSIDE6_QTADS_VERSION) \
		python tools/dump_api.py PySide6QtAds pyside6-qtads tests/data/pyside6_qtads_api.json

qa: format test lint
