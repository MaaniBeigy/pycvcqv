"""Abu-Shawiesh, Akyuz & Kibria augmented-large-sample CI for the cv."""

# --------------------------- Import libraries and functions --------------------------
import math
from statistics import NormalDist

import pandas as pd

from pycvcqv.formulas import _cv, _kappa_e5
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt


# -------------------------------- function definition --------------------------------
def _aak_als_cv_confidence_interval(
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
    """Compute the AA&K-ALS CI for the coefficient of variation (CV).

    Abu-Shawiesh, Aky & Kibria (2019), Eq. 32, propose a CI for the
    population CV obtained from Burch's augmented-large-sample CI for the
    population variance. The construction uses the three-term Taylor
    expansion of log(S**2): kappa_e5 (Abu-Shawiesh, Aky & Kibria, 2019,
    Eq. 13), and

        K = kappa_e5 + 2n / (n - 1)
        B = (K / n) * (1 + K / (2n))      # variance of log(S^2)
        C = K / (2n)                       # bias of log(S^2)

    The (1 - alpha) * 100% CI is

        lower = cv * sqrt(exp(-z * sqrt(B) + C))
        upper = cv * sqrt(exp(+z * sqrt(B) + C))

    where z = qnorm(1 - alpha/2). The constant `C` is a bias-correction
    term *added on the log scale outside the radical over B*, not a
    variance term combined with B under the radical: B is the variance
    of log(S**2) and C is the (negative of the) bias of log(S**2), as
    Abu-Shawiesh, Aky & Kibria (2019), Eq. 11 makes explicit.

    Per Abu-Shawiesh, Aky & Kibria (2019), Tables 2-4, AA&K-ALS gives
    the closest coverage to the nominal level across both symmetric and
    skewed distributions, at the cost of a slightly wider interval than
    AA&K-LS.

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
        ValueError: If `data` has fewer than 4 observations (needed by the
            G_2 / kappa_e5 denominator), if NaNs are present with
            skipna=False, or if alpha/2 is outside (0, 0.5). `B` is
            always non-negative for n >= 4 because kappa_e5
            (Abu-Shawiesh, Aky & Kibria, 2019, Eq. 13) has a minimum
            of approximately -(n+1)/(20(n-1)), which never falls below
            -2n/(n-1) and so K = kappa_e5 + 2n/(n-1) stays positive.

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
        raise ValueError("AA&K-ALS CI requires at least 4 observations.")

    calculated_cv = _cv(data, ddof, skipna, ndigits, correction, multiplier)

    if math.isinf(calculated_cv):
        return {"cv": calculated_cv, "lower": math.inf, "upper": math.inf}

    mult = 1 if multiplier is None else multiplier
    cv_internal = calculated_cv / mult

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

    # ------------------------ compute AA&K-ALS interval ------------------------------
    # B = (K/n)(1 + K/(2n)) is always non-negative for real data with
    # n >= 4. Proof: g_2 has its minimum -2 at fully bimodal data;
    # kappa_e5(G_2) is a quadratic in G_2 with minimum ((n+1)/(n-1)) *
    # (-n/20) >= -n/5 in magnitude, never below -2n/(n-1); so K stays
    # positive and B with it.
    kappa = _kappa_e5(_data)
    k_value = kappa + 2.0 * _length / (_length - 1.0)
    b_value = (k_value / _length) * (1.0 + k_value / (2.0 * _length))
    c_value = k_value / (2.0 * _length)

    z_score = NormalDist().inv_cdf(1.0 - alpha_over_2)
    radical = z_score * math.sqrt(b_value)

    lower_bound = round(
        mult * (cv_internal * math.sqrt(math.exp(-radical + c_value))), ndigits
    )
    upper_bound = round(
        mult * (cv_internal * math.sqrt(math.exp(+radical + c_value))), ndigits
    )

    return {
        "cv": calculated_cv,
        "lower": lower_bound,
        "upper": upper_bound,
    }
