"""Tests for cv function."""

# --------------------------- Import libraries and functions --------------------------
import pandas as pd
import pytest
from numpy import inf
from pandas.testing import assert_frame_equal

from pycvcqv.cv import coefficient_of_variation


def test_cv_with_kwarg():
    """Tests cv function without correction with data kwarg."""
    assert coefficient_of_variation(
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
    ) == pytest.approx(57.77, 0.001)


def test_cv_without_kwarg():
    """Tests cv function without correction without data kwarg."""
    assert coefficient_of_variation(
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
    ) == pytest.approx(57.77, 0.001)


def test_cv_corrected():
    """Tests cv function with correction."""
    assert coefficient_of_variation(
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
    ) == pytest.approx(58.05, 0.001)


def test_cv_nonnumeric_type_data_with_kwarg():
    """Tests cv function with nonnumeric type of data with kwarg."""
    with pytest.raises(TypeError) as execinfo:
        coefficient_of_variation(
            data=pd.Series(["0.2", "0.5", "1.1", "1.4", "1.8", "2.3", "2.5", " 2.7"]),
            correction=True,
            multiplier=100,
        )

    assert execinfo.value.args[0] == "The data is not numeric!"


def test_cv_nonnumeric_type_data_without_kwarg():
    """Tests cv function with nonnumeric type of data without kwarg."""
    with pytest.raises(TypeError) as execinfo:
        coefficient_of_variation(
            ["0.2", "0.5", "1.1", "1.4", "1.8", "2.3", "2.5", " 2.7"],
            correction=True,
            multiplier=100,
        )

    assert execinfo.value.args[0] == "The data is not numeric!"


def test_cv_dataframe_single_thread():
    """Tests cv function for dataframe when num_threads is default."""
    data = pd.DataFrame(
        {
            "col-1": pd.Series([0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]),
            "col-2": pd.Series([5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9]),
        }
    )
    result = coefficient_of_variation(data)
    assert_frame_equal(
        result,
        pd.DataFrame(
            {
                "columns": pd.Series(["col-1", "col-2"]),
                "cv": pd.Series([0.6076, 0.1359]),
            }
        ),
    )


def test_cv_dataframe_zerothread():
    """Tests cv function for dataframe when num_threads is zero."""
    data = pd.DataFrame(
        {
            "col-1": pd.Series([0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]),
            "col-2": pd.Series([5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9]),
        }
    )
    result = coefficient_of_variation(data=data, num_threads=0)
    assert_frame_equal(
        result,
        pd.DataFrame(
            {
                "columns": pd.Series(["col-1", "col-2"]),
                "cv": pd.Series([0.6076, 0.1359]),
            }
        ),
    )


def test_cv_dataframe_multithread():
    """Tests cv function for dataframe when num_threads is multi."""
    data = pd.DataFrame(
        {
            "col-1": pd.Series([0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]),
            "col-2": pd.Series([5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9]),
        }
    )
    result = coefficient_of_variation(data=data, num_threads=-1)
    assert_frame_equal(
        result,
        pd.DataFrame(
            {
                "columns": pd.Series(["col-1", "col-2"]),
                "cv": pd.Series([0.6076, 0.1359]),
            }
        ),
    )


def test_cv_dataframe_multithread_default_3_cores():
    """Tests cv function for dataframe when num_threads is multi."""
    data = pd.DataFrame(
        {
            "col-1": pd.Series([0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]),
            "col-2": pd.Series([5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9]),
        }
    )
    result = coefficient_of_variation(data=data, num_threads=3)
    assert_frame_equal(
        result,
        pd.DataFrame(
            {
                "columns": pd.Series(["col-1", "col-2"]),
                "cv": pd.Series([0.6076, 0.1359]),
            }
        ),
    )


def test_zero_division_cv_returns_none_with_kwargs():
    """Tests cv function for zero division with kwargs."""
    assert coefficient_of_variation(data=[-2, -1, 0, 1, 2]) == float("inf")


def test_zero_division_cv_returns_none_without_kwargs():
    """Tests cv function for zero division without kwargs."""
    assert coefficient_of_variation([-2, -1, 0, 1, 2]) == float("inf")


def test_zero_division_cv_returns_none_without_kwargs_dataframe():
    """Tests cv function for zero division for dataframe."""
    data = pd.DataFrame(
        {
            "col-1": pd.Series([-2, -1, 0, 1, 2]),
            "col-2": pd.Series([-2, -1, 0, 1, 2]),
        }
    )
    result = coefficient_of_variation(data=data, num_threads=3)
    assert_frame_equal(
        result,
        pd.DataFrame(
            {
                "columns": pd.Series(["col-1", "col-2"]),
                "cv": pd.Series([float(inf), float(inf)]),
            }
        ),
    )


def test_zero_division_cv_returns_none_when_std_is_high():
    """Tests cv function for zero division when std is high."""
    vector = [
        -1.687949,
        -1.556078,
        -1.292336,
        -1.160465,
        -0.984637,
        -0.764852,
        -0.676938,
        -0.589024,
        -0.237368,
        0.158245,
        0.246159,
        0.597815,
        0.597815,
        0.729686,
        0.773643,
        0.817600,
        0.861557,
        1.125299,
        1.345084,
        1.696740,
    ]
    assert coefficient_of_variation(data=vector) == float("inf")
