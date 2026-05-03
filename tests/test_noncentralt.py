"""Tests for noncentral t-distribution module."""

# --------------------------- Import libraries and functions --------------------------

from math import isinf

import pytest

from pycvcqv.noncentralt import (
    conf_limits_nct,
    conf_limits_nct_minimize,
    conf_limits_nct_minimize_scalar,
)


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


def test_conf_limits_nct_minimize_all_none():
    """Tests the conf_limits_nct_minimize when conf_level and alphas are None."""
    result = conf_limits_nct_minimize(ncp=2.83, dof=126)

    assert result["lower_limit"] == pytest.approx(0.833750253390236, rel=1e-9)
    assert result["prob_less_lower"] == pytest.approx(0.024999999571209908, rel=1e-9)
    assert result["upper_limit"] == pytest.approx(4.815359132565956, rel=1e-9)
    assert result["prob_greater_upper"] == pytest.approx(0.025000000428616057, rel=1e-9)


def test_conf_limits_nct_minimize_conf_level_95():
    """Tests the conf_limits_nct_minimize when conf_level is set to 0.95."""
    result = conf_limits_nct_minimize(ncp=2.83, dof=126, conf_level=0.95)

    assert result["lower_limit"] == pytest.approx(0.833750253390236, rel=1e-9)
    assert result["prob_less_lower"] == pytest.approx(0.024999999571209908, rel=1e-9)
    assert result["upper_limit"] == pytest.approx(4.815359132565956, rel=1e-9)
    assert result["prob_greater_upper"] == pytest.approx(0.025000000428616057, rel=1e-9)


def test_conf_limits_nct_minimize_alpha_lower_0_01_alpha_upper_0_04():
    """Tests the conf_limits_nct_minimize when alpha levels are non-zero.

    The fixture values match the conf_limits_nct_minimize_scalar reference (the
    two methods should converge to the same NCP) with a slightly looser
    tolerance to account for the different optimizer (minimize vs.
    minimize_scalar/Brent). Previously this test was locked to the output of a
    copy-paste bug that fed valid_alpha_upper into the lower-limit objective;
    the expected values were updated when that bug was fixed.
    """
    result = conf_limits_nct_minimize(
        ncp=2.83, dof=126, conf_level=None, alpha_lower=0.01, alpha_upper=0.04
    )

    assert result["lower_limit"] == pytest.approx(0.46169197879015583, rel=1e-4)
    assert result["prob_less_lower"] == pytest.approx(0.01, abs=1e-6)
    assert result["upper_limit"] == pytest.approx(4.602743332359321, rel=1e-4)
    assert result["prob_greater_upper"] == pytest.approx(0.04, abs=1e-6)


def test_conf_limits_nct_minimize_alpha_lower_0_alpha_upper_0_05():
    """Tests the conf_limits_nct_minimize when alpha_lower is zero."""
    result = conf_limits_nct_minimize(
        ncp=2.83, dof=126, conf_level=None, alpha_lower=0, alpha_upper=0.05
    )

    assert isinf(result["lower_limit"]) and result["lower_limit"] < 0
    assert result["prob_less_lower"] == 0
    assert result["upper_limit"] == pytest.approx(4.495224834255373, rel=1e-9)
    assert result["prob_greater_upper"] == pytest.approx(0.05000000075637537, rel=1e-9)


def test_conf_limits_nct_all_none():
    """Tests the conf_limits_nct when conf_level and alphas are None."""
    result = conf_limits_nct(ncp=2.83, dof=126)

    assert result["lower_limit"] == pytest.approx(0.8337502600175457, rel=1e-9)
    assert result["prob_less_lower"] == pytest.approx(0.02499999995262825, rel=1e-9)
    assert result["upper_limit"] == pytest.approx(4.815359140504376, rel=1e-9)
    assert result["prob_greater_upper"] == pytest.approx(0.024999999971943743, rel=1e-9)


def test_conf_limits_nct_conf_level_95():
    """Tests the conf_limits_nct when conf_level is set to 0.95."""
    result = conf_limits_nct(ncp=2.83, dof=126, conf_level=0.95)

    assert result["lower_limit"] == pytest.approx(0.8337502600175457, rel=1e-9)
    assert result["prob_less_lower"] == pytest.approx(0.02499999995262825, rel=1e-9)
    assert result["upper_limit"] == pytest.approx(4.815359140504376, rel=1e-9)
    assert result["prob_greater_upper"] == pytest.approx(0.024999999971943743, rel=1e-9)


def test_conf_limits_nct_alpha_lower_0_01_alpha_upper_0_04():
    """Tests the conf_limits_nct when alpha levels are non-zero."""
    result = conf_limits_nct(
        ncp=2.83, dof=126, conf_level=None, alpha_lower=0.01, alpha_upper=0.04
    )

    assert result["lower_limit"] == pytest.approx(0.46169197879015583, rel=1e-9)
    assert result["prob_less_lower"] == pytest.approx(0.01000000006700108, rel=1e-9)
    assert result["upper_limit"] == pytest.approx(4.602743339958727, rel=1e-9)
    assert result["prob_greater_upper"] == pytest.approx(0.03999999998737774, rel=1e-9)


def test_conf_limits_nct_alpha_lower_0_alpha_upper_0_05():
    """Tests the conf_limits_nct when alpha_lower is zero."""
    result = conf_limits_nct(
        ncp=2.83, dof=126, conf_level=None, alpha_lower=0, alpha_upper=0.05
    )

    assert isinf(result["lower_limit"]) and result["lower_limit"] < 0
    assert result["prob_less_lower"] == 0
    assert result["upper_limit"] == pytest.approx(4.495224841782837, rel=1e-9)
    assert result["prob_greater_upper"] == pytest.approx(0.04999999999219518, rel=1e-9)


# The next three tests exercise the symmetric `alpha_upper == 0` branch in each
# of the three NCP confidence-interval functions. Without them, the
# `ncp_upper_limit = np.inf` line is unreached (the existing tests above only
# cover `alpha_lower == 0`). Assertions are semantic — we check that the upper
# tail collapses to +inf with prob 0 and that the lower tail converges to the
# requested alpha — instead of locking to magic numbers, so they're robust
# across optimizer-version differences.
def test_conf_limits_nct_minimize_scalar_alpha_lower_0_05_alpha_upper_0():
    """Tests the conf_limits_nct_minimize_scalar when alpha_upper is zero."""
    ncp = 2.83
    result = conf_limits_nct_minimize_scalar(
        ncp=ncp, dof=126, conf_level=None, alpha_lower=0.05, alpha_upper=0
    )

    # Upper tail: alpha=0 ⇒ +inf, no probability mass beyond it.
    assert isinf(result["upper_limit"]) and result["upper_limit"] > 0
    assert result["prob_greater_upper"] == 0
    # Lower tail: optimizer should drive prob_less_lower to ≈alpha_lower (0.05),
    # and the bound must be finite and below ncp.
    assert result["prob_less_lower"] == pytest.approx(0.05, abs=1e-6)
    assert result["lower_limit"] < ncp
    assert not isinf(result["lower_limit"])


def test_conf_limits_nct_minimize_alpha_lower_0_05_alpha_upper_0():
    """Tests the conf_limits_nct_minimize when alpha_upper is zero."""
    ncp = 2.83
    result = conf_limits_nct_minimize(
        ncp=ncp, dof=126, conf_level=None, alpha_lower=0.05, alpha_upper=0
    )

    assert isinf(result["upper_limit"]) and result["upper_limit"] > 0
    assert result["prob_greater_upper"] == 0
    assert result["prob_less_lower"] == pytest.approx(0.05, abs=1e-6)
    assert result["lower_limit"] < ncp
    assert not isinf(result["lower_limit"])


def test_conf_limits_nct_alpha_lower_0_05_alpha_upper_0():
    """Tests the conf_limits_nct (combined) when alpha_upper is zero."""
    ncp = 2.83
    result = conf_limits_nct(
        ncp=ncp, dof=126, conf_level=None, alpha_lower=0.05, alpha_upper=0
    )

    assert isinf(result["upper_limit"]) and result["upper_limit"] > 0
    assert result["prob_greater_upper"] == 0
    assert result["prob_less_lower"] == pytest.approx(0.05, abs=1e-6)
    assert result["lower_limit"] < ncp
    assert not isinf(result["lower_limit"])
