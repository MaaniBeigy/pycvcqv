"""Confidence Intervals for Coefficient of Variation (cv)."""

# --------------------------- Import libraries and functions --------------------------
from pycvcqv.kelley import _kelley_cv_confidence_interval
from pycvcqv.types import NumArrayLike  # custom numeric array defined in types.py.

# -------------------------------- function definition --------------------------------


def _cv_confidence_intervals(
    data: NumArrayLike,
    method: str = "kelley",
    ddof: int | None = 1,
    skipna: bool | None = True,
    ndigits: int | None = 4,
    correction: bool | None = False,
    multiplier: int | None = 1,
    conf_level: float | None = None,
    alpha_lower: float | None = None,
    alpha_upper: float | None = None,
    tol: float | None = 1e-9,
    max_iter: int | None = 10000,
) -> dict[str, float | int]:
    """Internal function to calculate cv with confidence intervals."""
    # ------------- apply corresponding method for cv confidence intervals ------------
    methods = {
        "kelley": _kelley_cv_confidence_interval,
    }
    result: dict[str, float | int] = methods[method](
        data,
        ddof,
        skipna,
        ndigits,
        correction,
        multiplier,
        conf_level,
        alpha_lower,
        alpha_upper,
        tol,
        max_iter,
    )

    # Coerce numpy scalars to native Python floats so the public output is
    # consistent across numpy versions (numpy >=2 reprs scalars as
    # `np.float64(x)` rather than `x`, which breaks doctests and downstream
    # JSON-serialization). The return annotation already promises plain float.
    return {
        "cv": float(result["cv"]),
        "lower": float(result["lower"]),
        "upper": float(result["upper"]),
    }
