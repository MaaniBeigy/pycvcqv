# Delete the 'maintainability.txt' file if it exists
Get-ChildItem -Path . -Recurse -Filter 'maintainability.txt' | Remove-Item -Force

# Run radon to calculate the maintainability index and save the output to a log file
poetry run python -m radon mi pycvcqv -s | Out-File -FilePath ".logs/maintainability.txt" -Append

# Extract and calculate the maintainability score
$maintainabilityScores = poetry run python -m radon mi pycvcqv -s | Select-String -Pattern '\((.*?)\)' | ForEach-Object {
    $_.Matches.Value.Trim('()')
}

# Calculate the average maintainability score
$total = 0
$count = 0

foreach ($score in $maintainabilityScores) {
    $total += [double]$score
    $count++
}

$averageMaintainability = if ($count -gt 0) { 
    $average = $total / $count
    "{0:N1}%%" -f $average
}
else { 
    "0.0%%"
}

# Output the maintainability score (for verification)
Write-Output "maintainability: $averageMaintainability"

# Create an object to store the maintainability in JSON format
$jsonOutput = @{
    maintainability = $averageMaintainability
} | ConvertTo-Json

# Save the JSON output to a file
$jsonOutput | Set-Content -Path ".logs/maintainability.json"
