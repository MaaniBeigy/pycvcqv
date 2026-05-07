"""Tests for the CQV confidence-interval dispatcher."""

# --------------------------- Import libraries and functions --------------------------
import math
import warnings

import numpy as np
import pytest

from pycvcqv import _cqv_bootstrap as _cqvb_module
from pycvcqv._cqv_bootstrap import _bootstrap_cqv_confidence_interval
from pycvcqv.cqv_confidence_interval import _cqv_confidence_intervals
from pycvcqv.formulas import _cqv_statistic

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


def test_dispatcher_unknown_method_raises():
    """An unrecognised method name surfaces a clear ValueError."""
    with pytest.raises(ValueError, match="Unknown CQV CI method"):
        _cqv_confidence_intervals(data=REFERENCE_DATA, method="not_a_real_method")


@pytest.mark.parametrize("method", ["bonett", "norm", "basic", "perc", "bca"])
def test_dispatcher_returns_native_floats(method):
    """All methods coerce numpy scalars to native Python floats."""
    result = _cqv_confidence_intervals(
        data=REFERENCE_DATA,
        method=method,
        multiplier=100,
        ndigits=4,
        num_replicates=200,
        random_state=1,
    )
    assert isinstance(result["cqv"], float)
    assert isinstance(result["lower"], float)
    assert isinstance(result["upper"], float)


@pytest.mark.parametrize("method", ["bonett", "norm", "basic", "perc", "bca"])
def test_dispatcher_keys_are_consistent(method):
    """All methods return the same key set."""
    result = _cqv_confidence_intervals(
        data=REFERENCE_DATA,
        method=method,
        multiplier=100,
        ndigits=4,
        num_replicates=200,
        random_state=1,
    )
    assert set(result.keys()) == {"cqv", "lower", "upper"}


def test_bootstrap_helper_unknown_kind_raises():
    """_bootstrap_cqv_confidence_interval rejects bad ci_kind values."""
    with pytest.raises(ValueError, match="Unknown bootstrap CI kind"):
        _bootstrap_cqv_confidence_interval(ci_kind="not_real", data=REFERENCE_DATA)


def test_bootstrap_default_num_replicates_runs():
    """num_replicates=None falls back to 1000 (default) without error."""
    result = _cqv_confidence_intervals(
        data=REFERENCE_DATA,
        method="perc",
        multiplier=100,
        ndigits=4,
        random_state=42,
    )
    assert result["lower"] < result["cqv"] < result["upper"]


def test_bootstrap_skipna_false_passes_when_no_nans():
    """skipna=False is fine on data with no NaN values."""
    result = _cqv_confidence_intervals(
        data=REFERENCE_DATA,
        method="perc",
        multiplier=100,
        ndigits=4,
        num_replicates=200,
        random_state=1,
        skipna=False,
    )
    assert result["lower"] < result["cqv"] < result["upper"]


def test_cqv_statistic_returns_nan_for_size_below_two():
    """`_cqv_statistic` returns NaN for empty or single-element samples."""
    assert math.isnan(_cqv_statistic(np.array([], dtype=np.float64)))
    assert math.isnan(_cqv_statistic(np.array([5.0], dtype=np.float64)))


def test_cqv_statistic_returns_nan_when_quartiles_sum_to_zero():
    """`_cqv_statistic` returns NaN when q3 + q1 == 0 (CQV is undefined)."""
    sample = np.array([-1.0, -1.0, -1.0, 1.0, 1.0, 1.0], dtype=np.float64)
    assert math.isnan(_cqv_statistic(sample))


def test_bootstrap_returns_unrounded_bounds_when_non_finite(monkeypatch):
    """If all bootstrap replicates are non-finite, lower/upper come back as NaN.

    Triggers the early-return guard at the bottom of
    `_bootstrap_cqv_confidence_interval`: rounding NaN would silently produce
    NaN anyway, but skipping the round preserves the raw signal.
    """

    def _all_nan_resample(*_args, **_kwargs):
        return np.full(100, np.nan, dtype=np.float64)

    monkeypatch.setattr(_cqvb_module, "_resample_cqv_replicates", _all_nan_resample)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        result = _bootstrap_cqv_confidence_interval(
            ci_kind="norm",
            data=REFERENCE_DATA,
            multiplier=100,
            ndigits=4,
            num_replicates=100,
            random_state=42,
        )
    assert math.isnan(result["lower"])
    assert math.isnan(result["upper"])
    assert result["cqv"] == pytest.approx(45.625)
