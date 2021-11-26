"""Coefficient of Variation (cv)."""
# --------------------------- Import libraries and functions --------------------------
from typing import Optional, Union

import pandas as pd

from pycvcqv.dataframe import cv_dataframe
from pycvcqv.formulas import _cv
from pycvcqv.is_numeric import is_numeric
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
    ddof: Optional[int] = 1,
    skipna: Optional[bool] = True,
    ndigits: Optional[int] = 4,
    correction: Optional[bool] = False,
    multiplier: Optional[int] = 1,
    num_threads: Optional[int] = 1,
) -> Union[float, pd.DataFrame]:
    """Coefficient of variation.

    Args:
        data (pandas.core.series.Series, numpy.ndarray, list, tuple, or pd.DataFrame,
            default numpy.ndarray): Having either float or integer elements. In
            dataframes, columns with numeric data will be used.
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
        num_threads (int, default 1): The number of therads to use. This speeds up
            calculation for the pd.DataFrame inputs. Defaults to single thread. If -1
            is specified then multiprocessing.cpu_count() is used instead.


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
            num_threads=num_threads,
            ddof=ddof,
            skipna=skipna,
            ndigits=ndigits,
            correction=correction,
            multiplier=multiplier,
        )
    # --------------------------------- non DataFrame  --------------------------------
    else:
        result = float(_cv(data, ddof, skipna, ndigits, correction, multiplier))
    return result
