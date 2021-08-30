# type: ignore[attr-defined]
"""Coefficient of Variation (CV) and Coefficient of Quartile Variation (CQV)
with Confidence Intervals (CI)"""

import sys
from importlib import metadata as importlib_metadata

from .check_input_type import true_input
from .cqv import cqv
from .cv import cv
from .is_numeric import is_numeric


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()

__all__ = ["cv", "is_numeric", "true_input", "cqv"]
