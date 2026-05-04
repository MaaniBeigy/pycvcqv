# pycvcqv

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/pycvcqv?logo=pypi&logoColor=white&logoSize=auto)](https://pypi.org/project/pycvcqv/)
[![Python Version](https://img.shields.io/pypi/pyversions/pycvcqv?logo=python&logoColor=white&logoSize=auto)](https://pypi.org/project/pycvcqv/)
[![Build status](https://github.com/MaaniBeigy/pycvcqv/workflows/build/badge.svg)](https://github.com/MaaniBeigy/pycvcqv/actions?query=workflow%3Abuild)
[![coverage report](assets/images/coverage.svg)](.logs/coverage.txt)
[![Downloads](https://static.pepy.tech/badge/pycvcqv)](https://pepy.tech/project/pycvcqv)
[!["Buy Me A Coffee"](https://img.shields.io/badge/-buy_me_a%C2%A0coffee-gray?logo=buy-me-a-coffee)](https://buymeacoffee.com/maani)
[![static analysis](assets/images/mypy.svg)](.logs/mypy.txt)
[![dependencies](https://img.shields.io/github/issues-pr/MaaniBeigy/pycvcqv/dependencies?logo=dependabot&logoColor=white&logoSize=auto&label=outdated%20dependencies)](https://github.com/MaaniBeigy/pycvcqv/pulls?q=is%3Aopen+is%3Apr+label%3Adependencies)
[![vulnerabilities](assets/images/vulnerabilities.svg)](.logs/safety.json)
[![maintainability](assets/images/maintainability.svg)](.logs/maintainability.txt)
[![complexity](assets/images/complexity.svg)](.logs/complexity.txt)
[![lint report](assets/images/pylint.svg)](.logs/pylint-log.txt)
[![docstring](assets/images/interrogate_badge.svg)](.logs/docstring.txt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](.logs/black.txt)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](.logs/bandit.txt)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](.pre-commit-config.yaml)
[![License](https://img.shields.io/github/license/MaaniBeigy/pycvcqv)](LICENSE)

Find homogeneity with confidence.

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

`coefficient_of_variation` accepts a `method` argument that selects the
confidence-interval estimator. The closed-form methods listed below are
ported math-for-math from the R [`cvcqv`](https://github.com/MaaniBeigy/cvcqv)
package.

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
):
    print(method, coefficient_of_variation(
        data=x, method=method, multiplier=100, ndigits=3,
    ))
```

The output (95% CI, `multiplier=100`, `ndigits=3`):

| method                 |    est |  lower |   upper | description                            |
|:-----------------------|-------:|-------:|--------:|:---------------------------------------|
| `kelley`               | 57.774 | 41.303 |  97.950 | cv with Kelley 95% CI                  |
| `mckay`                | 57.774 | 41.441 | 108.483 | cv with McKay 95% CI                   |
| `miller`               | 57.774 | 34.053 |  81.495 | cv with Miller 95% CI                  |
| `vangel`               | 57.774 | 40.955 | 103.931 | cv with Vangel 95% CI                  |
| `mahmoudvand_hassani`  | 57.774 | 43.476 |  82.857 | cv with Mahmoudvand-Hassani 95% CI     |
| `equal_tailed`         | 57.774 | 43.937 |  84.383 | cv with Equal-Tailed 95% CI            |
| `shortest_length`      | 57.774 | 42.015 |  81.013 | cv with Shortest-Length 95% CI         |
| `normal_approximation` | 57.774 | 44.533 |  85.272 | cv with Normal Approximation 95% CI    |

The bootstrap-based methods (`norm`, `basic`, `perc`, `bca`) are not yet
ported.

## Credits

[![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)
This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)
