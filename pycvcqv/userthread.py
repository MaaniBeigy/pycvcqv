"""The userthread module."""
# --------------------------- Import libraries and functions --------------------------
from typing import Optional

import multiprocessing as mp

import pandas as pd

from pycvcqv.prepare_output import prepare_cqv_datafame, prepare_cv_datafame


# -------------------------------- function definition --------------------------------
def userthread_cv_processor(
    data: pd.DataFrame,
    num_threads: Optional[int] = 1,
    ddof: Optional[int] = 1,
    skipna: Optional[bool] = True,
    ndigits: Optional[int] = 4,
    correction: Optional[bool] = False,
    multiplier: Optional[int] = 1,
) -> pd.DataFrame:
    """Performs user-defined thread cv for pd.DataFrame."""
    with mp.Pool(num_threads) as pool:
        result = prepare_cv_datafame(
            data=data,
            ddof=ddof,
            skipna=skipna,
            ndigits=ndigits,
            correction=correction,
            multiplier=multiplier,
            pool=pool,
        )
    pool.close()
    return result


def userthread_cqv_processor(
    data: pd.DataFrame,
    ndigits: Optional[int] = 4,
    interpolation: Optional[str] = "linear",
    multiplier: Optional[int] = 1,
    num_threads: Optional[int] = 1,
) -> pd.DataFrame:
    """Performs user-defined thread cqv for pd.DataFrame."""
    with mp.Pool(num_threads) as pool:
        result = prepare_cqv_datafame(
            data=data,
            ndigits=ndigits,
            interpolation=interpolation,
            multiplier=multiplier,
            pool=pool,
        )
    pool.close()
    return result
