"""Tests for the bootstrap normal-approximation CI for the cqv (`method='norm'`)."""

# --------------------------- Import libraries and functions --------------------------
import numpy as np
import pandas as pd
import pytest

from pycvcqv.boot_norm_cqv import _boot_norm_cqv_confidence_interval
from pycvcqv.cqv import cqv

# Canonical 20-point R `cvcqv` example. The R README reports 95% CI:
#   norm  45.625  19.957  70.840
# Bootstrap CIs depend on the RNG seed, and Python/numpy's default_rng is
# not bit-compatible with R's set.seed Mersenne Twister stream, so we use
# a *ballpark* tolerance against the README and rely on fixed-seed
# Python-side reproducibility for the rest of the assertions.
REFERENCE_DATA = [
    0.2,
    0.5,
    1.1,
    1.4,
    1.8,
    2.3,
    2.5,
    2.7,
    3.5,
    4.4,
    4.6,
    5.4,
    5.4,
    5.7,
    5.8,
    5.9,
    6.0,
    6.6,
    7.1,
    7.9,
]


def test_boot_norm_cqv_in_ballpark_of_r_reference():
    """With R=10000, the norm-bootstrap CI sits within a few percent of R."""
    result = cqv(
        data=REFERENCE_DATA,
        method="norm",
        multiplier=100,
        ndigits=3,
        num_replicates=10000,
        random_state=42,
    )
    assert result["cqv"] == pytest.approx(45.625, abs=1e-6)
    assert result["lower"] == pytest.approx(19.957, abs=2.5)
    assert result["upper"] == pytest.approx(70.840, abs=2.5)


def test_boot_norm_cqv_is_reproducible_with_random_state():
    """Same `random_state` ⇒ identical CI bounds."""
    a = _boot_norm_cqv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, num_replicates=500, random_state=7
    )
    b = _boot_norm_cqv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, num_replicates=500, random_state=7
    )
    assert a == b


def test_boot_norm_cqv_accepts_external_generator():
    """A pre-built numpy Generator works the same as an int seed of the same value."""
    gen_a = np.random.default_rng(123)
    gen_b = np.random.default_rng(123)
    via_gen = _boot_norm_cqv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, num_replicates=400, random_state=gen_a
    )
    via_int = _boot_norm_cqv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, num_replicates=400, random_state=gen_b
    )
    assert via_gen == via_int


def test_boot_norm_cqv_with_pandas_series_matches_list():
    """A pd.Series input produces the same result as a plain list (same seed)."""
    list_result = cqv(
        data=REFERENCE_DATA,
        method="norm",
        multiplier=100,
        num_replicates=200,
        random_state=1,
    )
    series_result = cqv(
        data=pd.Series(REFERENCE_DATA),
        method="norm",
        multiplier=100,
        num_replicates=200,
        random_state=1,
    )
    assert list_result == series_result


def test_boot_norm_cqv_bounds_bracket_the_point_estimate():
    """The CI must contain the point estimate."""
    result = _boot_norm_cqv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, num_replicates=500, random_state=2
    )
    assert result["lower"] < result["cqv"] < result["upper"]


def test_boot_norm_cqv_narrower_at_lower_confidence():
    """Lower confidence level (wider alpha) yields a narrower CI."""
    cqv_95 = _boot_norm_cqv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        conf_level=0.95,
        num_replicates=2000,
        random_state=99,
    )
    cqv_80 = _boot_norm_cqv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        conf_level=0.80,
        num_replicates=2000,
        random_state=99,
    )
    assert (cqv_80["upper"] - cqv_80["lower"]) < (cqv_95["upper"] - cqv_95["lower"])


def test_boot_norm_cqv_skipna_drops_nans():
    """skipna=True (default) silently drops NaN entries."""
    data_with_nan = [*REFERENCE_DATA, float("nan"), float("nan")]
    with_nans = _boot_norm_cqv_confidence_interval(
        data=data_with_nan, multiplier=100, num_replicates=200, random_state=5
    )
    without_nans = _boot_norm_cqv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, num_replicates=200, random_state=5
    )
    assert with_nans == without_nans


def test_boot_norm_cqv_skipna_false_raises_on_nan():
    """skipna=False raises if NaNs are present."""
    data_with_nan = [*REFERENCE_DATA, float("nan")]
    with pytest.raises(ValueError, match="missing values"):
        _boot_norm_cqv_confidence_interval(
            data=data_with_nan, multiplier=100, skipna=False
        )


def test_boot_norm_cqv_too_short_raises():
    """Bootstrap norm CQV CI requires at least 2 observations."""
    with pytest.raises(ValueError, match="at least 2 observations"):
        _boot_norm_cqv_confidence_interval(data=[1.0], multiplier=100)


def test_boot_norm_cqv_invalid_conf_level_raises():
    """conf_level outside (0, 1) is rejected."""
    with pytest.raises(ValueError, match="conf_level must be between"):
        _boot_norm_cqv_confidence_interval(
            data=REFERENCE_DATA, multiplier=100, conf_level=1.5
        )


def test_boot_norm_cqv_too_few_replicates_raises():
    """num_replicates < 2 is rejected."""
    with pytest.raises(ValueError, match="num_replicates must be at least 2"):
        _boot_norm_cqv_confidence_interval(
            data=REFERENCE_DATA, multiplier=100, num_replicates=1
        )
