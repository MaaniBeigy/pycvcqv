# Start the script
Write-Output "start"

# Execute the PowerShell scripts in the .shell directory
& .\.shell\pylint.ps1
& .\.shell\mypy.ps1
& .\.shell\safety.ps1
& .\.shell\complexity.ps1
& .\.shell\maintainability.ps1
& .\.shell\docstring.ps1
& .\.shell\bandit.ps1
& .\.shell\black.ps1
