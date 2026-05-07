#!/bin/bash
# Regenerate the docstring-coverage report and the corresponding shields.io
# badge, then write the textual report to .logs/docstring.txt.

mkdir -p .logs assets/images

find . -name 'docstring.txt' -delete

poetry run interrogate -v pycvcqv >.logs/docstring.txt
poetry run interrogate pycvcqv

# Generate the SVG badge (forward slashes — backslashes get eaten by bash).
# NOTE: pass `pycvcqv` so the badge mirrors the package-only score (100%);
# omitting the path makes interrogate scan the whole repo (tests/, .shell/, ...)
# and produces a misleading lower percentage.
poetry run interrogate pycvcqv --generate-badge assets/images/interrogate_badge.svg
