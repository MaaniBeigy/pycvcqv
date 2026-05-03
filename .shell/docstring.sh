#!/bin/bash
# Regenerate the docstring-coverage report and the corresponding shields.io
# badge, then write the textual report to .logs/docstring.txt.

mkdir -p .logs assets/images

find . -name 'docstring.txt' -delete

poetry run interrogate -v pycvcqv >.logs/docstring.txt
poetry run interrogate pycvcqv

# Generate the SVG badge (forward slashes — backslashes get eaten by bash).
poetry run interrogate --generate-badge assets/images/interrogate_badge.svg
