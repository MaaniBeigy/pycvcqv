# Run pylint using poetry and save the output to a log file
poetry run interrogate -v pycvcqv | Tee-Object -FilePath ".logs/docstring.txt"
# Run the interrogate command and capture the output
$output = poetry run interrogate pycvcqv

# Extract the RESULT
$result = $output | Select-String -Pattern 'RESULT:' | ForEach-Object {
    $_.Line -split ' ' | Select-Object -Index 1
}

# Extract the actual percentage
$actual = $output | Select-String -Pattern 'actual:' | ForEach-Object {
    $line = $_.Line -split ' ' | Select-Object -Index 3
    $line.TrimEnd(')')
}

# Create an object to store the RESULT and actual percentage in JSON format
$jsonOutput = @{
    RESULT = $result
    actual = $actual
} | ConvertTo-Json

# Save the JSON output to a file
$jsonOutput | Set-Content -Path ".logs/docstring.json"

# Output for verification
Write-Output "RESULT: $result, actual: $actual"
# Run the interrogate --generate-badge command to save the badge svg file
poetry run interrogate --generate-badge .\assets\images\interrogate_badge.svg
