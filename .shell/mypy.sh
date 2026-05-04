#!/bin/bash
find . -name 'mypy.txt' -delete
find . -name 'mypy.svg' -delete
poetry run mypy --config-file pyproject.toml ./ | tee .logs/mypy.txt

# Extract the first whitespace-delimited token from the 'Success' line, if any.
mypy_result=$(grep 'Success' .logs/mypy.txt | cut -d\  -f1 | tr -d ':')

# If mypy did not print a 'Success' line, treat the run as a failure.
if [ -z "$mypy_result" ]; then
    mypy_result="Failure"
fi
export mypy_result
echo "mypy_result:" "$mypy_result"

# Persist a JSON artifact for downstream tooling (parity with .shell/mypy.ps1).
printf '{\n    "mypy_result":  "%s"\n}\n' "$mypy_result" > .logs/mypy.json

# Read the mypy result back from the JSON so the badge stays in lock-step with
# the on-disk artifact that downstream tooling consumes.
mypy_result=$(jq -r '.mypy_result' .logs/mypy.json)

# Pick a color based on whether mypy passed (anybadge requires uppercase names).
if [ "$mypy_result" = "Success" ]; then
    color="GREEN"
else
    color="RED"
fi

# Generate the mypy badge using anybadge (already in the venv via dev deps).
rm -rf assets/images/mypy.svg
poetry run python3 -m anybadge --overwrite --label=mypy --value="${mypy_result}" --color="${color}" --file=assets/images/mypy.svg
