"""The multithread module."""

# --------------------------- Import libraries and functions --------------------------
from typing import Optional

import multiprocessing as mp

import pandas as pd

from pycvcqv.prepare_output import prepare_cqv_datafame, prepare_cv_datafame


# -------------------------------- function definition --------------------------------
def multithread_cv_processor(
    data: pd.DataFrame,
    method: str = "kelley",
    num_threads: Optional[int] = 1,
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
    """Performs multiprocessing cv for pd.DataFrame."""
    print(num_threads)
    with mp.Pool(mp.cpu_count()) as pool:
        result = prepare_cv_datafame(
            pool=pool,
            data=data,
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
        )
    pool.close()
    return result


def multithread_cqv_processor(
    data: pd.DataFrame,
    ndigits: Optional[int] = 4,
    interpolation: Optional[str] = "linear",
    multiplier: Optional[int] = 1,
    num_threads: Optional[int] = 1,
) -> pd.DataFrame:
    """Performs multiprocessing cqv for pd.DataFrame."""
    print(num_threads)
    with mp.Pool(mp.cpu_count()) as pool:
        result = prepare_cqv_datafame(
            data=data,
            ndigits=ndigits,
            interpolation=interpolation,
            multiplier=multiplier,
            pool=pool,
        )
    pool.close()
    return result
