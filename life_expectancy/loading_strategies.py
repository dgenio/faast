from abc import ABC, abstractmethod
import pandas as pd
from os.path import dirname, abspath, join, splitext
from inspect import getsourcefile


class LoadStrategy(ABC):
    @abstractmethod
    def load_data(self, file_path: str = None) -> pd.DataFrame:
        """Load data from file
        """


class TSVLoadStrategy(LoadStrategy):
    def load_data(self, file_path: str = None) -> pd.DataFrame:
        # Ensure path
        if file_path is None:
            file_path = join(
                get_current_directory_full_path(),
                "data",
                "eu_life_expectancy_raw.tsv"
            )
        # Load data
        raw_data: pd.DataFrame = pd.read_csv(
            file_path,
            sep="\t",
            header=0
        )

        return raw_data


class JSONLoadStrategy(LoadStrategy):
    def load_data(self, file_path: str = None) -> pd.DataFrame:
        # Ensure path
        if file_path is None:
            file_path = join(
                get_current_directory_full_path(),
                "data",
                "eurostat_life_expect.json"
            )
        # Load data
        raw_data: pd.DataFrame = pd.read_json(file_path)

        return raw_data


class LoadStrategyFactory:
    @staticmethod
    def create_strategy(file_extension: str) -> LoadStrategy:
        strategies = {
            ".tsv": TSVLoadStrategy,
            ".json": JSONLoadStrategy
        }
        strategy = strategies.get(file_extension)
        if strategy is None:
            raise ValueError(f"File format {file_extension} not supported")
        return strategy()


class DataLoader:
    @staticmethod
    def load_data(file_path: str) -> pd.DataFrame:
        if not file_path:
            raise ValueError("Input file not specified")
        _, file_extension = splitext(file_path)
        load_strategy = LoadStrategyFactory.create_strategy(file_extension)
        return load_strategy.load_data(file_path=file_path)


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


def get_file_extension(file_path: str) -> str:
    _, file_extension = splitext(file_path)
    return file_extension


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
