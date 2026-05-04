"""Tests for the Shortest-Length confidence interval method."""

# --------------------------- Import libraries and functions --------------------------
import math

import pandas as pd
import pytest

from pycvcqv.cv import coefficient_of_variation
from pycvcqv.shortest_length import (
    _lookup_ab,
    _shortest_length_cv_confidence_interval,
)

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


def test_shortest_length_matches_r_reference_with_multiplier_100():
    """Shortest-Length CI matches the R README's all_ci() table value."""
    result = coefficient_of_variation(
        data=REFERENCE_DATA,
        method="shortest_length",
        multiplier=100,
        ndigits=4,
    )

    assert result["cv"] == pytest.approx(57.7735, abs=0.001)
    assert result["lower"] == pytest.approx(42.015, abs=0.01)
    assert result["upper"] == pytest.approx(81.013, abs=0.01)


def test_shortest_length_matches_r_reference_unscaled():
    """Shortest-Length without multiplier returns CV in raw decimal form."""
    result = coefficient_of_variation(
        data=REFERENCE_DATA,
        method="shortest_length",
        multiplier=1,
        ndigits=6,
    )

    assert result["cv"] == pytest.approx(0.577735, abs=1e-5)
    assert result["lower"] == pytest.approx(0.42015, abs=1e-4)
    assert result["upper"] == pytest.approx(0.81013, abs=1e-4)


def test_shortest_length_with_pandas_series_matches_list():
    """A pd.Series input produces the same result as a plain list."""
    list_result = coefficient_of_variation(
        data=REFERENCE_DATA, method="shortest_length", multiplier=100, ndigits=4
    )
    series_result = coefficient_of_variation(
        data=pd.Series(REFERENCE_DATA),
        method="shortest_length",
        multiplier=100,
        ndigits=4,
    )
    assert list_result == series_result


def test_shortest_length_bounds_bracket_the_point_estimate():
    """The CI must contain the point estimate."""
    result = coefficient_of_variation(
        data=REFERENCE_DATA, method="shortest_length", multiplier=100, ndigits=4
    )
    assert result["lower"] < result["cv"] < result["upper"]


def test_shortest_length_skipna_drops_nans():
    """skipna=True (default) silently drops NaN entries."""
    data_with_nan = [*REFERENCE_DATA, float("nan"), float("nan")]
    with_nans = coefficient_of_variation(
        data=data_with_nan, method="shortest_length", multiplier=100, ndigits=4
    )
    without_nans = coefficient_of_variation(
        data=REFERENCE_DATA, method="shortest_length", multiplier=100, ndigits=4
    )
    assert with_nans == without_nans


def test_shortest_length_skipna_false_raises_on_nan():
    """skipna=False raises if NaNs are present."""
    data_with_nan = [*REFERENCE_DATA, float("nan")]
    with pytest.raises(ValueError, match="missing values"):
        _shortest_length_cv_confidence_interval(
            data=data_with_nan, multiplier=100, skipna=False
        )


def test_shortest_length_too_short_raises():
    """Shortest-Length requires at least 2 observations."""
    with pytest.raises(ValueError, match="at least 2 observations"):
        _shortest_length_cv_confidence_interval(data=[1.0], multiplier=100)


def test_shortest_length_unsupported_alpha_raises():
    """alpha not in {0.1, 0.05, 0.01} is rejected (table only covers those)."""
    # conf_level=0.975 → alpha=0.025, which is not tabulated.
    with pytest.raises(ValueError, match="only tabulated for alpha"):
        _shortest_length_cv_confidence_interval(
            data=REFERENCE_DATA, multiplier=100, conf_level=0.975
        )


def test_shortest_length_untabulated_dof_raises():
    """v outside the tabulated grid (e.g. v=31) is rejected."""
    # 32 points → v = 31, which sits between tabulated 30 and 40.
    data = [float(i) + 1.0 for i in range(32)]
    with pytest.raises(ValueError, match="only tabulated for v"):
        _shortest_length_cv_confidence_interval(
            data=data, multiplier=100, conf_level=0.95
        )


def test_shortest_length_dof_above_300_uses_v300_row():
    """For v > 300, R falls back to the v = 300 row; we mirror this."""
    data_310 = [1.0 + 0.001 * i for i in range(311)]  # n=311 → v=310
    a_310, b_310 = _lookup_ab(0.05, 310)
    a_300, b_300 = _lookup_ab(0.05, 300)
    assert (a_310, b_310) == (a_300, b_300)
    # And the function itself should work without raising:
    result = _shortest_length_cv_confidence_interval(
        data=data_310, multiplier=100, ndigits=4
    )
    assert math.isfinite(result["cv"])
    assert math.isfinite(result["lower"])
    assert math.isfinite(result["upper"])


def test_shortest_length_invalid_alpha_value_raises():
    """alpha outside (0, 1) is rejected."""
    with pytest.raises(ValueError, match="alpha must be between 0 and 1"):
        _shortest_length_cv_confidence_interval(
            data=REFERENCE_DATA,
            multiplier=100,
            alpha_lower=1.5,
            alpha_upper=1.5,
        )


def test_shortest_length_infinite_cv_yields_infinite_bounds():
    """If the underlying CV is ±inf, CI is also ±inf."""
    symmetric_data = [-1.0, -0.5, 0.5, 1.0]
    result = _shortest_length_cv_confidence_interval(
        data=symmetric_data, multiplier=100
    )
    assert math.isinf(result["lower"])
    assert math.isinf(result["upper"])


def test_shortest_length_skipna_false_with_clean_data_succeeds():
    """skipna=False on clean data takes the elif's False branch."""
    result = _shortest_length_cv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, ndigits=4, skipna=False
    )
    assert result["cv"] == pytest.approx(57.7735, abs=0.001)
    assert result["lower"] == pytest.approx(42.015, abs=0.01)
    assert result["upper"] == pytest.approx(81.013, abs=0.01)


def test_shortest_length_only_alpha_lower_propagates_to_alpha_upper():
    """When only alpha_lower is given, alpha_upper is back-filled from it."""
    result_only_lower = _shortest_length_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        alpha_lower=0.05,
        alpha_upper=None,
    )
    result_both = _shortest_length_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        alpha_lower=0.05,
        alpha_upper=0.05,
    )
    assert result_only_lower == result_both


def test_shortest_length_only_alpha_upper_propagates_to_alpha_lower():
    """When only alpha_upper is given, alpha_lower is back-filled from it."""
    result_only_upper = _shortest_length_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        alpha_lower=None,
        alpha_upper=0.05,
    )
    result_both = _shortest_length_cv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        alpha_lower=0.05,
        alpha_upper=0.05,
    )
    assert result_only_upper == result_both
