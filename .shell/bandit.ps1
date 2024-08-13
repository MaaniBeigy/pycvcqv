
# Find and delete files named 'bandit'
Get-ChildItem -Path . -Recurse -Filter 'bandit.txt' | Remove-Item -Force
Get-ChildItem -Path . -Recurse -Filter 'bandit.json' | Remove-Item -Force
# Run bandit using poetry and save the output to a log file
poetry run bandit --configfile pyproject.toml --recursive pycvcqv tests --format json --output .logs/bandit.json
poetry run bandit --configfile pyproject.toml --recursive pycvcqv tests --format txt --output .logs/bandit.txt
