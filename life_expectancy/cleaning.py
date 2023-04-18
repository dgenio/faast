from inspect import getsourcefile
from os.path import dirname, abspath, join
import argparse
import pandas as pd


def get_current_directory_full_path() -> str:
    """
    Returns the absolute path of the directory containing the current 
    Python file.
    :return: A string representing the absolute path of the directory 
    containing the current Python file.
    """
    current_file_path: str = abspath(getsourcefile(lambda: 0))
    current_dir_path: str = dirname(current_file_path)

    return current_dir_path


def load_data() -> pd.DataFrame:
    """
    Loads the 'eu_life_expectancy_raw.tsv' data file from the 'data' folder
    :return: Pandas dataframe with data
    :raises FileNotFoundError: If the 'eu_life_expectancy_raw.tsv' file cannot
     be found.
    """
    # Load data
    raw_data: pd.DataFrame = pd.read_csv(
        join(
            get_current_directory_full_path(),
            "data",
            "eu_life_expectancy_raw.tsv"
        ),
        sep="\t",
        header=0
    )
    return raw_data


def clean_data(
        wide_data: pd.DataFrame,
        country_code: str = 'PT',
) -> pd.DataFrame:
    """
    Cleans and transforms the input wide_data to a long format.

    The input raw_data should have the following columns:
    - unit,sex,age,geo\\time: A mixed column with the variables unit, sex, age,
     and region separated by commas.
    - One column for each year of data.

    The function performs the following steps:
    - Splits the mixed column into separate columns and sets them as the first
    columns of the data frame.
    - Transforms the raw_data from a wide format to a long format with columns
    'year' and 'value'.
    - Converts the 'year' and 'value' columns to numeric data types and drops
    rows with missing values.
    - Selects the rows corresponding to the specified country_code.

    :param wide_data: A pandas DataFrame containing the data to be cleaned and
    transformed.
    :param country_code: A string representing the country code of the country
    to be selected.
    :return: A pandas DataFrame containing the cleaned and transformed data.
    """
    # Split mixed column into separate columns
    spliced_columns: pd.DataFrame = wide_data[
        'unit,sex,age,geo\\time'
    ].str.split(
        ',',
        expand=True
    )
    spliced_columns.columns = ['unit', 'sex', 'age', 'region']
    spliced_data: pd.DataFrame = pd.concat(
        [spliced_columns, wide_data.iloc[:, 1:]],
        axis=1
    )

    # Transform spliced_data to long format
    long_data: pd.DataFrame = pd.melt(
        frame=spliced_data,
        id_vars=["unit", "sex", "age", "region"],
        var_name="year",
        value_name="value"
    )

    # Convert year to numeric data types and drop rows with missing values
    long_data['year'] = pd.to_numeric(
        long_data['year'],
        errors="coerce")
    long_data = long_data.dropna(subset=["year"])

    # Convert value columns to numeric data types and drop rows with missing
    # values
    numeric_pattern = r'(\d+\.\d+|\d+)'
    numeric_values: pd.Series = long_data["value"].str.extract(
        numeric_pattern,
        expand=False
    )
    long_data['value'] = pd.to_numeric(
        numeric_values,
        downcast="float",
        errors="coerce"
    )
    long_data = long_data.dropna(subset=["value"])

    # Select rows corresponding to specified country_code
    selected_data: pd.DataFrame = long_data[
        long_data['region'].str.upper() == country_code.upper()
    ]

    return selected_data


def save_data(data: pd.DataFrame) -> None:
    """
    Data is saved to a CSV file named 'pt_life_expectancy.csv' in the 'data'
    folder.
    :param data: 
    :return: 
    """
    data.to_csv(
        join(
            get_current_directory_full_path(),
            "data",
            "pt_life_expectancy.csv"
        ),
        index=False
    )


def main(country_code: str = 'PT') -> None:
    """
    Calls load data, clean data and save data
    :param country_code: A string representing the country code of the country
    to be selected.
    :return:
    """
    wide_data = load_data()
    cleaned_data = clean_data(
        wide_data=wide_data,
        country_code=country_code)
    save_data(data=cleaned_data)


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description='Clean life expectancy data.')
    parser.add_argument(
        '--country',
        type=str, default='PT',
        help='Country code to filter data'
    )
    args = parser.parse_args()

    main(country_code=args.country)
