# Find and delete files named 'mypy.txt'
Get-ChildItem -Path . -Recurse -Filter 'mypy.txt' | Remove-Item -Force

# Find and delete files named 'mypy.svg'
Get-ChildItem -Path . -Recurse -Filter 'mypy.svg' | Remove-Item -Force

# Run mypy using poetry and save the output to a log file
poetry run mypy --config-file pyproject.toml ./ | Tee-Object -FilePath ".logs/mypy.txt"

# Extract the mypy result from the log file
$mypy_result = Select-String -Path ".logs/mypy.txt" -Pattern 'Success' | ForEach-Object {
    $_.Line -split ' ' | Select-Object -First 1
} | ForEach-Object {
    $_ -replace ':', ''
}

# If no 'Success' line was found, treat the run as a failure.
if ([string]::IsNullOrEmpty($mypy_result)) {
    $mypy_result = "Failure"
}

# Create an object to store the mypy_result in JSON format
$jsonOutput = @{
    mypy_result = $mypy_result
} | ConvertTo-Json

# Save the JSON output to a file
$jsonOutput | Set-Content -Path ".logs/mypy.json"

# Output the lint score (for verification)
Write-Output "mypy_result: $mypy_result"

# Read the mypy result back from the JSON so the badge stays in lock-step with
# the on-disk artifact that downstream tooling consumes.
$mypy_result = (Get-Content -Path ".logs/mypy.json" -Raw | ConvertFrom-Json).mypy_result

# Pick a color based on whether mypy passed (anybadge requires uppercase names).
$color = if ($mypy_result -eq "Success") { "GREEN" } else { "RED" }

# Generate the mypy badge using anybadge (already in the venv via dev deps).
poetry run python -m anybadge --overwrite --label=mypy --value=$mypy_result --color=$color --file=assets/images/mypy.svg
