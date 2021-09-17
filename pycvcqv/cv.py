"""Coefficient of Variation (cv)"""
# --------------------------- Import libraries and functions --------------------------
from typing import List, Optional, Tuple, Union

import numpy as np
import numpy.typing as npt
import pandas as pd

from .check_input_type import true_input
from .is_numeric import is_numeric

# ---------------------------------- types definition ---------------------------------
ListFloat = List[float]
ListInt = List[int]
TupleFloat = Tuple[float]
TupleInt = Tuple[int]
ArrayFloat = npt.NDArray[np.float_]
ArrayInt = npt.NDArray[np.int_]

# -------------------------------- function definition --------------------------------


@true_input  # decorator to check whether the input_vector has correct type
@is_numeric  # decorator to check whether the input vector is numeric
def coefficient_of_variation(
    numeric_vector: Union[
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
        numeric_vector (pandas.core.series.Series, numpy.ndarray, list, or
            tuple, default numpy.ndarray): An atomic vector of either float or
            integer elements.
        ddof (int, default 1): Delta Degrees of Freedom, The divisor used in
            calculations is ``N - ddof``, where ``N`` represents the number of
            elements of the numeric_vector. By default `ddof` is 1.
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
            ...     numeric_vector=pd.Series([
            ...         0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5, 4.4,
            ...         4.6, 5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9
            ...     ]),
            ...     ddof=1,
            ...     correction=False,
            ...     multiplier=100
            ... )
            57.77
    """
    # -------------- convert numeric_vector to pandas.core.series.Series --------------
    numeric_vector = pd.Series(numeric_vector)
    # ------------------ the basic coefficient of variation function ------------------
    _cv = numeric_vector.std(  # -------------- std in pandas.core.generic -------------
        skipna=skipna,  # ------------------- Exclude NA/null values ------------------
        ddof=ddof,  # -------------------- Delta Degrees of Freedom -------------------
        # ------------- mean in pandas.core.generic -------------
    ) / numeric_vector.mean(
        skipna=skipna  # ------------------- Exclude NA/null values -------------------
    )

    # ------------------------ the length of the numeric_vector -----------------------
    length = len(numeric_vector)
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
            ndigits=ndigits,  # --------------- decimals for the round ---------------
        )
    return round(  # ---------------------- round the result ----------------------
        # ---------------- multiply the cv e.g, 100 for percentage ----------------
        multiplier * (_cv),
        ndigits=ndigits,  # ---------------- decimals for the round ---------------
    )
