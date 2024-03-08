import csv
import datetime
from io import TextIOWrapper
import logging
from src.utils.file_handler import get_file_name_from_path, compare_file_names
from src.domain.use_cases.process_shares_csv.iprocess_shares_csv import (
    ISharesCsvProcessor,
)
from src.domain.models.shares import Share
from src.infra.db.repositories.shares.shares_repository import (
    SharesRepository,
)


class SharesCsvProcessor(ISharesCsvProcessor):
    def __init__(
        self,
        shares_repository=SharesRepository,
        open_file_func=open,
    ):
        self.__shares_repository = shares_repository
        self.__open_file = open_file_func

    def process(self, file_path: str) -> dict:
        try:
            expected_csv_file = "Shares.csv"
            self.__validate_file_name(file_path, expected_csv_file)
            with self.__open_file(file_path, "r") as shares_csv:
                self.__validate_csv(shares_csv)
                reader = csv.reader(shares_csv)
                headers = self.__headers
                shares_model_list = list()
                for index, row in enumerate(reader):
                    share_link = row[headers.index("ShareLink")]
                    if not share_link:
                        logging.warning(
                            f"The ShareLink in the row {index} of the table is empty, so it will not be processed."
                        )
                        continue
                    shared_date = self.__set_date_str_to_date_type(
                        row[headers.index("Date")]
                    )
                    share_model = Share(
                        share_link=share_link,
                        shared_date=shared_date,
                        num_of_comments=10,  # must implement scrap method
                        num_of_likes=40,  # must implement scrap method
                    )
                    shares_model_list.append(share_model)
                self.__shares_repository().bulk_insert_shares(shares_model_list)

        except Exception as e_info:
            logging.error(
                "Error processing the Shares.csv file: %s",
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
            "Date",
            "ShareLink",
            "ShareCommentary",
            "SharedURL",
            "MediaURL",
            "Visibility",
        ]
        for index, line in enumerate(file_content):
            line = line.strip().split(",")
            if sorted(line) == sorted(expected_columns):
                self.__headers = line
                return
            if index == 5:
                break
        raise ValueError("Shares.csv doesn't have the expected columns")

    @staticmethod
    def __set_date_str_to_date_type(date_str: str) -> datetime.date:
        """
        Converts a string representation of a date and time to a `datetime.date` object.

        This static method is designed to convert a string in the format YYYY-MM-DD HH:MM:SS
        to a `datetime.date` object, discarding the time portion.

        Args:
            date_str (str): The string representation of the date and time.
                The expected format is YYYY-MM-DD HH:MM:SS.

        Returns:
            datetime.date: The parsed date object, with the time portion discarded.
        """
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
