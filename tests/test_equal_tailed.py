"""Tests for the Equal-Tailed confidence interval method."""

# --------------------------- Import libraries and functions --------------------------
import math

import pandas as pd
import pytest

from pycvcqv.cv import coefficient_of_variation
from pycvcqv.equal_tailed import _equal_tailed_cv_confidence_interval

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


def test_equal_tailed_matches_r_reference_with_multiplier_100():
    """Equal-Tailed CI matches the R README's all_ci() table value."""
    result = coefficient_of_variation(
        data=REFERENCE_DATA,
        method="equal_tailed",
        multiplier=100,
        ndigits=4,
    )

    assert result["cv"] == pytest.approx(57.7735, abs=0.001)
    assert result["lower"] == pytest.approx(43.937, abs=0.01)
    assert result["upper"] == pytest.approx(84.383, abs=0.01)


def test_equal_tailed_matches_r_reference_unscaled():
    """Equal-Tailed without multiplier returns CV in raw decimal form."""
    result = coefficient_of_variation(
        data=REFERENCE_DATA,
        method="equal_tailed",
        multiplier=1,
        ndigits=6,
    )

    assert result["cv"] == pytest.approx(0.577735, abs=1e-5)
    assert result["lower"] == pytest.approx(0.43937, abs=1e-4)
    assert result["upper"] == pytest.approx(0.84383, abs=1e-4)


def test_equal_tailed_with_pandas_series_matches_list():
    """A pd.Series input produces the same result as a plain list."""
    list_result = coefficient_of_variation(
        data=REFERENCE_DATA, method="equal_tailed", multiplier=100, ndigits=4
    )
    series_result = coefficient_of_variation(
        data=pd.Series(REFERENCE_DATA),
        method="equal_tailed",
        multiplier=100,
        ndigits=4,
    )
    assert list_result == series_result


def test_equal_tailed_bounds_bracket_the_point_estimate():
    """The CI must contain the point estimate."""
    result = coefficient_of_variation(
        data=REFERENCE_DATA, method="equal_tailed", multiplier=100, ndigits=4
    )
    assert result["lower"] < result["cv"] < result["upper"]


def test_equal_tailed_narrower_at_lower_confidence():
    """Lower confidence level (wider alpha) yields a narrower CI."""
    cv_95 = coefficient_of_variation(
        data=REFERENCE_DATA,
        method="equal_tailed",
        conf_level=0.95,
        multiplier=100,
    )
    cv_80 = coefficient_of_variation(
        data=REFERENCE_DATA,
        method="equal_tailed",
        conf_level=0.80,
        multiplier=100,
    )
    assert (cv_80["upper"] - cv_80["lower"]) < (cv_95["upper"] - cv_95["lower"])


def test_equal_tailed_skipna_drops_nans():
    """skipna=True (default) silently drops NaN entries."""
    data_with_nan = [*REFERENCE_DATA, float("nan"), float("nan")]
    with_nans = coefficient_of_variation(
        data=data_with_nan, method="equal_tailed", multiplier=100, ndigits=4
    )
    without_nans = coefficient_of_variation(
        data=REFERENCE_DATA, method="equal_tailed", multiplier=100, ndigits=4
    )
    assert with_nans == without_nans


def test_equal_tailed_skipna_false_raises_on_nan():
    """skipna=False raises if NaNs are present."""
    data_with_nan = [*REFERENCE_DATA, float("nan")]
    with pytest.raises(ValueError, match="missing values"):
        _equal_tailed_cv_confidence_interval(
            data=data_with_nan, multiplier=100, skipna=False
        )


def test_equal_tailed_too_short_raises():
    """Equal-Tailed requires at least 2 observations."""
    with pytest.raises(ValueError, match="at least 2 observations"):
        _equal_tailed_cv_confidence_interval(data=[1.0], multiplier=100)


def test_equal_tailed_invalid_alpha_raises():
    """alpha/2 outside (0, 0.5) is rejected."""
    with pytest.raises(ValueError, match=r"alpha/2 must be between 0 and 0.5"):
        _equal_tailed_cv_confidence_interval(
            data=REFERENCE_DATA, multiplier=100, alpha_lower=0.6, alpha_upper=0.6
        )


def test_equal_tailed_infinite_cv_yields_infinite_bounds():
    """If the underlying CV is ±inf, CI is also ±inf."""
    symmetric_data = [-1.0, -0.5, 0.5, 1.0]
    result = _equal_tailed_cv_confidence_interval(data=symmetric_data, multiplier=100)
    assert math.isinf(result["lower"])
    assert math.isinf(result["upper"])


def test_equal_tailed_skipna_false_with_clean_data_succeeds():
    """skipna=False on clean data takes the elif's False branch."""
    result = _equal_tailed_cv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, ndigits=4, skipna=False
    )
    assert result["cv"] == pytest.approx(57.7735, abs=0.001)
    assert result["lower"] == pytest.approx(43.937, abs=0.01)
    assert result["upper"] == pytest.approx(84.383, abs=0.01)


def test_equal_tailed_only_alpha_lower_propagates_to_alpha_upper():
    """When only alpha_lower is given, alpha_upper is back-filled from it."""
    result_only_lower = _equal_tailed_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        alpha_lower=0.025,
        alpha_upper=None,
    )
    result_both = _equal_tailed_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        alpha_lower=0.025,
        alpha_upper=0.025,
    )
    assert result_only_lower == result_both


def test_equal_tailed_only_alpha_upper_propagates_to_alpha_lower():
    """When only alpha_upper is given, alpha_lower is back-filled from it."""
    result_only_upper = _equal_tailed_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        alpha_lower=None,
        alpha_upper=0.025,
    )
    result_both = _equal_tailed_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        alpha_lower=0.025,
        alpha_upper=0.025,
    )
    assert result_only_upper == result_both
