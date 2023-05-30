"""Tests for the load_save_data module"""
from unittest import mock
import pandas as pd
from life_expectancy.data_load_save import load_data, save_data
from . import FIXTURES_DIR


def test_load_data(life_expectancy_data):
    """Test the load_data function """
    pt_life_expectancy_input_actual = load_data(
        FIXTURES_DIR / "eu_life_expectancy_input.tsv" )
    pd.testing.assert_frame_equal(
        pt_life_expectancy_input_actual, life_expectancy_data
    )


def test_save_data(pt_life_expectancy_expected):
    """ Test the save_data function """
    with mock.patch.object(
            pt_life_expectancy_expected, "to_csv") as mock_to_csv:
        save_data(pt_life_expectancy_expected)
        mock_to_csv.assert_called_once()
