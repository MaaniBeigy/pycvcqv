"""The dataframe module."""

# --------------------------- Import libraries and functions --------------------------
import numpy as np
import pandas as pd

from pycvcqv.multithread import multithread_cqv_processor, multithread_cv_processor
from pycvcqv.singlethread import singlethread_cqv_processor, singlethread_cv_processor
from pycvcqv.types import CqvProcessor, CvProcessor
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
    num_replicates: int | None = None,
    random_state: int | np.random.Generator | None = None,
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
        num_replicates,
        random_state,
    )


def cqv_dataframe(
    data: pd.DataFrame,
    method: str | None = None,
    ndigits: int | None = 4,
    interpolation: str | None = "linear",
    multiplier: int | None = 1,
    num_threads: int | None = 1,
    skipna: bool | None = True,
    conf_level: float | None = None,
    alpha_lower: float | None = None,
    alpha_upper: float | None = None,
    num_replicates: int | None = None,
    random_state: int | np.random.Generator | None = None,
) -> pd.DataFrame:
    """Selects method to perform cqv calculations on dataframe or array-like objects."""
    # ------------------------------------ threads  -----------------------------------
    operators: list[CqvProcessor] = list(
        k
        for k, v in {
            multithread_cqv_processor: -1,
            singlethread_cqv_processor: 0,
            userthread_cqv_processor: num_threads,
        }.items()
        if v == num_threads
    )
    return operators[0](
        data,
        method,
        ndigits,
        interpolation,
        multiplier,
        num_threads,
        skipna,
        conf_level,
        alpha_lower,
        alpha_upper,
        num_replicates,
        random_state,
    )
