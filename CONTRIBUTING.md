# How to contribute

## Dependencies

We use `poetry` to manage the [dependencies](https://github.com/python-poetry/poetry).
If you dont have `poetry`, you should install with `make poetry-download`.

To install dependencies and prepare [`pre-commit`](https://pre-commit.com/) hooks you would need to run `install` command:

### Linux

```bash
make install
make pre-commit-install
```

### Windows

```powershell
poetry run pre-commit install
pre-commit run --all-files
```

#### Linux

```bash
export PATH="$HOME/.poetry/bin:$PATH"
make install
make pre-commit-install
pre-commit run --all-files
make test && make coverage && make check-codestyle && make mypy && make check-safety && make extrabadges
pre-commit run --all-files
```

#### Windows

1. Install Poetry:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

2. Find the poetry installation directory:

```text
C:\Users\YourUsername\AppData\Roaming\Python\Scripts
C:\Users\YourUsername\AppData\Local\Programs\Python\PythonXX\Scripts (where XX is the Python version)
```

3. Add the correct Path to `PATH`:

```powershell
$env:PATH = "C:\Users\YourUsername\AppData\Roaming\Python\Scripts;" + $env:PATH
```

4. Verify poetry installation:

```powershell
poetry --version
```

5. Create and activate a new virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

5. Install required libraries:

```powershell
poetry lock -n; poetry export --without-hashes > requirements.txt
poetry install -n
```

6. Type check with mypy

```powershell
poetry run mypy --install-types --non-interactive pycvcqv/ tests/
```

7. Unit tests and coverage

```powershell
poetry run pytest --cov-report term --cov pycvcqv tests/
poetry run coverage-badge -o assets/images/coverage.svg -f
```

8. Lint

```powershell
poetry run pylint pycvcqv
```

9. Code-style check

```powershell
poetry run pyupgrade --exit-zero-even-if-changed --py37-plus
poetry run isort --diff --check-only --settings-path pyproject.toml ./
poetry run black --diff --check --config pyproject.toml ./
poetry run darglint --verbosity 2 pycvcqv tests
poetry run interrogate -v pycvcqv
```

10. Safety check

```powershell
poetry check
poetry run safety check --policy-file safety_policy.yml
poetry run bandit -ll --configfile pyproject.toml --recursive pycvcqv tests
```

11. Creating badges data

```powershell
.\.shell\badges.ps1
```

### Upload code to GitHub

```bash
git pull
pre-commit run --all-files
git add .
git commit -m ":tada: Initial commit"
git push -u origin main
```

12. Upload to pypi (for maintainers)

```powershell
pip install twine
pip install --upgrade build
python -m build
python -m twine upload --repository pycvcqv dist/*
git tag -a <tag_name> -m "<message>"
git push -u origin <tag_name>
```

## Other help

You can contribute by spreading a word about this library.
It would also be a huge contribution to write
a short article on how you are using this project.
You can also share your best practices with us.
