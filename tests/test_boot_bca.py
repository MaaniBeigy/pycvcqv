"""Tests for the BCa bootstrap CI for the cv (`method='bca'`)."""

# --------------------------- Import libraries and functions --------------------------
import math

import pandas as pd
import pytest

from pycvcqv.boot_bca import _boot_bca_cv_confidence_interval
from pycvcqv.cv import coefficient_of_variation

# R README: bca 57.774 40.807 82.297.
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


def test_boot_bca_in_ballpark_of_r_reference():
    """With R=10000, BCa should sit within a few percent of the R README."""
    result = coefficient_of_variation(
        data=REFERENCE_DATA,
        method="bca",
        multiplier=100,
        ndigits=4,
        num_replicates=10000,
        random_state=42,
    )
    assert result["cv"] == pytest.approx(57.7735, abs=0.001)
    assert result["lower"] == pytest.approx(40.807, abs=3.0)
    assert result["upper"] == pytest.approx(82.297, abs=3.0)


def test_boot_bca_is_reproducible_with_random_state():
    """Same `random_state` ⇒ identical CI bounds."""
    a = _boot_bca_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=500,
        random_state=7,
    )
    b = _boot_bca_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=500,
        random_state=7,
    )
    assert a == b


def test_boot_bca_bounds_bracket_the_point_estimate():
    """The CI must contain the point estimate."""
    result = _boot_bca_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=2000,
        random_state=3,
    )
    assert result["lower"] < result["cv"] < result["upper"]


def test_boot_bca_with_pandas_series_matches_list():
    """A pd.Series input produces the same result as a plain list (same seed)."""
    list_result = coefficient_of_variation(
        data=REFERENCE_DATA,
        method="bca",
        multiplier=100,
        ndigits=4,
        num_replicates=400,
        random_state=1,
    )
    series_result = coefficient_of_variation(
        data=pd.Series(REFERENCE_DATA),
        method="bca",
        multiplier=100,
        ndigits=4,
        num_replicates=400,
        random_state=1,
    )
    assert list_result == series_result


def test_boot_bca_narrower_at_lower_confidence():
    """Lower confidence level (wider alpha) yields a narrower CI."""
    cv_95 = _boot_bca_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        conf_level=0.95,
        num_replicates=2000,
        random_state=99,
    )
    cv_80 = _boot_bca_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        conf_level=0.80,
        num_replicates=2000,
        random_state=99,
    )
    assert (cv_80["upper"] - cv_80["lower"]) < (cv_95["upper"] - cv_95["lower"])


def test_boot_bca_skipna_drops_nans():
    """skipna=True (default) silently drops NaN entries."""
    data_with_nan = [*REFERENCE_DATA, float("nan")]
    with_nans = _boot_bca_cv_confidence_interval(
        data=data_with_nan,
        multiplier=100,
        ndigits=4,
        num_replicates=400,
        random_state=5,
    )
    without_nans = _boot_bca_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=400,
        random_state=5,
    )
    assert with_nans == without_nans


def test_boot_bca_skipna_false_raises_on_nan():
    """skipna=False raises if NaNs are present."""
    with pytest.raises(ValueError, match="missing values"):
        _boot_bca_cv_confidence_interval(
            data=[1.0, float("nan"), 2.0],
            multiplier=100,
            skipna=False,
        )


def test_boot_bca_too_short_raises():
    """Bootstrap BCa CI requires at least 2 observations."""
    with pytest.raises(ValueError, match="at least 2 observations"):
        _boot_bca_cv_confidence_interval(data=[1.0], multiplier=100)


def test_boot_bca_too_few_replicates_raises():
    """num_replicates < 2 is rejected."""
    with pytest.raises(ValueError, match="num_replicates must be at least 2"):
        _boot_bca_cv_confidence_interval(
            data=REFERENCE_DATA,
            multiplier=100,
            num_replicates=1,
        )


def test_boot_bca_invalid_conf_level_raises():
    """conf_level outside (0, 1) is rejected."""
    with pytest.raises(ValueError, match="conf_level must be between"):
        _boot_bca_cv_confidence_interval(
            data=REFERENCE_DATA,
            multiplier=100,
            conf_level=2.0,
        )


def test_boot_bca_infinite_cv_yields_infinite_bounds():
    """If the underlying CV is ±inf, CI is also ±inf."""
    symmetric_data = [-1.0, -0.5, 0.5, 1.0]
    result = _boot_bca_cv_confidence_interval(data=symmetric_data, multiplier=100)
    assert math.isinf(result["lower"])
    assert math.isinf(result["upper"])


def test_boot_bca_raises_when_z0_is_infinite():
    """If every bootstrap replicate sits on the same side of t0, BCa is undefined.

    A two-point sample where one observation is much larger than the
    other can yield a bootstrap distribution where every replicate is
    either equal to t0 or all above/below it (depending on which
    indices are drawn). For [1, 1] the cv is 0, and any resample is
    also constant, so #{t* < t0} == 0 and z0 = qnorm(0) = -inf.
    """
    constant_with_one_outlier = [1.0, 1.0]
    with pytest.raises(ValueError, match="z0.*infinite"):
        _boot_bca_cv_confidence_interval(
            data=constant_with_one_outlier,
            multiplier=100,
            num_replicates=200,
            random_state=0,
        )
