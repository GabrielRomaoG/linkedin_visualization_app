import pandas as pd


def validate_dataframe_columns(dataframe: pd.DataFrame, expected_columns: list) -> None:
    if not set(expected_columns) == set(dataframe.columns):
        raise ValueError("DataFrame does not contain all expected columns")
