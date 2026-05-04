"""Shortest-Length confidence interval for the coefficient of variation."""

# --------------------------- Import libraries and functions --------------------------
import math

import pandas as pd

from pycvcqv.formulas import _cv
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt

# Tabulated (a, b) values for the Shortest-Length method, transcribed verbatim
# from the R `cvcqv` package (see CoefVarCI.R: shortest_length data.frame).
# Indexed by (alpha, v) where v = n - 1 is the degrees of freedom.
# Only alpha in {0.1, 0.05, 0.01} and v in {2..30, 40, 50, 60, 70, 80, 90, 100,
# 150, 200, 250, 300} are tabulated; for v > 300 the v=300 row is reused.
_TABULATED_V: tuple[int, ...] = (
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    40,
    50,
    60,
    70,
    80,
    90,
    100,
    150,
    200,
    250,
    300,
)

_A_BY_ALPHA: dict[float, tuple[float, ...]] = {
    0.1: (
        0.2065,
        0.5654,
        1.02,
        1.5352,
        2.093,
        2.6828,
        3.2981,
        3.9343,
        4.5883,
        5.2573,
        5.9397,
        6.6337,
        7.3382,
        8.0521,
        8.7745,
        9.5047,
        10.2421,
        10.9861,
        11.7362,
        12.4919,
        13.253,
        14.0191,
        14.7899,
        15.565,
        16.3443,
        17.1275,
        17.9144,
        18.7049,
        19.4987,
        27.5919,
        35.9012,
        44.3661,
        52.9501,
        61.629,
        70.386,
        79.2086,
        124.0372,
        169.6646,
        215.8057,
        262.3132,
    ),
    0.05: (
        0.1015,
        0.3449,
        0.6918,
        1.1092,
        1.5776,
        2.0851,
        2.6235,
        3.1874,
        3.7729,
        4.3768,
        4.9967,
        5.6308,
        6.2776,
        6.9357,
        7.6042,
        8.282,
        8.9685,
        9.6629,
        10.3647,
        11.0733,
        11.7882,
        12.5092,
        13.2357,
        13.9675,
        14.7043,
        15.4458,
        16.1917,
        16.9419,
        17.6961,
        25.4233,
        33.4085,
        41.5794,
        49.8923,
        58.3183,
        66.8374,
        75.4347,
        119.2737,
        164.0642,
        209.4667,
        255.3057,
    ),
    0.01: (
        0.02,
        0.114,
        0.2937,
        0.5461,
        0.8567,
        1.2143,
        1.6107,
        2.0394,
        2.4958,
        2.976,
        3.4771,
        3.9968,
        4.5329,
        5.084,
        5.6487,
        6.2256,
        6.8139,
        7.4126,
        8.0209,
        8.6383,
        9.264,
        9.8976,
        10.5385,
        11.1864,
        11.8408,
        12.5014,
        13.1678,
        13.8397,
        14.517,
        21.5331,
        28.8879,
        36.4863,
        44.2711,
        52.2044,
        60.2597,
        68.4177,
        110.3262,
        153.4834,
        197.444,
        241.9776,
    ),
}

_B_BY_ALPHA: dict[float, tuple[float, ...]] = {
    0.1: (
        12.5208,
        13.1532,
        14.18,
        15.3498,
        16.5807,
        17.8391,
        19.1099,
        20.3848,
        21.6598,
        22.9325,
        24.2016,
        25.4666,
        26.7269,
        27.9825,
        29.2334,
        30.4796,
        31.7212,
        32.9585,
        34.1915,
        35.4205,
        36.6455,
        37.8668,
        39.0844,
        40.2986,
        41.5095,
        42.7171,
        43.9217,
        45.1234,
        46.3222,
        58.1755,
        69.8342,
        81.3479,
        92.7487,
        104.0584,
        115.2925,
        126.4628,
        181.6128,
        235.9748,
        289.8273,
        343.3155,
    ),
    0.05: (
        15.1194,
        15.5897,
        16.5735,
        17.7432,
        18.9954,
        20.2863,
        21.5953,
        22.9118,
        24.2303,
        25.5476,
        26.8618,
        28.1717,
        29.4769,
        30.777,
        32.072,
        33.3619,
        34.6467,
        35.9266,
        37.2016,
        38.472,
        39.7379,
        40.9995,
        42.257,
        43.5105,
        44.7601,
        46.006,
        47.2483,
        48.4872,
        49.7229,
        61.9217,
        73.892,
        85.6914,
        97.3573,
        108.9153,
        120.3839,
        131.7767,
        187.9079,
        243.1025,
        297.691,
        351.8461,
    ),
    0.01: (
        20.8264,
        20.9856,
        21.8371,
        22.9867,
        24.2618,
        25.6017,
        26.9749,
        28.3643,
        29.7602,
        31.158,
        32.5543,
        33.9474,
        35.3358,
        36.7192,
        38.0968,
        39.4688,
        40.8347,
        42.1952,
        43.5498,
        44.8989,
        46.2426,
        47.581,
        48.9144,
        50.2428,
        51.5665,
        52.8856,
        54.2002,
        55.5107,
        56.8169,
        69.6808,
        82.2534,
        94.6063,
        106.7867,
        118.8272,
        130.7514,
        142.5771,
        200.6194,
        257.4375,
        313.462,
        368.9185,
    ),
}


def _lookup_ab(alpha: float, dof: int) -> tuple[float, float]:
    """Return (a, b) from the Shortest-Length table for the given alpha, v."""
    # Snap alpha to the nearest tabulated value if it's within float-precision
    # tolerance — covers cases like `1.0 - 0.95 = 0.05000000000000004`.
    matched_alpha: float | None = next(
        (a for a in _A_BY_ALPHA if math.isclose(alpha, a, abs_tol=1e-9)),
        None,
    )
    if matched_alpha is None:
        raise ValueError(
            "Shortest-Length CI is only tabulated for alpha in "
            "{0.1, 0.05, 0.01} (got %r)" % alpha
        )
    # R's behaviour: if v > 300, fall back to v = 300.
    effective_dof = 300 if dof > 300 else dof
    if effective_dof not in _TABULATED_V:
        raise ValueError(
            "Shortest-Length CI is only tabulated for v in "
            f"{{2..30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300}} "
            f"(got v = n - 1 = {dof})"
        )
    idx = _TABULATED_V.index(effective_dof)
    return _A_BY_ALPHA[matched_alpha][idx], _B_BY_ALPHA[matched_alpha][idx]


# -------------------------------- function definition --------------------------------
def _shortest_length_cv_confidence_interval(
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
    """Compute the Shortest-Length CI for the coefficient of variation (CV).

    Panichkitkosolkul (2013) proposed a CI obtained by minimizing the interval
    length, parameterized by tabulated constants (a, b) keyed on the type-I
    error rate alpha and the degrees of freedom v = n - 1:

        lower = cv * sqrt(v) / sqrt(b)
        upper = cv * sqrt(v) / sqrt(a)

    The (a, b) table is shipped with the R `cvcqv` package and only covers
    alpha in {0.1, 0.05, 0.01} and v in
    {2..30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300}; for v > 300 R
    falls back to the v = 300 row. We mirror that behavior verbatim.

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
        ValueError: If inputs are invalid, or alpha / v fall outside the
            tabulated grid.
    """

    _ = (tol, max_iter)
    _data: pd.Series = pd.Series(data)

    if skipna:
        _data = _data.dropna()
    elif _data.isna().any():
        raise ValueError("missing values not allowed when skipna=False")

    _length = len(_data)
    if _length < 2:
        raise ValueError("Shortest-Length CI requires at least 2 observations.")

    calculated_cv = _cv(data, ddof, skipna, ndigits, correction, multiplier)

    if math.isinf(calculated_cv):
        return {"cv": calculated_cv, "lower": math.inf, "upper": math.inf}

    mult = 1 if multiplier is None else multiplier
    cv_internal = calculated_cv / mult

    # ---------------------- determine alpha from arguments ---------------------------
    # The Shortest-Length table is keyed on alpha (not alpha/2). conf_level=0.95
    # therefore maps to alpha=0.05.
    if conf_level is not None:
        alpha = 1.0 - float(conf_level)
    else:
        if alpha_lower is None and alpha_upper is None:
            alpha = 0.05
        else:
            if alpha_upper is None:
                alpha_upper = alpha_lower
            if alpha_lower is None:
                alpha_lower = alpha_upper
            assert alpha_upper is not None
            # The R CoefVarCI table treats alpha as a single number, so we use
            # alpha_upper (back-filled above to equal alpha_lower) directly.
            alpha = float(alpha_upper)

    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be between 0 and 1.")

    degrees_of_freedom = _length - 1
    a_value, b_value = _lookup_ab(alpha, degrees_of_freedom)

    sqrt_dof = math.sqrt(degrees_of_freedom)

    lower_bound = round(mult * (cv_internal * sqrt_dof / math.sqrt(b_value)), ndigits)
    upper_bound = round(mult * (cv_internal * sqrt_dof / math.sqrt(a_value)), ndigits)

    return {
        "cv": calculated_cv,
        "lower": lower_bound,
        "upper": upper_bound,
    }
