"""Adjusted Bootstrap Percentile (BCa) CI for the cv (R `boot.ci(type='bca')`)."""

# --------------------------- Import libraries and functions --------------------------
import numpy as np
import pandas as pd

from pycvcqv._bootstrap import _bootstrap_cv_confidence_interval
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt


# -------------------------------- function definition --------------------------------
def _boot_bca_cv_confidence_interval(
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
    num_replicates: int | None = None,
    random_state: int | np.random.Generator | None = None,
) -> dict[str, float | int]:
    """Compute the BCa (bias-corrected and accelerated) bootstrap CI for the CV.

    Mirrors R `boot::boot.ci(type='bca')` with default jackknife empirical
    influence (`empinf(type='jack')`):

        z0     = qnorm( #{t* < t0} / R_finite )
        L_i    = (n - 1) * (mean(jack) - jack_i)
        a      = sum(L^3) / (6 * (sum(L^2))^(3/2))
        adj.a1 = pnorm(z0 + (z0 + z_{alpha/2})     / (1 - a*(z0 + z_{alpha/2})))
        adj.a2 = pnorm(z0 + (z0 + z_{1-alpha/2})   / (1 - a*(z0 + z_{1-alpha/2})))

    Lower/upper are then `norm.inter(sort(t*), [adj.a1, adj.a2])`.

    Args:
        data: A sequence of numeric values.
        ddof: Delta degrees of freedom for the std.
        skipna: If True, drop NaNs; if False, raise on any NaN.
        ndigits: Number of decimal digits for rounding.
        correction: Whether to apply the small-sample bias correction.
        multiplier: Multiplier applied to the reported CV and bounds.
        conf_level: Confidence level in (0, 1).
        alpha_lower: Lower-tail probability.
        alpha_upper: Upper-tail probability.
        tol: Unused (kept for API consistency).
        max_iter: Unused (kept for API consistency).
        num_replicates: Number of bootstrap resamples (default 1000).
        random_state: Optional seed or numpy `Generator` for reproducibility.

    Returns:
        Dict with keys cv, lower, upper.
    """
    _ = (tol, max_iter)
    return _bootstrap_cv_confidence_interval(
        ci_kind="bca",
        data=data,
        ddof=ddof,
        skipna=skipna,
        ndigits=ndigits,
        correction=correction,
        multiplier=multiplier,
        conf_level=conf_level,
        alpha_lower=alpha_lower,
        alpha_upper=alpha_upper,
        num_replicates=num_replicates,
        random_state=random_state,
    )
