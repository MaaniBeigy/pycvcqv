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
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMaaniBeigy%2Fpycvcqv.svg?type=shield&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2FMaaniBeigy%2Fpycvcqv?ref=badge_shield&issueType=license)

Find homogeneity with confidence.

Python port of [cvcqv](https://github.com/MaaniBeigy/cvcqv)

</div>

## Introduction

`pycvcqv` provides some easy-to-use functions to calculate the
Coefficient of Variation (`cv`) and Coefficient of Quartile Variation (`cqv`)
with confidence intervals provided with a variety of methods.

## Install

```bash
pip install pycvcqv
```

## Usage

```python
import pandas as pd
from pycvcqv import coefficient_of_variation, cqv

coefficient_of_variation(
    data=[
        0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5, 4.4,
        4.6, 5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9
    ],
    multiplier=100,
    ndigits=2
)
# {'cv': 57.77, 'lower': 41.43, 'upper': 98.38}
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
#   columns      cv      lower      upper
# 0   col-1  0.6076     0.3770     1.6667
# 1   col-2  0.1359     0.0913     0.2651
cqv(data=data, num_threads=-1)
#   columns      cqv
# 0   col-1  0.3889
# 1   col-2  0.0732
```

## Confidence-interval methods for `cv`

`coefficient_of_variation` accepts a `method` argument that selects the confidence-interval estimator.

```python
from pycvcqv import coefficient_of_variation

x = [
    0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5, 4.4,
    4.6, 5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9,
]

for method in (
    "kelley", "mckay", "miller", "vangel",
    "mahmoudvand_hassani", "equal_tailed",
    "shortest_length", "normal_approximation",
    "norm", "basic", "perc", "bca",
):
    print(method, coefficient_of_variation(
        data=x,
        method=method,
        multiplier=100,
        ndigits=3,
        num_replicates=10000,
        random_state=42,
    ))
```

Output (95% CI, `multiplier=100`, `ndigits=3`, bootstrap methods use
`num_replicates=10000`, `random_state=42`):

| method                 |    est |  lower |   upper | description                                        |
|:-----------------------|-------:|-------:|--------:|:---------------------------------------------------|
| `kelley`               | 57.774 | 41.303 |  97.950 | cv with Kelley 95% CI                              |
| `mckay`                | 57.774 | 41.441 | 108.483 | cv with McKay 95% CI                               |
| `miller`               | 57.774 | 34.053 |  81.495 | cv with Miller 95% CI                              |
| `vangel`               | 57.774 | 40.955 | 103.931 | cv with Vangel 95% CI                              |
| `mahmoudvand_hassani`  | 57.774 | 43.476 |  82.857 | cv with Mahmoudvand-Hassani 95% CI                 |
| `equal_tailed`         | 57.774 | 43.937 |  84.383 | cv with Equal-Tailed 95% CI                        |
| `shortest_length`      | 57.774 | 42.015 |  81.013 | cv with Shortest-Length 95% CI                     |
| `normal_approximation` | 57.774 | 44.533 |  85.272 | cv with Normal Approximation 95% CI                |
| `norm`                 | 57.774 | 38.850 |  78.379 | cv with Normal Approximation Bootstrap 95% CI      |
| `basic`                | 57.774 | 37.716 |  77.166 | cv with Basic Bootstrap 95% CI                     |
| `perc`                 | 57.774 | 38.382 |  77.832 | cv with Bootstrap Percentile 95% CI                |
| `bca`                  | 57.774 | 41.556 |  83.032 | cv with Adjusted Bootstrap Percentile (BCa) 95% CI |


## Confidence-interval methods for `cqv`

`cqv` accepts a `method` argument that selects the confidence-interval estimator.
When `method` is omitted only the point estimate is returned (the legacy behavior).

```python
from pycvcqv import cqv

x = [
    0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5, 4.4,
    4.6, 5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9,
]

for method in ("bonett", "norm", "basic", "perc", "bca"):
    print(method, cqv(
        data=x,
        method=method,
        multiplier=100,
        ndigits=3,
        num_replicates=10000,
        random_state=42,
    ))
```

Output (95% CI, `multiplier=100`, `ndigits=3`, bootstrap methods use
`num_replicates=10000`, `random_state=42`):

| method   |    est |  lower |  upper | description                                     |
|:---------|-------:|-------:|-------:|:------------------------------------------------|
| `bonett` | 45.625 | 24.785 | 77.329 | cqv with Bonett 95% CI                          |
| `norm`   | 45.625 | 19.937 | 70.403 | cqv with Normal Approximation Bootstrap 95% CI  |
| `basic`  | 45.625 | 21.081 | 73.923 | cqv with Basic Bootstrap 95% CI                 |
| `perc`   | 45.625 | 17.327 | 70.169 | cqv with Bootstrap Percentile 95% CI            |
| `bca`    | 45.625 | 22.006 | 76.331 | cqv with Adjusted Bootstrap Percentile (BCa) 95% CI |


## Credits

[![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)
This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)
