"""Algorithm-level tests for the private bootstrap helpers."""

# --------------------------- Import libraries and functions --------------------------
import math

import numpy as np
import pytest
from scipy.stats import norm

from pycvcqv._bootstrap import (
    _basic_bootstrap_ci,
    _bca_bootstrap_ci,
    _bootstrap_cv_confidence_interval,
    _cv_statistic,
    _jackknife_cv_replicates,
    _norm_bootstrap_ci,
    _norm_inter,
    _perc_bootstrap_ci,
    _resample_cv_replicates,
    _resolve_conf_level,
)


# ------------------------------------- _cv_statistic ---------------------------------
def test_cv_statistic_matches_sd_over_mean():
    """Plain sd/mean for a non-degenerate sample."""
    sample = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    expected = float(np.std(sample, ddof=1) / np.mean(sample))
    assert _cv_statistic(sample) == pytest.approx(expected, rel=1e-12)


def test_cv_statistic_correction_applied():
    """correction=True applies the same coefficient as formulas._cv."""
    sample = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    cv = float(np.std(sample, ddof=1) / np.mean(sample))
    n = sample.size
    expected = cv * (
        1.0 - (1.0 / (4.0 * (n - 1))) + (cv**2 / n) + 1.0 / (2.0 * (n - 1) ** 2)
    )
    got = _cv_statistic(sample, correction=True)
    assert got == pytest.approx(expected, rel=1e-12)


def test_cv_statistic_returns_inf_when_mean_is_zero():
    """Mean exactly zero ⇒ +inf (mirrors formulas._cv)."""
    sample = np.array([-1.0, 1.0], dtype=np.float64)
    assert math.isinf(_cv_statistic(sample))


def test_cv_statistic_empty_sample_returns_nan():
    """Empty sample is a defensive guard; returns NaN, not raises."""
    assert math.isnan(_cv_statistic(np.array([], dtype=np.float64)))


# ------------------------------------- _norm_inter ----------------------------------
def test_norm_inter_integer_rank_returns_order_statistic():
    """When (R+1)*alpha is an integer, R's norm.inter returns t_sorted[k-1]."""
    # R = 999, alpha = 0.025 → rk = 1000 * 0.025 = 25.0 (integer)
    t_sorted = np.arange(1.0, 1000.0)  # length 999, sorted
    out = _norm_inter(t_sorted, np.array([0.025], dtype=np.float64))
    # 25th order statistic (1-indexed) → t_sorted[24] in 0-indexed terms.
    assert out[0] == pytest.approx(t_sorted[24])


def test_norm_inter_clamps_below_one_to_first():
    """rk <= 0 (alpha extremely small) ⇒ first order statistic."""
    t_sorted = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    # (5+1)*1e-6 << 1 ⇒ k = 0.
    out = _norm_inter(t_sorted, np.array([1e-6], dtype=np.float64))
    assert out[0] == 1.0


def test_norm_inter_clamps_above_r_to_last():
    """rk >= R (alpha extremely close to 1) ⇒ last order statistic."""
    t_sorted = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    out = _norm_inter(t_sorted, np.array([1.0 - 1e-9], dtype=np.float64))
    assert out[0] == 5.0


def test_norm_inter_interpolates_on_inverse_normal_scale():
    """Non-integer rk uses inverse-normal-CDF interpolation, not linear.

    Hand-compute for R=4, alpha=0.5: rk=2.5, k=2.
        z_alpha = qnorm(0.5)         = 0
        z_lower = qnorm(2/5)         = qnorm(0.4)
        z_upper = qnorm(3/5)         = qnorm(0.6)
        t_lower = t_sorted[1] = 2
        t_upper = t_sorted[2] = 3
        out = 2 + (0 - z_lower)/(z_upper - z_lower) * (3 - 2)
    """
    t_sorted = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float64)
    out = _norm_inter(t_sorted, np.array([0.5], dtype=np.float64))

    z_alpha = norm.ppf(0.5)
    z_lower = norm.ppf(2 / 5)
    z_upper = norm.ppf(3 / 5)
    expected = 2.0 + (z_alpha - z_lower) / (z_upper - z_lower) * (3.0 - 2.0)
    assert out[0] == pytest.approx(expected, rel=1e-12)


def test_norm_inter_handles_multiple_alphas():
    """Multiple alphas in one call return the corresponding interpolated quantiles."""
    t_sorted = np.arange(1.0, 1000.0)  # R=999
    alphas = np.array([0.025, 0.5, 0.975], dtype=np.float64)
    out = _norm_inter(t_sorted, alphas)
    # rk = 1000*alpha; for alpha=0.025 rk=25 (integer) → 25.
    assert out[0] == pytest.approx(25.0)
    # rk=500 (integer) → 500.
    assert out[1] == pytest.approx(500.0)
    # rk=975 (integer) → 975.
    assert out[2] == pytest.approx(975.0)


# --------------------------------- _resample_cv_replicates --------------------------
def test_resample_cv_replicates_is_deterministic_with_seed():
    """Same seed (or Generator) ⇒ identical bootstrap distribution."""
    data = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], dtype=np.float64)
    rng_a = np.random.default_rng(42)
    rng_b = np.random.default_rng(42)
    out_a = _resample_cv_replicates(data, 50, ddof=1, correction=False, rng=rng_a)
    out_b = _resample_cv_replicates(data, 50, ddof=1, correction=False, rng=rng_b)
    np.testing.assert_array_equal(out_a, out_b)


def test_resample_cv_replicates_yields_finite_values_for_positive_data():
    """All-positive input ⇒ all replicates finite (no zero-mean degeneracy)."""
    data = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], dtype=np.float64)
    rng = np.random.default_rng(0)
    replicates = _resample_cv_replicates(data, 200, ddof=1, correction=False, rng=rng)
    assert replicates.size == 200
    assert np.all(np.isfinite(replicates))


# --------------------------------- _jackknife_cv_replicates -------------------------
def test_jackknife_cv_replicates_returns_n_leave_one_out_estimates():
    """Length of jackknife replicates equals sample size; values are finite."""
    data = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], dtype=np.float64)
    jack = _jackknife_cv_replicates(data, ddof=1, correction=False)
    assert jack.size == data.size
    assert np.all(np.isfinite(jack))
    # Sanity: each entry equals the cv of (data minus one element).
    for i in range(data.size):
        without_i = np.delete(data, i)
        expected = float(np.std(without_i, ddof=1) / np.mean(without_i))
        assert jack[i] == pytest.approx(expected, rel=1e-12)


# ------------------------- _norm_bootstrap_ci (unit math check) ---------------------
def test_norm_bootstrap_ci_formula():
    """Verify (t0 - bias) ± z*SE on a hand-built bootstrap distribution.

    Use a flat replicate array so bias and SE are easy: replicates ~ N(0,1)
    with known sample mean/sd at moderate size.
    """
    rng = np.random.default_rng(123)
    replicates = rng.normal(loc=10.0, scale=2.0, size=5000)
    t0 = 10.0
    bias = float(np.mean(replicates)) - t0
    se = float(np.std(replicates, ddof=1))
    z = float(norm.ppf(0.975))
    expected_lower = (t0 - bias) - z * se
    expected_upper = (t0 - bias) + z * se

    lower, upper = _norm_bootstrap_ci(t0, replicates, conf=0.95)
    assert lower == pytest.approx(expected_lower, rel=1e-12)
    assert upper == pytest.approx(expected_upper, rel=1e-12)


# ------------------------- _basic_bootstrap_ci (unit math check) --------------------
def test_basic_bootstrap_ci_uses_pivotal_quantiles():  # noqa: D200
    """Lower = 2t0 - q_(1-alpha/2);  upper = 2t0 - q_(alpha/2)."""
    # Hand-pick replicates: 0..99, R=100. R's norm.inter on integer rk
    # (here rk = 101*0.025 ≈ 2.525, non-integer) → interpolates.
    replicates = np.arange(100.0)
    t0 = 50.0
    lower, upper = _basic_bootstrap_ci(t0, replicates, conf=0.95)
    # Compute expected via the same _norm_inter path.
    qq = _norm_inter(np.sort(replicates), np.array([0.025, 0.975], dtype=np.float64))
    assert lower == pytest.approx(2 * t0 - qq[1], rel=1e-12)
    assert upper == pytest.approx(2 * t0 - qq[0], rel=1e-12)


# ------------------------- _perc_bootstrap_ci (unit math check) ---------------------
def test_perc_bootstrap_ci_returns_quantiles_directly():
    """Lower/upper bounds equal the raw bootstrap quantiles via norm.inter."""
    replicates = np.arange(100.0)
    lower, upper = _perc_bootstrap_ci(replicates, conf=0.95)
    qq = _norm_inter(np.sort(replicates), np.array([0.025, 0.975], dtype=np.float64))
    assert lower == pytest.approx(qq[0], rel=1e-12)
    assert upper == pytest.approx(qq[1], rel=1e-12)


# -------------------------- _bca_bootstrap_ci edge cases ----------------------------
def test_bca_raises_when_no_replicate_below_t0():
    """If proportion_below = 0 ⇒ z0 = -inf ⇒ explicit raise (mirrors R)."""
    replicates = np.array([10.0, 11.0, 12.0, 13.0, 14.0])
    jackknife = np.array([8.0, 9.0, 10.0, 11.0, 12.0])
    with pytest.raises(ValueError, match="z0.*infinite"):
        _bca_bootstrap_ci(
            t0=5.0, replicates=replicates, conf=0.95, jackknife_replicates=jackknife
        )


def test_bca_raises_when_jackknife_variance_is_zero():
    """Constant jackknife ⇒ a undefined ⇒ explicit raise."""
    replicates = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
    jackknife = np.full(10, 3.0)  # zero variance
    with pytest.raises(ValueError, match="variance is zero"):
        _bca_bootstrap_ci(
            t0=5.0, replicates=replicates, conf=0.95, jackknife_replicates=jackknife
        )


def test_bca_raises_when_all_replicates_non_finite():
    """All-non-finite bootstrap distribution ⇒ defensive raise (line 251)."""
    replicates = np.array([np.nan, np.inf, -np.inf, np.nan])
    jackknife = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    with pytest.raises(ValueError, match="at least one finite bootstrap replicate"):
        _bca_bootstrap_ci(
            t0=2.5,
            replicates=replicates,
            conf=0.95,
            jackknife_replicates=jackknife,
        )


def test_bca_raises_when_jackknife_has_fewer_than_two_finite():
    """Jackknife with <2 finite values ⇒ defensive raise (line 264).

    We pick replicates that straddle t0 so the z0 guard passes first,
    leaving the jackknife-finite-count check to fire.
    """
    replicates = np.array([1.0, 2.0, 3.0, 4.0, 5.0])  # straddles t0 = 3.0
    jackknife = np.array([np.nan, np.inf, np.nan])  # zero finite values
    with pytest.raises(ValueError, match="at least 2 finite jackknife replicates"):
        _bca_bootstrap_ci(
            t0=3.0,
            replicates=replicates,
            conf=0.95,
            jackknife_replicates=jackknife,
        )


def test_bca_raises_when_acceleration_is_not_finite():
    """`a` overflowing to ±inf or NaN ⇒ defensive raise (line 274).

    With float64, jackknife values around 1e200 cause `(centred)**3` to
    overflow to ±inf, so `sum_cubed` becomes inf - inf = NaN, propagates
    to `a`, and the explicit `math.isfinite(a)` guard fires.
    """
    replicates = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    # Symmetric centred extremes ⇒ centred = [-1e200, 0, 1e200] ⇒
    # centred**3 = [-inf, 0, inf] ⇒ sum_cubed = NaN.
    jackknife = np.array([1e200, 2e200, 3e200])
    # The overflow is the *point* of this test — silence numpy's RuntimeWarning
    # so it doesn't pollute pytest output; the assertion below is the contract.
    with (
        np.errstate(over="ignore", invalid="ignore"),
        pytest.raises(ValueError, match="acceleration .a. is not finite"),
    ):
        _bca_bootstrap_ci(
            t0=3.0,
            replicates=replicates,
            conf=0.95,
            jackknife_replicates=jackknife,
        )


# ------------------------------- _resolve_conf_level --------------------------------
def test_resolve_conf_level_defaults_to_0_95_when_nothing_specified():
    """No knobs ⇒ default 0.95 confidence (matches R's boot.ci default)."""
    assert _resolve_conf_level(None, None, None) == 0.95


def test_resolve_conf_level_uses_explicit_conf_level():
    """When conf_level is given, it overrides the default."""
    assert _resolve_conf_level(0.99, None, None) == 0.99


def test_resolve_conf_level_collapses_alphas_into_symmetric_conf():
    """Bootstrap CIs are symmetric: alpha_upper=0.05 ⇒ conf = 1 - 2*0.05 = 0.9."""
    assert _resolve_conf_level(None, 0.05, 0.05) == pytest.approx(0.9, rel=1e-12)


def test_resolve_conf_level_back_fills_missing_alpha_knob():
    """Only one of alpha_lower/alpha_upper provided ⇒ the other is back-filled."""
    assert _resolve_conf_level(None, 0.025, None) == pytest.approx(0.95, rel=1e-12)
    assert _resolve_conf_level(None, None, 0.025) == pytest.approx(0.95, rel=1e-12)


def test_resolve_conf_level_rejects_out_of_range_value():
    """conf_level must be in (0, 1)."""
    with pytest.raises(ValueError, match="conf_level must be between"):
        _resolve_conf_level(1.5, None, None)


# ---------------------- _bootstrap_cv_confidence_interval edges ---------------------
def test_bootstrap_cv_confidence_interval_rejects_unknown_kind():
    """Unknown ci_kind raises a clear ValueError (defensive contract)."""
    with pytest.raises(ValueError, match="Unknown bootstrap CI kind"):
        _bootstrap_cv_confidence_interval(ci_kind="bogus", data=[1.0, 2.0, 3.0])


def test_bootstrap_cv_confidence_interval_uses_default_replicates_when_none():
    """num_replicates=None ⇒ pipeline runs with the package default of 1000."""
    result = _bootstrap_cv_confidence_interval(
        ci_kind="norm",
        data=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        multiplier=100,
        ndigits=4,
        num_replicates=None,
        random_state=2025,
    )
    assert math.isfinite(result["cv"])
    assert result["lower"] < result["cv"] < result["upper"]


def test_bootstrap_cv_confidence_interval_skipna_false_with_clean_data_succeeds():
    """skipna=False on clean (no-NaN) data takes the elif's False branch."""
    result = _bootstrap_cv_confidence_interval(
        ci_kind="perc",
        data=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        multiplier=100,
        ndigits=4,
        skipna=False,
        num_replicates=200,
        random_state=2025,
    )
    assert math.isfinite(result["cv"])
    assert result["lower"] < result["cv"] < result["upper"]
