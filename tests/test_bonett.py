"""Tests for Bonett's centering-adjusted CI for the cqv (`method='bonett'`)."""

# --------------------------- Import libraries and functions --------------------------
import pandas as pd
import pytest

from pycvcqv import bonett as _bonett_module
from pycvcqv.bonett import _bonett_cqv_confidence_interval
from pycvcqv.cqv import cqv

# 20-point R `cvcqv` README example. R reports for Bonett 95% CI:
#   bonett  45.625  24.785  77.329
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


def test_bonett_matches_r_reference():
    """Bonett CI matches R's published values to 3 digits."""
    result = _bonett_cqv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=3,
    )
    assert result["cqv"] == pytest.approx(45.625, abs=1e-6)
    assert result["lower"] == pytest.approx(24.785, abs=0.01)
    assert result["upper"] == pytest.approx(77.329, abs=0.01)


def test_bonett_via_public_api_matches_helper():
    """`cqv(method='bonett')` produces the same result as the helper."""
    direct = _bonett_cqv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
    )
    via_api = cqv(
        data=REFERENCE_DATA,
        method="bonett",
        multiplier=100,
        ndigits=4,
    )
    assert direct == via_api


def test_bonett_with_pandas_series_matches_list():
    """A pd.Series input produces the same result as a plain list."""
    list_result = cqv(data=REFERENCE_DATA, method="bonett", multiplier=100, ndigits=4)
    series_result = cqv(
        data=pd.Series(REFERENCE_DATA),
        method="bonett",
        multiplier=100,
        ndigits=4,
    )
    assert list_result == series_result


def test_bonett_bounds_bracket_the_point_estimate():
    """The CI must contain the point estimate."""
    result = _bonett_cqv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
    )
    assert result["lower"] < result["cqv"] < result["upper"]


def test_bonett_skipna_drops_nans():
    """skipna=True (default) silently drops NaN entries."""
    data_with_nan = [*REFERENCE_DATA, float("nan"), float("nan")]
    with_nans = _bonett_cqv_confidence_interval(
        data=data_with_nan,
        multiplier=100,
        ndigits=4,
    )
    without_nans = _bonett_cqv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
    )
    assert with_nans == without_nans


def test_bonett_skipna_false_raises_on_nan():
    """skipna=False raises if NaNs are present."""
    data_with_nan = [*REFERENCE_DATA, float("nan")]
    with pytest.raises(ValueError, match="missing values"):
        _bonett_cqv_confidence_interval(
            data=data_with_nan,
            multiplier=100,
            skipna=False,
        )


def test_bonett_too_short_raises():
    """Bonett CI requires at least 4 observations to define a/b/c/d indices."""
    with pytest.raises(ValueError, match="at least 4 observations"):
        _bonett_cqv_confidence_interval(data=[1.0, 2.0, 3.0], multiplier=100)


def test_bonett_zero_quartiles_raises_warning():
    """When q3 + q1 == 0 the CQV is undefined and Bonett raises."""
    with pytest.raises(Warning, match="cqv is NaN because q3 and q1 are 0"):
        _bonett_cqv_confidence_interval(
            data=[-1.0, -1.0, -1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0],
            multiplier=100,
        )


def test_bonett_unused_kwargs_dont_change_output():
    """conf_level / num_replicates / random_state are accepted but ignored."""
    base = _bonett_cqv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, ndigits=4
    )
    with_extras = _bonett_cqv_confidence_interval(
        data=REFERENCE_DATA,
        multiplier=100,
        ndigits=4,
        conf_level=0.99,
        num_replicates=999,
        random_state=42,
    )
    assert base == with_extras


def test_bonett_dataframe_path():
    """cqv DataFrame path with bonett returns a 4-column frame."""
    data = pd.DataFrame(
        {
            "col-1": pd.Series([0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]),
            "col-2": pd.Series([5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9]),
        }
    )
    result = cqv(data=data, method="bonett", multiplier=100, ndigits=3)
    assert list(result.columns) == ["columns", "cqv", "lower", "upper"]
    assert list(result["columns"]) == ["col-1", "col-2"]
    # Each lower < cqv < upper.
    for _, row in result.iterrows():
        assert row["lower"] < row["cqv"] < row["upper"]


def test_bonett_default_multiplier_is_one():
    """multiplier=1 (default) returns the raw CQV in (0, 1)."""
    result = _bonett_cqv_confidence_interval(data=REFERENCE_DATA, ndigits=5)
    assert 0.0 < result["cqv"] < 1.0
    assert 0.0 < result["lower"] < result["cqv"] < result["upper"] < 1.0


def test_bonett_skipna_false_passes_when_no_nans():
    """skipna=False is fine on data with no NaN values."""
    result = _bonett_cqv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, ndigits=4, skipna=False
    )
    assert result["lower"] < result["cqv"] < result["upper"]


def test_bonett_indices_outside_sample_raises(monkeypatch):
    """Defensive guard fires if a/b/c/d indices fall outside the sample.

    The math at the top of the function always produces valid indices for
    n >= 4, so the only way to exercise the defensive branch is to force a
    bad b via monkeypatching `round` on the module's namespace.
    """
    monkeypatch.setattr(
        _bonett_module, "round", lambda *args, **kwargs: 0, raising=False
    )
    with pytest.raises(ValueError, match="indices fell outside the sample"):
        _bonett_cqv_confidence_interval(data=REFERENCE_DATA, multiplier=100)
