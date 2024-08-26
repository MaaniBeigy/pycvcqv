"""The prepare_output module."""

# --------------------------- Import libraries and functions --------------------------
from typing import Optional

from functools import partial

import pandas as pd

from pycvcqv.cv_confidence_interval import _cv_confidence_intervals
from pycvcqv.formulas import _cqv
from pycvcqv.types import PoolTypeT


# -------------------------------- function definition --------------------------------
def prepare_cv_datafame(
    pool: PoolTypeT,
    data: pd.DataFrame,
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
) -> pd.DataFrame:
    """Prepares result pd.DataFrame for cv."""
    data = data.select_dtypes(include="number")
    # Calculate CV and its bounds for each column
    cv_results = pool.map(
        partial(
            _cv_confidence_intervals,
            method=method,
            ddof=ddof,
            skipna=skipna,
            ndigits=ndigits,
            correction=correction,
            multiplier=multiplier,
            conf_level=conf_level,
            alpha_lower=alpha_lower,
            alpha_upper=alpha_upper,
            tol=tol,
            max_iter=max_iter,
        ),
        (pd.Series(data.loc[:, col]) for col in data.columns),
    )
    # Split the dictionary into separate columns
    result = pd.DataFrame(
        {
            "columns": data.columns,
            "cv": [res["cv"] for res in cv_results],
            "lower": [res["lower"] for res in cv_results],
            "upper": [res["upper"] for res in cv_results],
        }
    )
    return result


def prepare_cqv_datafame(
    pool: PoolTypeT,
    data: pd.DataFrame,
    ndigits: Optional[int] = 4,
    interpolation: Optional[str] = "linear",
    multiplier: Optional[int] = 1,
) -> pd.DataFrame:
    """Prepares result pd.DataFrame for cqv."""
    data = data.select_dtypes(include="number")
    result = pd.DataFrame(
        {
            "columns": data.columns,
            "cqv": pool.map(
                partial(
                    _cqv,
                    ndigits=ndigits,
                    interpolation=interpolation,
                    multiplier=multiplier,
                ),
                (pd.Series(data.loc[:, col]) for col in data.columns),
            ),
        }
    )
    return result
