"""Tests for checkers module."""

# --------------------------- Import libraries and functions --------------------------

import pytest

from pycvcqv.checkers import is_dof_positive_natural_number, is_ncp_huge


@is_dof_positive_natural_number
@is_ncp_huge
def mocked_conf_limits_nct(ncp: float, dof: int) -> float:
    """Mock function for conf_limits_nct decorator tests."""
    return ncp * dof


def test_mocked_conf_limits_nct_positive_natural_dof_kwarg():
    """Tests mocked_conf_limits_nct function for positive natural dof kwarg."""
    assert mocked_conf_limits_nct(
        ncp=10.0,
        dof=1,
    ) == pytest.approx(10, 0.1)


def test_mocked_conf_limits_nct_positive_natural_dof_arg():
    """Tests mocked_conf_limits_nct function for positive natural dof arg."""
    assert mocked_conf_limits_nct(
        10.0,
        1,
    ) == pytest.approx(10, 0.1)


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
    assert mocked_conf_limits_nct(37.0, 1) == pytest.approx(37.0, 0.1)
    assert mocked_conf_limits_nct(37.0, dof=2) == pytest.approx(74.0, 0.1)


def test_mocked_conf_limits_nct_ncp_exceeds_limit():
    """Tests mocked_conf_limits_nct with ncp exceeding the limit."""
    with pytest.warns(
        RuntimeWarning,
        match="The noncentrality parameter exceeds 37.62, which may affect accuracy.",
    ):
        assert mocked_conf_limits_nct(38.0, 1) == pytest.approx(38.0, 0.1)
        assert mocked_conf_limits_nct(38.0, dof=2) == pytest.approx(76.0, 0.1)


def test_mocked_conf_limits_nct_ncp_negative_within_limit():
    """Tests mocked_conf_limits_nct with negative ncp within the limit."""
    assert mocked_conf_limits_nct(-37.0, 1) == pytest.approx(-37.0, 0.1)
    assert mocked_conf_limits_nct(-37.0, dof=2) == pytest.approx(-74.0, 0.1)


def test_mocked_conf_limits_nct_ncp_negative_exceeds_limit():
    """Tests mocked_conf_limits_nct with negative ncp exceeding the limit."""
    with pytest.warns(
        RuntimeWarning,
        match="The noncentrality parameter exceeds 37.62, which may affect accuracy.",
    ):
        assert mocked_conf_limits_nct(-38.0, 1) == pytest.approx(-38.0, 0.1)
        assert mocked_conf_limits_nct(-38.0, dof=2) == pytest.approx(-76.0, 0.1)
