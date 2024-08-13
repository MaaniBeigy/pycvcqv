#!/bin/bash
find . -name 'docstring.txt' -delete
interrogate -v lib/web/ >>.logs/docstring.txt
poetry run interrogate pycvcqv
# Run the interrogate --generate-badge command to save the badge svg file
poetry run interrogate --generate-badge .\assets\images\interrogate_badge.svg
