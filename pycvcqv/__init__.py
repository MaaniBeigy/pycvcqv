# type: ignore[attr-defined]
"""Coefficient of Variation (CV) and Coefficient of Quartile Variation (CQV)
with Confidence Intervals (CI)"""

import sys
from importlib import metadata as importlib_metadata

from .cqv import cqv
from .cv import coefficient_of_variation
from .is_numeric import is_numeric
from .method_selector import processor_dataframe_cqv, processor_dataframe_cv

# -------------------------------- function definition --------------------------------


def get_version() -> str:
    """gets the version of package"""
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()

__all__ = [
    "coefficient_of_variation",
    "is_numeric",
    "cqv",
    "processor_dataframe_cv",
    "processor_dataframe_cqv",
]
