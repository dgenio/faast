import argparse

import pandas as pd

from life_expectancy.loading_strategies import DataLoader, save_data, Region
from life_expectancy.transformation_interface import (
    ConvertValueToNumericTransformation, ConvertYearToNumericTransformation,
    DropMissingValuesTransformation, RenameColumnsTransformation,
    SelectCountryTransformation, TransformationPipeline,
    WideToLongTransformation)


def main(file_path: str, country_code: Region = Region.PT) -> pd.DataFrame:
    # Load the data using the appropriate strategy
    raw_data = DataLoader.load_data(file_path=file_path)

    transformations = [
        RenameColumnsTransformation({
            'life_expectancy': 'value',
            'country': 'region'
        }),
        WideToLongTransformation(),
        SelectCountryTransformation(
            country_code=country_code
        ),
        ConvertYearToNumericTransformation(),
        ConvertValueToNumericTransformation(),
        DropMissingValuesTransformation(
            columns=['year', 'value']
        )
    ]

    # Define the transformation pipeline
    pipeline = TransformationPipeline()
    for transformation in transformations:
        pipeline.add_transformation(transformation)

    # Apply the transformations
    cleaned_data = pipeline.transform(raw_data)
    save_data(data=cleaned_data)

    return cleaned_data


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description='Clean life expectancy data.')
    parser.add_argument(
        '--country',
        type=str, default='PT',
        help='Country code to filter data'
    )
    args = parser.parse_args()

    # Convert the country code string to the corresponding Region enum value
    country_code = Region(args.country.upper())

    main(country_code=country_code)
