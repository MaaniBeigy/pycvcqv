"""Tests for noncentral t-distribution module."""

# --------------------------- Import libraries and functions --------------------------

from math import isinf

import pytest

from pycvcqv.noncentralt import conf_limits_nct_minimize_scalar


def test_conf_limits_nct_minimize_scalar_all_none():
    """Tests the conf_limits_nct_minimize_scalar when conf_level and alphas are None."""
    result = conf_limits_nct_minimize_scalar(ncp=2.83, dof=126)

    assert result["lower_limit"] == pytest.approx(0.8337502600175457, rel=1e-9)
    assert result["prob_less_lower"] == pytest.approx(0.02499999995262825, rel=1e-9)
    assert result["upper_limit"] == pytest.approx(4.815359140504376, rel=1e-9)
    assert result["prob_greater_upper"] == pytest.approx(0.024999999971943743, rel=1e-9)


def test_conf_limits_nct_minimize_scalar_conf_level_95():
    """Tests the conf_limits_nct_minimize_scalar when conf_level is set to 0.95."""
    result = conf_limits_nct_minimize_scalar(ncp=2.83, dof=126, conf_level=0.95)

    assert result["lower_limit"] == pytest.approx(0.8337502600175457, rel=1e-9)
    assert result["prob_less_lower"] == pytest.approx(0.02499999995262825, rel=1e-9)
    assert result["upper_limit"] == pytest.approx(4.815359140504376, rel=1e-9)
    assert result["prob_greater_upper"] == pytest.approx(0.024999999971943743, rel=1e-9)


def test_conf_limits_nct_minimize_scalar_alpha_lower_0_01_alpha_upper_0_04():
    """Tests the conf_limits_nct_minimize_scalar when alpha levels are non-zero."""
    result = conf_limits_nct_minimize_scalar(
        ncp=2.83, dof=126, conf_level=None, alpha_lower=0.01, alpha_upper=0.04
    )

    assert result["lower_limit"] == pytest.approx(0.46169197879015583, rel=1e-9)
    assert result["prob_less_lower"] == pytest.approx(0.01000000006700108, rel=1e-9)
    assert result["upper_limit"] == pytest.approx(4.602743339958727, rel=1e-9)
    assert result["prob_greater_upper"] == pytest.approx(0.03999999998737774, rel=1e-9)


def test_conf_limits_nct_minimize_scalar_alpha_lower_0_alpha_upper_0_05():
    """Tests the conf_limits_nct_minimize_scalar when alpha_lower is zero."""
    result = conf_limits_nct_minimize_scalar(
        ncp=2.83, dof=126, conf_level=None, alpha_lower=0, alpha_upper=0.05
    )

    assert isinf(result["lower_limit"]) and result["lower_limit"] < 0
    assert result["prob_less_lower"] == 0
    assert result["upper_limit"] == pytest.approx(4.495224841782837, rel=1e-9)
    assert result["prob_greater_upper"] == pytest.approx(0.04999999999219518, rel=1e-9)
