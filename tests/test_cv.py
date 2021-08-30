"""Tests for cv function."""
# --------------------------- Import libraries and functions --------------------------
import pandas as pd
import pytest

from pycvcqv.cv import cv


def test_cv_with_kwarg():
    """test cv function without correction with numeric_vector kwarg"""
    assert (
        cv(
            numeric_vector=pd.Series(
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
    """test cv function without correction without numeric_vector kwarg"""
    assert (
        cv(
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
        cv(
            numeric_vector=pd.Series(
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


def test_cv_nonnumeric_type_numeric_vector_with_kwarg():
    """test cv function with nonnumeric type of numeric_vector with kwarg"""
    with pytest.raises(TypeError) as execinfo:
        cv(
            numeric_vector=pd.Series(
                ["0.2", "0.5", "1.1", "1.4", "1.8", "2.3", "2.5", " 2.7"]
            ),
            correction=True,
            multiplier=100,
        )

    assert execinfo.value.args[0] == "The vector is not numeric!"


def test_cv_nonnumeric_type_numeric_vector_without_kwarg():
    """test cv function with nonnumeric type of numeric_vector without kwarg"""
    with pytest.raises(TypeError) as execinfo:
        cv(
            ["0.2", "0.5", "1.1", "1.4", "1.8", "2.3", "2.5", " 2.7"],
            correction=True,
            multiplier=100,
        )

    assert execinfo.value.args[0] == "The vector is not numeric!"


def test_cv_wrong_type_numeric_vector_with_kwarg():
    """test cv function with wrong type of numeric_vector with kwarg"""
    with pytest.raises(TypeError) as execinfo:
        cv(
            numeric_vector={
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
        == """numeric_vector must be \
pandas.core.series.Series, numpy.ndarray, list, or tuple!"""
    )


def test_cv_wrong_type_numeric_vector_without_kwarg():
    """test cv function with wrong type of numeric_vector without kwarg"""
    with pytest.raises(TypeError) as execinfo:
        cv(
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
        == """numeric_vector must be \
pandas.core.series.Series, numpy.ndarray, list, or tuple!"""
    )
