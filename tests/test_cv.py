"""Tests for cv function."""
# --------------------------- Import libraries and functions --------------------------
import pandas as pd
import pytest

from pycvcqv.cv import coefficient_of_variation


def test_cv_with_kwarg():
    """test cv function without correction with data kwarg"""
    assert (
        coefficient_of_variation(
            data=pd.Series(
                [
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
            ),
            multiplier=100,
        )
        == pytest.approx(57.77, 0.001)
    )


def test_cv_without_kwarg():
    """test cv function without correction without data kwarg"""
    assert (
        coefficient_of_variation(
            [
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
            ],
            multiplier=100,
        )
        == pytest.approx(57.77, 0.001)
    )


def test_cv_corrected():
    """test cv function with correction"""
    assert (
        coefficient_of_variation(
            data=pd.Series(
                [
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
            ),
            correction=True,
            multiplier=100,
        )
        == pytest.approx(58.05, 0.001)
    )


def test_cv_nonnumeric_type_data_with_kwarg():
    """test cv function with nonnumeric type of data with kwarg"""
    with pytest.raises(TypeError) as execinfo:
        coefficient_of_variation(
            data=pd.Series(["0.2", "0.5", "1.1", "1.4", "1.8", "2.3", "2.5", " 2.7"]),
            correction=True,
            multiplier=100,
        )

    assert execinfo.value.args[0] == "The data is not numeric!"


def test_cv_nonnumeric_type_data_without_kwarg():
    """test cv function with nonnumeric type of data without kwarg"""
    with pytest.raises(TypeError) as execinfo:
        coefficient_of_variation(
            ["0.2", "0.5", "1.1", "1.4", "1.8", "2.3", "2.5", " 2.7"],
            correction=True,
            multiplier=100,
        )

    assert execinfo.value.args[0] == "The data is not numeric!"


def test_cv_wrong_type_data_with_kwarg():
    """test cv function with wrong type of data with kwarg"""
    with pytest.raises(TypeError) as execinfo:
        coefficient_of_variation(
            data={
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
            },
            correction=True,
            multiplier=100,
        )

    assert (
        execinfo.value.args[0]
        == """data must be \
pandas.core.series.Series, numpy.ndarray, list, or tuple!"""
    )


def test_cv_wrong_type_data_without_kwarg():
    """test cv function with wrong type of data without kwarg"""
    with pytest.raises(TypeError) as execinfo:
        coefficient_of_variation(
            {
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
            },
            correction=True,
            multiplier=100,
        )

    assert (
        execinfo.value.args[0]
        == """data must be \
pandas.core.series.Series, numpy.ndarray, list, or tuple!"""
    )
