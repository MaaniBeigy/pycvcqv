# Read the JSON file content
$jsonContent = Get-Content -Path ".logs/safety.json" -Raw

# Parse the JSON content
$jsonObject = $jsonContent | ConvertFrom-Json

# Extract the value
$vulnerabilities_found = $jsonObject.report_meta.vulnerabilities_found

# Output the value
Write-Output $vulnerabilities_found

# Remove the old vulnerabilities.svg file
# Remove-Item -Path "assets/images/vulnerabilities.svg" -Force -Recurse

# Define the path to the input and output files
$inputFilePath = ".logs/safety.json"
$outputFilePath = ".logs/safety.json"

# Read the content of the JSON file
$jsonContent = Get-Content -Path $inputFilePath -Raw | ConvertFrom-Json

# Extract the value from the specific path
$vulnerabilitiesFound = $jsonContent.report_meta.vulnerabilities_found

# Create a new object with the desired structure
$result = @{
    vulnerabilities_found = $vulnerabilitiesFound
}

# Convert the object to JSON format
$jsonOutput = $result | ConvertTo-Json

# Write the output JSON to a file
$jsonOutput | Set-Content -Path $outputFilePath

Write-Output "The JSON data has been extracted and saved to $outputFilePath"

# Run the Python command using poetry and the extracted value
# Note: Make sure 'poetry' and 'python3' are in your system's PATH
# $command = "poetry run python -m pybadges --left-text='vulnerabilities' --right-text='$vulnerabilities_found' --left-color='#40aef9' --right-color='#0c2739' --logo=assets/images/safety.png --embed-logo >> assets/images/vulnerabilities.svg"
# Invoke-Expression $command
