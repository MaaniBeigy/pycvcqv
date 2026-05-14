"""Tests for the basic bootstrap CI for the cv (`method='basic'`)."""

# --------------------------- Import libraries and functions --------------------------
import math

import pandas as pd
import pytest

from pycvcqv.boot_basic import _boot_basic_cv_confidence_interval
from pycvcqv.cv import coefficient_of_variation

# R README: basic 57.774 35.055 78.167. Bootstrap CIs depend on the RNG
# stream, so we use a wide tolerance against the README and rely on
# Python-side reproducibility for the rest.
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


def test_boot_basic_in_ballpark_of_r_reference():
    """With R=10000, the basic CI sits within a few percent of the R README."""
    result = coefficient_of_variation(
        data=REFERENCE_DATA,
        method="basic",
        multiplier=100,
        ndigits=4,
        num_replicates=10000,
        random_state=42,
    )
    assert result["cv"] == pytest.approx(57.7735, abs=0.001)
    assert result["lower"] == pytest.approx(35.055, abs=3.5)
    assert result["upper"] == pytest.approx(78.167, abs=3.5)


def test_boot_basic_is_reproducible_with_random_state():
    """Same `random_state` ⇒ identical CI bounds."""
    a = _boot_basic_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=500,
        random_state=7,
    )
    b = _boot_basic_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=500,
        random_state=7,
    )
    assert a == b


def test_boot_basic_pivots_around_point_estimate():
    """Basic CI uses the pivotal formula 2*t0 - q. Verify lower < t0 < upper."""
    result = _boot_basic_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=2000,
        random_state=3,
    )
    assert result["lower"] < result["cv"] < result["upper"]


def test_boot_basic_with_pandas_series_matches_list():
    """A pd.Series input produces the same result as a plain list (same seed)."""
    list_result = coefficient_of_variation(
        data=REFERENCE_DATA,
        method="basic",
        multiplier=100,
        ndigits=4,
        num_replicates=200,
        random_state=1,
    )
    series_result = coefficient_of_variation(
        data=pd.Series(REFERENCE_DATA),
        method="basic",
        multiplier=100,
        ndigits=4,
        num_replicates=200,
        random_state=1,
    )
    assert list_result == series_result


def test_boot_basic_narrower_at_lower_confidence():
    """Lower confidence level (wider alpha) yields a narrower CI."""
    cv_95 = _boot_basic_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        conf_level=0.95,
        num_replicates=2000,
        random_state=99,
    )
    cv_80 = _boot_basic_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        conf_level=0.80,
        num_replicates=2000,
        random_state=99,
    )
    assert (cv_80["upper"] - cv_80["lower"]) < (cv_95["upper"] - cv_95["lower"])


def test_boot_basic_skipna_drops_nans():
    """skipna=True (default) silently drops NaN entries."""
    data_with_nan = [*REFERENCE_DATA, float("nan")]
    with_nans = _boot_basic_cv_confidence_interval(
        data=data_with_nan,
        multiplier=100,
        ndigits=4,
        num_replicates=200,
        random_state=5,
    )
    without_nans = _boot_basic_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=200,
        random_state=5,
    )
    assert with_nans == without_nans


def test_boot_basic_skipna_false_raises_on_nan():
    """skipna=False raises if NaNs are present."""
    with pytest.raises(ValueError, match="missing values"):
        _boot_basic_cv_confidence_interval(
            data=[1.0, float("nan"), 2.0],
            multiplier=100,
            skipna=False,
        )


def test_boot_basic_too_short_raises():
    """Bootstrap basic CI requires at least 2 observations."""
    with pytest.raises(ValueError, match="at least 2 observations"):
        _boot_basic_cv_confidence_interval(data=[1.0], multiplier=100)


def test_boot_basic_too_few_replicates_raises():
    """num_replicates < 2 is rejected."""
    with pytest.raises(ValueError, match="num_replicates must be at least 2"):
        _boot_basic_cv_confidence_interval(
            data=REFERENCE_DATA,
            multiplier=100,
            num_replicates=1,
        )


def test_boot_basic_invalid_conf_level_raises():
    """conf_level outside (0, 1) is rejected."""
    with pytest.raises(ValueError, match="conf_level must be between"):
        _boot_basic_cv_confidence_interval(
            data=REFERENCE_DATA,
            multiplier=100,
            conf_level=-0.1,
        )


def test_boot_basic_infinite_cv_yields_infinite_bounds():
    """If the underlying CV is ±inf, CI is also ±inf."""
    symmetric_data = [-1.0, -0.5, 0.5, 1.0]
    result = _boot_basic_cv_confidence_interval(
        data=symmetric_data,
        multiplier=100,
    )
    assert math.isinf(result["lower"])
    assert math.isinf(result["upper"])


def test_boot_basic_accepts_alpha_lower_alone():
    """Only alpha_lower given ⇒ symmetric tail is back-filled."""
    result = _boot_basic_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=400,
        random_state=2025,
        alpha_lower=0.025,
    )
    assert result["lower"] < result["cv"] < result["upper"]


def test_boot_basic_accepts_alpha_upper_alone():
    """Only alpha_upper given ⇒ alpha_lower is back-filled."""
    result = _boot_basic_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        num_replicates=400,
        random_state=2025,
        alpha_upper=0.025,
    )
    assert result["lower"] < result["cv"] < result["upper"]
