"""Tests for checkers module."""

# --------------------------- Import libraries and functions --------------------------

from typing import Optional

import pytest

from pycvcqv.checkers import is_dof_positive_natural_number, is_ncp_huge
from pycvcqv.sanitizers import validate_ncp_confidence_level_arguments


@is_dof_positive_natural_number
@is_ncp_huge
@validate_ncp_confidence_level_arguments
def mocked_conf_limits_nct(
    ncp: float,
    dof: int,
    conf_level: Optional[float] = None,
    alpha_lower: Optional[float] = None,
    alpha_upper: Optional[float] = None,
) -> float:
    """Mock function for conf_limits_nct decorator tests."""
    # Ensure alpha_lower and alpha_upper are not None
    if conf_level is None and alpha_lower is None and alpha_upper is None:
        conf_level = 0.95
        alpha_lower = (1 - conf_level) / 2
        alpha_upper = (1 - conf_level) / 2
    if alpha_lower is None or alpha_upper is None:
        raise ValueError(
            "alpha_lower and alpha_upper must not be None after validation."
        )

    return (ncp * dof) * (alpha_lower + alpha_upper)


def test_mocked_conf_limits_nct_positive_natural_dof_kwarg():
    """Tests mocked_conf_limits_nct function for positive natural dof kwarg."""
    assert mocked_conf_limits_nct(
        ncp=10.0,
        dof=1,
    ) == pytest.approx(10 * 0.05, 0.1)


def test_mocked_conf_limits_nct_positive_natural_dof_arg():
    """Tests mocked_conf_limits_nct function for positive natural dof arg."""
    assert mocked_conf_limits_nct(
        10.0,
        1,
    ) == pytest.approx(10 * 0.05, 0.1)


def test_mocked_conf_limits_nct_non_positive_natural_dof_kwarg():
    """Tests mocked_conf_limits_nct function for positive natural dof kwarg."""
    with pytest.raises(ValueError) as execinfo:
        mocked_conf_limits_nct(
            ncp=10.0,
            dof=-1,
        )

    assert execinfo.value.args[0] == "Argument dof should be a positive natural number!"


def test_mocked_conf_limits_nct_non_positive_natural_dof_arg():
    """Tests mocked_conf_limits_nct function for positive natural dof arg."""
    with pytest.raises(ValueError) as execinfo:
        mocked_conf_limits_nct(
            10.0,
            -1,
        )

    assert execinfo.value.args[0] == "Argument dof should be a positive natural number!"


def test_mocked_conf_limits_nct_ncp_within_limit():
    """Tests mocked_conf_limits_nct with ncp within the limit."""
    assert mocked_conf_limits_nct(37.0, 1) == pytest.approx(37.0 * 0.05, 0.1)
    assert mocked_conf_limits_nct(37.0, dof=2) == pytest.approx(74.0 * 0.05, 0.1)


def test_mocked_conf_limits_nct_ncp_exceeds_limit():
    """Tests mocked_conf_limits_nct with ncp exceeding the limit."""
    with pytest.warns(
        RuntimeWarning,
        match="The noncentrality parameter exceeds 37.62, which may affect accuracy.",
    ):
        assert mocked_conf_limits_nct(38.0, 1) == pytest.approx(38.0 * 0.05, 0.1)
        assert mocked_conf_limits_nct(38.0, dof=2) == pytest.approx(76.0 * 0.05, 0.1)


def test_mocked_conf_limits_nct_ncp_negative_within_limit():
    """Tests mocked_conf_limits_nct with negative ncp within the limit."""
    assert mocked_conf_limits_nct(-37.0, 1) == pytest.approx(-37.0 * 0.05, 0.1)
    assert mocked_conf_limits_nct(-37.0, dof=2) == pytest.approx(-74.0 * 0.05, 0.1)


def test_mocked_conf_limits_nct_ncp_negative_exceeds_limit():
    """Tests mocked_conf_limits_nct with negative ncp exceeding the limit."""
    with pytest.warns(
        RuntimeWarning,
        match="The noncentrality parameter exceeds 37.62, which may affect accuracy.",
    ):
        assert mocked_conf_limits_nct(-38.0, 1) == pytest.approx(-38.0 * 0.05, 0.1)
        assert mocked_conf_limits_nct(-38.0, dof=2) == pytest.approx(-76.0 * 0.05, 0.1)


def test_default_conf_level():
    """Test case where no conf_level, alpha_lower, or alpha_upper are provided."""
    result = mocked_conf_limits_nct(2.0, 100)
    expected_alpha = (1 - 0.95) / 2
    assert result == (2.0 * 100) * (expected_alpha * 2)


def test_given_alpha_values():
    """Test case where alpha_lower and alpha_upper are provided."""
    result = mocked_conf_limits_nct(2.0, 100, alpha_lower=0.01, alpha_upper=0.02)
    assert result == (2.0 * 100) * (0.01 + 0.02)


def test_given_conf_level_and_alpha_raises_error():
    """Test case where only one of alpha_lower or alpha_upper is provided."""
    with pytest.raises(ValueError) as execinfo:
        mocked_conf_limits_nct(2.0, 100, alpha_lower=0.01)
    assert (
        execinfo.value.args[0]
        == "Both alpha_lower and alpha_upper must be provided or both None."
    )


def test_invalid_alpha_lower():
    """Test case where alpha_lower is out of the [0, 1] range."""
    with pytest.raises(ValueError) as execinfo:
        mocked_conf_limits_nct(2.0, 100, alpha_lower=-0.1, alpha_upper=0.02)
    assert (
        execinfo.value.args[0]
        == "conf_level and alpha values must be in the range [0, 1]."
    )


def test_invalid_alpha_upper():
    """Test case where alpha_upper is out of the [0, 1] range."""
    with pytest.raises(ValueError) as execinfo:
        mocked_conf_limits_nct(2.0, 100, alpha_lower=0.01, alpha_upper=1.2)
    assert (
        execinfo.value.args[0]
        == "conf_level and alpha values must be in the range [0, 1]."
    )


def test_invalid_conf_level():
    """Test case where conf_level is out of the [0, 1] range."""
    with pytest.raises(ValueError) as execinfo:
        mocked_conf_limits_nct(
            ncp=2.0, dof=100, conf_level=1.5, alpha_lower=0.01, alpha_upper=0.95
        )
    assert (
        execinfo.value.args[0]
        == "conf_level and alpha values must be in the range [0, 1]."
    )
