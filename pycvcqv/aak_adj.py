"""Abu-Shawiesh, Akyuz & Kibria adjusted-degrees-of-freedom CI for the cv."""

# --------------------------- Import libraries and functions --------------------------
import math

import pandas as pd
from scipy.stats import chi2

from pycvcqv.formulas import _cv, _gamma_hat_hummel
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt


# -------------------------------- function definition --------------------------------
def _aak_adj_cv_confidence_interval(
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
    """Compute the AA&K-ADJ CI for the coefficient of variation (CV).

    Abu-Shawiesh, Aky & Kibria (2019), Eq. 21, propose a CI for the
    population CV obtained from Hummel et al.'s adjusted-degrees-of-freedom
    CI for the population variance. Given the adjusted kurtosis estimator
    gamma_hat (Abu-Shawiesh, Aky & Kibria, 2019, Eq. 5) and adjusted
    degrees of freedom

        r_hat = 2n / (gamma_hat + 2n / (n - 1))

    the (1 - alpha) * 100% CI is

        lower = sqrt(r_hat / chisq(1 - alpha/2, r_hat)) * cv
        upper = sqrt(r_hat / chisq(    alpha/2, r_hat)) * cv

    where chisq(p, df) is the p-quantile of the central chi-square
    distribution with `df` degrees of freedom. `r_hat` is generally
    non-integer; `scipy.stats.chi2.ppf` accepts non-integer `df`.

    Note: AA&K-ADJ undercovers under strong skewness in the simulation
    of Abu-Shawiesh, Aky & Kibria (2019), Tables 2-4. For symmetric data
    its average width is the narrowest among the methods compared there.

    Args:
        data: A sequence of numeric values.
        ddof: Delta degrees of freedom used in CV calculation.
        skipna: If True, ignore missing values (None/NaN). If False, raise
            if any are present.
        ndigits: Number of decimal digits for rounding outputs.
        correction: Whether to apply bias correction (kept for API
            compatibility with the other CV CI methods).
        multiplier: A multiplier applied to the reported CV and bounds
            (e.g., 100 for percent).
        conf_level: Confidence level in (0, 1). Mutually exclusive with
            alpha_lower/alpha_upper.
        alpha_lower: Lower tail probability. Mutually exclusive with
            conf_level.
        alpha_upper: Upper tail probability. Mutually exclusive with
            conf_level.
        tol: Numerical tolerance (unused; kept for API consistency).
        max_iter: Maximum iterations (unused; kept for API consistency).

    Returns:
        A dictionary with keys cv, lower, upper.

    Raises:
        ValueError: If `data` has fewer than 4 observations (needed by
            the gamma_hat denominator), if NaNs are present with
            skipna=False, or if alpha/2 is outside (0, 0.5).

    References:
        Abu-Shawiesh, M. O. A., Aky, H. E., & Kibria, B. G. (2019).
        Performance of Some Confidence Intervals for Estimating the
        Population Coefficient of Variation under both Symmetric and
        Skewed Distributions. Statistics, Optimization & Information
        Computing, 7(2), 277-290. https://doi.org/10.19139/soic.v7i2.630
    """
    _ = (tol, max_iter)
    _data: pd.Series = pd.Series(data)

    if skipna:
        _data = _data.dropna()
    elif _data.isna().any():
        raise ValueError("missing values not allowed when skipna=False")

    _length = len(_data)
    if _length < 4:
        raise ValueError("AA&K-ADJ CI requires at least 4 observations.")

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

    # ------------------------ compute AA&K-ADJ interval ------------------------------
    gamma_hat = _gamma_hat_hummel(_data, ddof=1)
    r_hat = (2.0 * _length) / (gamma_hat + 2.0 * _length / (_length - 1.0))
    if r_hat <= 0.0:
        raise ValueError(
            "AA&K-ADJ: non-positive adjusted degrees of freedom "
            f"(gamma_hat={gamma_hat!r}, r_hat={r_hat!r})."
        )

    u_high = float(chi2.ppf(1.0 - alpha_over_2, r_hat))
    u_low = float(chi2.ppf(alpha_over_2, r_hat))

    lower_bound = round(mult * (cv_internal * math.sqrt(r_hat / u_high)), ndigits)
    upper_bound = round(mult * (cv_internal * math.sqrt(r_hat / u_low)), ndigits)

    return {
        "cv": calculated_cv,
        "lower": lower_bound,
        "upper": upper_bound,
    }
