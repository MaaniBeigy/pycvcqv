# pycvcqv

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/pycvcqv)](https://pypi.org/project/pycvcqv/)
[![Python Version](https://img.shields.io/pypi/pyversions/pycvcqv.svg)](https://pypi.org/project/pycvcqv/)
[![Build status](https://github.com/MaaniBeigy/pycvcqv/workflows/build/badge.svg)](https://github.com/MaaniBeigy/pycvcqv/actions?query=workflow%3Abuild)
[![coverage report](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/coverage.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/coverage.txt)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/MaaniBeigy/pycvcqv/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)
[![Downloads](https://static.pepy.tech/badge/pycvcqv)](https://pepy.tech/project/pycvcqv)

[![static analysis](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/mypy.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/mypy.txt)
[![vulnerabilities](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/vulnerabilities.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/safety.txt)
[![maintainability](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/maintainability.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/maintainability.txt)
[![complexity](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/complexity.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/complexity.txt)
[![lint report](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/pylint.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/pylint-log.txt)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/MaaniBeigy/pycvcqv/blob/master/.pre-commit-config.yaml)
[![License](https://img.shields.io/github/license/MaaniBeigy/pycvcqv)](https://github.com/MaaniBeigy/pycvcqv/blob/master/LICENSE)

Coefficient of Variation (CV) and Coefficient of Quartile Variation (CQV) with Confidence Intervals (CI)

Python port of [cvcqv](https://github.com/MaaniBeigy/cvcqv)

</div>

## Introduction

`pycvcqv` provides some easy-to-use functions to calculate the
Coefficient of Variation (`cv`) and Coefficient of Quartile Variation (`cqv`)
with confidence intervals provided with all available methods.

## Install

```bash
pip install pycvcqv
```

## Usage

```python
import pandas as pd
from pycvcqv import coefficient_of_variation, cqv

coefficient_of_variation(
    data=[0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5, 4.4, 4.6, 5.4, 5.4],
    multiplier=100,
)
# 64.6467
cqv(
    data=[0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5, 4.4, 4.6, 5.4, 5.4],
    multiplier=100,
)
# 51.7241
data = pd.DataFrame(
    {
        "col-1": pd.Series([0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]),
        "col-2": pd.Series([5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9]),
    }
)
coefficient_of_variation(data=data, num_threads=3)
#   columns      cv
# 0   col-1  0.6076
# 1   col-2  0.1359
cqv(data=data, num_threads=-1)
#   columns      cqv
# 0   col-1  0.3889
# 1   col-2  0.0732
```

## For contributors

### Testing

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

8. Code-style check

```powershell
poetry run pyupgrade --exit-zero-even-if-changed --py37-plus
poetry run isort --diff --check-only --settings-path pyproject.toml ./
poetry run black --diff --check --config pyproject.toml ./
poetry run darglint --verbosity 2 pycvcqv tests
```

9. Safety check

```powershell
poetry check
poetry run safety check --policy-file safety_policy.yml --output json > .logs/safety.json
poetry run bandit -ll --recursive pycvcqv tests
```

### Upload code to GitHub

```bash
git pull
pre-commit run --all-files
git add .
git commit -m ":tada: Initial commit"
git push -u origin main
```

## Credits

[![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)   
This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)
