"""Bonett confidence interval for the coefficient of quartile variation."""

# --------------------------- Import libraries and functions --------------------------
from typing import Any, cast

import math

import numpy as np
import pandas as pd
from scipy.stats import norm as _normal

from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt


# -------------------------------- function definition --------------------------------
def _bonett_cqv_confidence_interval(
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
    ndigits: int | None = 4,
    interpolation: str | None = "linear",
    multiplier: int | None = 1,
    skipna: bool | None = True,
    conf_level: float | None = None,  # unused (kept for API consistency)
    alpha_lower: float | None = None,  # unused (kept for API consistency)
    alpha_upper: float | None = None,  # unused (kept for API consistency)
    num_replicates: int | None = None,  # unused (kept for API consistency)
    random_state: int | np.random.Generator | None = None,  # unused
) -> dict[str, float | int]:
    """Compute Bonett's centering-adjusted CI for the CQV.

    Mirrors R `cvcqv::CoefQuartVarCI$bonett_ci()`. Given the order
    statistics `Y_a, Y_b, Y_c, Y_d` with

        a = ceil(n/4 - 1.96 * sqrt(3n/16))
        b = round(n/4 + 1.96 * sqrt(3n/16))
        c = n + 1 - b
        d = n + 1 - a

    the (asymptotic) variance of `ln(D/S)` is

        f1^2 = 3 z^2 / (4 n (Y_b - Y_a)^2)
        f3^2 = 3 z^2 / (4 n (Y_d - Y_c)^2)
        v    = (1 / (16 n)) * [
                  (3/f1^2 + 3/f3^2 - 2/sqrt(f1^2 f3^2)) / D^2
                + (3/f1^2 + 3/f3^2 + 2/sqrt(f1^2 f3^2)) / S^2
                - 2 (3/f3^2 - 3/f1^2)              / (D S)
               ]

    with `D = q3 - q1`, `S = q3 + q1`. The CI on the original scale is

        exp( ln(D/S) * n/(n - 1)  ±  z * sqrt(v) )

    Note: because R's f1^2 / f3^2 carry a factor of `z^2`, the term
    `z * sqrt(v)` collapses to a constant that no longer depends on z —
    the resulting interval is effectively pinned to the 95% level baked
    into the indices via the `1.96`. `conf_level` / `alpha_*` are accepted
    for API symmetry with the bootstrap methods but do not affect output.

    Args:
        data: A sequence of numeric values.
        ndigits: Number of decimal digits for rounding outputs.
        interpolation: Quantile interpolation mode (default `"linear"`,
            matching R's `type=7`).
        multiplier: Multiplier applied to the reported CQV and bounds
            (e.g. 100 for percent).
        skipna: If True, drop NaNs; if False, raise on any NaN.
        conf_level: Unused (kept for API consistency with bootstrap CIs).
        alpha_lower: Unused (kept for API consistency).
        alpha_upper: Unused (kept for API consistency).
        num_replicates: Unused (kept for API consistency).
        random_state: Unused (kept for API consistency).

    Returns:
        Dict with keys cqv, lower, upper.

    Raises:
        ValueError: If the sample is too short (< 4 observations) or if
            the indices a/b/c/d fall outside the sample, or if `skipna`
            is False but NaNs are present.
        Warning: If q3 + q1 == 0 (CQV is undefined).
    """
    _ = (conf_level, alpha_lower, alpha_upper, num_replicates, random_state)

    series: pd.Series = pd.Series(data)
    if skipna:
        series = series.dropna()
    elif series.isna().any():
        raise ValueError("missing values not allowed when skipna=False")

    sample = np.sort(series.to_numpy(dtype=np.float64))
    n = sample.size
    if n < 4:
        raise ValueError("Bonett CQV CI requires at least 4 observations.")

    half_band = 1.96 * math.sqrt(3.0 * n / 16.0)
    a = max(1, math.ceil(n / 4.0 - half_band))
    b = round(n / 4.0 + half_band)
    c = n + 1 - b
    d = n + 1 - a
    if not 1 <= a < b <= n or not 1 <= c < d <= n:
        raise ValueError(
            "Bonett CQV CI indices fell outside the sample; "
            "n is too small for the asymptotic approximation."
        )

    method = cast(Any, interpolation or "linear")
    quantile1 = float(np.quantile(sample, 0.25, method=method))
    quantile3 = float(np.quantile(sample, 0.75, method=method))
    if quantile1 + quantile3 == 0:
        raise Warning("cqv is NaN because q3 and q1 are 0")

    cqv_internal = (quantile3 - quantile1) / (quantile3 + quantile1)

    # Match R's CoefQuartVarCI$alphastar(): the loop returns on the first
    # iteration, so alphastar = 1 - choose(n, a) * 0.25^a * 0.75^(n-a).
    star_a = math.comb(n, a) * (0.25**a) * (0.75 ** (n - a))
    alphastar = 1.0 - star_a
    zzz = float(_normal.ppf((1.0 + alphastar) / 2.0))

    y_a = sample[a - 1]
    y_b = sample[b - 1]
    y_c = sample[c - 1]
    y_d = sample[d - 1]

    f1_square = (3.0 * zzz**2) / (4.0 * n * (y_b - y_a) ** 2)
    f3_square = (3.0 * zzz**2) / (4.0 * n * (y_d - y_c) ** 2)

    big_d = quantile3 - quantile1
    big_s = quantile3 + quantile1

    cross = math.sqrt(f1_square * f3_square)
    v_var = (1.0 / (16.0 * n)) * (
        ((3.0 / f1_square + 3.0 / f3_square - 2.0 / cross) / big_d**2)
        + ((3.0 / f1_square + 3.0 / f3_square + 2.0 / cross) / big_s**2)
        - ((2.0 * (3.0 / f3_square - 3.0 / f1_square)) / (big_d * big_s))
    )

    ccc = n / (n - 1.0)
    log_ds_centred = math.log(big_d / big_s) * ccc
    half_width = zzz * math.sqrt(v_var)

    mult = 1 if multiplier is None else multiplier
    return {
        "cqv": round(mult * cqv_internal, ndigits),
        "lower": round(mult * math.exp(log_ds_centred - half_width), ndigits),
        "upper": round(mult * math.exp(log_ds_centred + half_width), ndigits),
    }
