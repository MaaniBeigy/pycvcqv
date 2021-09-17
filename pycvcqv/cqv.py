"""Coefficient of Quartile Variation (cqv)"""
# --------------------------- Import libraries and functions --------------------------
from typing import Optional, Union

import pandas as pd

from pycvcqv.check_input_type import true_input
from pycvcqv.is_numeric import is_numeric
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt

# -------------------------------- function definition --------------------------------


@true_input  # decorator to check whether the input_vector has correct type
@is_numeric  # decorator to check whether the input vector is numeric
def cqv(
    numeric_vector: Union[
        pd.Series, ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt
    ],
    ndigits: Optional[int] = 4,
    interpolation: Optional[str] = "linear",
    multiplier: Optional[int] = 1,
) -> float:
    """Coefficient of quartile variation.

    Args:
        numeric_vector (pandas.core.series.Series, numpy.ndarray, list, or
            tuple, default numpy.ndarray): An atomic vector of either float or
            integer elements.
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


    Returns:
        float: the coefficient of quartile variation for a numeric vector, i.e.,
            (q3-q1))/(q3 + q1).

    Raises:
        Warning: If q3 and q1 are 0, and the result will be NaN.

    Examples:
        .. code:: python

            >>> cqv(
            ...     numeric_vector=pd.Series([
            ...         0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5, 4.4,
            ...         4.6, 5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9
            ...     ]),
            ...     multiplier=100
            ... )
            45.625
    """
    # -------------- convert numeric_vector to pandas.core.series.Series --------------
    numeric_vector = pd.Series(numeric_vector)
    # ----------------- calculate the quantiles of the numeric_vector -----------------
    quantile1 = numeric_vector.quantile(0.25, interpolation=interpolation)  # q1 = p25
    quantile3 = numeric_vector.quantile(0.75, interpolation=interpolation)  # q3 = p75
    # ------------------- raise warning for 0 divisor when q3+q1 = 0 ------------------
    if quantile1 + quantile3 == 0:
        raise Warning("cqv is NaN because q3 and q1 are 0")
    # -------------- the basic coefficient of quartile variation function -------------
    _cqv = (quantile3 - quantile1) / (quantile3 + quantile1)
    # ----------------------- return the corrected or basic cqv -----------------------
    return round(
        multiplier * _cqv,  # -------- multiply the cqv e.g, 100 for percentage --------
        ndigits=ndigits,  # ------------------ decimals for the round -----------------
    )
