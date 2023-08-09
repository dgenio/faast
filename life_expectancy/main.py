import argparse
import pandas as pd
from cleaning import clean_data
from data_load_save import DataLoader, save_data


def main(
        country_code: str = 'PT',
        path: str = None
) -> pd.DataFrame:
    """
    Calls load data, clean data and save data
    :param country_code: A string representing the country code of the country
    to be selected.
    :param path: path to file to load.
    :return: Cleaned data frame
    """
    long_data = DataLoader.load_data(path=path)
    cleaned_data = clean_data(
        long_data=long_data,
        country_code=country_code)
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

    main(country_code=args.country)
