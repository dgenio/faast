from inspect import getsourcefile
from os.path import dirname, abspath, join, splitext
import pandas as pd
from abc import ABC, abstractmethod
from cleaning import wide_to_long_format


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


class LoadStrategy(ABC):
    @abstractmethod
    def load_data(self, file_path: str = None) -> pd.DataFrame:
        """Load data from file and ensure common strucutre ( long )

        Args:
            file_path (str, optional): _description_. Defaults to None.

        Returns:
            pd.DataFrame: _description_
        """


class TSVLoadStrategy(LoadStrategy):
    def load_data(self, file_path: str = None) -> pd.DataFrame:
        # Ensure path
        if file_path is None:
            file_path = join(
                __get_current_directory_full_path(),
                "data",
                "eu_life_expectancy_raw.tsv"
            )
        # Load data
        raw_data: pd.DataFrame = pd.read_csv(
            file_path,
            sep="\t",
            header=0
        )

        long_data = wide_to_long_format(wide_data=raw_data)

        return long_data


class JSONLoadStrategy(LoadStrategy):
    def load_data(self, file_path: str = None) -> pd.DataFrame:
        # Ensure path
        if file_path is None:
            file_path = join(
                __get_current_directory_full_path(),
                "data",
                "eurostat_life_expect.json"
            )
        # Load data
        raw_data: pd.DataFrame = pd.read_json(file_path)
        return raw_data


class DataLoader:
    @staticmethod
    def load_data(file_path: str) -> pd.DataFrame:
        if not file_path:
            raise ValueError("Input file not specified")
        file_name, file_extension = splitext(file_path)
        if file_extension == ".tsv":
            load_strategy = TSVLoadStrategy()
        elif file_extension == ".json":
            load_strategy = JSONLoadStrategy()
        else:
            raise ValueError("File format not supported")
        return load_strategy.load_data(file_path=file_path)


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
