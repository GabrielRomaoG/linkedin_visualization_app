from abc import ABC, abstractmethod


class LinkedinCsvDataExtractor(ABC):
    @abstractmethod
    def extract(self, zip_path: str, destine_folder: str):
        """
        Extracts specific files from a zip to a destination folder.

        Args:
        - zip_path (str): Path to the zip file.
        - destine_folder (str): Path to the destination folder.
        """
