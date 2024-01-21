import pandas as pd
from src.utils.file_handler import get_file_name_from_path, compare_file_names
from src.utils.dataframe_utils import validate_dataframe_columns


class ConnectionsCsvProcessor:
    def __init__(self, read_csv_func=pd.read_csv):
        self.__expected_csv_file = "Connections.csv"
        self.__read_csv_func = read_csv_func

    def process(self, file_path: str):
        self.__validate_file_name(file_path, self.__expected_csv_file)
        connections_df = self.__read_connections_csv(file_path)
        self.__validate_columns(connections_df)
        connections_df = self.__set_data_types(connections_df)
        connections_df = self.__create_user_name_column(connections_df)
        connections_df = self.__select_interest_columns(connections_df)
        return connections_df

    @classmethod
    def __validate_file_name(cls, file_path: str, interest_file_name: str) -> None:
        file_name = get_file_name_from_path(file_path)
        compare_file_names(file_name, interest_file_name)

    def __read_connections_csv(self, file_path: str):
        connections_df = self.__read_csv_func(file_path, skiprows=range(0, 3))
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

    def __select_interest_columns(self, connections_df: pd.DataFrame) -> pd.DataFrame:
        interest_columns = ["user_name", "Company", "Position", "Connected On"]
        return connections_df[interest_columns]

    @classmethod
    def __set_data_types(cls, connections_df: pd.DataFrame):
        connections_df = connections_df.astype(
            {
                "Company": "string",
                "Position": "string",
            }
        )
        connections_df["Connected On"] = pd.to_datetime(
            connections_df["Connected On"], format="%d %b %Y"
        )
        return connections_df

    @classmethod
    def __create_user_name_column(cls, connections_df: pd.DataFrame) -> pd.DataFrame:
        connections_df["user_name"] = (
            connections_df["URL"].str.split("/").str.get(-1).astype("string")
        )
        return connections_df
