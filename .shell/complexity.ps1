# Delete the 'complexity' files if it exists
Get-ChildItem -Path . -Recurse -Filter 'complexity.txt' | Remove-Item -Force
Get-ChildItem -Path . -Recurse -Filter 'complexity.json' | Remove-Item -Force

# Run radon using poetry and save the output to a log file
poetry run python -m radon cc pycvcqv -s -a | Out-File -FilePath ".logs/complexity.txt" -Append

# Extract the average complexity from the log file
$complexity = Select-String -Path ".logs/complexity.txt" -Pattern 'Average complexity:' | ForEach-Object {
    $_.Line -split ' ' | Select-Object -Index 2
}

# Create an object to store the complexity in JSON format
$jsonOutput = @{
    complexity = $complexity
} | ConvertTo-Json

# Save the JSON output to a file
$jsonOutput | Set-Content -Path ".logs/complexity.json"

# Output the complexity (for verification)
Write-Output "complexity: $complexity"
