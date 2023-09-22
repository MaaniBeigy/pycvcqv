#!/bin/bash
find . -name 'coverage.txt' -delete
poetry run pytest --cov-report term --cov pycvcqv tests/ > .logs/coverage.txt
