"""Coefficient of Variation (cv)"""
# --------------------------- Import libraries and functions --------------------------
from typing import Optional, Union

import pandas as pd

from pycvcqv.check_input_type import true_input
from pycvcqv.is_numeric import is_numeric
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt

# -------------------------------- function definition --------------------------------


@true_input  # decorator to check whether the input_vector has correct type
@is_numeric  # decorator to check whether the input vector is numeric
def coefficient_of_variation(
    data: Union[
        pd.Series, ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt
    ],
    ddof: Optional[int] = 1,
    skipna: Optional[bool] = True,
    ndigits: Optional[int] = 4,
    correction: Optional[bool] = False,
    multiplier: Optional[int] = 1,
) -> float:
    """Coefficient of variation.

    Args:
        data (pandas.core.series.Series, numpy.ndarray, list, or
            tuple, default numpy.ndarray): Having either float or integer elements.
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


    Returns:
        float: the coefficient of variation for a numeric vector, i.e.,
            sd(x)/mean(x).

    Examples:
        .. code:: python

            >>> cv(
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
    # ------------------------------------ return  ------------------------------------
    result = float(_cv(data, ddof, skipna, ndigits, correction, multiplier))
    return result


@true_input  # decorator to check whether the input_vector has correct type
@is_numeric  # decorator to check whether the input vector is numeric
def _cv(
    data: Union[
        pd.Series, ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt
    ],
    ddof: Optional[int] = 1,
    skipna: Optional[bool] = True,
    ndigits: Optional[int] = 4,
    correction: Optional[bool] = False,
    multiplier: Optional[int] = 1,
) -> float:
    """Internal function to calculate cv"""
    # ------------------- convert data to pandas.core.series.Series -------------------
    data = pd.Series(data)
    # ------------------ the basic coefficient of variation function ------------------
    _cv = data.std(skipna=skipna, ddof=ddof) / data.mean(skipna=skipna)
    length = len(data)
    # ------------------------ return the corrected or basic cv -----------------------
    if correction:
        return round(  # ---------------------- round the result ----------------------
            # ---------------- multiply the cv e.g, 100 for percentage ----------------
            multiplier
            * (
                _cv
                * (
                    1
                    - ((4 * (length - 1)) ** (-1))
                    + ((_cv ** 2) * (length ** (-1)))
                    + (2 * ((length - 1) ** (2))) ** (-1)
                )
            ),
            ndigits=ndigits,  # --------------- decimals for the round ----------------
        )
    return round(  # ------------------------ round the result ------------------------
        # ------------------ multiply the cv e.g, 100 for percentage ------------------
        multiplier * (_cv),
        ndigits=ndigits,  # ------------------ decimals for the round -----------------
    )
