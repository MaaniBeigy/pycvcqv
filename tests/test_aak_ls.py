"""Tests for the AA&K-LS confidence interval method (`method='aak_ls'`)."""

# --------------------------- Import libraries and functions --------------------------
import math

import pandas as pd
import pytest

from pycvcqv.aak_ls import _aak_ls_cv_confidence_interval
from pycvcqv.cv import coefficient_of_variation

INFANTS_DATA = [
    4960,
    5130,
    4260,
    5160,
    4050,
    5240,
    4350,
    4360,
    3930,
    4410,
    4610,
    4102,
    3530,
    4550,
    4460,
    2940,
    4160,
    4110,
    4410,
    4800,
    5130,
    3670,
    4550,
    4290,
    5210,
    4950,
    5210,
    3210,
    4030,
    3580,
    4360,
    4360,
    3920,
    4050,
    4630,
    3756,
    4382,
    4586,
    5336,
    2828,
    4172,
    4256,
    4594,
    4866,
    4784,
    4520,
    5238,
    4320,
    5070,
    5330,
    3836,
    5916,
    5010,
    4344,
    3496,
    4148,
    4044,
    5192,
    4368,
    4180,
    5044,
]

PMI_DATA = [
    5.5,
    14.5,
    6.0,
    5.5,
    5.3,
    5.8,
    11.0,
    6.1,
    7.0,
    14.5,
    10.4,
    4.6,
    4.3,
    7.2,
    10.5,
    6.5,
    3.3,
    7.0,
    4.1,
    6.2,
    10.4,
    4.9,
]

SMALL_DATA = [
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


def test_aak_ls_matches_paper_infants_table_5():
    """
    Abu-Shawiesh, Aky & Kibria (2019), Table 5: AA&K-LS on infants is (0.1144, 0.1672).
    """
    result = _aak_ls_cv_confidence_interval(data=INFANTS_DATA, ndigits=4)
    assert result["lower"] == pytest.approx(0.1144, abs=0.005)
    assert result["upper"] == pytest.approx(0.1672, abs=0.005)


def test_aak_ls_matches_paper_pmi_table_6():
    """
    Abu-Shawiesh, Aky & Kibria (2019), Table 6: AA&K-LS on PMI is (0.3122, 0.6095).
    """
    result = _aak_ls_cv_confidence_interval(data=PMI_DATA, ndigits=4)
    assert result["lower"] == pytest.approx(0.3122, abs=0.005)
    assert result["upper"] == pytest.approx(0.6095, abs=0.005)


def test_aak_ls_via_public_api_matches_helper():
    """`coefficient_of_variation(method='aak_ls')` matches the helper."""
    direct = _aak_ls_cv_confidence_interval(data=SMALL_DATA, ndigits=4)
    via_api = coefficient_of_variation(data=SMALL_DATA, method="aak_ls", ndigits=4)
    assert direct == via_api


def test_aak_ls_conf_level_matches_alpha_split():
    """conf_level=0.95 and alpha_lower=alpha_upper=0.025 give identical bounds."""
    via_conf = _aak_ls_cv_confidence_interval(
        data=SMALL_DATA, conf_level=0.95, ndigits=6
    )
    via_alpha = _aak_ls_cv_confidence_interval(
        data=SMALL_DATA, alpha_lower=0.025, alpha_upper=0.025, ndigits=6
    )
    assert via_conf == via_alpha


def test_aak_ls_alpha_lower_only_back_fills_upper():
    """Passing only alpha_lower back-fills alpha_upper from it."""
    only_lower = _aak_ls_cv_confidence_interval(
        data=SMALL_DATA, alpha_lower=0.025, ndigits=6
    )
    both = _aak_ls_cv_confidence_interval(
        data=SMALL_DATA, alpha_lower=0.025, alpha_upper=0.025, ndigits=6
    )
    assert only_lower == both


def test_aak_ls_alpha_upper_only_back_fills_lower():
    """Passing only alpha_upper back-fills alpha_lower from it."""
    only_upper = _aak_ls_cv_confidence_interval(
        data=SMALL_DATA, alpha_upper=0.025, ndigits=6
    )
    both = _aak_ls_cv_confidence_interval(
        data=SMALL_DATA, alpha_lower=0.025, alpha_upper=0.025, ndigits=6
    )
    assert only_upper == both


def test_aak_ls_alpha_out_of_range_raises():
    """alpha/2 outside (0, 0.5) raises."""
    with pytest.raises(ValueError, match="alpha/2 must be between"):
        _aak_ls_cv_confidence_interval(data=SMALL_DATA, conf_level=0.0)


def test_aak_ls_bounds_bracket_the_point_estimate():
    """The CI must contain the point estimate."""
    result = _aak_ls_cv_confidence_interval(data=SMALL_DATA, ndigits=6)
    assert result["lower"] < result["cv"] < result["upper"]


def test_aak_ls_skipna_drops_nans():
    """skipna=True (default) drops NaNs."""
    with_nans = _aak_ls_cv_confidence_interval(
        data=[*SMALL_DATA, float("nan"), float("nan")], ndigits=6
    )
    without_nans = _aak_ls_cv_confidence_interval(data=SMALL_DATA, ndigits=6)
    assert with_nans == without_nans


def test_aak_ls_skipna_false_raises_on_nan():
    """skipna=False raises if NaNs are present."""
    with pytest.raises(ValueError, match="missing values"):
        _aak_ls_cv_confidence_interval(data=[*SMALL_DATA, float("nan")], skipna=False)


def test_aak_ls_skipna_false_passes_when_no_nans():
    """skipna=False is fine on NaN-free data."""
    result = _aak_ls_cv_confidence_interval(data=SMALL_DATA, skipna=False, ndigits=6)
    assert result["lower"] < result["cv"] < result["upper"]


def test_aak_ls_too_short_raises():
    """AA&K-LS requires n >= 4 because G_2 has (n-2)(n-3) in the denom."""
    with pytest.raises(ValueError, match="at least 4 observations"):
        _aak_ls_cv_confidence_interval(data=[1.0, 2.0, 3.0])


def test_aak_ls_zero_mean_returns_inf_bounds():
    """A degenerate mean produces inf bounds."""
    result = _aak_ls_cv_confidence_interval(
        data=[-1.0, -1.0, 0.0, 0.0, 1.0, 1.0], ndigits=6
    )
    assert math.isinf(result["cv"])
    assert math.isinf(result["lower"])
    assert math.isinf(result["upper"])


def test_aak_ls_multiplier_scales_the_output():
    """multiplier=100 produces the percent-scaled bounds and CV."""
    base = _aak_ls_cv_confidence_interval(data=SMALL_DATA, multiplier=1, ndigits=6)
    percent = _aak_ls_cv_confidence_interval(data=SMALL_DATA, multiplier=100, ndigits=4)
    assert percent["cv"] == pytest.approx(100.0 * base["cv"], abs=0.01)
    assert percent["lower"] == pytest.approx(100.0 * base["lower"], abs=0.01)
    assert percent["upper"] == pytest.approx(100.0 * base["upper"], abs=0.01)


def test_aak_ls_dataframe_path():
    """The DataFrame path returns one row per column with valid bounds."""
    data = pd.DataFrame(
        {
            "col-1": pd.Series([0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]),
            "col-2": pd.Series([5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9]),
        }
    )
    result = coefficient_of_variation(data=data, method="aak_ls", ndigits=4)
    assert list(result.columns) == ["columns", "cv", "lower", "upper"]
    for _, row in result.iterrows():
        assert row["lower"] < row["cv"] < row["upper"]


def test_aak_ls_unused_kwargs_dont_change_output():
    """tol / max_iter are accepted but ignored."""
    base = _aak_ls_cv_confidence_interval(data=SMALL_DATA, ndigits=6)
    with_extras = _aak_ls_cv_confidence_interval(
        data=SMALL_DATA, tol=1e-3, max_iter=42, ndigits=6
    )
    assert base == with_extras
