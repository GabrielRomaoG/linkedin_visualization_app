from abc import ABC, abstractmethod


class IConnectionsCsvProcessor(ABC):
    """
    Process the Connections.csv data
    """

    @abstractmethod
    def process(self, file_path: str):
        """
        Read the Connections.csv file, treat the data and save in the database.

        Args:
        file_path (str): The path to the connections CSV file.
        """
