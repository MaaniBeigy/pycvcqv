#!/bin/bash
find . -name 'safety.txt' -delete
find . -name 'vulnerabilities.svg' -delete
poetry run safety check --policy-file safety_policy.yml --output text > .logs/safety.txt
poetry run safety check --policy-file safety_policy.yml --output json > .logs/safety.json
vulnerabilities_found=$(jq -r '.report_meta.vulnerabilities_found' .logs/safety.json)
export VULNERABILITIES_FOUND=$vulnerabilities_found
echo "vulnerabilities:" $VULNERABILITIES_FOUND
rm -rf assets/images/vulnerabilities.svg
poetry run python3 -m pybadges --left-text="vulnerabilities" --right-text=${VULNERABILITIES_FOUND} --left-color="#40aef9" --right-color="#0c2739" --logo=assets/images/safety.png --embed-logo >>assets/images/vulnerabilities.svg
