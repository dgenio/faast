"""Tests for the cleaning module"""
import pandas as pd
from life_expectancy.cleaning import clean_data


def test_clean(
        pt_life_expectancy_expected,
        life_expectancy_data
):
    """
    Test clean function
    :param pt_life_expectancy_expected:
    :param life_expectancy_data:
    :return:
    """
    cleaned_data = clean_data(
        wide_data=life_expectancy_data
    )
    pd.testing.assert_frame_equal(
        cleaned_data.reset_index(drop=True), pt_life_expectancy_expected
    )
