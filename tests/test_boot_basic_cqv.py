"""Tests for the basic bootstrap CI for the cqv (`method='basic'`)."""

# --------------------------- Import libraries and functions --------------------------
import numpy as np
import pandas as pd
import pytest

from pycvcqv.boot_basic_cqv import _boot_basic_cqv_confidence_interval
from pycvcqv.cqv import cqv

# R `cvcqv` README values for `basic` 95% CI: 45.625, 18.992, 73.917
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


def test_boot_basic_cqv_in_ballpark_of_r_reference():
    """With R=10000, the basic-bootstrap CI sits within a few percent of R."""
    result = cqv(
        data=REFERENCE_DATA,
        method="basic",
        multiplier=100,
        ndigits=3,
        num_replicates=10000,
        random_state=42,
    )
    assert result["cqv"] == pytest.approx(45.625, abs=1e-6)
    assert result["lower"] == pytest.approx(18.992, abs=3.5)
    assert result["upper"] == pytest.approx(73.917, abs=3.5)


def test_boot_basic_cqv_is_reproducible_with_random_state():
    """Same seed ⇒ identical CI bounds."""
    a = _boot_basic_cqv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, num_replicates=500, random_state=7
    )
    b = _boot_basic_cqv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, num_replicates=500, random_state=7
    )
    assert a == b


def test_boot_basic_cqv_accepts_external_generator():
    """An external numpy Generator with the same seed reproduces results."""
    gen_a = np.random.default_rng(321)
    gen_b = np.random.default_rng(321)
    via_gen = _boot_basic_cqv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, num_replicates=400, random_state=gen_a
    )
    via_int = _boot_basic_cqv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, num_replicates=400, random_state=gen_b
    )
    assert via_gen == via_int


def test_boot_basic_cqv_with_pandas_series_matches_list():
    """A pd.Series input matches a plain list under the same seed."""
    list_result = cqv(
        data=REFERENCE_DATA,
        method="basic",
        multiplier=100,
        num_replicates=200,
        random_state=1,
    )
    series_result = cqv(
        data=pd.Series(REFERENCE_DATA),
        method="basic",
        multiplier=100,
        num_replicates=200,
        random_state=1,
    )
    assert list_result == series_result


def test_boot_basic_cqv_bounds_bracket_the_point_estimate():
    """The CI brackets the point estimate."""
    result = _boot_basic_cqv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, num_replicates=500, random_state=2
    )
    assert result["lower"] < result["cqv"] < result["upper"]


def test_boot_basic_cqv_skipna_drops_nans():
    """skipna=True silently drops NaNs."""
    data_with_nan = [*REFERENCE_DATA, float("nan")]
    with_nans = _boot_basic_cqv_confidence_interval(
        data=data_with_nan, multiplier=100, num_replicates=200, random_state=5
    )
    without_nans = _boot_basic_cqv_confidence_interval(
        data=REFERENCE_DATA, multiplier=100, num_replicates=200, random_state=5
    )
    assert with_nans == without_nans


def test_boot_basic_cqv_skipna_false_raises_on_nan():
    """skipna=False raises on NaN."""
    data_with_nan = [*REFERENCE_DATA, float("nan")]
    with pytest.raises(ValueError, match="missing values"):
        _boot_basic_cqv_confidence_interval(
            data=data_with_nan, multiplier=100, skipna=False
        )


def test_boot_basic_cqv_too_short_raises():
    """Bootstrap basic CQV CI requires at least 2 observations."""
    with pytest.raises(ValueError, match="at least 2 observations"):
        _boot_basic_cqv_confidence_interval(data=[1.0], multiplier=100)


def test_boot_basic_cqv_too_few_replicates_raises():
    """num_replicates < 2 is rejected."""
    with pytest.raises(ValueError, match="num_replicates must be at least 2"):
        _boot_basic_cqv_confidence_interval(
            data=REFERENCE_DATA, multiplier=100, num_replicates=1
        )
