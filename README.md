# pycvcqv

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/pycvcqv)](https://pypi.org/project/pycvcqv/)
[![Python Version](https://img.shields.io/pypi/pyversions/pycvcqv.svg)](https://pypi.org/project/pycvcqv/)
[![Build status](https://github.com/MaaniBeigy/pycvcqv/workflows/build/badge.svg)](https://github.com/MaaniBeigy/pycvcqv/actions?query=workflow%3Abuild)
[![coverage report](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/coverage.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/coverage.txt)
[![static analysis](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/mypy.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/mypy.txt)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/MaaniBeigy/pycvcqv/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![maintainability](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/maintainability.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/maintainability.txt)
[![complexity](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/complexity.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/complexity.txt)
[![Safety Vulnerabilities](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/vulnerabilities.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/safety.txt)
[![docstring coverage](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/interrogate_badge.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/docstring.txt)
[![lint report](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/pylint.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/pylint-log.txt)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/MaaniBeigy/pycvcqv/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/MaaniBeigy/pycvcqv/releases)
[![License](https://img.shields.io/github/license/MaaniBeigy/pycvcqv)](https://github.com/MaaniBeigy/pycvcqv/blob/master/LICENSE)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMaaniBeigy%2Fpycvcqv.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FMaaniBeigy%2Fpycvcqv?ref=badge_shield)

Coefficient of Variation (CV) and Coefficient of Quartile Variation (CQV) with Confidence Intervals (CI)

Python port of [cvcqv](https://github.com/MaaniBeigy/cvcqv)

</div>

## Introduction

`pycvcqv` provides some easy-to-use functions to calculate the
Coefficient of  Variation (`cv`) and Coefficient of Quartile Variation (`cqv`)
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

## For contributors:

### Testing:

```bash
make install
make pre-commit-install
make test && make coverage && make check-codestyle && make mypy && make check-safety && make extrabadges
```

### Upload code to GitHub:

```bash
pre-commit run --all-files
git add .
git commit -m ":tada: Initial commit"
git push -u origin main
```


## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMaaniBeigy%2Fpycvcqv.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FMaaniBeigy%2Fpycvcqv?ref=badge_shield)

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMaaniBeigy%2Fpycvcqv.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FMaaniBeigy%2Fpycvcqv?ref=badge_large)
