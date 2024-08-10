# Find and delete files named 'pylint-log.txt'
Get-ChildItem -Path . -Recurse -Filter 'pylint-log.txt' | Remove-Item -Force

# Find and delete files named 'pylint.svg'
Get-ChildItem -Path . -Recurse -Filter 'pylint.svg' | Remove-Item -Force

# Run pylint using poetry and save the output to a log file
poetry run pylint pycvcqv | Tee-Object -FilePath ".logs/pylint-log.txt"

# Extract the lint score from the log file
$lintscore = Select-String -Path ".logs/pylint-log.txt" -Pattern 'rated at' | ForEach-Object {
    $_.Line -split ' ' | Select-Object -Index 6
} | ForEach-Object {
    $_ -split '/' | Select-Object -First 1
}

# Output the lint score (for verification)
Write-Output "lintscore: $lintscore"

# Generate the pylint badge using anybadge and save it to a file
$command = "poetry run python -m anybadge -o --value=$lintscore --file=assets/images/pylint.svg pylint"
Invoke-Expression $command
