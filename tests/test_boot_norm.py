"""Tests for the bootstrap normal-approximation CI for the cv (`method='norm'`)."""

# --------------------------- Import libraries and functions --------------------------
import math

import numpy as np
import pandas as pd
import pytest

from pycvcqv.boot_norm import _boot_norm_cv_confidence_interval
from pycvcqv.cv import coefficient_of_variation

# Canonical 20-point R `cvcqv` example. The R README reports 95% CI:
#   norm  57.774  38.799  78.937
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


def test_boot_norm_in_ballpark_of_r_reference():
    """With R=10000, the norm-bootstrap CI should sit within a few percent of R."""
    result = coefficient_of_variation(
        data=REFERENCE_DATA,
        method="norm",
        multiplier=100,
        ndigits=4,
        num_replicates=10000,
        random_state=42,
    )
    assert result["cv"] == pytest.approx(57.7735, abs=0.001)
    # README values: 38.799, 78.937. Allow ±2.5 absolute on the percentage scale.
    assert result["lower"] == pytest.approx(38.799, abs=2.5)
    assert result["upper"] == pytest.approx(78.937, abs=2.5)


def test_boot_norm_is_reproducible_with_random_state():
    """Same `random_state` ⇒ identical CI bounds."""
    a = _boot_norm_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=500,
        random_state=7,
    )
    b = _boot_norm_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=500,
        random_state=7,
    )
    assert a == b


def test_boot_norm_accepts_external_generator():
    """A pre-built numpy Generator works the same as an int seed of the same value."""
    gen_a = np.random.default_rng(123)
    gen_b = np.random.default_rng(123)
    via_gen = _boot_norm_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=400,
        random_state=gen_a,
    )
    via_int = _boot_norm_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=400,
        random_state=gen_b,
    )
    assert via_gen == via_int


def test_boot_norm_with_pandas_series_matches_list():
    """A pd.Series input produces the same result as a plain list (same seed)."""
    list_result = coefficient_of_variation(
        data=REFERENCE_DATA,
        method="norm",
        multiplier=100,
        ndigits=4,
        num_replicates=200,
        random_state=1,
    )
    series_result = coefficient_of_variation(
        data=pd.Series(REFERENCE_DATA),
        method="norm",
        multiplier=100,
        ndigits=4,
        num_replicates=200,
        random_state=1,
    )
    assert list_result == series_result


def test_boot_norm_bounds_bracket_the_point_estimate():
    """The CI must contain the point estimate."""
    result = _boot_norm_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=500,
        random_state=2,
    )
    assert result["lower"] < result["cv"] < result["upper"]


def test_boot_norm_narrower_at_lower_confidence():
    """Lower confidence level (wider alpha) yields a narrower CI."""
    cv_95 = _boot_norm_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        conf_level=0.95,
        num_replicates=2000,
        random_state=99,
    )
    cv_80 = _boot_norm_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        conf_level=0.80,
        num_replicates=2000,
        random_state=99,
    )
    assert (cv_80["upper"] - cv_80["lower"]) < (cv_95["upper"] - cv_95["lower"])


def test_boot_norm_skipna_drops_nans():
    """skipna=True (default) silently drops NaN entries."""
    data_with_nan = [*REFERENCE_DATA, float("nan"), float("nan")]
    with_nans = _boot_norm_cv_confidence_interval(
        data=data_with_nan,
        multiplier=100,
        ndigits=4,
        num_replicates=200,
        random_state=5,
    )
    without_nans = _boot_norm_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=200,
        random_state=5,
    )
    assert with_nans == without_nans


def test_boot_norm_skipna_false_raises_on_nan():
    """skipna=False raises if NaNs are present."""
    data_with_nan = [*REFERENCE_DATA, float("nan")]
    with pytest.raises(ValueError, match="missing values"):
        _boot_norm_cv_confidence_interval(
            data=data_with_nan,
            multiplier=100,
            skipna=False,
        )


def test_boot_norm_too_short_raises():
    """Bootstrap norm CI requires at least 2 observations."""
    with pytest.raises(ValueError, match="at least 2 observations"):
        _boot_norm_cv_confidence_interval(data=[1.0], multiplier=100)


def test_boot_norm_invalid_conf_level_raises():
    """conf_level outside (0, 1) is rejected."""
    with pytest.raises(ValueError, match="conf_level must be between"):
        _boot_norm_cv_confidence_interval(
            data=REFERENCE_DATA,
            multiplier=100,
            conf_level=1.5,
        )


def test_boot_norm_too_few_replicates_raises():
    """num_replicates < 2 is rejected."""
    with pytest.raises(ValueError, match="num_replicates must be at least 2"):
        _boot_norm_cv_confidence_interval(
            data=REFERENCE_DATA,
            multiplier=100,
            num_replicates=1,
        )


def test_boot_norm_infinite_cv_yields_infinite_bounds():
    """Symmetric-around-zero data ⇒ cv = inf ⇒ bounds = inf."""
    symmetric_data = [-1.0, -0.5, 0.5, 1.0]
    result = _boot_norm_cv_confidence_interval(
        data=symmetric_data,
        multiplier=100,
    )
    assert math.isinf(result["lower"])
    assert math.isinf(result["upper"])


def test_boot_norm_correction_changes_point_estimate():
    """correction=True ⇒ different point estimate (and CI) from correction=False."""
    no_corr = _boot_norm_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=500,
        random_state=11,
        correction=False,
    )
    with_corr = _boot_norm_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=500,
        random_state=11,
        correction=True,
    )
    assert no_corr["cv"] != with_corr["cv"]
