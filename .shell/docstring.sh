#!/bin/bash
find . -name 'docstring.txt' -delete
poetry run python3 -m interrogate -v pycvcqv >>.logs/docstring.txt
poetry run python3 -m interrogate pycvcqv
