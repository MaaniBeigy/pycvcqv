# type: ignore[attr-defined]
"""Coefficient of Variation (CV) and Coefficient of Quartile Variation (CQV)."""

from importlib import metadata as importlib_metadata

from pycvcqv.cqv import cqv
from pycvcqv.cv import coefficient_of_variation
from pycvcqv.dataframe import cqv_dataframe, cv_dataframe
from pycvcqv.is_numeric import is_numeric

# -------------------------------- function definition --------------------------------


def get_version() -> str:
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
