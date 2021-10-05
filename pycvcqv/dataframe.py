"""dataframe"""
# --------------------------- Import libraries and functions --------------------------
from typing import Optional

import multiprocessing as mp
from functools import partial

import pandas as pd

from pycvcqv.formulas import _cqv, _cv


# -------------------------------- function definition --------------------------------
def processor_cv(
    data: pd.DataFrame,
    num_threads: Optional[int] = 1,
    ddof: Optional[int] = 1,
    skipna: Optional[bool] = True,
    ndigits: Optional[int] = 4,
    correction: Optional[bool] = False,
    multiplier: Optional[int] = 1,
) -> pd.DataFrame:
    """selects method to perform cv calculations whether on dataframe or array-like
    objects
    """

    # ------------------------------------ threads  -----------------------------------
    if num_threads == -1:
        # ------------------------ multiprocessing.cpu_count() ------------------------
        with mp.Pool(mp.cpu_count()) as pool:
            # ---------------------- return only numeric columns ----------------------
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
        pool.close()
    elif num_threads in (1, 0):
        # ------------------------------ single threaded ------------------------------
        with mp.Pool(1) as pool:
            # ---------------------- return only numeric columns ----------------------
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
        pool.close()
    else:
        # ---------------------------- user-defined threads ---------------------------
        with mp.Pool(num_threads) as pool:
            # ---------------------- return only numeric columns ----------------------
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
        pool.close()
    return result


def processor_cqv(
    data: pd.DataFrame,
    ndigits: Optional[int] = 4,
    interpolation: Optional[str] = "linear",
    multiplier: Optional[int] = 1,
    num_threads: Optional[int] = 1,
) -> pd.DataFrame:
    """selects method to perform cqv calculations whether on dataframe or array-like
    objects
    """

    # ------------------------------------ threads  -----------------------------------
    if num_threads == -1:
        # ------------------------ multiprocessing.cpu_count() ------------------------
        with mp.Pool(mp.cpu_count()) as pool:
            # ---------------------- return only numeric columns ----------------------
            data = data.select_dtypes(include="number")
            result = pd.DataFrame(
                {
                    "columns": data.columns,
                    "cv": pool.map(
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
        pool.close()
    elif num_threads in (1, 0):
        # ------------------------------ single threaded ------------------------------
        with mp.Pool(1) as pool:
            # ---------------------- return only numeric columns ----------------------
            data = data.select_dtypes(include="number")
            result = pd.DataFrame(
                {
                    "columns": data.columns,
                    "cv": pool.map(
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
        pool.close()
    else:
        # ---------------------------- user-defined threads ---------------------------
        with mp.Pool(num_threads) as pool:
            # ---------------------- return only numeric columns ----------------------
            data = data.select_dtypes(include="number")
            result = pd.DataFrame(
                {
                    "columns": data.columns,
                    "cv": pool.map(
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
        pool.close()
    return result
