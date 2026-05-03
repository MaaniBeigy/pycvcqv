"""Miller confidence interval."""

# --------------------------- Import libraries and functions --------------------------
import math
from statistics import NormalDist

import pandas as pd

from pycvcqv.formulas import _cv
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt


# -------------------------------- function definition --------------------------------
def _miller_cv_confidence_interval(
    data: (
        pd.Series
        | ArrayInt
        | ArrayFloat
        | ListFloat
        | ListInt
        | TupleFloat
        | TupleInt
        | pd.DataFrame
    ),
    ddof: int | None = 1,
    skipna: bool | None = True,
    ndigits: int | None = 4,
    correction: bool | None = False,
    multiplier: int | None = 1,
    conf_level: float | None = None,
    alpha_lower: float | None = None,
    alpha_upper: float | None = None,
    tol: float | None = 1e-9,  # unused (kept for API consistency)
    max_iter: int | None = 10000,  # unused (kept for API consistency)
) -> dict[str, float | int]:
    """Compute Miller's confidence interval for the coefficient of variation (CV).

    Args:
        data: A sequence of numeric values.
        skipna: If True, ignore missing values (None/NaN). If False, raise if
            any are present.
        ddof: Delta degrees of freedom used in CV calculation.
        ndigits: Number of decimal digits for rounding outputs.
        correction: Whether to apply bias correction (kept for API
            compatibility).
        multiplier: A multiplier applied to the reported CV and bounds
            (e.g., 100 for percent).
        conf_level: Confidence level in (0, 1). Mutually exclusive with
            alpha_lower/alpha_upper.
        alpha_lower: Lower tail probability. Mutually exclusive with conf_level.
        alpha_upper: Upper tail probability. Mutually exclusive with conf_level.
        tol: Numerical tolerance (unused; kept for API consistency).
        max_iter: Maximum iterations (unused; kept for API consistency).

    Returns:
        A dictionary with keys:
        - cv: The coefficient of variation.
        - lower: The lower confidence bound.
        - upper: The upper confidence bound.
        - alpha_lower: Lower tail probability used.
        - alpha_upper: Upper tail probability used.
        - conf_level: Confidence level used.

    Raises:
        ValueError: If inputs are invalid (e.g., insufficient length, invalid
            alphas/conf_level, or missing values when skipna is False).
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
            # Both are guaranteed non-None after the propagation above (we got
            # here because at least one was non-None). Assert for mypy.
            assert alpha_upper is not None
            alpha_over_2 = float(alpha_upper)

    if not 0.0 < alpha_over_2 < 0.5:
        raise ValueError("alpha/2 must be between 0 and 0.5.")

    # -------------------------- compute Miller interval -------------------------------
    degrees_of_freedom = _length - 1
    z_value = NormalDist().inv_cdf(1.0 - alpha_over_2)

    u_value = math.sqrt((cv_internal**2 / degrees_of_freedom) * (0.5 + cv_internal**2))

    half_width = z_value * u_value

    lower_bound = round(mult * (cv_internal - half_width), ndigits)
    upper_bound = round(mult * (cv_internal + half_width), ndigits)

    return {
        "cv": calculated_cv,
        "lower": lower_bound,
        "upper": upper_bound,
    }
