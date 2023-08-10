from abc import ABC, abstractmethod
import pandas as pd


class Transformation(ABC):
    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform the input data and return the transformed data."""

    def is_necessary(self, data: pd.DataFrame) -> bool:
        """Test if transformation is necessry"""
        return True


class TransformationPipeline:
    def __init__(self):
        self.transformations = []

    def add_transformation(self, transformation: Transformation):
        self.transformations.append(transformation)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        for transformation in self.transformations:
            if transformation.is_necessary(data):
                data = transformation.transform(data)
        return data


class WideToLongTransformation(Transformation):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        # Convert from wide to long format
        # Split mixed column into separate columns
        spliced_columns: pd.DataFrame = data[
            'unit,sex,age,geo\\time'
        ].str.split(
            ',',
            expand=True
        )
        spliced_columns.columns = ['unit', 'sex', 'age', 'region']
        spliced_data: pd.DataFrame = pd.concat(
            [spliced_columns, data.iloc[:, 1:]],
            axis=1
        )

        # Transform spliced_data to long format
        long_data: pd.DataFrame = pd.melt(
            frame=spliced_data,
            id_vars=["unit", "sex", "age", "region"],
            var_name="year",
            value_name="value"
        )

        return long_data

    def is_necessary(self, data: pd.DataFrame) -> bool:
        return 'unit,sex,age,geo\\time' in data.columns


class RenameColumnsTransformation(Transformation):
    def __init__(self, column_mapping: dict):
        self.column_mapping = column_mapping

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        # Rename columns according to the mapping
        return data.rename(columns=self.column_mapping)

    def is_necessary(self, data: pd.DataFrame) -> bool:
        return any(col in data.columns for col in self.column_mapping.keys())


class SelectCountryTransformation(Transformation):
    def __init__(self, country_code: str = 'PT'):
        self.country_code = country_code

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        return data[data['region'].str.upper() == self.country_code.upper()]


class ConvertYearToNumericTransformation(Transformation):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        data.loc[:, 'year'] = pd.to_numeric(data['year'], errors="coerce")
        return data

    def is_necessary(self, data: pd.DataFrame) -> bool:
        return data['year'].dtype != 'int64'


class ConvertValueToNumericTransformation(Transformation):
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        numeric_pattern = r'(\d+\.\d+|\d+)'
        numeric_values = data["value"].str.extract(
            numeric_pattern,
            expand=False
        )
        data['value'] = pd.to_numeric(
            numeric_values,
            downcast="float",
            errors="coerce"
        )
        return data

    def is_necessary(self, data: pd.DataFrame) -> bool:
        return data['value'].dtype != 'float64'


class DropMissingValuesTransformation(Transformation):
    def __init__(self, columns: list):
        self.columns = columns

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.dropna(subset=self.columns)
