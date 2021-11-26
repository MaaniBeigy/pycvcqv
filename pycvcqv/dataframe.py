"""The dataframe module."""
# --------------------------- Import libraries and functions --------------------------
from typing import Optional

import pandas as pd

from pycvcqv.multithread import multithread_cqv_processor, multithread_cv_processor
from pycvcqv.singlethread import singlethread_cqv_processor, singlethread_cv_processor
from pycvcqv.userthread import userthread_cqv_processor, userthread_cv_processor


# -------------------------------- function definition --------------------------------
def cv_dataframe(
    data: pd.DataFrame,
    num_threads: Optional[int] = 1,
    ddof: Optional[int] = 1,
    skipna: Optional[bool] = True,
    ndigits: Optional[int] = 4,
    correction: Optional[bool] = False,
    multiplier: Optional[int] = 1,
) -> pd.DataFrame:
    """Selects method to perform cv calculations on dataframe or array-like objects."""
    operators = list(
        k
        for k, v in {
            multithread_cv_processor: -1,
            singlethread_cv_processor: 0,
            userthread_cv_processor: num_threads,
        }.items()
        if v == num_threads
    )
    return operators[0](
        data, num_threads, ddof, skipna, ndigits, correction, multiplier
    )


def cqv_dataframe(
    data: pd.DataFrame,
    ndigits: Optional[int] = 4,
    interpolation: Optional[str] = "linear",
    multiplier: Optional[int] = 1,
    num_threads: Optional[int] = 1,
) -> pd.DataFrame:
    """Selects method to perform cqv calculations on dataframe or array-like objects."""
    # ------------------------------------ threads  -----------------------------------
    operators = list(
        k
        for k, v in {
            multithread_cqv_processor: -1,
            singlethread_cqv_processor: 0,
            userthread_cqv_processor: num_threads,
        }.items()
        if v == num_threads
    )
    return operators[0](data, ndigits, interpolation, multiplier, num_threads)
