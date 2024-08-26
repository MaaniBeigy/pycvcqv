"""Confidence Intervals for Coefficient of Variation (cv)."""

# --------------------------- Import libraries and functions --------------------------
from typing import Dict, Optional, Union  # Optional type for function arguments.

from pycvcqv.kelley import _kelley_cv_confidence_interval
from pycvcqv.types import NumArrayLike  # custom numeric array defined in types.py.

# -------------------------------- function definition --------------------------------


def _cv_confidence_intervals(
    data: NumArrayLike,
    method: str = "kelley",
    ddof: Optional[int] = 1,
    skipna: Optional[bool] = True,
    ndigits: Optional[int] = 4,
    correction: Optional[bool] = False,
    multiplier: Optional[int] = 1,
    conf_level: Optional[float] = None,
    alpha_lower: Optional[float] = None,
    alpha_upper: Optional[float] = None,
    tol: Optional[float] = 1e-9,
    max_iter: Optional[int] = 10000,
) -> Dict[str, Union[float, int]]:
    """Internal function to calculate cv with confidence intervals."""
    # ------------- apply corresponding method for cv confidence intervals ------------
    methods = {
        "kelley": _kelley_cv_confidence_interval,
    }
    result: Dict[str, Union[float, int]] = methods[method](
        data,
        ddof,
        skipna,
        ndigits,
        correction,
        multiplier,
        conf_level,
        alpha_lower,
        alpha_upper,
        tol,
        max_iter,
    )

    return {
        "cv": result["cv"],
        "lower": result["lower"],
        "upper": result["upper"],
    }
