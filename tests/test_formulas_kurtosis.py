"""Tests for the kurtosis-family helpers in `pycvcqv.formulas`."""

# --------------------------- Import libraries and functions --------------------------
import math

import pandas as pd
import pytest
from scipy.stats import kurtosis as _scipy_kurtosis

from pycvcqv.formulas import (
    _central_moment,
    _g2_bias_corrected,
    _g2_excess_kurtosis,
    _gamma_hat_hummel,
    _kappa_e5,
)

# Note on conventions: pycvcqv implements Abu-Shawiesh, Aky & Kibria
# (2019), Eq. 10 *literally*, using (n - 1) * g_2 + 6 inside the
# bracket. This differs from the standard Fisher-Pearson G_2 returned
# by scipy.stats.kurtosis(bias=False), which uses (n + 1) * g_2 + 6.
# Both are valid "bias-corrected" excess-kurtosis estimators; we keep
# the form from Abu-Shawiesh, Aky & Kibria (2019) so AA&K-LS /
# AA&K-ADJ / AA&K-ALS reproduce their worked examples.

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


def test_central_moment_second_matches_population_variance():
    """The second central moment is the population variance (ddof = 0)."""
    series = pd.Series(SMALL_DATA)
    expected = float(series.var(ddof=0))
    assert _central_moment(series, 2) == pytest.approx(expected)


def test_central_moment_first_is_zero():
    """The first central moment is exactly zero (up to float noise)."""
    series = pd.Series(SMALL_DATA)
    assert _central_moment(series, 1) == pytest.approx(0.0, abs=1e-12)


def test_g2_excess_kurtosis_matches_scipy():
    """g_2 matches scipy.stats.kurtosis(bias=True) which is m_4 / m_2^2 - 3."""
    series = pd.Series(SMALL_DATA)
    expected = float(_scipy_kurtosis(series.to_numpy(), bias=True))
    assert _g2_excess_kurtosis(series) == pytest.approx(expected)


def test_g2_bias_corrected_matches_paper_eq_10_formula():
    """
    G_2 evaluates Abu-Shawiesh, Aky & Kibria (2019), Eq. 10 exactly,
    using (n - 1) * g_2 + 6.
    """
    series = pd.Series(SMALL_DATA)
    n = len(series)
    g_2 = _g2_excess_kurtosis(series)
    expected = (n - 1) / ((n - 2) * (n - 3)) * ((n - 1) * g_2 + 6.0)
    assert _g2_bias_corrected(series) == pytest.approx(expected)


def test_g2_bias_corrected_differs_from_scipy_fisher_pearson():
    """Abu-Shawiesh, Aky & Kibria (2019), Eq. 10 is NOT scipy's Fisher-Pearson G_2.

    scipy.stats.kurtosis(bias=False) uses the Fisher-Pearson form
    (n + 1) * g_2 + 6, which is the more common "bias-corrected"
    convention in software. Abu-Shawiesh, Aky & Kibria (2019) instead
    use (n - 1) * g_2 + 6. This test exists to document the divergence
    (so a future contributor doesn't "fix" pycvcqv to match scipy and
    silently break the AA&K methods' agreement with Abu-Shawiesh, Aky
    & Kibria, 2019).
    """
    series = pd.Series(SMALL_DATA)
    aak_eq_10 = _g2_bias_corrected(series)
    fisher_pearson = float(_scipy_kurtosis(series.to_numpy(), bias=False))
    assert aak_eq_10 != pytest.approx(fisher_pearson)


def test_g2_bias_corrected_too_short_raises():
    """G_2 needs n >= 4 because of (n-2)(n-3) in the denominator."""
    with pytest.raises(ValueError, match="at least 4 observations"):
        _g2_bias_corrected(pd.Series([1.0, 2.0, 3.0]))


def test_kappa_e5_formula_value_normal_sample():
    """kappa_e5 evaluates the Eq. 13 formula exactly."""
    series = pd.Series(SMALL_DATA)
    big_g2 = _g2_bias_corrected(series)
    n = len(series)
    expected = ((n + 1.0) / (n - 1.0)) * big_g2 * (1.0 + 5.0 * big_g2 / n)
    assert _kappa_e5(series) == pytest.approx(expected)


def test_kappa_e5_too_short_propagates_g2_error():
    """kappa_e5 inherits G_2's minimum-length requirement."""
    with pytest.raises(ValueError, match="at least 4 observations"):
        _kappa_e5(pd.Series([1.0, 2.0, 3.0]))


def test_gamma_hat_hummel_matches_eq_5_definition():
    """gamma_hat evaluates Abu-Shawiesh, Aky & Kibria (2019), Eq. 5 exactly."""
    series = pd.Series(SMALL_DATA)
    n = len(series)
    mean = float(series.mean())
    sum_fourth = float(((series - mean) ** 4).sum())
    s_value = float(series.std(ddof=1))
    s_quartic = s_value**4
    first = (n * (n + 1.0) / ((n - 1.0) * (n - 2.0) * (n - 3.0))) * (
        sum_fourth / s_quartic
    )
    second = 3.0 * (n - 1.0) ** 2 / ((n - 2.0) * (n - 3.0))
    expected = first - second
    assert _gamma_hat_hummel(series) == pytest.approx(expected)


def test_gamma_hat_hummel_too_short_raises():
    """gamma_hat needs n >= 4."""
    with pytest.raises(ValueError, match="at least 4 observations"):
        _gamma_hat_hummel(pd.Series([1.0, 2.0, 3.0]))


def test_gamma_hat_hummel_custom_ddof_changes_value():
    """ddof=0 (population variance under-S) gives a different gamma_hat."""
    series = pd.Series(SMALL_DATA)
    default_ddof = _gamma_hat_hummel(series, ddof=1)
    population = _gamma_hat_hummel(series, ddof=0)
    assert not math.isclose(default_ddof, population, rel_tol=1e-9)
