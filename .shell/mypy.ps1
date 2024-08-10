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

# Output the mypy result (for verification)
Write-Output "mypy_result: $mypy_result"

# Remove the old mypy.svg file
Remove-Item -Path "assets/images/mypy.svg" -Force -Recurse

# Generate the mypy badge using pybadges and save it to a file
$command = "poetry run python -m pybadges --left-text='mypy' --right-color='brightgreen' --right-text=$mypy_result --embed-logo >> assets/images/mypy.svg"
Invoke-Expression $command
