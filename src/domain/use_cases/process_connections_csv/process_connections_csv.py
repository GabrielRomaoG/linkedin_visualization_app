import pandas as pd
from src.utils.file_handler import get_file_name_from_path, compare_file_names
from src.utils.dataframe_utils import validate_dataframe_columns


class ConnectionsCsvProcessor:
    def __init__(self):
        self.__expected_csv_file = "Connections.csv"
        self.__interest_columns = [
            "URL",
            "Company",
            "Position",
            "Connected On",
        ]

    def process(self, file_path: str):
        self.__validate_file_name(file_path, self.__expected_csv_file)
        connections_df = self.__read_connections_csv(file_path)
        self.__validate_columns(connections_df)
        connections_df = connections_df[self.__interest_columns]
        connections_df = self.__set_data_types(connections_df)

        connections_df["user_name"] = (
            connections_df["URL"].str.split("/").str.get(-1).astype("string")
        )

        connections_df = connections_df.drop(columns=["URL"])
        return connections_df

    @classmethod
    def __read_connections_csv(self, file_path: str):
        connections_df = pd.read_csv(file_path, skiprows=range(0, 3))
        return connections_df

    @classmethod
    def __validate_columns(cls, connections_df: pd.DataFrame):
        expected_columns = [
            "First Name",
            "Last Name",
            "Company",
            "URL",
            "Email Address",
            "Position",
            "Connected On",
        ]
        validate_dataframe_columns(connections_df, expected_columns)

    @classmethod
    def __validate_file_name(cls, file_path: str, interest_file_name: str) -> None:
        file_name = get_file_name_from_path(file_path)
        compare_file_names(file_name, interest_file_name)

    @classmethod
    def __set_data_types(cls, connections_df: pd.DataFrame):
        str_columns = ["Company", "Position"]
        for col in str_columns:
            connections_df[col] = connections_df[col].astype("string")

        connections_df["Connected On"] = pd.to_datetime(
            connections_df["Connected On"], format="%d %b %Y"
        )
        return connections_df
