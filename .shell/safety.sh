#!/bin/bash
find . -name 'safety.txt' -delete
find . -name 'safety.json' -delete
find . -name 'vulnerabilities.svg' -delete

# Run safety twice to capture both report formats.
poetry run safety check --policy-file safety_policy.yml --output text > .logs/safety.txt
poetry run safety check --policy-file safety_policy.yml --output json > .logs/safety.json

# Pull out the vulnerability count. jq's `// 0` defaults a missing or null
# field to 0 so the downstream badge shows a number instead of "null".
vulnerabilities_found=$(jq -r '.report_meta.vulnerabilities_found // 0' .logs/safety.json)
if [ -z "$vulnerabilities_found" ] || [ "$vulnerabilities_found" = "null" ]; then
    vulnerabilities_found=0
fi
export vulnerabilities_found
echo "vulnerabilities_found:" "$vulnerabilities_found"

# Slim the on-disk JSON down to a single, downstream-friendly field (parity
# with .shell/safety.ps1). Anything else from the safety report is already
# in the .txt log.
printf '{\n    "vulnerabilities_found":  %s\n}\n' "$vulnerabilities_found" > .logs/safety.json

# Pick a color based on whether anything was flagged (anybadge needs an
# uppercase color name).
if [ "$vulnerabilities_found" -eq 0 ]; then
    color="GREEN"
else
    color="RED"
fi

# Generate the badge from the slimmed JSON's value via anybadge (already in
# the venv via dev deps; pybadges is not).
poetry run python3 -m anybadge --overwrite --label=vulnerabilities --value="${vulnerabilities_found}" --color="${color}" --file=assets/images/vulnerabilities.svg
