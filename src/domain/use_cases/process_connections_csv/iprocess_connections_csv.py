from abc import ABC, abstractmethod
from src.domain.models.connection import Connection


class IConnectionsCsvProcessor(ABC):
    """
    Process the Connections.csv data
    """

    @abstractmethod
    def process(self, file_path: str) -> list[Connection]:
        """
        Read the Connections.csv file, treat the data and save in the database.

        Args:
        file_path (str): The path to the connections CSV file.
        """
