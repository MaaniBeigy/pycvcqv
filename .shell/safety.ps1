# Read the JSON file content
$jsonContent = Get-Content -Path ".logs/safety.json" -Raw

# Parse the JSON content
$jsonObject = $jsonContent | ConvertFrom-Json

# Extract the value
$vulnerabilities_found = $jsonObject.report_meta.vulnerabilities_found

# Output the value
Write-Output $vulnerabilities_found

# Remove the old vulnerabilities.svg file
Remove-Item -Path "assets/images/vulnerabilities.svg" -Force -Recurse

# Run the Python command using poetry and the extracted value
# Note: Make sure 'poetry' and 'python3' are in your system's PATH
$command = "poetry run python -m pybadges --left-text='vulnerabilities' --right-text='$vulnerabilities_found' --left-color='#40aef9' --right-color='#0c2739' --logo=assets/images/safety.png --embed-logo >> assets/images/vulnerabilities.svg"
Invoke-Expression $command