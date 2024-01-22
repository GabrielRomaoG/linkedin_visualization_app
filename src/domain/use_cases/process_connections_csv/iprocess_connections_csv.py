from abc import ABC, abstractmethod


class IConnectionsCsvProcessor(ABC):
    """
    Process the Connections.csv data
    """

    @abstractmethod
    def process(self, file_path: str):
        """
        Process the connections CSV file and return a pandas DataFrame.

        Args:
        file_path (str): The path to the connections CSV file.

        Returns:
        pd.DataFrame: The processed connections data as a pandas DataFrame.
        """
