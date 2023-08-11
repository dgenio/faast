"""Tests for the load_save_data module"""
from os.path import join
from unittest import mock

import pandas as pd
import pytest

from life_expectancy.loading_strategies import (
    DataLoader, JSONLoadStrategy, create_strategy, TSVLoadStrategy,
    get_current_directory_full_path, get_file_extension)
from life_expectancy.save_data import save_data

from . import FIXTURES_DIR


def test_load_data(life_expectancy_data):
    """Test the load_data function """
    pt_life_expectancy_input_actual = DataLoader.load_data(
        file_path=FIXTURES_DIR / "eu_life_expectancy_input.tsv"
    )
    pd.testing.assert_frame_equal(
        pt_life_expectancy_input_actual, life_expectancy_data
    )


def test_save_data(pt_life_expectancy_expected):
    """ Test the save_data function """
    with mock.patch.object(
            pt_life_expectancy_expected, "to_csv") as mock_to_csv:
        save_data(pt_life_expectancy_expected)
        mock_to_csv.assert_called_once()


def test_tsv_load_strategy_default_path():
    strategy = TSVLoadStrategy()
    with mock.patch('pandas.read_csv') as mock_read_csv:
        strategy.load_data()
        expected_path = join(get_current_directory_full_path(), "data", "eu_life_expectancy_raw.tsv")
        mock_read_csv.assert_called_with(expected_path, sep="\t", header=0)


def test_default_json_file_path():
    strategy = JSONLoadStrategy()
    data = strategy.load_data()
    assert isinstance(data, pd.DataFrame)
    # You can add more assertions based on the expected content of the default file.


def test_create_strategy_for_tsv():
    strategy = create_strategy(".tsv")
    assert isinstance(strategy, TSVLoadStrategy)


def test_create_strategy_for_json():
    strategy = create_strategy(".json")
    assert isinstance(strategy, JSONLoadStrategy)


def test_create_strategy_with_unsupported_extension():
    with pytest.raises(ValueError) as excinfo:
        create_strategy(".unsupported_extension")
    assert str(excinfo.value) == "File format .unsupported_extension not supported"


def test_load_data_without_file_path():
    # Test that a ValueError is raised when no file_path is provided
    with pytest.raises(ValueError, match="Input file not specified"):
        DataLoader.load_data(file_path=None)


def test_get_file_extension():
    # Test that the correct file extension is returned
    file_path = "example_file.tsv"
    expected_extension = ".tsv"
    assert get_file_extension(file_path) == expected_extension
