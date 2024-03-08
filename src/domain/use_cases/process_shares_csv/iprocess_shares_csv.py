from abc import ABC, abstractmethod


class ISharesCsvProcessor(ABC):
    """
    Process the Shares.csv data
    """

    @abstractmethod
    def process(self, file_path: str):
        pass

    """
    Read the Shares.csv file, treat the data and save in the database.

    Args:
    file_path (str): The path to the shares CSV file.
    """
