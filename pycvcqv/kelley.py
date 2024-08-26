"""Kelley confidence interval."""

# --------------------------- Import libraries and functions --------------------------
from typing import Dict, Optional, Union  # Optional type for function arguments.

import math

import pandas as pd  # Data analysis and manipulation library.

from pycvcqv.formulas import _cv, _noncentral_t_parameter
from pycvcqv.noncentralt import conf_limits_nct
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt


# -------------------------------- function definition --------------------------------
def _kelley_cv_confidence_interval(
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
    conf_level: Optional[float] = None,
    alpha_lower: Optional[float] = None,
    alpha_upper: Optional[float] = None,
    tol: Optional[float] = 1e-9,
    max_iter: Optional[int] = 10000,
) -> Dict[str, Union[float, int]]:
    """Calculates Kelley's confidence interval for the coefficient of variation.

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
        conf_level (float, optional): The confidence level for the interval.
        alpha_lower (float, optional): The significance level for the lower tail.
        alpha_upper (float, optional): The significance level for the upper tail.
        tol (float, optional): Tolerance for the optimization algorithms. Default is 1e-9.
        max_iter (int, optional): Maximum number of iterations to perform. Default is 10000.

    Returns:
        dict: A dictionary with the following keys:
            - lower_limit (float): Lower confidence limit for the NCP.
            - upper_limit (float): Upper confidence limit for the NCP.

    """
    _data: pd.Series = pd.Series(data)
    # ----------------------- calculates noncentral t parameter -----------------------
    _ncp = _noncentral_t_parameter(data, ddof, skipna, ndigits, correction)
    _data_length = len(_data)  # --------- calculate the length of input array --------
    _dof = _data_length - 1  # ----------- calculate the degrees of freedom -----------
    _ncp_confidence_limits = conf_limits_nct(
        ncp=_ncp,
        dof=_dof,
        conf_level=conf_level,
        alpha_lower=alpha_lower,
        alpha_upper=alpha_upper,
        tol=tol,
        max_iter=max_iter,
    )
    # ---------------------- calculates coefficient of variation ----------------------
    calculated_cv: float = _cv(data, ddof, skipna, ndigits, correction, multiplier)
    # --------------------- calculates lower/upper tiles of Kelley --------------------
    multiplier = multiplier if multiplier is not None else 1
    lower_bound: float = round(
        multiplier * (math.sqrt(_data_length) / _ncp_confidence_limits["upper_limit"]),
        ndigits,
    )
    upper_bound: float = round(
        multiplier * (math.sqrt(_data_length) / _ncp_confidence_limits["lower_limit"]),
        ndigits,
    )
    return {"cv": calculated_cv, "lower": lower_bound, "upper": upper_bound}
