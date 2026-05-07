"""Bootstrap helpers for the coefficient of quartile variation.

Mirrors the structure of `pycvcqv._bootstrap` for the CQV statistic.
The high-level CI wrappers reuse the bias / quantile / BCa helpers from
the cv module so that R `boot::boot.ci` semantics are identical for both
statistics.

Refs:
- Canty, A. & Ripley, B., `boot` R package source: `norm.ci`,
  `basic.ci`, `perc.ci`, `bca.ci`, `norm.inter`, `empinf` (`type="jack"`).
- Davison, A.C. & Hinkley, D.V. (1997), Bootstrap Methods and Their
  Applications, CUP.
- Bonett, D.G. (2006), Confidence interval for a coefficient of quartile
  variation, Computational Statistics & Data Analysis, 50(11), 2953-7.
- Altunkaynak, B., Gamgam, H. (2018), Bootstrap confidence intervals for
  the coefficient of quartile variation, Simulation and Computation.
"""

import math

# --------------------------- Import libraries and functions --------------------------
import numpy as np
import pandas as pd
from numpy import typing as npt

from pycvcqv._bootstrap import (
    _basic_bootstrap_ci,
    _bca_bootstrap_ci,
    _norm_bootstrap_ci,
    _perc_bootstrap_ci,
    _resolve_conf_level,
)
from pycvcqv.formulas import _cqv, _cqv_statistic
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt

_DEFAULT_REPLICATES: int = 1000


# -------------------------------- function definition --------------------------------
def _resample_cqv_replicates(
    data: npt.NDArray[np.float64],
    num_replicates: int,
    interpolation: str,
    rng: np.random.Generator,
) -> npt.NDArray[np.float64]:
    """Generate `num_replicates` bootstrap CQV replicates for `data`.

    Args:
        data: 1-D float array of observations (NaNs already dropped).
        num_replicates: Number of bootstrap resamples (R in R-speak).
        interpolation: Quantile interpolation mode (matches R's type=7
            via "linear").
        rng: A NumPy `Generator` for reproducibility.

    Returns:
        1-D array of bootstrap CQV values, length `num_replicates` (may
        contain NaN, which downstream callers filter via finite-mask).
    """
    n = data.size
    indices = rng.integers(low=0, high=n, size=(num_replicates, n))
    replicates = np.empty(num_replicates, dtype=np.float64)
    for i in range(num_replicates):
        replicates[i] = _cqv_statistic(data[indices[i]], interpolation=interpolation)
    return replicates


def _jackknife_cqv_replicates(
    data: npt.NDArray[np.float64],
    interpolation: str,
) -> npt.NDArray[np.float64]:
    """Compute the leave-one-out (jackknife) CQV replicates for `data`.

    Used to estimate the BCa acceleration constant `a` via R's `empinf`
    fallback (`type="jack"`).

    Args:
        data: 1-D float array of observations.
        interpolation: Quantile interpolation mode.

    Returns:
        1-D array of length n with the leave-one-out CQVs.
    """
    n = data.size
    out = np.empty(n, dtype=np.float64)
    full_mask = np.ones(n, dtype=bool)
    for i in range(n):
        full_mask[i] = False
        out[i] = _cqv_statistic(data[full_mask], interpolation=interpolation)
        full_mask[i] = True
    return out


def _bootstrap_cqv_confidence_interval(
    ci_kind: str,
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
    """Compute a bootstrap CI for the coefficient of quartile variation.

    Mirrors R `cvcqv::CoefQuartVarCI$<norm|basic|perc|bca>_ci()`, which
    delegates to `boot::boot.ci`.

    Args:
        ci_kind: One of "norm", "basic", "perc", "bca".
        data: A sequence of numeric values.
        ndigits: Number of decimal digits for rounding outputs.
        interpolation: Quantile interpolation mode (default `"linear"`,
            matching R's `type=7`).
        multiplier: Multiplier applied to the reported CQV and bounds.
        skipna: If True, drop NaNs; if False, raise on any NaN.
        conf_level: Confidence level in (0, 1). Mutually exclusive with
            the alpha knobs.
        alpha_lower: Lower-tail probability.
        alpha_upper: Upper-tail probability.
        num_replicates: Number of bootstrap resamples (default 1000,
            matching R's `cvcqv` default).
        random_state: Optional seed (int) or pre-built numpy `Generator`.

    Returns:
        Dict with keys cqv, lower, upper.

    Raises:
        ValueError: If inputs are invalid (length, missing values when
            `skipna=False`, conf_level out of range, BCa edge cases,
            etc.).
    """
    if ci_kind not in {"norm", "basic", "perc", "bca"}:
        raise ValueError(
            f"Unknown bootstrap CI kind {ci_kind!r}; "
            "expected one of 'norm', 'basic', 'perc', 'bca'."
        )

    series: pd.Series = pd.Series(data)
    if skipna:
        series = series.dropna()
    elif series.isna().any():
        raise ValueError("missing values not allowed when skipna=False")

    length = len(series)
    if length < 2:
        raise ValueError(
            f"Bootstrap '{ci_kind}' CQV CI requires at least 2 observations."
        )

    sample_array = series.to_numpy(dtype=np.float64)

    # Reuse the closed-form _cqv path so the reported point estimate honors
    # rounding/multiplier exactly the way every other CQV method does.
    calculated_cqv = _cqv(series, ndigits, interpolation, multiplier)
    mult = 1 if multiplier is None else multiplier
    cqv_internal = calculated_cqv / mult

    conf = _resolve_conf_level(conf_level, alpha_lower, alpha_upper)

    if num_replicates is None:
        num_replicates = _DEFAULT_REPLICATES
    if num_replicates < 2:
        raise ValueError("num_replicates must be at least 2.")

    rng = (
        random_state
        if isinstance(random_state, np.random.Generator)
        else np.random.default_rng(random_state)
    )

    interp = interpolation or "linear"

    replicates = _resample_cqv_replicates(sample_array, num_replicates, interp, rng)

    if ci_kind == "norm":
        lower_internal, upper_internal = _norm_bootstrap_ci(
            cqv_internal, replicates, conf
        )
    elif ci_kind == "basic":
        lower_internal, upper_internal = _basic_bootstrap_ci(
            cqv_internal, replicates, conf
        )
    elif ci_kind == "perc":
        lower_internal, upper_internal = _perc_bootstrap_ci(replicates, conf)
    else:  # bca
        jackknife = _jackknife_cqv_replicates(sample_array, interp)
        lower_internal, upper_internal = _bca_bootstrap_ci(
            cqv_internal, replicates, conf, jackknife
        )

    if not math.isfinite(lower_internal) or not math.isfinite(upper_internal):
        return {
            "cqv": calculated_cqv,
            "lower": lower_internal,
            "upper": upper_internal,
        }

    lower_bound = round(mult * lower_internal, ndigits)
    upper_bound = round(mult * upper_internal, ndigits)

    return {
        "cqv": calculated_cqv,
        "lower": lower_bound,
        "upper": upper_bound,
    }
