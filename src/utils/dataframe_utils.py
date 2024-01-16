import pandas as pd


def validate_dataframe_columns(dataframe: pd.DataFrame, expected_columns: list) -> None:
    if not all(col in dataframe.columns for col in expected_columns):
        raise ValueError("DataFrame does not contain all expected columns")
