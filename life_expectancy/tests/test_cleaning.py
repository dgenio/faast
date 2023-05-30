"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import main
from . import OUTPUT_DIR, FIXTURES_DIR


def test_main(pt_life_expectancy_expected, life_expectancy_data):
    """Run the `main` function and compare the output to the expected output"""
    main(path=FIXTURES_DIR / "eu_life_expectancy_input.tsv")
    pt_life_expectancy_actual = pd.read_csv(
        OUTPUT_DIR / "pt_life_expectancy.csv"
    )
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )
