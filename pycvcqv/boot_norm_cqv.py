"""Bootstrap normal-approximation CI for the cqv (R `boot.ci(type='norm')`)."""

# --------------------------- Import libraries and functions --------------------------
import numpy as np
import pandas as pd

from pycvcqv._cqv_bootstrap import _bootstrap_cqv_confidence_interval
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt


# -------------------------------- function definition --------------------------------
def _boot_norm_cqv_confidence_interval(
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
    conf_level: float | None = None,
    alpha_lower: float | None = None,
    alpha_upper: float | None = None,
    num_replicates: int | None = None,
    random_state: int | np.random.Generator | None = None,
) -> dict[str, float | int]:
    """Compute the bootstrap normal-approximation CI for the CQV.

    Mirrors R `boot::boot.ci(type="norm")`. Given bootstrap replicates t*
    of the cqv statistic and the original-sample estimate t0:

        bias  = mean(t*) - t0
        SE    = sd(t*)        # sample sd, ddof=1
        z     = qnorm((1 + conf) / 2)
        lower = (t0 - bias) - z * SE
        upper = (t0 - bias) + z * SE

    Args:
        data: A sequence of numeric values.
        ndigits: Number of decimal digits for rounding outputs.
        interpolation: Quantile interpolation mode (default `"linear"`,
            matching R's `type=7`).
        multiplier: Multiplier applied to the reported CQV and bounds.
        skipna: If True, drop NaNs; if False, raise on any NaN.
        conf_level: Confidence level in (0, 1).
        alpha_lower: Lower-tail probability.
        alpha_upper: Upper-tail probability.
        num_replicates: Number of bootstrap resamples (default 1000).
        random_state: Optional seed or numpy `Generator` for reproducibility.

    Returns:
        Dict with keys cqv, lower, upper.
    """
    return _bootstrap_cqv_confidence_interval(
        ci_kind="norm",
        data=data,
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
