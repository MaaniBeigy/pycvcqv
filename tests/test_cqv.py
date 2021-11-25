"""Tests for cqv function."""
# --------------------------- Import libraries and functions --------------------------
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from pycvcqv.cqv import cqv


def test_cqv_with_kwarg():
    """Tests cqv function with data kwarg."""
    assert (
        cqv(
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
        == pytest.approx(45.625, 0.001)
    )


def test_cqv_without_kwarg():
    """Tests cqv function without data kwarg."""
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


def test_cqv_nonnumeric_type_data_with_kwarg():
    """Tests cqv function with nonnumeric type of data with kwarg."""
    with pytest.raises(TypeError) as execinfo:
        cqv(
            data=pd.Series(["0.2", "0.5", "1.1", "1.4", "1.8", "2.3", "2.5", " 2.7"]),
            multiplier=100,
        )

    assert execinfo.value.args[0] == "The data is not numeric!"


def test_cqv_nonnumeric_type_data_without_kwarg():
    """Tests cqv function with nonnumeric type of data without kwarg."""
    with pytest.raises(TypeError) as execinfo:
        cqv(
            ["0.2", "0.5", "1.1", "1.4", "1.8", "2.3", "2.5", " 2.7"],
            multiplier=100,
        )

    assert execinfo.value.args[0] == "The data is not numeric!"


def test_cqv_wrong_type_data_with_kwarg():
    """Tests cvq function with wrong type of data with kwarg."""
    with pytest.raises(TypeError) as execinfo:
        cqv(
            data=dict({"1": 2}),
            multiplier=100,
        )

    assert (
        execinfo.value.args[0]
        == """data must be \
pandas.core.series.Series, numpy.ndarray, list, or tuple!"""
    )


def test_cqv_wrong_type_data_without_kwarg():
    """Tests cqv function with wrong type of data without kwarg."""
    with pytest.raises(TypeError) as execinfo:
        cqv(
            dict({"1": 2}),
            multiplier=100,
        )

    assert (
        execinfo.value.args[0]
        == """data must be \
pandas.core.series.Series, numpy.ndarray, list, or tuple!"""
    )


def test_cqv_warning_when_divisor_makes_cqv_nan_without_kwargs():
    """Tests cqv function when divisor makes cqv nan without kwargs."""
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


def test_cqv_warning_when_divisor_makes_cqv_nan_with_kwargs():
    """Tests cqv function when divisor makes cqv nan with kwargs."""
    with pytest.raises(Warning) as execinfo:
        cqv(
            data=pd.Series(
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


def test_cqv_without_kwarg_raise_warning():
    """Tests cqv function without data kwarg raise warning."""
    with pytest.raises(Warning) as execinfo:
        cqv(
            [
                0.1,
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
            ],
            multiplier=100,
        )
    assert execinfo.value.args[0] == "cqv is NaN because q3 and q1 are 0"


def test_cqv_dataframe_single_thread_default():
    """Tests cqv function for dataframe when num_threads is default."""
    data = pd.DataFrame(
        {
            "col-1": pd.Series([0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]),
            "col-2": pd.Series([5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9]),
        }
    )
    result = cqv(data=data)
    assert_frame_equal(
        result,
        pd.DataFrame(
            {
                "columns": pd.Series(["col-1", "col-2"]),
                "cv": pd.Series([0.3889, 0.0732]),
            }
        ),
    )


def test_cqv_dataframe_zerothread():
    """Tests cqv function for dataframe when num_threads is zero."""
    data = pd.DataFrame(
        {
            "col-1": pd.Series([0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]),
            "col-2": pd.Series([5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9]),
        }
    )
    result = cqv(data=data, num_threads=0)
    assert_frame_equal(
        result,
        pd.DataFrame(
            {
                "columns": pd.Series(["col-1", "col-2"]),
                "cv": pd.Series([0.3889, 0.0732]),
            }
        ),
    )


def test_cqv_dataframe_multithread():
    """Tests cqv function for dataframe when num_threads is multi."""
    data = pd.DataFrame(
        {
            "col-1": pd.Series([0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]),
            "col-2": pd.Series([5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9]),
        }
    )
    result = cqv(data=data, num_threads=-1)
    assert_frame_equal(
        result,
        pd.DataFrame(
            {
                "columns": pd.Series(["col-1", "col-2"]),
                "cv": pd.Series([0.3889, 0.0732]),
            }
        ),
    )


def test_cqv_dataframe_multithread_3_threads():
    """Tests cqv function for dataframe when num_threads is multi."""
    data = pd.DataFrame(
        {
            "col-1": pd.Series([0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]),
            "col-2": pd.Series([5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9]),
        }
    )
    result = cqv(data=data, num_threads=3)
    assert_frame_equal(
        result,
        pd.DataFrame(
            {
                "columns": pd.Series(["col-1", "col-2"]),
                "cv": pd.Series([0.3889, 0.0732]),
            }
        ),
    )
