# pycvcqv

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/pycvcqv?logo=pypi&logoColor=white&logoSize=auto)](https://pypi.org/project/pycvcqv/)
[![Python Version](https://img.shields.io/pypi/pyversions/pycvcqv?logo=python&logoColor=white&logoSize=auto)](https://pypi.org/project/pycvcqv/)
[![Build status](https://github.com/MaaniBeigy/pycvcqv/workflows/build/badge.svg)](https://github.com/MaaniBeigy/pycvcqv/actions?query=workflow%3Abuild)
[![coverage report](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/coverage.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/coverage.txt)
[![Downloads](https://static.pepy.tech/badge/pycvcqv)](https://pepy.tech/project/pycvcqv)
[!["Buy Me A Coffee"](https://img.shields.io/badge/-buy_me_a%C2%A0coffee-gray?logo=buy-me-a-coffee)](https://buymeacoffee.com/maani)
[![static analysis](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FMaaniBeigy%2Fpycvcqv%2Fmain%2F.logs%2Fmypy.json&query=%24.mypy_result&label=mypy&color=brightgreen)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/mypy.txt)
[![dependencies](https://img.shields.io/github/issues-pr/MaaniBeigy/pycvcqv/dependencies?logo=dependabot&logoColor=white&logoSize=auto&label=outdated%20dependencies)](https://github.com/MaaniBeigy/pycvcqv/pulls?q=is%3Aopen+is%3Apr+label%3Adependencies)
[![vulnerabilities](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FMaaniBeigy%2Fpycvcqv%2Fmain%2F.logs%2Fsafety.json&query=%24.vulnerabilities_found&label=vulnerabilities&labelColor=%234AADF1&color=%230A0C10)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/safety.txt)
[![maintainability](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FMaaniBeigy%2Fpycvcqv%2Fmain%2F.logs%2Fmaintainability.json&query=%24.maintainability&label=maintainability&color=brightgreen)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/maintainability.txt)
[![complexity](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FMaaniBeigy%2Fpycvcqv%2Fmain%2F.logs%2Fcomplexity.json&query=%24.complexity&label=complexity&color=brightgreen)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/complexity.txt)
[![lint report](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FMaaniBeigy%2Fpycvcqv%2Fmain%2F.logs%2Fpylint-log.json&query=%24.lintscore&label=pylint&color=brightgreen)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/pylint-log.txt)
[![docstring](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/assets/images/interrogate_badge.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/docstring.txt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/black.txt)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://raw.githubusercontent.com/MaaniBeigy/pycvcqv/main/.logs/bandit.txt)
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

## Credits

[![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)
This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)
