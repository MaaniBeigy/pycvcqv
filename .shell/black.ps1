# Delete the 'black.txt' file if it exists
Get-ChildItem -Path . -Recurse -Filter 'black.txt' | Remove-Item -Force
# Run the black command and capture the output
$output = poetry run black --diff --check --config pyproject.toml ./ 2>&1

# Extract the first line from the original output
$firstLine = $output | Select-Object -First 1

# Clean the first line by removing any Unicode escape sequences
# This regex removes \uXXXX and \UXXXXXXXX patterns
$cleanFirstLine = $firstLine -replace '\\u[0-9A-Fa-f]{4}', '' -replace '\\U[0-9A-Fa-f]{8}', ''

# Extract the last line from the original output
$lastLine = $output | Select-Object -Last 1

# Write the cleaned first line and the last line to the file
@($cleanFirstLine, $lastLine) | Set-Content .logs/black.txt
