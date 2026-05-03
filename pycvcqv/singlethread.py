"""The singlethread module."""

# --------------------------- Import libraries and functions --------------------------
import multiprocessing as mp

import pandas as pd

from pycvcqv.prepare_output import prepare_cqv_datafame, prepare_cv_datafame


# -------------------------------- function definition --------------------------------
def singlethread_cv_processor(
    data: pd.DataFrame,
    method: str = "kelley",
    num_threads: int | None = 1,
    ddof: int | None = 1,
    skipna: bool | None = True,
    ndigits: int | None = 4,
    correction: bool | None = False,
    multiplier: int | None = 1,
    conf_level: float | None = None,
    alpha_lower: float | None = None,
    alpha_upper: float | None = None,
    tol: float | None = 1e-9,
    max_iter: int | None = 10000,
) -> pd.DataFrame:
    """Performs single thread cv for pd.DataFrame."""
    print(num_threads)
    with mp.Pool(1) as pool:
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


def singlethread_cqv_processor(
    data: pd.DataFrame,
    ndigits: int | None = 4,
    interpolation: str | None = "linear",
    multiplier: int | None = 1,
    num_threads: int | None = 1,
) -> pd.DataFrame:
    """Performs single thread cqv for pd.DataFrame."""
    print(num_threads)
    with mp.Pool(1) as pool:
        result = prepare_cqv_datafame(
            data=data,
            ndigits=ndigits,
            interpolation=interpolation,
            multiplier=multiplier,
            pool=pool,
        )
    pool.close()
    return result
