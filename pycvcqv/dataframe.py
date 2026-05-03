"""The dataframe module."""

# --------------------------- Import libraries and functions --------------------------
import pandas as pd

from pycvcqv.multithread import multithread_cqv_processor, multithread_cv_processor
from pycvcqv.singlethread import singlethread_cqv_processor, singlethread_cv_processor
from pycvcqv.types import CvProcessor
from pycvcqv.userthread import userthread_cqv_processor, userthread_cv_processor


# -------------------------------- function definition --------------------------------
def cv_dataframe(
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
    """Selects method to perform cv calculations on dataframe or array-like objects."""
    operators: list[CvProcessor] = list(
        k
        for k, v in {
            multithread_cv_processor: -1,
            singlethread_cv_processor: 0,
            userthread_cv_processor: num_threads,
        }.items()
        if v == num_threads
    )
    return operators[0](
        data,
        method,
        num_threads,
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


def cqv_dataframe(
    data: pd.DataFrame,
    ndigits: int | None = 4,
    interpolation: str | None = "linear",
    multiplier: int | None = 1,
    num_threads: int | None = 1,
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
