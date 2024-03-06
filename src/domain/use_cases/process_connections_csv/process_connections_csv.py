import csv
import datetime
from io import TextIOWrapper
import logging
from src.utils.file_handler import get_file_name_from_path, compare_file_names
from .iprocess_connections_csv import IConnectionsCsvProcessor
from src.domain.models.connection import Connection
from src.infra.db.repositories.connections.connections_repository import (
    ConnectionsRepository,
)


class ConnectionsCsvProcessor(IConnectionsCsvProcessor):
    def __init__(
        self,
        connections_repository=ConnectionsRepository,
        open_file_func=open,
    ):
        self.__connections_repository = connections_repository
        self.__open_file = open_file_func

    def process(self, file_path: str) -> dict:
        try:
            expected_csv_file = "Connections.csv"
            self.__validate_file_name(file_path, expected_csv_file)
            with self.__open_file(file_path, "r") as connections_csv:
                self.__validate_csv(connections_csv)
                reader = csv.reader(connections_csv)
                headers = self.__headers
                connections_model_list = list()
                for index, row in enumerate(reader):
                    url = row[headers.index("URL")]
                    if not url:
                        logging.warning(
                            f"The URL in the row {index} of the table is empty, so it will not be processed."
                        )
                        continue
                    user_name = self.__get_user_name_from_url(url)
                    connected_on_date = self.__set_connected_on_to_date_type(
                        row[headers.index("Connected On")]
                    )
                    connection_model = Connection(
                        user_name=user_name,
                        company=row[headers.index("Company")],
                        position=row[headers.index("Position")],
                        connected_on=connected_on_date,
                    )
                    connections_model_list.append(connection_model)
                self.__connections_repository().bulk_insert_connections(
                    connections_model_list
                )

        except Exception as e_info:
            logging.error(
                "Error processing the Connections.csv file: %s",
                e_info,
                exc_info=True,
            )
            raise e_info

    @classmethod
    def __validate_file_name(cls, file_path: str, interest_file_name: str) -> None:
        file_name = get_file_name_from_path(file_path)
        compare_file_names(file_name, interest_file_name)

    def __validate_csv(self, file_content: TextIOWrapper) -> None:
        expected_columns = [
            "First Name",
            "Last Name",
            "URL",
            "Email Address",
            "Company",
            "Position",
            "Connected On",
        ]
        for index, line in enumerate(file_content):
            line = line.strip().split(",")
            if sorted(line) == sorted(expected_columns):
                self.__headers = line
                return
            if index == 5:
                break
        raise ValueError("Connections.csv doesn't have the expected columns")

    @classmethod
    def __get_user_name_from_url(cls, url: str) -> str:
        return url.split("/")[-1]

    @classmethod
    def __set_connected_on_to_date_type(cls, connected_on: str) -> datetime.date:
        return datetime.datetime.strptime(connected_on, "%d %b %Y").date()
