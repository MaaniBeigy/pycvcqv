"""Bootstrap helpers for the coefficient of variation.

These primitives mirror the algorithms in the R `boot` package (Canty &
Ripley) so that, given the same bootstrap distribution, the CI computations
match R bit-for-bit. The bootstrap *resampling* itself uses NumPy's RNG, so
absolute output values diverge from R's `set.seed` runs even with the
same nominal seed; the algorithms (norm/basic/perc/BCa formulas, R's
`norm.inter` quantile, jackknife acceleration) are reproduced verbatim.

Refs:
- Canty, A. & Ripley, B., `boot` R package source (R/bootfuns.q,
  R/bootpracs.q): `norm.ci`, `basic.ci`, `perc.ci`, `bca.ci`, `norm.inter`,
  `empinf` with `type="jack"`.
- Davison, A.C. & Hinkley, D.V. (1997), Bootstrap Methods and Their
  Applications, CUP.
"""

import math

# --------------------------- Import libraries and functions --------------------------
from collections.abc import Callable

import numpy as np
import pandas as pd
from numpy import typing as npt
from scipy.stats import norm as _normal

from pycvcqv.formulas import _cv
from pycvcqv.types import ArrayFloat, ArrayInt, ListFloat, ListInt, TupleFloat, TupleInt

_DEFAULT_REPLICATES: int = 1000


# -------------------------------- function definition --------------------------------
def _cv_statistic(
    sample: npt.NDArray[np.float64],
    ddof: int = 1,
    correction: bool = False,
) -> float:
    """Compute the (unscaled) coefficient of variation for a single bootstrap sample.

    Mirrors `pycvcqv.formulas._cv` but skips rounding so the bootstrap
    distribution stays at full float precision.

    Args:
        sample: 1-D float array of resampled observations.
        ddof: Delta degrees of freedom for the standard deviation.
        correction: If True, apply the small-sample bias correction used by
            `_cv` (matches R's bootstrap-of-corrected-cv path).

    Returns:
        The CV (sd/mean), or +inf if the resample's mean is at/near zero in
        the same regime as the closed-form `_cv` helper.
    """
    if sample.size == 0:
        return float("nan")
    # `np.std` with ddof >= sample.size emits a runtime warning and returns
    # NaN. R's `sd()` does the same; for the bootstrap path we just want NaN
    # downstream (the finite-mask in the CI helpers filters it out), so
    # short-circuit silently rather than letting the warning escape into code.
    if sample.size <= ddof:
        return float("nan")
    mean = float(np.mean(sample))
    std = float(np.std(sample, ddof=ddof))
    # Mirror _cv's degenerate-mean handling so bootstrap stats stay consistent
    # with the closed-form path.
    if mean == 0 or (mean < 0.000001 and std > mean):
        return float("inf")
    cv = std / mean
    if not correction:
        return cv
    length = sample.size
    # Same coefficient as in formulas._cv.
    return cv * (
        1.0
        - (1.0 / (4.0 * (length - 1)))
        + (cv**2 / length)
        + 1.0 / (2.0 * (length - 1) ** 2)
    )


def _resample_cv_replicates(
    data: npt.NDArray[np.float64],
    num_replicates: int,
    ddof: int,
    correction: bool,
    rng: np.random.Generator,
) -> npt.NDArray[np.float64]:
    """Generate `num_replicates` bootstrap CV replicates for `data`.

    Args:
        data: 1-D float array of observations (NaNs already dropped).
        num_replicates: Number of bootstrap resamples (R in R-speak).
        ddof: Delta degrees of freedom for the std.
        correction: Whether to apply small-sample bias correction.
        rng: A NumPy `Generator` for reproducibility.

    Returns:
        1-D array of bootstrap CV values, length `num_replicates` (may
        contain inf/NaN, which downstream callers filter via finite-mask).
    """
    n = data.size
    indices = rng.integers(low=0, high=n, size=(num_replicates, n))
    replicates = np.empty(num_replicates, dtype=np.float64)
    for i in range(num_replicates):
        replicates[i] = _cv_statistic(
            data[indices[i]], ddof=ddof, correction=correction
        )
    return replicates


def _jackknife_cv_replicates(
    data: npt.NDArray[np.float64],
    ddof: int,
    correction: bool,
) -> npt.NDArray[np.float64]:
    """Compute the leave-one-out (jackknife) CV replicates for `data`.

    Used to estimate the BCa acceleration constant `a` via R's `empinf`
    fallback (`type="jack"`).

    Args:
        data: 1-D float array of observations.
        ddof: Delta degrees of freedom for the std.
        correction: Whether to apply small-sample bias correction.

    Returns:
        1-D array of length n with the leave-one-out CVs.
    """
    n = data.size
    out = np.empty(n, dtype=np.float64)
    full_mask = np.ones(n, dtype=bool)
    for i in range(n):
        full_mask[i] = False
        out[i] = _cv_statistic(data[full_mask], ddof=ddof, correction=correction)
        full_mask[i] = True
    return out


def _norm_inter(
    t_sorted: npt.NDArray[np.float64],
    alphas: npt.NDArray[np.float64],
) -> npt.NDArray[np.float64]:
    """Bootstrap quantile a la R's `boot::norm.inter`.

    R's `boot.ci` does not use a plain order-statistic / linear-interp
    quantile. For each `alpha`:

        rk = (R + 1) * alpha
        k  = floor(rk)

    If `rk` is integer, return the k-th order statistic. Otherwise
    interpolate on the inverse-normal-CDF scale:

        out = t_(k) + (qnorm(alpha) - qnorm(k/(R+1)))
                    / (qnorm((k+1)/(R+1)) - qnorm(k/(R+1)))
                    * (t_(k+1) - t_(k))

    Args:
        t_sorted: 1-D ascending-sorted bootstrap replicates (already
            finite-filtered — non-finite values must be removed by the
            caller, matching R's `t <- t[is.finite(t)]`).
        alphas: 1-D array of probabilities in (0, 1).

    Returns:
        1-D array of interpolated quantiles, same length as `alphas`.
    """
    big_r = t_sorted.size
    out = np.empty(alphas.size, dtype=np.float64)
    for i, alpha in enumerate(alphas):
        rk = (big_r + 1) * float(alpha)
        k = int(math.floor(rk))
        if k <= 0:
            out[i] = t_sorted[0]
        elif k >= big_r:
            out[i] = t_sorted[big_r - 1]
        elif k == rk:
            # Integer rank; pick the k-th order stat (1-indexed in R).
            out[i] = t_sorted[k - 1]
        else:
            z_alpha = _normal.ppf(float(alpha))
            z_lower = _normal.ppf(k / (big_r + 1))
            z_upper = _normal.ppf((k + 1) / (big_r + 1))
            t_lower = t_sorted[k - 1]
            t_upper = t_sorted[k]
            out[i] = t_lower + (z_alpha - z_lower) / (z_upper - z_lower) * (
                t_upper - t_lower
            )
    return out


def _norm_bootstrap_ci(
    t0: float,
    replicates: npt.NDArray[np.float64],
    conf: float,
) -> tuple[float, float]:
    """R `boot.ci(type='norm')`: bias-corrected normal CI on the bootstrap SE."""
    finite = replicates[np.isfinite(replicates)]
    bias = float(np.mean(finite)) - t0
    # R `var(t)` is sample variance with ddof=1.
    se = float(np.std(finite, ddof=1))
    z = float(_normal.ppf((1.0 + conf) / 2.0))
    centre = t0 - bias
    return (centre - z * se, centre + z * se)


def _basic_bootstrap_ci(
    t0: float,
    replicates: npt.NDArray[np.float64],
    conf: float,
) -> tuple[float, float]:
    """R `boot.ci(type='basic')`: 2*t0 - q_(1-alpha/2), 2*t0 - q_(alpha/2)."""
    finite = np.sort(replicates[np.isfinite(replicates)])
    alphas = np.array([(1.0 - conf) / 2.0, (1.0 + conf) / 2.0], dtype=np.float64)
    qq = _norm_inter(finite, alphas)
    # R's basic.ci returns 2*t0 - q_(1-alpha/2), 2*t0 - q_(alpha/2).
    return (2.0 * t0 - qq[1], 2.0 * t0 - qq[0])


def _perc_bootstrap_ci(
    replicates: npt.NDArray[np.float64],
    conf: float,
) -> tuple[float, float]:
    """R `boot.ci(type='perc')`: raw bootstrap quantiles via norm.inter."""
    finite = np.sort(replicates[np.isfinite(replicates)])
    alphas = np.array([(1.0 - conf) / 2.0, (1.0 + conf) / 2.0], dtype=np.float64)
    qq = _norm_inter(finite, alphas)
    return (qq[0], qq[1])


def _bca_bootstrap_ci(
    t0: float,
    replicates: npt.NDArray[np.float64],
    conf: float,
    jackknife_replicates: npt.NDArray[np.float64],
) -> tuple[float, float]:
    """R `boot.ci(type='bca')` with `empinf(type='jack')` acceleration.

    Computes:
        z0     = qnorm( #{t* < t0} / R_finite )
        L_i    = (n - 1) * (mean(jackknife) - jackknife_i)
        a      = sum(L^3) / (6 * (sum(L^2))**1.5)
        adj.a1 = pnorm(z0 + (z0 + z_(alpha/2))     / (1 - a*(z0 + z_(alpha/2))))
        adj.a2 = pnorm(z0 + (z0 + z_(1-alpha/2))   / (1 - a*(z0 + z_(1-alpha/2))))

    Then `lower, upper = norm.inter(sort(t*), [adj.a1, adj.a2])`.
    """
    finite = np.sort(replicates[np.isfinite(replicates)])
    if finite.size == 0:
        raise ValueError("BCa CI requires at least one finite bootstrap replicate.")
    proportion_below = float(np.mean(finite < t0))
    if proportion_below in (0.0, 1.0):
        # qnorm(0) = -inf, qnorm(1) = +inf — R explicitly errors here.
        raise ValueError(
            "BCa estimated bias-correction 'z0' is infinite "
            "(no bootstrap replicates straddle t0). "
            "Increase R or check that the statistic is non-degenerate."
        )
    z0 = float(_normal.ppf(proportion_below))

    jack_finite = jackknife_replicates[np.isfinite(jackknife_replicates)]
    if jack_finite.size < 2:
        raise ValueError(
            "BCa acceleration requires at least 2 finite jackknife replicates."
        )
    centred = float(np.mean(jack_finite)) - jack_finite
    sum_cubed = float(np.sum(centred**3))
    sum_squared = float(np.sum(centred**2))
    if sum_squared == 0.0:
        raise ValueError("BCa acceleration is undefined (jackknife variance is zero).")
    a = sum_cubed / (6.0 * sum_squared**1.5)
    if not math.isfinite(a):
        raise ValueError("BCa estimated acceleration 'a' is not finite.")

    z_lower = float(_normal.ppf((1.0 - conf) / 2.0))
    z_upper = float(_normal.ppf((1.0 + conf) / 2.0))
    adj_alpha_lower = _normal.cdf(z0 + (z0 + z_lower) / (1.0 - a * (z0 + z_lower)))
    adj_alpha_upper = _normal.cdf(z0 + (z0 + z_upper) / (1.0 - a * (z0 + z_upper)))
    qq = _norm_inter(
        finite,
        np.array([float(adj_alpha_lower), float(adj_alpha_upper)], dtype=np.float64),
    )
    return (qq[0], qq[1])


# Type alias used by the per-method modules.
BootstrapCi = Callable[
    [float, npt.NDArray[np.float64], float],
    tuple[float, float],
]


def _resolve_conf_level(
    conf_level: float | None,
    alpha_lower: float | None,
    alpha_upper: float | None,
) -> float:
    """Resolve the bootstrap `conf` argument from pycvcqv's tri-knob API.

    The bootstrap CIs are inherently two-sided and equal-tailed (R's
    `boot.ci` only accepts a single `conf`), so when `alpha_lower` and
    `alpha_upper` disagree we take the symmetric tail mass implied by the
    larger one and warn-by-construction (matching how the closed-form
    methods collapse the two knobs onto a single alpha/2).
    """
    if conf_level is not None:
        conf = float(conf_level)
    elif alpha_lower is None and alpha_upper is None:
        conf = 0.95
    else:
        if alpha_upper is None:
            alpha_upper = alpha_lower
        if alpha_lower is None:
            alpha_lower = alpha_upper
        assert alpha_upper is not None
        conf = 1.0 - 2.0 * float(alpha_upper)

    if not 0.0 < conf < 1.0:
        raise ValueError("conf_level must be between 0 and 1.")
    return conf


def _bootstrap_cv_confidence_interval(
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
    ddof: int | None = 1,
    skipna: bool | None = True,
    ndigits: int | None = 4,
    correction: bool | None = False,
    multiplier: int | None = 1,
    conf_level: float | None = None,
    alpha_lower: float | None = None,
    alpha_upper: float | None = None,
    num_replicates: int | None = None,
    random_state: int | np.random.Generator | None = None,
) -> dict[str, float | int]:
    """Compute a bootstrap CI for the coefficient of variation.

    Mirrors the API of the other `_*_cv_confidence_interval` helpers and
    routes to the requested R `boot.ci` algorithm.

    Args:
        ci_kind: One of "norm", "basic", "perc", "bca".
        data: A sequence of numeric values.
        ddof: Delta degrees of freedom for the std.
        skipna: If True, drop NaNs; if False, raise on any NaN.
        ndigits: Number of decimal digits for rounding the returned bounds.
        correction: Whether to apply the small-sample bias correction (the
            same coefficient used by `pycvcqv.formulas._cv` is applied to
            both the point estimate and each bootstrap replicate, matching
            R's `boot_cv_corr` path).
        multiplier: Multiplier applied to the reported CV and bounds (e.g.
            100 for percent).
        conf_level: Confidence level in (0, 1). Mutually exclusive with the
            alpha knobs.
        alpha_lower: Lower-tail probability. Mutually exclusive with conf_level.
        alpha_upper: Upper-tail probability. Mutually exclusive with conf_level.
        num_replicates: Number of bootstrap resamples (R in R-speak).
            Defaults to 1000, matching the R `cvcqv` default.
        random_state: Optional seed (int) or pre-built `numpy.random.Generator`
            for reproducible draws. None ⇒ fresh non-deterministic Generator.

    Returns:
        Dict with keys cv, lower, upper.

    Raises:
        ValueError: If inputs are invalid (length, missing values when
            `skipna=False`, conf_level out of range, BCa edge cases, etc.).
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
        raise ValueError(f"Bootstrap '{ci_kind}' CI requires at least 2 observations.")

    sample_array = series.to_numpy(dtype=np.float64)

    # Reuse the closed-form _cv path so the reported point estimate honors
    # rounding/correction/multiplier exactly the way every other method does.
    calculated_cv = _cv(data, ddof, skipna, ndigits, correction, multiplier)
    if math.isinf(calculated_cv):
        return {"cv": calculated_cv, "lower": math.inf, "upper": math.inf}

    mult = 1 if multiplier is None else multiplier
    cv_internal = calculated_cv / mult

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

    ddof_int = 1 if ddof is None else int(ddof)
    correction_bool = bool(correction) if correction is not None else False

    replicates = _resample_cv_replicates(
        sample_array, num_replicates, ddof_int, correction_bool, rng
    )

    if ci_kind == "norm":
        lower_internal, upper_internal = _norm_bootstrap_ci(
            cv_internal, replicates, conf
        )
    elif ci_kind == "basic":
        lower_internal, upper_internal = _basic_bootstrap_ci(
            cv_internal, replicates, conf
        )
    elif ci_kind == "perc":
        lower_internal, upper_internal = _perc_bootstrap_ci(replicates, conf)
    else:  # bca
        jackknife = _jackknife_cv_replicates(sample_array, ddof_int, correction_bool)
        lower_internal, upper_internal = _bca_bootstrap_ci(
            cv_internal, replicates, conf, jackknife
        )

    lower_bound = round(mult * lower_internal, ndigits)
    upper_bound = round(mult * upper_internal, ndigits)

    return {
        "cv": calculated_cv,
        "lower": lower_bound,
        "upper": upper_bound,
    }
