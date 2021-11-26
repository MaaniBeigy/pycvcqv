"""Coefficient of Quartile Variation (cqv)."""
# --------------------------- Import libraries and functions --------------------------
from typing import Optional, Union

import pandas as pd

from pycvcqv.dataframe import cqv_dataframe
from pycvcqv.formulas import _cqv
from pycvcqv.is_numeric import is_numeric
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt


# -------------------------------- function definition --------------------------------
@is_numeric  # decorator to check whether the input vector is numeric
def cqv(
    data: Union[
        pd.Series,
        ArrayFloat,
        ArrayInt,
        ListFloat,
        ListInt,
        TupleFloat,
        TupleInt,
        pd.DataFrame,
    ],
    ndigits: Optional[int] = 4,
    interpolation: Optional[str] = "linear",
    multiplier: Optional[int] = 1,
    num_threads: Optional[int] = 1,
) -> Union[pd.DataFrame, float]:
    """Coefficient of quartile variation.

    Args:
        data (pandas.core.series.Series, numpy.ndarray, list, tuple, or pd.DataFrame,
            default numpy.ndarray): Having either float or integer elements. In
            dataframes, columns with numeric data will be used.
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

    Returns:
        Union[pd.DataFrame, float]: the coefficient(s) of quartile variation.

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
        result = cqv_dataframe(
            data=data,
            num_threads=num_threads,
            ndigits=ndigits,
            interpolation=interpolation,
            multiplier=multiplier,
        )
    # --------------------------------- non DataFrame  --------------------------------
    else:
        result = float(_cqv(data, ndigits, interpolation, multiplier))
    return result
