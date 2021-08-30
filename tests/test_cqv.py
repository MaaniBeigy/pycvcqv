"""Tests for cqv function."""
# --------------------------- Import libraries and functions --------------------------
import pandas as pd
import pytest

from pycvcqv.cqv import cqv


def test_cqv_with_kwarg():
    """test cqv function with numeric_vector kwarg"""
    assert (
        cqv(
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
        == pytest.approx(45.625, 0.001)
    )


def test_cqv_without_kwarg():
    """test cv function without numeric_vector kwarg"""
    assert (
        cqv(
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
        == pytest.approx(45.625, 0.001)
    )


def test_cqv_nonnumeric_type_vector_with_kwarg():
    """test cqv function with nonnumeric type of numeric_vector with kwarg"""
    with pytest.raises(TypeError) as execinfo:
        cqv(
            numeric_vector=pd.Series(
                ["0.2", "0.5", "1.1", "1.4", "1.8", "2.3", "2.5", " 2.7"]
            ),
            multiplier=100,
        )

    assert execinfo.value.args[0] == "The vector is not numeric!"


def test_cqv_nonnumeric_type_numeric_vector_without_kwarg():
    """test cqv function with nonnumeric type of numeric_vector without kwarg"""
    with pytest.raises(TypeError) as execinfo:
        cqv(
            ["0.2", "0.5", "1.1", "1.4", "1.8", "2.3", "2.5", " 2.7"],
            multiplier=100,
        )

    assert execinfo.value.args[0] == "The vector is not numeric!"


def test_cqv_wrong_type_numeric_vector_with_kwarg():
    """test cvq function with wrong type of numeric_vector with kwarg"""
    with pytest.raises(TypeError) as execinfo:
        cqv(
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
            multiplier=100,
        )

    assert (
        execinfo.value.args[0]
        == """numeric_vector must be \
pandas.core.series.Series, numpy.ndarray, list, or tuple!"""
    )


def test_cqv_wrong_type_numeric_vector_without_kwarg():
    """test cqv function with wrong type of numeric_vector without kwarg"""
    with pytest.raises(TypeError) as execinfo:
        cqv(
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
            multiplier=100,
        )

    assert (
        execinfo.value.args[0]
        == """numeric_vector must be \
pandas.core.series.Series, numpy.ndarray, list, or tuple!"""
    )


def test_cqv_warning_when_divisor_makes_cqv_nan():
    """test cqv function when divisor makes cqv nan"""
    with pytest.raises(Warning) as execinfo:
        cqv(
            pd.Series(
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1771,
                    0,
                    0,
                    106,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    84,
                    168,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    124,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    127,
                    0,
                    0,
                    0,
                    100,
                    0,
                    0,
                    0,
                    0,
                    0,
                    104,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    554,
                    1174,
                    0,
                    0,
                    0,
                    0,
                    8,
                    0,
                    0,
                    0,
                    0,
                    263,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    2,
                    130,
                    0,
                    0,
                    0,
                    272,
                    0,
                    0,
                    0,
                    0,
                    42,
                    0,
                    0,
                    130,
                    0,
                    0,
                    0,
                    0,
                    0,
                    9,
                    0,
                    0,
                    2,
                    0,
                    0,
                    0,
                    0,
                    0,
                    826,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    231,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    522,
                    2313,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    836,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    49,
                    1176,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ]
            )
        )

    assert execinfo.value.args[0] == "cqv is NaN because q3 and q1 are 0"
