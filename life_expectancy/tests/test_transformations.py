import os
import unittest

import pandas as pd

from life_expectancy.loading_strategies import get_current_directory_full_path
from life_expectancy.region import Region
from life_expectancy.main import main
from life_expectancy.transformation_interface import (
    ConvertValueToNumericTransformation, ConvertYearToNumericTransformation,
    DropMissingValuesTransformation, RenameColumnsTransformation,
    SelectCountryTransformation, WideToLongTransformation)


class TestTransformations(unittest.TestCase):
    def test_wide_to_long_transformation(self):
        data = pd.DataFrame({
            'unit,sex,age,geo\\time': ['YR,F,Y65,PT'],
            '2021': [100]
        })
        transformation = WideToLongTransformation()
        transformed_data = transformation.transform(data)
        self.assertEqual(transformed_data['year'].iloc[0], '2021')
        self.assertEqual(transformed_data['value'].iloc[0], 100)

    def test_rename_columns_transformation(self):
        data = pd.DataFrame({
            'life_expectancy': [100],
            'country': ['PT']
        })
        transformation = RenameColumnsTransformation({
            'life_expectancy': 'value',
            'country': 'region'
        })
        transformed_data = transformation.transform(data)
        self.assertIn('value', transformed_data.columns)
        self.assertIn('region', transformed_data.columns)

    def test_select_country_transformation(self):
        data = pd.DataFrame({
            'region': ['PT', 'US'],
            'value': [100, 200]
        })
        transformation = SelectCountryTransformation(country_code=Region.PT)
        transformed_data = transformation.transform(data)
        self.assertEqual(len(transformed_data), 1)
        self.assertEqual(transformed_data['region'].iloc[0], 'PT')

    def test_convert_year_to_numeric_transformation(self):
        data = pd.DataFrame({
            'year': ['2021']
        })
        transformation = ConvertYearToNumericTransformation()
        transformed_data = transformation.transform(data)
        self.assertEqual(transformed_data['year'].dtype, 'int64')

    def test_convert_value_to_numeric_transformation(self):
        data = pd.DataFrame({
            'value': ['100.5']
        })
        transformation = ConvertValueToNumericTransformation()
        transformed_data = transformation.transform(data)
        self.assertEqual(transformed_data['value'].dtype, 'float64')

    def test_drop_missing_values_transformation(self):
        data = pd.DataFrame({
            'year': [2021, None],
            'value': [100, None]
        })
        transformation = DropMissingValuesTransformation(
            columns=['year', 'value']
        )
        transformed_data = transformation.transform(data)
        self.assertEqual(len(transformed_data), 1)

    def test_end_to_end_pipeline_with_json(self):
        # Assuming the JSON file is in the correct format and path
        file_path = os.path.join(
            get_current_directory_full_path(),
            'data',
            'eurostat_life_expect.json'
        )
        cleaned_data = main(file_path=file_path, country_code=Region.PT)
        # Add assertions based on the expected structure and content of the
        # cleaned data
        self.assertIn('year', cleaned_data.columns)
        self.assertIn('value', cleaned_data.columns)
        self.assertNotIn('life_expectancy', cleaned_data.columns)
        self.assertNotIn('country', cleaned_data.columns)
        self.assertEqual(cleaned_data['region'].iloc[0], 'PT')


if __name__ == '__main__':
    unittest.main()
