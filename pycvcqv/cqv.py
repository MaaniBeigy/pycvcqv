"""Coefficient of Quartile Variation (cqv)."""

# --------------------------- Import libraries and functions --------------------------
from typing import Any

import numpy as np
import pandas as pd

from pycvcqv.checkers import is_numeric
from pycvcqv.cqv_confidence_interval import _cqv_confidence_intervals
from pycvcqv.dataframe import cqv_dataframe
from pycvcqv.formulas import _cqv
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt


# -------------------------------- function definition --------------------------------
@is_numeric  # decorator to check whether the input vector is numeric
def cqv(
    data: (
        pd.Series
        | ArrayFloat
        | ArrayInt
        | ListFloat
        | ListInt
        | TupleFloat
        | TupleInt
        | pd.DataFrame
    ),
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
) -> dict[str, Any] | pd.DataFrame | float:
    """Coefficient of quartile variation.

    Args:
        data (pandas.core.series.Series, numpy.ndarray, list, tuple, or pd.DataFrame,
            default numpy.ndarray): Having either float or integer elements. In
            dataframes, columns with numeric data will be used.
        method (str, optional): Confidence-interval method. One of
            "bonett", "norm", "basic", "perc", "bca". When `None` (default)
            only the point estimate is returned.
        ndigits (int, default 4): Indicates the number of decimal places, from
            built-in function round in module builtins.
        interpolation (str, default 'linear'): It specifies the interpolation method to
            use, when the desired quantile lies between two data points `i` and `j`:
            * linear: `i + (j - i) * fraction`, where `fraction` is the
              fractional part of the index surrounded by `i` and `j`.
            * lower: `i`.
            * higher: `j`.
            * nearest: `i` or `j` whichever is nearest.
            * midpoint: (`i` + `j`) / 2.
        multiplier (int, default 1): cqv will be multiplied by it, such as 100,
            when you want to report cqv as percentage.
        num_threads (int, default 1): The number of therads to use. This speeds up
            calculation for the pd.DataFrame inputs. Defaults to single thread. If -1
            is specified then multiprocessing.cpu_count() is used instead.
        skipna (bool, default True): Exclude NA/null values when computing the
            result. Only consumed by the CI methods.
        conf_level (float, optional): Confidence level for the interval (e.g. 0.95).
            Only consumed by the bootstrap methods.
        alpha_lower (float, optional): Lower-tail probability.
        alpha_upper (float, optional): Upper-tail probability.
        num_replicates (int, optional): Number of bootstrap resamples (R in
            R-speak). Only consumed by the bootstrap-based methods. Defaults to 1000.
        random_state (int or numpy.random.Generator, optional): Seed or
            pre-built `numpy.random.Generator` for reproducible bootstrap draws.
            Only consumed by the bootstrap-based methods.

    Returns:
        Union[float, pd.DataFrame, dict]: When `method` is None, the
            point estimate (or a 2-column DataFrame for DataFrame input).
            When `method` is given, a dict with cqv/lower/upper (or a
            4-column DataFrame for DataFrame input).

    Examples:
        .. code:: python

            >>> cqv(
            ...     data=pd.Series([
            ...         0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5, 4.4,
            ...         4.6, 5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9
            ...     ]),
            ...     multiplier=100
            ... )
            45.625
    """
    # ----------------------------------- DataFrame  ----------------------------------
    if isinstance(data, pd.DataFrame):
        result: dict[str, Any] | pd.DataFrame | float = cqv_dataframe(
            data=data,
            method=method,
            num_threads=num_threads,
            ndigits=ndigits,
            interpolation=interpolation,
            multiplier=multiplier,
            skipna=skipna,
            conf_level=conf_level,
            alpha_lower=alpha_lower,
            alpha_upper=alpha_upper,
            num_replicates=num_replicates,
            random_state=random_state,
        )
    # --------------------------------- non DataFrame  --------------------------------
    elif method is None:
        result = float(_cqv(data, ndigits, interpolation, multiplier))
    else:
        result = _cqv_confidence_intervals(
            data=data,
            method=method,
            ndigits=ndigits,
            interpolation=interpolation,
            multiplier=multiplier,
            skipna=skipna,
            conf_level=conf_level,
            alpha_lower=alpha_lower,
            alpha_upper=alpha_upper,
            num_replicates=num_replicates,
            random_state=random_state,
        )
    return result
