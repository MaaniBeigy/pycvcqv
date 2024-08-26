"""Tests for kelley module."""

# --------------------------- Import libraries and functions --------------------------
import pandas as pd
from pandas.testing import assert_frame_equal

from pycvcqv.cv import coefficient_of_variation
from pycvcqv.cv_confidence_interval import _cv_confidence_intervals


def test_cv_dataframe_kelley():
    """Tests cv function with kelley CI method for dataframe."""
    data = pd.DataFrame(
        {
            "col-1": pd.Series([0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]),
            "col-2": pd.Series([5.4, 5.4, 5.7, 5.8, 5.9, 6.0, 6.6, 7.1, 7.9]),
        }
    )
    result = coefficient_of_variation(data=data, num_threads=0, method="kelley")
    assert_frame_equal(
        result,
        pd.DataFrame(
            {
                "columns": pd.Series(["col-1", "col-2"]),
                "cv": pd.Series([0.6076, 0.1359]),
                "lower": pd.Series([0.377, 0.0913]),
                "upper": pd.Series([1.6667, 0.2651]),
            }
        ),
    )


def test_cv_dataframe_cv_confidence_intervals():
    """Tests _cv_confidence_intervals function with kelley CI method for dataframe."""
    data = [0.2, 0.5, 1.1, 1.4, 1.8, 2.3, 2.5, 2.7, 3.5]
    result = _cv_confidence_intervals(data=data, method="kelley")
    assert result == {"cv": 0.6076, "lower": 0.377, "upper": 1.6667}
