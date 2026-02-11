"""Tests for miller module."""

# --------------------------- Import libraries and functions --------------------------
import math

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from pycvcqv.cv import coefficient_of_variation
from pycvcqv.cv_confidence_interval import _cv_confidence_intervals


def test_cv_dataframe_miller():
    """Tests cv function with miller CI method for dataframe."""
    data = pd.DataFrame(
        {
            "col-1": pd.Series([0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]),
            "col-2": pd.Series([5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9]),
        }
    )

    result = coefficient_of_variation(data=data, num_threads=0, method="miller")

    expected = pd.DataFrame(
        {
            "columns": pd.Series(["col-1", "col-2"]),
            "cv": pd.Series([0.6076, 0.1359]),
            "lower": pd.Series([0.2151, 0.0681]),
            "upper": pd.Series([1.0001, 0.2037]),
        }
    )

    assert_frame_equal(result, expected, atol=1e-4)


def test_cv_confidence_intervals_miller_default_alpha():
    """Tests _cv_confidence_intervals function with miller CI method (default alpha)."""
    data = [0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]
    result = _cv_confidence_intervals(data=data, method="miller")

    expected = {"cv": 0.6076, "lower": 0.2151, "upper": 1.0001}

    assert abs(result["cv"] - expected["cv"]) < 1e-4
    assert abs(result["lower"] - expected["lower"]) < 1e-4
    assert abs(result["upper"] - expected["upper"]) < 1e-4


def test_miller_skipna_false_with_nan_raises():
    """Tests that skipna=False raises if data contains missing values."""
    with pytest.raises(ValueError):
        _cv_confidence_intervals(data=[1.0, None], method="miller", skipna=False)


def test_miller_skipna_false_without_nan_ok():
    """Tests skipna=False branch when there is no missing value."""
    result = _cv_confidence_intervals(
        data=[1.0, 2.0, 3.0], method="miller", skipna=False
    )
    assert result["lower"] <= result["cv"] <= result["upper"]


def test_miller_length_less_than_two_raises():
    """Tests that Miller CI requires at least 2 observations."""
    with pytest.raises(ValueError):
        _cv_confidence_intervals(data=[1.0], method="miller")


def test_miller_infinite_cv_returns_infinite_bounds():
    """Tests that Miller returns infinite bounds when cv is infinite."""
    # Mean is very close to zero and std > mean => _cv returns inf in formulas.py
    data = [0.0, 1e-7]
    result = _cv_confidence_intervals(data=data, method="miller")
    assert math.isinf(result["cv"])
    assert math.isinf(result["lower"])
    assert math.isinf(result["upper"])


def test_miller_conf_level_branch():
    """Tests Miller CI when conf_level is provided (conf_level branch)."""
    data = [0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]
    result = _cv_confidence_intervals(data=data, method="miller", conf_level=0.95)
    assert result["lower"] <= result["cv"] <= result["upper"]


def test_miller_alpha_upper_branch():
    """Tests Miller CI when alpha_upper is provided."""
    data = [0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]
    result = _cv_confidence_intervals(data=data, method="miller", alpha_upper=0.01)
    assert result["lower"] <= result["cv"] <= result["upper"]


def test_miller_alpha_lower_only_branch():
    """Tests Miller CI when only alpha_lower is provided (alpha_upper is None)."""
    data = [0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]
    result = _cv_confidence_intervals(data=data, method="miller", alpha_lower=0.01)
    assert result["lower"] <= result["cv"] <= result["upper"]


def test_miller_invalid_alpha_raises():
    """Tests that invalid alpha/2 values raise ValueError."""
    with pytest.raises(ValueError):
        _cv_confidence_intervals(data=[1.0, 2.0, 3.0], method="miller", alpha_upper=0.9)
