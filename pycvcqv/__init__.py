"""Coefficient of Variation (CV) and Coefficient of Quartile Variation (CQV)."""

from typing import Any

from importlib import metadata as importlib_metadata

from pycvcqv.checkers import is_numeric
from pycvcqv.cqv import cqv
from pycvcqv.cv import coefficient_of_variation
from pycvcqv.dataframe import cqv_dataframe, cv_dataframe


# -------------------------------- function definition --------------------------------
def get_version() -> Any:
    """Gets the version of package."""
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()

__all__ = [
    "coefficient_of_variation",
    "is_numeric",
    "cqv",
    "cv_dataframe",
    "cqv_dataframe",
]
