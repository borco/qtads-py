.PHONY: setup lint format test clean clean-setup configure build install docs-serve qa

setup:
	uv sync

# pyright isn't run yet: the extension has no .pyi stub until #2 adds
# tools/generate_pyi.py, so `import ._pyside6_qtads_borco` can't be resolved.
lint:
	uv run ruff check .
	uv run ruff format --check .

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

qa: format test lint
