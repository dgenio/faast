from inspect import getsourcefile
from os.path import dirname, abspath, join
import pandas as pd


def __get_current_directory_full_path() -> str:
    """
    Returns the absolute path of the directory containing the current
    Python file.
    :return: A string representing the absolute path of the directory
    containing the current Python file.
    """
    current_file_path: str = abspath(getsourcefile(lambda: 0))
    current_dir_path: str = dirname(current_file_path)

    return current_dir_path


def load_data(
        path: str = None
) -> pd.DataFrame:
    """
    Loads the 'eu_life_expectancy_raw.tsv' data file from the 'data' folder
    :param path: path to file to load.
    :return: Pandas dataframe with data
    :raises FileNotFoundError: If the 'eu_life_expectancy_raw.tsv' file cannot
     be found.
    """
    # Ensure path
    if path is None:
        path = join(
            __get_current_directory_full_path(),
            "data",
            "eu_life_expectancy_raw.tsv"
        )
    # Load data
    raw_data: pd.DataFrame = pd.read_csv(
        path,
        sep="\t",
        header=0
    )
    return raw_data


def save_data(data: pd.DataFrame) -> None:
    """
    Data is saved to a CSV file named 'pt_life_expectancy.csv' in the 'data'
    folder.
    :param data:
    :return:
    """
    data.to_csv(
        join(
            __get_current_directory_full_path(),
            "data",
            "pt_life_expectancy.csv"
        ),
        index=False
    )
