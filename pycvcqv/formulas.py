"""formulas"""
# --------------------------- Import libraries and functions --------------------------
from typing import Optional, Union

import numpy as np
import pandas as pd

from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt


# -------------------------------- function definition --------------------------------
def _cv(
    data: Union[
        pd.Series, ArrayInt, ArrayFloat, ListFloat, ListInt, TupleFloat, TupleInt
    ],
    ddof: Optional[int] = 1,
    skipna: Optional[bool] = True,
    ndigits: Optional[int] = 4,
    correction: Optional[bool] = False,
    multiplier: Optional[int] = 1,
) -> float:
    """Internal function to calculate cv"""
    # ------------------- convert data to pandas.core.series.Series -------------------
    if isinstance(data, (list, np.ndarray, pd.Series, tuple)):
        data = pd.Series(data)
    else:
        raise TypeError(
            """data must be \
pandas.core.series.Series, numpy.ndarray, list, or tuple!"""
        )
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


def _cqv(
    data: Union[
        pd.Series, ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt
    ],
    ndigits: Optional[int] = 4,
    interpolation: Optional[str] = "linear",
    multiplier: Optional[int] = 1,
) -> float:
    """Internal function to calculate cqv"""
    # ------------------- convert data to pandas.core.series.Series -------------------
    data = pd.Series(data)
    # ---------------------- calculate the quantiles of the data ----------------------
    quantile1 = data.quantile(0.25, interpolation=interpolation)  # q1 = p25
    quantile3 = data.quantile(0.75, interpolation=interpolation)  # q3 = p75
    # ------------------- raise warning for 0 divisor when q3+q1 = 0 ------------------
    if quantile1 + quantile3 == 0:
        raise Warning("cqv is NaN because q3 and q1 are 0")
    # -------------- the basic coefficient of quartile variation function -------------
    _cqv = (quantile3 - quantile1) / (quantile3 + quantile1)
    # ----------------------- return the corrected or basic cqv -----------------------
    return round(
        multiplier * _cqv,  # -------- multiply the cqv e.g, 100 for percentage -------
        ndigits=ndigits,  # ------------------ decimals for the round -----------------
    )
