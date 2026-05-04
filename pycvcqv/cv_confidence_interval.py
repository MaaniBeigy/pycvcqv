"""Confidence Intervals for Coefficient of Variation (cv)."""

# --------------------------- Import libraries and functions --------------------------
import numpy as np

from pycvcqv.boot_basic import _boot_basic_cv_confidence_interval
from pycvcqv.boot_bca import _boot_bca_cv_confidence_interval
from pycvcqv.boot_norm import _boot_norm_cv_confidence_interval
from pycvcqv.boot_perc import _boot_perc_cv_confidence_interval
from pycvcqv.equal_tailed import _equal_tailed_cv_confidence_interval
from pycvcqv.kelley import _kelley_cv_confidence_interval
from pycvcqv.mahmoudvand_hassani import _mahmoudvand_hassani_cv_confidence_interval
from pycvcqv.mckay import _mckay_cv_confidence_interval
from pycvcqv.miller import _miller_cv_confidence_interval
from pycvcqv.normal_approximation import _normal_approximation_cv_confidence_interval
from pycvcqv.shortest_length import _shortest_length_cv_confidence_interval
from pycvcqv.types import NumArrayLike  # custom numeric array defined in types.py.
from pycvcqv.vangel import _vangel_cv_confidence_interval

# Methods that consume `num_replicates`/`random_state`. Closed-form methods
# don't accept these, so we route them to the dispatcher only when the kind
# is bootstrap-based.
_BOOTSTRAP_METHODS: frozenset[str] = frozenset({"norm", "basic", "perc", "bca"})

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
    num_replicates: int | None = None,
    random_state: int | np.random.Generator | None = None,
) -> dict[str, float | int]:
    """Internal function to calculate cv with confidence intervals."""
    # Closed-form methods all share the legacy 11-kwarg signature.
    closed_form_methods = {
        "kelley": _kelley_cv_confidence_interval,
        "mckay": _mckay_cv_confidence_interval,
        "miller": _miller_cv_confidence_interval,
        "vangel": _vangel_cv_confidence_interval,
        "mahmoudvand_hassani": _mahmoudvand_hassani_cv_confidence_interval,
        "equal_tailed": _equal_tailed_cv_confidence_interval,
        "normal_approximation": _normal_approximation_cv_confidence_interval,
        "shortest_length": _shortest_length_cv_confidence_interval,
    }
    # Bootstrap methods additionally take num_replicates and random_state.
    bootstrap_methods = {
        "norm": _boot_norm_cv_confidence_interval,
        "basic": _boot_basic_cv_confidence_interval,
        "perc": _boot_perc_cv_confidence_interval,
        "bca": _boot_bca_cv_confidence_interval,
    }

    if method in bootstrap_methods:
        result: dict[str, float | int] = bootstrap_methods[method](
            data,
            ddof=ddof,
            skipna=skipna,
            ndigits=ndigits,
            correction=correction,
            multiplier=multiplier,
            conf_level=conf_level,
            alpha_lower=alpha_lower,
            alpha_upper=alpha_upper,
            tol=tol,
            max_iter=max_iter,
            num_replicates=num_replicates,
            random_state=random_state,
        )
    else:
        result = closed_form_methods[method](
            data,
            ddof=ddof,
            skipna=skipna,
            ndigits=ndigits,
            correction=correction,
            multiplier=multiplier,
            conf_level=conf_level,
            alpha_lower=alpha_lower,
            alpha_upper=alpha_upper,
            tol=tol,
            max_iter=max_iter,
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
