from inspect import getsourcefile
from os import path
import argparse
import pandas as pd


def clean_data(country_code: str = 'PT') -> None:
    """Clean life expectancy data and save it to a CSV file for a specific
    country.

    Loads the 'eu_life_expectancy_raw.tsv' data file from the 'data' folder,
    transforms it from wide format to long format, and filters the data to
    include only rows with the specified 'country_code' in the 'region' column.
    The resulting data frame has the following columns: 'unit', 'sex', 'age',
    'region', 'year', and 'value'. The 'year' column is converted to integers,
    and the 'value' column is converted to floating-point numbers. The cleaned
    data is saved to a CSV file named 'pt_life_expectancy.csv' in the 'data'
    folder.

    :param country_code: The ISO 3166-1 alpha-2 country code to filter data
    by. Defaults to 'PT' (Portugal).
    :type country_code: str :return: None
    :rtype: None :raises FileNotFoundError: If the
    'eu_life_expectancy_raw.tsv' file cannot be found.
    """
    # Load data
    data: pd.DataFrame = pd.read_csv(
        path.join(
            path.dirname(path.abspath(getsourcefile(lambda: 0))),
            "data",
            "eu_life_expectancy_raw.tsv"
        ),
        sep="\t",
        header=0
    )

    # From wide to long
    # Split mixed column
    spliced_data = data['unit,sex,age,geo\\time'].str.split(',', expand=True)
    spliced_data.columns = ['unit', 'sex', 'age', 'region']
    data = spliced_data.join(data.iloc[:, 1:].set_axis(spliced_data.index))
    # Actual wide 2 long
    data = pd.melt(
        frame=data,
        id_vars=["unit", "sex", "age", "region"],
        var_name="year", value_name="value"
    )

    # Clean year
    data['year'] = pd.to_numeric(data['year'], errors="coerce")
    data = data.dropna(subset=["year"])

    # Clean value
    numeric_pattern = r'(\d+\.\d+|\d+)'
    numeric_values = data["value"].str.extract(numeric_pattern, expand=False)
    data['value'] = pd.to_numeric(numeric_values, downcast="float",
                                  errors="coerce")
    data = data.dropna(subset=["value"])

    # Select PT
    data = data[data['region'].str.upper() == country_code]

    # Save data
    data.to_csv(
        path.join(
            path.dirname(path.abspath(getsourcefile(lambda: 0))),
            "data",
            "pt_life_expectancy.csv"
        ),
        index=False
    )


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description='Clean life expectancy data.')
    parser.add_argument(
        '--country',
        type=str, default='PT',
        help='Country code to filter data'
    )
    args = parser.parse_args()

    clean_data(args.country)
