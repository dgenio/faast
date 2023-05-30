"""Tests for the main module"""
from unittest import mock
import pandas as pd
from life_expectancy.main import main
from . import FIXTURES_DIR


def test_main(pt_life_expectancy_expected):
    """Run the `main` function and compare the output to the expected output"""
    with mock.patch.object(pd.DataFrame, "to_csv") as mock_to_csv:
        mock_to_csv.side_effect = print("Message: Dataframe saved to CSV")
        cleaned_data = main(path=FIXTURES_DIR / "eu_life_expectancy_input.tsv")
        pd.testing.assert_frame_equal(
            cleaned_data.reset_index(drop=True), pt_life_expectancy_expected
        )
