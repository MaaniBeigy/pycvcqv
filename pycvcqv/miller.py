"""Miller confidence interval."""

# --------------------------- Import libraries and functions --------------------------
from typing import Dict, Optional, Union

import math
from statistics import NormalDist

import pandas as pd

from pycvcqv.formulas import _cv
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt


# -------------------------------- function definition --------------------------------
def _miller_cv_confidence_interval(
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
    tol: Optional[float] = 1e-9,      # unused (kept for API consistency)
    max_iter: Optional[int] = 10000,  # unused (kept for API consistency)
) -> Dict[str, Union[float, int]]:
    """Compute Miller's confidence interval for the coefficient of variation (CV).

    This function calculates the confidence interval for the coefficient of
    variation using Miller's normal approximation method. The CV is computed
    internally using the project's `_cv` function, and the interval is derived
    based on an asymptotic normal approximation.

    Args:
        data (Union[pd.Series, ArrayInt, ArrayFloat, ListFloat, ListInt,
            TupleFloat, TupleInt, pd.DataFrame]):
            Input data used to compute the coefficient of variation.
            Must contain at least two non-missing observations.

        ddof (int, optional):
            Delta degrees of freedom used in standard deviation calculation.
            Defaults to 1.

        skipna (bool, optional):
            Whether to ignore missing values (NaNs). If False and missing values
            are present, a ValueError is raised. Defaults to True.

        ndigits (int, optional):
            Number of decimal places for rounding the confidence bounds.
            Defaults to 4.

        correction (bool, optional):
            Whether to apply bias correction in the internal CV calculation.
            Passed directly to `_cv`. Defaults to False.

        multiplier (int, optional):
            Scaling factor applied to the final CV and confidence bounds.
            Defaults to 1.

        conf_level (float, optional):
            Confidence level (e.g., 0.95 for a 95% confidence interval).
            If provided, `alpha_lower` and `alpha_upper` are ignored.

        alpha_lower (float, optional):
            Lower tail probability (α/2) for the confidence interval.
            Used only if `conf_level` is not provided.

        alpha_upper (float, optional):
            Upper tail probability (α/2) for the confidence interval.
            Used only if `conf_level` is not provided.

        tol (float, optional):
            Unused parameter kept for API consistency. Defaults to 1e-9.

        max_iter (int, optional):
            Unused parameter kept for API consistency. Defaults to 10000.

    Returns:
        Dict[str, Union[float, int]]:
            A dictionary containing:
                - "cv": The calculated coefficient of variation.
                - "lower": Lower bound of the confidence interval.
                - "upper": Upper bound of the confidence interval.

    Raises:
        ValueError:
            If the number of valid observations is less than 2.
            If missing values are present and `skipna=False`.
            If the derived alpha/2 is not between 0 and 0.5.

    Notes:
        - Miller's interval is based on a normal approximation and is most
          appropriate for moderate to large sample sizes.
        - If the calculated CV is infinite, both confidence bounds are
          returned as positive infinity.
        - Internally, the multiplier is removed before interval calculation
          and reapplied to the final bounds.
    """

    # unused parameters kept for API compatibility
    _ = (tol, max_iter)
    _data: pd.Series = pd.Series(data)

    if skipna:
        _data = _data.dropna()
    elif _data.isna().any():
        raise ValueError("missing values not allowed when skipna=False")

    _length = len(_data)
    if _length < 2:
        raise ValueError("Miller CI requires at least 2 observations.")

    # -------------------- get cv using internal project function ---------------------
    calculated_cv = _cv(data, ddof, skipna, ndigits, correction, multiplier)

    # If cv is infinity, return infinite bounds
    if math.isinf(calculated_cv):
        return {"cv": calculated_cv, "lower": math.inf, "upper": math.inf}

    # Remove multiplier for internal CI calculation
    mult = 1 if multiplier is None else multiplier
    cv_internal = calculated_cv / mult

    # ---------------------- determine alpha/2 from arguments -------------------------
    if conf_level is not None:
        alpha = 1.0 - float(conf_level)
        alpha_over_2 = alpha / 2.0
    else:
        if alpha_lower is None and alpha_upper is None:
            alpha_over_2 = 0.05 / 2.0
        else:
            if alpha_upper is None:
                alpha_upper = alpha_lower
            if alpha_lower is None:
                alpha_lower = alpha_upper
            alpha_over_2 = float(alpha_upper)

    if not 0.0 < alpha_over_2 < 0.5:
        raise ValueError("alpha/2 must be between 0 and 0.5.")

    # -------------------------- compute Miller interval -------------------------------
    degrees_of_freedom = _length - 1
    z_value = NormalDist().inv_cdf(1.0 - alpha_over_2)

    u_value = math.sqrt(
        (cv_internal**2 / degrees_of_freedom)
        * (0.5 + cv_internal**2)
    )

    half_width = z_value * u_value


    lower_bound = round(mult * (cv_internal - half_width), ndigits)
    upper_bound = round(mult * (cv_internal + half_width), ndigits)

    return {
        "cv": calculated_cv,
        "lower": lower_bound,
        "upper": upper_bound,
    }
