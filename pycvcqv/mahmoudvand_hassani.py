"""Mahmoudvand-Hassani confidence interval for the coefficient of variation."""

# --------------------------- Import libraries and functions --------------------------
import math
from statistics import NormalDist

import pandas as pd

from pycvcqv.formulas import _cv
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt


# -------------------------------- function definition --------------------------------
def _mahmoudvand_hassani_cv_confidence_interval(
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
    """Compute Mahmoudvand-Hassani's CI for the coefficient of variation (CV).

    Mahmoudvand and Hassani (2009) proposed a CI based on ranked-set sampling
    that uses a closed-form correction factor C_n. With n the sample size,
    alpha the type-I error rate and z = qnorm(alpha/2):

        C_n   = sqrt(2/(n - 1)) * gamma(n/2) / gamma((n - 1)/2)
        u_low = 2 - (C_n + z * sqrt(1 - C_n^2))
        u_up  = 2 - (C_n - z * sqrt(1 - C_n^2))
        lower = cv / u_low
        upper = cv / u_up

    For n > 340 R falls back to lgamma() to avoid gamma() overflow; we mirror
    that fallback verbatim so the outputs stay byte-aligned with the R
    package, even though lgamma()/lgamma() is not the asymptotically correct
    substitution. Math ported from the R `cvcqv` package.

    Args:
        data: A sequence of numeric values.
        ddof: Delta degrees of freedom used in CV calculation.
        skipna: If True, ignore missing values (None/NaN). If False, raise if
            any are present.
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
        A dictionary with keys cv, lower, upper.

    Raises:
        ValueError: If inputs are invalid (e.g., insufficient length, missing
            values when skipna is False, or alpha/2 outside (0, 0.5)).
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
        raise ValueError("Mahmoudvand-Hassani CI requires at least 2 observations.")

    # -------------------- get cv using internal project function ---------------------
    calculated_cv = _cv(data, ddof, skipna, ndigits, correction, multiplier)

    if math.isinf(calculated_cv):
        return {"cv": calculated_cv, "lower": math.inf, "upper": math.inf}

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
            assert alpha_upper is not None
            alpha_over_2 = float(alpha_upper)

    if not 0.0 < alpha_over_2 < 0.5:
        raise ValueError("alpha/2 must be between 0 and 0.5.")

    # ---------------------- compute Mahmoudvand-Hassani interval ---------------------
    # gamma() is finite for n <= 340; for larger n, R uses lgamma() (note this
    # changes the answer because lgamma()/lgamma() is not gamma()/gamma(); we
    # preserve R's exact behavior).
    if _length <= 340:
        c_n = math.sqrt(2.0 / (_length - 1)) * (
            math.gamma(_length / 2.0) / math.gamma((_length - 1) / 2.0)
        )
    else:
        c_n = math.sqrt(2.0 / (_length - 1)) * (
            math.lgamma(_length / 2.0) / math.lgamma((_length - 1) / 2.0)
        )

    z_lower = NormalDist().inv_cdf(alpha_over_2)
    rss_radical = math.sqrt(1.0 - c_n**2)

    u_lower = 2.0 - (c_n + z_lower * rss_radical)
    u_upper = 2.0 - (c_n - z_lower * rss_radical)

    lower_bound = round(mult * (cv_internal / u_lower), ndigits)
    upper_bound = round(mult * (cv_internal / u_upper), ndigits)

    return {
        "cv": calculated_cv,
        "lower": lower_bound,
        "upper": upper_bound,
    }
