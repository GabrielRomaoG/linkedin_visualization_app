import csv
import datetime
import logging
from src.utils.file_handler import get_file_name_from_path, compare_file_names
from .iprocess_connections_csv import IConnectionsCsvProcessor
from src.domain.models.connection import Connection
from src.infra.db.repositories.connections_repository import ConnectionsRepository


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
            expected_columns = [
                "First Name",
                "Last Name",
                "Company",
                "URL",
                "Email Address",
                "Position",
                "Connected On",
            ]
            with self.__open_file(file_path, "r") as connections_csv:
                reader = csv.reader(connections_csv)
                is_valid_connections_csv = False
                for index, row in enumerate(reader):
                    if (
                        sorted(row) == sorted(expected_columns)
                        and not is_valid_connections_csv
                    ):
                        is_valid_connections_csv = True
                        column_names = row
                        continue

                    if index == 5 and not is_valid_connections_csv:
                        break

                    if is_valid_connections_csv:
                        user_name = self.__get_user_name_from_url(
                            row[column_names.index("URL")]
                        )
                        connected_on_date = self.__set_connected_on_to_date_type(
                            row[column_names.index("Connected On")]
                        )
                        connection_model = Connection(
                            user_name=user_name,
                            company=row[column_names.index("Company")],
                            position=row[column_names.index("Position")],
                            connected_on=connected_on_date,
                        )
                        self.__connections_repository.insert_connection(
                            connection_model
                        )
                if not is_valid_connections_csv:
                    raise ValueError("Connections.csv doesn't has the expected columns")

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

    @classmethod
    def __get_user_name_from_url(cls, url: str) -> str:
        return url.split("/")[-1]

    @classmethod
    def __set_connected_on_to_date_type(cls, connected_on: str) -> datetime.date:
        return datetime.datetime.strptime(connected_on, "%d %b %Y").date()
