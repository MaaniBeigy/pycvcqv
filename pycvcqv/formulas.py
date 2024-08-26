"""Formulas of cvcqv."""

# --------------------------- Import libraries and functions --------------------------
from typing import Optional  # Optional type for function arguments.

import math

import numpy as np  # To handle numeric infinity values.
import pandas as pd  # Data analysis and manipulation library.

from pycvcqv.types import NumArrayLike  # custom numeric array defined in types.py.


# -------------------------------- function definition --------------------------------
def _cv(
    data: NumArrayLike,
    ddof: Optional[int] = 1,
    skipna: Optional[bool] = True,
    ndigits: Optional[int] = 4,
    correction: Optional[bool] = False,
    multiplier: Optional[int] = 1,
) -> float:
    """Internal function to calculate cv."""
    _data: pd.Series = pd.Series(data)
    if _data.mean(skipna=skipna) == 0 or (  # check if the mean is 0
        _data.mean(skipna=skipna) < 0.000001  # check if the mean is close to 0
        # ----------------- also, check if the std is higher than mean ----------------
        and _data.std(skipna=skipna, ddof=ddof) > _data.mean(skipna=skipna)
    ):  # ------- The Inf value which comes from numpy to handle infinity cases -------
        return float(np.inf)  # to ensure that the returned infinity value is 'float'
    # ------------------ the basic coefficient of variation function ------------------
    _cv = _data.std(skipna=skipna, ddof=ddof) / _data.mean(skipna=skipna)
    _length = len(_data)  # ------------ calculate the length of input array ----------
    if correction:  # -------------------- return the corrected cv --------------------
        corrected_rounded_cv: float = round(  # ----------- round the result ----------
            multiplier  # ----------- multiply the cv e.g, 100 for percentage ---------
            * (
                _cv
                * (  # --- this is the coefficient for the correction of sample size --
                    1  # ----------- the coefficient should be less than zero ----------
                    - ((4 * (_length - 1)) ** (-1))  # ------------ 1/(4n-1) -----------
                    + ((_cv**2) * (_length ** (-1)))  # ----------- (cv^2/n) -----------
                    + (2 * ((_length - 1) ** (2))) ** (-1)  # ----- 1/2*(n-1)^2 --------
                )
            ),
            ndigits=ndigits,  # --------------- decimals for the round ----------------
        )
        return corrected_rounded_cv
    rounded_cv: float = round(  # ---------------- return the basic cv ----------------
        multiplier * (_cv),  # -------- multiply the cv e.g, 100 for percentage -------
        ndigits=ndigits,  # ------------------ decimals for the round -----------------
    )
    return rounded_cv


def _noncentral_t_parameter(
    data: NumArrayLike,
    ddof: Optional[int] = 1,
    skipna: Optional[bool] = True,
    ndigits: Optional[int] = 4,
    correction: Optional[bool] = False,
) -> float:
    """Internal function to calculate noncentral t parameter (NCP)."""
    _data: pd.Series = pd.Series(data)
    # -------------------- calculates cv based on the _cv function --------------------
    _calculated_cv = _cv(data, ddof, skipna, ndigits, correction)
    _data_length = len(_data)  # --------- calculate the length of input array --------
    ncp: float = math.sqrt(_data_length) / _calculated_cv
    return ncp


def _cqv(
    data: NumArrayLike,
    ndigits: Optional[int] = 4,
    interpolation: Optional[str] = "linear",
    multiplier: Optional[int] = 1,
) -> float:
    """Internal function to calculate cqv."""
    _data: pd.Series = pd.Series(data)
    # ---------------------- calculate the quantiles of the data ----------------------
    quantile1 = _data.quantile(0.25, interpolation=interpolation)  # q1 = p25
    quantile3 = _data.quantile(0.75, interpolation=interpolation)  # q3 = p75
    # ------------------- raise warning for 0 divisor when q3+q1 = 0 ------------------
    if quantile1 + quantile3 == 0:
        raise Warning("cqv is NaN because q3 and q1 are 0")
    _cqv = (quantile3 - quantile1) / (quantile3 + quantile1)  # ---- the basic cqv ----
    rounded_cqv: float = round(  # ------------------ return the cqv ------------------
        multiplier * _cqv,  # -------- multiply the cqv e.g, 100 for percentage -------
        ndigits=ndigits,  # ------------------ decimals for the round -----------------
    )
    return rounded_cqv
