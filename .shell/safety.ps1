# Find and delete previous safety artifacts so a fresh run starts clean.
Get-ChildItem -Path . -Recurse -Filter 'safety.txt' | Remove-Item -Force
Get-ChildItem -Path . -Recurse -Filter 'safety.json' | Remove-Item -Force
Get-ChildItem -Path . -Recurse -Filter 'vulnerabilities.svg' | Remove-Item -Force

# Run safety twice to capture both report formats.
poetry run safety check --policy-file safety_policy.yml --output text | Tee-Object -FilePath ".logs/safety.txt"
poetry run safety check --policy-file safety_policy.yml --output json > ".logs/safety.json"

# Read the full safety report and pull out the vulnerability count.
$report = Get-Content -Path ".logs/safety.json" -Raw | ConvertFrom-Json
$vulnerabilities_found = $report.report_meta.vulnerabilities_found

# Safety reports null when nothing is flagged; surface that as a literal 0 so
# the downstream badge shows a number instead of the word "null".
if ($null -eq $vulnerabilities_found -or "$vulnerabilities_found" -eq "") {
    $vulnerabilities_found = 0
}
# Coerce to an integer so JSON serialization writes `0` rather than `"0"`.
$vulnerabilities_found = [int]$vulnerabilities_found

# Slim the on-disk JSON down to a single, downstream-friendly field. Anything
# else in the safety report is already in the .txt log.
@{
    vulnerabilities_found = $vulnerabilities_found
} | ConvertTo-Json | Set-Content -Path ".logs/safety.json"

Write-Output "vulnerabilities_found: $vulnerabilities_found"

# Pick a color based on whether anything was flagged (anybadge needs an
# uppercase color name).
$color = if ($vulnerabilities_found -eq 0) { "GREEN" } else { "RED" }

# Generate the badge from the slimmed JSON's value via anybadge (already in
# the venv via dev deps; pybadges is not).
poetry run python -m anybadge --overwrite --label=vulnerabilities --value=$vulnerabilities_found --color=$color --file=assets/images/vulnerabilities.svg
