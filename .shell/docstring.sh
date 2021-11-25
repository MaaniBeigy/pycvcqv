#!/bin/bash
find . -name 'docstring.txt' -delete
interrogate -v pycvcqv >>.logs/docstring.txt
poetry run interrogate pycvcqv
