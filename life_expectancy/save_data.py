import pandas as pd
from os.path import join
from life_expectancy.loading_strategies import get_current_directory_full_path


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
