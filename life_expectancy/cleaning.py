import pandas as pd


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

    # Select rows corresponding to specified country_code
    selected_data: pd.DataFrame = spliced_data[
        spliced_data['region'].str.upper() == country_code.upper()
        ]

    # Transform spliced_data to long format
    long_data: pd.DataFrame = pd.melt(
        frame=selected_data,
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

    return long_data
