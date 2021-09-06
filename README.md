# pycvcqv

<div align="center">

[![Build status](https://github.com/MaaniBeigy/pycvcqv/workflows/build/badge.svg)](https://github.com/MaaniBeigy/pycvcqv/actions?query=workflow%3Abuild)
[![coverage report](assets/images/coverage.svg)](https://github.com/MaaniBeigy/pycvcqv)
[![lint report](assets/images/pylint.svg)](https://github.com/MaaniBeigy/pycvcqv)
[![Python Version](https://img.shields.io/pypi/pyversions/pycvcqv.svg)](https://pypi.org/project/pycvcqv/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/MaaniBeigy/pycvcqv/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/MaaniBeigy/pycvcqv/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/MaaniBeigy/pycvcqv/releases)
[![License](https://img.shields.io/github/license/MaaniBeigy/pycvcqv)](https://github.com/MaaniBeigy/pycvcqv/blob/master/LICENSE)

:construction: WIP   
Coefficient of Variation (CV) and Coefficient of Quartile Variation (CQV) with Confidence Intervals (CI)   
Python port of [cvcqv](https://github.com/MaaniBeigy/cvcqv)

</div>

### Testing:  

```bash
make install
make test && make coverage && make check-codestyle && make mypy && make check-safety
```

### Pylint Badge:  

```bash
. .venv/bin/activate
pylint pycvcqv -> pylint-log.txt
lintscore=$(grep 'rated at' pylint-log.txt | cut -d\   -f10 | cut -d \/ -f 1)
pip3 install anybadge
anybadge -o --value=$lintscore --file=assets/images/pylint.svg pylint
```


### Upload initial code to GitHub:

```bash
git add .
git commit -m ":tada: Initial commit"
git push -u origin main
```


## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)
