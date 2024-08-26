"""Coefficient of Variation (cv)."""

# --------------------------- Import libraries and functions --------------------------
from typing import Any, Dict, Optional, Union

import pandas as pd

from pycvcqv.checkers import is_numeric
from pycvcqv.cv_confidence_interval import _cv_confidence_intervals
from pycvcqv.dataframe import cv_dataframe
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt

# -------------------------------- function definition --------------------------------


@is_numeric  # decorator to check whether the input vector is numeric
def coefficient_of_variation(
    data: Union[
        pd.Series,
        ArrayInt,
        ArrayFloat,
        ListFloat,
        ListInt,
        TupleFloat,
        TupleInt,
        pd.DataFrame,
    ],
    method: str = "kelley",
    ddof: Optional[int] = 1,
    skipna: Optional[bool] = True,
    ndigits: Optional[int] = 4,
    correction: Optional[bool] = False,
    multiplier: Optional[int] = 1,
    num_threads: Optional[int] = 1,
    conf_level: Optional[float] = None,
    alpha_lower: Optional[float] = None,
    alpha_upper: Optional[float] = None,
    tol: Optional[float] = 1e-9,
    max_iter: Optional[int] = 10000,
) -> Union[Dict[str, Any], pd.DataFrame]:
    """Coefficient of variation.

    Args:
        data (pandas.core.series.Series, numpy.ndarray, list, tuple, or pd.DataFrame,
            default numpy.ndarray): Having either float or integer elements. In
            dataframes, columns with numeric data will be used.
        method (str): Method for the calculation of confidence interval. By default
            `method` is "kelley".
        ddof (int, default 1): Delta Degrees of Freedom, The divisor used in
            calculations is ``N - ddof``, where ``N`` represents the number of
            elements of the data. By default `ddof` is 1.
        skipna (bool, default True): Exclude NA/null values when computing
            the result.
        ndigits (int, default 4): Indicates the number of decimal places, from
            built-in function round in module builtins.
        correction (bool, default False): To account for the sample size,
            correction might be set to True.
        multiplier (int, default 1): cv will be multiplied by it, such as 100,
            when you want to report cv as percentage.
        num_threads (int, default 1): The number of threads to use. This speeds up
            calculation for the pd.DataFrame inputs. Defaults to single thread. If -1
            is specified then multiprocessing.cpu_count() is used instead.
        conf_level (float, optional): The confidence level for the interval.
        alpha_lower (float, optional): The significance level for the lower tail.
        alpha_upper (float, optional): The significance level for the upper tail.
        tol (float, optional): Tolerance for the optimization algorithms. Default is 1e-9.
        max_iter (int, optional): Maximum number of iterations to perform. Default is 10000.


    Returns:
        Union[float, pd.DataFrame]: the coefficient(s) of variation i.e.,
            sd(x)/mean(x).

    Examples:
        .. code:: python

            >>> coefficient_of_variation(
            ...     data=pd.Series([
            ...         0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5, 4.4,
            ...         4.6, 5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9
            ...     ]),
            ...     ddof=1,
            ...     correction=False,
            ...     multiplier=100
            ... )
            57.77
    """
    # ----------------------------------- DataFrame  ----------------------------------
    if isinstance(data, pd.DataFrame):
        result = cv_dataframe(
            data=data,
            method=method,
            ddof=ddof,
            skipna=skipna,
            ndigits=ndigits,
            correction=correction,
            multiplier=multiplier,
            num_threads=num_threads,
            conf_level=conf_level,
            alpha_lower=alpha_lower,
            alpha_upper=alpha_upper,
            tol=tol,
            max_iter=max_iter,
        )
    # --------------------------------- non DataFrame  --------------------------------
    else:
        result = _cv_confidence_intervals(
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

    return result
