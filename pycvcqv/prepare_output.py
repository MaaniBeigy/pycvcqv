"""The prepare_output module."""
# --------------------------- Import libraries and functions --------------------------
from typing import Optional

from functools import partial

import pandas as pd

from pycvcqv.formulas import _cqv, _cv
from pycvcqv.types import PoolType


# -------------------------------- function definition --------------------------------
def prepare_cv_datafame(
    pool: PoolType,
    data: pd.DataFrame,
    ddof: Optional[int] = 1,
    skipna: Optional[bool] = True,
    ndigits: Optional[int] = 4,
    correction: Optional[bool] = False,
    multiplier: Optional[int] = 1,
) -> pd.DataFrame:
    """Prepares result pd.DataFrame for cv."""
    data = data.select_dtypes(include="number")
    result = pd.DataFrame(
        {
            "columns": data.columns,
            "cv": pool.map(
                partial(
                    _cv,
                    ddof=ddof,
                    skipna=skipna,
                    ndigits=ndigits,
                    correction=correction,
                    multiplier=multiplier,
                ),
                (pd.Series(data.loc[:, col]) for col in data.columns),
            ),
        }
    )
    return result


def prepare_cqv_datafame(
    pool: PoolType,
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
