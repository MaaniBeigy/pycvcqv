"""Confidence Intervals for Coefficient of Quartile Variation (cqv)."""

# --------------------------- Import libraries and functions --------------------------
import numpy as np

from pycvcqv.bonett import _bonett_cqv_confidence_interval
from pycvcqv.boot_basic_cqv import _boot_basic_cqv_confidence_interval
from pycvcqv.boot_bca_cqv import _boot_bca_cqv_confidence_interval
from pycvcqv.boot_norm_cqv import _boot_norm_cqv_confidence_interval
from pycvcqv.boot_perc_cqv import _boot_perc_cqv_confidence_interval
from pycvcqv.types import NumArrayLike

# Methods that consume `num_replicates`/`random_state`.
_BOOTSTRAP_METHODS: frozenset[str] = frozenset({"norm", "basic", "perc", "bca"})


# -------------------------------- function definition --------------------------------
def _cqv_confidence_intervals(
    data: NumArrayLike,
    method: str = "bonett",
    ndigits: int | None = 4,
    interpolation: str | None = "linear",
    multiplier: int | None = 1,
    skipna: bool | None = True,
    conf_level: float | None = None,
    alpha_lower: float | None = None,
    alpha_upper: float | None = None,
    num_replicates: int | None = None,
    random_state: int | np.random.Generator | None = None,
) -> dict[str, float | int]:
    """Internal function to calculate cqv with confidence intervals."""
    methods = {
        "bonett": _bonett_cqv_confidence_interval,
        "norm": _boot_norm_cqv_confidence_interval,
        "basic": _boot_basic_cqv_confidence_interval,
        "perc": _boot_perc_cqv_confidence_interval,
        "bca": _boot_bca_cqv_confidence_interval,
    }
    if method not in methods:
        raise ValueError(
            f"Unknown CQV CI method {method!r}; " f"expected one of {sorted(methods)}."
        )

    result = methods[method](
        data,
        ndigits=ndigits,
        interpolation=interpolation,
        multiplier=multiplier,
        skipna=skipna,
        conf_level=conf_level,
        alpha_lower=alpha_lower,
        alpha_upper=alpha_upper,
        num_replicates=num_replicates,
        random_state=random_state,
    )

    return {
        "cqv": float(result["cqv"]),
        "lower": float(result["lower"]),
        "upper": float(result["upper"]),
    }
